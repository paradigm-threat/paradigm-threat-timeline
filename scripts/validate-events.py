#!/usr/bin/env python3
"""Validate events.json: schema compliance and title matches first header of md_path."""
import json
import os
import re
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
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip(), None
                # Skip YAML frontmatter
                if line.startswith('---') and f.tell() < 200:
                    continue
        return None, "No # header found"
    except Exception as e:
        return None, str(e)

def validate():
    if not os.path.exists(EVENTS_PATH):
        print(f"Error: {EVENTS_PATH} not found")
        sys.exit(1)

    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    events = data.get("events", data) if isinstance(data, dict) else data
    if not isinstance(events, list):
        events = [data]
    sections = data.get("sections", []) if isinstance(data, dict) else []
    section_ids = {s["id"] for s in sections if isinstance(s, dict)}

    errors = []
    for i, evt in enumerate(events):
        evt_id = evt.get("id", f"#{i}")
        title = evt.get("title")
        md_path = evt.get("md_path")

        if not md_path:
            errors.append(f"{evt_id}: missing md_path")
            continue

        first_header, err = get_first_header(md_path)
        if err:
            errors.append(f"{evt_id}: {err}")
            continue

        if title and title != first_header:
            errors.append(f"{evt_id}: title mismatch\n  title: {repr(title)}\n  first header: {repr(first_header)}")
        if section_ids and evt.get("section") and evt["section"] not in section_ids:
            errors.append(f"{evt_id}: invalid section {repr(evt['section'])}")

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(f"  - {e}\n")
        sys.exit(1)
    print(f"Validated {len(events)} events")
    sys.exit(0)

if __name__ == "__main__":
    validate()
