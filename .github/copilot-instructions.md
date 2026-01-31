# paradigm-threat-timeline: Copilot Instructions

## Purpose

Alternate Earth History Timeline correlating Scaligerian, Fomenko's New Chronology, Saturnian Cosmology, and other sources. This project is an **investigation** into chronology, not a textbook. Assume redaction and victors' bias.

## Guiding Principles

1. **Victors write the history.** Mainstream (Scaligerian) dates may reflect those who controlled record-keeping.
2. **Mass-redaction is plausible.** World wars, plagues, regime changes, and church chronologists could have altered records at any time. Absence of a source ≠ it never existed.
3. **Add all dates.** For each event, add every relevant date from every chronology system we can find.

## When Adding or Editing Events

- Use `data/timeline-schema.json` as the schema. Events live in `data/events.json`.
- `dates[]` supports **multiple entries** per event—one per chronology system. Include `source`, `note`, `confidence` when known.
- Chronology systems to consider: Saturnian, Fomenko, Scaligerian, Phantom Time, Byzantine, Alexandrian, Judaic, indigenous (Quiche Maya, etc.).
- Add `duplicate_of` and `related_events` for Fomenko-identified duplicates.
- Event markdown files: `events/{bce|ce}-{year}-{slug}.md`. Title must match first `#` header exactly.

## When Investigating Claims

- Use `investigations/` for validation research. Do not assume mainstream sources are complete or unaltered.
- If a cited source cannot be found: document the gap, add to `docs/OUTSTANDING_QUESTIONS.md`. Prefer "source may be redacted/lost" over "claimant made an error."

## Scripts (run after edits)

```bash
npm run normalize-events
npm run refactor-sections
npm run validate-events
```

## Key Paths

- `data/events.json` — canonical event list
- `data/timeline-schema.json` — schema
- `events/` — markdown per event
- `investigations/` — validation research
- `docs/AGENT_INSTRUCTIONS.md` — detailed agent guide
- `scripts/` — Python scripts for split, normalize, validate, refactor
