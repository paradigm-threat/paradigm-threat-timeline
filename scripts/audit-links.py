#!/usr/bin/env python3
"""DEPRECATED: catalog JSON is gone. Prefer content/ + validate-events / Relay QUERY.

Audit /timeline/evt-xxx links in content against events.json. Report broken links and output fix mapping."""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")
CONTENT_DIR = os.path.join(REPO_DIR, "content")

LINK_RE = re.compile(r'\]\(/timeline/(evt-[a-z0-9-]+)\)')


def collect_ids(nodes, acc=None):
    acc = acc or []
    for n in nodes:
        if "id" in n:
            acc.append(n["id"])
        collect_ids(n.get("children", []), acc)
    return acc


def main():
    with open(EVENTS_JSON) as f:
        data = json.load(f)
    valid_ids = set(collect_ids(data.get("entries", [])))

    broken = []  # (file, link, suggested_fix)
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
            for m in LINK_RE.finditer(text):
                link_id = m.group(1)
                if link_id not in valid_ids:
                    # Find closest match (id that contains or is contained in link_id)
                    candidates = [vid for vid in valid_ids if link_id in vid or vid in link_id]
                    suggested = candidates[0] if len(candidates) == 1 else (candidates[:3] if candidates else None)
                    broken.append((rel, link_id, suggested))

    if not broken:
        print("All timeline links valid.")
        return 0

    # Build fix mapping: broken_id -> correct_id (only when unambiguous)
    fix_map = {}
    for _rel, link_id, suggested in broken:
        if suggested and isinstance(suggested, str):
            fix_map[link_id] = suggested
        elif suggested and isinstance(suggested, list) and len(suggested) == 1:
            fix_map[link_id] = suggested[0]

    # Output fix mapping JSON to stdout for apply-fix script
    if "--json" in sys.argv:
        json.dump(fix_map, sys.stdout, indent=2)
        return 0

    print("Broken timeline links:\n", file=sys.stderr)
    for rel, link_id, suggested in broken:
        sug = f"  → suggested: {suggested}" if suggested else ""
        print(f"  {rel}: {link_id}{sug}", file=sys.stderr)
    print(f"\nTotal: {len(broken)} broken links", file=sys.stderr)
    print(f"Unambiguous fix mapping: {len(fix_map)} links", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
