# Timeline Update: Chapter Consolidation, New Articles, Print-Ready PDF, and Chronological Corrections

*February 27, 2026 — Paradigm Threat*

---

A major structural pass across chapters 3, 5, 6, 7, 8, 9, and 10 — consolidating redundant articles, adding new research, correcting chronological placement, and implementing a print-ready PDF pipeline. 12 commits since the last update bring the project to **v1.1.31** with **156 entries** and **320 indexed files**.

---

## Print-Ready PDF Pipeline (PRINT_GOALS)

The PDF export has been completely overhauled for physical publication:

- **6×9 trade paperback** format (152.4 × 228.6 mm) replacing A4
- **Mirrored recto/verso margins** with 25 mm gutter for binding
- **Professional typography**: EB Garamond body, Libre Franklin headings, JetBrains Mono code — all bundled under OFL in `fonts/`
- Alternating **running headers** (book title verso, chapter title recto)
- **Recto chapter openers** with blank verso inserts
- Copyright page (page ii), **table of contents with leader dots**, ornamental section breaks (— ✦ —)
- H4 rendered as serif bold italic, first-line indent (5 mm) for subsequent paragraphs
- Image settings: 120 mm max width, 100 mm height, 82 JPEG quality
- Full spec documented in `docs/PRINT_GOALS.md`
- New `npm run export` command bootstraps a Python venv automatically and runs both PDF and DOCX generators

Current export: **597+ pages** (PDF ~47 MB, DOCX ~37 MB).

---

## Chapter 3: Dark Ages Consolidation (26 → 17 files)

The Dark Ages chapter was significantly consolidated:

- Merged scattered orbital-change articles into parent events (year-length changes now documented inline rather than as separate files)
- Rewrote **03.01.00** (Golden Age Ends Violently) and **03.00.00** chapter root with expanded context
- Combined the deluge, planetary war, and orbital stabilization into a cleaner narrative arc
- Added new section: **03.12.00** — 684 BCE Solar System Becomes Stable (final orbital settlement)
- Fixed all cross-links across chapters referencing moved/renumbered Dark Ages content

---

## Chapter 5: New Religion of Constancy (05.03.01)

New article documenting the Deep State's replacement theology after the catastrophes ended:

- Once the solar system stabilized, the ruling class needed populations to forget that the sky had ever changed
- The "Religion of Constancy" — the doctrine that the heavens have always been as they are — becomes the foundational axiom of both mainstream science and institutional religion
- Expanded existing ch5 articles with new images: `year-of-the-lord-deception.png`, `deep-state-centralizes-world-religion.png`, `sun-replaces-mars-as-saviour.png`, `constancy.png`

---

## Chapter 6: Consolidation (10 → 8 files) + Hairy Mary Article

Major rewrite of the 12th-century Christianity chapter:

- **Merged** naming/giants/census articles into single root `06.01.00`
- **New: 06.01.01 — Hairy Mary**: The Wild Woman / matrilineal threat thesis
  - Medieval Wild Woman iconography = memory of real hairy giants from Rus'/Jotunheim
  - Church reframed the Wild Woman as sinful to justify genocide of the giant lineage
  - Christ's mother carried the eastern matrilineal heritage tradition, threatening the patriarchal Church
  - The Trojan War = religious dispute over the "woman" (Mary / Rus' tradition)
  - Fomenko: Russia = Risaland = Land of Giants = Jotunheim
  - Added "The Father Who Was Never Named" subsection
- **Expanded 06.02.00**: Birth in Crimea, the Magi, cesarean etymology
- **Expanded 06.03.00**: Crucifixion, Turin Shroud, Yoros archaeological site
- **Rewrote 06.03.01**: The brother on the cross — Isukiri legend, Romulus & Remus parallel
- **Rewrote 06.04.00**: Revolution survives despite Christ's martyrdom, the Two Branches thesis

---

## Chapter 7: Consolidation (6 → 4 files) + The Masons (07.01.01)

- **Merged** Fall of Troy, Capture of Jerusalem, and Israelites into single chapter root `07.00.00`
- **Renamed 07.01.00** to "A Second Golden Age" with expanded content on the Horde's imperial expansion
- **New: 07.01.01 — The Masons** (315-line article):
  - Imperial builders of the Rus-Horde: temple rebuild commission after Crusade destruction
  - Cathars as operative masons; Gothic architecture = Hordian style
  - The geopolymer concrete secret (cast stone, not carved)
  - Reformation rebranding: operative masons → speculative Freemasons
  - GAOTU monotheism preserving Saturnian/Electric Universe knowledge
  - Illuminati capitals (Washington DC / London / Vatican) as planned power centers
  - Saturnian spire symbolism in Masonic architecture
- **New: 07.01.02 — The Giants of the Rus-Horde**: 132-line article on giant evidence within the Horde period, Extraordinary Black Book (1832) contextualized as living memory

---

## Chapter 8: Consolidation + Kulikovo Expansion

- **Rewrote 08.00.00** as "The Great Expansion — Triumph and Betrayal"
  - Merged Hundred Years War content into root article with "The Worm in the Court" section on Deep State infiltration
- **Expanded 08.01.00** schism article with Deep State operations, Two Branches framework, Seeds of 1492
- **Expanded 08.02.00** (Kulikovo) with Fomenko's 30 phantom reflections:
  - David vs Goliath, Gallic War giant, King Arthur, Zeus vs Titans (Cyclops = cannons), Marathon
- **New: 08.01.01 — Imperial Technology and the Knowledge of the Horde** (66 lines)
- **New: 08.01.02 — European Castles: Fortresses Against Giants** (92 lines)
- **Split Hundred Years War** between ch08 (1337 begins) and ch09 (1453 ends) with bidirectional cross-links

---

## Chapter 9: Hierarchy Renumbered + New Content

Full renumbering of the ch09 hierarchy to fix structural issues:

- 09.02.00 (HYW ends) → 09.00.01 (child of root)
- Deep State steals history, Latin/Deep State language, Gutenberg Bible, Jesuits, Revelation, Apocalypse Crusade — all renumbered and cross-references updated across ch05, ch08, ch09
- **Expanded 09.00.01** (Hundred Years War Ends) with 76 lines of new content
- **Expanded 09.05.00** (Revelation) with 69 lines of additional analysis
- **New: 09.06.00 — The Apocalypse Crusade** (68 lines, split from combined article)
- **New: 09.07.00 — The Reverse Exodus Theory** (133 lines)
- Added `star-metal.png` to 09.01.00 (meteorite article)

---

## Chapter 10: Major Refactor — Joan of Arc Move + Four New Articles

### Joan of Arc Moved to Chapter 9

Fomenko dates Joan of Arc to the XV century / epoch of Ottoman conquest, not the XVI century Reformation. Corrected:

- Moved content file from `10.07.00` → `09.01.01` (child of meteorite/star-metal event)
- Moved media files (`jeanne-darc-is-executed.png`, `painting_samson_and_delilah_by_rubens.jpg`) from `media/10.*` to `media/09.*`
- Updated all cross-references in `10.03.02` (Cathar Suppression) and events.json
- Both Scaligerian (1431) and Fomenko (1580) dates preserved in events.json

### New: 10.05.01 — The Cathar–Khazar–Katya Connection

Bridging article connecting two simultaneous annihilation campaigns:

- Shared etymological root: Cathar / Khazar / Katya / Katherine — all derive from the same name
- Pre-schism unity thesis: Cathars and Khazars were branches of the same Horde civilization
- **Velikovsky citation**: "Those Who Return" etymology from *khazar* = Hebrew for "return"
- Simultaneous annihilation table showing parallel destruction timelines
- Illustrated with `cathar-khazar-katya.png`

### New: 10.03.03 — The Pentateuch as a Horde Chronicle

Fomenko's argument (ch8.07) that the Hordians wrote the Pentateuch:

- Old Testament books as administrative and military records of the Great Empire
- Cross-links to Judges = Inquisition, Esther = Oprichnina, Romanov erasure mechanism

### New: 10.06.02 — Shakespeare Encodes the Oprichnina (Cross-Reference)

Slim cross-reference article in ch10 linking to the primary Shakespeare article in ch11:

- King Lear = Ivan IV / Oprichnina division of Russia
- Henry VIII = reflection of Ivan's court
- Points to full analysis in ch11

### Gregorian Calendar Article Rewritten (10.08.00)

Complete rewrite of the 1582 Gregorian calendar article with Fomenko ch7.34 analysis:

- **Computus could not have been established at Nicaea 325 CE** — astronomical proof that the Easter/Passover rule breaks before 784 CE
- **Dionysius Exiguus = Dionysius Petavius** (XVII century) — "Exiguus" (small) = French "petit" = Petavius
- **Scaliger's *De emendatione temporum* (1583)** — published one year after the Gregorian reform, coordinated operation to rebuild chronology
- **Anno Domini era** only systematically used from 1431
- Preserved original content on lunisolar calendar, natural month names, and the 1053-year shift

---

## Chapter 11: Shakespeare Primary Article (11.02.04)

### New: Shakespeare Encodes the Great Empire

Primary article on Fomenko's Shakespeare identification ([SAK] analysis), placed in ch11 where Shakespeare actually lived (1564–1616):

- Full identification table: Hamlet = Christ, King Lear = Ivan IV, Macbeth = Herod, Titus Andronicus = Andronicus I, Antony & Cleopatra = XII century original
- XII century plays section (encoded memories of the Crusade era)
- XVI century plays section (Oprichnina and Reformation encodings)
- Fomenko's method: statistical textual parallels + proper name analysis
- The authorship question reframed: Shakespeare as a committee project to preserve dangerous history
- Illustrated with `shakespeare.png`

---

## Infrastructure

- **New `scripts/export.sh`**: Bootstraps `.venv/`, installs Python dependencies, runs both PDF and DOCX generators — invoked via `npm run export`
- **Updated `.github/copilot-instructions.md`** with venv/export workflow documentation
- **All validation scripts pass**: 156 entries validated, all 156 content files registered, 320 files indexed
- PDF and DOCX exports regenerated with every structural commit

---

## Summary of Numbers

| Metric | Before | After |
|--------|--------|-------|
| Total entries | ~140 | 156 |
| Total indexed files | ~280 | 320 |
| Ch03 files | 26 | 17 |
| Ch06 files | 10 | 8 |
| Ch07 files | 6 | 4 (+2 new) |
| New articles this session | — | 13 |
| PDF pages | ~500 | 597+ |
| Version | 1.1.19 | 1.1.31 |
