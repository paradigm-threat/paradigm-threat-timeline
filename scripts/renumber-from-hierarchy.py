#!/usr/bin/env python3
"""
Renumber content files so XX.YY.ZZ reflects the events.json hierarchy.

Algorithm
─────────
  XX.00.00  Chapter root (first top-level entry in each section XX)
  XX.YY.00  Direct children of chapter root get their own YY slot
            Additional top-level entries continue the same YY counter
  XX.YY.ZZ  Children of any XX.YY.00 entry (where ZZ ≠ 0)
            Grandchildren of chapter root's children
            Deeper descendants flatten into the same ZZ space

Key rules:
  ZZ = 00 → standalone / parent article (not a child of another article)
  ZZ ≠ 0  → sub-article of XX.YY.00
  Cross-section children inherit the parent's XX prefix.
  Duplicate md_paths: first DFS occurrence is canonical.

Steps:
  1. Renames content/*.md files (finds misplaced files by slug)
  2. Rewrites data/events.json md_path fields
  3. Rewrites internal cross-links in content/*.md
  4. Reports broken links
"""

import json
import os
import re

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_DIR, "content")
MEDIA_DIR = os.path.join(REPO_DIR, "media")
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

NUM_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})(-.*)")


def _build_chapter_folder_map() -> dict[str, str]:
    """Map chapter number ('00', '01', …) → subfolder name under content/."""
    folder_map: dict[str, str] = {}
    # Prefer media/ directory names as canonical source
    if os.path.isdir(MEDIA_DIR):
        for d in os.listdir(MEDIA_DIR):
            dp = os.path.join(MEDIA_DIR, d)
            if os.path.isdir(dp):
                m = re.match(r'^(\d{2})', d)
                if m:
                    folder_map[m.group(1)] = d
    # Fallback: derive from chapter root filenames for chapters without media dirs
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            m = re.match(r'^(\d{2})\.00\.00-(.+)\.md$', fname)
            if m and m.group(1) not in folder_map:
                folder_map[m.group(1)] = f"{m.group(1)}-{m.group(2)}"
    return folder_map


CHAPTER_FOLDERS = _build_chapter_folder_map()


def slug_from_path(md_path: str) -> str:
    """Extract slug (dash + rest) from 'content/…/XX.YY.ZZ-slug.md'."""
    fname = os.path.basename(md_path)
    m = NUM_RE.match(fname)
    if m:
        return m.group(4)
    m2 = re.match(r"^\d{2}\.\d{3}(-.*)", fname)
    if m2:
        return m2.group(1)
    idx = fname.index("-")
    return fname[idx:]


def _all_md_files() -> dict[str, str]:
    """Return {basename: full_path} for every .md file under content/."""
    result = {}
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith('.md'):
                result[f] = os.path.join(root, f)
    return result


def find_by_slug(slug: str) -> str | None:
    """Find a file on disk (across all content subdirs) whose slug matches."""
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            m = NUM_RE.match(f)
            if m and m.group(4) == slug:
                return f
    return None


class Renumberer:
    """Walk events.json hierarchy and compute XX.YY.ZZ for every entry."""

    def __init__(self):
        self.section_yy: dict[str, int] = {}   # XX → next YY value
        self.slug_to_new: dict[str, str] = {}   # slug → canonical new md_path
        self.assignments: list[tuple[dict, str, bool]] = []  # (entry, new_path, is_dup)
        self.rename_map: dict[str, str] = {}    # old_basename → new_basename

    # ── counters ──────────────────────────────────────────────

    def _next_yy(self, xx: str) -> int:
        yy = self.section_yy.get(xx, 0)
        self.section_yy[xx] = yy + 1
        return yy

    # ── assignment ────────────────────────────────────────────

    def _assign(self, entry: dict, xx: str, yy: int, zz: int) -> bool:
        """Assign XX.YY.ZZ to *entry*.  Returns True unless duplicate."""
        slug = slug_from_path(entry["md_path"])

        if slug in self.slug_to_new:
            # Duplicate — just make it point to the canonical path
            self.assignments.append((entry, self.slug_to_new[slug], True))
            return False

        new_fname = f"{xx}.{yy:02d}.{zz:02d}{slug}"
        folder = CHAPTER_FOLDERS.get(xx, xx)
        new_path = f"content/{folder}/{new_fname}"
        old_fname = os.path.basename(entry["md_path"])

        self.slug_to_new[slug] = new_path
        self.assignments.append((entry, new_path, False))

        if old_fname != new_fname:
            self.rename_map[old_fname] = new_fname

        return True

    # ── ZZ children (children of any non-chapter-root entry) ─

    def _process_zz_children(
        self, children: list, parent_xx: str, parent_yy: int
    ) -> None:
        """Children get ZZ ≠ 0 under parent's YY.  Deeper levels flatten."""
        zz = [0]  # mutable counter shared across recursion
        self._walk_zz(children, parent_xx, parent_yy, zz)

    def _walk_zz(
        self, children: list, xx: str, yy: int, zz: list[int]
    ) -> None:
        """Recursively assign ZZ slots, flattening all depths."""
        for child in children:
            slug = slug_from_path(child["md_path"])
            if slug in self.slug_to_new:
                self.assignments.append(
                    (child, self.slug_to_new[slug], True)
                )
                continue
            zz[0] += 1
            self._assign(child, xx, yy, zz[0])
            # Recurse deeper descendants into the same ZZ space
            self._walk_zz(child.get("children", []), xx, yy, zz)

    # ── main walk ─────────────────────────────────────────────

    def process_entries(self, entries: list) -> None:
        for entry in entries:
            md_path = entry.get("md_path", "")
            if not md_path:
                continue

            slug = slug_from_path(md_path)
            if slug in self.slug_to_new:
                self.assignments.append(
                    (entry, self.slug_to_new[slug], True)
                )
                continue

            xx = os.path.basename(md_path)[:2]
            yy = self._next_yy(xx)
            self._assign(entry, xx, yy, 0)

            children = entry.get("children", [])
            if not children:
                continue

            if yy == 0:
                # ── Chapter root: children each get their own YY ──
                for child in children:
                    child_slug = slug_from_path(child["md_path"])
                    if child_slug in self.slug_to_new:
                        self.assignments.append(
                            (child, self.slug_to_new[child_slug], True)
                        )
                        continue
                    # Use PARENT's XX — fixes cross-section children
                    child_yy = self._next_yy(xx)
                    self._assign(child, xx, child_yy, 0)
                    # Grandchildren of chapter root → ZZ under this child
                    self._process_zz_children(
                        child.get("children", []), xx, child_yy
                    )
            else:
                # ── Non-root top-level entry: children get ZZ ─────
                self._process_zz_children(children, xx, yy)


# ═══════════════════════════════════════════════════════════════
# Steps
# ═══════════════════════════════════════════════════════════════

def step1_rename_files(ren: Renumberer) -> int:
    """Rename files on disk.  Finds misplaced files by slug if needed."""
    print("\n── Step 1: Renaming content files ──────────────────────────")
    all_files = _all_md_files()  # {basename: full_path}
    changed = 0
    for entry, new_path, is_dup in ren.assignments:
        if is_dup:
            continue
        new_fname = os.path.basename(new_path)
        # Destination is in the chapter subfolder
        new_dir = os.path.join(CONTENT_DIR, os.path.dirname(new_path).replace("content/", "", 1))
        os.makedirs(new_dir, exist_ok=True)
        dst = os.path.join(new_dir, new_fname)

        # Already correct on disk?
        if os.path.exists(dst):
            continue

        old_fname = os.path.basename(entry["md_path"])

        # Try finding by old filename
        if old_fname in all_files:
            src = all_files[old_fname]
            os.rename(src, dst)
            print(f"  [RENAME] {old_fname}  ->  {os.path.relpath(dst, CONTENT_DIR)}")
            changed += 1
        else:
            # File is somewhere on disk under a different number — find it by slug
            slug = slug_from_path(entry["md_path"])
            actual = find_by_slug(slug)
            if actual and actual in all_files:
                os.rename(all_files[actual], dst)
                print(f"  [FOUND]  {actual}  ->  {os.path.relpath(dst, CONTENT_DIR)}")
                ren.rename_map[actual] = new_fname  # for cross-link step
                changed += 1
            else:
                print(f"  [MISS]   {new_fname}  (no matching file on disk)")
    print(f"\n  {changed} files renamed.")
    return changed


def step2_update_events_json(ren: Renumberer, data: dict) -> None:
    """Set every entry's md_path to its canonical new path."""
    print("\n── Step 2: Updating data/events.json ───────────────────────")
    updated = 0
    for entry, new_path, _ in ren.assignments:
        if entry.get("md_path") != new_path:
            entry["md_path"] = new_path
            updated += 1
    # The entry dicts are the same objects inside `data`, so write it out
    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  {updated} md_path values updated.")


def step3_update_crosslinks(ren: Renumberer) -> None:
    """Rewrite markdown cross-links that reference renamed files."""
    print("\n── Step 3: Updating cross-links in content/**/*.md ─────────")
    # Build old_basename → new_basename map (both exact and prefix)
    fname_map: dict[str, str] = {}
    for old, new in ren.rename_map.items():
        if old != new:
            fname_map[old] = new

    if not fname_map:
        print("  Nothing to update.\n")
        return

    total_files = 0
    total_links = 0
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                text = f.read()

            new_text = text
            count = 0
            for old_ref, new_ref in fname_map.items():
                if old_ref in new_text:
                    n = new_text.count(old_ref)
                    new_text = new_text.replace(old_ref, new_ref)
                    count += n

            if new_text != text:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_text)
                rel = os.path.relpath(fpath, REPO_DIR)
                print(f"  [LINKS] {rel}  ({count} ref(s))")
                total_files += 1
                total_links += count
    print(f"\n  {total_links} link(s) in {total_files} file(s) updated.")


def step4_broken_links() -> None:
    print("\n── Step 4: Checking for broken links ───────────────────────")
    existing = set()
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith(".md"):
                existing.add(f)
    broken = []
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                text = f.read()
            rel = os.path.relpath(fpath, REPO_DIR)
            for m in re.finditer(
                r"(?:\.\/|\/content\/[^/]+\/|\/content\/)(\d{2}\.\d{2}\.\d{2}-[^)\s\"'\n]+\.md)",
                text,
            ):
                tgt = m.group(1)
                if tgt not in existing:
                    broken.append((rel, tgt))
    if broken:
        print(f"  [WARN] {len(broken)} broken link(s):")
        for src, tgt in broken:
            print(f"    {src}  →  {tgt}")
    else:
        print("  No broken links found.")


# ═══════════════════════════════════════════════════════════════

def main() -> None:
    print("=== Renumber content from events.json hierarchy (v3) ===\n")

    with open(EVENTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    ren = Renumberer()
    ren.process_entries(data["entries"])

    unique = [a for a in ren.assignments if not a[2]]
    dups = [a for a in ren.assignments if a[2]]
    changes = {k: v for k, v in ren.rename_map.items() if k != v}
    print(
        f"Assignments: {len(unique)} unique, {len(dups)} duplicates, "
        f"{len(changes)} to rename\n"
    )
    for old, new in sorted(changes.items()):
        print(f"  {old:65s}  ->  {new}")

    step1_rename_files(ren)
    step2_update_events_json(ren, data)
    step3_update_crosslinks(ren)
    step4_broken_links()

    print("\n=== Done. Run: ===")
    print(
        "  npm run validate-events && npm run audit-missing && npm run generate-index"
    )


if __name__ == "__main__":
    main()
