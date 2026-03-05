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

## 13. Page Budget & Content Size Targets

### Two-Book Strategy (decided Mar 5, 2026)

The appendix (Chapter 16) will be printed as a **separate companion volume**.
This removes the appendix from the main book's page budget entirely, allowing
a **max content approach**: pack the main timeline as densely as possible,
and overflow all extended evidence, dossiers, author profiles, and reference
tables into the appendix book without page-count anxiety.

#### Book 1: *Paradigm Threat: The Third Story* (main timeline)

Chapters 00–15 + 17 (credits). The chronological narrative.

| Metric | Current (Mar 2026) | Target |
|---|---|---|
| Body text words | 95,615 | ≤ 70,000 |
| Articles | 169 | ≤ 140 |
| Embedded images | ~110 | Keep all; compress later |
| Blank recto inserts | ~85 | ~70 (from article consolidation) |
| Est. text pages | ~319 | ≤ 280 |
| Est. total pages (incl. images, blanks, front matter) | ~440 | **≤ 350** |
| PDF file size | — | ≤ 12 MB |

#### Book 2: *Paradigm Threat: Appendix — Evidence & Profiles*

Chapter 16 only. Reference material, dossiers, author profiles, investigation
summaries, film/TV catalogs, chronological tables.

| Metric | Current (Mar 2026) | Target |
|---|---|---|
| Body text words | 21,827 | **No hard limit** — grow freely |
| Articles | 35 | No limit |
| Embedded images | ~31 | Keep all |
| Est. pages | ~100+ | No cap (trade paperback up to ~600) |
| PDF file size | — | ≤ 10 MB |

The appendix book is the **overflow reservoir**. When any main-timeline
article needs to shed detail, that detail moves to an appendix article.
New dossiers, profiles, and reference tables always go here. This is where
the "max content" approach lives — every piece of research we produce can
be included; the only constraint on the main book is narrative density.

#### How Cross-References Work Between Books

Main-timeline articles reference appendix articles with the standard link
format: `[Title](/timeline/evt-slug)`. On the website, this is a direct
link. In print, the main book includes a note: *"See companion volume:
Appendix — Evidence & Profiles."* The PDF generator will add this print
note automatically for any cross-reference to a Ch 16 article.

### Core Philosophy: Pack, Don't Pad

The main book should be **dense with research, not narrative**. Every paragraph
should convey facts, citations, or author thesis. Remove:

- Expository warm-up sentences ("In order to understand X, we must first…")
- Restated thesis from prior articles (use cross-references)
- Multi-sentence transitions between sections
- Preambles before block quotes (let the quote speak)
- Repeated definitions of recurring concepts (define once, link always)

### Voice Separation Rule

Each article has two modes of content. Keep them cleanly separated:

1. **The bulk: cited evidence, sources, and cross-references.** This is
   third-person investigative. Present claims with attribution: "Fomenko
   argues…", "Burroughs describes…", "Wells published…". This constitutes
   80%+ of article text.

2. **Author thesis (usually at end of article).** Clearly marked:
   *"Author's thesis (Ari Bencuya):"* or bold **I believe / I propose**.
   This is where personal sentiment, original synthesis, and interpretive
   conclusions go. Never interleaved with sourced claims.

### Topic Placement Rule: Last Significant Century + Appendix Book

**The bulk of a topic appears in the chapter for the last significant century
in which that topic is active.** Earlier chapters contain brief mentions with
cross-references forward. Extended evidence overflows to the **appendix book**.

| Topic | Last Significant Century | Main Book Article | Appendix Book |
|---|---|---|---|
| Mars literature | 19th–20th (publication) | 15.06.01 (reclassified nonfiction) | 16.10 (author profiles), 16.02 (contacts) |
| Predictive programming | 20th–21st (Wells→Card) | 15.01.00 (literature) | 16.01 (fiction as control), 16.03 (film/TV) |
| Deep State | 17th (Romanovs/British Empire) | 11.x (canonical) | — |
| Masons | 13th (Horde era) | 07.01.01 | — |
| Jesuits | 16th–17th (operations) | 10.x/11.x (canonical) | — |
| False flags | 21st (architecture) | 15.04.00 | 16.07 (investigation) |
| Nuclear weapons | 20th (1938+) | 14.07.00 | — |
| Maxwell/aether | 19th (suppression) | 13.06.00 | 16.09 (energy X-ref) |
| Weather control | 20th (1946+) | 14.08.00 | — |
| Historical antibodies | 21st (analysis) | 15.03.00 | 16.06 (profiles) |

Earlier chapters referencing these topics should use **one sentence + link**:
*"For the full encoding analysis, see [Predictive Programming: Literature](/timeline/evt-20th-century-predictive-programming-literature)."*

### Reduction Strategy for Main Book (updated Mar 2026)

1. **Pack prose: eliminate waste.** Every sentence must carry information.
   Remove warm-ups, restated theses, narrative padding, multi-sentence
   transitions. Target: 300–600 words per timeline article; 800–1500 for
   canonical topic articles.

2. **Consolidate articles to reduce recto blanks.** Merge child articles
   under 300 words into parents. Target: ≤ 140 articles (saves ~15
   blank pages).

3. **Move extended evidence to appendix book.** Main-timeline articles
   present thesis + key evidence + cross-references. The appendix book
   holds the full dossier. No limit on appendix growth.

4. **Cross-reference, don't repeat.** One canonical article per topic.
   All other mentions: one sentence + link. Zero duplicate paragraphs.

5. **Trim the large files in the main book.** Files over 1500 words in
   Ch 00–15 need targeted reduction:
   - Move tables/dossiers to appendix book
   - Convert block quotes to cited summaries
   - Eliminate repeated material

6. **Keep all images; compress later.** Images stay in place for now.
   Final pass before print: reduce to 800px max width, JPEG quality 72,
   greyscale conversion.

### Priority Order for Main Book Reduction

| Priority | Action | Est. page savings |
|---|---|---|
| 1 | Pack prose globally (remove waste) | ~30 pages |
| 2 | Consolidate small articles (169 → ≤ 140) | ~15 pages (recto inserts) |
| 3 | Move evidence overflow to appendix book | ~20 pages |
| 4 | Cross-reference deduplication | ~10 pages |
| 5 | Trim largest main-book files | ~15 pages |
| 6 | Image compression (final pass) | file size only |
| **Total estimated** | | **~90 pages** |

This brings the main book from ~440 to ~350 pages — well within the 400-page limit,
with headroom to add new content as research continues.

### Tracking

Progress on content reduction is tracked in `docs/CONTENT_REDUCTION_TRACKER.md`.
Every reduction pass should log:
- Date, chapter/file affected, words before → after, technique used.

---

## 14. Vellum Feature Parity Checklist

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

Check the output file size and page count printed at the end.

**Current status (Feb 2026):** 176 articles → 792 pages, 47 MB.  
**Target:** ≤ 350 pages, ≤ 12 MB. See §13 *Page Budget & Content Size Targets*.
