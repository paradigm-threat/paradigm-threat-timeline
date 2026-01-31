#!/usr/bin/env python3
"""
Build recursive hierarchy from source markdown header structure.
Parses #, ##, ###, #### from chronology/mudflood/mars. Matches to events.
Outputs per-section trees for CustomTimelineView.
"""
import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

SOURCE_FILES = [
    ("history/chronology", "history/chronology/page.md"),
    ("history/mudflood", "history/mudflood/page.md"),
    ("cosmos/mars", "cosmos/mars/page.md"),
]

SECTIONS = [
    {"id": "before-creation", "name": "Before Creation", "era": "BCE", "start": -5000, "end": -4078},
    {"id": "golden-age", "name": "The Golden Age", "era": "BCE", "start": -4077, "end": -3148},
    {"id": "dark-ages", "name": "The Dark Ages", "era": "BCE", "start": -3147, "end": -687},
    {"id": "iron-age-blip", "name": "Iron Age / The Blip", "era": "BCE", "start": -686, "end": -1},
    {"id": "11th-century", "name": "11th Century C.E.", "era": "CE", "start": 1000, "end": 1099},
    {"id": "12th-century", "name": "12th Century C.E.", "era": "CE", "start": 1100, "end": 1199},
    {"id": "13th-century", "name": "13th Century C.E.", "era": "CE", "start": 1200, "end": 1299},
    {"id": "14th-century", "name": "14th Century C.E.", "era": "CE", "start": 1300, "end": 1399},
    {"id": "15th-century", "name": "15th Century C.E.", "era": "CE", "start": 1400, "end": 1499},
    {"id": "16th-century", "name": "16th Century C.E.", "era": "CE", "start": 1500, "end": 1599},
    {"id": "17th-century", "name": "17th Century C.E.", "era": "CE", "start": 1600, "end": 1699},
    {"id": "18th-century", "name": "18th Century C.E.", "era": "CE", "start": 1700, "end": 1799},
    {"id": "19th-century", "name": "19th Century C.E.", "era": "CE", "start": 1800, "end": 1999},
]


def section_for_year(year):
    """Return section id for a given year."""
    for s in SECTIONS:
        if s["era"] == "BCE" and year < 0:
            if s["start"] <= year <= s["end"]:
                return s["id"]
        elif s["era"] == "CE" and year >= 0:
            if s["start"] <= year <= s["end"]:
                return s["id"]
    return SECTIONS[0]["id"]


def parse_headers(content):
    """Return list of (level, title) in document order."""
    result = []
    for m in re.finditer(r"^(#{1,4})\s+(.+)$", content, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        result.append((level, title))
    return result


def build_tree(headers, event_by_title):
    """
    Build tree from headers. Parent = last prior header with lower level.
    Returns list of root nodes (each with 'children').
    """
    roots = []
    stack = []  # (level, node)

    for level, title in headers:
        evt = event_by_title.get(title)
        if evt is not None:
            node = {"type": "event", "title": title, "level": level, "event": evt, "children": []}
        else:
            node = {"type": "group", "title": title, "level": level, "children": []}

        while stack and stack[-1][0] >= level:
            stack.pop()

        if not stack:
            roots.append(node)
        else:
            parent = stack[-1][1]
            parent["children"].append(node)

        stack.append((level, node))

    return roots


def assign_section(node):
    """Assign section to node. Events use event.section; groups inherit from first descendant."""
    if node["type"] == "event":
        evt = node.get("event", {})
        sec = evt.get("section")
        if not sec:
            dates = evt.get("dates") or []
            if dates:
                year = dates[0].get("start", dates[0].get("value"))
                sec = section_for_year(year) if year is not None else None
            sec = sec or SECTIONS[0]["id"]
        node["section"] = sec
        for child in node.get("children", []):
            assign_section(child)
        return sec

    sec = None
    for child in node.get("children", []):
        csec = assign_section(child)
        if csec and sec is None:
            sec = csec
    node["section"] = sec if sec else SECTIONS[0]["id"]
    return node["section"]


def filter_subtree_by_section(node, section_id):
    """Return a copy of node with only children whose section matches. For JSON output."""
    sec = node.get("section")
    if sec != section_id:
        return None
    out = {k: v for k, v in node.items() if k != "children"}
    out["children"] = []
    for c in node.get("children", []):
        sub = filter_subtree_by_section(c, section_id)
        if sub is not None:
            out["children"].append(sub)
    return out


def extract_roots_for_section(roots, section_id):
    """
    From tree roots, extract nodes that belong to section_id and are roots
    (parent has different section or is null). Return filtered subtrees.
    """
    result = []

    def visit(nodes, parent_sec=None):
        for n in nodes:
            sec = n.get("section")
            if sec == section_id:
                if parent_sec != section_id:
                    filtered = filter_subtree_by_section(n, section_id)
                    if filtered is not None:
                        result.append(filtered)
                visit(n.get("children", []), section_id)
            else:
                visit(n.get("children", []), parent_sec)

    visit(roots)
    return result


def build_hierarchy(roots):
    """Build per-section hierarchy. Each section gets a block with its roots."""
    hierarchy = []
    for sec in SECTIONS:
        sid = sec["id"]
        children = extract_roots_for_section(roots, sid)
        if children:
            hierarchy.append({"type": "section", "id": sid, "name": sec["name"], "children": children})
    return hierarchy


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source-dir",
        default=os.path.join(os.path.dirname(REPO_DIR), "paradigm-threat-files"),
        help="Path to paradigm-threat-files",
    )
    args = ap.parse_args()
    source_base = os.path.abspath(args.source_dir)

    with open(EVENTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = data.get("events", [])
    event_by_title = {e["title"]: e for e in events}

    all_headers = []
    for _prefix, rel_path in SOURCE_FILES:
        filepath = os.path.join(source_base, rel_path)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        headers = parse_headers(content)
        all_headers.extend(headers)

    roots = build_tree(all_headers, event_by_title)
    for r in roots:
        assign_section(r)

    hierarchy = build_hierarchy(roots)

    data["hierarchy"] = hierarchy
    data["meta"] = data.get("meta", {})
    data["meta"]["hierarchy_source"] = "build-hierarchy.py"

    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    def count_nodes(nodes):
        return sum(1 + count_nodes(n.get("children", [])) for n in nodes)

    total = sum(count_nodes(h["children"]) for h in hierarchy)
    print(f"Built hierarchy: {len(hierarchy)} sections, {total} nodes")


if __name__ == "__main__":
    main()
