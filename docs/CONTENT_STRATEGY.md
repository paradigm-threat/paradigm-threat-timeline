# Content Strategy: Paradigm Threat Timeline

This document outlines the strategy for aligning writing styles, improving pacing and organization, resolving contradictions, recommending new threads and investigations, and guiding content placement across the timeline. **All proposed changes require approval before implementation.**

**Investigative strategy:** How we treat evidence, consensus, and burden of proof is defined in **`docs/INVESTIGATIVE_STRATEGY.md`**. Investigations are conducted objectively from scratch; we do not rule out possibilities due to "scientific consensus" or "lack of evidence" alone. See that doc for burden-of-proof rules, predictive programming as data, and when the burden lies on new scientists.

**Audience book editions:** Strategy for **two** products — definitive **`content/`** (default and educational, one tree), and **`content-editions/modern-religious/`** — is in **`docs/BOOK_EDITIONS_PLAN.md`**. Implementation of export switches for alternate content roots requires the same approval process as other strategy changes.

**Public slogans (Third Story):** *One human family. One shattered memory. One story to reunite it.* — *Sacred memory + honest inquiry = the Third Story.* Documented with sticker assets in **`paradigm-threat-site/public/brand/README.md`** and **`docs/PRINT_GOALS.md`**.

---

## 1. Writing Style Alignment

### Current Variation

Content exhibits several distinct voices that can jar when read sequentially:

| Voice | Examples | Characteristics |
|-------|----------|-----------------|
| **Personal/confessional** | Introduction (00.00.00) | First person, author's journey, faith/tech framing |
| **Technical/scholarly** | Maxwell/Aether (13.06.00), Core Concepts (00.03.00) | Equations, citations, proposition lists, "Observation — not a theory" |
| **Polemical/thesis-driven** | Controlled Opposition (15.02.00), Thunderbolts Case Study | "Author's thesis," argumentative, personal experience |
| **Expository/survey** | Mars Contacts (16.02.00), Building New Chronology (04.01.00) | Dossier format, tables, chronological narrative |
| **Mythological/cosmic** | Atlantis (02.07.00), Dark Ages events | Present-tense cosmic description, sparse citation |
| **Investigative/debate** | Hairy Mary (06.01.01), Operation Mockingbird (14.06.00) | Art-historical argument, Fomenko quote integration |

### Recommended Unified Style

1. **Default voice: Third-person investigative.** Present claims as "this timeline argues" or "sources indicate" rather than "I believe." Reserve first person for explicitly marked author theses.
2. **Author thesis blocks:** When presenting original synthesis, use explicit markup: *"Author's thesis:"* or a dedicated callout. Place at **end of article**, after all cited evidence. Do not interleave personal opinion with sourced claims. The 80/20 rule: ~80% cited evidence, ~20% author thesis. **Exception:** under `content/`, follow **§ Timeline book voice** — show inference chains instead of thesis labels unless a rare exception is requested.
3. **Pack, don't pad.** Every sentence must carry information. Remove expository warm-ups ("In order to understand X…"), restated theses from prior articles, multi-sentence transitions, preambles before block quotes. Let cross-references do the connecting.
4. **Proposition lists:** Reserve numbered propositions for methodology (Core Concepts). Avoid proposition-style exposition in narrative articles.
5. **Tone consistency:** Maintain "investigation, not adjudication" — document claims, trace sources, stay open. Avoid absolute certainty language ("proven," "definitely") unless citing a primary source.
6. **Block quotes:** Prefer short, punchy quotes. Long passages should be summarized with citation. See PRINT_GOALS §13.
7. **Inline emphasis (`content/` only):** Use `**bold**` and `*italic*` sparingly for rhetorical stress—not dense highlighting. Target about **one to four** emphasized spans per paragraph on average (see `docs/CONTENT_MARKDOWN_STYLE.md`). Italics for titles of works follow normal typography and are not “decoration.”

### Style Checklist (for editors/AI)

- [ ] No unexplained first-person unless author thesis block
- [ ] Claims attributed to source or marked as synthesis
- [ ] Cross-references use standard format: `[Title](/timeline/evt-slug)`
- [ ] Links to **paradigm-threat-files** (investigations, `history/`, `governance/`, assets, etc.) use **root-relative** paths from the site root (e.g. `/governance/war/investigations/foo.md`, `/history/chronology/investigations/bar.md`). **paradigmthreat.net** serves that repo at `/`; those paths work on the live site. Timeline events use `/timeline/evt-...` or `/timeline?view=browser&path=content/...`
- [ ] Word count target: 300–800 per article (PRINT_GOALS §13)
- [ ] `content/` Markdown follows `docs/CONTENT_MARKDOWN_STYLE.md` for bold/italic density
- [ ] Long articles (>12 paragraph-blocks): optional `> **TL;DR:**` block present (see § TL;DR below)

### TL;DR summaries (long pieces)

**Scope:** Timeline `content/**/*.md` and paradigm-threat-files markdown (investigations, hubs, etc.) when length warrants it.

**Threshold:** Add a TL;DR when the body (after YAML frontmatter) has **more than 12 paragraph-blocks**. A **paragraph-block** is a non-empty stretch of text separated from the next by one or more blank lines (horizontal-rule-only blocks excluded). Headings count as their own block when separated by blank lines. **Omit** TL;DR when the piece is short enough.

**Markup (option A):**

```markdown
> **TL;DR:** TODO
```

(Replace **`TODO`** with one paragraph in a model/editor pass.)

**Placement:** Immediately after the first `#` line; if a hero image line follows the title, put TL;DR **immediately under the image**, then the rest of the body.

**Substance:** Restate what the file already argues or documents—**no** new theses, citations, or hedges that the body does not support.

**Openers:** Do **not** begin with meta framing such as “this article,” “this chapter,” “this piece,” “here,” or “below we.” Prefer **subject-first** or **neutral declarative** sentences (e.g. “Mainstream chronology may reflect who kept the records,” “The trial record stops at X; the open web only shows Y.”).

**Tone options** (pick one per file and stay consistent with investigative stance):

| Tone | Aim | Example shape (not a template line) |
|------|-----|-------------------------------------|
| **Plain third-person** | Default for timeline book voice; sounds like compressed narrative | Opens on the topic: who did what, what’s disputed, what stays open. |
| **Direct “you”** | Slightly warmer lay access | “You’ll see …” / “Expect …” only when it restates the article’s actual flow—still no “in this article.” |
| **Dry précis** | Maximum compression | Short clauses: topic → claims → limits. Still no “this chapter.” |
| **Investigation file** | Best fit for `paradigm-threat-files` investigations | States what is traced, what is out of scope, what remains unknown—without calling the file “this investigation” in the first words (e.g. “Sources on X are …; Y is left open.”). |

**Exports:** TL;DR lives in the markdown; book PDF/DOCX will include it unless a later filter strips blockquotes—if print layout needs a different treatment, decide in `PRINT_GOALS` / export scripts separately.

**Tooling:** In **paradigm-threat-timeline**, `npm run generate-tldr` runs `scripts/generate_tldr.py` on `content/`, inserting `> **TL;DR:** TODO` where the >12 paragraph-block rule applies. For **paradigm-threat-files**: `python3 scripts/generate_tldr.py --root /path/to/paradigm-threat-files` from the timeline repo. The script **skips** `blog/` and `docs/` and root `REORGANIZATION_MAP.md` / `README.md`. Use `--refresh-tldr` to strip an existing TL;DR line and re-insert `TODO`. **Replace `TODO` with real copy in a dedicated model/editor pass** (not auto-filled by the script).

**Approval:** Bulk retrofits across the corpus require the same editorial sign-off as other strategy changes.

### Timeline book voice (`content/**/*.md` only)

For **print-facing narrative** under `content/`, prefer **demonstrated logic** over **ownership labels**:

1. **Do not** frame arguments as "author thesis," "Paradigm Threat," "author only," or "this site's theory" in ordinary prose.
2. **Do** chain inference: named source **scope** → **gap** → what **else** the chronology already establishes → **conclusion**, in third person or "this chronology holds…".
3. **Exception:** First-person or explicit "thesis" blocks remain acceptable in **intro/overview** pieces where the project already uses confessional voice (e.g. ch.00 intro) — do not retroactively strip those without editorial intent.
4. **Scope:** This convention applies to **timeline `content/`** only; **paradigm-threat-files**, blog, and investigations are unchanged unless separately edited.

---

## 2. Pacing, Organization, Topics, and Themes

### Pacing Recommendations

| Chapter | Current Notes | Recommendation |
|---------|---------------|----------------|
| **00 Overview** | Dense; Core Concepts is proposition-heavy | Split methodology (01) from background. Consider moving "Authors Challenging" to appendix. |
| **01–04 BCE** | Variable; some events very short | Ensure each Dark Ages event has ~300+ words or merge into parent. |
| **05–11 CE** | Good narrative flow; some overlap | Consolidate Deep State, Masons, British Empire into single canonical treatment (see §6). |
| **12–15 CE** | 19th–21st century articles vary widely | Maxwell, Weapons, Nuclear: ensure technical articles don't sprawl. Move long author profiles to appendix. |
| **16 Appendix** | Mars Contacts, False Flags very long | Consider print-only summary + web full text; or split into sub-appendices. |

### Organization Improvements

- **Theme threading:** Create explicit "through-lines" (e.g., Deep State origin → Jesuits → British Empire → Mockingbird → Censorship) with a single canonical article per theme and others cross-referencing.
- **Chronological vs thematic:** Keep timeline chronological; use cross-references for thematic grouping. Avoid duplicate thematic articles in different chapters.
- **Recurring concepts:** Establish canonical definitions for: Deep State, Pyramidal Empire, Rex Bellator, Phantom Time, Revelation of the Method. Link from first use.

### Topics to Strengthen

- **Dating recalibration:** Proposition 6 (C-14, dendrochronology) is asserted but under-developed. Add investigation or dedicated article.
- **Indigenous chronologies:** Quiche Maya, Popol Vuh, etc. mentioned in rules but rarely in content. Recommend new investigation.
- **Electric fossilization:** Instant fossilization article exists; link more explicitly to SAFIRE/plasma transmutation.
- **CERN/portal technology:** Maxwell article raises it; no dedicated investigation. Recommend investigation folder.

### Themes to Clarify

- **Control vs. suppression:** Distinguish "information suppressed" (classified, destroyed) from "information controlled" (managed disclosure, gatekeeping). Both appear; terminology should be consistent.
- **Mars as breakaway civilization:** Establish in one place; reference elsewhere. Currently scattered (Atlantis, Mars Contacts, Death on Mars).

---

## 3. Contradictions and Open Questions

### Contradictions to Resolve

| Contradiction | Location | Action |
|---------------|----------|--------|
| **Phantom time boundaries** | Illig 297 yr (614–911) vs Fomenko ~1053 yr | Add to OUTSTANDING_QUESTIONS: "How do Illig and Fomenko boundaries interact? Nested or overlapping?" |
| **Year Zero identity** | 670 BCE = 1 CE = 1053 CE (Blip) vs Dionysius/Bede rationale | Document in OUTSTANDING_QUESTIONS; add source gap note. |
| **Atlantis city names (Og, Aryan, Poseida)** | 02.07.00; OUTSTANDING_QUESTIONS | Investigation ongoing. Do not present as canonical until resolved. |
| **Carbon-14 spike 774 CE** | Multiple possible dates (774, 1063 BCE, 1774) | Add to OUTSTANDING_QUESTIONS with all interpretations. |
| **Rus-Horde breakup** | 1775 (Fomenko) vs Scaligerian narrative | Cross-reference both in relevant articles; flag in OUTSTANDING_QUESTIONS. |

### Outstanding Questions to Add

- **Joan of Arc naming:** "Maid of Orleans" vs "Joan of Arc" (second half 16th c.). What was she called before? (Already in OUTSTANDING_QUESTIONS — verify.)
- **Requerimiento 1513:** Possibly pushed back ~150 years by redactors. Source verification needed.
- **Creation dates:** Multiple (5969–3491 BCE). How to present without implying single "correct" one?
- **Jerusalem 3-wall/6-gate architecture:** Mars/Atlantis vs Saturn hexagon — combined or separate memory? (Already in OUTSTANDING_QUESTIONS.)

### Update Process

When editing content, if a contradiction or unresolved question appears:
1. Document in `docs/OUTSTANDING_QUESTIONS.md` under appropriate section.
2. Add `(see OUTSTANDING_QUESTIONS)` in the article if the claim is provisional.
3. Do not remove contradictory evidence; present both and flag.

---

## 4. New Threads, Authors, Events, and Investigations

### Recommended New Investigations

| Topic | Rationale | Proposed Path |
|-------|-----------|---------------|
| **CERN and portal technology** | Maxwell article raises it; no systematic research | paradigm-threat-files: `science/cern_portal/` |
| **Heaviside reduction of Maxwell** | Critical to aether thesis; needs primary-source verification | Extend `investigations/maxwell-aether/` |
| **Dayton Miller interferometry** | Maxwell article cites; "dismissed but never refuted" — verify | `investigations/maxwell-aether/03-dayton-miller.md` |
| **Indigenous creation chronologies** | Rules mention; content lacks | `investigations/chronology/indigenous-creation-dates.md` |
| **Joan of Arc naming history** | OUTSTANDING_QUESTIONS | `investigations/joan-of-arc/naming-history.md` |
| **Requerimiento 1513 dating** | OUTSTANDING_QUESTIONS | `investigations/requerimiento-dating.md` |
| **Steinmetz and Heaviside primary sources** | Maxwell article cites; need verification | `investigations/maxwell-aether/04-steinmetz-heaviside-sources.md` |
| **Remote viewing as aether physics** | Maxwell links consciousness to aether; Stargate targeted Mars | Extend `investigations/remote-viewing/` or new `investigations/aether-consciousness/` |
| **Thunderbolts forum deletions** | Controlled Opposition cites; document evidence | `investigations/thunderbolts-forum-archives.md` |
| **Illig vs Fomenko boundary overlap** | Phantom time; clarify relationship | `investigations/chronology/illig-fomenko-boundary.md` |

### Additional Authors/Figures to Profile

| Name | Relevance | Existing |
|------|------------|----------|
| **Robert Potter** (*The Germ Growers*, 1892) | Pre-Wells Mars incursion fiction | Mars Contacts appendix only |
| **Garrett P. Serviss** (*Edison's Conquest of Mars*, 1898) | Unauthorised sequel; counter-invasion | Mars Contacts only |
| **Stephen Baxter** (*The Massacre of Mankind*, 2017) | Authorised sequel; second invasion 1920 | Mars Contacts only |
| **Eric P. Dollard** | Tesla longitudinal waves; aether replication | Maxwell article, investigations |
| **Ken Wheeler** | Magnetism, dielectric; Maxwell investigation | investigations/maxwell-aether |
| **Wilhelm Kammeyer** | Document forgery analysis | Building New Chronology |
| **David Straight** | Chernobyl/probiotics | investigations/probiotics-chernobyl |

### Additional Events to Consider

- **1894 Lick/Nice Mars light** — Already in Mars Contacts; consider main timeline reference.
- **1901 NYT Mars flash** — Same.
- **Battle of Los Angeles 1942** — Could be main timeline event with appendix cross-ref.
- **Quito broadcast 1949** — Deadliest WotW; main timeline mention.
- **Tesla Wardenclyffe demolition** — Link to Maxwell suppression narrative.

---

## 5. No Changes Without Approval

**All edits to content, investigations, or docs that implement recommendations from this strategy document require explicit user approval.**

- AI/agents must not auto-apply strategy recommendations.
- When suggesting changes, present them as proposals with rationale.
- Batch edits (e.g., style pass) should be presented as a checklist for approval before execution.
- Exception: Adding entries to OUTSTANDING_QUESTIONS when a contradiction is discovered during routine editing — this is consistent with existing AGENT_INSTRUCTIONS.

---

## 6. Content Placement: Last Significant Century + Appendix

### Principle

**The bulk of a topic belongs in the chapter for the last significant century in which that topic is active.** Earlier chapters mention the topic briefly with a forward cross-reference. Extended evidence, dossiers, and profiles overflow to the appendix.

This ensures the reader encounters the full treatment at the point of maximum relevance, while earlier chapters remain lean and chronologically focused.

### Placement Rules

1. **Main timeline:** One canonical article per major topic. 300–800 words for standard articles; 800–1500 for canonical topic articles. **The main article must contain all key dates, facts, arguments, and the core thesis.** A reader who never opens the appendix should still get the full picture.
2. **Earlier mentions:** One sentence + link: *"For the full encoding analysis, see [Title](/timeline/evt-slug)."*
3. **Appendix:** Extended evidence **only** — primary-source quotations, detailed source-by-source analysis, exhaustive bibliographies, chronological sub-dossiers. The appendix is for material that supports but does not change the main article's argument. **Never defer core arguments, key dates, event catalogues, or thesis statements to the appendix.** If a reader must consult the appendix to understand the topic, the main article has failed.
4. **Investigations:** Excluded from print. Content articles link via Browser URL.
5. **Anti-overflow test:** Before creating or editing an appendix article, ask: "Does the main article stand alone without this?" If not, move the missing material into the main article first.

### Topic Placement Map

| Topic | Last Significant Century | Canonical Article | Appendix Overflow |
|---|---|---|---|
| Mars literature | 19th–20th (publication era) | 15.06.01 (reclassified nonfiction) | 16.10 (author profiles), 16.02 (contacts) |
| Predictive programming | 20th–21st (Wells→Card) | 15.01.00 (literature) | 16.01 (fiction as control), 16.03 (film/TV) |
| Deep State | 17th (Romanovs/British Empire) | 11.x (canonical) | — |
| Masons | 13th (Horde era) | 07.01.01 | — |
| Jesuits | 16th–17th (operations) | 10.x/11.x (canonical) | — |
| False flags | 21st (architecture) | 15.04.00 | 16.07 (investigation) |
| Nuclear weapons | 20th (1938+) | 14.07.00 | — |
| Maxwell/aether | 19th (suppression) | 13.06.00 | 16.09 (energy X-ref) |
| Weather control | 20th (1946+) | 14.08.00 | — |
| Historical antibodies | 21st (analysis) | 15.03.00 | 16.06 (profiles) |

---

## 7. Periodic Rescan Schedule

Content should be rescanned against this strategy document on a regular basis.

### Rescan Triggers

- **After each major content batch** (e.g., new chapter or 5+ new articles)
- **Before each PDF export** (pre-print review)
- **Quarterly** (e.g., first week of Jan, Apr, Jul, Oct)
- **When OUTSTANDING_QUESTIONS or CONCLUSIONS are updated**

### Rescan Checklist

1. **Writing style:** Sample 3–5 random articles. Check for first-person leakage, unattributed theses, tone consistency.
2. **Cross-references:** Verify all `/timeline/evt-` links resolve. Verify investigation links use Browser URL.
3. **Contradictions:** Re-read OUTSTANDING_QUESTIONS. Confirm no new contradictions introduced without documentation.
4. **Content placement:** For each major theme (Deep State, Jesuits, Masons, etc.), confirm canonical article exists and others cross-reference.
5. **Word counts:** Run `wc -w content/**/*.md`; flag articles >1500 words for trim or split.
6. **New investigation opportunities:** After adding content, ask: "Does this claim need an investigation folder?"

### Rescan Output

Append to `docs/CONTENT_REDUCTION_TRACKER.md` or create `docs/STRATEGY_RESCAN_LOG.md`:

```
## [Date] Rescan

- Style issues found: [list]
- Cross-refs broken: [list]
- Contradictions flagged: [list]
- Placement violations: [list]
- New investigation recommendations: [list]
```

---

## References

- `docs/INVESTIGATIVE_STRATEGY.md` — How we treat evidence, consensus, burden of proof; objective-from-scratch; predictive programming as data
- `docs/PRINT_GOALS.md` — Page budget, typography, reduction strategy
- `docs/AGENT_INSTRUCTIONS.md` — Content conventions, scripts, investigations workflow
- `docs/OUTSTANDING_QUESTIONS.md` — Contradictions, clarifications, open theories
- `docs/CONCLUSIONS.md` — Synthesized conclusions with confidence levels
- `docs/CONTENT_REDUCTION_TRACKER.md` — Reduction log and word counts
- paradigm-threat-files investigations (e.g. `history/chronology/investigations/index-investigations.md`) — investigation topic indexes
- `.cursor/rules/paradigm-threat-timeline.mdc` — AI instructions
- `.github/copilot-instructions.md` — Copilot instructions
