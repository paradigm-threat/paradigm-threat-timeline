#!/usr/bin/env python3
"""
Generate a native PDF from all content/*.md files -> export/timeline.pdf

Uses fpdf2 for direct PDF generation — no HTML/CSS intermediate step.
Markdown is parsed with markdown-it-py and rendered directly to PDF primitives.
Images are resized with Pillow and embedded as native JPEG streams.

Print spec: docs/PRINT_GOALS.md
  - 6″ × 9″ trade paperback, mirrored margins, PDF 1.4
  - EB Garamond body, Libre Franklin headings, JetBrains Mono code
  - Alternating running headers, recto chapter openers, leader-dot TOC

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
FONTS_DIR   = REPO_DIR / "fonts"

with open(REPO_DIR / "package.json") as _f:
    PKG_VERSION = json.load(_f)["version"]

# ---------------------------------------------------------------------------
# Page geometry  (6″ × 9″ trade paperback)
# ---------------------------------------------------------------------------
PAGE_W_MM  = 152.4   # 6 inches
PAGE_H_MM  = 228.6   # 9 inches

# Mirrored margins — inside (gutter) is larger for binding
MARGIN_INSIDE  = 25   # mm  (gutter side)
MARGIN_OUTSIDE = 16   # mm
MARGIN_TOP     = 20   # mm
MARGIN_BOTTOM  = 22   # mm

# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
MAX_IMG_PX   = 1400          # max width in pixels before resize
JPEG_QUALITY = 82            # B&W edition
MAX_IMG_W_MM = 120           # max image width in PDF (mm)
MAX_IMG_H_MM = 100           # max image height in PDF (mm)

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
# Roman numerals & tier classifier
# ---------------------------------------------------------------------------
_ROMAN = [
    "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
]

_TIER_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})")

def _classify_tier(filename: str):
    """Return (tier, xx, yy, zz) from an ``XX.YY.ZZ-slug.md`` filename."""
    m = _TIER_RE.match(filename)
    if not m:
        return ("part", "00", "00", "00")
    xx, yy, zz = m.group(1), m.group(2), m.group(3)
    if yy == "00" and zz == "00":
        return ("part", xx, yy, zz)
    if zz == "00":
        return ("chapter", xx, yy, zz)
    return ("subsection", xx, yy, zz)

# ---------------------------------------------------------------------------
# Font discovery — priority: fonts/ repo dir > system fonts > built-in
# ---------------------------------------------------------------------------
_FONT_DIRS = [
    FONTS_DIR,                                      # 1. repo fonts/ directory
    Path("/usr/share/fonts"),                        # 2. system fonts
    Path("/usr/local/share/fonts"),
    Path.home() / ".fonts",
    Path.home() / ".local/share/fonts",
]


def _find_ttf(pattern: str):
    """Walk font dirs for a .ttf matching *pattern* (case-insensitive)."""
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
# PDF subclass  — running headers + mirrored margins + page numbers
# ===================================================================
class TimelinePDF(FPDF):
    _sans  = "Helvetica"      # overridden by renderer after font setup
    _serif = "Times"          # overridden by renderer after font setup
    book_title    = "Paradigm Threat: The Third Story"
    part_title    = ""         # updated per Part
    chapter_title = ""         # updated per Chapter
    _in_front_matter   = True  # suppress headers/numbers during front matter
    _chapter_opener    = False # suppress header on chapter-opening pages
    _part_opener       = False # suppress header on Part title pages

    def __init__(self, **kw):
        super().__init__(**kw)
        self._use_unicode = False

    def _apply_margins(self):
        """Set left/right margins based on current page parity."""
        if self.page % 2 == 1:
            # Recto (odd) — gutter on left
            self.set_left_margin(MARGIN_INSIDE)
            self.set_right_margin(MARGIN_OUTSIDE)
        else:
            # Verso (even) — gutter on right
            self.set_left_margin(MARGIN_OUTSIDE)
            self.set_right_margin(MARGIN_INSIDE)
        self.set_x(self.l_margin)

    def accept_page_break(self):
        """Called by fpdf2 before an automatic page break."""
        return True

    def header(self):
        """Running header — alternating recto/verso, suppressed on front matter
        and chapter openers."""
        self._apply_margins()

        if self._in_front_matter or self._chapter_opener or self._part_opener:
            self._chapter_opener = False
            self._part_opener = False
            return

        pw = self.w - self.l_margin - self.r_margin
        self.set_y(MARGIN_TOP - 8)
        self.set_font(self._sans, "", 7.5)
        self.set_text_color(*C_GRAY)

        if self.page % 2 == 0:
            # Verso (even): Part title left, page# right (outer)
            self.set_x(self.l_margin)
            title = (self.part_title or self.book_title).upper()
            self.cell(pw / 2, 5, self._t_header(title[:55]), align="L")
            self.cell(pw / 2, 5, str(self.page_no()), align="R")
        else:
            # Recto (odd): page# left (outer), chapter title right
            self.set_x(self.l_margin)
            self.cell(pw / 2, 5, str(self.page_no()), align="L")
            chap = self.chapter_title[:55].upper() if self.chapter_title else ""
            self.cell(pw / 2, 5, self._t_header(chap), align="R")

        # Separator rule
        y = self.get_y() + 5.5
        self.set_draw_color(*C_RULE)
        self.set_line_width(0.3)
        self.line(self.l_margin, y, self.w - self.r_margin, y)

        # Reset cursor so body content starts at left margin
        self.set_x(self.l_margin)
        self.set_y(self.t_margin)

    def _t_header(self, text: str) -> str:
        """Sanitise header text when using built-in fonts."""
        if self._use_unicode:
            return _EMOJI_RE.sub("", text)
        return _sanitize(_EMOJI_RE.sub("", text))

    def footer(self):
        """Page number on outer bottom corner, version on inner corner.
        Suppressed during front matter."""
        if self._in_front_matter:
            return

        self.set_y(-MARGIN_BOTTOM + 4)

        if self.page % 2 == 1:
            # Recto — version left (inner), page# right (outer)
            self.set_x(MARGIN_INSIDE)
            self.set_font(self._sans, "", 7)
            self.set_text_color(*C_LGRAY)
            pw = self.w - MARGIN_INSIDE - MARGIN_OUTSIDE
            self.cell(pw / 2, 8, f"v{PKG_VERSION}")
            self.set_font(self._sans, "", 8)
            self.set_text_color(*C_GRAY)
            self.cell(pw / 2, 8, str(self.page_no()), align="R")
        else:
            # Verso — page# left (outer), version right (inner)
            self.set_x(MARGIN_OUTSIDE)
            self.set_font(self._sans, "", 8)
            self.set_text_color(*C_GRAY)
            pw = self.w - MARGIN_INSIDE - MARGIN_OUTSIDE
            self.cell(pw / 2, 8, str(self.page_no()), align="L")
            self.set_font(self._sans, "", 7)
            self.set_text_color(*C_LGRAY)
            self.cell(pw / 2, 8, f"v{PKG_VERSION}", align="R")


# ===================================================================
# Main renderer
# ===================================================================
class PDFRenderer:
    """Parse Markdown with markdown-it-py; render with fpdf2 primitives."""

    # Logical font family names (resolved in _setup_fonts)
    SERIF = "Serif"
    SANS  = "Sans"
    MONO  = "Mono"

    # Body typography
    BODY_SIZE    = 11      # pt
    BODY_LEADING = 5.3     # mm  (≈ 15 pt)
    INDENT_MM    = 5       # first-line indent for subsequent paragraphs

    def __init__(self):
        self.pdf = TimelinePDF(format=(PAGE_W_MM, PAGE_H_MM))
        self.pdf.set_margins(MARGIN_INSIDE, MARGIN_TOP, MARGIN_OUTSIDE)
        self.pdf.set_auto_page_break(True, margin=MARGIN_BOTTOM)

        self.md = MarkdownIt("commonmark", {"typographer": False}).enable("table")

        self._tmp = tempfile.mkdtemp(prefix="timeline_pdf_")
        self._img_cache: dict = {}
        self._use_unicode = False

        self._setup_fonts()

        # Effective printable width (use narrower dimension for safe layout)
        self.pw = PAGE_W_MM - MARGIN_INSIDE - MARGIN_OUTSIDE

        # Rendering state
        self._text_color = C_BLACK
        self._link_href = None
        self._lh = self.BODY_LEADING
        self._para_index = 0
        self._chapter_title = ""

        # Part / Chapter counters
        self._current_part_xx = None   # XX string of current Part
        self._chapter_counter = 0      # resets per Part
        self._current_part_num = 0     # integer for Roman numeral

    # ---------------------------------------------------------------
    #  Font bootstrap — prioritise fonts/ dir (EB Garamond, Libre
    #  Franklin, JetBrains Mono), fall back to DejaVu, then built-in
    # ---------------------------------------------------------------
    def _setup_fonts(self):
        # --- Preferred: EB Garamond / Libre Franklin / JetBrains Mono ---
        eb_r   = _find_ttf("ebgaramond-variable")
        eb_i   = _find_ttf("ebgaramond-italic-variable")
        lf_r   = _find_ttf("librefranklin-variable")
        lf_i   = _find_ttf("librefranklin-italic-variable")
        jb_r   = _find_ttf("jetbrainsmono-variable")
        jb_i   = _find_ttf("jetbrainsmono-italic-variable")

        if eb_r and lf_r and jb_r:
            self._use_unicode = True
            self.pdf._use_unicode = True
            # Serif — EB Garamond
            self.pdf.add_font(self.SERIF, "",   eb_r)
            self.pdf.add_font(self.SERIF, "B",  eb_r)
            self.pdf.add_font(self.SERIF, "I",  eb_i or eb_r)
            self.pdf.add_font(self.SERIF, "BI", eb_i or eb_r)
            # Sans — Libre Franklin
            self.pdf.add_font(self.SANS, "",    lf_r)
            self.pdf.add_font(self.SANS, "B",   lf_r)
            self.pdf.add_font(self.SANS, "I",   lf_i or lf_r)
            self.pdf.add_font(self.SANS, "BI",  lf_i or lf_r)
            # Mono — JetBrains Mono
            self.pdf.add_font(self.MONO, "",    jb_r)
            self.pdf.add_font(self.MONO, "B",   jb_r)
            self.pdf.add_font(self.MONO, "I",   jb_i or jb_r)
            print("  Fonts: EB Garamond + Libre Franklin + JetBrains Mono (full Unicode)")
        else:
            # --- Fallback: DejaVu system fonts ---
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
                self.pdf._use_unicode = True
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
                self.pdf._use_unicode = False
                self.SERIF = "Times"
                self.SANS  = "Helvetica"
                self.MONO  = "Courier"
                print("  Fonts: built-in Latin-1 (Unicode chars replaced)")

        self.pdf._sans  = self.SANS
        self.pdf._serif = self.SERIF

    def _t(self, text: str) -> str:
        """Sanitise text: strip emojis always, plus Latin-1 fixes if no TTF."""
        text = _EMOJI_RE.sub("", text)
        return text if self._use_unicode else _sanitize(text)

    # ---------------------------------------------------------------
    #  Page helpers
    # ---------------------------------------------------------------
    def _ensure_recto(self):
        """If next add_page() would land on verso, insert a blank page first
        so the article opens on recto (odd)."""
        if self.pdf.page % 2 == 1:
            # Currently recto → next add_page() = verso; insert blank
            self.pdf.add_page()

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
        sizes  = {1: 20, 2: 14, 3: 11, 4: 10.5}
        colors = {1: C_DARK, 2: C_H2, 3: C_H3, 4: C_H3}
        sz  = sizes.get(level, 10)
        clr = colors.get(level, C_H3)

        # Space before heading — check for page break
        space_before = 8 if level <= 2 else 5
        if self.pdf.get_y() + space_before + sz * 0.6 > self.pdf.h - self.pdf.b_margin:
            self.pdf.add_page()
        else:
            self.pdf.ln(space_before)

        if level <= 3:
            self.pdf.set_font(self.SANS, "B", sz)
        else:
            # H4: serif, bold italic
            self.pdf.set_font(self.SERIF, "BI", sz)
        self.pdf.set_text_color(*clr)

        # Ensure x is at left margin before multi_cell
        self.pdf.set_x(self.pdf.l_margin)
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

        # Reset paragraph counter (next paragraph = no indent)
        self._para_index = 0
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

            # Image-with-caption pattern
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

            # First-line indent for subsequent paragraphs
            if self._para_index > 0:
                self.pdf.set_x(self.pdf.l_margin + self.INDENT_MM)

            self._render_inline(inline_tok.children)
        elif inline_tok.content:
            if self._para_index > 0:
                self.pdf.set_x(self.pdf.l_margin + self.INDENT_MM)
            self.pdf.write(self._lh, self._t(inline_tok.content))

        self._para_index += 1
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

            bullet = f"{idx}. " if ordered else "\u2022 "
            self.pdf.cell(7, self._lh, self._t(bullet))

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
        """Ornamental section break:  — ✦ —  """
        self.pdf.ln(4)
        self.pdf.set_font(self.SERIF, "", 12)
        self.pdf.set_text_color(*C_GOLD)
        ornament = self._t("\u2014 \u2726 \u2014")
        self.pdf.cell(0, 6, ornament, align="C",
                      new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(4)
        self._restore_body()

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
                i += 2
                if inline:
                    level = int(tok.tag[1])
                    self._render_heading(level, inline)

            elif tp == "paragraph_open":
                inline = tokens[i + 1] if i + 1 < len(tokens) else None
                i += 2
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
        self.pdf.set_font(self.SERIF, "", self.BODY_SIZE)
        self.pdf.set_text_color(*C_BLACK)
        self._text_color = C_BLACK
        self._link_href = None

    # ---------------------------------------------------------------
    #  Table of Contents renderer  (callback for insert_toc_placeholder)
    # ---------------------------------------------------------------
    def _render_toc(self, pdf, outline):
        """Render the Table of Contents with leader dots."""
        start_page = pdf.page

        pdf.set_font(self.SANS, "B", 22)
        pdf.set_text_color(*C_DARK)
        pdf.cell(0, 15, self._t("Table of Contents"), align="C",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        y = pdf.get_y()
        pdf.set_draw_color(*C_GOLD)
        pdf.set_line_width(0.7)
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(8)

        pw = pdf.w - pdf.l_margin - pdf.r_margin

        for entry in outline:
            level = entry.level
            page  = entry.page_number
            name  = entry.name

            if level == 0:
                # Part — extra top spacing before each Part
                if pdf.get_y() > pdf.t_margin + 10:
                    pdf.ln(3)
                pdf.set_font(self.SANS, "B", 10.5)
                pdf.set_text_color(*C_DARK)
                indent  = 0
                line_h  = 6.5
                spacing = 1.5
            elif level == 1:
                pdf.set_font(self.SERIF, "", 9.5)
                pdf.set_text_color(*C_H2)
                indent  = 8
                line_h  = 5.5
                spacing = 0.5
            else:
                # Sub-section (level 2+)
                pdf.set_font(self.SERIF, "I", 8.5)
                pdf.set_text_color(*C_GRAY)
                indent  = 14
                line_h  = 5.0
                spacing = 0.2

            if pdf.get_y() + line_h > pdf.h - pdf.b_margin:
                pdf.add_page()

            x0 = pdf.l_margin + indent
            pdf.set_x(x0)

            # Measure text width
            name_w = pdf.get_string_width(name)
            page_str = str(page)
            page_w = 12

            avail_w = pw - indent - page_w

            # Print entry name (truncated if needed)
            pdf.cell(min(name_w + 2, avail_w), line_h, name)

            # Leader dots
            dot_start = x0 + min(name_w + 2, avail_w)
            dot_end   = pdf.w - pdf.r_margin - page_w
            if dot_end > dot_start + 4:
                saved_font = (pdf.font_family, pdf.font_style, pdf.font_size_pt)
                pdf.set_font(self.SANS, "", 8)
                pdf.set_text_color(*C_LGRAY)
                pdf.set_x(dot_start)
                dot_w = pdf.get_string_width(" .")
                if dot_w > 0:
                    ndots = int((dot_end - dot_start) / dot_w)
                    dots = " ." * ndots
                    pdf.cell(dot_end - dot_start, line_h, dots)
                # Restore font for page number
                pdf.set_font(saved_font[0], saved_font[1], saved_font[2])
                if level == 0:
                    pdf.set_text_color(*C_DARK)
                else:
                    pdf.set_text_color(*C_H2)

            # Page number
            pdf.set_font(self.SANS, "", 9)
            pdf.set_text_color(*C_GRAY)
            pdf.set_x(pdf.w - pdf.r_margin - page_w)
            pdf.cell(page_w, line_h, page_str, align="R",
                     new_x="LMARGIN", new_y="NEXT")

            pdf.ln(spacing)

        # Pad remaining reserved pages
        pages_used = pdf.page - start_page + 1
        print(f"  TOC: {len(outline)} entries on {pages_used} pages (reserved {self._toc_pages})")
        while pages_used < self._toc_pages:
            pdf.add_page()
            pages_used += 1

    # ---------------------------------------------------------------
    #  Part title page  (full-page divider with Roman numeral)
    # ---------------------------------------------------------------
    def _render_part_title_page(self, part_num: int, title: str):
        """Insert an ornamental Part title page (always recto)."""
        self._ensure_recto()
        self.pdf._part_opener = True
        self.pdf.add_page()

        roman = _ROMAN[part_num] if part_num < len(_ROMAN) else str(part_num)

        # Vertical centering
        self.pdf.ln(60)

        # "PART XI" label
        self.pdf.set_font(self.SANS, "", 13)
        self.pdf.set_text_color(*C_GRAY)
        self.pdf.cell(0, 8, self._t(f"PART {roman}"), align="C",
                      new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(4)

        # Ornamental rule
        y = self.pdf.get_y()
        mid_l = self.pdf.l_margin + 25
        mid_r = self.pdf.w - self.pdf.r_margin - 25
        self.pdf.set_draw_color(*C_GOLD)
        self.pdf.set_line_width(0.7)
        self.pdf.line(mid_l, y, mid_r, y)
        self.pdf.ln(6)

        # Part title
        self.pdf.set_font(self.SANS, "B", 26)
        self.pdf.set_text_color(*C_DARK)
        self.pdf.multi_cell(0, 13, self._t(title), align="C",
                            new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(4)

        # Lower ornamental rule
        y = self.pdf.get_y()
        self.pdf.set_draw_color(*C_GOLD)
        self.pdf.set_line_width(0.7)
        self.pdf.line(mid_l, y, mid_r, y)

    # ---------------------------------------------------------------
    #  Heading-demoted token renderer (for sub-sections)
    # ---------------------------------------------------------------
    def _render_tokens_demoted(self, tokens: list, demote: int = 1):
        """Like _render_tokens but demotes heading levels by *demote*."""
        for tok in tokens:
            if tok.type == "heading_open" and tok.tag and tok.tag[0] == "h":
                old_level = int(tok.tag[1])
                new_level = min(old_level + demote, 6)
                tok.tag = f"h{new_level}"
        self._render_tokens(tokens)

    # ---------------------------------------------------------------
    #  Article + main entry  (3-tier: Part / Chapter / Sub-section)
    # ---------------------------------------------------------------
    def render_article(self, path: Path):
        text = path.read_text("utf-8")
        text = re.sub(r"<[A-Z][A-Za-z0-9]*[^>]*/?>", "", text)    # strip JSX
        text = re.sub(r"</?[A-Z][A-Za-z0-9]*>", "", text)          # strip closing JSX

        # Extract H1 title for the Table of Contents
        h1_match = re.match(r"^#\s+(.+)", text, re.MULTILINE)
        h1_title = h1_match.group(1).strip() if h1_match else path.stem

        # Classify into Part / Chapter / Sub-section
        tier, xx, yy, zz = _classify_tier(path.name)
        part_num = int(xx)
        roman = _ROMAN[part_num] if part_num < len(_ROMAN) else str(part_num)

        if tier == "part":
            # ── PART ──────────────────────────────────────────────
            self._current_part_xx = xx
            self._chapter_counter = 0
            self._current_part_num = part_num

            # Part title page
            self._render_part_title_page(part_num, h1_title)

            # Update running headers
            part_label = f"Part {roman} — {h1_title}"
            self.pdf.part_title = part_label
            self.pdf.chapter_title = h1_title
            self._chapter_title = h1_title

            # TOC entry (level 0)
            toc_label = f"Part {roman}:  {h1_title}"
            self.pdf.start_section(toc_label, level=0)

            # Render Part body on the next recto page
            self.pdf._chapter_opener = True
            self.pdf.add_page()
            self._para_index = 0

            # Small Part reference label at top
            self.pdf.set_font(self.SANS, "", 7.5)
            self.pdf.set_text_color(*C_GRAY)
            self.pdf.cell(0, 4, f"Part {roman}",
                          new_x="LMARGIN", new_y="NEXT")
            self.pdf.ln(1)

            self._restore_body()
            tokens = self.md.parse(text)
            self._render_tokens(tokens)

        elif tier == "chapter":
            # ── CHAPTER ───────────────────────────────────────────
            self._chapter_counter += 1
            ch_num = self._chapter_counter

            # Recto opener
            self._ensure_recto()
            self.pdf._chapter_opener = True
            self.pdf.add_page()
            self._para_index = 0

            # Update running header
            self.pdf.chapter_title = h1_title
            self._chapter_title = h1_title

            # Chapter label
            self.pdf.set_font(self.SANS, "", 7.5)
            self.pdf.set_text_color(*C_GRAY)
            self.pdf.cell(0, 4, f"Part {roman}, Chapter {ch_num}",
                          new_x="LMARGIN", new_y="NEXT")
            self.pdf.ln(1)

            # TOC entry (level 1)
            toc_label = f"Chapter {ch_num}:  {h1_title}"
            self.pdf.start_section(toc_label, level=1)

            self._restore_body()
            tokens = self.md.parse(text)
            self._render_tokens(tokens)

        else:
            # ── SUB-SECTION ───────────────────────────────────────
            # No page break — continue on the current page
            self._render_hr()
            self._para_index = 0

            # TOC entry (level 2)
            toc_label = h1_title
            self.pdf.start_section(toc_label, level=2)

            # Demote headings: H1 → H2, H2 → H3, etc.
            self._restore_body()
            tokens = self.md.parse(text)
            self._render_tokens_demoted(tokens, demote=1)

    def generate(self):
        EXPORT_DIR.mkdir(exist_ok=True)
        md_files = sorted(CONTENT_DIR.rglob("*.md"))
        if not md_files:
            sys.exit("No markdown files in content/")

        n = len(md_files)
        print(f"Generating PDF from {n} content files ...")
        print(f"  Format: {PAGE_W_MM} x {PAGE_H_MM} mm (6 x 9 in trade paperback)")
        print(f"  Margins: inside={MARGIN_INSIDE}mm outside={MARGIN_OUTSIDE}mm "
              f"top={MARGIN_TOP}mm bottom={MARGIN_BOTTOM}mm")

        # ---- Title page (page i) ----
        self.pdf.add_page()
        self.pdf.ln(55)
        self.pdf.set_font(self.SANS, "B", 36)
        self.pdf.set_text_color(*C_DARK)
        self.pdf.cell(0, 18, self._t("Paradigm Threat:"), align="C",
                      new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_font(self.SANS, "B", 28)
        self.pdf.set_text_color(*C_GOLD)
        self.pdf.cell(0, 14, self._t("The Third Story"), align="C",
                      new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(6)

        # Ornamental rule
        self.pdf.set_draw_color(*C_GOLD)
        self.pdf.set_line_width(0.7)
        mid_l = self.pdf.l_margin + 20
        mid_r = self.pdf.w - self.pdf.r_margin - 20
        self.pdf.line(mid_l, self.pdf.get_y(), mid_r, self.pdf.get_y())
        self.pdf.ln(8)

        # Edition label
        self.pdf.set_font(self.SANS, "I", 10)
        self.pdf.set_text_color(*C_GRAY)
        self.pdf.cell(0, 7, self._t("Early Draft \u2014 Not for Distribution"),
                      align="C", new_x="LMARGIN", new_y="NEXT")
        self.pdf.ln(3)

        # Version
        self.pdf.set_font(self.SANS, "", 11)
        self.pdf.cell(0, 8, self._t(f"Version {PKG_VERSION}"), align="C",
                      new_x="LMARGIN", new_y="NEXT")

        # ---- Copyright page (page ii — verso) ----
        self.pdf.add_page()
        self.pdf.ln(80)
        self.pdf.set_font(self.SERIF, "", 9)
        self.pdf.set_text_color(*C_GRAY)
        copyright_text = (
            "Copyright \u00a9 Paradigm Threat Research Project\n"
            "All rights reserved.\n\n"
            "Early draft \u2014 not for distribution.\n"
            f"Version {PKG_VERSION}"
        )
        self.pdf.multi_cell(0, 5, self._t(copyright_text),
                            align="C", new_x="LMARGIN", new_y="NEXT")

        # ---- Table of Contents (starts page iii) ----
        self._toc_pages = 7
        self.pdf.insert_toc_placeholder(self._render_toc, pages=self._toc_pages)

        # End front matter — body content starts
        self.pdf._in_front_matter = False

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
