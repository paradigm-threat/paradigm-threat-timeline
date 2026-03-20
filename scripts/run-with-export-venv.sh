#!/usr/bin/env bash
# Bootstrap .venv with PDF/DOCX export deps, then run a Python script.
# Usage: bash scripts/run-with-export-venv.sh scripts/generate-pdf.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
PIP="$ROOT/.venv/bin/pip"
if [[ ! -x "$PY" ]]; then
  echo "Creating .venv for PDF/DOCX export …"
  python3 -m venv "$ROOT/.venv"
fi
"$PIP" install -q --upgrade fpdf2 markdown-it-py mdit-py-plugins Pillow python-docx cairosvg
exec "$PY" "$@"
