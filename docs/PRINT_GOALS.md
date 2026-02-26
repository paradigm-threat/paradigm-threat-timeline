# Print Production Goals — Paradigm Threat: The Third Story

## Purpose

This document defines the print quality target for `export/timeline.pdf`.
The benchmark is the output Vellum produces for trade-paperback and black-and-white
print editions. All requirements here are implemented in `scripts/generate-pdf.py`.

---

## 1. Page Setup

| Attribute | Value | Notes |
|---|---|---|
| Format | 6″ × 9″ (152.4 mm × 228.6 mm) | Standard US trade paperback — default Vellum format |
| Orientation | Portrait | |
| Color mode | Black & white (greyscale) | Primary edition. Color edition: same spec, JPEG quality raised |
| PDF version | PDF 1.4 | All fonts embedded; compatible with print-on-demand (KDP, IngramSpark) |

---

## 2. Margins & Gutter

Margins are **mirrored** (recto/verso) to allow for spine binding.

| Page side | Inside (gutter) | Outside | Top | Bottom |
|---|---|---|---|---|
| Recto (odd) | 25 mm | 16 mm | 20 mm | 22 mm |
| Verso (even) | 16 mm | 25 mm | 20 mm | 22 mm |

Running header and page-number areas are within the top/bottom margin zones.

---

## 3. Typography

### Body Text
| Attribute | Value |
|---|---|
| Font | Liberation Serif (metrically identical to Times New Roman) |
| Size | 11 pt |
| Leading | 15 pt (line height) |
| Alignment | Justified |
| First paragraph after heading/break | No indent (block style) |
| Subsequent paragraphs | 5 mm first-line indent |
| Paragraph spacing | 0 pt between; indent distinguishes paragraphs |

> **Preferred upgrade**: Download EB Garamond or Libre Baskerville from Google Fonts
> and place in `fonts/` directory. The script detects these automatically. See §8.

### Headings
| Level | Font | Size | Weight | Colour | Treatment |
|---|---|---|---|---|---|
| H1 (article title) | Liberation Sans | 20 pt | Bold | Near-black (#111) | Gold rule beneath |
| H2 | Liberation Sans | 14 pt | Bold | Dark grey (#2c2c2c) | Light grey rule beneath |
| H3 | Liberation Sans | 11 pt | Bold | Medium grey (#3a3a3a) | No rule |
| H4 | Liberation Serif | 10.5 pt | Bold Italic | Medium grey | No rule |

### Supporting Text
| Element | Font | Size | Style |
|---|---|---|---|
| Section number (above H1) | Liberation Sans | 7.5 pt | Regular, grey |
| Block quote | Liberation Serif | 10 pt | Italic, indented, gold left bar |
| Caption | Liberation Sans | 8.5 pt | Italic, centred, grey |
| Code/fence | Liberation Mono | 8 pt | Regular, grey background |
| Table header | Liberation Sans | 7.5 pt | Bold, light grey fill |
| Table body | Liberation Sans | 7 pt | Regular |

---

## 4. Running Headers

Alternating chapter-aware headers on every page except chapter openers and blank pages.

| Page type | Left side | Right side |
|---|---|---|
| Verso (even) | Book title in small caps | Page number (outer edge) |
| Recto (odd) | Page number (outer edge) | Chapter/article title in small caps |

- Separated from body by a 0.3 pt horizontal rule
- Font: Liberation Sans, 7.5 pt, medium grey
- Chapter title is truncated to 55 characters

---

## 5. Chapter Openings

Each content article starts on a **recto (odd-numbered) page**. If the previous
article ends on an odd page, a blank verso is inserted automatically.

The chapter-opening page has:
- No running header
- Section number in small grey type, top-left
- Large centred article title (20 pt bold)
- Gold ornamental rule beneath title
- Body begins ~12 mm below rule

---

## 6. Page Numbers

- Position: outer bottom corner (right on recto, left on verso)
- Font: Liberation Sans, 8 pt, grey
- Version string printed on inner bottom corner, 7 pt, light grey
- Front matter (title page, copyright, TOC) uses no page numbers
- Body content starts at page 1 (Arabic numerals)

---

## 7. Front Matter

### Title Page (page i)
- Book title: 36 pt bold sans, centred, near-black
- Subtitle: 28 pt bold sans, centred, gold
- Gold ornamental rule
- Edition label: 10 pt italic sans, grey
- Version string: 11 pt sans

### Copyright Page (page ii — verso)
Blank or minimal copyright block. Placeholder:
```
Copyright © Paradigm Threat Research Project
All rights reserved.
Early draft — not for distribution.
```

### Table of Contents (starts page iii)
- Title: "Table of Contents", 22 pt bold sans
- Gold rule beneath title
- Chapter entries (level 0): 10.5 pt bold sans, full width, leader dots to page number
- Article entries (level 1): 9.5 pt serif, indented 8 mm, leader dots to page number
- Leader dots: evenly spaced periods filling space between title and page
- Page number: right-aligned, 9 pt sans, grey
- Reserves 6 pages (auto-expands)

---

## 8. Images

| Attribute | Value |
|---|---|
| Max width | 120 mm (fits within text block with margins) |
| Max height | 100 mm |
| Max source resolution | 1400 px wide (downsampled with LANCZOS) |
| Embedded format | JPEG |
| JPEG quality | 82 (B&W edition) / 88 (color edition) |
| Captions | Centred italic below image |
| Remote images | Skipped (print requires embedded assets) |

---

## 9. Section Breaks (HR)

Horizontal rules in source markdown are rendered as a centred ornamental break:
```
— ✦ —
```
Font: Liberation Serif, 12 pt, gold colour. No line drawn.

---

## 10. Special Blocks

| Block | Rendering |
|---|---|
| Blockquote | Indented 10 mm, italic serif, gold 1 mm left bar |
| Code fence | 0.5 mm left/right pad, light grey background, monospace 8 pt |
| Inline code | Monospace, 1.5 pt smaller than surrounding text |
| Ordered/unordered lists | 7 mm indent, hanging bullet/number |

---

## 11. Font Upgrade Path

The script searches for fonts in this priority order:
1. `fonts/` directory in the repo root (place downloaded fonts here)
2. System fonts (`/usr/share/fonts`, `~/.local/share/fonts`, etc.)
3. Fallback: built-in fpdf2 fonts (Helvetica/Times/Courier — Latin-1 only)

**Recommended fonts** (free, open source, drop into `fonts/`):

| Use | Font | Source |
|---|---|---|
| Body serif | EB Garamond | fonts.google.com/specimen/EB+Garamond |
| Alternative body | Libre Baskerville | fonts.google.com/specimen/Libre+Baskerville |
| Headings sans | Libre Franklin | fonts.google.com/specimen/Libre+Franklin |
| Mono | JetBrains Mono | jetbrains.com/lp/mono |

Download the TTF files and place them in `fonts/` at the repo root.
The script will detect them automatically without any code changes.

---

## 12. DOCX Export

`export/timeline.docx` is maintained as a separate editing artefact.
It uses its own script (`scripts/generate-docx.py`) and is **not** affected
by PDF print changes. Its purpose is collaborative editing and Word-compatible
review, not final print output.

---

## 13. Vellum Feature Parity Checklist

| Vellum Feature | Status | Implementation |
|---|---|---|
| 6×9 trade paperback format | ✅ | `format=(152.4, 228.6)` in fpdf2 |
| Mirrored margins (gutter) | ✅ | Recto/verso margin swap in `header()` |
| Running headers (chapter/book title) | ✅ | `header()` override with chapter tracking |
| Recto chapter starts | ✅ | Blank verso inserted when needed |
| Justified body text | ✅ | `align="J"` on `multi_cell` |
| First-line indent (post-heading block) | ✅ | State-tracked `_first_para` flag |
| TOC with leader dots | ✅ | Dot-fill algorithm in `_render_toc()` |
| Professional serif body font | ✅ | Liberation Serif (upgradeable to Garamond) |
| Ornamental section breaks | ✅ | `— ✦ —` centred gold glyph |
| Page numbers (outer edge) | ✅ | `footer()` recto/verso aware |
| Widow/orphan control | ⚠️ Partial | fpdf2 auto-page-break prevents most; full control needs Typst/LaTeX |
| Large print edition | 🔲 Planned | Font-size parameter (`--large-print`) |
| EPUB output | 🔲 Planned | Pandoc pipeline from same markdown source |
| PDF/X-1a compliance | 🔲 Planned | WeasyPrint or Typst for full PDF/X-1a |
| Metadata/ISBN embedding | 🔲 Planned | `pdf.set_title()`, `pdf.set_author()` — trivial add |

---

## 14. Running the Export

```bash
# Standard B&W print
npm run generate-pdf

# Or directly
source .venv/bin/activate
python3 scripts/generate-pdf.py

# Output: export/timeline.pdf
```

Check the output file size and page count printed at the end. A 160-article
export typically produces ~350–450 pages at 2–3 MB.
