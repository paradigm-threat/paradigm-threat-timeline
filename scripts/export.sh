#!/usr/bin/env bash
# ── export.sh ─────────────────────────────────────────────────────────
# Bootstrap a Python venv (if needed), install deps, generate DOCX then
# convert to PDF via LibreOffice.
# Russian translation: use scripts/export-russian-remote.sh (separate; slow).
# Usage:  bash scripts/export.sh                (text-only, default)
#         bash scripts/export.sh --images       (with images)
#         npm run export
#         npm run export:images
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

# Line-buffered Python logs when stdout is a pipe (e.g. tee, CI).
export PYTHONUNBUFFERED=1

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"

# ── 1. Create venv if missing ─────────────────────────────────────────
if [[ ! -x "$PYTHON" ]]; then
  echo "Creating Python venv at $VENV_DIR …"
  python3 -m venv "$VENV_DIR"
fi

# ── 2. Install / upgrade dependencies ────────────────────────────────
"$PIP" install -q --upgrade markdown-it-py mdit-py-plugins Pillow python-docx cairosvg

# ── 3. Generate DOCX (book + appendix) ────────────────────────────────
EXPORT_DIR="$REPO_DIR/export"

echo "=== Generating DOCX (book + appendix) ==="
"$PYTHON" "$REPO_DIR/scripts/generate-docx.py" "$@"

# ── 4. Convert English DOCX → PDF via LibreOffice (not *-ru.docx) ─────
if command -v libreoffice &>/dev/null; then
  echo "=== Converting DOCX → PDF (LibreOffice) ==="
  for base in timeline-book timeline-appendix; do
    docx="$EXPORT_DIR/${base}.docx"
    if [[ -f "$docx" ]]; then
      echo "  Converting $(basename "$docx") ..."
      libreoffice --headless --convert-to pdf --outdir "$EXPORT_DIR" "$docx" 2>/dev/null
    fi
  done
else
  echo "WARNING: LibreOffice not found — skipping PDF conversion."
  echo "  Install: sudo apt install libreoffice (Debian/Ubuntu)"
  echo "           brew install --cask libreoffice (macOS)"
fi

echo "=== Done ==="
echo "Output files:"
ls -lh "$EXPORT_DIR"/timeline-book.docx "$EXPORT_DIR"/timeline-appendix.docx 2>/dev/null || true
ls -lh "$EXPORT_DIR"/timeline-*.pdf 2>/dev/null || true
echo "Russian: npm run export:russian-remote   (defaults: atlanta3 + jp-osa; override PARADIGM_TRANSLATE_URL)"
