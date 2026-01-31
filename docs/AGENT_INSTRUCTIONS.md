# Agent Instructions for paradigm-threat-timeline

## Overview

paradigm-threat-timeline is a standalone project. It does NOT reference paradigm-threat-files. paradigm-threat-site fetches only `data/events.json` from the timeline; all markdown and assets are referenced from events.json.

**Guiding principles:** Victors write the history. Mass-redaction may have occurred after world wars, plagues, or regime changes. Add all relevant dates; attempt alternate dates for each chronology system. Absence of a source does not mean it never existed.

## Adding Events

1. Add an event to `data/events.json` following the schema in `data/timeline-schema.json`.
2. Create the corresponding markdown file in `events/` with the first `#` header matching `title` exactly.
3. Run `python3 scripts/validate-events.py` to verify.

## Event Schema

- **id**: Unique (e.g. `evt-1774-pugachev`)
- **title**: Must exactly match first `#` header in md_path file
- **md_path**: Path relative to repo root (e.g. `events/ce-1774-pugachev-rebellion.md`)
- **dates**: Array of `{ start, end?, calendar, source?, confidence?, note? }` — **add multiple dates** for different chronology systems. Use section end for `end` if unknown.
- **section**: Assigned by refactor-sections (BCE Option A or CE century)
- **timeline_sources**: Per-event override; omit to inherit from section. e.g. Saturnian, Fomenko, MudFlood, Mars
- **context**: `{ mainstream, theoretical }`
- **priority**: From header level in source (#=1, ##=2, ###=3, ####=4; 1 = highest)
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

- **generate-index.py**: Builds `index.json` (for file browser). Run on pre-commit.
- **validate-events.py**: Checks schema and title/header match. Run after edits.
- **split-chronology.py**: Extracts events from paradigm-threat-files. Reads only; writes to timeline. Use `--source-dir` to point at paradigm-threat-files.
- **normalize-events.py**: Adds missing dates using the "last date header" rule, renames files to `bce-YYYY-` or `ce-YYYY-` format (era before year, start date only, no ranges). Run after split or when adding dates.
- **refactor-sections.py**: Assigns each event to a section (BCE Option A + CE centuries), moves duplicate timeline_sources to sections, keeps per-event sources when different. Run after split or normalize.

## Last Date Header Rule

The chronology page is the timeline. Sections without date headers occur within the date of the **last** preceding `###` that has a date. normalize-events.py applies this rule when assigning dates.

## Running Scripts

```bash
npm run split-chronology
npm run normalize-events
npm run validate-events
npm run generate-index
```

## Investigations

- Use `investigations/` for source validation (e.g. tracing creation dates, verifying claims).
- When a cited source cannot be found online or in mainstream refs: assume redaction or gatekeeping before assuming error. Document the gap.
- See `investigations/README.md` for the investigation template and index.

## Updating OUTSTANDING_QUESTIONS.md

When you find contradictions, unresolved dates, or need clarification, add entries to `docs/OUTSTANDING_QUESTIONS.md`.

## Updating CONCLUSIONS.md

When the timeline supports a conclusion or speculation, add it to `docs/CONCLUSIONS.md`. Mark confidence level when uncertain.
