#!/usr/bin/env python3
"""
Rename chapter root files (XX.00.00-YYYY-ce-*.md) to XX.00.00-*.md without the year prefix.

Preserves stable timeline URLs by writing frontmatter:
  id: evt-<old-slug>

Requires: build-events-from-content.py to support frontmatter `id` (already added).

Run:  python3 scripts/rename-chapter-root-filenames.py
Then: npm run build-events && npm run generate-index
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "content"

# Strip one leading calendar year token from slug: 1400-ce-, 4077-bce-, 670-bce-
STRIP_YEAR_PREFIX = re.compile(r"^\d{1,4}-(?:ce|bce)-", re.I)

FILENAME_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})-(.+)\.md$")


def load_build_events():
    spec = importlib.util.spec_from_file_location(
        "bec", REPO / "scripts" / "build-events-from-content.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines(keepends=True)
    if not lines[0].strip() == "---":
        return None, text
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            fm_raw = "".join(lines[1:i])
            body = "".join(lines[i + 1 :])
            try:
                data = yaml.safe_load(fm_raw)
            except yaml.YAMLError:
                return None, text
            return (data if isinstance(data, dict) else {}), body
        i += 1
    return None, text


def merge_frontmatter(old_slug: str, existing: dict | None, dates_from_slug: list | None) -> dict:
    stable_id = f"evt-{old_slug}"
    fm: dict = dict(existing) if existing else {}
    fm["id"] = stable_id
    if not fm.get("dates") and dates_from_slug:
        d0 = dates_from_slug[0]
        start = d0.get("start")
        end = d0.get("end", start)
        cal = d0.get("calendar", "CE")
        if start is not None:
            fm["dates"] = [{"start": start, "end": end, "calendar": cal}]
    return fm


def dump_frontmatter(fm: dict) -> str:
    return "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).rstrip() + "\n---\n"


def main() -> int:
    bec = load_build_events()
    extract_dates_from_slug = bec.extract_dates_from_slug

    renames: list[tuple[Path, Path, str, str]] = []
    for path in sorted(CONTENT.rglob("*.md")):
        m = FILENAME_RE.match(path.name)
        if not m:
            continue
        xx, yy, zz, slug = m.group(1), m.group(2), m.group(3), m.group(4)
        if yy != "00" or zz != "00":
            continue
        if not STRIP_YEAR_PREFIX.match(slug):
            continue
        new_slug = STRIP_YEAR_PREFIX.sub("", slug, count=1)
        if not new_slug or new_slug == slug:
            continue
        new_name = f"{xx}.{yy}.{zz}-{new_slug}.md"
        new_path = path.parent / new_name
        renames.append((path, new_path, slug, new_slug))

    for old_path, new_path, old_slug, new_slug in renames:
        if new_path.exists():
            print(f"Skip (target exists): {new_path}", file=sys.stderr)
            continue
        text = old_path.read_text(encoding="utf-8")
        dates_from_slug, date_err = extract_dates_from_slug(old_slug)
        if date_err:
            print(f"Error extracting dates from {old_slug}: {date_err}", file=sys.stderr)
            return 1

        fm_existing, body = split_frontmatter(text)
        fm = merge_frontmatter(old_slug, fm_existing, dates_from_slug)
        new_text = dump_frontmatter(fm) + body

        new_path.write_text(new_text, encoding="utf-8")
        old_path.unlink()
        print(f"{old_path.relative_to(REPO)} -> {new_path.relative_to(REPO)}")

    print(f"Renamed {len(renames)} chapter roots.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
