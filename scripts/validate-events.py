#!/usr/bin/env python3
"""Validate events.json: schema compliance and title matches first header of md_path."""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_PATH = os.path.join(REPO_DIR, "data", "events.json")

def validate_hierarchy(hierarchy, section_ids, event_ids):
    """Validate hierarchy structure. Returns list of error strings."""
    errs = []

    for sec in hierarchy:
        if sec.get("type") != "section":
            errs.append(f"Hierarchy section missing type='section': {sec.get('id', '?')}")
        if section_ids and sec.get("id") and sec["id"] not in section_ids:
            errs.append(f"Hierarchy section id not in sections: {sec.get('id')}")
        if "children" not in sec:
            errs.append(f"Hierarchy section missing children: {sec.get('id')}")
        else:
            errs.extend(_validate_tree_nodes(sec["children"], event_ids, "hierarchy"))
    return errs


def _validate_tree_nodes(nodes, event_ids, path):
    errs = []
    for i, n in enumerate(nodes):
        p = f"{path}[{i}]"
        if n.get("type") not in ("group", "event"):
            errs.append(f"{p}: node type must be 'group' or 'event', got {n.get('type')}")
        if "title" not in n:
            errs.append(f"{p}: node missing title")
        if "children" not in n:
            errs.append(f"{p}: node missing children array")
        else:
            if n.get("type") == "event" and n.get("event"):
                eid = n["event"].get("id")
                if eid and event_ids and eid not in event_ids:
                    errs.append(f"{p}: event id {eid} not in events list")
            errs.extend(_validate_tree_nodes(n["children"], event_ids, f"{p}.children"))
    return errs


def count_hierarchy_nodes(hierarchy):
    n = 0
    for sec in hierarchy:
        n += 1
        n += _count_tree_nodes(sec.get("children", []))
    return n


def _count_tree_nodes(nodes):
    return sum(1 + _count_tree_nodes(n.get("children", [])) for n in nodes)


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

    hierarchy = data.get("hierarchy", [])
    if hierarchy:
        hierarchy_errors = validate_hierarchy(hierarchy, section_ids, {e.get("id") for e in events})
        errors.extend(hierarchy_errors)

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(f"  - {e}\n")
        sys.exit(1)
    msg = f"Validated {len(events)} events"
    if hierarchy:
        total = count_hierarchy_nodes(hierarchy)
        msg += f", {len(hierarchy)} hierarchy sections, {total} nodes"
    print(msg)
    sys.exit(0)

if __name__ == "__main__":
    validate()
