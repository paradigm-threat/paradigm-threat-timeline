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

## Image Generation (Golden Age vs Dark Age)

When generating or replacing illustrations for timeline articles:

- **Saturn’s rings:** Saturn does **not** have rings in BCE times, only in CE. In BCE/Golden Age images, do not draw Saturn with the distinct ring system; use a sunlike body, spoked wheel, or plasma halo/Absu only.

- **Venus vs Mars (Wheel of Heaven):** In Golden Age / BCE images, **Venus** is a **plasmoid** appearing as a **single** star figure (one 3–8 sided star, e.g. six- or eight-pointed)—luminous, plasma-like—not many stars or symbols. **Mars** always looks **solid** (a distinct spherical or solid body, not plasmoid). Do not show other symbols in the sky; only Mars, Venus (single star), and Saturn.

- **Golden Age (and before-creation / creation-era):** Always use **Saturnian Cosmology** backgrounds showing the **Wheel of Heaven**. The **northern hemisphere** looked like the Northern Hemisphere Configuration: **Saturn + Venus + Mars = Tree of Life**—central luminous body (Saturn as sunlike, no rings), polar view “up the magnetic tube,” central spoked wheel, eight-pointed Sun Wheel / Shamash-style motif, Dharmachakra-style wheel; plasma halo or Absu (no distinct planetary rings). Sky can transition from deep blue to hazy yellowish-orange near the horizon. The **southern hemisphere** looked like the Southern Hemisphere Configuration: **petroglyph images in the sky**—Uranus + Neptune + Mercury forming the squatting-man figure; purple-tinged, plasma-like sky with luminous swirls; white or glowing stylized petroglyph figures (anthropomorphic, zoomorphic, squatting-man, Kokopelli-style) superimposed in the sky as if ancient rock art were celestial; barren rocky landscape with ancient observers. This applies to any image set in or before the Golden Age.

- **Dark Age:** Do **not** show the Wheel of Heaven—it is no longer present. Instead show **Venus and Mars tethered together as the dragon** (the new celestial configuration of the Dark Age). No Saturnian polar wheel or sunlike Saturn in the sky.

## Key Paths

- `data/events.json` — canonical event list
- `data/timeline-schema.json` — schema
- `events/` — markdown per event
- `investigations/` — validation research
- `docs/AGENT_INSTRUCTIONS.md` — detailed agent guide
- `scripts/` — Python scripts for split, normalize, validate, refactor
