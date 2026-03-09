#!/usr/bin/env python3
"""
Generate a DOCX flyer requesting test readers / feedback for the
Paradigm Threat timeline draft.

Page 1     — flyer (call to action, feedback categories, links)
Page 2     — mini table of contents for the sample chapters
Pages 3+   — full rendered content of each sample chapter

Uses the same DOCXRenderer from generate-docx.py but with letter-size
pages and compact (smaller) fonts so more content fits per page.
"""

import sys
from pathlib import Path

# ── Bootstrap: make sibling scripts importable ────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Import the full renderer from the book generator
import importlib
gd = importlib.import_module("generate-docx")
DOCXRenderer = gd.DOCXRenderer

REPO_DIR    = SCRIPT_DIR.parent
CONTENT_DIR = REPO_DIR / "content"
OUT         = REPO_DIR / "export" / "test-reader-flyer.docx"

# ── Sample chapter paths (in print order) ─────────────────────────────
SAMPLE_CHAPTERS = [
    "content/00.overview/00.00.00-introduction.md",
    "content/02.the-golden-age/02.02.00-the-225-day-year.md",
    "content/05.ce-11th-common-era-begins/05.00.00-1053-ce-11th-century-ce-common-era-begins.md",
    "content/09.ce-15th-ottoman-conquest-of-europe/09.01.00-meteorite-falls-on-yaroslavl.md",
    "content/14.ce-20th-the-1917-revolution/14.01.00-world-war-i-reverse-crusade-ii.md",
    "content/15.ce-21st-the-final-struggle/15.07.00-historical-antibodies.md",
    "content/15.ce-21st-the-final-struggle/15.07.01-trump.md",
]

# ── Letter-size overrides ─────────────────────────────────────────────
LETTER_W       = Inches(8.5)
LETTER_H       = Inches(11)
LETTER_MARGIN  = Cm(1.5)
LETTER_MARGIN_TB = Cm(1.2)

# ── Compact font sizes (≈80 % of book sizes) ─────────────────────────
BODY_SIZE      = Pt(9)
COMPACT_SECONDARY = Pt(8)
H1_SIZE        = Pt(16)
H2_SIZE        = Pt(11.5)
H3_SIZE        = Pt(9.5)
H4_SIZE        = Pt(9)


# =====================================================================
#  Compact renderer — inherits DOCXRenderer, overrides layout + fonts
# =====================================================================
class CompactRenderer(DOCXRenderer):
    """Letter-size, dense variant of DOCXRenderer for the flyer."""

    SECONDARY_SIZE = COMPACT_SECONDARY

    # Override page dimensions ------------------------------------------
    def _apply_section_dims(self, section):
        section.page_width    = LETTER_W
        section.page_height   = LETTER_H
        section.top_margin    = LETTER_MARGIN_TB
        section.bottom_margin = LETTER_MARGIN_TB
        section.left_margin   = LETTER_MARGIN
        section.right_margin  = LETTER_MARGIN

    # Override styles to use compact sizes ------------------------------
    def _setup_styles(self):
        super()._setup_styles()
        doc = self.doc

        # Body text — smaller
        style = doc.styles["Normal"]
        style.font.size = BODY_SIZE
        style.paragraph_format.space_after = Pt(4)

        # Headings — smaller
        h_specs = {
            "Heading 1": (H1_SIZE, True, RGBColor(0x1a, 0x1a, 0x1a), self.FONT_SANS),
            "Heading 2": (H2_SIZE, True, RGBColor(0x2c, 0x2c, 0x2c), self.FONT_SANS),
            "Heading 3": (H3_SIZE, True, RGBColor(0x3a, 0x3a, 0x3a), self.FONT_SANS),
            "Heading 4": (H4_SIZE, True, RGBColor(0x4e, 0x4e, 0x4e), self.FONT_SERIF),
        }
        for sname, (sz, bold, clr, fname) in h_specs.items():
            s = doc.styles[sname]
            s.font.size = sz
            s.paragraph_format.space_before = Pt(8 if sz >= Pt(14) else 6)
            s.paragraph_format.space_after  = Pt(2)

        # Quote — smaller
        qs = doc.styles["Quote"]
        qs.font.size = COMPACT_SECONDARY
        qs.paragraph_format.left_indent = Cm(0.8)
        qs.paragraph_format.space_before = Pt(2)
        qs.paragraph_format.space_after  = Pt(2)

        # Lists — tighter
        for ls_name in ("List Bullet", "List Number"):
            try:
                ls = doc.styles[ls_name]
                ls.font.size = COMPACT_SECONDARY
                ls.paragraph_format.space_before = Pt(0)
                ls.paragraph_format.space_after  = Pt(0)
            except KeyError:
                pass

        # Caption — smaller
        try:
            cs = doc.styles["Caption"]
            cs.font.size = Pt(7.5)
        except KeyError:
            pass

    # Cap image width for the wider letter page -------------------------
    def _embed_image(self, src: str, caption: str = ""):
        result = self._prepare_image(src)
        if not result:
            return
        buf, width_in = result
        width_in = min(width_in, 5.5)
        buf.seek(0)
        para = self.doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(buf, width=Inches(width_in))
        if caption:
            cp = self.doc.add_paragraph(style="Caption")
            cp.add_run(caption)


# =====================================================================
#  Helper utilities for the flyer cover page
# =====================================================================

def _add_run(paragraph, text, bold=False, italic=False, size=None, color=None, font_name=None):
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    if font_name:
        run.font.name = font_name
    return run


def _add_para(doc, text="", bold=False, italic=False, size=11, alignment=None,
              color=None, space_after=Pt(4), space_before=Pt(0), font_name=None):
    p = doc.add_paragraph()
    if alignment is not None:
        p.alignment = alignment
    p.paragraph_format.space_after = space_after
    p.paragraph_format.space_before = space_before
    if text:
        _add_run(p, text, bold=bold, italic=italic, size=size, color=color, font_name=font_name)
    return p


def _add_hyperlink(paragraph, url, text, font_size=None, bold=False):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = paragraph._element.makeelement(qn("w:hyperlink"), {qn("r:id"): r_id})
    new_run = paragraph._element.makeelement(qn("w:r"), {})
    rPr = paragraph._element.makeelement(qn("w:rPr"), {})
    u = paragraph._element.makeelement(qn("w:u"), {qn("w:val"): "single"})
    rPr.append(u)
    c = paragraph._element.makeelement(qn("w:color"), {qn("w:val"): "1155CC"})
    rPr.append(c)
    if bold:
        b = paragraph._element.makeelement(qn("w:b"), {})
        rPr.append(b)
    if font_size:
        sz = paragraph._element.makeelement(qn("w:sz"), {qn("w:val"): str(int(font_size * 2))})
        rPr.append(sz)
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)


def _set_cell_shading(cell, color_hex: str):
    shading = cell._element.get_or_add_tcPr()
    shd = shading.makeelement(qn("w:shd"), {
        qn("w:val"): "clear",
        qn("w:color"): "auto",
        qn("w:fill"): color_hex,
    })
    shading.append(shd)


# =====================================================================
#  Build the flyer cover page (page 1)
# =====================================================================

def _build_cover_page(doc):
    """Write the single-page flyer / call-to-action onto the document."""
    _add_para(doc, "PARADIGM THREAT", bold=True, size=36,
              alignment=WD_ALIGN_PARAGRAPH.CENTER,
              color=(0x22, 0x22, 0x22), space_after=Pt(0))
    _add_para(doc, "An Alternate Earth History Timeline", italic=True, size=16,
              alignment=WD_ALIGN_PARAGRAPH.CENTER,
              color=(0x55, 0x55, 0x55), space_after=Pt(4))
    _add_para(doc, "— TEST READERS WANTED —", bold=True, size=22,
              alignment=WD_ALIGN_PARAGRAPH.CENTER,
              color=(0xCC, 0x33, 0x00), space_before=Pt(6), space_after=Pt(10))

    # What is this?
    _add_para(doc, "What is this?", bold=True, size=14, space_before=Pt(6), space_after=Pt(2))
    p = _add_para(doc, size=11, space_after=Pt(4))
    _add_run(p, "Paradigm Threat", bold=True, size=11)
    _add_run(p, " is a draft book that re-examines world history by correlating mainstream "
                "(Scaligerian) chronology with Fomenko's New Chronology, Saturnian Cosmology, "
                "and other alternative frameworks. It's an ", size=11)
    _add_run(p, "investigation", bold=True, italic=True, size=11)
    _add_run(p, ", not a textbook — the goal is to ask better questions, not to "
                "declare final answers.", size=11)

    # What I'm looking for
    _add_para(doc, "What I'm looking for", bold=True, size=14, space_before=Pt(6), space_after=Pt(2))
    bullets = [
        ("Clarity: ",  "Are the arguments easy to follow? Where do you get lost or confused?"),
        ("Gaps: ",     "What questions does a chapter raise that it doesn't answer?"),
        ("Tone: ",     "Does the writing feel investigative, or does it veer into lecture / rant?"),
        ("Interest: ", "Which chapters grabbed you? Which ones didn't?"),
        ("Errors: ",   "Typos, broken logic, factual mistakes — all welcome."),
    ]
    for b, rest in bullets:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        _add_run(p, b, bold=True, size=11)
        _add_run(p, rest, size=11)

    # Sample chapters table
    _add_para(doc, "Sample chapters included", bold=True, size=14,
              space_before=Pt(8), space_after=Pt(2))
    _add_para(doc, "These chapters are attached — a taste of the range and tone:",
              size=11, space_after=Pt(3))

    chapters = [
        ("Introduction",                                    "What the project is and why it exists"),
        ("The 225-Day Year",                                "Evidence from the Sumerian King-List"),
        ("1053 CE — Common Era Begins",                     "The 11th century as the true start of recorded history"),
        ("1421 CE — Meteorite Falls on Yaroslavl",          "A cosmic catastrophe and its political aftermath"),
        ("1914–1918 CE — World War I: Reverse Crusade II",  "WWI as a controlled demolition of empires"),
        ("Historical Antibodies",                           "Independent agents who preserved suppressed knowledge"),
        ("Trump and the MAGA Revolution",                   "The antibody that survived crucifixion"),
    ]
    table = doc.add_table(rows=len(chapters), cols=2)
    table.style = "Table Grid"
    for i, (title, desc) in enumerate(chapters):
        row = table.rows[i]
        row.cells[0].width = Inches(2.0)
        row.cells[1].width = Inches(4.5)
        if i % 2 == 0:
            for cell in row.cells:
                _set_cell_shading(cell, "F2F2F2")
        cp = row.cells[0].paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        cp.paragraph_format.space_before = Pt(2)
        _add_run(cp, title, bold=True, size=10.5)
        dp = row.cells[1].paragraphs[0]
        dp.paragraph_format.space_after = Pt(2)
        dp.paragraph_format.space_before = Pt(2)
        _add_run(dp, desc, size=10.5, italic=True)

    # How to read the full draft
    _add_para(doc, "How to read the full draft", bold=True, size=14,
              space_before=Pt(8), space_after=Pt(2))
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    _add_run(p, "Read online: ", bold=True, size=11)
    _add_hyperlink(p, "https://paradigmthreat.net/timeline",
                   "paradigmthreat.net/timeline", font_size=11, bold=True)

    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    _add_run(p, "Google Doc: ", bold=True, size=11)
    _add_run(p, "Ask and I'll share an editable link — leave comments directly.", size=11)

    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    _add_run(p, "PDF download: ", bold=True, size=11)
    _add_run(p, "A printable PDF of the current version is available — just ask.", size=11)

    # No rush
    _add_para(doc, "No rush, no rules", bold=True, size=14,
              space_before=Pt(8), space_after=Pt(2))
    _add_para(doc,
              "Read as much or as little as you like. You don't need to agree — "
              "honest reactions are what matter most. Even a single page of notes is "
              "valuable. This is a draft; it will change based on your feedback.",
              size=11, space_after=Pt(6))

    p = _add_para(doc, "", alignment=WD_ALIGN_PARAGRAPH.CENTER,
                  space_before=Pt(4), space_after=Pt(0))
    _add_run(p, "Interested?  ", bold=True, size=13)
    _add_run(p, "Reach out — I'd love to hear from you.", size=13)


# =====================================================================
#  Build the TOC pages — full book TOC, sample chapters marked
# =====================================================================

def _build_toc(doc, sample_set: set):
    """Add the complete book TOC. Entries whose path is in *sample_set*
    are marked with a bullet so the reader knows which chapters are
    printed in this flyer."""
    import re

    doc.add_page_break()

    # Gather all book files (same logic as the main exporter)
    all_files = sorted(CONTENT_DIR.rglob("*.md"))
    book_files = [p for p in all_files if not p.name.startswith(("16.", "17."))]
    if not book_files:
        return

    heading = doc.add_paragraph()
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hr = heading.add_run("Table of Contents")
    hr.bold = True
    hr.font.size = Pt(16)
    hr.font.name = "Libre Franklin"
    hr.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

    rule = doc.add_paragraph()
    rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = rule.add_run("\u2500" * 72)
    rr.font.size = Pt(6)
    rr.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)
    rule.paragraph_format.space_after = Pt(4)

    # Legend
    legend = doc.add_paragraph()
    legend.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lr = legend.add_run("\u25cf = sample chapter included in this flyer")
    lr.italic = True
    lr.font.size = Pt(7.5)
    lr.font.color.rgb = RGBColor(0xCC, 0x33, 0x00)
    legend.paragraph_format.space_after = Pt(6)

    _ROMAN = gd._ROMAN
    chapter_counter = 0

    for path in book_files:
        tier, xx, yy, zz = gd._classify_tier(path.name)
        is_sample = path.resolve() in sample_set

        try:
            with open(path, encoding="utf-8") as f:
                first_line = f.readline().strip()
            title = first_line.lstrip("#").strip() if first_line.startswith("#") else path.stem
        except Exception:
            title = path.stem

        marker = "\u25cf " if is_sample else ""

        if tier == "part":
            roman = _ROMAN[int(xx)] if int(xx) < len(_ROMAN) else str(xx)
            display = f"Part {roman}: {title}"

            pm = re.match(
                r"^(\d{1,2}(?:st|nd|rd|th)\s+Century(?:\s+C\.E\.)?)"
                r"(?:\s*[.:\-\u2014]\s*|\s+)(.+)$",
                title,
            )
            if pm:
                main_title = f"Part {roman}: {pm.group(1).strip().rstrip('.')}"
                subtitle   = pm.group(2).strip().rstrip(".")
            else:
                main_title = display
                subtitle   = ""

            para = doc.add_paragraph(style="TOC 1")
            para.paragraph_format.space_before = Pt(4)
            para.paragraph_format.space_after  = Pt(1)
            run = para.add_run(f"{marker}{main_title}")
            run.bold = True
            run.font.name = "Libre Franklin"
            run.font.size = Pt(8.5)
            if is_sample:
                run.font.color.rgb = RGBColor(0xCC, 0x33, 0x00)

            if subtitle:
                sub_para = doc.add_paragraph(style="TOC 1")
                sub_para.paragraph_format.space_before = Pt(0)
                sub_para.paragraph_format.space_after  = Pt(0)
                sub_para.paragraph_format.left_indent = Cm(0.4)
                sr = sub_para.add_run(subtitle)
                sr.italic = True
                sr.bold = False
                sr.font.name = "Libre Franklin"
                sr.font.size = Pt(7)
                sr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        elif tier == "chapter":
            chapter_counter += 1
            para = doc.add_paragraph(style="TOC 2")
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after  = Pt(0)
            cr = para.add_run(f"{marker}Chapter {chapter_counter}: {title}")
            cr.font.name = "EB Garamond"
            cr.font.size = Pt(8)
            if is_sample:
                cr.font.color.rgb = RGBColor(0xCC, 0x33, 0x00)

        elif tier == "subsection":
            para = doc.add_paragraph(style="TOC 3")
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after  = Pt(0)
            sr = para.add_run(f"{marker}{title}")
            sr.italic = True
            sr.font.name = "EB Garamond"
            sr.font.size = Pt(7)
            sr.font.color.rgb = RGBColor(0xCC, 0x33, 0x00) if is_sample else RGBColor(0x66, 0x66, 0x66)

    doc.add_page_break()


# =====================================================================
#  Main build
# =====================================================================

def build():
    # Resolve chapter paths
    chapter_paths = [REPO_DIR / p for p in SAMPLE_CHAPTERS]
    for cp in chapter_paths:
        if not cp.is_file():
            print(f"WARNING: chapter not found: {cp}", file=sys.stderr)

    # Build set of resolved sample paths for TOC highlighting
    sample_set = {cp.resolve() for cp in chapter_paths if cp.is_file()}

    # Create compact renderer (sets up document with letter-size + small fonts)
    renderer = CompactRenderer()
    doc = renderer.doc

    # ── Page 1: Flyer cover ───────────────────────────────────────────
    _build_cover_page(doc)

    # ── Pages 2+: Full book TOC (sample chapters highlighted) ─────────
    _build_toc(doc, sample_set)

    # ── Remaining pages: Rendered sample chapter content ──────────────
    for i, cp in enumerate(chapter_paths):
        if not cp.is_file():
            continue
        print(f"  [{i + 1}/{len(chapter_paths)}] {cp.name}")
        renderer.render_article(cp)

    # ── Save ──────────────────────────────────────────────────────────
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    kb = OUT.stat().st_size / 1024
    print(f"✅ Flyer saved to {OUT}  ({kb:.0f} KB)")


if __name__ == "__main__":
    build()
