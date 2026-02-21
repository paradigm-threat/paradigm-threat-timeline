#!/usr/bin/env python3
"""Rename media/ subdirectories to match the decimal chapter numbering system,
then update all /media/<old-name>/ references in content/ files."""

import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(ROOT, 'media')
CONTENT_DIR = os.path.join(ROOT, 'content')

# Mapping: old name → new name
RENAME_MAP = {
    'overview':                                         '00-overview',
    'project-objective':                                '00-project-objective',
    'before-creation':                                  '01-before-creation',
    'the-golden-age':                                   '02-the-golden-age',
    'the-dark-ages':                                    '03-the-dark-ages',
    'the-blip':                                         '04-the-blip',
    '11th-century-ce-common-era-begins':                '05-11th-century-ce-common-era-begins',
    '12th-century-ce-birth-of-christianity':            '06-12th-century-ce-birth-of-christianity',
    '13th-century-ce-the-russian-horde-tartarian-empire': '07-13th-century-ce-the-russian-horde-tartarian-empire',
    '14th-century-ce-great-expansion-of-the-mongol-slav': '08-14th-century-ce-great-expansion-of-the-mongol-slav',
    '15th-century-ce-ottoman-conquest-of-europe':       '09-15th-century-ce-ottoman-conquest-of-europe',
    '16th-century-ce-reformation-and-inquisition':      '10-16th-century-ce-reformation-and-inquisition',
    '17th-century-romanovs-rise-to-power':              '11-17th-century-romanovs-rise-to-power',
    '18th-century-ce-mudflood-and-pugachev':            '12-18th-century-ce-mudflood-and-pugachev',
}

def rename_media_dirs():
    renamed = []
    for old, new in RENAME_MAP.items():
        old_path = os.path.join(MEDIA_DIR, old)
        new_path = os.path.join(MEDIA_DIR, new)
        if os.path.isdir(old_path):
            if os.path.exists(new_path):
                print(f'  SKIP (target exists): {old} → {new}')
            else:
                shutil.move(old_path, new_path)
                renamed.append((old, new))
                print(f'  Renamed: {old} → {new}')
        else:
            print(f'  Missing (skipped): {old}')
    return renamed

def update_content_files():
    # Build a sorted list of replacements (longest old name first to avoid partial matches)
    replacements = sorted(RENAME_MAP.items(), key=lambda x: len(x[0]), reverse=True)
    
    md_files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    total_changes = 0

    for fname in sorted(md_files):
        fpath = os.path.join(CONTENT_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        updated = original
        for old, new in replacements:
            updated = updated.replace(f'/media/{old}/', f'/media/{new}/')

        if updated != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(updated)
            count = sum(original.count(f'/media/{old}/') for old, _ in replacements)
            print(f'  Updated: {fname}')
            total_changes += 1

    return total_changes

if __name__ == '__main__':
    print('=== Renaming media/ directories ===')
    renamed = rename_media_dirs()
    print(f'\n✓ Renamed {len(renamed)} directories\n')

    print('=== Updating content/ file references ===')
    changed = update_content_files()
    print(f'\n✓ Updated {changed} content files\n')

    print('Done.')
