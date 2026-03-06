# paradigm-threat-timeline: Copilot Instructions

## Purpose

Alternate Earth History Timeline correlating Scaligerian, Fomenko's New Chronology, Saturnian Cosmology, and other sources. This project is an **investigation** into chronology, not a textbook. Assume redaction and victors' bias.

## Guiding Principles

1. **Victors write the history.** Mainstream (Scaligerian) dates may reflect those who controlled record-keeping.
2. **Mass-redaction is plausible.** World wars, plagues, regime changes, and church chronologists could have altered records at any time. Absence of a source ≠ it never existed.
3. **Add all dates.** For each event, add every relevant date from every chronology system we can find.

## Content File Numbering Convention

Files in `content/` are organized into chapter-specific subfolders that mirror the `media/` directory structure. Each file uses the format `XX.YY.ZZ-slug.md`:

- **XX** = chapter/section number (01–15). Never change this.
- **YY** = position within the chapter. `00` is reserved for the chapter root article.
- **ZZ** = `00` → standalone or parent article; **non-zero** → child/sub-article of `XX.YY.00`.

Content subfolders match media subfolders by chapter number:
- `content/00.overview/` — overview, background, core concepts
- `content/01.before-creation/` — chapter 01
- `content/02.the-golden-age/` — chapter 02
- …and so on for each chapter

The numbers must match the `children[]` hierarchy in `data/events.json`:
- Chapter root (top-level entry in `entries[]`) → `XX.00.00`
- Direct children of chapter root → `XX.YY.00` (YY = 01, 02, … in DFS order)
- Children of `XX.YY.00` → `XX.YY.01`, `XX.YY.02`, … (ZZ ≠ 0)
- Grandchildren are flattened into the same `XX.YY.ZZ` space as their parent group

**Rule:** `ZZ = 00` always means the article is NOT a child of any other article. `ZZ ≠ 0` always means it IS a child of `XX.YY.00`.

When adding a new content file:
1. Determine where it sits in the `events.json` hierarchy (parent entry).
2. Assign the next available `ZZ` number if it is a child, or the next `YY` if it is top-level.
3. Place the file in the correct chapter subfolder under `content/`.
4. Run `python3 scripts/renumber-from-hierarchy.py` any time the hierarchy changes to re-derive all numbers automatically.

## When Adding or Editing Events

- Use `data/timeline-schema.json` as the schema. Events live in `data/events.json`.
- `dates[]` supports **multiple entries** per event—one per chronology system. Include `source`, `note`, `confidence` when known.
- Chronology systems to consider: Saturnian, Fomenko, Scaligerian, Phantom Time, Byzantine, Alexandrian, Judaic, indigenous (Quiche Maya, etc.).
- Add `duplicate_of` and `related_events` for Fomenko-identified duplicates.
- Content markdown files live in `content/` and follow the `XX.YY.ZZ-slug.md` convention above. Title must match the first `#` header exactly.

## Investigations as Knowledge Pool

The `investigations/` folder is the project's **living knowledge base**. It contains research, debates, source analysis, and validation documents organized by topic (e.g. `investigations/maxwell-aether/`, `investigations/nuclear/`, `investigations/text/`).

### When adding or editing timeline content

- **Consult `docs/CONTENT_STRATEGY.md`** for writing style, content placement, and contradiction handling.
- **Always scan `investigations/` for relevant material** before writing or modifying assertions in `content/` articles. This ensures the timeline stays internally coherent and doesn't contradict established research.
- If an investigation supports or challenges a claim in the timeline, cross-reference it.
- If editing reveals a contradiction with existing investigations, flag it in `docs/OUTSTANDING_QUESTIONS.md` and optionally open a new investigation.
- New research or debates that inform timeline content should be added to `investigations/` under the appropriate topic folder.

### Investigations are NOT part of the book

- Investigation files are **not included** in the PDF/DOCX exports. They are reference material for the website only.
- **Do not** refer to investigation files as if they appear in the book's index or table of contents.
- **Do not** use relative paths like `../../investigations/...` in timeline articles — these work in the repo but not in the rendered book.
- Instead, link readers to the **website's Browser mode** using this URL format:
  ```
  [See: Investigation Title](https://paradigm-threat.net/timeline?view=browser&path=investigations/topic/filename.md)
  ```
  This deep-links directly to the `.md` file in the repo's file browser on the live site.
- Investigations may become the basis for a separate book, online articles, or supplementary web content.

### When investigating claims

- Use `investigations/` for validation research. Do not assume mainstream sources are complete or unaltered.
- If a cited source cannot be found: document the gap, add to `docs/OUTSTANDING_QUESTIONS.md`. Prefer "source may be redacted/lost" over "claimant made an error."
- See `investigations/index.md` for the full topic index.

## Scripts (run after edits)

After editing `data/events.json` or content markdown files:
```bash
npm run validate-events
npm run audit-missing
```

After changing the `children[]` hierarchy in `events.json` (adding/moving entries):
```bash
python3 scripts/renumber-from-hierarchy.py
npm run validate-events && npm run audit-missing && npm run generate-index
```

After adding or renaming any file in `content/`, `events/`, or `media/` (to update `index.json`):
```bash
npm run generate-index
```

> The husky pre-commit hook runs `generate-index` automatically on `git commit`, but run it manually after adding content files so `index.json` stays current during the session.

## Regenerating PDF / DOCX exports

The PDF and DOCX generators require Python packages (`fpdf2`, `markdown-it-py`, `Pillow`, `python-docx`) that are **not** installed system-wide. A venv at `.venv/` is used.

To regenerate both exports in one command:
```bash
npm run export
```

This runs `scripts/export.sh`, which:
1. Creates `.venv/` if it doesn't exist (`python3 -m venv .venv`)
2. Installs/upgrades the required packages (`fpdf2`, `markdown-it-py`, `Pillow`, `python-docx`) into the venv
3. Runs `generate-docx.py` using the venv Python
4. Converts DOCX → PDF via LibreOffice (`libreoffice --headless --convert-to pdf`); if LibreOffice is not installed, falls back to `generate-pdf.py`

**Do not** use bare `python3 scripts/generate-pdf.py` or `python3 scripts/generate-docx.py` — they will fail if the system Python lacks the dependencies. Always use `npm run export`.

> **LibreOffice dependency:** The PDF conversion requires `libreoffice` on the PATH. On Ubuntu/Debian: `sudo apt install libreoffice`. On macOS: `brew install --cask libreoffice`. Without it, the fallback native PDF generator produces lower-fidelity output.

## Image Generation (Golden Age vs Dark Age)

When generating or replacing illustrations for timeline articles:

- **Saturn’s rings:** Saturn does **not** have rings in BCE times, only in CE. In BCE/Golden Age images, do not draw Saturn with the distinct ring system; use a sunlike body, spoked wheel, or plasma halo/Absu only.

- **Venus vs Mars (Wheel of Heaven):** In Golden Age / BCE images, **Venus** is a **plasmoid** appearing as a **single** star figure (one 3–8 sided star, e.g. six- or eight-pointed)—luminous, plasma-like—not many stars or symbols. **Mars** always looks **solid** (a distinct spherical or solid body, not plasmoid). Do not show other symbols in the sky; only Mars, Venus (single star), and Saturn.

- **Golden Age (and before-creation / creation-era):** Always use **Saturnian Cosmology** backgrounds showing the **Wheel of Heaven**. The **northern hemisphere** looked like the Northern Hemisphere Configuration: **Saturn + Venus + Mars = Tree of Life**—central luminous body (Saturn as sunlike, no rings), polar view “up the magnetic tube,” central spoked wheel, eight-pointed Sun Wheel / Shamash-style motif, Dharmachakra-style wheel; plasma halo or Absu (no distinct planetary rings). Sky can transition from deep blue to hazy yellowish-orange near the horizon. The **southern hemisphere** looked like the Southern Hemisphere Configuration: **petroglyph images in the sky**—Uranus + Neptune + Mercury forming the squatting-man figure; purple-tinged, plasma-like sky with luminous swirls; white or glowing stylized petroglyph figures (anthropomorphic, zoomorphic, squatting-man, Kokopelli-style) superimposed in the sky as if ancient rock art were celestial; barren rocky landscape with ancient observers. This applies to any image set in or before the Golden Age.

- **Dark Age:** Do **not** show the Wheel of Heaven—it is no longer present. Instead show **Venus and Mars tethered together as the dragon** (the new celestial configuration of the Dark Age). No Saturnian polar wheel or sunlike Saturn in the sky.

## Blog Entries

Blog posts live in `blog/` and follow the naming convention `YYYY-MM-DD-slug.md`. They serve as changelogs and highlights for the project.

### When to create a new blog entry

Create a new blog entry whenever the user requests one, or when a significant batch of work has been completed.

### How to create a blog entry

1. **Gather changes since the last entry.** Run:
   ```bash
   git log --oneline --since="<date-of-last-blog-entry>" --no-decorate
   ```
   Use the date from the most recent file in `blog/` (e.g. `2026-03-01` for `2026-03-01-timeline-update.md`).

2. **Read the diff for new files.** For each commit, check what was added/changed:
   ```bash
   git diff --stat <oldest-commit>^..HEAD
   ```
   Pay special attention to **new files** — these deserve headline coverage.

3. **Highlight new content by topic.** Group changes into sections:
   - **New articles** — list each new content file with its chapter, title, and a 1–2 sentence summary
   - **New investigations** — list each new investigation file/folder with a description and a **Browser mode deep link**:
     ```
     [Investigation Title](https://paradigm-threat.net/timeline?view=browser&path=investigations/topic/filename.md)
     ```
   - **Structural changes** — hierarchy reorganizations, renumbering, chapter moves
   - **Export/tooling improvements** — PDF/DOCX changes, script updates
   - **Bug fixes** — notable fixes

4. **Include a Stats table** at the end comparing previous vs current metrics:
   - Version, entry count, word count, PDF pages, PDF size, content file count, image count
   - Get current stats from `npm run validate-events`, `npm run audit-missing`, and `wc -w content/**/*.md`.

5. **Use the same format** as existing blog entries (see `blog/` for examples): H1 title, date line, horizontal rules between sections, bold key terms.

6. **Include images.** Pick 1–3 choice images from `media/` that relate to the new content and embed them using **root-relative URLs**:
   ```markdown
   ![Alt text](/media/chapter-folder/image-name.png)
   ```
   Choose images that are visually striking and represent the key topics of the update.

7. **After creating the blog entry**, run:
   ```bash
   npm run generate-index
   ```
   to include the new blog file in `index.json`.

### Linking to investigations and browser-viewable files

Always use the **Browser mode deep link** format when referencing investigation files or any repo file that readers can view on the website:
```
[Title](https://paradigm-threat.net/timeline?view=browser&path=<relative-path>)
```
Examples:
- `[Death on Mars Analysis](https://paradigm-threat.net/timeline?view=browser&path=investigations/mars/death-on-mars.md)`
- `[De Grazia Book Summaries](https://paradigm-threat.net/timeline?view=browser&path=investigations/de-grazia/books/chaos-and-creation.md)`

This ensures links work on the live site regardless of how the repo is hosted.

## Key Paths

- `data/events.json` — canonical event list and hierarchy
- `data/timeline-schema.json` — schema
- `content/` — article markdown files in chapter subfolders (`content/<chapter>/XX.YY.ZZ-slug.md`)
- `investigations/` — validation research
- `docs/INVESTIGATIVE_STRATEGY.md` — evidence, consensus, burden of proof; investigate from scratch; predictive programming as data; **when unsure, ask for interpretation**
- `docs/CONTENT_STRATEGY.md` — writing style, pacing, placement, contradictions, rescan schedule; **consult before content edits; never implement strategy changes without approval**
- `docs/AGENT_INSTRUCTIONS.md` — detailed agent guide
- `docs/PRINT_GOALS.md` — print specs and page budget
- `docs/CONTENT_REDUCTION_TRACKER.md` — tracks progress toward ≤ 350 page target
- `scripts/renumber-from-hierarchy.py` — re-derives all file numbers from `events.json` hierarchy
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
