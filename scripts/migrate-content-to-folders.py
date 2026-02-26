#!/usr/bin/env python3
"""
Migrate content/*.md into chapter-specific subfolders matching the media/ layout.

Steps:
  1. Build chapter → folder-name mapping from events.json chapter roots
  2. Create content/<chapter-folder>/ directories
  3. Move each .md file into its chapter folder
  4. Update events.json md_path values:  content/XX.YY.ZZ-slug.md → content/<folder>/XX.YY.ZZ-slug.md
  5. Update cross-links in every .md file (all three link styles)
  6. Report any broken links

Folder naming: uses media/ directory names where they exist, otherwise derives
from the chapter root filename slug.
"""

import json
import os
import re
import shutil
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_DIR, "content")
MEDIA_DIR = os.path.join(REPO_DIR, "media")
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")


def build_chapter_folder_map() -> dict[str, str]:
    """Map chapter number (e.g. '00', '01') → folder name."""
    # Start from media/ directory names as the canonical source
    media_map: dict[str, str] = {}
    if os.path.isdir(MEDIA_DIR):
        for d in os.listdir(MEDIA_DIR):
            dp = os.path.join(MEDIA_DIR, d)
            if os.path.isdir(dp):
                # Extract leading number: "00.overview" → "00", "15-author-profiles" → "15"
                m = re.match(r'^(\d{2})', d)
                if m:
                    media_map[m.group(1)] = d

    # For any chapter in content/ that doesn't have a media folder, derive from filename
    for fname in os.listdir(CONTENT_DIR):
        if not fname.endswith('.md'):
            continue
        m = re.match(r'^(\d{2})\.00\.00-(.+)\.md$', fname)
        if m:
            ch = m.group(1)
            if ch not in media_map:
                slug = m.group(2)
                media_map[ch] = f"{ch}-{slug}"

    return media_map


def collect_all_md() -> list[str]:
    """Collect all .md filenames in content/ (flat)."""
    return sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith('.md'))


def update_events_json(folder_map: dict[str, str]) -> int:
    """Update md_path in events.json to include subfolder."""
    with open(EVENTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = [0]

    def walk(nodes):
        for node in nodes:
            if 'md_path' in node:
                old = node['md_path']
                # old format: content/XX.YY.ZZ-slug.md
                fname = os.path.basename(old)
                ch = fname[:2]
                folder = folder_map.get(ch)
                if folder:
                    new = f"content/{folder}/{fname}"
                    if old != new:
                        node['md_path'] = new
                        count[0] += 1
            walk(node.get('children', []))

    walk(data.get('entries', []))
    walk(data.get('introArticles', []))

    with open(EVENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    return count[0]


def update_crosslinks(folder_map: dict[str, str]) -> tuple[int, int]:
    """Update all markdown cross-links that reference content files.

    Link styles handled:
      - /content/XX.YY.ZZ-slug.md          (absolute)
      - ./XX.YY.ZZ-slug.md                 (relative same-dir)
      - XX.YY.ZZ-slug.md                   (bare)
      - /content/<folder>/XX.YY.ZZ-slug.md (already migrated — skip)
    """
    # Pattern: capture optional /content/ or ./ prefix, then the numbered filename
    # Must NOT already have a subfolder in the path
    link_re = re.compile(
        r'(/content/|\./)(\d{2}\.\d{2}\.\d{2}-[^)\s"\'>\n]+\.md)'
    )
    # Bare reference (just the filename, no prefix) — in markdown link targets
    bare_re = re.compile(
        r'(\()(\d{2}\.\d{2}\.\d{2}-[^)\s"\'>\n]+\.md)(\))'
    )

    total_files = 0
    total_links = 0

    # Walk all content subfolders
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()

            new_text = text
            count = 0

            def replace_prefixed(m):
                nonlocal count
                prefix = m.group(1)
                target_fname = m.group(2)
                ch = target_fname[:2]
                folder = folder_map.get(ch)
                if folder:
                    count += 1
                    if prefix == '/content/':
                        return f'/content/{folder}/{target_fname}'
                    else:  # ./
                        return f'/content/{folder}/{target_fname}'
                return m.group(0)

            new_text = link_re.sub(replace_prefixed, new_text)

            def replace_bare(m):
                nonlocal count
                paren_open = m.group(1)
                target_fname = m.group(2)
                paren_close = m.group(3)
                ch = target_fname[:2]
                folder = folder_map.get(ch)
                if folder:
                    count += 1
                    return f'{paren_open}/content/{folder}/{target_fname}{paren_close}'
                return m.group(0)

            new_text = bare_re.sub(replace_bare, new_text)

            if new_text != text:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                rel = os.path.relpath(fpath, REPO_DIR)
                print(f"  [LINKS] {rel}  ({count} ref(s))")
                total_files += 1
                total_links += count

    return total_files, total_links


def check_broken_links(folder_map: dict[str, str]) -> list[tuple[str, str]]:
    """Check for broken links across all content files."""
    # Build set of all existing .md filenames
    existing = set()
    for root, dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith('.md'):
                existing.add(f)

    broken = []
    link_target_re = re.compile(
        r'(?:/content/[^/]+/|/content/|\./)(\d{2}\.\d{2}\.\d{2}-[^)\s"\'>\n]+\.md)'
    )
    bare_target_re = re.compile(
        r'\((\d{2}\.\d{2}\.\d{2}-[^)\s"\'>\n]+\.md)\)'
    )

    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()

            rel = os.path.relpath(fpath, REPO_DIR)
            for m in link_target_re.finditer(text):
                tgt = m.group(1)
                if tgt not in existing:
                    broken.append((rel, tgt))
            for m in bare_target_re.finditer(text):
                tgt = m.group(1)
                if tgt not in existing:
                    broken.append((rel, tgt))

    return broken


def main():
    print("=== Migrate content/ to chapter subfolders ===\n")

    # Step 1: Build mapping
    folder_map = build_chapter_folder_map()
    print("Chapter → Folder mapping:")
    for ch in sorted(folder_map):
        print(f"  {ch} → {folder_map[ch]}")
    print()

    # Step 2: Create directories and move files
    all_md = collect_all_md()
    print(f"── Step 1: Moving {len(all_md)} files ──────────────────────────")
    moved = 0
    for fname in all_md:
        ch = fname[:2]
        folder = folder_map.get(ch)
        if not folder:
            print(f"  [SKIP] {fname} — no folder for chapter {ch}")
            continue

        dest_dir = os.path.join(CONTENT_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)

        src = os.path.join(CONTENT_DIR, fname)
        dst = os.path.join(dest_dir, fname)
        shutil.move(src, dst)
        moved += 1

    print(f"  {moved} files moved.\n")

    # Step 3: Update events.json
    print("── Step 2: Updating events.json ─────────────────────────────")
    n = update_events_json(folder_map)
    print(f"  {n} md_path values updated.\n")

    # Step 4: Update cross-links
    print("── Step 3: Updating cross-links ─────────────────────────────")
    nf, nl = update_crosslinks(folder_map)
    print(f"\n  {nl} link(s) in {nf} file(s) updated.\n")

    # Step 5: Check broken links
    print("── Step 4: Checking for broken links ────────────────────────")
    broken = check_broken_links(folder_map)
    if broken:
        print(f"  [WARN] {len(broken)} broken link(s):")
        for src, tgt in broken:
            print(f"    {src}  →  {tgt}")
    else:
        print("  No broken links found.")

    print("\n=== Done. Now update scripts and run: ===")
    print("  npm run validate-events && npm run audit-missing && npm run generate-index")


if __name__ == '__main__':
    main()
