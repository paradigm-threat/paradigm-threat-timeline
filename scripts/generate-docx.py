#!/usr/bin/env python3
"""
Generate a Word document (.docx) from all content/*.md files -> export/timeline.docx

Uses python-docx for document generation and markdown-it-py for markdown parsing.
Images are embedded using Pillow for pre-processing.

Requirements:  pip install python-docx markdown-it-py Pillow
"""

import io
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------
try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    sys.exit("ERROR: pip install python-docx")

try:
    from markdown_it import MarkdownIt
except ImportError:
    sys.exit("ERROR: pip install markdown-it-py")

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: pip install Pillow")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR  = Path(__file__).resolve().parent
REPO_DIR    = SCRIPT_DIR.parent
CONTENT_DIR = REPO_DIR / "content"
EXPORT_DIR  = REPO_DIR / "export"
OUTPUT_DOCX = EXPORT_DIR / "timeline.docx"

with open(REPO_DIR / "package.json") as _f:
    PKG_VERSION = json.load(_f)["version"]

# ---------------------------------------------------------------------------
# Roman numerals & tier classifier (shared with generate-pdf.py logic)
# ---------------------------------------------------------------------------
_ROMAN = [
    "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
]

_NUM_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})")

def _classify_tier(filename: str):
    """Return (tier, xx, yy, zz) from an ``XX.YY.ZZ-slug.md`` filename."""
    m = _NUM_RE.match(filename)
    if not m:
        return ("part", "00", "00", "00")
    xx, yy, zz = m.group(1), m.group(2), m.group(3)
    if yy == "00" and zz == "00":
        return ("part", xx, yy, zz)
    if zz == "00":
        return ("chapter", xx, yy, zz)
    return ("subsection", xx, yy, zz)

# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
MAX_IMG_PX    = 1200
JPEG_QUALITY  = 82
MAX_IMG_IN    = 5.5    # max image width in inches (fits A4 with margins)

# ---------------------------------------------------------------------------
# Token attribute helper (markdown-it-py can use dict or list-of-tuples)
# ---------------------------------------------------------------------------
def _attr(tok, key: str, default: str = "") -> str:
    if tok.attrs is None:
        return default
    if isinstance(tok.attrs, dict):
        return tok.attrs.get(key, default)
    for k, v in tok.attrs:
        if k == key:
            return v
    return default

# ---------------------------------------------------------------------------
# Plain text extractor from inline token tree
# ---------------------------------------------------------------------------
def _plain(tok) -> str:
    parts = []
    if tok.children:
        for c in tok.children:
            if c.type in ("text", "code_inline"):
                parts.append(c.content)
            elif c.type == "softbreak":
                parts.append(" ")
            elif c.type == "hardbreak":
                parts.append("\n")
            elif c.children:
                parts.append(_plain(c))
    elif tok.content:
        parts.append(tok.content)
    return "".join(parts)

# ---------------------------------------------------------------------------
# Build a real TOC from the H1 heading of each markdown file
# ---------------------------------------------------------------------------
_H1_RE = re.compile(r'^#\s+(.+)', re.MULTILINE)

def _extract_h1(md_path: Path) -> str:
    text = md_path.read_text(encoding='utf-8')
    m = _H1_RE.search(text)
    return m.group(1).strip() if m else md_path.stem

def _add_toc(doc: Document, md_files: list):
    # Heading
    heading = doc.add_paragraph()
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hr = heading.add_run("Table of Contents")
    hr.bold = True
    hr.font.size = Pt(16)
    hr.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
    doc.add_paragraph()

    current_part = None
    chapter_counter = 0
    for i, path in enumerate(md_files):
        title = _extract_h1(path)
        tier, xx, yy, zz = _classify_tier(path.name)
        part_num = int(xx)
        roman = _ROMAN[part_num] if part_num < len(_ROMAN) else str(part_num)

        # Reset chapter counter when Part changes
        if xx != current_part:
            current_part = xx
            chapter_counter = 0

        if tier == "chapter":
            chapter_counter += 1

        # TOC entry paragraph — indent chapters and sub-sections
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(1)
        para.paragraph_format.space_after  = Pt(1)

        if tier == "part":
            # Extra spacing before each Part (except the very first)
            if i > 0:
                para.paragraph_format.space_before = Pt(10)
            para.paragraph_format.left_indent = Cm(0)

            # "Part V:  Title" — bold
            label_run = para.add_run(f"Part {roman}:  ")
            label_run.font.size      = Pt(10.5)
            label_run.bold           = True
            label_run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

            title_run = para.add_run(title)
            title_run.font.size      = Pt(10.5)
            title_run.bold           = True
            title_run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

        elif tier == "chapter":
            para.paragraph_format.left_indent = Cm(0.8)

            # "Chapter 3:  Title" — normal weight
            label_run = para.add_run(f"Chapter {chapter_counter}:  ")
            label_run.font.size      = Pt(10)
            label_run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

            title_run = para.add_run(title)
            title_run.font.size      = Pt(10)
            title_run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

        else:
            # Sub-section — italic, further indented
            para.paragraph_format.left_indent = Cm(1.4)

            title_run = para.add_run(title)
            title_run.font.size      = Pt(9.5)
            title_run.italic         = True
            title_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_page_break()

# ---------------------------------------------------------------------------
# DOCX Renderer
# ---------------------------------------------------------------------------
class DOCXRenderer:
    def __init__(self):
        self.doc = Document()
        self.md  = MarkdownIt("commonmark", {"typographer": False}).enable("table")
        self._img_cache: dict = {}
        self._chapter_counter = 0
        self._current_part_xx = None
        self._setup_styles()

    def _setup_styles(self):
        doc = self.doc

        # Page margins: 2.5 cm all sides
        for section in doc.sections:
            section.top_margin    = Cm(2.5)
            section.bottom_margin = Cm(2.5)
            section.left_margin   = Cm(2.5)
            section.right_margin  = Cm(2.5)

        # Body text default
        style = doc.styles["Normal"]
        style.font.name = "Calibri"
        style.font.size = Pt(11)
        style.paragraph_format.space_after = Pt(8)

        # Heading styles — reuse built-in Word heading styles for TOC compat
        h_specs = {
            "Heading 1": (18, True, RGBColor(0x1a, 0x1a, 0x1a)),
            "Heading 2": (14, True, RGBColor(0x2c, 0x2c, 0x2c)),
            "Heading 3": (12, True, RGBColor(0x3a, 0x3a, 0x3a)),
            "Heading 4": (11, True, RGBColor(0x4e, 0x4e, 0x4e)),
        }
        for sname, (sz, bold, clr) in h_specs.items():
            s = doc.styles[sname]
            s.font.name  = "Calibri"
            s.font.size  = Pt(sz)
            s.font.bold  = bold
            s.font.color.rgb = clr
            s.paragraph_format.space_before = Pt(14 if sz >= 16 else 10)
            s.paragraph_format.space_after  = Pt(4)

        # Quote style
        if "Quote" not in [s.name for s in doc.styles]:
            qs = doc.styles.add_style("Quote", WD_STYLE_TYPE.PARAGRAPH)
        else:
            qs = doc.styles["Quote"]
        qs.base_style = doc.styles["Normal"]
        qs.font.italic = True
        qs.font.size   = Pt(10.5)
        qs.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        qs.paragraph_format.left_indent  = Cm(1.2)
        qs.paragraph_format.space_before = Pt(6)
        qs.paragraph_format.space_after  = Pt(6)

        # Caption style
        if "Caption" not in [s.name for s in doc.styles]:
            cs = doc.styles.add_style("Caption", WD_STYLE_TYPE.PARAGRAPH)
        else:
            cs = doc.styles["Caption"]
        cs.base_style = doc.styles["Normal"]
        cs.font.italic = True
        cs.font.size   = Pt(9)
        cs.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        cs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cs.paragraph_format.space_before = Pt(2)
        cs.paragraph_format.space_after  = Pt(8)

    # ---------------------------------------------------------------
    #  Image handling
    # ---------------------------------------------------------------
    def _prepare_image(self, src: str):
        if src in self._img_cache:
            return self._img_cache[src]

        if src.startswith(("http://", "https://")):
            self._img_cache[src] = None
            return None

        rel = src.lstrip("/")
        abs_path = REPO_DIR / rel
        if not abs_path.is_file():
            print(f"    WARN image not found: {rel}", file=sys.stderr)
            self._img_cache[src] = None
            return None

        try:
            img = Image.open(abs_path)
            if img.width > MAX_IMG_PX:
                r = MAX_IMG_PX / img.width
                img = img.resize((MAX_IMG_PX, int(img.height * r)), Image.LANCZOS)

            if img.mode in ("RGBA", "P", "LA"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                img = bg
            elif img.mode != "RGB":
                img = img.convert("RGB")

            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
            buf.seek(0)

            # Compute display width in inches, respecting max
            orig_w_in = img.width / 96   # assume 96 dpi
            display_w = min(orig_w_in, MAX_IMG_IN)

            self._img_cache[src] = (buf, display_w)
            return self._img_cache[src]
        except Exception as exc:
            print(f"    WARN image failed ({rel}): {exc}", file=sys.stderr)
            self._img_cache[src] = None
            return None

    def _embed_image(self, src: str, caption: str = ""):
        result = self._prepare_image(src)
        if not result:
            return
        buf, width_in = result
        buf.seek(0)

        para = self.doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(buf, width=Inches(width_in))

        if caption:
            cp = self.doc.add_paragraph(style="Caption")
            cp.add_run(caption)

    # ---------------------------------------------------------------
    #  Inline run builder (bold / italic / code / link)
    # ---------------------------------------------------------------
    def _apply_inline(self, para, children):
        if not children:
            return
        bold = False
        italic = False
        link_text_parts: list = []
        link_href: str = ""
        in_link = False

        for tok in children:
            tp = tok.type

            if tp == "text":
                if in_link:
                    link_text_parts.append(tok.content)
                else:
                    run = para.add_run(tok.content)
                    run.bold   = bold
                    run.italic = italic

            elif tp == "softbreak":
                if in_link:
                    link_text_parts.append(" ")
                else:
                    run = para.add_run(" ")
                    run.bold = bold; run.italic = italic

            elif tp == "hardbreak":
                run = para.add_run("\n")

            elif tp == "code_inline":
                run = para.add_run(tok.content)
                run.font.name = "Courier New"
                run.font.size = Pt(10)

            elif tp == "strong_open":
                bold = True
            elif tp == "strong_close":
                bold = False
            elif tp == "em_open":
                italic = True
            elif tp == "em_close":
                italic = False

            elif tp == "link_open":
                link_href = _attr(tok, "href")
                link_text_parts = []
                in_link = True
            elif tp == "link_close":
                # Add link text as a coloured run (hyperlink XML is complex — plain text + color is cleaner)
                link_text = "".join(link_text_parts)
                run = para.add_run(link_text)
                run.bold   = bold
                run.italic = italic
                run.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)  # gold
                # Optionally embed actual hyperlink relationship
                try:
                    self._add_hyperlink(para, run, link_href)
                except Exception:
                    pass
                in_link = False
                link_text_parts = []

            elif tp == "image":
                # Inline image (e.g. inside a paragraph)
                isrc = _attr(tok, "src")
                ialt = _attr(tok, "alt") or tok.content or ""
                self._embed_image(isrc, ialt)

            elif tp == "html_inline":
                if "<br" in (tok.content or ""):
                    para.add_run("\n")

            else:
                if tok.children:
                    self._apply_inline(para, tok.children)
                elif tok.content:
                    run = para.add_run(tok.content)
                    run.bold = bold; run.italic = italic

    def _add_hyperlink(self, para, run, url: str):
        """Replace the last run with a proper Word hyperlink field."""
        # python-docx doesn't support adding hyperlinks to existing runs easily;
        # we add the relationship and mark the run with it
        part = para.part
        r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
        hyperlink = OxmlElement("w:hyperlink")
        hyperlink.set(qn("r:id"), r_id)
        hyperlink.append(run._r)
        para._p.append(hyperlink)

    # ---------------------------------------------------------------
    #  Block rendering
    # ---------------------------------------------------------------
    def _render_heading(self, level: int, inline_tok):
        text  = _plain(inline_tok)
        style = f"Heading {min(level, 4)}"
        para  = self.doc.add_paragraph(style=style)
        para.add_run(text)

    def _render_paragraph(self, inline_tok):
        if not inline_tok.children:
            if inline_tok.content:
                self.doc.add_paragraph(inline_tok.content)
            return

        # Pure image paragraph
        real = [c for c in inline_tok.children
                if c.type not in ("softbreak", "hardbreak")]
        if len(real) == 1 and real[0].type == "image":
            img = real[0]
            self._embed_image(_attr(img, "src"), _attr(img, "alt") or img.content or "")
            return

        # Image + caption pattern
        if (len(real) >= 2 and real[0].type == "image" and real[1].type == "em_open"):
            img = real[0]
            cap_parts = []
            for c in real[2:]:
                if c.type == "em_close": break
                if c.type == "text": cap_parts.append(c.content)
            caption = "".join(cap_parts) or _attr(img, "alt") or img.content or ""
            self._embed_image(_attr(img, "src"), caption)
            return

        para = self.doc.add_paragraph()
        self._apply_inline(para, inline_tok.children)

    def _render_blockquote(self, inner_tokens: list):
        # Collect text runs from nested tokens into quote paragraphs
        for tok in inner_tokens:
            if tok.type == "inline":
                para = self.doc.add_paragraph(style="Quote")
                self._apply_inline(para, tok.children)
            elif tok.type in ("paragraph_open", "paragraph_close",
                              "blockquote_open", "blockquote_close"):
                pass
            elif tok.type == "inline":
                para = self.doc.add_paragraph(style="Quote")
                self._apply_inline(para, tok.children)

    def _render_list(self, items: list, ordered: bool, depth: int = 0):
        word_style = "List Number" if ordered else "List Bullet"
        for item_tokens in items:
            # Flatten inline content from the list item
            for tok in item_tokens:
                if tok.type == "inline":
                    para = self.doc.add_paragraph(style=word_style)
                    if depth > 0:
                        para.paragraph_format.left_indent = Cm(depth * 1.0)
                    self._apply_inline(para, tok.children)
                elif tok.type == "bullet_list_open":
                    # nested list
                    pass

    def _render_table(self, header_row: list, body_rows: list):
        cols = len(header_row)
        if cols == 0:
            return
        table = self.doc.add_table(rows=1, cols=cols)
        table.style = "Table Grid"

        # Header
        hdr_cells = table.rows[0].cells
        for j, cell_tokens in enumerate(header_row):
            p = hdr_cells[j].paragraphs[0]
            for tok in cell_tokens:
                if tok.type == "inline":
                    for child in (tok.children or []):
                        run = p.add_run(child.content if child.content else "")
                        run.bold = True
            hdr_cells[j].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Body
        for row_cells in body_rows:
            row = table.add_row().cells
            for j, cell_tokens in enumerate(row_cells[:cols]):
                p = row[j].paragraphs[0]
                for tok in cell_tokens:
                    if tok.type == "inline":
                        self._apply_inline(p, tok.children or [])

        self.doc.add_paragraph()  # spacing after table

    def _render_code_block(self, content: str):
        # Use a shaded paragraph with monospace font
        para = self.doc.add_paragraph()
        para.paragraph_format.left_indent = Cm(1)
        run = para.add_run(content.rstrip())
        run.font.name = "Courier New"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
        # Light grey shading
        pPr = para._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  "F5F5F5")
        pPr.append(shd)

    # ---------------------------------------------------------------
    #  Token stream walker
    # ---------------------------------------------------------------
    def _render_tokens(self, tokens):
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            tp  = tok.type

            if tp == "heading_open":
                level = int(tok.tag[1]) if tok.tag else 2
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                if inline_tok and inline_tok.type == "inline":
                    self._render_heading(level, inline_tok)
                    i += 2  # skip heading_close
                else:
                    i += 1

            elif tp == "paragraph_open":
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                if inline_tok and inline_tok.type == "inline":
                    self._render_paragraph(inline_tok)
                    i += 2  # skip paragraph_close
                else:
                    i += 1

            elif tp == "blockquote_open":
                # collect until matching blockquote_close
                depth = 1
                j = i + 1
                while j < len(tokens) and depth > 0:
                    if tokens[j].type == "blockquote_open":  depth += 1
                    if tokens[j].type == "blockquote_close": depth -= 1
                    j += 1
                self._render_blockquote(tokens[i + 1: j - 1])
                i = j

            elif tp in ("bullet_list_open", "ordered_list_open"):
                ordered = tp == "ordered_list_open"
                depth_counter = 1
                j = i + 1
                items: list = []
                current_item: list = []
                while j < len(tokens):
                    jt = tokens[j].type
                    if jt in ("bullet_list_open", "ordered_list_open"):
                        depth_counter += 1
                    elif jt in ("bullet_list_close", "ordered_list_close"):
                        depth_counter -= 1
                        if depth_counter == 0:
                            if current_item:
                                items.append(current_item)
                            j += 1
                            break
                    elif jt == "list_item_open":
                        current_item = []
                    elif jt == "list_item_close":
                        items.append(current_item)
                        current_item = []
                    else:
                        current_item.append(tokens[j])
                    j += 1
                self._render_list(items, ordered)
                i = j

            elif tp == "fence" or tp == "code_block":
                self._render_code_block(tok.content)
                i += 1

            elif tp == "hr":
                para = self.doc.add_paragraph()
                pPr = para._p.get_or_add_pPr()
                pBdr = OxmlElement("w:pBdr")
                bottom = OxmlElement("w:bottom")
                bottom.set(qn("w:val"),   "single")
                bottom.set(qn("w:sz"),    "6")
                bottom.set(qn("w:space"), "1")
                bottom.set(qn("w:color"), "CCCCCC")
                pBdr.append(bottom)
                pPr.append(pBdr)
                i += 1

            elif tp == "table_open":
                # Collect header and body rows
                header_row: list = []
                body_rows:  list = []
                in_head = False
                in_body = False
                current_row: list = []
                current_cell: list = []
                j = i + 1
                while j < len(tokens) and tokens[j].type != "table_close":
                    tt = tokens[j].type
                    if tt == "thead_open":   in_head = True
                    elif tt == "thead_close": in_head = False
                    elif tt == "tbody_open":  in_body = True
                    elif tt == "tbody_close": in_body = False
                    elif tt == "tr_open":     current_row = []
                    elif tt == "tr_close":
                        if in_head: header_row = current_row
                        else:       body_rows.append(current_row)
                    elif tt in ("th_open", "td_open"): current_cell = []
                    elif tt in ("th_close", "td_close"):
                        current_row.append(current_cell)
                    else:
                        current_cell.append(tokens[j])
                    j += 1
                self._render_table(header_row, body_rows)
                i = j + 1  # skip table_close

            elif tp == "html_block":
                # Skip raw HTML blocks (iframes etc.)
                i += 1

            else:
                i += 1

    # ---------------------------------------------------------------
    #  Strip first H1 from a token stream
    # ---------------------------------------------------------------
    @staticmethod
    def _strip_first_h1(tokens: list) -> list:
        """Remove the first H1 heading (open + inline + close) from tokens."""
        out = []
        skipped = False
        i = 0
        while i < len(tokens):
            if (not skipped and tokens[i].type == "heading_open"
                    and tokens[i].tag == "h1"):
                skipped = True
                i += 1
                while i < len(tokens) and tokens[i].type != "heading_close":
                    i += 1
                i += 1
                continue
            out.append(tokens[i])
            i += 1
        return out

    # ---------------------------------------------------------------
    #  Heading-demoted token renderer (for sub-sections)
    # ---------------------------------------------------------------
    def _render_tokens_demoted(self, tokens, demote: int = 1):
        """Like _render_tokens but demotes heading levels by *demote*."""
        for tok in tokens:
            if tok.type == "heading_open" and tok.tag and tok.tag[0] == "h":
                old_level = int(tok.tag[1])
                new_level = min(old_level + demote, 6)
                tok.tag = f"h{new_level}"
        self._render_tokens(tokens)

    # ---------------------------------------------------------------
    #  Article entry point  (3-tier: Part / Chapter / Sub-section)
    # ---------------------------------------------------------------
    def render_article(self, md_path: Path):
        text   = md_path.read_text(encoding="utf-8")
        tokens = self.md.parse(text)

        tier, xx, yy, zz = _classify_tier(md_path.name)
        part_num = int(xx)
        roman = _ROMAN[part_num] if part_num < len(_ROMAN) else str(part_num)

        # Extract H1 for labelling
        h1_match = re.match(r"^#\s+(.+)", text, re.MULTILINE)
        h1_title = h1_match.group(1).strip() if h1_match else md_path.stem

        if tier == "part":
            # ── PART ──────────────────────────────────────────────
            self._current_part_xx = xx
            self._chapter_counter = 0

            # Part title heading
            h = self.doc.add_paragraph(style="Heading 1")
            run = h.add_run(f"Part {roman} — {h1_title}")
            run.bold = True

            tokens = self._strip_first_h1(tokens)
            self._render_tokens(tokens)
            self.doc.add_paragraph()

        elif tier == "chapter":
            # ── CHAPTER ───────────────────────────────────────────
            self._chapter_counter += 1
            ch_num = self._chapter_counter

            # Chapter heading
            h = self.doc.add_paragraph(style="Heading 2")
            run = h.add_run(f"Chapter {ch_num}: {h1_title}")
            run.bold = True

            tokens = self._strip_first_h1(tokens)
            self._render_tokens(tokens)
            self.doc.add_paragraph()

        else:
            # ── SUB-SECTION ───────────────────────────────────────
            # Horizontal rule separator (not a page break)
            para = self.doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = para.add_run("— ✦ —")
            r.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)
            r.font.size = Pt(12)

            tokens = self._strip_first_h1(tokens)
            self._render_tokens_demoted(tokens, demote=1)
            self.doc.add_paragraph()

    # ---------------------------------------------------------------
    #  Main driver
    # ---------------------------------------------------------------
    def generate(self):
        EXPORT_DIR.mkdir(exist_ok=True)
        md_files = sorted(CONTENT_DIR.rglob("*.md"))
        if not md_files:
            sys.exit("No markdown files in content/")

        n = len(md_files)
        print(f"Generating DOCX from {n} content files ...")

        # ---- Title page ----
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        title_para = self.doc.add_paragraph()
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title_para.add_run("Paradigm Threat:")
        run.bold      = True
        run.font.size = Pt(36)
        run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
        sub_para = self.doc.add_paragraph()
        sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sr = sub_para.add_run("The Third Story")
        sr.bold      = True
        sr.font.size = Pt(28)
        sr.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)
        self.doc.add_paragraph()
        desc_para = self.doc.add_paragraph()
        desc_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        desc_run = desc_para.add_run(
            "A cross-chronology investigation challenging the official timeline of Earth history \u2014 "
            "Scaligerian, Fomenko\u2019s New Chronology, Saturnian Cosmology, and indigenous traditions."
        )
        desc_run.font.size      = Pt(11)
        desc_run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        ver_para = self.doc.add_paragraph()
        ver_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        vr = ver_para.add_run(f"Version {PKG_VERSION}")
        vr.font.size      = Pt(12)
        vr.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        self.doc.add_page_break()

        # ---- Table of Contents ----
        _add_toc(self.doc, md_files)

        # ---- Articles ----
        for i, p in enumerate(md_files):
            print(f"  [{i + 1:3d}/{n}] {p.name}")

            # Page break before article — but NOT before sub-sections
            tier, xx, yy, zz = _classify_tier(p.name)
            if i > 0 and tier != "subsection":
                self.doc.add_page_break()

            self.render_article(p)

        print(f"Writing -> {OUTPUT_DOCX}")
        self.doc.save(str(OUTPUT_DOCX))
        kb = OUTPUT_DOCX.stat().st_size / 1024
        print(f"Done.  {kb:.0f} KB")


# ---------------------------------------------------------------------------
def main():
    renderer = DOCXRenderer()
    renderer.generate()


if __name__ == "__main__":
    main()
