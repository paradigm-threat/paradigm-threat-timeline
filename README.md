# paradigm-threat-timeline

**Paradigm Threat: The Third Story** — A cross-chronology investigation challenging the official timeline of Earth history — Scaligerian, Fomenko's New Chronology, Saturnian Cosmology, and indigenous traditions.

The PDF and DOCX exports in `export/` are **early drafts of an upcoming book**. They are generated automatically from the research articles in `content/` and should be treated as working drafts: citations are ongoing, sections will be restructured, and conclusions may be revised as new evidence is incorporated. Do not cite page numbers from these drafts.

## Principles

- **Victors write the history.** Mainstream chronology may reflect the perspective of those who controlled record-keeping, not objective fact.
- **Mass-redaction is plausible.** Records could have been altered or destroyed at any point. Absence of a source does not mean it never existed.
- **Add all dates.** We add every relevant date we can find for each event and attempt to calculate alternate dates based on different chronology systems (Saturnian, Fomenko, Scaligerian, Phantom Time, Byzantine, Judaic, indigenous).
- **Investigation over adjudication.** Document claims, trace sources, stay open to alternate chronologies. Do not dismiss a date because mainstream scholarship disagrees.

## Structure

- **data/events.json** — Canonical event list (the only file paradigm-threat-site loads)
- **data/timeline-schema.json** — Event and section schema
- **events/** — Markdown files for each event
- **investigations/** — Validation research (e.g. creation dates, source tracing)
- **index.json** — Generated file tree (for file browser, not timeline)
- **docs/** — AGENT_INSTRUCTIONS, OUTSTANDING_QUESTIONS, CONCLUSIONS

## Maintaining and Updating the Timeline

1. **Add events** from paradigm-threat-files or new research. Follow `docs/AGENT_INSTRUCTIONS.md`.
2. **Add multiple dates per event** — each `dates[]` entry can have a different `source` (Saturnian, Fomenko, Scaligerian, etc.). Use `note` to explain shifts (e.g. phantom time +1000 years).
3. **Mark duplicates** — use `duplicate_of` and `related_events` for Fomenko-identified duplicates.
4. **Investigate claims** — use `investigations/` for source validation. Document gaps; prefer "source may be redacted" over "claimant erred."
5. **Run scripts** after edits:
   ```bash
   npm run split-chronology   # If adding from paradigm-threat-files
   npm run normalize-events  # Assign dates, rename files
   npm run refactor-sections # Assign sections
   npm run validate-events   # Verify schema and titles
   npm run generate-index   # Pre-commit
   ```

## Scripts

```bash
npm run generate-index    # Build index.json (runs on pre-commit)
npm run validate-events   # Verify events.json
npm run split-chronology  # Extract events from paradigm-threat-files (read-only)
npm run normalize-events  # Dates, filenames, priorities
npm run refactor-sections # Sections, timeline_sources
```

## AI Instructions

- **Cursor:** `.cursor/rules/paradigm-threat-timeline.mdc` — maintenance and investigation principles
- **GitHub Copilot:** `.github/copilot-instructions.md` — repo-wide guidance

## Deployment

To serve the timeline to paradigm-threat-site:

1. Push to GitHub
2. Enable GitHub Pages (Settings → Pages → source: GitHub Actions)
3. The workflow in `.github/workflows/static.yml` deploys on push to `master`

paradigm-threat-site fetches from `NEXT_PUBLIC_TIMELINE_BASE_URL` (default: `https://clevertree.github.io/paradigm-threat-timeline`).

## Local Development

To test the timeline locally before deploying:

```bash
# From paradigm-threat-timeline
npx serve . -p 3011 --cors

# In paradigm-threat-site .env
NEXT_PUBLIC_TIMELINE_BASE_URL=http://localhost:3011
```
