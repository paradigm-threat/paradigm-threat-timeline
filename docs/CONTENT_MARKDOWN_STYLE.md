# Markdown prose style — `content/` only

This document applies **only** to Markdown files under `content/` in paradigm-threat-timeline (the book-facing timeline source). It does **not** govern paradigm-threat-files, investigations, blog, or site copy unless those repos adopt the same rule explicitly.

## Emphasis (`**bold**` and `*italic*`)

Use emphasis **sparingly** to highlight a point the reader should retain—not to decorate every proper noun or clause.

- **Target:** about **one to four** emphasized spans per paragraph on average (combined bold + italic used as emphasis, not counting titles of works set in italics by convention).
- **Prefer meaning over habit:** if the sentence already carries the stress (syntax, contrast words), leave it unstyled.
- **Book and story titles:** keep using *italics* for titles of works (standard typography). That does not count toward the “1–4 emphasis” budget if it is title styling, not rhetorical stress.
- **Avoid:** bolding most words in a sentence, bolding every list item lead-in, or using bold where a `##` / `###` heading would do.

**Bold** suits a short factual hook or contrast (*heat ray*, *no surviving original*). *Italic* suits foreign terms, titles, or a lighter stress on a phrase. Mixing both in one paragraph is fine if the total stays in the intended range.

## Headings

Hierarchy is structural (`#` … `####`). Do not compensate for reduced inline bold by stacking extra heading levels.

## Cross-links

- **Timeline events:** root-relative `/timeline/evt-...` (and browser deep-links as in `CONTENT_STRATEGY.md`).
- **paradigm-threat-files on the live site:** `https://paradigmthreat.net` exposes the **full** paradigm-threat-files tree at the **URL root** (repo path = URL path). Link investigations and other repo files with root-relative paths, e.g. `/governance/war/investigations/example.md` → `https://paradigmthreat.net/governance/war/investigations/example.md`. See `docs/LINKING_AND_SITE_PATHS.md` in paradigm-threat-files for the canonical note.
- **Do not link to `https://github.com/clevertree/...`:** that GitHub account is gone; those URLs 404. Prefer root-relative or `https://paradigmthreat.net/...` for reader-facing links. Full policy, replacements, and a file inventory: **paradigm-threat-files** `docs/LINKING_AND_SITE_PATHS.md` (section *Do not use the old github.com/clevertree URLs*).

Emphasis rules do not apply inside link text in ways that hurt readability—prefer plain link labels when the surrounding prose already stresses the point.

## Keywords line (end of article)

Many chapter files end with a single metadata line:

```markdown
Keywords: #topic #another #example
```

Use **Instagram-safe** tokens: **letters, numbers, and underscores** only inside each `#` tag. Do **not** use **hyphens** inside a tag (Instagram treats the hyphen as ending the hashtag). Prefer `#jadehelm`, `#2016primary`, or separate tags (`#deep` `#state`) rather than `#jade-helm` or `#2016-primary`.

This matches the same `Keywords:` convention in **paradigm-threat-files** (investigations, blog-adjacent notes, etc.).
