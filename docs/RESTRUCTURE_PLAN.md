# Restructure Plan: Unified Decimal-Numbered Content Folder

## Goal

Merge `events/` and `articles/*/` into a single flat `content/` folder.  
File sort order = timeline order. Insert new files anywhere without renaming existing ones.

---

## Numbering System

```
<chapter>.<item> — <slug>.md
```

- **Chapter** = 2-digit zero-padded integer (`00`–`12`+). Each major section = one chapter.
- **Item** = 2-digit zero-padded integer, **spaced by 10** (`10`, `20`, `30`…).  
  - Insert between items by using the gap: `15` fits between `10` and `20`.
  - Files sort naturally in shell and file browsers.
- **Chapter `.00`** = the chapter header / event marker (replaces the old event file).
- No BCE/CE in filenames — the number encodes position.

---

## Chapter Map

| # | Old section | Date range |
|---|-------------|------------|
| 00 | overview + saturnian-cosmology-video + chronology-chat | (meta/intro) |
| 01 | project-objective | (methodology) |
| 02 | before-creation | ~5000 BCE |
| 03 | the-golden-age | ~4077–3147 BCE |
| 04 | the-dark-ages | ~3147–684 BCE |
| 05 | the-blip | ~684 BCE–1053 CE |
| 06 | 11th century | 1053–1099 CE |
| 07 | 12th century | 1100–1199 CE |
| 08 | 13th century | 1200–1299 CE |
| 09 | 14th century | 1300–1399 CE |
| 10 | 15th century | 1400–1499 CE |
| 11 | 16th century | 1500–1599 CE |
| 12 | 17th century | 1600–1699 CE |

Future centuries slot in naturally: 13 = 18th, 14 = 19th, etc.

---

## Full File Mapping

### Chapter 00 — Overview / Introduction

| New filename | Old path |
|---|---|
| `00.00-overview.md` | *(new chapter header, replaces nothing — or repurpose `overview/introduction.md` as header)* |
| `00.10-introduction.md` | `articles/overview/introduction.md` |
| `00.20-saturnian-cosmology-timeline-video.md` | `articles/saturnian-cosmology-timeline-video/saturnian-cosmology-timeline-video.md` |
| `00.30-chronology-chat.md` | `articles/chronology-chat/chronology-chat.md` |

---

### Chapter 01 — Project Objective / Methodology

| New filename | Old path |
|---|---|
| `01.00-project-objective.md` | `articles/project-objective/project-objective.md` |
| `01.10-the-length-of-a-year-changes-throughout-antiquity.md` | `articles/project-objective/the-length-of-a-year-changes-throughout-antiquity.md` |
| `01.20-timeline-synchronization.md` | `articles/project-objective/timeline-synchronization.md` |
| `01.30-cosmic-life-cycle.md` | `articles/project-objective/cosmic-life-cycle.md` |

---

### Chapter 02 — Before Creation (~5000 BCE)

| New filename | Old path |
|---|---|
| `02.00-before-creation.md` | `events/bce-5000-before-creation.md` |
| `02.10-scalar-energy-as-the-basis-of-creation.md` | `articles/before-creation/scalar-energy-as-the-basis-of-creation.md` |
| `02.20-3-plasmoids-in-the-southern-hemisphere.md` | `articles/before-creation/3-plasmoids-in-the-southern-hemisphere.md` |
| `02.30-spawning-of-the-first-life-forms.md` | `articles/before-creation/spawning-of-the-first-life-forms.md` |

---

### Chapter 03 — The Golden Age (~4077–3147 BCE)

| New filename | Old path |
|---|---|
| `03.00-the-golden-age.md` | `events/bce-4077-the-golden-age.md` |
| `03.10-proto-saturn-joins-the-suns-orbit-and-lights-up.md` | `events/bce-4077-proto-saturn-joins-the-suns-orbit-and-lights-up.md` |
| `03.20-all-planets-and-suns-are-hollow.md` | `articles/the-golden-age/all-planets-and-suns-are-hollow.md` |
| `03.30-northern-hemisphere-configuration.md` | `articles/the-golden-age/northern-hemisphere-configuration.md` |
| `03.40-southern-hemisphere-configuration.md` | `articles/the-golden-age/southern-hemisphere-configuration.md` |
| `03.50-saturns-collinear-planetary-configuration-the-tree-of-life.md` | `articles/the-golden-age/saturns-collinear-planetary-configuration-the-tree-of-life.md` |
| `03.60-the-absu-layers-surrounded-the-planets.md` | `articles/the-golden-age/the-absu-layers-surrounded-the-planets.md` |
| `03.70-priori-mars-as-the-ladder-stairway-mountain-of-heaven.md` | `articles/the-golden-age/priori-mars-as-the-ladder-stairway-mountain-of-heaven.md` |
| `03.80-atlantis-and-the-tree-of-knowledge.md` | `articles/the-golden-age/atlantis-and-the-tree-of-knowledge.md` |
| `03.90-the-first-jews-of-atlantis-first-jerusalem.md` | `articles/the-golden-age/the-first-jews-of-atlantis-first-jerusalem.md` |
| `03.100-quantum-entanglement.md` | `articles/the-golden-age/quantum-entanglement.md` |
| `03.110-the-length-of-a-year-was-225-days.md` | `articles/the-golden-age/the-length-of-a-year-was-225-days.md` |

---

### Chapter 04 — The Dark Ages (~3147–684 BCE)

| New filename | Old path |
|---|---|
| `04.00-the-dark-ages.md` | `events/bce-3147-the-dark-ages.md` |
| `04.10-the-golden-age-ends-violently.md` | `events/bce-3147-the-golden-age-ends-violently.md` |
| `04.20-the-great-deluge.md` | `articles/the-dark-ages/the-great-deluge.md` |
| `04.30-humanity-was-then-cast-out-of-the-garden-of-eden.md` | `articles/the-dark-ages/humanity-was-then-cast-out-of-the-garden-of-eden.md` |
| `04.40-how-many-lunar-months-are-in-a-year.md` | `articles/the-dark-ages/how-many-lunar-months-are-in-a-year.md` |
| `04.50-all-planets-enter-a-stable-non-linear-orbit.md` | `events/bce-2860-all-planets-enter-a-stable-non-linear-orbit.md` |
| `04.60-the-length-of-a-year-increases-by-an-additional-15-rotations-per-year-to-240-days.md` | `articles/the-dark-ages/the-length-of-a-year-increases-by-an-additional-15-rotations-per-year-to-240-day.md` |
| `04.70-the-length-of-a-year-increases-by-20-rotations-to-260-days.md` | `articles/the-dark-ages/the-length-of-a-year-increases-by-20-rotations-to-260-days.md` |
| `04.80-the-planets-are-at-war.md` | `events/bce-3067-the-planets-are-at-war.md` |
| `04.90-jupiter-catches-on-fire.md` | `events/bce-2167-jupiter-catches-on-fire.md` |
| `04.100-jupiter-replaces-saturn-as-the-new-saviour-aka-zeus-thor-king-arthur.md` | `articles/the-dark-ages/jupiter-replaces-saturn-as-the-new-saviour-aka-zeus-thor-king-arthur.md` |
| `04.110-earth-leaves-last-absu-layer-and-jupiter-consumes-venus-again.md` | `events/bce-2193-earth-leaves-last-absu-layer-and-jupiter-consumes-venus-again.md` |
| `04.120-jupiter-disappears-and-venus-attacks-earth.md` | `events/bce-2349-september-8-jupiter-disappears-and-venus-attacks-earth.md` |
| `04.130-venus-replaces-jupiter-as-the-new-saviour-aka-joshua-lucifer.md` | `articles/the-dark-ages/venus-replaces-jupiter-as-the-new-saviour-aka-joshua-lucifer.md` |
| `04.140-the-length-of-a-year-increases-by-13-rotations-to-273-days.md` | `articles/the-dark-ages/the-length-of-a-year-increases-by-13-rotations-to-273-days.md` |
| `04.150-sodom-and-gomorrah-are-completely-destroyed-by-mars.md` | `events/bce-1936-sodom-and-gomorrah-are-completely-destroyed-by-mars.md` |
| `04.160-mars-aka-prometheus-replaces-venus-as-the-new-saviour.md` | `articles/the-dark-ages/mars-aka-prometheus-replaces-venus-as-the-new-saviour.md` |
| `04.170-the-passover-of-comet-venus-and-exodus-from-the-pyramidal-empire.md` | `events/bce-1492-the-passover-of-comet-venus-and-exodus-from-the-pyramidal-empire.md` |
| `04.180-the-sun-stands-still-for-joshua.md` | `events/bce-1442-the-sun-stands-still-for-joshua.md` |
| `04.190-mysterious-carbon-14-spike.md` | `events/bce-1063-mysterious-carbon-14-spike.md` |
| `04.200-the-length-of-a-year-jumps-by-92-rotations-to-365-days.md` | `articles/the-dark-ages/the-length-of-a-year-jumps-by-92-rotations-to-365-days.md` |
| `04.210-the-length-of-a-year-jumps-by-14th-of-a-rotation-to-36525-days.md` | `articles/the-dark-ages/the-length-of-a-year-jumps-by-14th-of-a-rotation-to-36525-days.md` |
| `04.220-pyramids-were-portals.md` | `articles/the-dark-ages/pyramids-were-portals.md` |
| `04.230-formation-of-the-deep-state-pyramidal-empire.md` | `articles/the-dark-ages/formation-of-the-deep-state-pyramidal-empire.md` |
| `04.240-priori-mars-loses-its-outer-shell-iron-age-begins.md` | `events/bce-686-march-23-priori-mars-loses-its-outer-shell-iron-age-begins.md` |
| `04.250-mars-earth-and-mercury-finalize-orbits.md` | `events/bce-806-mars-earth-and-mercury-finalize-orbits.md` |
| `04.260-solar-system-becomes-stable.md` | `events/bce-684-solar-system-becomes-stable.md` |

---

### Chapter 05 — The Blip (~684 BCE–1053 CE)

| New filename | Old path |
|---|---|
| `05.00-the-blip.md` | `events/bce-670-the-blip-7th-century-bce-to-10th-century-ce-never-occurred.md` |
| `05.10-building-the-new-chronology.md` | `events/bce-670-building-the-new-chronology.md` |
| `05.20-russia-and-turkey-begin-300-years-of-war.md` | `events/ce-300-russia-and-turkey-begin-300-years-of-war.md` |

---

### Chapter 06 — 11th Century CE (1053–1099)

| New filename | Old path |
|---|---|
| `06.00-11th-century-common-era-begins.md` | `events/ce-1053-11th-century-ce-common-era-begins.md` |
| `06.10-year-of-our-lord-deception-1053-year-shift-forward.md` | `events/ce-1053-year-of-our-lord-deception-1053-year-shift-forward.md` |
| `06.20-deep-state-centralize-world-religion-at-jerusalem.md` | `articles/11th-century-ce-common-era-begins/deep-state-centralize-world-religion-at-jerusalem.md` |
| `06.30-the-sun-replaces-mars-as-the-new-saviour.md` | `articles/11th-century-ce-common-era-begins/the-sun-replaces-mars-as-the-new-saviour.md` |

---

### Chapter 07 — 12th Century CE (1100–1199)

| New filename | Old path |
|---|---|
| `07.00-12th-century-birth-of-christianity.md` | `events/ce-1100-12th-century-ce-birth-of-christianity.md` |
| `07.10-historical-christ-is-born-in-crimea.md` | `events/ce-1152-historical-christ-is-born-in-_crimea_.md` |
| `07.20-the-naming-of-christ.md` | `articles/12th-century-ce-birth-of-christianity/the-naming-of-christ.md` |
| `07.30-the-first-great-war-between-giants-and-smaller-sized-humans.md` | `articles/12th-century-ce-birth-of-christianity/the-first-great-war-between-giants-and-smaller-sized-humans.md` |
| `07.40-deep-state-eliminate-the-giants.md` | `articles/12th-century-ce-birth-of-christianity/deep-state-eliminate-the-giants.md` |
| `07.50-christs-family-flees-ahead-of-the-census.md` | `articles/12th-century-ce-birth-of-christianity/christs-family-flees-ahead-of-the-census.md` |
| `07.60-historical-christ-is-crucified-in-istanbul.md` | `events/ce-1185-historical-christ-is-crucified-in-istanbul.md` |
| `07.70-death-and-alleged-resurrection.md` | `articles/12th-century-ce-birth-of-christianity/death-and-alleged-resurrection.md` |
| `07.80-the-revolution-survives-despite-christs-martyrdom.md` | `articles/12th-century-ce-birth-of-christianity/the-revolution-survives-despite-christs-martyrdom.md` |
| `07.90-first-crusade-begins-as-revenge-for-the-crucifixion.md` | `events/ce-1196-first-crusade-begins-as-revenge-for-the-crucifixion.md` |

---

### Chapter 08 — 13th Century CE (1200–1299)

| New filename | Old path |
|---|---|
| `08.00-13th-century-russian-horde-tartarian-empire.md` | `events/ce-1200-13th-century-ce-the-russian-horde-tartarian-empire-emerges.md` |
| `08.10-capture-of-first-jerusalem.md` | `events/ce-1204-capture-of-first-jerusalem.md` |
| `08.20-whom-are-the-israelites-in-history.md` | `articles/13th-century-ce-the-russian-horde-tartarian-empire/whom-are-the-israelites-in-history.md` |
| `08.30-russian-empire-expands-through-conquest.md` | `articles/13th-century-ce-the-russian-horde-tartarian-empire/russian-empire-expands-through-conquest.md` |
| `08.40-historical-christ-dies.md` | `events/ce-1258-historical-christ-dies.md` |
| `08.50-first-olympic-games.md` | `events/ce-1285-first-olympic-games.md` |

---

### Chapter 09 — 14th Century CE (1300–1399)

| New filename | Old path |
|---|---|
| `09.00-14th-century-great-expansion-of-the-mongol-slavic-rus-horde-empire.md` | `events/ce-1300-14th-century-ce-great-expansion-of-the-mongol-slavic-rus-horde-empire.md` |
| `09.10-european-religious-schism-emerges.md` | `articles/14th-century-ce-great-expansion-of-the-mongol-slav/european-religious-schism-emerges.md` |
| `09.20-the-hundred-years-war-begins.md` | `events/ce-1337-the-hundred-years-war-begins.md` |
| `09.30-giants-are-defeated-at-the-battle-of-kulikovo.md` | `events/ce-1380-giants-are-defeated-at-the-battle-of-kulikovo.md` |

---

### Chapter 10 — 15th Century CE (1400–1499)

| New filename | Old path |
|---|---|
| `10.00-15th-century-ottoman-conquest-of-europe.md` | `events/ce-1400-15th-century-ce-ottoman-conquest-of-europe.md` |
| `10.10-meteorite-star-metal-falls-on-yaroslavl.md` | `events/ce-1421-meteorite-star-metal-falls-on-yaroslavl.md` |
| `10.20-jeanne-darc-is-executed-in-rouen-france.md` | `events/ce-1431-jeanne-darc-is-executed-in-rouen-france.md` |
| `10.30-hundred-years-war-ends.md` | `events/ce-1453-hundred-years-war-ends.md` |
| `10.40-bible-is-translated-into-latin.md` | `events/ce-1455-bible-is-translated-into-latin.md` |
| `10.50-deep-state-steals-russian-history.md` | `articles/15th-century-ce-ottoman-conquest-of-europe/deep-state-steals-russian-history.md` |
| `10.60-latin-is-the-language-of-the-deep-state.md` | `articles/15th-century-ce-ottoman-conquest-of-europe/latin-is-the-language-of-the-deep-state.md` |
| `10.70-revelation-of-the-coming-apocalypse.md` | `events/ce-1486-revelation-of-the-coming-apocalypse.md` |
| `10.80-jesuits-convert-native-religions-to-monotheism.md` | `articles/15th-century-ce-ottoman-conquest-of-europe/jesuits-convert-native-religions-to-monotheism.md` |
| `10.90-the-apocalypse-crusade-reverse-exodus.md` | `events/ce-1492-the-apocalypse-crusade-reverse-exodus.md` |
| `10.100-deep-state-redacts-christianity-into-jesuit-catholicism.md` | `articles/15th-century-ce-ottoman-conquest-of-europe/deep-state-redacts-christianity-into-jesuit-catholicism.md` |
| `10.110-jesuits-reach-america.md` | `articles/15th-century-ce-ottoman-conquest-of-europe/jesuits-reach-america.md` |

---

### Chapter 11 — 16th Century CE (1500–1599)

| New filename | Old path |
|---|---|
| `11.00-16th-century-reformation-and-inquisition.md` | `events/ce-1500-16th-century-ce-reformation-and-inquisition.md` |
| `11.10-protestant-reformation-begins.md` | `events/ce-1517-protestant-reformation-begins.md` |
| `11.20-heresy-of-the-judaizers.md` | `articles/16th-century-ce-reformation-and-inquisition/heresy-of-the-judaizers.md` |
| `11.30-jesuits-make-pilgrimage-to-palestine.md` | `events/ce-1523-jesuits-make-pilgrimage-to-palestine.md` |
| `11.40-the-holy-inquisition.md` | `events/ce-1542-the-holy-inquisition.md` |
| `11.50-jesuits-reach-africa.md` | `events/ce-1548-jesuits-reach-africa.md` |
| `11.60-cathar-suppression.md` | `articles/16th-century-ce-reformation-and-inquisition/cathar-suppression.md` |
| `11.70-khazar-rebellion-in-the-russia-horde-empire.md` | `events/ce-1552-khazar-rebellion-in-the-russia-horde-empire.md` |
| `11.80-romanov-dynasty-stages-the-oprichnina-coup.md` | `events/ce-1565-romanov-dynasty-stages-the-oprichnina-coup.md` |
| `11.90-deep-state-eliminates-its-enemies.md` | `articles/16th-century-ce-reformation-and-inquisition/deep-state-eliminates-its-enemies.md` |
| `11.100-redacted-into-the-books-of-esther-judith.md` | `articles/16th-century-ce-reformation-and-inquisition/redacted-into-the-books-of-esther-judith.md` |
| `11.110-gregorian-calendar-makes-slight-adjustment-to-length-of-a-year.md` | `events/ce-1582-gregorian-calendar-makes-slight-adjustment-to-length-of-a-year.md` |

---

### Chapter 12 — 17th Century CE (1600–1699+)

| New filename | Old path |
|---|---|
| `12.00-17th-century-romanovs-rise-to-power.md` | `events/ce-1600-17th-century-romanovs-rise-to-power.md` |
| `12.10-king-james-version-of-the-bible-is-published.md` | `events/ce-1611-king-james-version-of-the-bible-is-published.md` |
| `12.20-romanovs-zakharyin-yurievs-dynasty-takes-the-throne.md` | `events/ce-1613-romanovs-zakharyin-yurievs-dynasty-takes-the-throne.md` |
| `12.30-deep-state-erases-russian-empire-from-all-chronology.md` | `events/ce-1627-deep-state-erases-russian-empire-from-all-chronology.md` |
| `12.40-disputes-against-jews-reemerge.md` | `events/ce-1633-disputes-against-jews-reemerge.md` |
| `12.50-cossackpolish-war-begins-ethnic-cleansing-of-russians-in-ukraine.md` | `events/ce-1648-cossackpolish-war-begins-ethnic-cleansing-of-russians-in-ukraine.md` |
| `12.60-fall-of-the-avignon-powers.md` | `events/ce-1651-fall-of-the-avignon-powers.md` |
| `12.70-the-english-revolution-and-civil-wars.md` | `events/ce-1660-ce-the-english-revolution-and-civil-wars.md` |
| `12.80-the-great-comet-of-1664-1665.md` | `events/ce-1664-the-great-comet-of-1664-1665.md` |
| `12.90-the-great-plague-of-1665.md` | `events/ce-1665-the-great-plague-of-1665.md` |
| `12.100-byzantine-and-catalan-alliance.md` | `events/ce-1666-byzantine-and-catalan-alliance.md` |
| `12.110-london-burns-to-the-ground.md` | `events/ce-1666-sept-6-1666-ce-london-burns-to-the-ground.md` |
| `12.120-deep-state-plans-a-second-apocalypse-in-the-year-666.md` | `articles/17th-century-romanovs-rise-to-power/deep-state-plans-a-second-apocalypse-in-the-year-666.md` |
| `12.130-messianic-jewish-begins.md` | `events/ce-1670-messianic-jewish-begins.md` |
| `12.140-deep-state-targets-independent-banks.md` | `events/ce-1672-ce-deep-state-targets-independent-banks.md` |
| `12.150-disputes-against-jews-end-lasting-46-years.md` | `events/ce-1673-disputes-against-jews-end-lasting-46-years.md` |
| `12.160-great-fight-in-the-heart-of-western-europe.md` | `events/ce-1677-great-fight-in-the-heart-of-western-europe.md` |
| `12.170-the-order-of-the-temple-of-solomon-is-dismantled.md` | `events/ce-1677-the-order-of-the-temple-of-solomon-is-dismantled.md` |
| `12.180-rex-bellator-plan-unifies-all-military-orders.md` | `events/ce-1679-ce-rex-bellator-plan-unifies-all-military-orders.md` |
| `12.190-the-almogavars-conquer-athens-and-neopatria.md` | `events/ce-1681-the-almogavars-conquer-athens-and-neopatria.md` |
| `12.200-deep-state-solidifies-central-banking.md` | `events/ce-1694-deep-state-solidifies-central-banking.md` |
| `12.210-last-sprinkling-of-absu-dust.md` | `events/ce-1700-last-sprinkling-of-absu-dust.md` |
| `12.220-deep-state-breaks-up-the-hordian-empire.md` | `articles/17th-century-romanovs-rise-to-power/deep-state-breaks-up-the-hordian-empire.md` |
| `12.230-cathars-are-annihilated-in-a-reversed-holy-crusade-inquisition.md` | `articles/17th-century-romanovs-rise-to-power/cathars-are-annihilated-in-a-reversed-holy-crusade-inquisition.md` |
| `12.240-jesuits-missions-convert-asians-to-buddhism.md` | `articles/17th-century-romanovs-rise-to-power/jesuits-missions-convert-asians-to-buddhism.md` |
| `12.250-secret-society-of-jesus-goes-public.md` | `events/ce-1718-secret-society-of-jesus-goes-public.md` |
| `12.260-the-rebellion-of-pugachev.md` | `events/ce-1773-the-rebellion-of-pugachev.md` |
| `12.270-the-mudflood-and-world-cataclysm.md` | `events/ce-1774-the-mudflood-and-world-cataclysm.md` |
| `12.280-napoleonic-wars.md` | `events/ce-1803-napoleonic-wars.md` |
| `12.290-napoleon-invades-russia.md` | `events/ce-1812-napoleon-invades-russia.md` |
| `12.300-ecliptic-pathway-of-the-absu-last-seen.md` | `events/ce-1840-ecliptic-pathway-of-the-absu-last-seen.md` |
| `12.310-tchaikovsky-releases-1812-overture.md` | `events/ce-1880-tchaikovsky-releases-1812-overture.md` |

---

## Files Not Mapped (review needed)

| File | Reason |
|---|---|
| `articles/all-assets/all-assets.md` | Utility/asset index — keep as-is or drop |
| `events/ce-1600-todo-finish-17th-century-timeline.md` | TODO placeholder — drop |

---

## Implementation Steps (after approval)

1. Create `content/` directory.
2. Copy each file to its new name (no deletes yet — keep originals until verified).
3. Update all internal cross-links in markdown files.
4. Update `data/events.json` — add a `content_path` field pointing to `content/XX.YY-slug.md`.
5. Update scripts (`generate-index.py`, `validate-events.py`) to scan `content/` instead of `events/` + `articles/*/`.
6. Update site (`MarkdownCarousel`, `TimelineView`) to resolve paths from `content/` via `md_path`.
7. Delete old `events/` and `articles/` directories once fully verified.
8. Update `media/` folder names to match new chapter slugs (optional, lower priority).

---

## Insertion Convention (going forward)

To add a new file between `04.120` and `04.130`:
- Use `04.125` (or `04.121`–`04.129` for tighter sequences).
- No existing file ever needs renaming.
