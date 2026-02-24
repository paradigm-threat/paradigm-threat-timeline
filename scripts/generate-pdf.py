#!/usr/bin/env python3
"""
Generate a native PDF from all content/*.md files -> export/timeline.pdf

Uses fpdf2 for direct PDF generation — no HTML/CSS intermediate step.
Markdown is parsed with markdown-it-py and rendered directly to PDF primitives.
Images are resized with Pillow and embedded as native JPEG streams.

Requirements:  pip install fpdf2 markdown-it-py Pillow
"""

import io
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------
try:
    from fpdf import FPDF
except ImportError:
    sys.exit("ERROR: pip install fpdf2")

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
OUTPUT_PDF  = EXPORT_DIR / "timeline.pdf"

with open(REPO_DIR / "package.json") as _f:
    PKG_VERSION = json.load(_f)["version"]

# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
MAX_IMG_PX   = 1200          # max width in pixels before resize
JPEG_QUALITY = 72
MAX_IMG_W_MM = 170           # max image width in PDF (mm)
MAX_IMG_H_MM = 90            # max image height in PDF (mm)

# ---------------------------------------------------------------------------
# Colours  (R, G, B)
# ---------------------------------------------------------------------------
C_BLACK   = (26, 26, 26)
C_DARK    = (17, 17, 17)
C_H2      = (44, 44, 44)
C_H3      = (58, 58, 58)
C_GOLD    = (184, 134, 11)
C_GRAY    = (136, 136, 136)
C_LGRAY   = (170, 170, 170)
C_CAPTION = (102, 102, 102)
C_BQ_TEXT = (51, 51, 51)
C_CODE_BG = (245, 245, 245)
C_RULE    = (220, 220, 220)

# ---------------------------------------------------------------------------
# Font discovery
# ---------------------------------------------------------------------------
_FONT_DIRS = [
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path.home() / ".fonts",
    Path.home() / ".local/share/fonts",
]


def _find_ttf(pattern: str):
    """Walk common font dirs for a .ttf matching *pattern* (case-insensitive)."""
    pat = pattern.lower()
    for base in _FONT_DIRS:
        if not base.is_dir():
            continue
        for p in base.rglob("*.ttf"):
            if pat in p.name.lower():
                return str(p)
    return None


# ---------------------------------------------------------------------------
# Unicode sanitiser  (fallback when no TTF fonts available)
# ---------------------------------------------------------------------------
_SANITIZE_MAP = str.maketrans({
    "\u2013": "-",      # en dash
    "\u2014": "--",     # em dash
    "\u2018": "'",      # left single quote
    "\u2019": "'",      # right single quote
    "\u201c": '"',      # left double quote
    "\u201d": '"',      # right double quote
    "\u2022": "*",      # bullet
    "\u2026": "...",    # ellipsis
    "\u00a0": " ",      # non-breaking space
    "\u2011": "-",      # non-breaking hyphen
    "\u2010": "-",      # hyphen
    "\u2212": "-",      # minus sign
    "\u00b7": "*",      # middle dot
    "\u2032": "'",      # prime
    "\u2033": '"',      # double prime
    "\u200b": "",       # zero-width space
    "\ufeff": "",       # BOM
})

# Emoji / surrogate-pair chars that no standard text font supports
_EMOJI_RE = re.compile(
    "["
    "\U0001f300-\U0001f9ff"  # Misc Symbols, Emoticons, etc.
    "\U00002702-\U000027b0"  # Dingbats
    "\U0000fe00-\U0000fe0f"  # Variation Selectors
    "\U0000200d"             # Zero Width Joiner
    "]+",
    flags=re.UNICODE,
)


def _sanitize(text: str) -> str:
    """Replace Unicode chars unsupported by Latin-1 built-in fonts."""
    return text.translate(_SANITIZE_MAP)


# ---------------------------------------------------------------------------
# Token attribute helper  (markdown-it-py can use dict or list-of-tuples)
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


# ===================================================================
# PDF subclass  (footer w/ version + page number)
# ===================================================================
class TimelinePDF(FPDF):
    _sans = "Helvetica"          # overridden by renderer after font setup

    def footer(self):
        self.set_y(-18)
        self.set_font(self._sans, "", 7)
        self.set_text_color(*C_LGRAY)
        self.cell(40, 8, f"v{PKG_VERSION}")
        self.set_font(self._sans, "", 8)
        self.set_text_color(*C_GRAY)
        self.cell(0, 8, str(self.page_no()), align="R")


# ===================================================================
# Main renderer
# ===================================================================
class PDFRenderer:
    """Parse Markdown with markdown-it-py; render with fpdf2 primitives."""

    # Logical font family names (resolved in _setup_fonts)
    SERIF = "Serif"
    SANS  = "Sans"
    MONO  = "Mono"

    def __init__(self):
        self.pdf = TimelinePDF(format="A4")
        self.pdf.set_margins(20, 22, 20)
        self.pdf.set_auto_page_break(True, margin=25)

        self.md = MarkdownIt("commonmark", {"typographer": False}).enable("table")

        self._tmp = tempfile.mkdtemp(prefix="timeline_pdf_")
        self._img_cache: dict = {}
        self._use_unicode = False

        self._setup_fonts()

        # Effective printable width in mm
        self.pw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin

        # Rendering state
        self._text_color = C_BLACK
        self._link_href = None
        self._lh = 6.5                             # line-height (mm)

    # ---------------------------------------------------------------
    #  Font bootstrap
    # ---------------------------------------------------------------
    def _setup_fonts(self):
        serif_r  = _find_ttf("dejavuserif.")
        serif_b  = _find_ttf("dejavuserif-bold.")
        serif_i  = _find_ttf("dejavuserif-italic.")
        serif_bi = _find_ttf("dejavuserif-bolditalic.")
        sans_r   = _find_ttf("dejavusans.")
        sans_b   = _find_ttf("dejavusans-bold.")
        mono_r   = _find_ttf("dejavusansmono.")
        mono_b   = _find_ttf("dejavusansmono-bold.")

        if serif_r and sans_r and mono_r:
            self._use_unicode = True
            self.pdf.add_font(self.SERIF, "",   serif_r)
            self.pdf.add_font(self.SERIF, "B",  serif_b  or serif_r)
            self.pdf.add_font(self.SERIF, "I",  serif_i  or serif_r)
            self.pdf.add_font(self.SERIF, "BI", serif_bi or serif_r)
            sans_i   = _find_ttf("dejavusans-oblique.")
            mono_i   = _find_ttf("dejavusansmono-oblique.")
            self.pdf.add_font(self.SANS,  "",   sans_r)
            self.pdf.add_font(self.SANS,  "B",  sans_b or sans_r)
            self.pdf.add_font(self.SANS,  "I",  sans_i or sans_r)
            self.pdf.add_font(self.SANS,  "BI", sans_i or sans_r)
            self.pdf.add_font(self.MONO,  "",   mono_r)
            self.pdf.add_font(self.MONO,  "B",  mono_b or mono_r)
            self.pdf.add_font(self.MONO,  "I",  mono_i or mono_r)
            print("  Fonts: DejaVu TTF (full Unicode)")
        else:
            self._use_unicode = False
            self.SERIF = "Times"
            self.SANS  = "Helvetica"
            self.MONO  = "Courier"
            print("  Fonts: built-in Latin-1 (Unicode chars replaced)")

        self.pdf._sans = self.SANS

    def _t(self, text: str) -> str:
        """Sanitise text: strip emojis always, plus Latin-1 fixes if no TTF."""
        text = _EMOJI_RE.sub("", text)
        return text if self._use_unicode else _sanitize(text)

    # ---------------------------------------------------------------
    #  Image handling
    # ---------------------------------------------------------------
    def _prepare_image(self, src: str):
        """Resize + compress to temp JPEG; return file path or None."""
        if src in self._img_cache:
            return self._img_cache[src]

        # Skip remote URLs
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

            # Convert to RGB for JPEG
            if img.mode in ("RGBA", "P", "LA"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                img = bg
            elif img.mode != "RGB":
                img = img.convert("RGB")

            out = os.path.join(self._tmp, f"img_{len(self._img_cache)}.jpg")
            img.save(out, "JPEG", quality=JPEG_QUALITY, optimize=True)
            self._img_cache[src] = out
            return out
        except Exception as exc:
            print(f"    WARN image failed ({rel}): {exc}", file=sys.stderr)
            self._img_cache[src] = None
            return None

    def _embed_image(self, src: str, caption: str = ""):
        """Render an image block centred on the page."""
        path = self._prepare_image(src)
        if not path:
            return

        try:
            with Image.open(path) as pil:
                aspect = pil.height / pil.width
        except Exception:
            return

        w = min(self.pw, MAX_IMG_W_MM)
        h = w * aspect
        if h > MAX_IMG_H_MM:
            h = MAX_IMG_H_MM
            w = h / aspect

        # Page-break check
        needed = h + (10 if caption else 6)
        if self.pdf.get_y() + needed > self.pdf.h - self.pdf.b_margin:
            self.pdf.add_page()

        self.pdf.ln(3)
        x = self.pdf.l_margin + (self.pw - w) / 2
        self.pdf.image(path, x=x, w=w)

        if caption:
            self.pdf.set_font(self.SANS, "I", 8.5)
            self.pdf.set_text_color(*C_CAPTION)
            self.pdf.multi_cell(0, 4.5, self._t(caption),
                                align="C", new_x="LMARGIN", new_y="NEXT")
            self._restore_body()

        self.pdf.ln(3)

    # ---------------------------------------------------------------
    #  Inline rendering  (bold / italic / code / links inside text)
    # ---------------------------------------------------------------
    def _render_inline(self, children):
        if not children:
            return
        for tok in children:
            tp = tok.type

            if tp == "text":
                txt = self._t(tok.content)
                if self._link_href:
                    self.pdf.write(self._lh, txt, self._link_href)
                else:
                    self.pdf.write(self._lh, txt)

            elif tp == "softbreak":
                self.pdf.write(self._lh, " ")

            elif tp == "hardbreak":
                self.pdf.ln(self._lh)

            elif tp == "code_inline":
                prev = (self.pdf.font_family, self.pdf.font_style,
                        self.pdf.font_size_pt)
                self.pdf.set_font(self.MONO, "", max(prev[2] - 1.5, 7))
                self.pdf.write(self._lh, self._t(tok.content))
                self.pdf.set_font(prev[0], prev[1], prev[2])

            elif tp == "strong_open":
                s = self.pdf.font_style
                if "B" not in s:
                    self.pdf.set_font(self.pdf.font_family, s + "B",
                                      self.pdf.font_size_pt)

            elif tp == "strong_close":
                s = self.pdf.font_style.replace("B", "")
                self.pdf.set_font(self.pdf.font_family, s,
                                  self.pdf.font_size_pt)

            elif tp == "em_open":
                s = self.pdf.font_style
                if "I" not in s:
                    self.pdf.set_font(self.pdf.font_family, s + "I",
                                      self.pdf.font_size_pt)

            elif tp == "em_close":
                s = self.pdf.font_style.replace("I", "")
                self.pdf.set_font(self.pdf.font_family, s,
                                  self.pdf.font_size_pt)

            elif tp == "link_open":
                self._link_href = _attr(tok, "href")
                self.pdf.set_text_color(*C_GOLD)

            elif tp == "link_close":
                self._link_href = None
                self.pdf.set_text_color(*self._text_color)

            elif tp == "image":
                src = _attr(tok, "src")
                alt = _attr(tok, "alt") or tok.content or ""
                self._embed_image(src, alt)

            elif tp == "html_inline":
                if "<br" in (tok.content or ""):
                    self.pdf.ln(self._lh)

            else:
                # Recurse into children if any; else write raw content
                if tok.children:
                    self._render_inline(tok.children)
                elif tok.content:
                    self.pdf.write(self._lh, self._t(tok.content))

    # ---------------------------------------------------------------
    #  Block rendering
    # ---------------------------------------------------------------
    def _render_heading(self, level: int, inline_tok):
        sizes  = {1: 22, 2: 15, 3: 12, 4: 11}
        colors = {1: C_DARK, 2: C_H2, 3: C_H3, 4: C_H3}
        sz  = sizes.get(level, 10)
        clr = colors.get(level, C_H3)

        # Space before heading — check for page break
        space_before = 8 if level <= 2 else 5
        if self.pdf.get_y() + space_before + sz * 0.6 > self.pdf.h - self.pdf.b_margin:
            self.pdf.add_page()
        else:
            self.pdf.ln(space_before)

        self.pdf.set_font(self.SANS, "B", sz)
        self.pdf.set_text_color(*clr)

        text = self._t(self._plain(inline_tok))
        self.pdf.multi_cell(0, sz * 0.55, text,
                            new_x="LMARGIN", new_y="NEXT")

        if level == 1:
            y = self.pdf.get_y() + 1
            self.pdf.set_draw_color(*C_GOLD)
            self.pdf.set_line_width(0.7)
            self.pdf.line(self.pdf.l_margin, y,
                          self.pdf.w - self.pdf.r_margin, y)
            self.pdf.ln(4)
        elif level == 2:
            y = self.pdf.get_y() + 1
            self.pdf.set_draw_color(*C_RULE)
            self.pdf.set_line_width(0.3)
            self.pdf.line(self.pdf.l_margin, y,
                          self.pdf.w - self.pdf.r_margin, y)
            self.pdf.ln(3)
        else:
            self.pdf.ln(2)

        self._restore_body()

    def _render_paragraph(self, inline_tok):
        self._restore_body()

        if inline_tok.children:
            # If paragraph is just a single image, render as image block
            real = [c for c in inline_tok.children
                    if c.type not in ("softbreak", "hardbreak")]
            if len(real) == 1 and real[0].type == "image":
                img = real[0]
                self._embed_image(_attr(img, "src"),
                                  _attr(img, "alt") or img.content or "")
                return

            # Image-with-caption pattern:
            #   <image> <softbreak> <em_open> caption text <em_close>
            if (len(real) >= 2 and real[0].type == "image"
                    and real[1].type == "em_open"):
                img = real[0]
                cap_parts = []
                for c in real[2:]:
                    if c.type == "em_close":
                        break
                    if c.type == "text":
                        cap_parts.append(c.content)
                caption = "".join(cap_parts) or _attr(img, "alt") or img.content or ""
                self._embed_image(_attr(img, "src"), caption)
                return

            self._render_inline(inline_tok.children)
        elif inline_tok.content:
            self.pdf.write(self._lh, self._t(inline_tok.content))

        self.pdf.ln(self._lh + 2)

    def _render_blockquote(self, inner_tokens: list):
        self.pdf.ln(3)
        y0 = self.pdf.get_y()
        saved_l = self.pdf.l_margin

        self.pdf.set_left_margin(saved_l + 10)
        self.pdf.set_x(saved_l + 10)

        self.pdf.set_font(self.SERIF, "I", 10)
        self.pdf.set_text_color(*C_BQ_TEXT)
        self._text_color = C_BQ_TEXT

        self._render_tokens(inner_tokens)

        y1 = self.pdf.get_y()

        # Gold left bar
        self.pdf.set_draw_color(*C_GOLD)
        self.pdf.set_line_width(1.0)
        self.pdf.line(saved_l + 4, y0, saved_l + 4, y1)

        self.pdf.set_left_margin(saved_l)
        self.pdf.ln(3)
        self._restore_body()

    def _render_list(self, items: list, ordered: bool):
        saved_l = self.pdf.l_margin

        for idx, item_tokens in enumerate(items, 1):
            self.pdf.set_left_margin(saved_l + 7)
            self.pdf.set_x(saved_l)
            self._restore_body()

            bullet = f"{idx}. " if ordered else "- "
            self.pdf.cell(7, self._lh, bullet)

            for tok in item_tokens:
                if tok.type in ("paragraph_open", "paragraph_close"):
                    continue
                if tok.type == "inline":
                    if tok.children:
                        self._render_inline(tok.children)
                    elif tok.content:
                        self.pdf.write(self._lh, self._t(tok.content))

            self.pdf.ln(self._lh + 1)

        self.pdf.set_left_margin(saved_l)
        self.pdf.ln(2)

    def _render_fence(self, content: str):
        self.pdf.ln(2)
        self.pdf.set_font(self.MONO, "", 8)
        self.pdf.set_fill_color(*C_CODE_BG)
        self.pdf.set_text_color(*C_BQ_TEXT)

        self.pdf.multi_cell(0, 4.2, self._t(content.rstrip("\n")),
                            fill=True, new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(3)
        self._restore_body()

    def _render_hr(self):
        self.pdf.ln(4)
        y = self.pdf.get_y()
        self.pdf.set_draw_color(*C_RULE)
        self.pdf.set_line_width(0.3)
        self.pdf.line(self.pdf.l_margin, y, self.pdf.w - self.pdf.r_margin, y)
        self.pdf.ln(4)

    def _render_table(self, inner_tokens: list):
        headers: list = []
        rows: list = []
        in_head = False
        cur_row: list = []

        for tok in inner_tokens:
            if tok.type == "thead_open":
                in_head = True
            elif tok.type == "thead_close":
                in_head = False
            elif tok.type == "tr_open":
                cur_row = []
            elif tok.type == "tr_close":
                (headers if in_head else rows).append(cur_row)
            elif tok.type == "inline":
                cur_row.append(self._t(self._plain(tok)))

        all_rows = headers + rows
        if not all_rows:
            return
        ncols = max(len(r) for r in all_rows)
        if ncols == 0:
            return

        self.pdf.ln(3)
        col_w = self.pw / ncols

        # Header rows
        for row in headers:
            self.pdf.set_font(self.SANS, "B", 7.5)
            self.pdf.set_fill_color(240, 240, 240)
            for j in range(ncols):
                cell = row[j] if j < len(row) else ""
                self.pdf.cell(col_w, 5.5, cell[:55], border=1, fill=True)
            self.pdf.ln()

        # Data rows
        self.pdf.set_font(self.SANS, "", 7)
        for row in rows:
            if self.pdf.get_y() + 5 > self.pdf.h - self.pdf.b_margin:
                self.pdf.add_page()
                # Re-print header on new page
                for hrow in headers:
                    self.pdf.set_font(self.SANS, "B", 7.5)
                    self.pdf.set_fill_color(240, 240, 240)
                    for j in range(ncols):
                        cell = hrow[j] if j < len(hrow) else ""
                        self.pdf.cell(col_w, 5.5, cell[:55], border=1, fill=True)
                    self.pdf.ln()
                self.pdf.set_font(self.SANS, "", 7)

            for j in range(ncols):
                cell = row[j] if j < len(row) else ""
                self.pdf.cell(col_w, 5, cell[:55], border=1)
            self.pdf.ln()

        self.pdf.ln(3)
        self._restore_body()

    # ---------------------------------------------------------------
    #  Token walker
    # ---------------------------------------------------------------
    def _render_tokens(self, tokens: list):
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            tp = tok.type

            if tp == "heading_open":
                inline = tokens[i + 1] if i + 1 < len(tokens) else None
                i += 2                              # skip inline + heading_close
                if inline:
                    level = int(tok.tag[1])
                    self._render_heading(level, inline)

            elif tp == "paragraph_open":
                inline = tokens[i + 1] if i + 1 < len(tokens) else None
                i += 2                              # skip inline + paragraph_close
                if inline:
                    self._render_paragraph(inline)

            elif tp == "blockquote_open":
                depth, bq = 1, []
                i += 1
                while i < len(tokens) and depth > 0:
                    if tokens[i].type == "blockquote_open":
                        depth += 1
                    elif tokens[i].type == "blockquote_close":
                        depth -= 1
                        if depth == 0:
                            break
                    bq.append(tokens[i])
                    i += 1
                self._render_blockquote(bq)

            elif tp == "bullet_list_open":
                i, items = self._collect_list_items(
                    tokens, i + 1, "bullet_list_close")
                self._render_list(items, ordered=False)

            elif tp == "ordered_list_open":
                i, items = self._collect_list_items(
                    tokens, i + 1, "ordered_list_close")
                self._render_list(items, ordered=True)

            elif tp in ("fence", "code_block"):
                self._render_fence(tok.content or "")

            elif tp == "hr":
                self._render_hr()

            elif tp == "table_open":
                tbl = []
                i += 1
                while i < len(tokens) and tokens[i].type != "table_close":
                    tbl.append(tokens[i])
                    i += 1
                self._render_table(tbl)

            # Skip tokens we don't render (html_block, close tags, etc.)

            i += 1

    def _collect_list_items(self, tokens, start, close_type):
        """Return (index_of_close, list_of_item_token_lists)."""
        items: list = []
        i = start
        while i < len(tokens) and tokens[i].type != close_type:
            if tokens[i].type == "list_item_open":
                i += 1
                item: list = []
                while i < len(tokens) and tokens[i].type != "list_item_close":
                    item.append(tokens[i])
                    i += 1
                items.append(item)
            i += 1
        return i, items

    # ---------------------------------------------------------------
    #  Helpers
    # ---------------------------------------------------------------
    def _plain(self, tok) -> str:
        """Flatten a token tree to plain text."""
        if tok.children:
            return "".join(self._plain(c) for c in tok.children)
        if tok.type in ("text", "code_inline"):
            return tok.content or ""
        if tok.type == "softbreak":
            return " "
        return tok.content or ""

    def _restore_body(self):
        """Reset to default body font and colour."""
        self.pdf.set_font(self.SERIF, "", 10.5)
        self.pdf.set_text_color(*C_BLACK)
        self._text_color = C_BLACK
        self._link_href = None

    # ---------------------------------------------------------------
    #  Article + main entry
    # ---------------------------------------------------------------
    def render_article(self, path: Path):
        text = path.read_text("utf-8")
        text = re.sub(r"<[A-Z][A-Za-z0-9]*[^>]*/?>", "", text)    # strip JSX
        text = re.sub(r"</?[A-Z][A-Za-z0-9]*>", "", text)          # strip closing JSX

        self.pdf.add_page()

        # Section label  (e.g. "01.020")
        m = re.match(r"(\d+\.\d+)", path.name)
        if m:
            self.pdf.set_font(self.SANS, "", 7.5)
            self.pdf.set_text_color(*C_GRAY)
            self.pdf.cell(0, 4, m.group(1),
                          new_x="LMARGIN", new_y="NEXT")
            self.pdf.ln(1)

        self._restore_body()
        tokens = self.md.parse(text)
        self._render_tokens(tokens)

    def generate(self):
        EXPORT_DIR.mkdir(exist_ok=True)
        md_files = sorted(CONTENT_DIR.glob("*.md"))
        if not md_files:
            sys.exit("No markdown files in content/")

        n = len(md_files)
        print(f"Generating PDF from {n} content files ...")

        for i, p in enumerate(md_files):
            print(f"  [{i + 1:3d}/{n}] {p.name}")
            self.render_article(p)

        print(f"Writing -> {OUTPUT_PDF}")
        self.pdf.output(str(OUTPUT_PDF))
        mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
        print(f"Done.  {mb:.1f} MB  ({self.pdf.pages_count} pages)")

    def cleanup(self):
        shutil.rmtree(self._tmp, ignore_errors=True)


# ===================================================================
def main():
    renderer = PDFRenderer()
    try:
        renderer.generate()
    finally:
        renderer.cleanup()


if __name__ == "__main__":
    main()
