#!/usr/bin/env python3
"""
Build the timeline event catalog from content/ (in memory).

Source of truth: content/ folder. One entry per file.
Relay indexes via content_events — this script validates / dumps JSON to stdout (--json).
- Hierarchy from XX.YY.ZZ in filename
- Dates from filename slug when present (YYYY-YYYY, YYYY-bce, YYYY-ce)
- Optional fields (media, related_events, id, etc.) from YAML frontmatter.
  Auto-extracted media uses {\"path\": \"...\"} or {\"path\": \"...\", \"bookIllustration\": true}
  when the markdown image has {.book-illustration} (skipped in site TTS fullscreen slideshow).
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


# Markdown images: optional Pandoc block after ) e.g. {.book-illustration}
MD_IMG_RE = re.compile(
    r"!\[[^\]]*\]\(([^)\s\"]+)(?:\s+\"[^\"]*\")?\)(\s*\{[^}]+\})?"
)
# HTML img tags
HTML_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)

BOOK_ILLUSTRATION_IN_ATTRS = re.compile(r"\.book-illustration\b")

# Trailing "Keywords: #tag #tag" line (from append_article_keywords.py)
KEYWORDS_LINE_RE = re.compile(r"^Keywords:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


def extract_keywords_from_markdown(md_path: str) -> list[str]:
    """Parse hashtag tokens from a Keywords: line at end of markdown. Returns lowercase-ish tokens without #."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return []
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return []
    m = KEYWORDS_LINE_RE.search(content)
    if not m:
        return []
    return re.findall(r"#([a-zA-Z0-9\-]+)", m.group(1))


def _attr_block_marks_book_illustration(block: str | None) -> bool:
    if not block or not str(block).strip():
        return False
    s = str(block).strip()
    if len(s) < 3 or not (s.startswith("{") and s.endswith("}")):
        return False
    return bool(BOOK_ILLUSTRATION_IN_ATTRS.search(s[1:-1]))


def _normalize_media_path(raw: str) -> str:
    raw = raw.strip()
    if not raw or raw.startswith("data:") or raw.startswith("#"):
        return ""
    return raw if raw.startswith("/") else "/" + raw


def _media_item_dict(path: str, book_illustration: bool) -> dict:
    """events.json media[] item: {path} or {path, bookIllustration: true}."""
    p = _normalize_media_path(path)
    if not p:
        return {}
    if book_illustration:
        return {"path": p, "bookIllustration": True}
    return {"path": p}


def normalize_media_from_frontmatter(fm_media: list) -> list[dict]:
    """Convert YAML media list to events.json objects (path + optional bookIllustration)."""
    out: list[dict] = []
    for p in fm_media:
        if isinstance(p, str):
            item = _media_item_dict(p, False)
            if item:
                out.append(item)
        elif isinstance(p, dict):
            path = p.get("path") or p.get("src")
            if path is None:
                continue
            book = bool(p.get("bookIllustration") or p.get("book_illustration"))
            item = _media_item_dict(str(path), book)
            if item:
                out.append(item)
    return out


def extract_images_from_markdown(md_path: str) -> list[dict]:
    """Extract image entries from markdown for events.json media[].
    Each item is {\"path\": \"/...\"} or {\"path\": \"...\", \"bookIllustration\": true}
    when the image line ends with {.book-illustration} (Pandoc class syntax)."""
    full_path = os.path.join(REPO_DIR, md_path)
    if not os.path.exists(full_path):
        return []
    order: list[str] = []
    flags: dict[str, bool] = {}
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    for m in MD_IMG_RE.finditer(content):
        raw = m.group(1).strip()
        book = _attr_block_marks_book_illustration(m.group(2))
        p = _normalize_media_path(raw)
        if not p:
            continue
        if p not in flags:
            order.append(p)
            flags[p] = book
        else:
            flags[p] = flags[p] or book

    for m in HTML_IMG_RE.finditer(content):
        raw = m.group(1).strip()
        p = _normalize_media_path(raw)
        if not p:
            continue
        if p not in flags:
            order.append(p)
            flags[p] = False

    return [_media_item_dict(p, flags[p]) for p in order]


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
                if d0.get("display_year") is not None:
                    dates[0]["display_year"] = d0["display_year"]
                if d0.get("note") is not None:
                    dates[0]["note"] = d0["note"]
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
    # media: use frontmatter if present, otherwise extract from markdown (for TTS slideshow / auto-playback).
    # Items are {path} or {path, bookIllustration: true}; TTS slideshow skips book-only-print figures.
    if "media" in fm and fm["media"] is not None and isinstance(fm["media"], list):
        norm = normalize_media_from_frontmatter(fm["media"])
        if norm:
            entry["media"] = norm
    else:
        extracted = extract_images_from_markdown(md_path)
        if extracted:
            entry["media"] = extracted

    kws = extract_keywords_from_markdown(md_path)
    if kws:
        entry["keywords"] = kws

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


def count_entries(nodes: list) -> int:
    return sum(1 + count_entries(n.get("children", [])) for n in nodes)


def build_events_data() -> tuple[dict | None, list[str]]:
    """Build the events catalog from content/ (parity with gateway content_events).

    Returns (payload, errors). Payload is None when errors is non-empty.
    Does not write data/events.json — Relay indexes content/ on the server.
    """
    errors: list[str] = []
    if not os.path.isdir(CONTENT_DIR):
        return None, [f"content dir not found: {CONTENT_DIR}"]

    files, orphans = discover_content_files()
    if orphans:
        errors.extend(
            f"orphan .md file (must match XX.YY.ZZ-slug.md): {p}" for p in sorted(orphans)
        )
    if not files and not orphans:
        return None, ["no content files found"]
    if errors:
        return None, errors

    entries, intro_articles, tree_errors = build_tree(files)
    if tree_errors:
        return None, tree_errors

    all_ids = collect_ids(entries)
    seen: dict[str, list[str]] = {}
    for i, eid in enumerate(all_ids):
        seen.setdefault(eid, []).append(str(i))
    for eid, paths in seen.items():
        if len(paths) > 1:
            errors.append(f"duplicate entry id: {eid}")
    if errors:
        return None, errors

    return {
        "entries": entries,
        "introArticles": intro_articles,
        "meta": {"source": "build_events_from_content.py"},
    }, []


def main() -> int:
    """Validate content/ → event graph (no JSON write). Optional --json dumps to stdout."""
    out, errors = build_events_data()
    if errors:
        print("Error: validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    assert out is not None
    if "--json" in sys.argv:
        json.dump(out, sys.stdout, separators=(",", ":"), ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(
            f"Validated content events: {count_entries(out['entries'])} entries, "
            f"{len(out.get('introArticles') or [])} introArticles"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
