# Agent Instructions for paradigm-threat-timeline

## Overview

paradigm-threat-timeline is a standalone project. It does NOT reference paradigm-threat-files. paradigm-threat-site loads timeline catalogs via Relay QUERY (`content_events` / `path_tree`); markdown and assets are served from the timeline repo tip.

**Guiding principles:** Victors write the history. Mass-redaction may have occurred after world wars, plagues, or regime changes. Add all relevant dates; attempt alternate dates for each chronology system. Absence of a source does not mean it never existed.

**Investigative strategy:** See `docs/INVESTIGATIVE_STRATEGY.md`. We treat every possibility as open from scratch; do not rule out claims due to "scientific consensus" or "lack of evidence" alone. Predictive programming and media patterns are data. When an old belief was the default (e.g. aether), the burden of proof is on the new scientists. When unsure, ask for interpretation.

## Prose emphasis in `content/`

Markdown under `content/` is book-facing narrative. Use **bold** and *italic* sparingly for rhetorical stress—about **one to four** emphasized spans per paragraph on average—not word-by-word highlighting. Full rules: `docs/CONTENT_MARKDOWN_STYLE.md`.

## Content File Numbering Convention

**Source of truth:** The `content/` folder. ``content/` is indexed on the relay via `content_events`. Validate locally with `npm run validate-events`.

All articles live in `content/` and use the filename format `XX.YY.ZZ-slug.md`.

| Segment | Meaning |
|---|---|
| `XX` | Chapter number (01–17). **Never change.** |
| `YY` | Position within chapter. `00` = chapter root. |
| `ZZ` | `00` = standalone / parent article. **Non-zero = child of `XX.YY.00`.** |

### Hierarchy rules (derived from XX.YY.ZZ in filenames)

- Chapter root → `XX.00.00` (top-level in `entries[]`)
- Direct children of chapter root → `XX.YY.00` (YY = 01, 02, …)
- Children of a `XX.YY.00` article → `XX.YY.01`, `XX.YY.02`, … (ZZ = position among siblings)
- Grandchildren are flattened into the same `XX.YY.ZZ` space (3-level max)

**Key invariant:** `ZZ = 00` ↔ article is not a child of any other article. `ZZ ≠ 0` ↔ sub-article.

### Dates

Dates are extracted from the filename slug when present:
- `1664-1694` → range 1664–1694 CE
- `1774-ce` → single year 1774 CE
- `4077-bce` → single year 4077 BCE

### Event metadata (YAML frontmatter in `content/` only)

Timeline **chapter** markdown under `content/` may start with a `---` block for **event machine fields** (`id`, `dates`, `media`, `related_events`, `duplicate_of`, etc.) consumed by `build-events-from-content.py`. This is **not** the same as paradigm-threat-files **article** hub frontmatter (`title:`, `description:`, `keywords:`) — those article fields belong in the **body** (`#` title, `> **TL;DR:**`, `Keywords:` line). Do **not** add article-style hub YAML to timeline chapters.

### When adding a new content file

1. Create the markdown file in the correct chapter subfolder with `XX.YY.ZZ-slug.md` naming.
2. Run `npm run validate-events` (pre-commit runs it). Push to relay remotes to refresh QUERY indexes.

## Adding Events

1. Create the markdown file in `content/` with `XX.YY.ZZ-slug.md` naming.
2. The first `#` header becomes the `title` in `events.json`.
3. Run `python3 scripts/build-events-from-content.py` and `npm run validate-events`.

## Event Schema

- **id**: Unique (e.g. `evt-1774-pugachev`)
- **title**: Must exactly match first `#` header in md_path file
- **md_path**: Path relative to repo root (e.g. `events/ce-1774-pugachev-rebellion.md`)
- **dates**: Array of `{ start, end?, calendar, source?, confidence?, note? }` — **add multiple dates** for different chronology systems. Use section end for `end` if unknown.
- **section**: Assigned by refactor-sections (BCE Option A or CE century)
- **timeline_sources**: Per-event override; omit to inherit from section. e.g. Saturnian, Fomenko, MudFlood, Mars
- **context**: `{ mainstream, theoretical }`
- **level**: From hierarchy (header level in source #=1, ##=2, ###=3, ####=4; 1 = top)
- **media**: Optional URLs for thumbnails/assets

## Multiple Dates per Event

Add **all relevant dates** from every chronology system you can find. Each entry in `dates[]` can have:

- `start`: year (negative = BCE)
- `end`: year; use section end if unknown
- `calendar`: BCE or CE
- `source`: e.g. "Saturnian/Jno Cook", "Fomenko", "Scaligerian", "Judaic", "Byzantine", "indigenous"
- `note`: Explain shifts, e.g. "Fomenko: 1053-year phantom", "same event as crucifixion"
- `confidence`: optional

Chronology systems to consider: Saturnian, Fomenko, Scaligerian, Phantom Time, Byzantine, Alexandrian, Judaic, indigenous (Quiche Maya, etc.).

## Fomenko Duplicates

When correlating duplicate events (e.g. 774 CE ↔ 1774 Pugachev):
- Add `duplicate_of` pointing to the canonical event id.
- Add `related_events` for linked events.
- Add `note` in `dates[]` explaining the shift (e.g. phantom time +1000 years).

## Scripts

- **build_events_from_content.py**: Builds the event graph from `content/` (validation / `--json`). Hierarchy from XX.YY.ZZ. Dates from filename slug. Optional fields from YAML frontmatter. Relay indexes the same shape via `content_events`.
- **validate-events.py**: Checks schema and title/header match. Run after edits.
- **audit-missing.py**: Verifies every `content/*.md` matches `XX.YY.ZZ-slug.md` so it can be indexed.
- **audit-links.py**: Audits `/timeline/evt-xxx` links in content against events.json. Reports broken links.
- **apply-link-fixes.py**: Applies link fixes from `scripts/link-fix-mapping.json`. Use `--apply` to modify files.

### Link audit workflow

See `docs/LINK_AUDIT.md` for the full audit report. To fix broken timeline links:

1. Resolve duplicate XX.YY.ZZ (see LINK_AUDIT §1) so the build succeeds.
2. Review and approve link fix mapping in `docs/LINK_AUDIT.md` and `scripts/link-fix-mapping.json`.
3. Run `python scripts/apply-link-fixes.py --apply`.
4. Run `python scripts/audit-links.py` to confirm zero broken links.

## Running Scripts

```bash
# After adding/editing content:
npm run validate-events
npm run validate-events
npm run audit-missing

# Or just commit — pre-commit runs the above automatically.
```

## Investigations (Knowledge Pool)

Investigations live in **paradigm-threat-files** (separate repo), not in the timeline repo. Topic index: e.g. `history/chronology/investigations/index-investigations.md`, `governance/war/investigations/`, `cosmos/mars/investigations/`. Link from timeline articles using root-relative paths (e.g. `/history/chronology/investigations/wuxing-five-planets-dark-ages.md`).

### Coherence workflow

- **Before writing or editing any timeline article**, scan paradigm-threat-files investigations for relevant prior research. This prevents contradictions and keeps assertions in sync across the timeline.
- If an investigation supports or contradicts a timeline claim, cross-reference it or flag the contradiction in `docs/OUTSTANDING_QUESTIONS.md`.
- New research conducted while editing the timeline should be added to **paradigm-threat-files** under the appropriate topic folder (e.g. `history/chronology/investigations/`).

### Investigations are NOT part of the book

- Investigation files are **excluded** from PDF/DOCX exports. They are web-only reference material.
- Timeline articles in `content/` must **not** use relative paths to investigations (e.g. `../../investigations/...`) — these won't resolve in the printed book.
- Instead, link to the live website's Browser mode:
  ```
  [See: Title](/path/to/investigation.md)
  ```
- Investigations may later become a separate publication or online article series.

### Source validation

- Use `investigations/` for source validation (e.g. tracing creation dates, verifying claims).
- When a cited source cannot be found online or in mainstream refs: assume redaction or gatekeeping before assuming error. Document the gap.

## Content Strategy

See `docs/CONTENT_STRATEGY.md` for:
- Writing style alignment (voice, thesis blocks, cross-references)
- Pacing and organization recommendations
- Contradiction handling and OUTSTANDING_QUESTIONS workflow
- Content placement rules (canonical article + references + appendix)
- Periodic rescan checklist and triggers

**Never implement strategy recommendations without user approval.**

## Updating OUTSTANDING_QUESTIONS.md

When you find contradictions, unresolved dates, or need clarification, add entries to `docs/OUTSTANDING_QUESTIONS.md`.

## Updating CONCLUSIONS.md

When the timeline supports a conclusion or speculation, add it to `docs/CONCLUSIONS.md`. Mark confidence level when uncertain.

## Media and generated images

- Article images can live in `media/[section]/[image]` (e.g. `media/before-creation/spawning-first-life-forms.png`). Link from markdown with **relative** paths (e.g. `media/[section]/[filename]`).
- paradigm-threat-site resolves these relative URLs to absolute using the same domain as `events.json` (the timeline base URL), so images load from the timeline origin.
- We plan to generate images for more timeline articles in the future (e.g. AI-generated illustrations keyed to article content).

## Print Size Budget (≤ 350 pages)

The PDF export must stay within a **≤ 350 page / ≤ 12 MB** budget for trade-paperback viability. As of Feb 2026 it is **792 pages / 47 MB** — well over the target.

### Writing guidelines for print-aware content

1. **Brevity first.** New articles should target **300–800 words**. Anything over 1,500 words needs justification.
2. **Cross-reference, don't repeat.** If a topic is covered in another article, write one sentence + a cross-reference (`See §XX.YY.ZZ Title`) instead of re-explaining.
3. **One image per article maximum** for print. Additional images are fine for the website but should be marked with `<!-- web-only -->` so the PDF generator can skip them.
4. **Avoid long block quotes.** Summarize and cite. Print page space is expensive.
5. **Merge small children.** Child articles under ~250 words should be folded into their parent unless they serve a distinct navigational purpose.
6. **Author profiles are appendix-only in print.** Keep full profiles in markdown for the website; the PDF renders a short-form version.

See `docs/PRINT_GOALS.md` §13 and `docs/CONTENT_REDUCTION_TRACKER.md` for the full strategy and tracking.
