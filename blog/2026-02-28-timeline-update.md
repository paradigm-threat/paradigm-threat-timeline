# Timeline Update: New Chapters 13–15, Ch11 Reorganization, 3-Tier Export Hierarchy, and Animation Module

*February 28, 2026 — Paradigm Threat*

---

Seven commits since the last update bring the project to **v1.1.40** with **178 entries** and **327 content/media files**. Three entirely new chapters added (13, 14, 15), chapter 11 reorganized into thematic groups, author profiles and credits bumped to chapters 16–17, a 3-tier Part/Chapter/Sub-section hierarchy implemented in PDF & DOCX exports, and a new interactive animation module launched.

---

## New Chapter 13: 19th Century — The Rise of Communism (9 articles)

A full chapter tracing the 19th century as the period when the remnants of the Rus-Horde finally lost their grip on Eurasia:

- **13.00.00** — Chapter root: The century of manufactured prophets. After Pugachev's rebellion and the Napoleonic wars, the old empire was carved into competing nation-states with manufactured "ancient" histories
- **13.03.00 — The Battle for Communism's Soul: Marx vs. Kinkel** — The 19th century produced a *war* between radically different visions of communal ownership. Marx's version won not on merit but through mass-distribution via controlled publication networks. Gottfried Kinkel's romantic democratic socialism and Ivan Kinkel's synthetic evolutionary model were suppressed
- **13.03.01 — The Hijacking of Communism** — How Marx's version was specifically designed to make the transition to republicanism impossible by requiring total destruction of every existing institution
- **13.04.00 — The Assault on Hordian Memory** — Systematic destruction of the old imperial memory through language standardization, calendar reform, and institutional rewriting
- **13.05.00 — The Jesuit Restoration and the Missionary-Military Pattern** — The 1814 Jesuit restoration and its continuation of the infiltration-documentation-intervention cycle
- Existing Napoleonic wars, Napoleon invades Russia, Absu last seen, and 1812 Overture articles migrated from ch12 to ch13
- New images: `marx-vs-kinkel.png`, `gottfried-kinkel.png`, `gottfried-kinkel-escape.png`

---

## New Chapter 14: 20th Century — The 1917 Revolution (6 articles)

The Bolshevik Revolution as the final act of the centuries-long campaign to destroy the Rus-Horde:

- **14.00.00** — Chapter root: The 1917 revolution examined not as the triumph of the proletariat but as the completion of a script begun in 1613
- **14.01.00 — The Bolshevik Revolution** — Lenin's seizure and the systematic destruction of churches, documents, communal land systems, and memory-keepers
- **14.01.01 — The Aftermath: Flight, Exile, and Erasure** — Ivan Kinkel's story: Lenin's personal invitation to chair the Supreme Economic Council, Kinkel's refusal, the destruction of Lenin's letter during flight through Makhno's Ukraine, and the broader intellectual exodus (Philosophy Steamer, Pitrim Sorokin, Prokopovich, Berdyaev)
- **14.01.02 — The Hijacking of Communism (1921)** — The New Economic Policy as surrender; how every socialist revolution follows the same fork toward either dictatorship or republicanism
- **14.02.00 — The Russian Intellectual Emigration** — The wave of expelled scholars and theologians who carried suppressed knowledge to Western universities
- **14.03.00 — Soviet Historiography** — How the Soviet state rewrote Russian history to serve the regime's needs, destroying primary sources and manufacturing continuity
- **14.04.00 — From Missionaries to Corporations** — The 20th-century succession from Jesuit infiltration missions to SIL International, Wycliffe Bible Translators, and CIA-linked NGOs. The same operational pattern (linguistic fluency, cultural immersion, intelligence gathering) with secular institutional actors
- New image: `ivan-kinkel.png`

---

## New Chapter 15: 21st Century — The Final Struggle (2 articles)

- **15.00.00 — The Final Struggle** — The culmination of every thread in the timeline: the Pyramidal Empire's technocratic grid of finance, surveillance, and narrative control — and the antibodies it has generated. Historical pattern of resistance leaders who disrupted operations
- **15.01.00 — Predictive Programming: Fiction as Control** — How future plans and suppressed knowledge are embedded in entertainment media (Wizard of Oz, Matrix, Harry Potter, War of the Worlds) to psychologically inoculate populations. Two-directional technique: forward programming (announcing planned events) and backward programming (reframing historical truths as fantasy)

---

## Chapter Structure Reorganization

### Author Profiles → Chapter 16, Credits → Chapter 17

The 24 author profiles (Morozov, Thornhill, Juergens, Velikovsky, Fomenko, Talbott, Peratt, Jno Cook, de Grazia, Scott, Cochrane, de Santillana & von Dechend, Illig, Heinsohn, Cardona, Clube & Napier, Stecchini, Vaughan, van Flandern, van der Sluijs, Ginenthal, Schoch, Hancock, Cremo) were bumped from chapter 15 to **chapter 16** to make room for the new Final Struggle content. Credits moved to **chapter 17**.

All author profile articles were trimmed to concise summaries (biography cruft removed), reducing total author profile content from ~900 lines to ~250 lines.

### Chapter 11: Reorganized into 6 Thematic Groups (35 articles)

The 17th-century chapter was reorganized from a flat chronological list into six thematic sections:

1. **11.01 — The Romanov Seizure** (1611–1627): Dynasty takeover and fracturing of the empire
2. **11.02 — Resistance and Religious Wars** (1618+): Counter-movements against the new order
3. **11.03 — The MARFULL Framework**: Mediterranean realignment and the Byzantine-Catalan alliance
4. **11.04 — London 1664–1694: The Financial Coup**: Great Comet, Great Plague, Great Fire, goldsmiths' death of independent valuation, Dutch fleet burning, the Cabal — all grouped as a coordinated financial takeover
5. **11.05 — Jesuit Global Operations**: 17th-century Jesuit missions converting Asians to Buddhism, secret society going public (1718)
6. **11.06 — The British Empire as Deep State Instrument**: How the East India Company model became the template for invisible governance

New group introduction articles added for each thematic section. Shakespeare article renumbered to `11.01.05`.

---

## 3-Tier Part/Chapter/Sub-section Export Hierarchy

The PDF and DOCX generators were refactored to use a proper 3-tier hierarchy:

- **Part** — top-level groupings (Before Creation, Golden Age, Dark Ages, etc.)
- **Chapter** — numbered sections within each part
- **Sub-section** — individual articles within chapters

Changes:
- Table of contents now renders on its own page with Part/Chapter/Sub-section labels and leader dots
- Duplicate H1 headers stripped — the hierarchy label *is* the heading
- DOCX TOC updated to match the same Part/Chapter/Sub-section format as the PDF
- Both exports regenerated with every structural commit

---

## Animation Module (New)

A new `animation/` directory containing an interactive visualization framework built with **Three.js** (planetary 3D) and **Leaflet** (map view):

### Planetary View (Golden Age / BCE)
- **Collinear Saturnian configuration**: Saturn, Venus, Mars, Earth, Jupiter aligned along a central axis pointing at the Sun
- **Mercury, Neptune, Uranus** added as additional bodies
- **3 orbital styles**: collinear column, circular orbits, elliptical orbits — togglable via UI controls
- Plasma/glow effects for Venus, ring system for Saturn (CE only per Saturnian Cosmology rules)
- Camera orbits the collinear stack; bodies rendered with correct relative sizing

### Map View (CE / Post-Dark-Age)
- Leaflet map with **GeoJSON empire boundaries** for the Rus-Horde expansion and fragmentation phases
- Event markers from `animation/data/events.js` synced to a timeline scrubber
- Empire phase overlays showing territorial changes

### Infrastructure
- **Vite** build system with Three.js and Leaflet dependencies
- 1,635 lines of source across 6 modules (`main.js`, `planets.js`, `map.js`, `planetController.js`, `mapController.js`, `utils.js`)
- Pre-built dist included for static hosting
- Development tracked in `docs/ANIMATION_TRACKER.md`

---

## Other Changes

- **Peratt PDFs moved** from ch15 to ch01 (where the Peratt petroglyphs content lives)
- **Content reduction**: Author profiles trimmed from full biographies to concise summaries, contributing to the ≤400-page print target
- Gottfried Kinkel escape image optimized (4.1 MB → 3.5 MB)
- Cross-references updated across ch05, ch07, ch08, ch09, ch10 for all renumbered articles

---

## Summary of Numbers

| Metric | Before | After |
|--------|--------|-------|
| Total entries | 156 | 178 |
| Content + media files | ~320 | 327 |
| Chapters | 15 + author profiles + credits | 17 (15 content + profiles + credits) |
| Ch11 thematic groups | flat list | 6 groups |
| New articles this session | — | 22+ |
| Animation source lines | — | 1,635 |
| Commits | v1.1.31 | v1.1.40 |
