#!/usr/bin/env python3
"""
Post-process Russian DOCX exports after machine translation (Argos/LibreTranslate).

Applies safe, curated string fixes inside word/document.xml (formatting preserved).

Default: patches export/timeline-book-ru.docx and export/timeline-appendix-ru.docx.

Usage:
  python3 scripts/postprocess_ru_docx.py
  python3 scripts/postprocess_ru_docx.py --dry-run
  python3 scripts/postprocess_ru_docx.py path/to/custom-ru.docx --book
  python3 scripts/postprocess_ru_docx.py path/to/custom-ru.docx --appendix
  python3 scripts/postprocess_ru_docx.py --no-backup export/timeline-book-ru.docx --book
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from io import BytesIO
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent

# Full Norse “nine realms” paragraph (book only): fixes half-translated “Реалм”, English
# leftovers, and the “Норвежец также имел…” mistake.
NORSE_OLD = (
    "В скандинавской мифологии каждый хайм («дом») в конфигурации был назван так: "
    "Муспелхайм (Реалм Огня / Меркурий), Альфхайм (Яркое царство эльфов / Венера), "
    "Мидгард (Средняя Земля / Земля), Йотунхайм (Реалм Морозных Гигантов / Марс), "
    "Асгард (Реалм Эзира / Юпитер), Ванахейм (Реалм Ванира / Сатурна), "
    "Свартальфхайм (Темное царство гномов / Уран). Нифльхайм (Realm of Myst / Neptune), "
    "Гельхайм (Realm of the Dead / Underworld / Pluto), Норвежец также имел название "
    "Биркеландских течений, которые соединились между мирами: Бифрост."
)
NORSE_NEW = (
    "В скандинавской мифологии каждый хайм («дом») в конфигурации был назван так: "
    "Муспелхайм (царство огня / Меркурий), Альфхейм (светлое царство эльфов / Венера), "
    "Мидгард (Срединная земля / Земля), Йотунхайм (царство ледяных великанов / Марс), "
    "Асгард (царство асов / Юпитер), Ванахейм (царство ваниров / Сатурн), "
    "Свартальфхайм (тёмное царство гномов / Уран). Нифльхайм (царство тумана / Нептун), "
    "Гельхайм (царство мёртвых / подземный мир / Плутон). У скандинавов также было название "
    "для биркеландских токов, соединявших миры: Бифрост."
)

BOOK_REPLACEMENTS: list[tuple[str, str]] = [
    (NORSE_OLD, NORSE_NEW),
    ("Часть IV: The Blip", "Часть IV: Блип"),
    ("(The Blip)", "(блип)"),
    ("TL;DR:", "Кратко:"),
    ("Морлокс", "морлоки"),
    ("Марс (прометей)", "Марс (Прометей)"),
    ("чуждый Стандартной солнечной модели", "чуждый стандартной солнечной модели"),
    ("изобретенные тысячелетия", "выдуманные тысячелетия"),
]

APPENDIX_REPLACEMENTS: list[tuple[str, str]] = [
    ("TL;DR:", "Кратко:"),
    ("сфабрикованным Blip", "выдуманным «блипом»"),
    ("Посмотреть The Blip.", "См. «Блип»."),
    # Same link text without trailing period (Word/run splits differ)
    ("Посмотреть The Blip", "См. «Блип»"),
]

COMMON_REPLACEMENTS: list[tuple[str, str]] = [
    ("TL;DR:", "Кратко:"),
]


def patch_docx_xml(
    docx_path: Path,
    replacements: list[tuple[str, str]],
    *,
    dry_run: bool,
    backup: bool,
    warn_norse_missing: bool,
) -> int:
    """Rewrite word/document.xml inside docx. Returns total replacement hits, or -1 on error."""
    data = docx_path.read_bytes()
    z_in = zipfile.ZipFile(BytesIO(data), "r")
    xml_name = "word/document.xml"
    try:
        xml_bytes = z_in.read(xml_name)
    except KeyError:
        print(f"Error: {xml_name} not found in {docx_path}", file=sys.stderr)
        z_in.close()
        return -1

    text = xml_bytes.decode("utf-8")
    if warn_norse_missing and NORSE_OLD not in text and "Реалм" in text:
        print(
            "  Warning: 'Реалм' still present but full Norse paragraph pattern did not match; "
            "edit scripts/postprocess_ru_docx.py or fix by hand.",
            file=sys.stderr,
        )

    total_hits = 0
    report: list[tuple[str, int]] = []
    new_text = text

    for old, new in replacements:
        c = new_text.count(old)
        if c:
            report.append((old[:56] + ("…" if len(old) > 56 else ""), c))
        total_hits += c
        if not dry_run:
            new_text = new_text.replace(old, new)

    if dry_run:
        z_in.close()
        print(f"[dry-run] {docx_path} ({len(replacements)} rules, {total_hits} total hits)")
        for label, c in report:
            print(f"  {c}×  {label}")
        return total_hits

    z_in.close()

    if total_hits == 0:
        print(f"No matches in {docx_path}; left unchanged.")
        return 0

    if backup:
        bak = docx_path.with_suffix(docx_path.suffix + ".bak-postprocess")
        bak.write_bytes(data)
        print(f"Backup: {bak}")

    out_buf = BytesIO()
    z_out = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)
    z_in = zipfile.ZipFile(BytesIO(data), "r")
    for item in z_in.infolist():
        payload = new_text.encode("utf-8") if item.filename == xml_name else z_in.read(item.filename)
        z_out.writestr(item, payload)
    z_out.close()
    z_in.close()

    docx_path.write_bytes(out_buf.getvalue())
    zipfile.ZipFile(docx_path).testzip()
    print(f"Patched {docx_path} ({total_hits} replacement hits)")
    for label, c in report:
        print(f"  {c}×  {label}")
    return total_hits


def main() -> int:
    p = argparse.ArgumentParser(description="Post-process RU DOCX after machine translation.")
    p.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="DOCX paths (default: export/timeline-book-ru.docx and export/timeline-appendix-ru.docx)",
    )
    p.add_argument("--book", action="store_true", help="Treat all given files with book preset")
    p.add_argument("--appendix", action="store_true", help="Treat all given files with appendix preset")
    p.add_argument(
        "--common",
        action="store_true",
        help="Treat all given files with common preset (TL;DR → Кратко only)",
    )
    p.add_argument("--dry-run", action="store_true", help="Report counts; do not modify files")
    p.add_argument("--no-backup", action="store_true", help="Skip .bak-postprocess copy")
    args = p.parse_args()

    modes = sum(bool(x) for x in (args.book, args.appendix, args.common))
    if modes > 1:
        print("Error: use only one of --book, --appendix, --common", file=sys.stderr)
        return 1

    default_book = REPO_DIR / "export" / "timeline-book-ru.docx"
    default_appendix = REPO_DIR / "export" / "timeline-appendix-ru.docx"

    jobs: list[tuple[Path, list[tuple[str, str]], str]] = []

    if not args.files:
        if not default_book.is_file():
            print(f"Warning: missing default book path {default_book}", file=sys.stderr)
        else:
            jobs.append((default_book, BOOK_REPLACEMENTS, "book"))
        if not default_appendix.is_file():
            print(f"Warning: missing default appendix path {default_appendix}", file=sys.stderr)
        else:
            jobs.append((default_appendix, APPENDIX_REPLACEMENTS, "appendix"))
        if not jobs:
            print("Error: no default export files found; pass paths explicitly.", file=sys.stderr)
            return 1
    else:
        if args.book:
            preset = BOOK_REPLACEMENTS
            label = "book"
        elif args.appendix:
            preset = APPENDIX_REPLACEMENTS
            label = "appendix"
        elif args.common:
            preset = COMMON_REPLACEMENTS
            label = "common"
        else:
            print(
                "Error: with explicit files, pass --book, --appendix, or --common.\n"
                f"  Example: {Path(sys.argv[0]).name} export/foo-ru.docx --book",
                file=sys.stderr,
            )
            return 1
        for f in args.files:
            path = f.resolve()
            if not path.is_file():
                print(f"Error: not a file: {path}", file=sys.stderr)
                return 1
            jobs.append((path, preset, label))

    rc = 0
    for path, repls, label in jobs:
        print(f"--- {path.name} ({label}) ---")
        n = patch_docx_xml(
            path,
            repls,
            dry_run=args.dry_run,
            backup=not args.no_backup,
            warn_norse_missing=(label == "book"),
        )
        if n < 0:
            rc = 1

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
