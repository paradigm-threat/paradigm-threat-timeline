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
echo "=== Generating PDF ==="
"$PYTHON" "$REPO_DIR/scripts/generate-pdf.py"

echo "=== Generating DOCX ==="
"$PYTHON" "$REPO_DIR/scripts/generate-docx.py"

echo "=== Done ==="
