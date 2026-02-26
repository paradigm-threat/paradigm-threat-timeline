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

## When Investigating Claims

- Use `investigations/` for validation research. Do not assume mainstream sources are complete or unaltered.
- If a cited source cannot be found: document the gap, add to `docs/OUTSTANDING_QUESTIONS.md`. Prefer "source may be redacted/lost" over "claimant made an error."

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

## Image Generation (Golden Age vs Dark Age)

When generating or replacing illustrations for timeline articles:

- **Saturn’s rings:** Saturn does **not** have rings in BCE times, only in CE. In BCE/Golden Age images, do not draw Saturn with the distinct ring system; use a sunlike body, spoked wheel, or plasma halo/Absu only.

- **Venus vs Mars (Wheel of Heaven):** In Golden Age / BCE images, **Venus** is a **plasmoid** appearing as a **single** star figure (one 3–8 sided star, e.g. six- or eight-pointed)—luminous, plasma-like—not many stars or symbols. **Mars** always looks **solid** (a distinct spherical or solid body, not plasmoid). Do not show other symbols in the sky; only Mars, Venus (single star), and Saturn.

- **Golden Age (and before-creation / creation-era):** Always use **Saturnian Cosmology** backgrounds showing the **Wheel of Heaven**. The **northern hemisphere** looked like the Northern Hemisphere Configuration: **Saturn + Venus + Mars = Tree of Life**—central luminous body (Saturn as sunlike, no rings), polar view “up the magnetic tube,” central spoked wheel, eight-pointed Sun Wheel / Shamash-style motif, Dharmachakra-style wheel; plasma halo or Absu (no distinct planetary rings). Sky can transition from deep blue to hazy yellowish-orange near the horizon. The **southern hemisphere** looked like the Southern Hemisphere Configuration: **petroglyph images in the sky**—Uranus + Neptune + Mercury forming the squatting-man figure; purple-tinged, plasma-like sky with luminous swirls; white or glowing stylized petroglyph figures (anthropomorphic, zoomorphic, squatting-man, Kokopelli-style) superimposed in the sky as if ancient rock art were celestial; barren rocky landscape with ancient observers. This applies to any image set in or before the Golden Age.

- **Dark Age:** Do **not** show the Wheel of Heaven—it is no longer present. Instead show **Venus and Mars tethered together as the dragon** (the new celestial configuration of the Dark Age). No Saturnian polar wheel or sunlike Saturn in the sky.

## Key Paths

- `data/events.json` — canonical event list and hierarchy
- `data/timeline-schema.json` — schema
- `content/` — article markdown files in chapter subfolders (`content/<chapter>/XX.YY.ZZ-slug.md`)
- `investigations/` — validation research
- `docs/AGENT_INSTRUCTIONS.md` — detailed agent guide
- `scripts/renumber-from-hierarchy.py` — re-derives all file numbers from `events.json` hierarchy
- `scripts/` — all other Python utility scripts
