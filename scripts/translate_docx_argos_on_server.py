#!/usr/bin/env python3
"""
Translate an English .docx to Russian using Argos Translate in-process (no HTTP API).

Intended to run ON a relay host as user *relay*, with the LibreTranslate venv, e.g.:

  sudo -u relay /opt/libretranslate/venv/bin/python3 translate_docx_argos_on_server.py \\
    /path/to/timeline-book.docx /path/to/timeline-book-ru.docx

Requires the same en→ru models as LibreTranslate (--load-only en,ru). One-time:

  sudo -u relay /opt/libretranslate/venv/bin/pip install python-docx

Disconnect-safe: start this via nohup/tmux/systemd from your SSH session (see
run-docx-translate-on-atlanta3.sh).
"""

from __future__ import annotations

import argparse
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# DOCX structure (paragraphs + nested tables) — same rules as export_translate_util
# ---------------------------------------------------------------------------
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

_MAX_CHUNK = 4500
_URL_LINE = re.compile(r"^\s*https?://\S+\s*$")


def _iter_block_items(parent):
    if isinstance(parent, DocxDocument):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError(f"unsupported parent type: {type(parent)}")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def _collect_docx_paragraph_jobs(container, jobs: list) -> None:
    for block in _iter_block_items(container):
        if isinstance(block, Paragraph):
            txt = block.text
            if txt.strip():
                jobs.append((block, txt))
        elif isinstance(block, Table):
            seen_tc = set()
            for row in block.rows:
                for cell in row.cells:
                    tc_id = id(cell._tc)
                    if tc_id in seen_tc:
                        continue
                    seen_tc.add(tc_id)
                    _collect_docx_paragraph_jobs(cell, jobs)


def _hard_split(text: str, max_len: int) -> list[str]:
    if len(text) <= max_len:
        return [text]
    parts: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_len, n)
        if end < n:
            cut = text.rfind("\n", start + 1, end)
            if cut <= start:
                cut = text.rfind(". ", start + 1, end)
            if cut <= start:
                cut = end
        else:
            cut = end
        parts.append(text[start:cut])
        start = cut
    return parts


def _should_skip_chunk(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    if _URL_LINE.match(t):
        return True
    return False


def _count_translate_calls_for_block(s: str) -> int:
    if not s.strip():
        return 0
    if len(s) <= _MAX_CHUNK:
        return 1
    return sum(1 for piece in _hard_split(s, _MAX_CHUNK) if not _should_skip_chunk(piece))


def _count_docx_translate_requests(container) -> int:
    total = 0
    for block in _iter_block_items(container):
        if isinstance(block, Paragraph):
            txt = block.text
            if txt.strip():
                total += _count_translate_calls_for_block(txt)
        elif isinstance(block, Table):
            seen_tc = set()
            for row in block.rows:
                for cell in row.cells:
                    tc_id = id(cell._tc)
                    if tc_id in seen_tc:
                        continue
                    seen_tc.add(tc_id)
                    total += _count_docx_translate_requests(cell)
    return total


def _wrap_translate_chunked(
    translate_fn: Callable[[str], str], sleep_s: float = 0.0
) -> Callable[[str], str]:
    def inner(s: str) -> str:
        if not s.strip():
            return s
        if len(s) <= _MAX_CHUNK:
            return translate_fn(s)
        pieces: list[str] = []
        for piece in _hard_split(s, _MAX_CHUNK):
            if _should_skip_chunk(piece):
                pieces.append(piece)
            else:
                pieces.append(translate_fn(piece))
                if sleep_s > 0:
                    time.sleep(sleep_s)
        return "".join(pieces)

    return inner


def _walk_docx_translate(container, translate_fn: Callable[[str], str], stats: dict) -> None:
    for block in _iter_block_items(container):
        if isinstance(block, Paragraph):
            txt = block.text
            if txt.strip():
                block.text = translate_fn(txt)
                stats["paragraphs"] = stats.get("paragraphs", 0) + 1
        elif isinstance(block, Table):
            seen_tc = set()
            for row in block.rows:
                for cell in row.cells:
                    tc_id = id(cell._tc)
                    if tc_id in seen_tc:
                        continue
                    seen_tc.add(tc_id)
                    _walk_docx_translate(cell, translate_fn, stats)


def translate_docx_argos(
    path_en: Path,
    path_ru: Path,
    *,
    source: str,
    target: str,
    workers: int,
    chunk_sleep: float,
    progress: bool,
) -> None:
    from argostranslate.translate import get_translation_from_codes
    from docx import Document

    # Thread-local translator (avoid sharing one CTranslate2 handle across threads).
    tls = threading.local()

    def translate_segment(text: str) -> str:
        if not text.strip():
            return text
        tr = getattr(tls, "tr", None)
        if tr is None:
            tls.tr = get_translation_from_codes(source, target)
            tr = tls.tr
        return tr.translate(text)

    path_ru.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(str(path_en))
    stats: dict = {}
    n = [0]
    total_req = _count_docx_translate_requests(doc) if progress else 0
    prog_lock = threading.Lock()

    def counted(s: str) -> str:
        if progress:
            with prog_lock:
                n[0] += 1
                cur = n[0]
                tot = total_req if total_req > 0 else "?"
                print(
                    f"  [argos] segment {cur}/{tot} ({len(s)} chars) …",
                    flush=True,
                )
        return translate_segment(s)

    safe = _wrap_translate_chunked(counted, sleep_s=chunk_sleep)
    workers = max(1, int(workers))

    if workers > 1:
        jobs: list = []
        _collect_docx_paragraph_jobs(doc, jobs)
        stats["paragraphs"] = len(jobs)
        texts = [t for _, t in jobs]

        def one_block(t: str) -> str:
            return safe(t)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            translated = list(ex.map(one_block, texts))
        for (para, _), new_t in zip(jobs, translated):
            para.text = new_t
    else:
        _walk_docx_translate(doc, safe, stats)

    if progress:
        print(
            f"  [argos] done ({stats.get('paragraphs', 0)} paragraphs, "
            f"{n[0]}/{total_req} segments).",
            flush=True,
        )
    doc.save(str(path_ru))


def main() -> None:
    p = argparse.ArgumentParser(
        description="Translate DOCX en→ru via Argos (LibreTranslate venv), no HTTP."
    )
    p.add_argument("input_docx", type=Path, help="English .docx path")
    p.add_argument("output_docx", type=Path, help="Russian .docx path (written)")
    p.add_argument("--source", default="en", help="Source language code (default en)")
    p.add_argument("--target", default="ru", help="Target language code (default ru)")
    p.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Parallel paragraph workers (0 = CPU count, min 1, default 0)",
    )
    p.add_argument(
        "--chunk-sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep between chunk translates inside a long paragraph (default 0)",
    )
    p.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable per-segment progress lines",
    )
    args = p.parse_args()

    path_en = args.input_docx.resolve()
    path_ru = args.output_docx.resolve()
    if not path_en.is_file():
        sys.exit(f"Input not found: {path_en}")

    import os

    w = int(args.workers)
    if w <= 0:
        w = max(1, (os.cpu_count() or 2))

    print(
        f"Argos DOCX translate: {path_en} → {path_ru} "
        f"({args.source}→{args.target}, workers={w})",
        flush=True,
    )
    translate_docx_argos(
        path_en,
        path_ru,
        source=args.source,
        target=args.target,
        workers=w,
        chunk_sleep=float(args.chunk_sleep),
        progress=not args.no_progress,
    )
    print(f"Wrote {path_ru}", flush=True)


if __name__ == "__main__":
    main()
