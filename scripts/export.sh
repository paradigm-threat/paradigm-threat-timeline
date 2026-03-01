#!/usr/bin/env bash
# ── export.sh ─────────────────────────────────────────────────────────
# Bootstrap a Python venv (if needed), install deps, generate PDF + DOCX.
# Usage:  bash scripts/export.sh          (or: npm run export)
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

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
"$PIP" install -q --upgrade fpdf2 markdown-it-py Pillow python-docx

# ── 3. Generate exports ──────────────────────────────────────────────
echo "=== Generating DOCX ==="
"$PYTHON" "$REPO_DIR/scripts/generate-docx.py"

echo "=== Converting DOCX → PDF via LibreOffice ==="
DOCX_PATH="$REPO_DIR/export/timeline.docx"
EXPORT_DIR="$REPO_DIR/export"
if command -v libreoffice &>/dev/null; then
  libreoffice --headless --convert-to pdf \
    --outdir "$EXPORT_DIR" "$DOCX_PATH"
  echo "PDF generated at $EXPORT_DIR/timeline.pdf"
else
  echo "WARNING: LibreOffice not found — falling back to native PDF generator"
  "$PYTHON" "$REPO_DIR/scripts/generate-pdf.py"
fi

echo "=== Done ==="
