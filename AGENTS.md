# Agent instructions

Single entry point for assistants working in this repo. **Deep dives stay in linked docs.**

---

## Git and go-live

Catalog repo **`paradigm-threat-timeline`** · branch **`main`** · publish origin **`iad1`**.

| Step | Action |
|------|--------|
| 1 | Checkout **`main`**. |
| 2 | **`git push iad1 HEAD:main`** first — server waits for mesh; **push failure = publish failed**. |
| 3 | **`git push gitlab HEAD:main`** after iad1 succeeds. |

After editing **`content/`**: run **`npm run validate-events`** (pre-commit runs it). Push refreshes Relay QUERY indexes.

---

## What to read for each task

| Task | Document |
|------|----------|
| Timeline maintenance (numbering, events, scripts) | [`docs/AGENT_INSTRUCTIONS.md`](docs/AGENT_INSTRUCTIONS.md) |
| Investigative / epistemic stance | [`docs/INVESTIGATIVE_STRATEGY.md`](docs/INVESTIGATIVE_STRATEGY.md) |
| Writing style, TL;DR, pacing | [`docs/CONTENT_STRATEGY.md`](docs/CONTENT_STRATEGY.md) |
| Prose emphasis in `content/` | [`docs/CONTENT_MARKDOWN_STYLE.md`](docs/CONTENT_MARKDOWN_STYLE.md) |
| Print budget / brevity | [`docs/PRINT_GOALS.md`](docs/PRINT_GOALS.md) |
| Book editions | [`docs/BOOK_EDITIONS_PLAN.md`](docs/BOOK_EDITIONS_PLAN.md) |
| Open questions / contradictions | [`docs/OUTSTANDING_QUESTIONS.md`](docs/OUTSTANDING_QUESTIONS.md) |
| Speculative conclusions | [`docs/CONCLUSIONS.md`](docs/CONCLUSIONS.md) |
| Investigations (separate repo) | [`../paradigm-threat-files/docs/INVESTIGATIONS.md`](../paradigm-threat-files/docs/INVESTIGATIONS.md) |
| Æther vocabulary | [`../paradigm-threat-files/docs/LLM_AETHER_VOCABULARY_MAXWELL_DEBATE.md`](../paradigm-threat-files/docs/LLM_AETHER_VOCABULARY_MAXWELL_DEBATE.md) |
| Blog entries | [`../paradigm-threat-files/docs/BLOG.md`](../paradigm-threat-files/docs/BLOG.md) |

**Hard rules:** Timeline repo does **not** host investigations — link to **paradigm-threat-files** with root-relative paths (`/history/…`). Never implement **CONTENT_STRATEGY** recommendations without user approval.

*Last updated: 2026-08-23*
