# paradigm-threat-timeline: Copilot Instructions

## Purpose

Alternate Earth History Timeline correlating Scaligerian, Fomenko's New Chronology, Saturnian Cosmology, and other sources. This project is an **investigation** into chronology, not a textbook. Assume redaction and victors' bias.

## Guiding Principles

1. **Victors write the history.** Mainstream (Scaligerian) dates may reflect those who controlled record-keeping.
2. **Mass-redaction is plausible.** World wars, plagues, regime changes, and church chronologists could have altered records at any time. Absence of a source ≠ it never existed.
3. **Add all dates.** For each event, add every relevant date from every chronology system we can find.

## Content File Numbering Convention

**Source of truth:** The `content/` folder. `data/events.json` is **generated** from it by `build-events-from-content.py` (run automatically on pre-commit).

Files in `content/` are organized into chapter-specific subfolders that mirror the `media/` directory structure. Each file uses the format `XX.YY.ZZ-slug.md`:

- **XX** = chapter/section number (01–17). Never change this.
- **YY** = position within the chapter. `00` is reserved for the chapter root article.
- **ZZ** = `00` → standalone or parent article; **non-zero** → child/sub-article of `XX.YY.00`.

Content subfolders match media subfolders by chapter number:
- `content/00.overview/` — overview, background, core concepts
- `content/01.before-creation/` — chapter 01
- `content/02.the-golden-age/` — chapter 02
- …and so on for each chapter

**Hierarchy** (derived from XX.YY.ZZ in filenames):
- Chapter root → `XX.00.00` (top-level in `entries[]`)
- Direct children of chapter root → `XX.YY.00` (YY = 01, 02, …)
- Children of `XX.YY.00` → `XX.YY.01`, `XX.YY.02`, … (ZZ ≠ 0)

**Rule:** `ZZ = 00` always means the article is NOT a child of any other article. `ZZ ≠ 0` always means it IS a child of `XX.YY.00`.

**Dates:** When the filename slug contains a date pattern (e.g. `1664-1694`, `1774-ce`, `4077-bce`), dates are extracted automatically. Include date in the slug when the article has a timeline position.

**Optional fields (media, related_events, duplicate_of, etc.):** Add YAML frontmatter to the markdown file. See `scripts/build-events-from-content.py` for supported keys.

When adding a new content file:
1. Place the file in the correct chapter subfolder with the appropriate `XX.YY.ZZ-slug.md` name.
2. Run `python3 scripts/build-events-from-content.py` (or commit — pre-commit runs it).

## When Adding or Editing Events

- `content/` is the source of truth. `data/events.json` is generated from it.
- `dates[]` is extracted from the filename slug when present (e.g. `1664-1694`, `1774-ce`, `4077-bce`). For multiple chronology systems, use YAML frontmatter.
- Add `duplicate_of` and `related_events` in YAML frontmatter for Fomenko-identified duplicates.
- Content markdown files live in `content/` and follow the `XX.YY.ZZ-slug.md` convention above. Title is taken from the first `#` header.

## Investigations as Knowledge Pool

Investigations live in **paradigm-threat-files** (separate repo). They contain research, debates, source analysis, and validation documents organized by sphere: `governance/war/investigations/`, `cosmos/mars/investigations/`, `science/maxwell_aether/`, etc.

### When adding or editing timeline content

- **Consult `docs/CONTENT_STRATEGY.md`** for writing style, content placement, and contradiction handling.
- **Always scan paradigm-threat-files** for relevant investigations before writing or modifying assertions in `content/` articles. This ensures the timeline stays internally coherent and doesn't contradict established research.
- If an investigation supports or challenges a claim in the timeline, cross-reference it using root-relative paths (e.g. `/governance/war/investigations/filename.md`).
- If editing reveals a contradiction with existing investigations, flag it in `docs/OUTSTANDING_QUESTIONS.md` and optionally open a new investigation.
- New research or debates that inform timeline content should be added to paradigm-threat-files under the appropriate sphere folder.

## TL;DR (long `content/` articles)

When a timeline markdown file has **more than 12 paragraph-blocks** (see `docs/CONTENT_STRATEGY.md` § TL;DR for the counting rule), keep a TL;DR placeholder unless the user omits it on purpose.

- **Markup (option A):** a single blockquote with a bold label, immediately after the `#` title—or, if a hero image sits directly under the title, **immediately below that image**—then the body.

  ```markdown
  > **TL;DR:** TODO
  ```

  Replace **`TODO`** with one paragraph when running a model pass: compress what the article already says; **do not** add new claims; **do not** open with “this article,” “this chapter,” “this piece,” or “below.” See `docs/CONTENT_STRATEGY.md` § TL;DR for tone options.
- **If ≤12 paragraph-blocks:** omit TL;DR.

**Batch / refresh:** `npm run generate-tldr` inserts `> **TL;DR:** TODO` under `content/`. For paradigm-threat-files use `python3 scripts/generate_tldr.py --root ../paradigm-threat-files`. `--refresh-tldr` resets existing TL;DR lines to `TODO`.

### Investigations are NOT part of the book

- Investigation files are **not included** in the PDF/DOCX exports. They are reference material for the website only.
- **Do not** refer to investigation files as if they appear in the book's index or table of contents.
- **Do not** use relative paths like `../../investigations/...` in timeline articles — these work in the repo but not in the rendered book.
- Investigations live in **paradigm-threat-files** (separate repo). Use **root-relative URLs**:
  ```
  [See: Investigation Title](/governance/war/investigations/filename.md)
  ```
  Path prefixes: `governance/war/investigations/`, `events/false_flag/investigations/`, `cosmos/mars/investigations/`, `science/maxwell_aether/`, `influence/predictive_programming/fiction_encoding/`, etc. See paradigm-threat-files `REORGANIZATION_MAP.md` for full mapping.
- Investigations may become the basis for a separate book, online articles, or supplementary web content.

### When investigating claims

- Use paradigm-threat-files for validation research. Do not assume mainstream sources are complete or unaltered.
- If a cited source cannot be found: document the gap, add to `docs/OUTSTANDING_QUESTIONS.md`. Prefer "source may be redacted/lost" over "claimant made an error."
- See paradigm-threat-files and its `REORGANIZATION_MAP.md` for the investigation path index.

## Scripts (run after edits)

After adding, renaming, or editing content markdown files:
```bash
python3 scripts/build-events-from-content.py
npm run validate-events
npm run audit-missing
npm run generate-index
```

> The husky pre-commit hook runs `build-events-from-content`, `validate-events`, `audit-missing`, and `generate-index` automatically on `git commit`.

## Regenerating PDF / DOCX exports

The PDF and DOCX generators require Python packages that are **not** installed system-wide on many distros. **`npm run generate-pdf`**, **`npm run generate-docx`**, and **`npm run generate-exports`** use `scripts/run-with-export-venv.sh`, which creates `.venv/`, installs deps, and runs the generator — no manual venv step.

| Command | Output |
|---------|--------|
| `npm run generate-exports` | `export/timeline-book.pdf`, `timeline-appendix.pdf`, `timeline-book.docx`, `timeline-appendix.docx` (native fpdf2 PDFs + python-docx) |
| `npm run export` | DOCX via venv, then PDF via **LibreOffice** conversion (different PDF pipeline) |

`scripts/export.sh` still: venv → `generate-docx.py` → `libreoffice --headless --convert-to pdf`. Use **`generate-exports`** for the print-spec native PDFs in `PRINT_GOALS.md`.

**Do not** rely on bare `python3 scripts/generate-pdf.py` unless system Python has `fpdf2` etc. Prefer **`npm run generate-exports`**.

> **LibreOffice dependency (for `npm run export` only):** Without `libreoffice` on PATH, `export.sh` skips DOCX→PDF conversion. **`npm run generate-exports`** does not need LibreOffice.

## Image Generation (Golden Age vs Dark Age)

When generating or replacing illustrations for timeline articles:

- **Saturn’s rings:** Saturn does **not** have rings in BCE times, only in CE. In BCE/Golden Age images, do not draw Saturn with the distinct ring system; use a sunlike body, spoked wheel, or plasma halo/Absu only.

- **Venus vs Mars (Wheel of Heaven):** In Golden Age / BCE images, **Venus** is a **plasmoid** appearing as a **single** star figure (one 3–8 sided star, e.g. six- or eight-pointed)—luminous, plasma-like—not many stars or symbols. **Mars** always looks **solid** (a distinct spherical or solid body, not plasmoid). Do not show other symbols in the sky; only Mars, Venus (single star), and Saturn.

- **Golden Age (and before-creation / creation-era):** Always use **Saturnian Cosmology** backgrounds showing the **Wheel of Heaven**. The **northern hemisphere** looked like the Northern Hemisphere Configuration: **Saturn + Venus + Mars = Tree of Life**—central luminous body (Saturn as sunlike, no rings), polar view “up the magnetic tube,” central spoked wheel, eight-pointed Sun Wheel / Shamash-style motif, Dharmachakra-style wheel; plasma halo or Absu (no distinct planetary rings). Sky can transition from deep blue to hazy yellowish-orange near the horizon. The **southern hemisphere** looked like the Southern Hemisphere Configuration: **petroglyph images in the sky**—Uranus + Neptune + Mercury forming the squatting-man figure; purple-tinged, plasma-like sky with luminous swirls; white or glowing stylized petroglyph figures (anthropomorphic, zoomorphic, squatting-man, Kokopelli-style) superimposed in the sky as if ancient rock art were celestial; barren rocky landscape with ancient observers. This applies to any image set in or before the Golden Age.

- **Dark Age:** Do **not** show the Wheel of Heaven—it is no longer present. Instead show **Venus and Mars tethered together as the dragon** (the new celestial configuration of the Dark Age). No Saturnian polar wheel or sunlike Saturn in the sky.

## Blog Entries

**Blog posts live in paradigm-threat-files** (`paradigm-threat-files/blog/`), not in this repo. Add new blog entries there. See paradigm-threat-files `docs/BLOG.md` for conventions.

**Before drafting a new post:** Always run **`git log`** in **paradigm-threat-files**, **paradigm-threat-timeline**, and **paradigm-threat-site** since the **previous** `blog/YYYY-MM-DD-*.md` (see `docs/BLOG.md` § *Git history* in paradigm-threat-files). Do not summarize from memory alone. Target **~2×** typical 2026 roundup length and expanded per-item coverage — see `docs/BLOG.md` § *Length and depth*.

**URLs in blog files:** Use **fully absolute URLs** — `https://paradigmthreat.net/path` — for all links and images. Do not use relative paths.

### Linking to investigations and browser-viewable files

**Blog entries (`paradigm-threat-files/blog/*.md`):** Use **absolute URLs** — `https://paradigmthreat.net/path` — so links work when viewed in GitHub, RSS, or any context. Do not use relative paths like `/influence/...`.

**Timeline content (investigations, etc.):** Investigations live in **paradigm-threat-files**. Use **root-relative URLs** (no absolute domain):
```
[Title](/path/to/file.md)
```
Examples:
- `[Death on Mars Analysis](/cosmos/mars/death-on-mars-analysis.md)`
- `[De Grazia Book Summaries](/cosmos/cosmology/de_grazia/books/chaos-and-creation.md)`
- Timeline content: `/timeline?view=browser&path=content/...` or `/timeline/evt-...`

See paradigm-threat-files `REORGANIZATION_MAP.md` for the full path mapping.

## Key Paths

- `content/` — **source of truth**; one markdown file per timeline entry
- `data/events.json` — **generated** from content/ by `build-events-from-content.py`
- `data/timeline-schema.json` — schema
- `content/` — article markdown files in chapter subfolders (`content/<chapter>/XX.YY.ZZ-slug.md`)
- paradigm-threat-files — validation research (investigations)
- `docs/INVESTIGATIVE_STRATEGY.md` — evidence, consensus, burden of proof; investigate from scratch; predictive programming as data; **when unsure, ask for interpretation**
- `docs/CONTENT_STRATEGY.md` — writing style, pacing, placement, contradictions, rescan schedule; **consult before content edits; never implement strategy changes without approval**
- `docs/AGENT_INSTRUCTIONS.md` — detailed agent guide
- `docs/PRINT_GOALS.md` — print specs and page budget
- `docs/CONTENT_REDUCTION_TRACKER.md` — tracks progress toward ≤ 350 page target
- `scripts/build-events-from-content.py` — generates `events.json` from content/ file structure
- `scripts/` — all other Python utility scripts

## Print Size Budget

The PDF is currently **~792 pages / 47 MB** — the target is **≤ 350 pages / ≤ 12 MB**.
When writing or editing content:
- Keep articles to **300–800 words**; justify anything over 1,500.
- **Cross-reference** overlapping topics instead of repeating material.
- Limit to **1 image per article** for print; mark extras `<!-- web-only -->`.
- Avoid long block quotes — summarize and cite.
- Merge child articles under ~250 words into their parent.
- See `docs/PRINT_GOALS.md` §13 and `docs/CONTENT_REDUCTION_TRACKER.md`.

## Main Article vs. Appendix Overflow

**The main article must stand alone.** All key dates, facts, event catalogues, thesis arguments, and tables must appear in the main article — never deferred to the appendix. A reader who never opens the appendix should still understand the full topic.

Appendix articles are for **extended evidence only**: primary-source quotations, detailed source-by-source analysis, exhaustive bibliographies, and chronological sub-dossiers. If the main article is just a stub pointing at the appendix, it has failed.

**Anti-overflow test:** Before creating or editing an appendix article, ask: "Does the main article stand alone without this?" If not, move the missing material into the main article first.
