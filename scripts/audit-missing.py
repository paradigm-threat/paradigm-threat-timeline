#!/usr/bin/env python3
"""Audit content/ for markdown files not registered in data/events.json.
Exits with code 1 if any unregistered files are found."""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_PATH = os.path.join(REPO_DIR, "data", "events.json")
CONTENT_DIR = os.path.join(REPO_DIR, "content")


def collect_indexed_paths(nodes):
    """Recursively collect all md_path values from events.json."""
    paths = set()
    for node in nodes:
        if "md_path" in node:
            paths.add(node["md_path"])
        paths |= collect_indexed_paths(node.get("children", []))
    return paths


def main():
    if not os.path.exists(EVENTS_PATH):
        print(f"Error: {EVENTS_PATH} not found")
        sys.exit(1)

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries", [])
    intro = data.get("introArticles", [])
    indexed = collect_indexed_paths(entries) | collect_indexed_paths(intro)

    all_md = sorted(
        "content/" + fname
        for fname in os.listdir(CONTENT_DIR)
        if fname.endswith(".md")
    )

    missing = [p for p in all_md if p not in indexed]

    if missing:
        print(f"Audit failed: {len(missing)} content file(s) not registered in events.json:\n")
        for p in missing:
            print(f"  - {p}")
        print("\nAdd each file to data/events.json before committing.")
        sys.exit(1)

    print(f"Audit passed: all {len(all_md)} content files are registered in events.json")
    sys.exit(0)


if __name__ == "__main__":
    main()
