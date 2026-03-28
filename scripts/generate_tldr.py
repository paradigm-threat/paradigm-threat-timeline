#!/usr/bin/env python3
"""
Insert placeholder TL;DR blockquotes into long markdown files.
Each inserted line is: > **TL;DR:** TODO
(models replace TODO with a one-paragraph lay summary when ready).

See docs/CONTENT_STRATEGY.md § TL;DR.

Usage:
  python3 scripts/generate_tldr.py --dry-run
  python3 scripts/generate_tldr.py
  python3 scripts/generate_tldr.py --root /path/to/paradigm-threat-files
  python3 scripts/generate_tldr.py --refresh-tldr   # rewrite existing TL;DR lines back to TODO
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

THRESHOLD = 12
FRONTMATTER_END = re.compile(r"^---\s*$", re.M)
TLDR_LINE = "> **TL;DR:** TODO"
TLDR_BLOCK = f"\n{TLDR_LINE}\n\n"


def strip_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    m = FRONTMATTER_END.search(text, 3)
    if not m:
        return None, text
    end = m.end()
    rest = text[end:].lstrip("\n")
    return text[:end], rest


def count_paragraph_blocks(body: str) -> int:
    body = body.replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n+", body.strip())
    n = 0
    for b in blocks:
        b = b.strip()
        if not b or re.fullmatch(r"-{3,}\s*", b):
            continue
        n += 1
    return n


def has_tldr(text: str) -> bool:
    return bool(re.search(r">\s*\*\*TL;DR:\*\*", text, re.I))


def find_insertion_point(full_text: str, body: str, fm: str | None) -> int:
    search_from = len(fm) if fm else 0
    slice_ = full_text[search_from:]
    m = re.search(r"^#\s+[^\n]+\n", slice_, re.M)
    if not m:
        pos = search_from
    else:
        pos = search_from + m.end()
    rest = full_text[pos:]
    while True:
        ws = re.match(r"(\n*)", rest)
        if not ws:
            break
        pos += ws.end()
        rest = full_text[pos:]
        img = re.match(r"!\[[^\]]*\]\([^)]*\)\s*\n?", rest)
        if img:
            pos += img.end()
            rest = full_text[pos:]
            continue
        break
    return pos


def strip_first_tldr_block(text: str) -> str:
    return re.sub(
        r"(^|\n)> \*\*TL;DR:\*\*[^\n]*\n+",
        lambda m: m.group(1) or "",
        text,
        count=1,
    )


def process_file(path: Path, root: Path, dry_run: bool, refresh_tldr: bool) -> str:
    if "blog" in path.parts or "docs" in path.parts:
        return "skip_blog_or_docs"
    try:
        rel = path.relative_to(root.resolve())
        if len(rel.parts) == 1 and rel.name in (
            "REORGANIZATION_MAP.md",
            "README.md",
        ):
            return "skip_repo_meta"
    except ValueError:
        pass

    text = path.read_text(encoding="utf-8", errors="replace")
    if has_tldr(text):
        if not refresh_tldr:
            return "skip_has_tldr"
        text = strip_first_tldr_block(text)
        if has_tldr(text):
            return "skip_has_tldr"

    fm, body = strip_frontmatter(text)
    if count_paragraph_blocks(body) <= THRESHOLD:
        return "skip_short"

    ins = find_insertion_point(text, body, fm)
    new_text = text[:ins] + TLDR_BLOCK + text[ins:]
    if dry_run:
        return "would_write"
    path.write_text(new_text, encoding="utf-8")
    return "wrote"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "content",
        help="Root directory to scan (default: timeline content/)",
    )
    ap.add_argument(
        "--refresh-tldr",
        action="store_true",
        help="Remove existing TL;DR line and insert fresh TODO placeholder.",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root: Path = args.root
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    stats: dict[str, int] = {}
    for path in sorted(root.rglob("*.md")):
        if "node_modules" in path.parts or ".venv" in path.parts:
            continue
        r = process_file(path, root, args.dry_run, args.refresh_tldr)
        stats[r] = stats.get(r, 0) + 1

    for k in sorted(stats, key=lambda x: -stats[x]):
        print(f"{k}: {stats[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
