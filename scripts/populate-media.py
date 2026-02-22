#!/usr/bin/env python3
"""Populate the media[] field on every entry in events.json by extracting image references from each entry's markdown file."""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_PATH = os.path.join(REPO_DIR, "data", "events.json")

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def extract_images(md_path):
    """Extract (alt, src) tuples from a markdown file."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return []
    with open(full_path, "r", encoding="utf-8") as f:
        text = f.read()
    return IMAGE_RE.findall(text)


def populate_entry(entry):
    """Add media[] to an entry and recurse into children."""
    md_path = entry.get("md_path", "")
    images = extract_images(md_path)
    if images:
        entry["media"] = [src for _alt, src in images]
    elif "media" in entry:
        del entry["media"]
    for child in entry.get("children", []):
        populate_entry(child)


def count_media(entries):
    """Count total media items recursively."""
    total = 0
    for e in entries:
        total += len(e.get("media", []))
        total += count_media(e.get("children", []))
    return total


def main():
    if not os.path.exists(EVENTS_PATH):
        print(f"Error: {EVENTS_PATH} not found")
        sys.exit(1)

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data.get("entries", []):
        populate_entry(entry)

    with open(EVENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = count_media(data.get("entries", []))
    print(f"Populated media arrays: {total} images across all entries")


if __name__ == "__main__":
    main()
