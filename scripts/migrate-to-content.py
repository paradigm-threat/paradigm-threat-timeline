#!/usr/bin/env python3
"""
Migrate events/ + articles/ into a single flat content/ directory.
Numbering: <chapter>.<item>-<slug>.md, items spaced by 10 for future insertions.
Chapters: 00=overview 01=before-creation 02=golden-age 03=dark-ages
          04=blip 05=11th 06=12th 07=13th 08=14th 09=15th 10=16th 11=17th
"""

import os
import json
import shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (new_filename, old_relative_path_from_repo)
MAPPING = [
    # ── Chapter 00: Overview / Intro / Project Objective ──────────────────────
    ("00.10-introduction.md",                                          "articles/overview/introduction.md"),
    ("00.20-saturnian-cosmology-timeline-video.md",                    "articles/saturnian-cosmology-timeline-video/saturnian-cosmology-timeline-video.md"),
    ("00.30-chronology-chat.md",                                       "articles/chronology-chat/chronology-chat.md"),
    ("00.40-project-objective.md",                                     "articles/project-objective/project-objective.md"),
    ("00.50-the-length-of-a-year-changes-throughout-antiquity.md",     "articles/project-objective/the-length-of-a-year-changes-throughout-antiquity.md"),
    ("00.60-timeline-synchronization.md",                              "articles/project-objective/timeline-synchronization.md"),
    ("00.70-cosmic-life-cycle.md",                                     "articles/project-objective/cosmic-life-cycle.md"),

    # ── Chapter 01: Before Creation ────────────────────────────────────────────
    ("01.00-before-creation.md",                                       "events/bce-5000-before-creation.md"),
    ("01.10-scalar-energy-as-the-basis-of-creation.md",                "articles/before-creation/scalar-energy-as-the-basis-of-creation.md"),
    ("01.20-3-plasmoids-in-the-southern-hemisphere.md",                "articles/before-creation/3-plasmoids-in-the-southern-hemisphere.md"),
    ("01.30-spawning-of-the-first-life-forms.md",                      "articles/before-creation/spawning-of-the-first-life-forms.md"),

    # ── Chapter 02: The Golden Age ─────────────────────────────────────────────
    ("02.00-the-golden-age.md",                                        "events/bce-4077-the-golden-age.md"),
    ("02.10-proto-saturn-joins-the-suns-orbit-and-lights-up.md",       "events/bce-4077-proto-saturn-joins-the-suns-orbit-and-lights-up.md"),
    ("02.20-all-planets-and-suns-are-hollow.md",                       "articles/the-golden-age/all-planets-and-suns-are-hollow.md"),
    ("02.30-northern-hemisphere-configuration.md",                     "articles/the-golden-age/northern-hemisphere-configuration.md"),
    ("02.40-southern-hemisphere-configuration.md",                     "articles/the-golden-age/southern-hemisphere-configuration.md"),
    ("02.50-saturns-collinear-planetary-configuration-the-tree-of-life.md", "articles/the-golden-age/saturns-collinear-planetary-configuration-the-tree-of-life.md"),
    ("02.60-the-absu-layers-surrounded-the-planets.md",                "articles/the-golden-age/the-absu-layers-surrounded-the-planets.md"),
    ("02.70-priori-mars-as-the-ladder-stairway-mountain-of-heaven.md", "articles/the-golden-age/priori-mars-as-the-ladder-stairway-mountain-of-heaven.md"),
    ("02.80-atlantis-and-the-tree-of-knowledge.md",                    "articles/the-golden-age/atlantis-and-the-tree-of-knowledge.md"),
    ("02.90-the-first-jews-of-atlantis-first-jerusalem.md",            "articles/the-golden-age/the-first-jews-of-atlantis-first-jerusalem.md"),
    ("02.100-quantum-entanglement.md",                                 "articles/the-golden-age/quantum-entanglement.md"),
    ("02.110-the-length-of-a-year-was-225-days.md",                    "articles/the-golden-age/the-length-of-a-year-was-225-days.md"),

    # ── Chapter 03: The Dark Ages ──────────────────────────────────────────────
    ("03.00-the-dark-ages.md",                                         "events/bce-3147-the-dark-ages.md"),
    ("03.10-the-golden-age-ends-violently.md",                         "events/bce-3147-the-golden-age-ends-violently.md"),
    ("03.20-the-great-deluge.md",                                      "articles/the-dark-ages/the-great-deluge.md"),
    ("03.30-humanity-was-then-cast-out-of-the-garden-of-eden.md",      "articles/the-dark-ages/humanity-was-then-cast-out-of-the-garden-of-eden.md"),
    ("03.40-how-many-lunar-months-are-in-a-year.md",                   "articles/the-dark-ages/how-many-lunar-months-are-in-a-year.md"),
    ("03.50-all-planets-enter-a-stable-non-linear-orbit.md",           "events/bce-2860-all-planets-enter-a-stable-non-linear-orbit.md"),
    ("03.60-the-length-of-a-year-increases-by-an-additional-15-rotations-to-240-days.md", "articles/the-dark-ages/the-length-of-a-year-increases-by-an-additional-15-rotations-per-year-to-240-day.md"),
    ("03.70-the-length-of-a-year-increases-by-20-rotations-to-260-days.md", "articles/the-dark-ages/the-length-of-a-year-increases-by-20-rotations-to-260-days.md"),
    ("03.80-the-planets-are-at-war.md",                                "events/bce-3067-the-planets-are-at-war.md"),
    ("03.90-jupiter-catches-on-fire.md",                               "events/bce-2167-jupiter-catches-on-fire.md"),
    ("03.100-jupiter-replaces-saturn-as-the-new-saviour.md",           "articles/the-dark-ages/jupiter-replaces-saturn-as-the-new-saviour-aka-zeus-thor-king-arthur.md"),
    ("03.110-earth-leaves-last-absu-layer-and-jupiter-consumes-venus-again.md", "events/bce-2193-earth-leaves-last-absu-layer-and-jupiter-consumes-venus-again.md"),
    ("03.120-jupiter-disappears-and-venus-attacks-earth.md",           "events/bce-2349-september-8-jupiter-disappears-and-venus-attacks-earth.md"),
    ("03.130-venus-replaces-jupiter-as-the-new-saviour-aka-joshua-lucifer.md", "articles/the-dark-ages/venus-replaces-jupiter-as-the-new-saviour-aka-joshua-lucifer.md"),
    ("03.140-the-length-of-a-year-increases-by-13-rotations-to-273-days.md", "articles/the-dark-ages/the-length-of-a-year-increases-by-13-rotations-to-273-days.md"),
    ("03.150-sodom-and-gomorrah-are-completely-destroyed-by-mars.md",  "events/bce-1936-sodom-and-gomorrah-are-completely-destroyed-by-mars.md"),
    ("03.160-mars-aka-prometheus-replaces-venus-as-the-new-saviour.md", "articles/the-dark-ages/mars-aka-prometheus-replaces-venus-as-the-new-saviour.md"),
    ("03.170-the-passover-of-comet-venus-and-exodus.md",               "events/bce-1492-the-passover-of-comet-venus-and-exodus-from-the-pyramidal-empire.md"),
    ("03.180-the-sun-stands-still-for-joshua.md",                      "events/bce-1442-the-sun-stands-still-for-joshua.md"),
    ("03.190-mysterious-carbon-14-spike.md",                           "events/bce-1063-mysterious-carbon-14-spike.md"),
    ("03.200-the-length-of-a-year-jumps-by-92-rotations-to-365-days.md", "articles/the-dark-ages/the-length-of-a-year-jumps-by-92-rotations-to-365-days.md"),
    ("03.210-the-length-of-a-year-jumps-by-14th-of-a-rotation-to-36525-days.md", "articles/the-dark-ages/the-length-of-a-year-jumps-by-14th-of-a-rotation-to-36525-days.md"),
    ("03.220-pyramids-were-portals.md",                                "articles/the-dark-ages/pyramids-were-portals.md"),
    ("03.230-formation-of-the-deep-state-pyramidal-empire.md",         "articles/the-dark-ages/formation-of-the-deep-state-pyramidal-empire.md"),
    ("03.240-priori-mars-loses-its-outer-shell-iron-age-begins.md",    "events/bce-686-march-23-priori-mars-loses-its-outer-shell-iron-age-begins.md"),
    ("03.250-mars-earth-and-mercury-finalize-orbits.md",               "events/bce-806-mars-earth-and-mercury-finalize-orbits.md"),
    ("03.260-solar-system-becomes-stable.md",                          "events/bce-684-solar-system-becomes-stable.md"),

    # ── Chapter 04: The Blip ───────────────────────────────────────────────────
    ("04.00-the-blip.md",                                              "events/bce-670-the-blip-7th-century-bce-to-10th-century-ce-never-occurred.md"),
    ("04.10-building-the-new-chronology.md",                           "events/bce-670-building-the-new-chronology.md"),
    ("04.20-russia-and-turkey-begin-300-years-of-war.md",              "events/ce-300-russia-and-turkey-begin-300-years-of-war.md"),

    # ── Chapter 05: 11th Century CE ────────────────────────────────────────────
    ("05.00-11th-century-common-era-begins.md",                        "events/ce-1053-11th-century-ce-common-era-begins.md"),
    ("05.10-year-of-our-lord-deception-1053-year-shift-forward.md",    "events/ce-1053-year-of-our-lord-deception-1053-year-shift-forward.md"),
    ("05.20-deep-state-centralize-world-religion-at-jerusalem.md",     "articles/11th-century-ce-common-era-begins/deep-state-centralize-world-religion-at-jerusalem.md"),
    ("05.30-the-sun-replaces-mars-as-the-new-saviour.md",              "articles/11th-century-ce-common-era-begins/the-sun-replaces-mars-as-the-new-saviour.md"),

    # ── Chapter 06: 12th Century CE ────────────────────────────────────────────
    ("06.00-12th-century-birth-of-christianity.md",                    "events/ce-1100-12th-century-ce-birth-of-christianity.md"),
    ("06.10-historical-christ-is-born-in-crimea.md",                   "events/ce-1152-historical-christ-is-born-in-_crimea_.md"),
    ("06.20-the-naming-of-christ.md",                                  "articles/12th-century-ce-birth-of-christianity/the-naming-of-christ.md"),
    ("06.30-the-first-great-war-between-giants-and-smaller-sized-humans.md", "articles/12th-century-ce-birth-of-christianity/the-first-great-war-between-giants-and-smaller-sized-humans.md"),
    ("06.40-deep-state-eliminate-the-giants.md",                       "articles/12th-century-ce-birth-of-christianity/deep-state-eliminate-the-giants.md"),
    ("06.50-christs-family-flees-ahead-of-the-census.md",              "articles/12th-century-ce-birth-of-christianity/christs-family-flees-ahead-of-the-census.md"),
    ("06.60-historical-christ-is-crucified-in-istanbul.md",            "events/ce-1185-historical-christ-is-crucified-in-istanbul.md"),
    ("06.70-death-and-alleged-resurrection.md",                        "articles/12th-century-ce-birth-of-christianity/death-and-alleged-resurrection.md"),
    ("06.80-the-revolution-survives-despite-christs-martyrdom.md",     "articles/12th-century-ce-birth-of-christianity/the-revolution-survives-despite-christs-martyrdom.md"),
    ("06.90-first-crusade-begins-as-revenge-for-the-crucifixion.md",   "events/ce-1196-first-crusade-begins-as-revenge-for-the-crucifixion.md"),

    # ── Chapter 07: 13th Century CE ────────────────────────────────────────────
    ("07.00-13th-century-russian-horde-tartarian-empire.md",           "events/ce-1200-13th-century-ce-the-russian-horde-tartarian-empire-emerges.md"),
    ("07.10-capture-of-first-jerusalem.md",                            "events/ce-1204-capture-of-first-jerusalem.md"),
    ("07.20-whom-are-the-israelites-in-history.md",                    "articles/13th-century-ce-the-russian-horde-tartarian-empire/whom-are-the-israelites-in-history.md"),
    ("07.30-russian-empire-expands-through-conquest.md",               "articles/13th-century-ce-the-russian-horde-tartarian-empire/russian-empire-expands-through-conquest.md"),
    ("07.40-historical-christ-dies.md",                                "events/ce-1258-historical-christ-dies.md"),
    ("07.50-first-olympic-games.md",                                   "events/ce-1285-first-olympic-games.md"),

    # ── Chapter 08: 14th Century CE ────────────────────────────────────────────
    ("08.00-14th-century-great-expansion-of-the-mongol-slavic-horde.md", "events/ce-1300-14th-century-ce-great-expansion-of-the-mongol-slavic-rus-horde-empire.md"),
    ("08.10-european-religious-schism-emerges.md",                     "articles/14th-century-ce-great-expansion-of-the-mongol-slav/european-religious-schism-emerges.md"),
    ("08.20-the-hundred-years-war-begins.md",                          "events/ce-1337-the-hundred-years-war-begins.md"),
    ("08.30-giants-are-defeated-at-the-battle-of-kulikovo.md",         "events/ce-1380-giants-are-defeated-at-the-battle-of-kulikovo.md"),

    # ── Chapter 09: 15th Century CE ────────────────────────────────────────────
    ("09.00-15th-century-ottoman-conquest-of-europe.md",               "events/ce-1400-15th-century-ce-ottoman-conquest-of-europe.md"),
    ("09.10-meteorite-star-metal-falls-on-yaroslavl.md",               "events/ce-1421-meteorite-star-metal-falls-on-yaroslavl.md"),
    ("09.20-jeanne-darc-is-executed-in-rouen-france.md",               "events/ce-1431-jeanne-darc-is-executed-in-rouen-france.md"),
    ("09.30-hundred-years-war-ends.md",                                "events/ce-1453-hundred-years-war-ends.md"),
    ("09.40-bible-is-translated-into-latin.md",                        "events/ce-1455-bible-is-translated-into-latin.md"),
    ("09.50-deep-state-steals-russian-history.md",                     "articles/15th-century-ce-ottoman-conquest-of-europe/deep-state-steals-russian-history.md"),
    ("09.60-latin-is-the-language-of-the-deep-state.md",               "articles/15th-century-ce-ottoman-conquest-of-europe/latin-is-the-language-of-the-deep-state.md"),
    ("09.70-revelation-of-the-coming-apocalypse.md",                   "events/ce-1486-revelation-of-the-coming-apocalypse.md"),
    ("09.80-jesuits-convert-native-religions-to-monotheism.md",        "articles/15th-century-ce-ottoman-conquest-of-europe/jesuits-convert-native-religions-to-monotheism.md"),
    ("09.90-the-apocalypse-crusade-reverse-exodus.md",                 "events/ce-1492-the-apocalypse-crusade-reverse-exodus.md"),
    ("09.100-deep-state-redacts-christianity-into-jesuit-catholicism.md", "articles/15th-century-ce-ottoman-conquest-of-europe/deep-state-redacts-christianity-into-jesuit-catholicism.md"),
    ("09.110-jesuits-reach-america.md",                                "articles/15th-century-ce-ottoman-conquest-of-europe/jesuits-reach-america.md"),

    # ── Chapter 10: 16th Century CE ────────────────────────────────────────────
    ("10.00-16th-century-reformation-and-inquisition.md",              "events/ce-1500-16th-century-ce-reformation-and-inquisition.md"),
    ("10.10-protestant-reformation-begins.md",                         "events/ce-1517-protestant-reformation-begins.md"),
    ("10.20-heresy-of-the-judaizers.md",                               "articles/16th-century-ce-reformation-and-inquisition/heresy-of-the-judaizers.md"),
    ("10.30-jesuits-make-pilgrimage-to-palestine.md",                  "events/ce-1523-jesuits-make-pilgrimage-to-palestine.md"),
    ("10.40-the-holy-inquisition.md",                                  "events/ce-1542-the-holy-inquisition.md"),
    ("10.50-jesuits-reach-africa.md",                                  "events/ce-1548-jesuits-reach-africa.md"),
    ("10.60-cathar-suppression.md",                                    "articles/16th-century-ce-reformation-and-inquisition/cathar-suppression.md"),
    ("10.70-khazar-rebellion-in-the-russia-horde-empire.md",           "events/ce-1552-khazar-rebellion-in-the-russia-horde-empire.md"),
    ("10.80-romanov-dynasty-stages-the-oprichnina-coup.md",            "events/ce-1565-romanov-dynasty-stages-the-oprichnina-coup.md"),
    ("10.90-deep-state-eliminates-its-enemies.md",                     "articles/16th-century-ce-reformation-and-inquisition/deep-state-eliminates-its-enemies.md"),
    ("10.100-redacted-into-the-books-of-esther-judith.md",             "articles/16th-century-ce-reformation-and-inquisition/redacted-into-the-books-of-esther-judith.md"),
    ("10.110-gregorian-calendar-makes-slight-adjustment-to-length-of-a-year.md", "events/ce-1582-gregorian-calendar-makes-slight-adjustment-to-length-of-a-year.md"),

    # ── Chapter 11: 17th Century CE ────────────────────────────────────────────
    ("11.00-17th-century-romanovs-rise-to-power.md",                   "events/ce-1600-17th-century-romanovs-rise-to-power.md"),
    ("11.10-king-james-version-of-the-bible-is-published.md",          "events/ce-1611-king-james-version-of-the-bible-is-published.md"),
    ("11.20-romanovs-dynasty-takes-the-throne.md",                     "events/ce-1613-romanovs-zakharyin-yurievs-dynasty-takes-the-throne.md"),
    ("11.30-deep-state-erases-russian-empire-from-all-chronology.md",  "events/ce-1627-deep-state-erases-russian-empire-from-all-chronology.md"),
    ("11.40-disputes-against-jews-reemerge.md",                        "events/ce-1633-disputes-against-jews-reemerge.md"),
    ("11.50-cossackpolish-war-ethnic-cleansing-of-russians-in-ukraine.md", "events/ce-1648-cossackpolish-war-begins-ethnic-cleansing-of-russians-in-ukraine.md"),
    ("11.60-fall-of-the-avignon-powers.md",                            "events/ce-1651-fall-of-the-avignon-powers.md"),
    ("11.70-the-english-revolution-and-civil-wars.md",                 "events/ce-1660-ce-the-english-revolution-and-civil-wars.md"),
    ("11.80-the-great-comet-of-1664-1665.md",                          "events/ce-1664-the-great-comet-of-1664-1665.md"),
    ("11.90-the-great-plague-of-1665.md",                              "events/ce-1665-the-great-plague-of-1665.md"),
    ("11.100-byzantine-and-catalan-alliance.md",                       "events/ce-1666-byzantine-and-catalan-alliance.md"),
    ("11.110-london-burns-to-the-ground.md",                           "events/ce-1666-sept-6-1666-ce-london-burns-to-the-ground.md"),
    ("11.120-deep-state-plans-a-second-apocalypse-in-the-year-666.md", "articles/17th-century-romanovs-rise-to-power/deep-state-plans-a-second-apocalypse-in-the-year-666.md"),
    ("11.130-messianic-jewish-begins.md",                              "events/ce-1670-messianic-jewish-begins.md"),
    ("11.140-deep-state-targets-independent-banks.md",                 "events/ce-1672-ce-deep-state-targets-independent-banks.md"),
    ("11.150-disputes-against-jews-end-lasting-46-years.md",           "events/ce-1673-disputes-against-jews-end-lasting-46-years.md"),
    ("11.160-great-fight-in-the-heart-of-western-europe.md",           "events/ce-1677-great-fight-in-the-heart-of-western-europe.md"),
    ("11.170-the-order-of-the-temple-of-solomon-is-dismantled.md",     "events/ce-1677-the-order-of-the-temple-of-solomon-is-dismantled.md"),
    ("11.180-rex-bellator-plan-unifies-all-military-orders.md",        "events/ce-1679-ce-rex-bellator-plan-unifies-all-military-orders.md"),
    ("11.190-the-almogavars-conquer-athens-and-neopatria.md",          "events/ce-1681-the-almogavars-conquer-athens-and-neopatria.md"),
    ("11.200-deep-state-solidifies-central-banking.md",                "events/ce-1694-deep-state-solidifies-central-banking.md"),
    ("11.210-last-sprinkling-of-absu-dust.md",                         "events/ce-1700-last-sprinkling-of-absu-dust.md"),
    ("11.220-deep-state-breaks-up-the-hordian-empire.md",              "articles/17th-century-romanovs-rise-to-power/deep-state-breaks-up-the-hordian-empire.md"),
    ("11.230-cathars-are-annihilated-in-a-reversed-holy-crusade-inquisition.md", "articles/17th-century-romanovs-rise-to-power/cathars-are-annihilated-in-a-reversed-holy-crusade-inquisition.md"),
    ("11.240-jesuits-missions-convert-asians-to-buddhism.md",          "articles/17th-century-romanovs-rise-to-power/jesuits-missions-convert-asians-to-buddhism.md"),
    ("11.250-secret-society-of-jesus-goes-public.md",                  "events/ce-1718-secret-society-of-jesus-goes-public.md"),
    ("11.260-the-rebellion-of-pugachev.md",                            "events/ce-1773-the-rebellion-of-pugachev.md"),
    ("11.270-the-mudflood-and-world-cataclysm.md",                     "events/ce-1774-the-mudflood-and-world-cataclysm.md"),
    ("11.280-napoleonic-wars.md",                                      "events/ce-1803-napoleonic-wars.md"),
    ("11.290-napoleon-invades-russia.md",                              "events/ce-1812-napoleon-invades-russia.md"),
    ("11.300-ecliptic-pathway-of-the-absu-last-seen.md",               "events/ce-1840-ecliptic-pathway-of-the-absu-last-seen.md"),
    ("11.310-tchaikovsky-releases-1812-overture.md",                   "events/ce-1880-tchaikovsky-releases-1812-overture.md"),
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def update_md_paths(entries, old_to_new):
    """Recursively update md_path in events.json entries."""
    for entry in entries:
        old = entry.get("md_path", "")
        if old in old_to_new:
            entry["md_path"] = old_to_new[old]
        if "children" in entry:
            update_md_paths(entry["children"], old_to_new)


def main():
    content_dir = os.path.join(REPO, "content")
    os.makedirs(content_dir, exist_ok=True)

    old_to_new = {}  # old relative path → new relative path (content/XX.YY-slug.md)
    errors = []

    print(f"\n── Copying files to content/ ──────────────────────────────────────")
    for new_name, old_rel in MAPPING:
        src = os.path.join(REPO, old_rel)
        dst = os.path.join(content_dir, new_name)
        if not os.path.exists(src):
            errors.append(f"MISSING: {old_rel}")
            print(f"  MISSING  {old_rel}")
            continue
        shutil.copy2(src, dst)
        old_to_new[old_rel] = f"content/{new_name}"
        print(f"  OK  {new_name}")

    # ── Update events.json ─────────────────────────────────────────────────────
    events_path = os.path.join(REPO, "data", "events.json")
    with open(events_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    update_md_paths(data.get("entries", []), old_to_new)

    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n── events.json updated ({len(old_to_new)} paths rewritten) ───────────")

    if errors:
        print(f"\n── ERRORS ({len(errors)}) ─────────────────────────────────────────")
        for e in errors:
            print(f"  {e}")
    else:
        print("\n✓ All files migrated successfully.")

    # ── Delete old source files ────────────────────────────────────────────────
    print(f"\n── Removing old files ─────────────────────────────────────────────")
    for new_name, old_rel in MAPPING:
        src = os.path.join(REPO, old_rel)
        if os.path.exists(src):
            os.remove(src)
            print(f"  DELETED  {old_rel}")

    # Remove now-empty article subdirectories
    articles_dir = os.path.join(REPO, "articles")
    for subdir in sorted(os.listdir(articles_dir)):
        subpath = os.path.join(articles_dir, subdir)
        if os.path.isdir(subpath):
            remaining = [f for f in os.listdir(subpath) if not f.startswith('.')]
            if not remaining:
                os.rmdir(subpath)
                print(f"  RMDIR    articles/{subdir}/")

    print("\n✓ Done. Run: npm run validate-events && npm run generate-index")


if __name__ == "__main__":
    main()
