#!/usr/bin/env python3
"""
Build consolidated entries from chronology page. One recursive array of entries.
Every entry has id, title, md_path (required), dates, children.
Extracts section content from chronology and writes to dated md files.
"""
import json
import os
import re
import shutil
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_DIR = os.path.join(REPO_DIR, "events")
ARTICLES_DIR = os.path.join(REPO_DIR, "articles")
DATA_DIR = os.path.join(REPO_DIR, "data")
EVENTS_JSON = os.path.join(DATA_DIR, "events.json")
FILES_BASE_URL = "https://clevertree.github.io/paradigm-threat-files"
CHRONOLOGY_BASE = "history/chronology"

SOURCE_FILE = os.path.join(
    os.path.dirname(REPO_DIR), "paradigm-threat-files", "history", "chronology", "page.md"
)

# Section headers (level 2) that are type "event" with date ranges (not articles)
SECTIONS_AS_EVENTS = frozenset({
    "Before Creation", "The Golden Age", "The Dark Ages",
    "The Blip: 7th Century B.C.E. to 10th Century C.E. Never Occurred",
    "11th Century C.E. Common Era Begins", "12th Century C.E. Birth of Christianity",
    "13th Century C.E.: The Russian Horde 'Tartarian' Empire emerges",
    "14th Century C.E.: Great Expansion of the Mongol / Slavic Rus-Horde Empire",
    "15th Century C.E. Ottoman Conquest of Europe.",
    "16th Century C.E. Reformation and Inquisition.",
    "17th Century-Romanovs Rise to power", "18th Century C.E. MudFlood and Pugachev",
    "19th Century C.E.", "TODO: Finish 17th century timeline",
    "Building the New Chronology",
})

# Era name -> (start, end) for date inference when header has no explicit date
ERA_RANGES = {
    "Earth History Timeline Reconstruction": (-4077, -3148),
    "Saturnian Cosmology Timeline Video": (-4077, -3148),
    "Project Objective": (-4077, -3148),
    "Before Creation": (-5000, -4078),
    "The Golden Age": (-4077, -3148),
    "The Dark Ages": (-3147, -687),
    "The Blip: 7th Century B.C.E. to 10th Century C.E. Never Occurred": (-686, 999),
    "11th Century C.E. Common Era Begins": (1000, 1099),
    "12th Century C.E. Birth of Christianity": (1100, 1199),
    "13th Century C.E.: The Russian Horde 'Tartarian' Empire emerges": (1200, 1299),
    "14th Century C.E.: Great Expansion of the Mongol / Slavic Rus-Horde Empire": (1300, 1399),
    "15th Century C.E. Ottoman Conquest of Europe.": (1400, 1499),
    "16th Century C.E. Reformation and Inquisition.": (1500, 1599),
    "17th Century-Romanovs Rise to power": (1600, 1699),
    "18th Century C.E. MudFlood and Pugachev": (1700, 1799),
    "19th Century C.E.": (1800, 1999),
    "TODO: Finish 17th century timeline": (1600, 1699),
    "C.E. 1773 to 1775 - The Rebellion of Pugachev": (1773, 1775),
    "C.E. 1774-1814 The MudFlood and World Cataclysm": (1774, 1814),
    "C.E. 1803 to 1815 - Napoleonic Wars": (1803, 1815),
    "C.E. 1812 - Napoleon invades Russia": (1812, 1812),
}

INTRO_TITLE = "Introduction"
INTRO_ID = "evt-intro"
FIRST_SECTION_TITLE = "Earth History Timeline Reconstruction"


def slugify(text):
    """Create URL-safe slug from title. Strip date-like prefixes."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"^\d{3,4}\s*(?:to\s+\d{3,4}\s+)?(?:B\.?C\.?E\.?|A\.?D\.?|C\.?E\.?\.?)\s*[-–]?\s*", "", text, flags=re.I)
    text = re.sub(r"^C\.?E\.?\s*\d{3,4}(?:\s+to\s+\d{3,4})?\s*[-–]?\s*", "", text, flags=re.I)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:80] or "untitled"


def strip_date_prefix(title):
    """Remove leading date from title (e.g. '4077 B.C.E. Foo' -> 'Foo')."""
    t = re.sub(r"^\d{3,4}\s+to\s+\d{3,4}\s*(?:B\.?C\.?E\.?|BC)?\s*[-–—]?\s*", "", title, flags=re.I)
    t = re.sub(r"^\d{3,4}\s*(?:B\.?C\.?E\.?|BC)\s*[-–—]?\s*", "", t, flags=re.I)
    t = re.sub(r"^C\.?E\.?\s*\d{3,4}(?:\s+to\s+|\s*[-–—]\s*)\d{3,4}\s*[-–—]?\s*", "", t, flags=re.I)
    t = re.sub(r"^C\.?E\.?\s*\d{3,4}\s*[-–—]?\s*", "", t, flags=re.I)
    t = re.sub(r"^\d{3,4}\s*(?:A\.?D\.?|C\.?E\.?)\s*[-–—]?\s*", "", t, flags=re.I)
    t = re.sub(r"^\d{3,4}\s*[-–—]\s*\d{3,4}\s*[-–—]?\s*", "", t, flags=re.I)
    return t.strip()


def extract_date_from_header(header):
    """Parse year from header text. Returns (start, end, calendar) or (None, None, None)."""
    m = re.search(r"(\d{3,4})\s+to\s+(\d{3,4})\s*(?:B\.?C\.?E\.?|BC)\b", header, re.I)
    if m:
        return (-int(m.group(1)), -int(m.group(2)), "BCE")
    m = re.search(r"(\d{3,4})\s*(?:B\.?C\.?E\.?|BC)\b", header, re.I)
    if m:
        y = -int(m.group(1))
        return (y, y, "BCE")
    m = re.search(r"C\.?E\.?\s*(\d{3,4})\s+to\s+(\d{3,4})", header, re.I)
    if m:
        return (int(m.group(1)), int(m.group(2)), "CE")
    m = re.search(r"C\.?E\.?\s*(\d{3,4})-(\d{3,4})", header, re.I)
    if m:
        return (int(m.group(1)), int(m.group(2)), "CE")
    m = re.search(r"(\d{3,4})\s*(?:A\.?D\.?|C\.?E\.?)\b", header, re.I)
    if m:
        y = int(m.group(1))
        return (y, y, "CE")
    m = re.search(r"(\d{3,4})\s+to\s+(\d{3,4})", header)
    if m:
        return (int(m.group(1)), int(m.group(2)), "CE")
    m = re.search(r"(\d{3,4})\s(?!days|rotations|d\b)", header, re.I)
    if m:
        y = int(m.group(1))
        return (y, y, "CE")
    return (None, None, None)


def parse_headers_with_positions(content):
    """Return list of (level, title, start_pos, end_pos) in document order."""
    result = []
    for m in re.finditer(r"^(#{1,4})\s+(.+)$", content, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        start, end = m.span()
        result.append((level, title, start, end))
    return result


def extract_section_bodies(content, headers):
    """Return {title: body} - body from end of header to the next header (any level).
    Each section includes only its direct content; sub-headers define nested sections."""
    bodies = {}
    for i, (level, title, start, end) in enumerate(headers):
        next_start = len(content)
        if i + 1 < len(headers):
            next_start = headers[i + 1][2]
        body = content[end:next_start].strip()
        if i == 0 and start > 0:
            prefix = content[:start].strip()
            prefix = re.sub(r"^---\s*\n[\s\S]*?\n---\s*\n?", "", prefix).strip()
            if prefix:
                body = prefix + "\n\n" + body
        bodies[title] = body
    return bodies


def rewrite_image_paths(body):
    """Rewrite relative image/link paths to absolute paradigm-threat-files URLs."""
    def repl(m):
        path = m.group(1).strip()
        if path.startswith(("http://", "https://")):
            return m.group(0)
        if path.startswith("./"):
            path = f"{CHRONOLOGY_BASE}/{path[2:]}"
        elif path.startswith("../"):
            parts = CHRONOLOGY_BASE.split("/")
            while path.startswith("../"):
                path = path[3:]
                if parts:
                    parts.pop()
            base = "/".join(parts) if parts else ""
            path = f"{base}/{path}" if base else path
        else:
            path = f"{CHRONOLOGY_BASE}/{path}"
        path = path.replace("//", "/").strip("/")
        return f"]({FILES_BASE_URL}/{path})"

    return re.sub(r"\]\(([^)]+)\)", repl, body)


def make_event_filename(start_year, era, title):
    """Return bce-YYYY-slug.md or ce-YYYY-slug.md for events."""
    abs_year = abs(start_year)
    s = slugify(title)
    prefix = "bce" if start_year < 0 or era == "BCE" else "ce"
    return f"{prefix}-{abs_year}-{s}.md"


def make_article_filename(title):
    """Return slug.md for articles."""
    return f"{slugify(title)}.md"


def infer_dates(level, title, parent_dates, era_context):
    """Infer (start, end, calendar) for entry."""
    start, end, cal = extract_date_from_header(title)
    if start is not None and end is not None:
        return [{"start": start, "end": end, "calendar": cal or "BCE"}]

    if title in ERA_RANGES:
        start, end = ERA_RANGES[title]
        cal = "BCE" if start < 0 else "CE"
        return [{"start": start, "end": end, "calendar": cal}]

    if parent_dates:
        return [{"start": parent_dates[0], "end": parent_dates[1], "calendar": parent_dates[2]}]

    if era_context:
        start, end = era_context
        cal = "BCE" if start < 0 else "CE"
        return [{"start": start, "end": end, "calendar": cal}]

    return [{"start": -4077, "end": -3148, "calendar": "BCE"}]


def strip_frontmatter(text):
    """Remove YAML frontmatter (---\\n...\\n---) from text."""
    return re.sub(r"^---\s*\n[\s\S]*?\n---\s*\n?", "", text).strip()


def write_md_file(md_path, title, body):
    """Write md file with # title and body. Always overwrite."""
    full_path = os.path.join(REPO_DIR, md_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    body_clean = strip_frontmatter(body)
    body_rewritten = rewrite_image_paths(body_clean)
    content = f"# {title}\n\n{body_rewritten}\n"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote: {md_path}")


def get_era_context(title):
    """Return (start, end) for current era based on header, or None."""
    return ERA_RANGES.get(title)


def build_tree(headers_with_pos, section_bodies):
    """Build hierarchy strictly from chronology header tags. Flatten first header only: rename to Introduction,
    promote its direct children to roots. Events: date in header OR section in SECTIONS_AS_EVENTS. Articles: else."""
    roots = []
    stack = []
    seen_titles = {}
    seen_slugs_per_topic = {}
    first_header_title = headers_with_pos[0][1] if headers_with_pos else None
    current_level2_slug = "overview"

    for idx, (level, title, _start, _end) in enumerate(headers_with_pos):
        # Rename first section to Introduction
        display_title = INTRO_TITLE if (idx == 0 and title == first_header_title) else title

        if level == 2:
            current_level2_slug = slugify(title)[:50] or "overview"

        parent_dates = None
        era_context = None
        parent_slug = "overview"
        if stack:
            _, parent_entry, pd, ec = stack[-1]
            if "dates" in parent_entry and parent_entry["dates"]:
                d = parent_entry["dates"][0]
                parent_dates = (d["start"], d["end"], d["calendar"])
            else:
                parent_dates = pd
            era_context = ec
            parent_slug = slugify(parent_entry["title"])[:50]

        ec = get_era_context(title)
        if ec is not None:
            era_context = ec

        header_date = extract_date_from_header(title)
        is_section_event = title in SECTIONS_AS_EVENTS
        has_explicit_date = header_date != (None, None, None)
        is_event = has_explicit_date or is_section_event
        is_article = not is_event
        if has_explicit_date:
            display_title = strip_date_prefix(display_title)

        dates = infer_dates(level, title, parent_dates, era_context)
        start_year = dates[0]["start"]
        era = dates[0]["calendar"]
        slug_base = slugify(display_title)

        if is_article:
            topic = current_level2_slug or "overview"
            fname = make_article_filename(display_title)
            if topic not in seen_slugs_per_topic:
                seen_slugs_per_topic[topic] = {}
            if slug_base in seen_slugs_per_topic[topic]:
                seen_slugs_per_topic[topic][slug_base] += 1
                base = fname[:-3] if fname.endswith(".md") else fname
                fname = f"{base}-{seen_slugs_per_topic[topic][slug_base]}.md"
            else:
                seen_slugs_per_topic[topic][slug_base] = 0
            md_path = f"articles/{topic}/{fname}"
        else:
            fname = make_event_filename(start_year, era, display_title)
            if slug_base in seen_titles:
                seen_titles[slug_base] += 1
                base = fname[:-3] if fname.endswith(".md") else fname
                fname = f"{base}-{seen_titles[slug_base]}.md"
            else:
                seen_titles[slug_base] = 0
            md_path = f"events/{fname}"

        body = section_bodies.get(title, "")
        write_md_file(md_path, display_title, body)

        entry_id = INTRO_ID if (idx == 0 and title == first_header_title) else f"evt-{slugify(display_title)[:50]}"
        entry = {
            "id": entry_id,
            "title": display_title,
            "type": "article" if is_article else "event",
            "md_path": md_path,
            "children": [],
        }
        if not is_article:
            entry["dates"] = dates

        while stack and stack[-1][0] >= level:
            stack.pop()

        # Flatten: promote direct children of first header (level 2) to roots
        if len(stack) == 1 and level == 2:
            stack.pop()

        if not stack:
            roots.append(entry)
        else:
            parent_entry = stack[-1][1]
            parent_entry["children"].append(entry)

        if is_article:
            dates_for_children = parent_dates
        else:
            d0 = dates[0]
            dates_for_children = (d0["start"], d0["end"], d0["calendar"])
        stack.append((level, entry, dates_for_children, era_context))

    return roots


def split_intro_from_timeline(roots):
    """Split roots into introArticles (before first event) and timeline entries."""
    intro = []
    timeline = []
    seen_first_event = False
    for r in roots:
        if r.get("type") == "event":
            seen_first_event = True
        if seen_first_event:
            timeline.append(r)
        else:
            intro.append(r)
    return intro, timeline


def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: {SOURCE_FILE} not found")
        return 1

    if os.path.isdir(EVENTS_DIR):
        shutil.rmtree(EVENTS_DIR)
    if os.path.isdir(ARTICLES_DIR):
        shutil.rmtree(ARTICLES_DIR)
    os.makedirs(EVENTS_DIR, exist_ok=True)
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    headers = parse_headers_with_positions(content)
    section_bodies = extract_section_bodies(content, headers)
    all_roots = build_tree(headers, section_bodies)
    intro_articles, entries = split_intro_from_timeline(all_roots)

    def to_intro_item(node):
        return {"id": node["id"], "title": node["title"], "md_path": node["md_path"]}

    def collect_intro_flat(nodes):
        out = []
        for n in nodes:
            out.append(to_intro_item(n))
            out.extend(collect_intro_flat(n.get("children", [])))
        return out

    intro_flat = collect_intro_flat(intro_articles)

    out = {
        "entries": entries,
        "introArticles": intro_flat,
        "meta": {"source": "build-entries.py"},
    }

    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    def count_entries(nodes):
        return sum(1 + count_entries(n.get("children", [])) for n in nodes)

    total = count_entries(entries)
    print(f"Built {total} entries in events.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
