# Agent Instructions for paradigm-threat-timeline

## Overview

paradigm-threat-timeline is a standalone project. It does NOT reference paradigm-threat-files. paradigm-threat-site fetches only `data/events.json` from the timeline; all markdown and assets are referenced from events.json.

**Guiding principles:** Victors write the history. Mass-redaction may have occurred after world wars, plagues, or regime changes. Add all relevant dates; attempt alternate dates for each chronology system. Absence of a source does not mean it never existed.

## Content File Numbering Convention

All articles live in `content/` and use the filename format `XX.YY.ZZ-slug.md`.

| Segment | Meaning |
|---|---|
| `XX` | Chapter number (01–15). **Never change.** |
| `YY` | Position within chapter. `00` = chapter root. |
| `ZZ` | `00` = standalone / parent article. **Non-zero = child of `XX.YY.00`.** |

### Hierarchy rules (derived from `data/events.json`)

- The first top-level `entries[]` item for each section XX is the chapter root → `XX.00.00`
- Direct children of the chapter root → `XX.01.00`, `XX.02.00`, … (YY = position in DFS order)
- Children of a `XX.YY.00` article → `XX.YY.01`, `XX.YY.02`, … (ZZ = position among siblings)
- Grandchildren are flattened into the same `XX.YY.ZZ` space (3-level max)
- Additional top-level `entries[]` siblings in the same section → `XX.NN.00` (continuing YY sequence)

**Key invariant:** `ZZ = 00` ↔ article is not a child of any other article. `ZZ ≠ 0` ↔ sub-article.

### When adding a new content file

1. Add the entry to the correct `children[]` array in `data/events.json` (set `md_path` to a placeholder).
2. Run `python3 scripts/renumber-from-hierarchy.py` — this assigns the correct number based on hierarchy position, renames all files, and updates all cross-links and `md_path` values.
3. Create the markdown file at the new path printed by the script.
4. Run `npm run validate-events && npm run audit-missing && npm run generate-index`.

### When the hierarchy changes

If you move an entry between parents, add children, or restructure `events.json`:
```bash
python3 scripts/renumber-from-hierarchy.py
npm run validate-events && npm run audit-missing && npm run generate-index
```

## Adding Events

1. Add an event to `data/events.json` following the schema in `data/timeline-schema.json`.
2. Create the corresponding markdown file in `content/` at the path assigned by the numbering convention (use `renumber-from-hierarchy.py` after placing the entry in `children[]`).
3. The first `#` header in the markdown file must exactly match the `title` field in `events.json`.
4. Run `python3 scripts/validate-events.py` to verify.

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

- **renumber-from-hierarchy.py**: Re-derives all `XX.YY.ZZ` numbers from the `events.json` hierarchy. Run whenever hierarchy changes. Updates filenames, `md_path` values, and cross-links.
- **generate-index.py**: Builds `index.json` (for file browser). Run on pre-commit.
- **validate-events.py**: Checks schema and title/header match. Run after edits.
- **audit-missing.py**: Verifies every `content/*.md` file is registered in `events.json`. Run after any file rename.
- **split-chronology.py**: Extracts events from paradigm-threat-files. Reads only; writes to timeline. Use `--source-dir` to point at paradigm-threat-files.
- **normalize-events.py**: Adds missing dates using the "last date header" rule, renames files to `bce-YYYY-` or `ce-YYYY-` format (era before year, start date only, no ranges). Run after split or when adding dates.
- **refactor-sections.py**: Assigns each event to a section (BCE Option A + CE centuries), moves duplicate timeline_sources to sections, keeps per-event sources when different. Run after split or normalize.

## Last Date Header Rule

The chronology page is the timeline. Sections without date headers occur within the date of the **last** preceding `###` that has a date. normalize-events.py applies this rule when assigning dates.

## Running Scripts

```bash
# After restructuring hierarchy (adding/moving entries in events.json):
python3 scripts/renumber-from-hierarchy.py

# Standard post-edit validation:
npm run validate-events
npm run audit-missing
npm run generate-index

# Older pipeline scripts (for re-importing from paradigm-threat-files):
npm run split-chronology
npm run normalize-events
npm run refactor-sections
```

## Investigations

- Use `investigations/` for source validation (e.g. tracing creation dates, verifying claims).
- When a cited source cannot be found online or in mainstream refs: assume redaction or gatekeeping before assuming error. Document the gap.
- See `investigations/README.md` for the investigation template and index.

## Updating OUTSTANDING_QUESTIONS.md

When you find contradictions, unresolved dates, or need clarification, add entries to `docs/OUTSTANDING_QUESTIONS.md`.

## Updating CONCLUSIONS.md

When the timeline supports a conclusion or speculation, add it to `docs/CONCLUSIONS.md`. Mark confidence level when uncertain.

## Media and generated images

- Article images can live in `media/[section]/[image]` (e.g. `media/before-creation/spawning-first-life-forms.png`). Link from markdown with **relative** paths (e.g. `media/[section]/[filename]`).
- paradigm-threat-site resolves these relative URLs to absolute using the same domain as `events.json` (the timeline base URL), so images load from the timeline origin.
- We plan to generate images for more timeline articles in the future (e.g. AI-generated illustrations keyed to article content).
