#!/usr/bin/env python3
"""
Apply link fixes from scripts/link-fix-mapping.json to content/ markdown files.

Usage:
  python scripts/apply-link-fixes.py           # dry run (report only)
  python scripts/apply-link-fixes.py --apply   # actually modify files
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
CONTENT_DIR = os.path.join(REPO_DIR, "content")
MAPPING_PATH = os.path.join(SCRIPT_DIR, "link-fix-mapping.json")

LINK_RE = re.compile(r'(\(/timeline/)(evt-[a-z0-9-]+)(\))')


def main():
    if not os.path.exists(MAPPING_PATH):
        print(f"Error: mapping file not found: {MAPPING_PATH}", file=sys.stderr)
        return 1

    with open(MAPPING_PATH) as f:
        mapping = json.load(f)

    apply = "--apply" in sys.argv
    total_replacements = 0
    files_modified = []

    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO_DIR).replace("\\", "/")
            try:
                text = open(path, encoding="utf-8").read()
            except Exception:
                continue

            def replacer(m):
                prefix, link_id, suffix = m.groups()
                if link_id in mapping:
                    nonlocal total_replacements
                    total_replacements += 1
                    return prefix + mapping[link_id] + suffix
                return m.group(0)

            new_text = LINK_RE.sub(replacer, text)
            if new_text != text:
                files_modified.append((rel, path, text, new_text))

    if not files_modified:
        print("No links needed fixing.")
        return 0

    print(f"Would fix {total_replacements} links across {len(files_modified)} files.")
    for rel, _path, _old, _new in files_modified:
        print(f"  - {rel}")

    if apply:
        for _rel, path, _old, new_text in files_modified:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
        print(f"\nApplied fixes to {len(files_modified)} files.")
    else:
        print("\nDry run. Use --apply to make changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
