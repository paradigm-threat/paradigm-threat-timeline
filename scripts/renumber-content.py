#!/usr/bin/env python3
"""
Renumber content files from XX.YYY-slug.md to XX.XX.XX-slug.md format.

Mapping rule: XX.YYY -> XX.YY.ZZ
  where YY = (YYY // 10) zero-padded to 2 digits
        ZZ = (YYY %  10) zero-padded to 2 digits

Example: 02.050 -> 02.05.00
         09.005 -> 09.00.05
         10.085 -> 10.08.05
         01.000 -> 01.00.00  (section headers)

Updates:
  1. Renames all content/*.md files
  2. Rewrites data/events.json (md_path fields)
  3. Rewrites internal cross-links in content/*.md files
     (bare, ./-prefixed, and /content/-prefixed styles)
"""

import json
import os
import re
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_DIR, "content")
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

# ── Regex: matches the numeric prefix at the start of a content filename ──────
# Captures: (XX)(YYY)(slug_with_dash_and_rest)
# e.g.  "02.050-proto-saturn..."  -> ("02", "050", "-proto-saturn...")
PREFIX_RE = re.compile(r"^(\d{2})\.(\d{3})(-.*\.md)$")

# Regex to find any reference to a content file by its old numeric prefix inside
# markdown text.  We search for the pattern \d{2}\.\d{3} followed by a dash.
# We'll rebuild the map of old_prefix -> new_prefix and do a text substitution.
LINK_PREFIX_RE = re.compile(r"(\d{2})\.(\d{3})(-[^)\s\"']+\.md)")


def new_prefix(xx: str, yyy: str) -> str:
    n = int(yyy)
    yy = n // 10
    zz = n % 10
    return f"{xx}.{yy:02d}.{zz:02d}"


def build_rename_map() -> dict[str, str]:
    """Return {old_basename: new_basename} for every file in content/."""
    rename = {}
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if not fname.endswith(".md"):
            continue
        m = PREFIX_RE.match(fname)
        if not m:
            print(f"  [SKIP] Filename does not match XX.YYY pattern: {fname}")
            continue
        xx, yyy, rest = m.groups()
        old_prefix = f"{xx}.{yyy}"
        np = new_prefix(xx, yyy)
        new_name = f"{np}{rest}"
        if old_prefix != np:
            rename[fname] = new_name
        else:
            # Already in new format (shouldn't happen on initial run)
            rename[fname] = fname
    return rename


def step1_rename_files(rename_map: dict[str, str]) -> None:
    print("\n── Step 1: Renaming content files ──────────────────────────")
    changed = 0
    for old, new in sorted(rename_map.items()):
        if old == new:
            print(f"  [SAME] {old}")
            continue
        src = os.path.join(CONTENT_DIR, old)
        dst = os.path.join(CONTENT_DIR, new)
        if os.path.exists(dst):
            print(f"  [WARN] Target already exists, skipping: {new}")
            continue
        os.rename(src, dst)
        print(f"  [RENAME] {old}  →  {new}")
        changed += 1
    print(f"\n  {changed} files renamed.")


def step2_update_events_json(rename_map: dict[str, str]) -> None:
    print("\n── Step 2: Updating data/events.json ───────────────────────")
    with open(EVENTS_JSON, "r", encoding="utf-8") as f:
        raw = f.read()

    updated = raw
    changes = 0
    for old, new in rename_map.items():
        if old == new:
            continue
        old_path = f"content/{old}"
        new_path = f"content/{new}"
        if old_path in updated:
            updated = updated.replace(old_path, new_path)
            changes += 1
            print(f"  [JSON] {old_path}  →  {new_path}")
        else:
            print(f"  [WARN] Not found in events.json: {old_path}")

    if updated != raw:
        with open(EVENTS_JSON, "w", encoding="utf-8") as f:
            f.write(updated)
    print(f"\n  {changes} md_path values updated.")


def step3_update_crosslinks(rename_map: dict[str, str]) -> None:
    """Rewrite internal links in all content .md files."""
    print("\n── Step 3: Updating cross-links in content/*.md ────────────")

    # Build prefix-only substitution map: "02.050" -> "02.05.00"
    prefix_map: dict[str, str] = {}
    for old, new in rename_map.items():
        m_old = re.match(r"^(\d{2}\.\d{3})", old)
        m_new = re.match(r"^(\d{2}\.\d{2}\.\d{2})", new)
        if m_old and m_new:
            prefix_map[m_old.group(1)] = m_new.group(1)

    total_files = 0
    total_links = 0

    for fname in sorted(os.listdir(CONTENT_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(CONTENT_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        def replace_link(m: re.Match) -> str:
            xx, yyy, rest = m.groups()
            old_p = f"{xx}.{yyy}"
            new_p = prefix_map.get(old_p)
            if new_p:
                return f"{new_p}{rest}"
            return m.group(0)  # unchanged (already new format or unknown)

        new_text = LINK_PREFIX_RE.sub(replace_link, text)
        if new_text != text:
            link_count = len(LINK_PREFIX_RE.findall(text))
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"  [LINKS] {fname}  ({link_count} link(s) updated)")
            total_files += 1
            total_links += link_count

    print(f"\n  {total_links} link(s) in {total_files} file(s) updated.")


def step4_warn_broken_links() -> None:
    """Warn about links in content files that point to non-existent files."""
    print("\n── Step 4: Checking for broken links ───────────────────────")
    existing = set(os.listdir(CONTENT_DIR))
    broken = []
    for fname in sorted(existing):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(CONTENT_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
        # Find all links ending in .md (bare, ./, /content/)
        for m in re.finditer(r"(?:\.\/|\/content\/)?(\d{2}\.\d{2}\.\d{2}-[^)\s\"']+\.md)", text):
            target = m.group(1)
            if target not in existing:
                broken.append((fname, target))

    if broken:
        print(f"  [WARN] {len(broken)} broken link(s) found:")
        for src, tgt in broken:
            print(f"    {src}  ->  {tgt}  (target not found)")
    else:
        print("  No broken links found.")


def main() -> None:
    print("=== paradigm-threat-timeline: Content Renumber XX.YYY → XX.XX.XX ===")
    rename_map = build_rename_map()
    print(f"\nBuilt rename map: {len(rename_map)} files ({sum(1 for o,n in rename_map.items() if o!=n)} to rename)")

    step1_rename_files(rename_map)
    step2_update_events_json(rename_map)
    step3_update_crosslinks(rename_map)
    step4_warn_broken_links()

    print("\n=== Done. Run post-edit scripts: ===")
    print("  npm run normalize-events")
    print("  npm run refactor-sections")
    print("  npm run validate-events")
    print("  npm run generate-index")


if __name__ == "__main__":
    main()
