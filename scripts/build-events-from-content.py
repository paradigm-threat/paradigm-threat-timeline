#!/usr/bin/env python3
"""
Build data/events.json from content/ file structure.

Source of truth: content/ folder. One entry per file.
- Hierarchy from XX.YY.ZZ in filename
- Dates from filename slug when present (YYYY-YYYY, YYYY-bce, YYYY-ce)
- Optional fields (media, related_events, id, etc.) from YAML frontmatter.
  Use `id: evt-...` to keep stable timeline URLs when the filename slug no longer includes the year.
- Dates use one signed-year line (negative = BCE, positive = CE). Optional YAML `calendar` is legacy;
  if omitted, it is inferred. Spans crossing year 0 are stored as calendar "mixed".
"""
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
CONTENT_DIR = os.path.join(REPO_DIR, "content")
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

# Regex for XX.YY.ZZ-slug.md
NUM_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})-(.+?)\.md$")

# Date extraction patterns (order matters)
DATE_PATTERNS = [
    # YYYY-YYYY (range, assume CE)
    (re.compile(r"(\d{4})-(\d{4})"), lambda m: {"start": int(m.group(1)), "end": int(m.group(2)), "calendar": "CE"}),
    # YYYY-bce
    (re.compile(r"(\d{4})-bce", re.I), lambda m: {"start": -int(m.group(1)), "end": -int(m.group(1)), "calendar": "BCE"}),
    # YYYY-ce
    (re.compile(r"(\d{4})-ce", re.I), lambda m: {"start": int(m.group(1)), "end": int(m.group(1)), "calendar": "CE"}),
    # Standalone YYYY (before -ce or -bce or end) - e.g. 1100 in "1100-ce-12th-century"
    (re.compile(r"(?<![-\d])(\d{4})(?=-ce|-bce|-)"), lambda m: {"start": int(m.group(1)), "end": int(m.group(1)), "calendar": "CE"}),
]


def extract_dates_from_slug(slug: str) -> tuple[list | None, str | None]:
    """Extract dates from filename slug. Returns (dates_array, error_message).
    If valid dates found, error_message is None. If invalid (e.g. end < start), returns error."""
    for pat, fn in DATE_PATTERNS:
        m = pat.search(slug)
        if m:
            d = fn(m)
            start = d.get("start")
            end = d.get("end", start)
            if start is not None and (start < MIN_YEAR or start > MAX_YEAR):
                return None, f"year {start} out of range [{MIN_YEAR}, {MAX_YEAR}]"
            if end is not None and (end < MIN_YEAR or end > MAX_YEAR):
                return None, f"year {end} out of range [{MIN_YEAR}, {MAX_YEAR}]"
            if start is not None and end is not None and start > end:
                return None, f"invalid date range: start {start} > end {end}"
            return [d], None
    return None, None


def slug_to_id(slug: str) -> str:
    """Convert slug to evt- id. Slug is part after XX.YY.ZZ- in filename."""
    return "evt-" + slug


def get_first_header(md_path: str) -> str | None:
    """Extract first # header from markdown file, skipping YAML frontmatter."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return None
    in_frontmatter = False
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "---":
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return None


# Regex to extract image paths from markdown: ![alt](path) or ![alt](path "title")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s\"]+)(?:\s+\"[^\"]*\")?\)")
# HTML img tags
HTML_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)


def extract_images_from_markdown(md_path: str) -> list[str]:
    """Extract image paths from markdown content. Returns list of paths for events.json media.
    Paths are normalized to start with / for correct URL resolution against baseUrl."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return []
    seen: set[str] = set()
    result: list[str] = []
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []
    for pat in (MD_IMG_RE, HTML_IMG_RE):
        for m in pat.finditer(content):
            raw = m.group(1).strip()
            if not raw or raw.startswith("data:") or raw.startswith("#"):
                continue
            # Normalize: ensure path starts with / for baseUrl + path URL construction
            p = raw if raw.startswith("/") else "/" + raw
            if p not in seen:
                seen.add(p)
                result.append(p)
    return result


def parse_frontmatter(md_path: str) -> dict:
    """Parse first YAML frontmatter block from markdown file."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path) or not yaml:
        return {}
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip().startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 2:
            return {}
        fm = yaml.safe_load(parts[1])
        return fm if isinstance(fm, dict) else {}
    except Exception:
        return {}


# Reasonable year bounds for validation
MIN_YEAR = -10000
MAX_YEAR = 3000


def discover_content_files() -> tuple[list[tuple[str, int, int, int, str]], list[str]]:
    """Walk content/, return ([(md_path, xx, yy, zz, slug), ...], orphan_paths).
    Orphan = .md file that does not match XX.YY.ZZ-slug.md pattern."""
    result = []
    orphans = []
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            full_path = os.path.join(root, f)
            md_path = os.path.relpath(full_path, REPO_DIR).replace("\\", "/")
            m = NUM_RE.match(f)
            if not m:
                orphans.append(md_path)
                continue
            xx, yy, zz = int(m.group(1)), int(m.group(2)), int(m.group(3))
            slug = m.group(4)
            result.append((md_path, xx, yy, zz, slug))
    result.sort(key=lambda t: (t[1], t[2], t[3]))
    return result, orphans


def build_entry(md_path: str, xx: int, yy: int, zz: int, slug: str) -> tuple[dict, str | None]:
    """Build a single entry dict. Returns (entry, error_message)."""
    title = get_first_header(md_path)
    if not title or not title.strip():
        return None, f"{md_path}: missing first # header"

    fm = parse_frontmatter(md_path)
    id_override = fm.get("id") if isinstance(fm.get("id"), str) else None
    if id_override and id_override.strip():
        evt_id = id_override.strip()
        if not evt_id.startswith("evt-"):
            return None, f"{md_path}: frontmatter id must start with evt-"
    else:
        evt_id = slug_to_id(slug)
    dates, date_err = extract_dates_from_slug(slug)
    if date_err:
        return None, f"{md_path}: {date_err}"

    # Allow frontmatter "dates" to override slug dates or supply when slug has none
    if fm.get("dates") and isinstance(fm["dates"], list) and len(fm["dates"]) > 0:
        d0 = fm["dates"][0]
        if isinstance(d0, dict):
            start = d0.get("start") if d0.get("start") is not None else d0.get("value")
            end = d0.get("end") if d0.get("end") is not None else start
            if start is not None:
                if start < MIN_YEAR or start > MAX_YEAR:
                    return None, f"{md_path}: frontmatter year {start} out of range [{MIN_YEAR}, {MAX_YEAR}]"
                if end is not None and (end < MIN_YEAR or end > MAX_YEAR):
                    return None, f"{md_path}: frontmatter end year {end} out of range [{MIN_YEAR}, {MAX_YEAR}]"
                if end is not None and start > end:
                    return None, f"{md_path}: frontmatter invalid date range: start {start} > end {end}"
                if d0.get("calendar") is not None and str(d0.get("calendar")).strip() != "":
                    cal = str(d0["calendar"]).strip()
                elif end is not None and start < 0 < end:
                    cal = "mixed"
                else:
                    cal = "BCE" if start < 0 else "CE"
                dates = [{"start": start, "end": end or start, "calendar": cal}]
            elif end is not None:
                # Open lower bound (e.g. Before Creation): display as ∞ … end in UI
                if end < MIN_YEAR or end > MAX_YEAR:
                    return None, f"{md_path}: frontmatter end year {end} out of range [{MIN_YEAR}, {MAX_YEAR}]"
                cal = d0.get("calendar", "BCE" if end < 0 else "CE")
                start_label = d0.get("start_label")
                if start_label is None or start_label == "":
                    start_label = "∞"
                dates = [
                    {
                        "start": None,
                        "end": end,
                        "calendar": cal,
                        "start_label": start_label,
                    }
                ]

    entry = {
        "id": evt_id,
        "title": title,
        "type": "event" if dates else "article",
        "md_path": md_path,
        "children": [],
    }
    if dates:
        entry["dates"] = dates

    for key in ("related_events", "duplicate_of", "tags", "timeline_sources", "context", "categories"):
        if key in fm and fm[key] is not None:
            entry[key] = fm[key]
    # media: use frontmatter if present, otherwise extract from markdown (for TTS slideshow / auto-playback)
    if "media" in fm and fm["media"] is not None:
        entry["media"] = [str(p) if isinstance(p, str) else str(p.get("path", p)) for p in fm["media"]]
    else:
        extracted = extract_images_from_markdown(md_path)
        if extracted:
            entry["media"] = extracted

    return entry, None


def build_tree(files: list) -> tuple[list, list, list[str]]:
    """
    Build entries tree from sorted file list.
    Returns (entries, introArticles, errors).
    """
    errors: list[str] = []
    by_key: dict[tuple[int, int, int], list[dict]] = {}

    for md_path, xx, yy, zz, slug in files:
        entry, err = build_entry(md_path, xx, yy, zz, slug)
        if err:
            errors.append(err)
            continue
        key = (xx, yy, zz)
        if key in by_key:
            errors.append(
                f"Duplicate XX.YY.ZZ {xx:02d}.{yy:02d}.{zz:02d}: {by_key[key][0]['md_path']} and {md_path}"
            )
            continue
        by_key[key] = [entry]

    # Map (xx,) -> root entry; (xx, yy) -> last XX.YY.00 entry for attaching ZZ children
    root_by_xx: dict[int, dict] = {}
    yy00_by_xx_yy: dict[tuple[int, int], dict] = {}

    roots = []
    intro_articles = []
    sorted_keys = sorted(by_key.keys(), key=lambda k: (k[0], k[1], k[2]))

    for (xx, yy, zz) in sorted_keys:
        entries = by_key[(xx, yy, zz)]
        for entry in entries:
            if yy == 0 and zz == 0:
                root_by_xx[xx] = entry
                yy00_by_xx_yy[(xx, 0)] = entry
                roots.append(entry)
            elif zz == 0:
                root = root_by_xx.get(xx)
                if root:
                    root["children"].append(entry)
                yy00_by_xx_yy[(xx, yy)] = entry
            else:
                parent = yy00_by_xx_yy.get((xx, yy))
                if parent:
                    parent["children"].append(entry)
                else:
                    root = root_by_xx.get(xx)
                    if root:
                        root["children"].append(entry)

    # introArticles: all overview (xx=0) entries, DFS
    if 0 in root_by_xx:
        def collect_intro(node):
            intro_articles.append({"id": node["id"], "title": node["title"], "md_path": node["md_path"]})
            for c in node.get("children", []):
                collect_intro(c)
        collect_intro(root_by_xx[0])

    return roots, intro_articles, errors


def collect_ids(nodes: list) -> list[str]:
    """Recursively collect all entry ids."""
    ids = []
    for n in nodes:
        if "id" in n:
            ids.append(n["id"])
        ids.extend(collect_ids(n.get("children", [])))
    return ids


def main() -> int:
    if not os.path.isdir(CONTENT_DIR):
        print(f"Error: content dir not found: {CONTENT_DIR}", file=sys.stderr)
        return 1

    files, orphans = discover_content_files()

    if orphans:
        print("Error: orphan .md files (must match XX.YY.ZZ-slug.md):", file=sys.stderr)
        for p in sorted(orphans):
            print(f"  - {p}", file=sys.stderr)
        return 1

    if not files:
        print("Error: no content files found", file=sys.stderr)
        return 1

    entries, intro_articles, errors = build_tree(files)
    if errors:
        print("Error: validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    # Duplicate id check
    all_ids = collect_ids(entries)
    seen: dict[str, list[str]] = {}
    for i, eid in enumerate(all_ids):
        seen.setdefault(eid, []).append(str(i))
    dupes = [(eid, paths) for eid, paths in seen.items() if len(paths) > 1]
    if dupes:
        print("Error: duplicate entry ids:", file=sys.stderr)
        for eid, _ in dupes:
            print(f"  - {eid}", file=sys.stderr)
        return 1

    out = {
        "entries": entries,
        "introArticles": intro_articles,
        "meta": {"source": "build-events-from-content.py"},
    }

    os.makedirs(os.path.dirname(EVENTS_JSON), exist_ok=True)
    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    def count(nodes):
        return sum(1 + count(n.get("children", [])) for n in nodes)

    print(f"Built events.json: {count(entries)} entries, {len(intro_articles)} introArticles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
