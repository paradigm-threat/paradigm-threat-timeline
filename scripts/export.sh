#!/usr/bin/env bash
# ── export.sh ─────────────────────────────────────────────────────────
# Bootstrap a Python venv (if needed), install deps, generate DOCX then
# convert to PDF via LibreOffice.
# Usage:  bash scripts/export.sh                (text-only, default)
#         bash scripts/export.sh --images       (with images)
#         npm run export                        (text-only)
#         npm run export:images                 (with images)
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"

# Pass-through flags (e.g. --images)
EXTRA_FLAGS="${*:-}"

# ── 1. Create venv if missing ─────────────────────────────────────────
if [[ ! -x "$PYTHON" ]]; then
  echo "Creating Python venv at $VENV_DIR …"
  python3 -m venv "$VENV_DIR"
fi

# ── 2. Install / upgrade dependencies ────────────────────────────────
"$PIP" install -q --upgrade markdown-it-py Pillow python-docx

# ── 3. Generate DOCX (book + appendix) ───────────────────────────────
EXPORT_DIR="$REPO_DIR/export"

echo "=== Generating DOCX (book + appendix) ==="
"$PYTHON" "$REPO_DIR/scripts/generate-docx.py" $EXTRA_FLAGS

# ── 4. Convert DOCX → PDF via LibreOffice ────────────────────────────
if command -v libreoffice &>/dev/null; then
  echo "=== Converting DOCX → PDF (LibreOffice) ==="
  for docx in "$EXPORT_DIR"/timeline-*.docx; do
    echo "  Converting $(basename "$docx") ..."
    libreoffice --headless --convert-to pdf --outdir "$EXPORT_DIR" "$docx" 2>/dev/null
  done
else
  echo "WARNING: LibreOffice not found — skipping PDF conversion."
  echo "  Install: sudo apt install libreoffice (Debian/Ubuntu)"
  echo "           brew install --cask libreoffice (macOS)"
fi

echo "=== Done ==="
echo "Output files:"
ls -lh "$EXPORT_DIR"/timeline-*.{docx,pdf} 2>/dev/null || true
