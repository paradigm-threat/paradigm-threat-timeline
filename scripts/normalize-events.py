#!/usr/bin/env python3
"""
Add missing dates to events using 'last date header' rule: sections without date
headers occur within the date of the last preceding ### with a date.
Normalize filenames: YYYY-bce-title or YYYY-ce-title, no ranges (use start only).
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_DIR = os.path.join(REPO_DIR, "events")
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

def extract_date_from_header(header):
    """Parse year from header. For ranges (X to Y), return start year. Skip day counts (225 days)."""
    # BCE: 4077 B.C.E. or 806 to 687 B.C.E.
    m = re.search(r'(\d{3,4})\s*(?:to\s+\d{3,4}\s+)?(?:B\.?C\.?E\.?|BC)\b', header, re.I)
    if m:
        return -int(m.group(1))
    # CE: 1185 C.E. or C.E. 1666 to 1675 - exclude X days (e.g. 225 days)
    m = re.search(r'(?:C\.?E\.?\.?\s+)?(\d{3,4})\s*(?:to\s+\d{3,4}\s+)?(?:A\.?D\.?|C\.?E\.?)?(?!\s*days)\b', header, re.I)
    if m:
        return int(m.group(1))
    # Fallback: 3-4 digit number, but NOT followed by "days" (e.g. "225 days")
    m = re.search(r'(\d{3,4})\s+(?!days|rotations)', header, re.I)
    if m:
        return int(m.group(1))
    return None

def slugify(text):
    """Create URL-safe slug, stripping date-like prefixes."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:80] or "untitled"

def build_title_to_date_map(source_dir):
    """Parse source markdown files. Return {title: (year, era)} using last-date-header rule."""
    chronology_path = os.path.join(source_dir, "history", "chronology", "page.md")
    mudflood_path = os.path.join(source_dir, "history", "mudflood", "page.md")
    mars_path = os.path.join(source_dir, "cosmos", "mars", "page.md")

    result = {}

    def process_file(filepath):
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(r'^### (.+)$', re.MULTILINE)
        matches = list(pattern.finditer(content))
        first_date = None
        for m in matches:
            title = m.group(1).strip()
            year = extract_date_from_header(title)
            if year is not None and first_date is None:
                first_date = (year, "BCE" if year < 0 else "CE")
        last_date = first_date  # Sections before first dated ### use first date
        for m in matches:
            title = m.group(1).strip()
            year = extract_date_from_header(title)
            if year is not None:
                last_date = (year, "BCE" if year < 0 else "CE")
            if last_date is not None:
                result[title] = last_date

    process_file(chronology_path)
    process_file(mudflood_path)
    process_file(mars_path)
    if "Earth History Timeline Reconstruction" not in result:
        result["Earth History Timeline Reconstruction"] = (-4077, "BCE")
    return result

def build_title_to_priority_map(source_dir):
    """Parse source markdown. Return {title: priority} from header level (#=1, ##=2, ###=3, ####=4)."""
    files = [
        os.path.join(source_dir, "history", "chronology", "page.md"),
        os.path.join(source_dir, "history", "mudflood", "page.md"),
        os.path.join(source_dir, "cosmos", "mars", "page.md"),
    ]
    result = {}
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'^(#{1,4})\s+(.+)$', content, re.MULTILINE):
            level = len(m.group(1))
            title = m.group(2).strip()
            result[title] = level
    if "Earth History Timeline Reconstruction" not in result:
        result["Earth History Timeline Reconstruction"] = 1
    return result

def make_filename(year, era, title):
    """Format: bce-YYYY-slug or ce-YYYY-slug. Strip date from title when slugifying."""
    abs_year = abs(year)
    # Remove date-like parts from title for slug (e.g. "4077 B.C.E. Foo" -> "foo")
    clean_title = re.sub(r'^\d{3,4}\s*(?:to\s+\d{3,4}\s+)?(?:B\.?C\.?E\.?|A\.?D\.?|C\.?E\.?\.?)\s*', '', title, flags=re.I)
    clean_title = re.sub(r'^(?:C\.?E\.?\.?\s+)?\d{3,4}\s*(?:to\s+\d{3,4}\s+)?[-–]\s*', '', clean_title, flags=re.I)
    clean_title = re.sub(r'^Sept\s+\d+\s*,?\s*\d+\s*C\.?E\.?\.?\s*', '', clean_title, flags=re.I)
    slug = slugify(clean_title)
    if not slug:
        slug = slugify(title)
    return f"{era.lower()}-{abs_year}-{slug}.md"

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="/home/ari/dev/paradigm-threat-files")
    args = ap.parse_args()

    title_to_date = build_title_to_date_map(args.source_dir)
    title_to_priority = build_title_to_priority_map(args.source_dir)

    with open(EVENTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    events = data["events"]

    # First pass: assign dates from chronology (title_to_date) and compute new filenames
    for evt in events:
        title = evt["title"]
        if title in title_to_date:
            year, era = title_to_date[title]
            evt["dates"] = [{"value": year, "calendar": era}]
        elif evt.get("dates"):
            d = evt["dates"][0]
            year = d["value"]
            era = d.get("calendar", "CE" if year >= 0 else "BCE")
            title_to_date[title] = (year, era)

        evt["priority"] = title_to_priority.get(title, 3)

        if evt.get("dates"):
            year_val = evt["dates"][0]["value"]
            is_bce = year_val < 0 or evt["dates"][0].get("calendar") == "BCE"
            if is_bce:
                evt["timeline_sources"] = [
                    "Saturnian",
                    "Jno Cook",
                    "N. A. Morozov",
                    "Immanuel Velikovsky",
                    "David Talbott",
                ]

        if evt.get("dates"):
            year = evt["dates"][0]["value"]
            era = evt["dates"][0].get("calendar", "CE" if year >= 0 else "BCE")
            new_fname = make_filename(year, era, title)
        else:
            # No date - use existing filename (slug from title)
            old_path = evt.get("md_path", "")
            new_fname = os.path.basename(old_path) if old_path else f"{slugify(title)}.md"
        evt["_new_fname"] = new_fname

    # Build old_path -> new_path for renames
    renames = []
    for evt in events:
        old_path = evt.get("md_path", "")
        if not old_path:
            continue
        old_full = os.path.join(REPO_DIR, old_path)
        new_fname = evt["_new_fname"]
        new_path = f"events/{new_fname}"
        if os.path.basename(old_path) != new_fname:
            renames.append((old_full, os.path.join(EVENTS_DIR, new_fname)))
        evt["md_path"] = new_path
        evt["id"] = f"evt-{new_fname.replace('.md','')[:60]}"
        del evt["_new_fname"]

    # Rename files
    for old_full, new_full in renames:
        if os.path.exists(old_full):
            if old_full != new_full and os.path.exists(new_full):
                os.remove(new_full)  # avoid collision
            os.rename(old_full, new_full)
            print(f"Renamed: {os.path.basename(old_full)} -> {os.path.basename(new_full)}")

    with open(EVENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {EVENTS_JSON}")

    # Reassign sections and collapse duplicate timeline_sources
    subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "refactor-sections.py")], check=True)

if __name__ == "__main__":
    main()
