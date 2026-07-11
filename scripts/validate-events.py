#!/usr/bin/env python3
"""Validate timeline content/: build event graph from content/ and check titles / ids.

Does not read or write data/events.json — Relay content_events indexes content/ on the server.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from build_events_from_content import build_events_data, count_entries  # noqa: E402


def get_first_header(md_path):
    """Extract first # header from markdown file (skip YAML frontmatter)."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return None, f"File not found: {md_path}"
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            in_frontmatter = False
            for line in f:
                stripped = line.strip()
                if stripped == "---":
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue
                if stripped.startswith("# "):
                    return stripped[2:].strip(), None
        return None, "No # header found"
    except Exception as e:
        return None, str(e)


def get_all_h1_h2_headers(md_path):
    """Extract all # and ## headers from markdown file (for multi-section matching)."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return []
    headers = []
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    headers.append(line[2:].strip())
                elif line.startswith("## "):
                    headers.append(line[3:].strip())
    except Exception:
        pass
    return headers


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
        elif title and first_header:
            stripped = re.sub(r"^\d+\s*(?:BCE|CE|AD)\s*[—–-]\s*", "", first_header)
            all_headers = get_all_h1_h2_headers(md_path)
            stripped_headers = [re.sub(r"^\d+\s*(?:BCE|CE|AD)\s*[—–-]\s*", "", h) for h in all_headers]
            title_prefix_match = any(
                h.startswith(title) or title.startswith(h) for h in all_headers + stripped_headers
            )
            if (
                title != first_header
                and title != stripped
                and title not in all_headers
                and title not in stripped_headers
                and not title_prefix_match
            ):
                errors.append(
                    f"{evt_id}: title mismatch\n  title: {repr(title)}\n  first header: {repr(first_header)}"
                )

    for i, child in enumerate(children):
        validate_entry(child, f"{path}.children[{i}]", errors)


def collect_ids(entries):
    """Return list of (id, path) for all entries."""
    result = []

    def visit(nodes, path):
        for i, e in enumerate(nodes):
            evt_id = e.get("id")
            if evt_id:
                result.append((evt_id, f"{path}[{i}]"))
            visit(e.get("children", []), f"{path}[{i}].children")

    visit(entries, "entries")
    return result


def main():
    data, build_errors = build_events_data()
    if build_errors:
        print("Validation failed:\n")
        for e in build_errors:
            print(f"  - {e}\n")
        sys.exit(1)
    assert data is not None

    entries = data.get("entries", [])
    if not entries:
        print("Error: no entries built from content/")
        sys.exit(1)

    errors = []
    id_to_paths = {}
    for evt_id, path in collect_ids(entries):
        id_to_paths.setdefault(evt_id, []).append(path)
    for evt_id, paths in id_to_paths.items():
        if len(paths) > 1:
            errors.append(f"Duplicate id {repr(evt_id)} at: {', '.join(paths)}")

    for i, entry in enumerate(entries):
        validate_entry(entry, f"entries[{i}]", errors)

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(f"  - {e}\n")
        sys.exit(1)

    total = count_entries(entries)
    print(f"Validated {total} entries from content/")
    sys.exit(0)


if __name__ == "__main__":
    main()
