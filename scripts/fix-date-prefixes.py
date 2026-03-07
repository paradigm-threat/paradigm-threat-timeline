#!/usr/bin/env python3
"""
Fix H1 headers to include date prefix, and rename files to match events.json titles.

Rules:
- Only processes events (type=event) with dates[] and existing md files
- Skips files that are shared by multiple events
- H1 becomes: # {date} {cal} — {title}  (using events.json title)
- Filename slug derived from events.json title
- Updates md_path in events.json after renames
- Does NOT change the title field in events.json
"""

import json, os, re, sys
from collections import defaultdict

DRY_RUN = "--dry-run" in sys.argv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PATH = os.path.join(ROOT, "data", "events.json")

with open(EVENTS_PATH) as f:
    data = json.load(f)

# Pass 1: collect ALL entries pointing to each file (not just events with dates)
file_to_all_entries = defaultdict(list)
# Separate: events with dates that have existing files
file_to_dated_events = defaultdict(list)

def collect(entries):
    for e in entries:
        md = e.get("md_path", "")
        etype = e.get("type", "")
        dates = e.get("dates", [])
        if md:
            full = os.path.join(ROOT, md)
            if os.path.exists(full):
                file_to_all_entries[md].append(e)
                if etype == "event" and dates:
                    file_to_dated_events[md].append(e)
        collect(e.get("children", []))

collect(data.get("entries", []))

# Skip files used by multiple entries (any type)
shared = {md for md, entries in file_to_all_entries.items() if len(entries) > 1}
if shared:
    print(f"SKIPPING {len(shared)} shared files (multiple entries → same file):")
    for md in sorted(shared):
        entries = file_to_all_entries[md]
        print(f"  {os.path.basename(md)} ← {len(entries)} entries: {[e['id'] for e in entries]}")
    print()

def slugify(text, max_len=60):
    """Convert title to filename slug."""
    s = text.lower()
    # Normalize "C.E." / "B.C.E." to "ce" / "bce" before general cleanup
    s = re.sub(r"b\.?c\.?e\.?", "bce", s)
    s = re.sub(r"c\.?e\.?", "ce", s)
    s = re.sub(r"[''']", "", s)  # remove apostrophes
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s

def format_date(dates_list):
    """Get the date string from the first date entry."""
    d = dates_list[0]
    cal = d.get("calendar", "CE")
    start = d.get("start")
    if start is None:
        return None
    if cal == "BCE":
        return f"{abs(start)} BCE"
    else:
        return f"{start} CE"

h1_fixed = 0
renamed = 0
json_updated = False

for md, evts in sorted(file_to_dated_events.items()):
    if md in shared:
        continue
    
    e = evts[0]
    title = e["title"]
    dates = e["dates"]
    date_str = format_date(dates)
    if not date_str:
        continue
    
    full_path = os.path.join(ROOT, md)
    
    # If the title already starts with a date pattern, use it as-is
    title_has_date = bool(re.match(r"^\d+\s*(BCE|CE|AD)\b", title))
    if title_has_date:
        new_h1 = title
    else:
        new_h1 = f"{date_str} — {title}"
    
    # --- Fix H1 header ---
    with open(full_path, "r") as f:
        content = f.read()
    
    m = re.match(r"^(#\s+)(.+)", content, re.MULTILINE)
    if m:
        old_h1_line = m.group(0)
        current_h1 = m.group(2).strip()
        new_h1_line = f"# {new_h1}"
        
        if current_h1 != new_h1:
            if DRY_RUN:
                print(f"[H1] {os.path.basename(md)}")
                print(f"  OLD: # {current_h1}")
                print(f"  NEW: # {new_h1}")
            else:
                content = content.replace(old_h1_line, new_h1_line, 1)
                with open(full_path, "w") as f:
                    f.write(content)
                print(f"[H1] {os.path.basename(md)}: # {new_h1}")
            h1_fixed += 1
    
    # --- Rename file if slug doesn't match ---
    dirname = os.path.dirname(full_path)
    basename = os.path.basename(full_path)
    
    # Extract XX.YY.ZZ prefix
    prefix_m = re.match(r"^(\d+\.\d+\.\d+)-(.+)\.md$", basename)
    if not prefix_m:
        continue
    
    num_prefix = prefix_m.group(1)
    old_slug = prefix_m.group(2)
    
    # Build expected slug from date + title
    if title_has_date:
        new_slug = slugify(title)
    else:
        new_slug = slugify(f"{date_str} {title}")
    
    if old_slug != new_slug:
        new_basename = f"{num_prefix}-{new_slug}.md"
        new_full = os.path.join(dirname, new_basename)
        
        # Compute new md_path relative to ROOT
        new_md = os.path.relpath(new_full, ROOT)
        
        if DRY_RUN:
            print(f"[RENAME] {basename} → {new_basename}")
        else:
            os.rename(full_path, new_full)
            # Update md_path in events.json
            e["md_path"] = new_md
            json_updated = True
            print(f"[RENAME] {basename} → {new_basename}")
        renamed += 1

# Save events.json if changed
if json_updated and not DRY_RUN:
    with open(EVENTS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nUpdated {EVENTS_PATH}")

print(f"\nSummary: {h1_fixed} H1 headers fixed, {renamed} files renamed")
if DRY_RUN:
    print("(DRY RUN — no changes made)")
