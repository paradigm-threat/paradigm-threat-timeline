#!/usr/bin/env python3
"""
Plain-text export for the timeline book: index (TOC) + full body, mirroring
generate-docx.py chapter order and TOC structure.

Writes:
  export/timeline-book-index.txt
  export/timeline-book-plain.txt
  export/timeline-appendix-index.txt   (if appendix files exist)
  export/timeline-appendix-plain.txt

Not run by export.sh. Optional: npm run generate-plaintext
Russian: scripts/export-russian-remote.sh (DOCX only).
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

try:
    from mdit_py_plugins.attrs import attrs_plugin
except ImportError:
    attrs_plugin = None

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent
CONTENT_DIR = REPO_DIR / "content"
EXPORT_DIR = REPO_DIR / "export"

_APPENDIX_PREFIXES = tuple(f"{i}." for i in range(16, 23))

_ROMAN = [
    "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
]

_NUM_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{2})")


def _partition_files(md_files: list[Path]):
    book, appendix = [], []
    for p in md_files:
        if p.name.startswith(_APPENDIX_PREFIXES):
            appendix.append(p)
        else:
            book.append(p)
    return book, appendix


def _classify_tier(filename: str):
    m = _NUM_RE.match(filename)
    if not m:
        return ("part", "00", "00", "00")
    xx, yy, zz = m.group(1), m.group(2), m.group(3)
    if yy == "00" and zz == "00":
        return ("part", xx, yy, zz)
    if zz == "00":
        return ("chapter", xx, yy, zz)
    return ("subsection", xx, yy, zz)


def _read_title(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return path.stem
    body = _strip_frontmatter(text)
    m = re.search(r"(?m)^#\s+(.+)$", body)
    return m.group(1).strip() if m else path.stem


def _strip_frontmatter(text: str) -> str:
    """Remove leading ``--- ... ---`` YAML block (same rules as PDF/DOCX export)."""
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[i + 1 :])
    return text


def _md_to_plain_html_strip(md_src: str, md: MarkdownIt) -> str:
    """Render markdown to HTML and strip tags — good enough for archival plain text."""
    src = _strip_frontmatter(md_src)
    h = md.render(src)
    h = re.sub(r"(?is)<script.*?</script>", "", h)
    h = re.sub(r"(?is)<style.*?</style>", "", h)
    h = re.sub(r"<br\s*/?>", "\n", h, flags=re.I)
    h = re.sub(r"</p\s*>", "\n\n", h, flags=re.I)
    h = re.sub(r"</h[1-6]\s*>", "\n\n", h, flags=re.I)
    h = re.sub(r"</tr\s*>", "\n", h, flags=re.I)
    h = re.sub(r"</t[dh]\s*>", "\t", h, flags=re.I)
    h = re.sub(r"<li\s*>", "\n• ", h, flags=re.I)
    h = re.sub(r"</li\s*>", "", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+\n", "\n", h)
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h.strip()


def build_index_text(md_files: list[Path]) -> str:
    """Plain-text TOC matching generate-docx.py _add_toc hierarchy."""
    lines = [
        "TABLE OF CONTENTS",
        "=" * 60,
        "",
    ]
    chapter_counter = 0

    for path in md_files:
        tier, xx, yy, zz = _classify_tier(path.name)
        title = _read_title(path)

        if tier == "part":
            roman = _ROMAN[int(xx)] if int(xx) < len(_ROMAN) else str(xx)
            display = f"Part {roman}: {title}"
            pm = re.match(
                r"^(\d{1,2}(?:st|nd|rd|th)\s+Century(?:\s+C\.E\.)?)"
                r"(?:\s*[.:\-—]\s*|\s+)(.+)$",
                title,
            )
            if pm:
                main_title = f"Part {roman}: {pm.group(1).strip().rstrip('.')}"
                subtitle = pm.group(2).strip().rstrip(".")
            else:
                main_title = display
                subtitle = ""

            lines.append(main_title)
            if subtitle:
                lines.append(f"    {subtitle}")
            lines.append("")

        elif tier == "chapter":
            chapter_counter += 1
            lines.append(f"  Chapter {chapter_counter}: {title}")
            lines.append("")

        elif tier == "subsection":
            lines.append(f"      {title}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_volume(
    md_files: list[Path],
    slug: str,
    header_title: str,
    md: MarkdownIt,
) -> None:
    EXPORT_DIR.mkdir(exist_ok=True)
    index_path = EXPORT_DIR / f"{slug}-index.txt"
    plain_path = EXPORT_DIR / f"{slug}-plain.txt"

    index_path.write_text(build_index_text(md_files), encoding="utf-8")

    with open(REPO_DIR / "package.json", encoding="utf-8") as f:
        pkg_version = json.load(f)["version"]

    body_parts = [
        header_title,
        f"Version {pkg_version}",
        "",
        "=" * 72,
        "",
    ]

    for i, p in enumerate(md_files):
        print(f"  [{i + 1:3d}/{len(md_files)}] {p.name} -> plain")
        raw = p.read_text(encoding="utf-8")
        body_parts.append("\n" + "=" * 72)
        body_parts.append(p.name)
        body_parts.append("=" * 72 + "\n")
        body_parts.append(_md_to_plain_html_strip(raw, md))
        body_parts.append("")

    plain_path.write_text("\n".join(body_parts), encoding="utf-8")

    print(f"Wrote {index_path.relative_to(REPO_DIR)} ({index_path.stat().st_size // 1024} KB)")
    print(f"Wrote {plain_path.relative_to(REPO_DIR)} ({plain_path.stat().st_size // 1024} KB)")


def main() -> None:
    md = MarkdownIt("commonmark", {"typographer": False}).enable("table")
    if attrs_plugin:
        md.use(attrs_plugin)

    all_files = sorted(CONTENT_DIR.rglob("*.md"))
    book_files, appendix_files = _partition_files(all_files)

    if not book_files:
        sys.exit("No book markdown files in content/")

    print("\n=== Plain-text index + body (book) ===")
    write_volume(
        book_files,
        "timeline-book",
        "PARADIGM THREAT: THE THIRD STORY (plain text)",
        md,
    )

    if appendix_files:
        print("\n=== Plain-text index + body (appendix) ===")
        write_volume(
            appendix_files,
            "timeline-appendix",
            "PARADIGM THREAT: APPENDIX & REFERENCES (plain text)",
            md,
        )
    else:
        print("\n(No appendix markdown — skipping appendix plain text.)")


if __name__ == "__main__":
    main()
