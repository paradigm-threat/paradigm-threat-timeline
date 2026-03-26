#!/usr/bin/env python3
"""
Translate timeline export DOCX volumes to Russian.

Backends (first match):
  PARADIGM_TRANSLATE_URL — HTTP relay(s): POST {base}/translate JSON
    {"q","source","target","format"}. Use a comma-separated list to round-robin
    across multiple relays (e.g. Atlanta + Dallas) and spread load / rate limits.
  DEEPL_AUTH_KEY / DEEPL_API_KEY — DeepL.
  Else — Google via deep-translator.

Optional headers from env:
  PARADIGM_TRANSLATE_API_KEY — sent as Authorization: Bearer <key>
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, NamedTuple


def _env_truthy(name: str) -> bool:
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _should_skip_up_to_date(en_path: Path, ru_path: Path) -> bool:
    """PARADIGM_TRANSLATE_RESUME=1: skip if RU exists and is newer than EN."""
    if not _env_truthy("PARADIGM_TRANSLATE_RESUME"):
        return False
    if not ru_path.is_file():
        return False
    return ru_path.stat().st_mtime >= en_path.stat().st_mtime


# ---------------------------------------------------------------------------
# DOCX: document-order walk (paragraphs + nested tables)
# ---------------------------------------------------------------------------
try:
    from docx.document import Document as DocxDocument
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table, _Cell
    from docx.text.paragraph import Paragraph
except ImportError:
    DocxDocument = None  # type: ignore


def _iter_block_items(parent):
    if DocxDocument is None:
        raise RuntimeError("python-docx is required for DOCX translation")
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


def _count_translate_calls_for_block(s: str) -> int:
    """How many relay/API calls _wrap_translate_chunked will make for this block (matches translate path)."""
    if not s.strip():
        return 0
    if len(s) <= _MAX_CHUNK:
        return 1
    return sum(1 for piece in _hard_split(s, _MAX_CHUNK) if not _should_skip_chunk(piece))


def _count_docx_translate_requests(container) -> int:
    """Total translate calls for a DOCX body (paragraphs + tables); must match _walk_docx_translate + _wrap_translate_chunked."""
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


def _count_long_text_requests(text: str) -> int:
    """Total translate calls translate_long_text will make (same buffer / flush / split rules)."""
    count = 0
    paragraphs = text.split("\n\n")
    buf: list[str] = []
    buf_len = 0

    def flush_count() -> None:
        nonlocal buf, buf_len, count
        if not buf:
            return
        chunk = "\n\n".join(buf)
        buf = []
        buf_len = 0
        if _should_skip_chunk(chunk):
            return
        count += 1

    for para in paragraphs:
        if len(para) > _MAX_CHUNK:
            if buf:
                flush_count()
            for piece in _hard_split(para, _MAX_CHUNK):
                if not _should_skip_chunk(piece):
                    count += 1
            continue

        plen = len(para) + 2
        if buf_len + plen > _MAX_CHUNK and buf:
            flush_count()
        buf.append(para)
        buf_len += plen

    flush_count()
    return count


def _wrap_translate_chunked(
    translate_fn: Callable[[str], str], sleep_s: float = 0.08
) -> Callable[[str], str]:
    """Ensure single-block translation stays under service limits (DOCX paragraphs)."""

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


def translate_docx(
    path_en: Path,
    path_ru: Path,
    translate_fn: Callable[[str], str],
    *,
    docx_chunk_sleep: float = 0.08,
    progress_prefix: str | None = None,
) -> None:
    from docx import Document

    path_ru.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(str(path_en))
    stats: dict = {}
    n = [0]
    total_req = (
        _count_docx_translate_requests(doc) if progress_prefix else 0
    )

    def fn(s: str) -> str:
        if progress_prefix:
            n[0] += 1
            tot = total_req if total_req > 0 else "?"
            print(
                f"{progress_prefix} request {n[0]}/{tot} (in {len(s)} chars) …",
                flush=True,
            )
        return translate_fn(s)

    inner = fn if progress_prefix else translate_fn
    safe = _wrap_translate_chunked(inner, sleep_s=docx_chunk_sleep)
    _walk_docx_translate(doc, safe, stats)
    if progress_prefix:
        print(
            f"{progress_prefix} done ({stats.get('paragraphs', 0)} paragraphs, "
            f"{n[0]}/{total_req} requests).",
            flush=True,
        )
    doc.save(str(path_ru))


# ---------------------------------------------------------------------------
# Text chunking + translators
# ---------------------------------------------------------------------------
_MAX_CHUNK = 4500
_URL_LINE = re.compile(r"^\s*https?://\S+\s*$")


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


def translate_long_text(
    text: str,
    translate_fn: Callable[[str], str],
    sleep_s: float = 0.12,
    *,
    progress_prefix: str | None = None,
) -> str:
    """Translate long text; optional progress_prefix prints each API/chunk call."""
    n = [0]
    total_chunks = _count_long_text_requests(text) if progress_prefix else 0

    def call(s: str) -> str:
        if progress_prefix:
            n[0] += 1
            tot = total_chunks if total_chunks > 0 else "?"
            print(
                f"{progress_prefix} chunk {n[0]}/{tot} (in {len(s)} chars) …",
                flush=True,
            )
        r = translate_fn(s)
        return r

    tf = call if progress_prefix else translate_fn

    paragraphs = text.split("\n\n")
    out_parts: list[str] = []
    buf: list[str] = []
    buf_len = 0

    def flush() -> None:
        nonlocal buf, buf_len
        if not buf:
            return
        chunk = "\n\n".join(buf)
        buf = []
        buf_len = 0
        if _should_skip_chunk(chunk):
            out_parts.append(chunk)
            return
        out_parts.append(tf(chunk))
        if sleep_s > 0:
            time.sleep(sleep_s)

    for para in paragraphs:
        if len(para) > _MAX_CHUNK:
            if buf:
                flush()
            for piece in _hard_split(para, _MAX_CHUNK):
                if _should_skip_chunk(piece):
                    out_parts.append(piece)
                else:
                    out_parts.append(tf(piece))
                    if sleep_s > 0:
                        time.sleep(sleep_s)
            continue

        plen = len(para) + 2
        if buf_len + plen > _MAX_CHUNK and buf:
            flush()
        buf.append(para)
        buf_len += plen

    flush()
    if progress_prefix:
        print(
            f"{progress_prefix} text chunks complete ({n[0]}/{total_chunks} translated).",
            flush=True,
        )
    return "\n\n".join(out_parts)


def _parse_relay_response(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in (
            "translatedText",
            "translated_text",
            "text",
            "translation",
            "result",
            "t",
            "output",
            "q",  # some relays echo
        ):
            v = data.get(key)
            if isinstance(v, str) and v.strip():
                return v
        inner = data.get("data")
        if isinstance(inner, str) and inner.strip():
            return inner
        if isinstance(inner, dict):
            return _parse_relay_response(json.dumps(inner))
    raise ValueError(f"Unexpected /translate JSON (first 400 chars): {raw[:400]!r}")


def parse_relay_urls(raw: str) -> list[str]:
    """Split PARADIGM_TRANSLATE_URL on commas; strip; drop empties."""
    return [u.strip().rstrip("/") for u in (raw or "").split(",") if u.strip()]


def translate_via_relay(
    get_base_url: Callable[[], str],
    text: str,
    *,
    source: str,
    target: str,
    fmt: str,
) -> str:
    """POST to {base}/translate; get_base_url() picks the relay for this request (round-robin)."""
    base_url = get_base_url().rstrip("/")
    url = base_url + "/translate"
    payload = json.dumps(
        {"q": text, "source": source, "target": target, "format": fmt},
        ensure_ascii=False,
    ).encode("utf-8")
    timeout = float((os.environ.get("PARADIGM_TRANSLATE_TIMEOUT") or "300").strip())
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    key = (os.environ.get("PARADIGM_TRANSLATE_API_KEY") or "").strip()
    if key:
        req.add_header("Authorization", f"Bearer {key}")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:800]
        raise RuntimeError(f"HTTP {e.code} from {url}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Request failed {url}: {e}") from e

    return _parse_relay_response(body)


class TranslateBackend(NamedTuple):
    translate: Callable[[str], str]
    chunk_sleep: float
    docx_chunk_sleep: float
    label: str


def build_translate_backend() -> TranslateBackend:
    relay_raw = (os.environ.get("PARADIGM_TRANSLATE_URL") or "").strip()
    relay_urls = parse_relay_urls(relay_raw)
    if relay_urls:
        n = len(relay_urls)
        idx = [0]

        def next_base() -> str:
            u = relay_urls[idx[0] % n]
            idx[0] += 1
            return u

        if n == 1:
            label = f"Relay ({relay_urls[0]})"
        else:
            label = f"Relay pool ({n} endpoints, round-robin)"

        def relay_fn(s: str) -> str:
            if not s.strip():
                return s
            return translate_via_relay(
                next_base, s, source="en", target="ru", fmt="text"
            )

        return TranslateBackend(relay_fn, 0.0, 0.0, label)

    key = (os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY") or "").strip()

    if key:
        from deep_translator import DeeplTranslator

        free_raw = (os.environ.get("DEEPL_USE_FREE_API") or "1").strip().lower()
        use_free = free_raw not in ("0", "false", "no")
        tr = DeeplTranslator(
            api_key=key, source="en", target="ru", use_free_api=use_free
        )

        def deepl(s: str) -> str:
            if not s.strip():
                return s
            out = tr.translate(s)
            return s if out is None else out

        return TranslateBackend(deepl, 0.12, 0.08, "DeepL")

    from deep_translator import GoogleTranslator

    tr = GoogleTranslator(source="en", target="ru")

    def google(s: str) -> str:
        if not s.strip():
            return s
        out = tr.translate(s)
        return s if out is None else out

    return TranslateBackend(google, 0.12, 0.08, "Google")


def translate_utf8_file(
    path_en: Path,
    path_ru: Path,
    translate_fn: Callable[[str], str],
    *,
    chunk_sleep: float = 0.12,
    progress_prefix: str | None = None,
) -> None:
    raw = path_en.read_text(encoding="utf-8")
    translated = translate_long_text(
        raw,
        translate_fn,
        sleep_s=chunk_sleep,
        progress_prefix=progress_prefix,
    )
    path_ru.parent.mkdir(parents=True, exist_ok=True)
    path_ru.write_text(translated, encoding="utf-8")


def run_russian_export(
    export_dir: Path,
    *,
    progress: bool = True,
) -> None:
    relay = (os.environ.get("PARADIGM_TRANSLATE_URL") or "").strip()
    if not relay:
        try:
            import deep_translator  # noqa: F401
        except ImportError as e:
            raise SystemExit(
                "Set PARADIGM_TRANSLATE_URL to your relay (recommended), or "
                "pip install deep-translator for DeepL/Google.\n"
                "  Example: export PARADIGM_TRANSLATE_URL=http://host:5588"
            ) from e

    try:
        backend = build_translate_backend()
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Translation backend failed to initialize: {e}") from e

    print(f"\n=== Russian export (target=ru, backend={backend.label}) ===", flush=True)
    print("  Progress lines list each HTTP/chunk request.", flush=True)

    pairs = [
        ("timeline-book.docx", "timeline-book-ru.docx"),
        ("timeline-appendix.docx", "timeline-appendix-ru.docx"),
    ]

    missing_now = [en for en, _ in pairs if not (export_dir / en).is_file()]
    if missing_now:
        raise SystemExit(
            "English DOCX missing before translation. Run: npm run export\n  Missing: "
            + ", ".join(missing_now)
        )

    for en_name, ru_name in pairs:
        en_path = export_dir / en_name
        ru_path = export_dir / ru_name
        if not en_path.is_file():
            print(f"  Skip (missing): {en_name}", flush=True)
            continue
        if _should_skip_up_to_date(en_path, ru_path):
            print(
                f"  Skip (resume: RU newer than EN): {ru_name}",
                flush=True,
            )
            continue
        print(f"\n--- {en_name} → {ru_name} ---", flush=True)
        prefix = f"  [{ru_name}]" if progress else None
        if en_name.endswith(".docx"):
            translate_docx(
                en_path,
                ru_path,
                backend.translate,
                docx_chunk_sleep=backend.docx_chunk_sleep,
                progress_prefix=prefix,
            )
        else:
            translate_utf8_file(
                en_path,
                ru_path,
                backend.translate,
                chunk_sleep=backend.chunk_sleep,
                progress_prefix=prefix,
            )
        print(f"  Wrote {ru_path}", flush=True)

    print("\n=== Russian export done ===", flush=True)


def probe_relay_languages(base_url: str) -> None:
    """GET /languages for one base URL."""
    url = base_url.rstrip("/") + "/languages"
    timeout = float((os.environ.get("PARADIGM_TRANSLATE_TIMEOUT") or "60").strip())
    req = urllib.request.Request(url, method="GET")
    key = (os.environ.get("PARADIGM_TRANSLATE_API_KEY") or "").strip()
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        print(resp.read().decode("utf-8")[:2000], flush=True)


def probe_all_relays(relay_raw: str) -> None:
    """GET /languages for each comma-separated relay base."""
    for u in parse_relay_urls(relay_raw):
        print(f"GET {u}/languages", flush=True)
        probe_relay_languages(u)
        print("", flush=True)
