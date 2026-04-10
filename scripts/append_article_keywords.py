#!/usr/bin/env python3
"""
Append a trailing Keywords line (hashtag form) to markdown articles.

Each tag is Instagram-safe: letters, digits, underscores only (hyphens are stripped
when emitting; Instagram treats a hyphen inside a hashtag as ending the tag).

Format (avoids ATX headings: line does not start with #):
  ---
  Keywords: #one #two

For page.md hubs that end with "## Folder contents" + AutoIndex, inserts
that block *before* the "---" that precedes "## Folder contents".

Idempotent: skips files that already contain a line matching ^Keywords:\\s

Usage (default is dry-run; pass --apply to write):
  python3 scripts/append_article_keywords.py --timeline-root DIR --files-root DIR
  python3 scripts/append_article_keywords.py --apply --timeline-root DIR --files-root DIR

Omit --files-root or --timeline-root to skip that repo.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Iterable

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OVERRIDES = os.path.join(SCRIPT_DIR, "article_keyword_overrides.json")

TIMELINE_FILENAME_PREFIX = re.compile(r"^\d{2}\.\d{2}\.\d{2}-")
FOLDER_CONTENTS_BLOCK = re.compile(r"\n---\s*\n\n## Folder contents\r?\n", re.MULTILINE)
HAS_KEYWORDS_LINE = re.compile(r"^Keywords:\s", re.MULTILINE)

STOPWORDS = frozenset(
    """
    the and for with from that this were was are has had have been being
    into than then them their they these those there here when what which
    while where who whom whose why how all any both each few more most other
    some such same only own same such too very can could should would may might
    must shall will just also not but or nor if as of at by on in to up an a
    ce bce century centuries year years age era about above after again against
    among around because before below between beyond during under until
    through throughout toward towards within without
    open closed status conclusion purpose related see note tl dr
    investigation investigations speculative speculation chronology timeline
    file files page index overview introduction appendix
    never much still until realized lies cared studying human history
    realized take testimony literal description actual would looked
    this section contains scratch notes worked being
    what is theory are not earth north pole ruins
    if we of as it all
    """.split()
)


def load_overrides(path: str) -> dict[str, list[str]]:
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        out: dict[str, list[str]] = {}
        for k, v in data.items():
            if isinstance(v, list) and all(isinstance(x, str) for x in v):
                out[str(k).replace("\\", "/")] = [x.strip().lower() for x in v if x.strip()]
        return out
    except (OSError, json.JSONDecodeError):
        return {}


def strip_frontmatter_lines(lines: list[str]) -> int:
    """Return index of first line after closing --- of YAML frontmatter, or 0."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def extract_heading_text(md: str) -> str:
    lines = md.splitlines()
    i = strip_frontmatter_lines(lines)
    for j in range(i, len(lines)):
        s = lines[j].strip()
        if s.startswith("# "):
            return s[2:].strip()
        if s.startswith("## "):
            return s[3:].strip()
    return ""


def clean_md_text(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[*_`]+", "", s)
    return s


def tokenize_words(text: str) -> list[str]:
    text = clean_md_text(text).lower()
    return re.findall(r"[a-z][a-z0-9\-]{1,}", text)


def normalize_tag(raw: str) -> str | None:
    t = raw.strip().lower()
    t = re.sub(r"[^a-z0-9\-]+", "-", t)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    if len(t) < 2 or t in STOPWORDS:
        return None
    if t.isdigit() and len(t) != 4:
        return None
    return t


def slug_keyword_candidates(basename: str, timeline_style: bool) -> list[str]:
    name = basename
    if name.endswith(".md"):
        name = name[:-3]
    if timeline_style and TIMELINE_FILENAME_PREFIX.match(name):
        name = name[9:]
    parts = name.split("-")
    out: list[str] = []
    for p in parts:
        t = normalize_tag(p)
        if t:
            out.append(t)
    return out


def build_keyword_list(
    rel_path: str,
    basename: str,
    md: str,
    timeline_style: bool,
    overrides: dict[str, list[str]],
    max_keywords: int,
) -> list[str]:
    key = rel_path.replace("\\", "/")
    if key in overrides and overrides[key]:
        tags = []
        for w in overrides[key]:
            n = normalize_tag(w) or w.lower().replace(" ", "-")
            if n and n not in tags:
                tags.append(n)
        return tags[:max_keywords]

    seen: set[str] = set()
    ordered: list[str] = []

    def add_many(items: Iterable[str]) -> None:
        for raw in items:
            t = normalize_tag(raw)
            if not t or t in seen:
                continue
            seen.add(t)
            ordered.append(t)
            if len(ordered) >= max_keywords:
                break

    add_many(slug_keyword_candidates(basename, timeline_style))
    if len(ordered) < max_keywords:
        title = extract_heading_text(md)
        add_many(tokenize_words(title))
    return ordered[:max_keywords]


def format_keywords_line(tags: list[str]) -> str:
    if not tags:
        return "Keywords: #article"
    parts = [f"#{t.replace('-', '')}" for t in tags]
    return "Keywords: " + " ".join(parts)


def insert_keywords_block(content: str, keywords_line: str) -> str:
    if HAS_KEYWORDS_LINE.search(content):
        return content
    block = f"\n\n---\n\n{keywords_line}\n"
    last = None
    for m in FOLDER_CONTENTS_BLOCK.finditer(content):
        last = m
    if last is not None:
        return content[: last.start()] + block + content[last.start() :]
    return content.rstrip() + block + "\n"


def should_skip_dir(rel_parts: tuple[str, ...], skip_names: set[str]) -> bool:
    if any(p.startswith(".") for p in rel_parts):
        return True
    for prefix in skip_names:
        if prefix and len(rel_parts) >= 1 and rel_parts[0] == prefix:
            return True
    return False


def iter_timeline_md(repo_root: str) -> Iterable[tuple[str, str]]:
    for sub in ("content", "content-editions"):
        base = os.path.join(repo_root, sub)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            rel_parts = tuple(
                os.path.relpath(dirpath, repo_root).replace("\\", "/").split("/")
            )
            if rel_parts == (".",):
                rel_parts = ()
            if should_skip_dir(rel_parts, frozenset()):
                continue
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for fn in filenames:
                if not fn.endswith(".md"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, repo_root).replace("\\", "/")
                yield full, rel


def iter_files_repo_md(repo_root: str) -> Iterable[tuple[str, str]]:
    skip_roots = frozenset({"docs", ".github", "node_modules", ".venv"})
    for dirpath, dirnames, filenames in os.walk(repo_root):
        rel = os.path.relpath(dirpath, repo_root).replace("\\", "/")
        if rel == ".":
            rel_parts: tuple[str, ...] = ()
        else:
            rel_parts = tuple(rel.split("/"))
        if should_skip_dir(rel_parts, skip_roots):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in skip_roots]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(full, repo_root).replace("\\", "/")
            yield full, rel_path


def process_file(
    full_path: str,
    rel_path: str,
    *,
    timeline_style: bool,
    overrides: dict[str, list[str]],
    max_keywords: int,
    apply: bool,
) -> tuple[bool, str]:
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return False, f"read error {rel_path}: {e}"

    if HAS_KEYWORDS_LINE.search(content):
        return False, f"skip (already has Keywords): {rel_path}"

    basename = os.path.basename(full_path)
    tags = build_keyword_list(
        rel_path, basename, content, timeline_style, overrides, max_keywords
    )
    line = format_keywords_line(tags)
    new_content = insert_keywords_block(content, line)

    if new_content == content:
        return False, f"unchanged: {rel_path}"

    if apply:
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except OSError as e:
            return False, f"write error {rel_path}: {e}"
    return True, f"{'wrote' if apply else 'would write'} {rel_path}: {line}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write files (default is dry-run)")
    ap.add_argument("--timeline-root", type=str, default="", help="paradigm-threat-timeline repo root")
    ap.add_argument("--files-root", type=str, default="", help="paradigm-threat-files repo root")
    ap.add_argument("--overrides", type=str, default=DEFAULT_OVERRIDES, help="JSON map rel_path -> keyword list")
    ap.add_argument("--max-keywords", type=int, default=20)
    args = ap.parse_args()

    overrides = load_overrides(args.overrides)
    changed = 0
    errors: list[str] = []

    if args.timeline_root:
        root = os.path.abspath(args.timeline_root)
        if not os.path.isdir(root):
            print(f"Error: --timeline-root not a directory: {root}", file=sys.stderr)
            return 1
        for full, rel in iter_timeline_md(root):
            ok, msg = process_file(
                full,
                rel,
                timeline_style=True,
                overrides=overrides,
                max_keywords=args.max_keywords,
                apply=args.apply,
            )
            print(msg)
            if ok:
                changed += 1
            elif "error" in msg.lower():
                errors.append(msg)

    if args.files_root:
        root = os.path.abspath(args.files_root)
        if not os.path.isdir(root):
            print(f"Error: --files-root not a directory: {root}", file=sys.stderr)
            return 1
        for full, rel in iter_files_repo_md(root):
            ok, msg = process_file(
                full,
                rel,
                timeline_style=False,
                overrides=overrides,
                max_keywords=args.max_keywords,
                apply=args.apply,
            )
            print(msg)
            if ok:
                changed += 1
            elif "error" in msg.lower():
                errors.append(msg)

    if not args.timeline_root and not args.files_root:
        print("Nothing to do: pass --timeline-root and/or --files-root", file=sys.stderr)
        return 1

    mode = "apply" if args.apply else "dry-run"
    print(f"\n{mode}: {changed} files updated" + (f", {len(errors)} errors" if errors else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
