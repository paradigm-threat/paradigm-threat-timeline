# Timeline Update: New Articles, Restructure, and a Media Audit

*February 25, 2026 — Paradigm Threat*

---

A heavy session of structural and editorial work. This entry covers everything since yesterday: two new background articles, a full content renumbering, a media audit, infrastructure improvements, and a PDF/DOCX export update.

---

## Content Files Restructured to XX.YY.ZZ Naming Convention

The entire `content/` directory has been reorganized under a three-part numbering scheme: `XX.YY.ZZ-slug.md`. The first segment is the chapter, the second is position within the chapter, and the third distinguishes standalone/parent articles (`ZZ = 00`) from child articles (`ZZ ≠ 0`). The numbers now derive directly from the `children[]` hierarchy in `events.json` and can be regenerated at any time via `scripts/renumber-from-hierarchy.py`.

In the same pass, **76 content files** were renamed to include the event start date and era (e.g., `4077-bce-the-golden-age.md`), making the directory self-documenting without opening any file.

---

## New Article: Wal Thornhill (00.01.05)

**Wallace William Thornhill** (1942–2023) has been added as a full background article. Thornhill was the principal theorist of the Electric Universe framework, most associated with the Thunderbolts Project, and the person who gave the Saturn-Earth capture model its most coherent modern form.

The article covers:

- **The EU Framework** — the electric sun hypothesis (stars as anodes in a galactic current circuit), electric gravity, plasma-discharge comets, and Birkeland currents as the structural backbone of the cosmos
- **The Saturn-Earth Connection** — Thornhill's reconstruction of Saturn as a former brown dwarf that captured Earth, delivered the world's water, and maintained a polar plasma column (the "Wheel of Heaven") before a catastrophic reconfiguration broke the alignment
- **The JWST Crisis** — how data from the James Webb Space Telescope falsified standard cosmological predictions one observation at a time, and why Thornhill argued this validated the Electric cosmology
- **Specialization as the enemy of science** — his ongoing critique of how institutional fragmentation prevents recognition of plasma physics phenomena across disciplines

Thornhill died on February 7, 2023. His full name, Wallace William, and the note that his cause of death was not publicly released have been included. A tribute quote from the Thunderbolts Project is cited.

---

## New Article: Ralph Juergens (00.01.06)

**Ralph E. Juergens** (1924–1979) has been added as a companion background article. Juergens was the aerospace engineer who first formally proposed the Electric Sun hypothesis in 1972, more than a decade before the EU community had a coherent institutional form.

The article covers:

- **The Velikovsky Affair** — Juergens co-founded the Foundation for Studies of Modern Science (FOSMOS) in June 1968, directly in response to the academic suppression of Immanuel Velikovsky, and wrote some of the most incisive criticism of the methodological bad faith shown by mainstream scientists in that dispute
- **The Electric Sun Hypothesis (1972)** — his *Pensée* paper is quoted directly: the sun as an anode in a galactic current, the corona heated by electron bombardment rather than conduction from the interior, the photosphere as an anode glow. The model predicts surface temperature below corona temperature — which is exactly what is observed but inexplicable under standard fusion models
- **The anode/cathode discrepancy** — a note on the ongoing Thornhill correction: Juergens first described the sun as a cathode; Thornhill later established it is more accurately an anode. Both are documented
- **Death and redaction** — Juergens died in November 1979 at age 55, causes not publicly documented. His 2007 Wikipedia article was deleted and has never been restored, an act of institutional erasure consistent with the broader pattern of EU-adjacent suppression documented across this timeline
- **Alfvén's acknowledgment** — a direct quote from Hannes Alfvén's letter to David Talbott in which the Nobel laureate explicitly credited Juergens's empirical work

Four images are included: a portrait, an EU sun diagram, a historical photograph, and the "murdered by the mainstream" memorial image from the Thunderbolts community.

---

## Cosmic Life Cycle Article — Theoretical Context Added

The article on the **Short Cosmic Life Cycle** now includes a new section: *Theoretical Context and Related Views*. The section surveys four existing frameworks that partially overlap with the theory — Big Bang cosmology, Young Universe Creationism, the Apparent Age / Omphalos hypothesis (Gosse), and Gap Theory — and shows where each converges with or departs from the Short Cosmic Life Cycle model.

A comparison table is included. The conclusion is that **Gap Theory** is the closest existing match: both place a discontinuity between the initial creation event and the present age, both allow for an ancient universe alongside a recent Earth, and both treat the gap itself as catastrophic rather than gradual. The key difference is that the Short Cosmic Life Cycle specifies the mechanism and the chronology where Gap Theory leaves both open. Wal Thornhill is noted as compatible with the framework, though he did not state the theory himself.

---

## Media Audit — Six Misplaced Images Corrected

A full audit of the `media/` directory revealed six images stored in chapter folders that did not match their referenced articles. All have been moved to the correct folders and all references in content files and `events.json` have been updated:

- `na-morozov.png` — moved from `01.before-creation/` to `00.overview/`
- `hollow_earth_EU_model.jpg` — moved from `00.overview/` to `01.before-creation/`
- `golden_age_ends_kronos_devours.jpg` — moved from `02.the-golden-age/` to `03.the-dark-ages/`
- `hairy_mary.jpg`, `conjunction.jpg`, `twelve_tribes_zodiac.jpg` — moved from `05.ce-11th-common-era-begins/` to `06.ce-12th-birth-of-christianity/`

---

## Infrastructure: audit-missing.py and Pre-commit Hook

A new script, `scripts/audit-missing.py`, has been added. It cross-references each entry in `events.json` against the actual files present in `content/` and reports any articles referenced in the data but not yet written. The script is wired into the Husky pre-commit hook alongside the existing `validate-events` check, meaning every commit now automatically flags missing content files before they can be pushed.

---

## Credits Article Added (15.010)

A credits article has been added at position **15.010** for **Samuel Waweru**, acknowledging his contributions to the project's research base.

---

## Exports Updated

The PDF and DOCX exports have been regenerated. Current figures:

- **PDF**: 316 pages, ~19.9 MB
- **DOCX**: ~25 MB

Both are versioned with the repository and available in `export/`.

---

The timeline is at [paradigmthreat.net/timeline](https://paradigmthreat.net/timeline). The investigation continues.

---

*Filed under: updates, wal-thornhill, ralph-juergens, electric-universe, restructure, media, infrastructure, cosmic-life-cycle*
