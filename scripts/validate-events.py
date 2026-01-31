#!/usr/bin/env python3
"""Validate events.json: every entry has md_path and file exists; title matches first header."""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_PATH = os.path.join(REPO_DIR, "data", "events.json")


def get_first_header(md_path):
    """Extract first # header from markdown file."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return None, f"File not found: {md_path}"
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip(), None
                if line.startswith("---") and f.tell() < 200:
                    continue
        return None, "No # header found"
    except Exception as e:
        return None, str(e)


def validate_entry(entry, path, errors):
    """Recursively validate entry and children."""
    evt_id = entry.get("id", path)
    title = entry.get("title")
    md_path = entry.get("md_path")
    children = entry.get("children", [])

    if not md_path:
        errors.append(f"{evt_id}: missing md_path")
    else:
        first_header, err = get_first_header(md_path)
        if err:
            errors.append(f"{evt_id}: {err}")
        elif title and first_header and title != first_header:
            errors.append(
                f"{evt_id}: title mismatch\n  title: {repr(title)}\n  first header: {repr(first_header)}"
            )

    for i, child in enumerate(children):
        validate_entry(child, f"{path}.children[{i}]", errors)


def count_entries(entries):
    return sum(1 + count_entries(e.get("children", [])) for e in entries)


def main():
    if not os.path.exists(EVENTS_PATH):
        print(f"Error: {EVENTS_PATH} not found")
        sys.exit(1)

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries", [])
    if not entries:
        print("Error: no entries in events.json")
        sys.exit(1)

    errors = []
    for i, entry in enumerate(entries):
        validate_entry(entry, f"entries[{i}]", errors)

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(f"  - {e}\n")
        sys.exit(1)

    total = count_entries(entries)
    print(f"Validated {total} entries")
    sys.exit(0)


if __name__ == "__main__":
    main()
