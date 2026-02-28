# Content Reduction Tracker

Track progress toward the ≤ 400 page / ≤ 15 MB print target.
See `docs/PRINT_GOALS.md` §13 for the full strategy.

## Baseline (Feb 28, 2026)

| Metric | Value |
|---|---|
| Total pages | 792 |
| PDF file size | 47 MB |
| Total words | 146,863 |
| Total articles | 176 |
| Embedded images | 142 |

## Target

| Metric | Value |
|---|---|
| Total pages | ≤ 400 |
| PDF file size | ≤ 15 MB |
| Total words | ≤ 90,000 |
| Embedded images | ≤ 80 |

---

## Reduction Log

Record each reduction pass below. One row per editing session.

| Date | Chapter / File | Technique | Words before | Words after | Pages saved (est.) | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## Chapter Word Counts (baseline Feb 28, 2026)

| Ch | Folder | Files | Words | Est. pages |
|---|---|---|---|---|
| 00 | overview | 10 | 13,400 | 45 |
| 01 | before-creation | 5 | 6,378 | 21 |
| 02 | the-golden-age | 10 | 8,316 | 28 |
| 03 | the-dark-ages | 17 | 8,140 | 27 |
| 04 | the-blip | 3 | 4,487 | 15 |
| 05 | ce-11th | 5 | 5,417 | 18 |
| 06 | ce-12th | 8 | 5,828 | 19 |
| 07 | ce-13th | 6 | 9,798 | 33 |
| 08 | ce-14th | 5 | 5,852 | 20 |
| 09 | ce-15th | 11 | 13,663 | 46 |
| 10 | ce-16th | 14 | 12,118 | 40 |
| 11 | ce-17th | 35 | 18,728 | 62 |
| 12 | ce-18th | 6 | 4,714 | 16 |
| 13 | ce-19th | 9 | 12,388 | 41 |
| 14 | ce-20th | 6 | 5,722 | 19 |
| 15 | author-profiles | 25 | 11,851 | 40 |
| 16 | credits | 1 | 64 | 1 |
| **Total** | | **176** | **146,863** | **~490 text** |

---

## Top 10 Largest Files (reduction candidates)

| Words | File | Priority action |
|---|---|---|
| 4,452 | 07.01.01-the-masons.md | Cross-ref with Ch 09/11 Deep State articles |
| 3,448 | 13.03.01-1883-ce-the-hijacking-of-communism.md | Trim quoted sources; tighten narrative |
| 2,806 | 00.03.01-the-length-of-a-year-changes.md | Move detailed math to appendix |
| 2,698 | 09.03.00-language-of-the-deep-state.md | Cross-ref with 07.01.01 Masons |
| 2,507 | 07.01.02-the-giants-of-the-rus-horde.md | Trim block quotes |
| 2,285 | 13.03.00-1848-ce-battle-for-communisms-soul.md | Cross-ref with 13.03.01 |
| 2,264 | 02.07.00-atlantis-and-the-tree-of-knowledge.md | Tighten cosmology preamble |
| 2,238 | 00.02.03-challenging-established-physics.md | Condense; cross-ref author profiles |
| 2,106 | 04.01.00-building-the-new-chronology.md | Cross-ref Fomenko profile in Ch 15 |
| 1,979 | 08.02.01-european-castles-fortresses.md | Reduce repeated evidence lists |

---

## Articles Under 300 Words (merge candidates)

Small child articles that may be merged into their parent to save recto-insert pages.
Review each; if the parent + child combined < 800 words, merge.

To regenerate this list:
```bash
find content/ -name '*.md' -exec sh -c 'w=$(wc -w < "$1"); [ "$w" -lt 300 ] && echo "$w $1"' _ {} \; | sort -rn
```
