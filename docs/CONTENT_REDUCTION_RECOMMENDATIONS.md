# Content Reduction Recommendations — Mar 9, 2026

Analysis of `content/` against `docs/CONTENT_REDUCTION_TRACKER.md` targets.
**Do not implement without user approval.**

---

## Current State vs Target

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Main-book articles | **167** | ≤ 140 | **+27** |
| Main-book words | **~84,000** | ≤ 70,000 | **+14,000** |
| Est. pages | ~420 | ≤ 350 | +70 |

**Strategy:** Overflow to appendix first (no loss of detail). Merge small files to reduce recto blanks. Condense largest articles where overflow is not enough.

---

## Phase 1: Merge Stubs and Tiny Files (saves ~15–20 articles)

**Rationale:** Files under ~150 words are effectively stubs or cross-reference placeholders. Merging into parents removes recto blanks with minimal narrative impact.

### Tier 1 — Replace with inline cross-ref, delete file

| File | Words | Action |
|------|-------|--------|
| `15.03.00-controlled-opposition-gatekeeping.md` | 64 | Add 1-sentence cross-ref in `15.00.00` or `15.07.00`; delete. Event ID stays; redirect to appendix. |
| `09.03.00-jesuit-ops-stub.md` | 107 | Add 1–2 sentences to `09.00.00` or `09.02.01`; delete. Cross-ref Jesuit Ops appendix. |
| `03.04.02-pyramids-were-portals.md` | 116 | Merge into `03.04.00-all-planets-enter-stable` or `03.04.03-pyramids-myths-vs-reality`. |
| `10.04.00-jesuits-reach-africa.md` | 120 | Merge into `10.00.00` or `10.02.00-jesuits-make-pilgrimage` (Jesuit arc). |
| `13.01.01-1812-ce-napoleon-invades-russia.md` | 120 | Merge into `13.01.00-napoleonic-wars-reverse` (parent). |
| `15.02.01-1942-ce-asimov-marx-in-space.md` | 165 | Already a stub pointing to appendix. Merge thesis + cross-ref into `15.02.00` or `15.01.00`; delete. |
| `02.10.00-seven-days-of-creation-a.md` | 144 | Merge into `02.00.00` or nearest cosmology parent. |
| `09.00.00-1400-ce-15th-century-intro.md` | 162 | Merge into first substantive article of Ch 09, or keep as lone chapter opener. |

**Est. articles removed:** ~8

### Tier 2 — Merge small files into parents (< 300 words)

| File | Words | Merge into |
|------|-------|------------|
| `03.04.00-all-planets-enter-stable.md` | 174 | `03.04.01` or `03.03.00` |
| `03.07.00-sodom-gomorrah.md` | 255 | `03.08.00` (Passover/Venus sequence) or keep standalone if dated |
| `03.03.00-planets-at-war.md` | 253 | `03.02.00` or `03.04.00` |
| `02.03.00-saturn-collinear.md` | 256 | `02.00.00` or `02.01.00` |
| `02.06.00-southern-configuration.md` | 262 | `02.05.00-northern` (single "configurations" section) |
| `02.08.00-priori-mars.md` | 266 | `02.00.00` or `02.07.00-atlantis` |
| `02.02.00-225-day-year.md` | 294 | `02.00.00` |
| `02.00.00-golden-age.md` | 296 | Keep as chapter opener |
| `04.02.00-other-challenges-chronology.md` | 258 | Merge into `04.01.00-building-new-chronology` |
| `04.01.00-building-new-chronology.md` | 272 | Consider → Appendix 16.xx (methodology) |
| `12.03.00-mudflood-world-cataclysm.md` | 263 | Merge into `12.04.00-instant-fossilization` or vice versa |
| `12.02.00-carbon-14-spike.md` | 284 | Merge into `12.04.00` or `12.01.00-pugachev` |
| `03.10.00-mars-earth-mercury-finalize.md` | 281 | `03.10.01` or `03.12.00` |
| `09.01.00-meteorite-yaroslavl.md` | 225 | `09.00.00` |
| `09.01.03-hundred-years-war.md` | 278 | `09.01.02-fall-constantinople` or `09.00.00` |
| `09.02.00-gutenberg-bible.md` | 281 | `09.02.01-language-deep-state` |
| `10.01.00-protestant-reformation.md` | 235 | `10.00.00` or `10.03.00-holy-inquisition` |
| `13.03.01-orphan-trains.md` | 257 | `13.03.00-assault-on-hordian` |
| `15.02.00-predictive-programming.md` | 261 | Keep; already minimal. Or merge into `15.01.00` |
| `11.02.00-resistance-religious-wars.md` | 304 | `11.00.00` or `11.02.01` |
| `14.08.00-mars-literature.md` | 304 | → Appendix 16.02.01 (Mars Author Profiles); stub in main |
| `09.01.02-fall-constantinople.md` | 305 | Keep — key dated event |
| `11.02.05-russia-turkey-300-years.md` | 308 | `11.02.00` or `11.00.00` |
| `00.03.02-timeline-synchronization.md` | 373 | → Appendix 16.12.00; stub in 00.03.00 |
| `00.03.01-length-of-year.md` | 431 | → Appendix 16.12.01; stub in 00.03.00 |
| `00.02.02-authors-cataclysm-texts.md` | 357 | → Appendix 16.xx; stub in 00.02.00 |

**Est. articles removed (Tier 2):** ~12–15 (some "merge into" targets overlap)

**Phase 1 total est.:** 20–23 fewer articles → **~144–147 articles**

---

## Phase 2: Overflow Large Articles to Appendix (saves ~10–14K words)

**Rationale:** Main book = dated timeline, story pacing. Appendix = investigations, tables, extended evidence.

### Ch 15 — Primary overflow targets

| File | Words | Action |
|------|-------|--------|
| `15.00.00-2000-ce-21st-century-final-struggle.md` | **2,302** | Overflow: "Europe's War: Six Operators" table (~400w), "America's Escalation" section (~500w), "WW3 Blueprint" hybrid table (~300w) → New `16.xx` "21st Century Geopolitics Extended". Condense Immune Response, Infighting, Preparation to ~600w. **Est. save:** ~1,200w |
| `15.07.01-trump.md` | **1,949** | Overflow: biographical timeline, detailed quote blocks → `16.xx` "Historical Antibodies: Trump Case Study". Main keeps thesis + 2–3 key points (~400w). **Est. save:** ~1,500w |
| `15.04.00-false-flags-architecture.md` | **1,885** | Overflow: extended case studies, evidence tables → `16.21.00` (already exists). Main keeps framework + 1 para per pattern (~400w). **Est. save:** ~1,500w |
| `15.07.00-historical-antibodies.md` | 893 | Overflow: pattern analysis → `16.20.00`. Stub in main. **Est. save:** ~600w |
| `15.01.00-censorship-book-burning.md` | 704 | Overflow: century-spanning survey → `16.05.00` or new 16.xx. Stub. **Est. save:** ~500w |
| `15.05.00-population-control.md` | 428 | Condense or overflow case list → appendix. **Est. save:** ~200w |

### Ch 14 — Secondary overflow

| File | Words | Action |
|------|-------|--------|
| `14.12.01-world-war-ii-aftermath.md` | **2,134** | Overflow: extended Nuremberg/NATO/denazification evidence → `16.11.01` or new 16.xx. Main keeps dated narrative (~600w). **Est. save:** ~1,500w |
| `14.01.00-world-war-i.md` | 1,335 | Condense alliance/trigger sections; overflow Parvus/House/Warburg tables → appendix. **Est. save:** ~400w |
| `14.12.00-world-war-ii.md` | 1,642 | Condense; overflow extended evidence. **Est. save:** ~400w |

### Ch 00 — Methodology overflow

| File | Words | Action |
|------|-------|--------|
| `00.03.02-timeline-synchronization.md` | 373 | → Full article in appendix; 1–2 sentence stub in 00.03.00. |
| `00.03.01-length-of-year.md` | 431 | → Full article in appendix; stub in 00.03.00. |
| `00.02.02-authors-cataclysm-texts.md` | 357 | → Full article in appendix; stub in 00.02.00. |

**Phase 2 total est.:** ~8,000–10,000 words overflowed → **~74,000–76,000 main-book words** (still over 70K; may need Phase 3)

---

## Phase 3: Prose Tightening and Further Condensation

If after Phases 1–2 the main book is still > 70K words:

- **14.12.01, 14.01.00, 14.12.00:** Aggressive overflow of evidence blocks (quotes, tables) to appendix.
- **15.00.00:** Further condense "Preparation for the Event" and "The Immune Response" to bullets or 1 para each.
- **00.00.00-introduction.md (768w):** Tighten tech disillusionment arc, thesis restatement.
- **Chapter intros (08.00, 09.00, 10.00, etc.):** Ensure no list exceeds 4 bullets; convert to prose where possible.

**Est. save:** ~2,000–4,000 additional words

---

## Phase 4: Image Compression — SKIPPED

Image compression is handled automatically by the PDF generation script. No manual step required.

---

## Recommended Execution Order

1. **Phase 1 (merges)** — Reduces article count; updates `events.json` `md_path` for merged events; run `npm run normalize-events` and `npm run validate-events`.
2. **Phase 2 (overflow)** — Move content to new/existing appendix files; replace main-book articles with stubs. Preserves all detail.
3. **Phase 3 (tightening)** — Only if still over 70K.
4. **Phase 4 (images)** — Final pass before print.

---

## Merge Implementation Notes

- When merging file A into B: append A's body to B (remove duplicate H1); update `events.json` to point merged event to B's path; delete A.
- When moving to appendix: create new 16.xx file with full content; replace main file with 2–4 sentence stub + cross-ref to appendix.
- After each batch: `npm run normalize-events`, `npm run refactor-sections`, `npm run validate-events`, `npm run generate-index`.

---

## Summary

| Phase | Articles saved | Words saved (est.) |
|-------|----------------|-------------------|
| Phase 1 (merges) | 20–23 | ~500 (content preserved in parents) |
| Phase 2 (overflow) | 3–5 (stub replacements) | 8,000–10,000 |
| Phase 3 (tightening) | 0 | 2,000–4,000 |
| **Total** | **23–28** | **10,500–14,500** |

**Projected result:** ~139–144 articles, ~69,500–73,500 words — within or very close to target.
