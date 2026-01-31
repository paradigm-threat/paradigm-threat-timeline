# Agent Instructions for paradigm-threat-timeline

## Overview

paradigm-threat-timeline is a standalone project. It does NOT reference paradigm-threat-files. paradigm-threat-site fetches only `data/events.json` from the timeline; all markdown and assets are referenced from events.json.

## Adding Events

1. Add an event to `data/events.json` following the schema in `data/timeline-schema.json`.
2. Create the corresponding markdown file in `events/` with the first `#` header matching `title` exactly.
3. Run `python3 scripts/validate-events.py` to verify.

## Event Schema

- **id**: Unique (e.g. `evt-1774-pugachev`)
- **title**: Must exactly match first `#` header in md_path file
- **md_path**: Path relative to repo root (e.g. `events/pugachev-rebellion.md`)
- **dates**: Array of `{ value, calendar, source?, confidence?, note? }`
- **timeline_sources**: e.g. Scaligerian, Fomenko, Saturnian
- **context**: `{ mainstream, theoretical }`
- **priority**: From header level in source (#=1, ##=2, ###=3, ####=4; 1 = highest)
- **media**: Optional URLs for thumbnails/assets

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

## Updating OUTSTANDING_QUESTIONS.md

When you find contradictions, unresolved dates, or need clarification, add entries to `docs/OUTSTANDING_QUESTIONS.md`.

## Updating CONCLUSIONS.md

When the timeline supports a conclusion or speculation, add it to `docs/CONCLUSIONS.md`.
