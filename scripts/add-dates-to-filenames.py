#!/usr/bin/env python3
"""
Add start dates to content file names for events that have dates.

Format: XX.YY.ZZ-{year}-{bce|ce}-slug.md

- Skips files that already have the correct date in the name
- Shortens overly long slugs (target max ~80 chars for filename)
- Updates both files on disk and md_path in events.json
"""

import json
import os
import re
import sys

EVENTS_JSON = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')
CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'content')

MAX_FILENAME_LEN = 75  # target max filename length (without .md)

def slugify(text):
    """Create a short slug from text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def shorten_slug(slug, max_len):
    """Shorten a slug to max_len by trimming trailing words."""
    if len(slug) <= max_len:
        return slug
    # Remove trailing words until short enough
    parts = slug.split('-')
    while len('-'.join(parts)) > max_len and len(parts) > 2:
        parts.pop()
    return '-'.join(parts)

def build_new_filename(prefix, year, slug, is_bce):
    """Build new filename: prefix-year-bce/ce-slug.md"""
    era = 'bce' if is_bce else 'ce'
    abs_year = abs(year)
    date_part = f"{abs_year}-{era}"
    
    # Check if slug already starts with the date
    # Some files already have patterns like "ce-1421-..." 
    existing_date_pattern = re.compile(
        r'^(bce|ce)-?\d+-?|^\d+-(bce|ce)-?'
    )
    slug_cleaned = existing_date_pattern.sub('', slug).strip('-')
    if not slug_cleaned:
        slug_cleaned = slug
    
    base = f"{prefix}-{date_part}-{slug_cleaned}"
    
    # Shorten if too long
    if len(base) > MAX_FILENAME_LEN:
        available = MAX_FILENAME_LEN - len(f"{prefix}-{date_part}-")
        slug_cleaned = shorten_slug(slug_cleaned, max(available, 10))
        base = f"{prefix}-{date_part}-{slug_cleaned}"
    
    return base + ".md"

def has_correct_date_format(filename, year, is_bce):
    """Check if filename already has the correct date in YYYY-era format."""
    era = 'bce' if is_bce else 'ce'
    abs_year = abs(year)
    # Only accept the canonical format: XX.YY.ZZ-YYYY-era-
    pattern = re.compile(rf'^\d+\.\d+\.\d+-{abs_year}-{era}-')
    return bool(pattern.match(filename))

def collect_renames(entries):
    """Walk entries and collect (old_md_path, new_md_path) pairs."""
    renames = []
    
    def walk(entries):
        for e in entries:
            dates = e.get('dates', [])
            md_path = e.get('md_path', '')
            
            if dates and md_path:
                start_year = dates[0].get('start')
                if start_year is not None:
                    is_bce = start_year < 0
                    
                    # Parse current filename
                    filename = os.path.basename(md_path)
                    dirname = os.path.dirname(md_path)
                    
                    # Check if already has correct date in canonical format
                    if has_correct_date_format(filename, start_year, is_bce):
                        if 'children' in e:
                            walk(e['children'])
                        continue
                    
                    # Extract prefix (XX.YY.ZZ) and slug
                    m = re.match(r'^(\d+\.\d+\.\d+)-(.+)\.md$', filename)
                    if not m:
                        print(f"  SKIP (no match): {filename}")
                        if 'children' in e:
                            walk(e['children'])
                        continue
                    
                    prefix = m.group(1)
                    slug = m.group(2)
                    
                    new_filename = build_new_filename(prefix, start_year, slug, is_bce)
                    new_md_path = os.path.join(dirname, new_filename) if dirname else new_filename
                    
                    if new_md_path != md_path:
                        renames.append((md_path, new_md_path, e))
            
            if 'children' in e:
                walk(e['children'])
    
    walk(entries)
    return renames

def main():
    dry_run = '--dry-run' in sys.argv
    
    with open(EVENTS_JSON, 'r') as f:
        data = json.load(f)
    
    renames = collect_renames(data['entries'])
    
    if not renames:
        print("No renames needed.")
        return
    
    print(f"{'DRY RUN: ' if dry_run else ''}Planning {len(renames)} renames:\n")
    
    for old_path, new_path, entry in renames:
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        print(f"  {old_name}")
        print(f"  → {new_name}")
        print()
    
    if dry_run:
        print("Dry run complete. No changes made.")
        return
    
    # Execute renames
    for old_path, new_path, entry in renames:
        old_full = os.path.join(os.path.dirname(EVENTS_JSON), '..', old_path)
        new_full = os.path.join(os.path.dirname(EVENTS_JSON), '..', new_path)
        
        if os.path.exists(old_full):
            os.rename(old_full, new_full)
            print(f"  RENAMED: {os.path.basename(old_path)} → {os.path.basename(new_path)}")
        else:
            print(f"  WARNING: {old_full} does not exist, skipping file rename")
        
        # Update md_path in the entry
        entry['md_path'] = new_path
    
    # Write updated events.json
    with open(EVENTS_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print(f"\nDone! Renamed {len(renames)} files and updated events.json.")

if __name__ == '__main__':
    main()
