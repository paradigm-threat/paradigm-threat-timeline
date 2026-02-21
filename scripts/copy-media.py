#!/usr/bin/env python3
"""
Copy images from paradigm-threat-files into media/ organized by era folder,
and rewrite markdown image references to use relative local paths.

Usage:
    python3 scripts/copy-media.py [--dry-run]
"""
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

REPO_ROOT = Path(__file__).resolve().parent.parent
FILES_ROOT = REPO_ROOT.parent / "paradigm-threat-files"
MEDIA_ROOT = REPO_ROOT / "media"

CDN_PREFIX = "https://clevertree.github.io/paradigm-threat-files/"

# Regex to match image markdown with the CDN URL
# Captures: ![alt](url) — we need to replace the URL part
IMAGE_RE = re.compile(
    r'(!\[[^\]]*\]\()'                         # ![alt](
    r'(https://clevertree\.github\.io/paradigm-threat-files/[^)\s]+)'  # url
    r'(\))'                                     # )
)

# Map markdown source directories/files to their media era folder
# Articles map by their parent directory name
ARTICLE_DIR_TO_ERA = {
    "overview": "overview",
    "project-objective": "project-objective",
    "before-creation": "before-creation",
    "the-golden-age": "the-golden-age",
    "the-dark-ages": "the-dark-ages",
    "11th-century-ce-common-era-begins": "11th-century-ce-common-era-begins",
    "12th-century-ce-birth-of-christianity": "12th-century-ce-birth-of-christianity",
    "13th-century-ce-the-russian-horde-tartarian-empire": "13th-century-ce-the-russian-horde-tartarian-empire",
    "14th-century-ce-great-expansion-of-the-mongol-slav": "14th-century-ce-great-expansion-of-the-mongol-slav",
    "15th-century-ce-ottoman-conquest-of-europe": "15th-century-ce-ottoman-conquest-of-europe",
    "16th-century-ce-reformation-and-inquisition": "16th-century-ce-reformation-and-inquisition",
    "17th-century-romanovs-rise-to-power": "17th-century-romanovs-rise-to-power",
    "saturnian-cosmology-timeline-video": "project-objective",
}

# Map event file prefixes to era folders
# Key: (start_year, end_year) ranges — we match by filename prefix
EVENT_PREFIX_TO_ERA = [
    # (filename_prefix_pattern, era_folder)
    (r"^bce-5000", "before-creation"),
    (r"^bce-4077", "the-golden-age"),
    (r"^bce-3\d{3}", "the-dark-ages"),
    (r"^bce-2\d{3}", "the-dark-ages"),
    (r"^bce-1\d{3}", "the-dark-ages"),
    (r"^bce-80[0-9]", "the-dark-ages"),
    (r"^bce-68[4-6]", "the-dark-ages"),
    (r"^bce-670", "the-blip"),
    (r"^ce-10[0-5]\d", "11th-century-ce-common-era-begins"),
    (r"^ce-1[1]\d{2}", "12th-century-ce-birth-of-christianity"),
    (r"^ce-12\d{2}", "13th-century-ce-the-russian-horde-tartarian-empire"),
    (r"^ce-13\d{2}", "14th-century-ce-great-expansion-of-the-mongol-slav"),
    (r"^ce-14\d{2}", "15th-century-ce-ottoman-conquest-of-europe"),
    (r"^ce-15\d{2}", "16th-century-ce-reformation-and-inquisition"),
    (r"^ce-16\d{2}", "17th-century-romanovs-rise-to-power"),
    (r"^ce-17\d{2}", "18th-century-ce-mudflood-and-pugachev"),
    (r"^ce-18\d{2}", "18th-century-ce-mudflood-and-pugachev"),
    (r"^ce-30", "17th-century-romanovs-rise-to-power"),  # ce-300 Russia/Turkey
]


def get_era_for_md_file(md_path: Path) -> str:
    """Determine era folder for a markdown file."""
    rel = md_path.relative_to(REPO_ROOT)
    parts = rel.parts

    # articles/{era-dir}/filename.md
    if parts[0] == "articles" and len(parts) >= 3:
        era_dir = parts[1]
        if era_dir in ARTICLE_DIR_TO_ERA:
            return ARTICLE_DIR_TO_ERA[era_dir]
        # Fallback: use the directory name directly
        return era_dir

    # events/bce-YYYY-slug.md or events/ce-YYYY-slug.md
    if parts[0] == "events":
        filename = parts[1]
        for pattern, era in EVENT_PREFIX_TO_ERA:
            if re.match(pattern, filename):
                return era

    # Fallback
    print(f"  WARNING: No era mapping for {rel}, using 'overview'")
    return "overview"


def strip_query_params(url: str) -> str:
    """Remove ?w=384 and similar query params from URL."""
    return url.split("?")[0]


def url_to_local_source(url: str) -> Path | None:
    """Convert CDN URL to local paradigm-threat-files path."""
    clean = strip_query_params(url)
    if not clean.startswith(CDN_PREFIX):
        return None
    rel_path = clean[len(CDN_PREFIX):]
    local = FILES_ROOT / rel_path
    if local.is_file():
        return local
    return None


def copy_and_rewrite(dry_run: bool = False):
    """Main: scan all md files, copy images, rewrite links."""
    md_files = []
    for d in ["events", "articles"]:
        root = REPO_ROOT / d
        if root.exists():
            md_files.extend(root.rglob("*.md"))

    copied = {}   # old_url -> new_media_path (relative to REPO_ROOT)
    errors = []
    rewrites = 0
    files_modified = 0

    # First pass: discover all images and copy them
    print("=== Pass 1: Discovering and copying images ===\n")
    for md_file in sorted(md_files):
        content = md_file.read_text(encoding="utf-8")
        matches = IMAGE_RE.findall(content)
        if not matches:
            continue

        era = get_era_for_md_file(md_file)
        rel_md = md_file.relative_to(REPO_ROOT)

        for _, url, _ in matches:
            clean_url = strip_query_params(url)
            if clean_url in copied:
                continue  # Already handled

            source = url_to_local_source(url)
            if source is None:
                errors.append((rel_md, url, "Source file not found"))
                continue

            filename = source.name
            dest = MEDIA_ROOT / era / filename

            # Handle filename collisions within same era
            if dest.exists() and dest.resolve() != source.resolve():
                base = dest.stem
                ext = dest.suffix
                i = 2
                while dest.exists():
                    dest = MEDIA_ROOT / era / f"{base}_{i}{ext}"
                    i += 1

            print(f"  COPY {source.relative_to(FILES_ROOT)} -> media/{era}/{dest.name}")
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)

            copied[clean_url] = dest.relative_to(REPO_ROOT)
            # Also map the version with query params
            if url != clean_url:
                copied[url] = dest.relative_to(REPO_ROOT)

    print(f"\n  Copied {len(copied)} unique images\n")

    # Second pass: rewrite markdown references
    print("=== Pass 2: Rewriting markdown image links ===\n")
    for md_file in sorted(md_files):
        content = md_file.read_text(encoding="utf-8")
        if CDN_PREFIX not in content:
            continue

        original = content
        rel_md = md_file.relative_to(REPO_ROOT)
        md_dir = md_file.parent

        def replace_image(m):
            nonlocal rewrites
            prefix = m.group(1)   # ![alt](
            url = m.group(2)      # full URL
            suffix = m.group(3)   # )

            clean_url = strip_query_params(url)
            media_rel = copied.get(clean_url) or copied.get(url)
            if media_rel is None:
                return m.group(0)  # Leave unchanged if not copied

            # Compute relative path from the markdown file to the media file
            media_abs = REPO_ROOT / media_rel
            try:
                rel_path = os.path.relpath(media_abs, md_dir)
            except ValueError:
                rel_path = str(media_rel)

            rewrites += 1
            return f"{prefix}{rel_path}{suffix}"

        new_content = IMAGE_RE.sub(replace_image, content)

        if new_content != original:
            files_modified += 1
            print(f"  REWRITE {rel_md}")
            if not dry_run:
                md_file.write_text(new_content, encoding="utf-8")

    print(f"\n=== Summary ===")
    print(f"  Images copied: {len(copied)}")
    print(f"  Links rewritten: {rewrites}")
    print(f"  Files modified: {files_modified}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for md, url, reason in errors:
            print(f"    {md}: {url} — {reason}")

    return len(errors) == 0


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN — no files will be modified\n")
    success = copy_and_rewrite(dry_run=dry_run)
    sys.exit(0 if success else 1)
