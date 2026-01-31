#!/usr/bin/env python3
"""
Split chronology/mudflood/mars pages into event markdown files.
Reads from paradigm-threat-files (--source-dir). Writes to paradigm-threat-timeline/events/.
Does NOT modify paradigm-threat-files.
"""
import argparse
import json
import os
import re
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_DIR = os.path.join(REPO_DIR, "events")
DATA_DIR = os.path.join(REPO_DIR, "data")
FILES_BASE_URL = "https://clevertree.github.io/paradigm-threat-files"

def slugify(text):
    """Create URL-safe slug from section title."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:80] or "untitled"

def rewrite_image_paths(content, base_dir, files_base_url):
    """Rewrite relative image/link paths to full paradigm-threat-files URLs."""
    if "chronology" in base_dir:
        prefix = "history/chronology"
    elif "mudflood" in base_dir:
        prefix = "history/mudflood"
    elif "mars" in base_dir:
        prefix = "cosmos/mars"
    else:
        prefix = ""

    def repl(m):
        path = m.group(1).strip()
        if path.startswith(('http://', 'https://')):
            return m.group(0)
        if path.startswith('./'):
            path = f"{prefix}/{path[2:]}"
        elif path.startswith('../'):
            # From chronology: ../../cosmos/ = cosmos/ (relative to repo root)
            while path.startswith('../'):
                path = path[3:]
            # path is now cosmos/cosmology/foo.jpg
        else:
            path = f"{prefix}/{path}"
        path = path.replace("//", "/").strip("/")
        return f"]({files_base_url}/{path})"

    content = re.sub(r'\]\(([^)]+)\)', repl, content)
    return content

def extract_date_from_header(header):
    """Parse year from ### 4077 B.C.E. ... or ### 1185 C.E. ..."""
    m = re.search(r'(\d{3,4})\s*(?:B\.?C\.?E\.?|BC)\b', header, re.I)
    if m:
        return -int(m.group(1))
    m = re.search(r'(\d{3,4})\s*(?:A\.?D\.?|C\.?E\.?)\b', header, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d{3,4})\s', header)
    if m:
        return int(m.group(1))  # assume CE
    return None

def header_level_to_priority(level):
    """Map markdown header level (#=1, ##=2, ###=3, ####=4) to priority (1=highest)."""
    return level

def build_title_priority_map(content):
    """Return {title: priority} from all headers in content."""
    result = {}
    for m in re.finditer(r'^(#{1,4})\s+(.+)$', content, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        result[title] = header_level_to_priority(level)
    return result

def split_markdown(content, base_dir, files_base_url):
    """Split content by ### headers. Returns list of (title, body, year)."""
    sections = []
    pattern = re.compile(r'^### (.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        body = rewrite_image_paths(body, base_dir, files_base_url)
        year = extract_date_from_header(title)
        sections.append((title, body, year))
    return sections

def extract_intro(content, base_dir, files_base_url):
    """Extract content before first ### as intro section."""
    m = re.search(r'^### ', content, re.MULTILINE)
    if not m:
        return None
    intro = content[:m.start()].strip()
    if len(intro) < 100:
        return None
    intro = rewrite_image_paths(intro, base_dir, files_base_url)
    return ("Earth History Timeline Reconstruction", intro, None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="../paradigm-threat-files", help="Path to paradigm-threat-files")
    ap.add_argument("--files-base-url", default=FILES_BASE_URL)
    args = ap.parse_args()
    source = os.path.abspath(os.path.join(SCRIPT_DIR, args.source_dir))

    os.makedirs(EVENTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    sources = [
        (os.path.join(source, "history", "chronology", "page.md"), "history/chronology"),
        (os.path.join(source, "history", "mudflood", "page.md"), "history/mudflood"),
        (os.path.join(source, "cosmos", "mars", "page.md"), "cosmos/mars"),
    ]

    all_events = []
    seen_slugs = set()

    for filepath, base_dir in sources:
        if not os.path.exists(filepath):
            print(f"Skip (not found): {filepath}")
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        intro = extract_intro(content, base_dir, args.files_base_url)
        sections = split_markdown(content, base_dir, args.files_base_url)
        if intro and base_dir == "history/chronology":
            sections = [intro] + sections
        title_to_priority = build_title_priority_map(content)
        print(f"{filepath}: {len(sections)} sections")

        for title, body, year in sections:
            slug = slugify(title)
            if slug in seen_slugs:
                slug = f"{slug}-{hash(title) % 10000}"
            seen_slugs.add(slug)
            fname = f"{slug}.md"
            out_path = os.path.join(EVENTS_DIR, fname)

            md_content = f"# {title}\n\n{body}\n"
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            evt_id = f"evt-{slug[:50]}"
            evt = {
                "id": evt_id,
                "title": title,
                "md_path": f"events/{fname}",
                "dates": [{"start": year, "calendar": "BCE" if year < 0 else "CE"}] if year is not None else [],
                "timeline_sources": (
                    ["Saturnian", "Jno Cook", "N. A. Morozov", "Immanuel Velikovsky", "David Talbott"]
                    if (year is not None and year < 0)
                    else (["Saturnian", "Fomenko"] if "chronology" in base_dir else ["MudFlood"] if "mudflood" in base_dir else ["Mars"])
                ),
                "context": {"mainstream": False, "theoretical": True},
                "priority": title_to_priority.get(title, 3),
                "categories": [],
                "tags": []
            }
            all_events.append(evt)

    events_data = {"events": all_events, "meta": {"source": "split-chronology.py"}}
    with open(os.path.join(DATA_DIR, "events.json"), 'w', encoding='utf-8') as f:
        json.dump(events_data, f, indent=2)

    print(f"Wrote {len(all_events)} events to data/events.json")

    # Assign sections and collapse duplicate timeline_sources
    import subprocess
    subprocess.run(
        [__import__("sys").executable, os.path.join(SCRIPT_DIR, "refactor-sections.py")],
        check=True,
    )

if __name__ == "__main__":
    main()
