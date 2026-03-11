# Timeline Update: Stolen Credit Suite, Yakuza Investigation, Site SSR, and TTS Improvements

*March 11, 2026 — Paradigm Threat*

---

One day since the last update: paradigm-threat-timeline v1.2.43 → **v1.2.51**; paradigm-threat-files expanded with nine stolen-credit investigations and the Yakuza remote-control thesis; paradigm-threat-site gained server-side rendering for articles and article TTS parity with the timeline overlay. The stolen-credit corpus is now the largest single investigation area on the site.

---

## Stolen Credit Suite (paradigm-threat-files)

Nine investigations added or expanded in [Stolen Credit](/influence/stolen_credit):

### Video Game Composers (7 files)

| Investigation | Summary |
|---------------|---------|
| [Dave Wise / Rare](/influence/stolen_credit/dave-wise) | DKC3 GBA amateur dive; sampling/QA thesis vs. composition; Eveline Fischer major contributor; Yukio Kaneoka (Nintendo) on Aquatic Ambience copyright; Tropical Freeze/Returns Hamano pattern; Prime 4 credit anomaly |
| [Minako Hamano](/influence/stolen_credit/minako-hamano) | Super Metroid (Ridley, Maridia, Mother Brain); "often credited only to Yamamoto"; Returns/Tropical Freeze excellence; Prime 4 Beyond soundtrack disaster |
| [Rare & Nintendo R&D](/influence/stolen_credit/rare-nintendo-rd) | Games without credits — Battletoads, PIN·BOT; 335 games in VGMPF; Nintendo R&D contribution thesis |
| [Capcom / Mega Man](/influence/stolen_credit/capcom) | Platform betrayal, composer churn, leftover theory; MM9 from original projects |
| [Yasunori Mitsuda](/influence/stolen_credit/yasunori-mitsuda) | Chrono Trigger third hands; Chrono Cross RD Edition corruption; franchise corruption thesis |
| [Koji Kondo](/influence/stolen_credit/koji-kondo) | Nintendo institutional support; Kaneoka; unrecognized Zelda composers |
| [Robin Beanland](/influence/stolen_credit/robin-beanland) | DKC Aquatic Ambience four-way copyright; role vs. Wise/Fischer |

### Nintendo–Sony Breakup (1 expansion)

- **Super Mario RPG section** added to [Nintendo–Sony Breakup](/influence/stolen_credit/nintendo-sony-breakup): Suspicious timing (1995–96); Square courting Sony while Nintendo believed the collaboration signified commitment; the game as "reassurance signal" or sincere last gesture before the divorce; connection to stolen-credit thesis.

### Classical Composers (2 files)

| Investigation | Summary |
|---------------|---------|
| [Fanny Mendelssohn](/influence/stolen_credit/fanny-mendelssohn) | 6 songs under Felix's name; Easter Sonata misattributed 40 years |
| [Ferde Grofé](/influence/stolen_credit/ferde-grofe) | Rhapsody in Blue orchestration; blurry composition line |

### Methodology

- [VGM Preservation / Credits](/influence/stolen_credit/vgm-preservation-credits) — 335 games without credits; publisher policies; ROM/hex methodology

---

## Yakuza Remote-Control Investigation

New governance investigation: [Yakuza Remote Control: British Influence, Media Capture, and Technology Containment in Japan](/governance/war/investigations/yakuza-remote-control-investigation).

**Thesis:** The Yakuza may function as a remote-controlled instrument of Western (chiefly British) interests in Japan — enforcing compliance, media capture, and technology containment.

**Sections:**
- Yakuza influence on Japanese media (Kobe Geinosha 1957; post-WWII entrenchment; Adelstein; talent agencies)
- Nintendo–Sony CD-ROM and technology containment — parallel to Taiwan chip situation; technology channeled through Western-approved partners
- Assassination of Shinzo Abe (July 2022) — alternative reading; "nobody said anything"
- Consolidation of power after natural disasters
- Ideological separation of youth and elderly; mockery of tradition

**Linked:** [nintendo-sony-breakup](/influence/stolen_credit/nintendo-sony-breakup) for technology containment thesis.

---

## paradigm-threat-site: SSR and TTS

### Server-Side Rendering (Crawlers)

Articles are now server-rendered for SEO and crawling:
- `fetchArticle` + `compileMDX` (next-mdx-remote/rsc) — full article HTML in first response
- Removed `isHydrated` gates in root/main layouts so crawlers receive content instead of a loading shell
- `generateMetadata` for per-article title and description
- Directory listings remain client-side (require fileList)

### Article TTS Parity

Article TTS now matches timeline overlay capabilities:
- **Retry** (3 attempts) with Retry button
- **Seekable progress bar** — scrub to any position
- **DOM-only scroll sync** — preserve styles; no layout shift
- **Double-click to jump** — jump to sentence from article text
- Same options as timeline overlay (voice, rate, provider, Piper, speaker map, etc.)

### Other Site Changes

- Article nav; race condition fix; autolink preprocessing; metadata filter; extensionless URLs
- PWA: `_version` in index.json for cache busting

---

## paradigm-threat-timeline

- **Event title/header validation** — Fix validation; register appendix extended articles
- **Introduction** — "Intellectual challenge" framing
- **Overview image** — Updated; package version bump v1.2.43 → v1.2.51

---

## paradigm-threat-files

- **Root-relative URLs** — Fix links; remove dead wget references
- **PWA cache busting** — `_version` in index.json

---

## Stats

| Metric | Previous (Mar 10) | Current (Mar 11) |
|--------|-------------------|-------------------|
| Timeline version | 1.2.43 | 1.2.51 |
| Stolen-credit investigations | ~10 | 20 |
| New governance investigation | — | Yakuza remote control |
| Site rendering | Client-only | SSR for articles |
| Article TTS | Basic | Full parity with timeline overlay |

> **Stolen credit is now the largest single investigation topic.** The corpus spans video game composers (Rare/Nintendo, Square, Capcom), classical music (Mendelssohn, Grofé, Mozart, Gershwin, Beethoven), and methodology (VGM preservation, 335 games without credits). The Yakuza investigation bridges governance, technology containment, and the Nintendo–Sony thesis.
