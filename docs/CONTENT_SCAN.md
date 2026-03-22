# Content scan: chapters 05–15

Snapshot of **timeline book content** under `content/` — markdown event/chapter files only. Generated from line and byte totals (`wc`); counts include blank lines and headings.

| Ch | Folder (short) | Articles | Lines | Bytes | Avg lines/article |
|----|----------------|----------|-------|-------|-------------------|
| 05 | `05.ce-11th-common-era-begins` | 5 | 195 | 19,842 | 39.0 |
| 06 | `06.ce-12th-birth-of-christianity` | 8 | 266 | 32,408 | 33.3 |
| 07 | `07.ce-13th-the-russian-horde-tartarian-empire` | 6 | 205 | 22,922 | 34.2 |
| 08 | `08.ce-14th-great-expansion-of-the-mongol-slav` | 7 | 276 | 28,113 | 39.4 |
| 09 | `09.ce-15th-ottoman-conquest-of-europe` | 8 | 294 | 28,668 | 36.8 |
| 10 | `10.ce-16th-reformation-and-inquisition` | 11 | 466 | 49,303 | 42.4 |
| 11 | `11.ce-17th-romanovs-rise-to-power` | 20 | 599 | 77,725 | 30.0 |
| 12 | `12.ce-18th-mudflood-and-pugachev` | 9 | 411 | 38,313 | 45.7 |
| 13 | `13.ce-19th-rise-of-communism` | 12 | 442 | 52,281 | 36.8 |
| 14 | `14.ce-20th-the-1917-revolution` | 18 | 725 | 82,128 | 40.3 |
| 15 | `15.ce-21st-the-final-struggle` | 9 | 234 | 28,933 | 26.0 |

**Totals (chapters 05–15):** 113 articles, ~4,113 lines (sum of per-file counts; minor rounding).

---

## Most content (by chapter)

1. **14 — 20th century / 1917 revolution** — **725 lines**, 18 articles. Densest narrative block; world wars, revolution, Cold War threads.
2. **11 — 17th century / Romanovs** — **599 lines**, **20 articles** (most files of any chapter). Many shorter pieces; chapter spreads volume across more entries.
3. **10 — 16th century / Reformation & Inquisition** — **466 lines**, 11 articles.
4. **13 — 19th century / communism** — **442 lines**, 12 articles.
5. **12 — 18th century / mudflood & Pugachev** — **411 lines**, 9 articles; **highest average length per article** (~46 lines).

## Least content (by chapter)

1. **05 — 11th century / CE begins** — **195 lines**, 5 articles (fewest files).
2. **07 — 13th century / Russian Horde** — **205 lines**, 6 articles.
3. **15 — 21st century / final struggle** — **234 lines**, 9 articles. Several **stub-length** files pull the average down (~26 lines/article) despite the long chapter intro.

---

## Article count only

| Rank | Chapter | Articles |
|------|---------|------------|
| Most | 11 | 20 |
| | 14 | 18 |
| | 13 | 12 |
| | 10 | 11 |
| Least | 05 | 5 |
| | 07 | 6 |
| | 08 | 7 |

---

## Longest single articles (lines, chapters 05–15)

Useful for “where did the words go?”

| Lines | Path |
|------:|------|
| 103 | `15.ce-21st-the-final-struggle/15.00.00-21st-century-the-final-struggle-reverse-crusade-iv.md` |
| 89 | `14.ce-20th-the-1917-revolution/14.12.00-world-war-ii-reverse-crusade-iii.md` |
| 85 | `14.ce-20th-the-1917-revolution/14.01.00-world-war-i-reverse-crusade-ii.md` |
| 80 | `12.ce-18th-mudflood-and-pugachev/12.08.00-trail-tears-century-long-erasure.md` |
| 69 | `08.ce-14th-great-expansion-of-the-mongol-slav/08.01.00-1300-ce-european-religious.md` |
| 67 | `10.ce-16th-reformation-and-inquisition/10.05.01-cathar-khazar-katya-link.md` |
| 65 | `11.ce-17th-romanovs-rise-to-power/11.01.03-shakespeare-encodes-the-horde.md` |
| 61 | `12.ce-18th-mudflood-and-pugachev/12.05.00-1774-ce-the-mars-catastrophe.md` |
| 58 | `12.ce-18th-mudflood-and-pugachev/12.00.00-18th-century-ce-mudflood-and-pugachev.md` |
| 52 | `14.ce-20th-the-1917-revolution/14.11.00-flexner-report-suppression-of.md` |

---

## Shortest articles (stubs / minimal entries)

Files at **≤5 lines** are effectively placeholders or near-empty; worth expanding or merging when editing.

| Lines | Path |
|------:|------|
| 3 | `14.ce-20th-the-1917-revolution/14.12.01-world-war-ii-aftermath.md` |
| 3 | `15.ce-21st-the-final-struggle/15.01.00-censorship-book-burning-from.md` |
| 3 | `15.ce-21st-the-final-struggle/15.07.01-trump.md` |
| 5 | `15.ce-21st-the-final-struggle/15.04.00-false-flags-architecture-of.md` |

Other very short (11–15 lines) cluster in **ch.15** and **ch.11**; see repository search or `wc -l` on `content/1[0-5].*` as needed.

---

## How to refresh

From repo root (`paradigm-threat-timeline`):

```bash
cd content
for d in 0[5-9].* 1[0-5].*; do
  [ -d "$d" ] || continue
  n=$(find "$d" -name '*.md' | wc -l)
  lines=$(find "$d" -name '*.md' -exec cat {} + | wc -l)
  echo "$d $n $lines"
done | sort -k3 -n
```

Update the table and rankings after large adds or splits.
