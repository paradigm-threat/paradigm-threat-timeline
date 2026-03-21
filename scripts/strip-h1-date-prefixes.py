#!/usr/bin/env python3
"""
Strip leading Scaliger-style year prefixes from the first # H1 in each content .md file.

Transforms e.g.  # 1400 CE — 15th Century ...  ->  # 15th Century ...
Dates remain in events.json via filename + YAML dates[]; titles are display-only.

Run from repo root:  python3 scripts/strip-h1-date-prefixes.py
Then:                 npm run build-events && npm run validate-events
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "content"

# One leading segment: YYYY CE, YYYY–YYYY CE, YYYY– CE, YYYY BCE, YYYY–YYYY BCE, then — : or –
H1_DATE_PREFIX = re.compile(
    r"^(#\s*)"
    r"(?:\d{1,4}(?:[–-]\d{1,4})?\s*(?:CE|BCE)|\d{1,4}\s*[–-]\s*(?:CE|BCE))"
    r"\s*[—–:]\s*",
    re.UNICODE,
)


def strip_h1_date_prefixes(line: str, max_passes: int = 8) -> str:
    """Remove one or more leading `1234 CE — ` style segments from an H1 line."""
    out = line
    for _ in range(max_passes):
        m = H1_DATE_PREFIX.match(out)
        if not m:
            break
        out = m.group(1) + out[m.end() :]
    return out


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    i = 0
    # Skip YAML frontmatter
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        if i < len(lines) and lines[i].strip() == "---":
            i += 1
    changed = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("# " * 2):  # single # only
            new_line = strip_h1_date_prefixes(line)
            if new_line != line:
                lines[i] = new_line
                changed = True
            break
        i += 1
    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def main() -> int:
    if not CONTENT.is_dir():
        print(f"Missing {CONTENT}", file=sys.stderr)
        return 1
    n = 0
    for md in sorted(CONTENT.rglob("*.md")):
        if process_file(md):
            print(md.relative_to(REPO))
            n += 1
    print(f"Updated {n} files.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
