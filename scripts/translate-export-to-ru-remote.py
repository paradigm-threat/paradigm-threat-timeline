#!/usr/bin/env python3
"""
Translate export/timeline-*.docx (book + appendix) to Russian via PARADIGM_TRANSLATE_URL relay.

Requires English artifacts from: npm run export
Run:      PARADIGM_TRANSLATE_URL=http://host:5588 bash scripts/export-russian-remote.sh
Multi:    PARADIGM_TRANSLATE_URL='http://atlanta1...:5588,http://dallas1...:5588' (round-robin)
Probe:    bash scripts/export-russian-remote.sh 'http://a:5588,http://d:5588' --probe
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent
EXPORT_DIR = REPO_DIR / "export"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Russian export via HTTP /translate relay (separate from export.sh)"
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        help="GET /languages from relay and print response, then exit",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Do not print per-chunk progress lines",
    )
    args = parser.parse_args()

    url = (os.environ.get("PARADIGM_TRANSLATE_URL") or "").strip()
    if not url:
        sys.exit(
            "Set PARADIGM_TRANSLATE_URL to one or more relay bases (comma-separated), e.g.\n"
            "  export PARADIGM_TRANSLATE_URL=http://atlanta1.relaygateway.net:5588\n"
            "  export PARADIGM_TRANSLATE_URL='http://atlanta1.relaygateway.net:5588,http://dallas1.relaygateway.net:5588'"
        )

    sys.path.insert(0, str(SCRIPT_DIR))
    from export_translate_util import probe_all_relays, run_russian_export

    if args.probe:
        probe_all_relays(url)
        return

    need = [
        EXPORT_DIR / "timeline-book.docx",
        EXPORT_DIR / "timeline-appendix.docx",
    ]
    missing = [p for p in need if not p.is_file()]
    if missing:
        sys.exit(
            "Missing English export files. Run first:\n"
            f"  npm run export\n"
            f"Missing: {', '.join(str(p.relative_to(REPO_DIR)) for p in missing)}"
        )

    run_russian_export(EXPORT_DIR, progress=not args.no_progress)


if __name__ == "__main__":
    main()
