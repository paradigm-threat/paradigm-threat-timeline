#!/usr/bin/env bash
# Russian DOCX + TXT export via remote relay (slow — run separately from export.sh).
# Prerequisite: npm run export  (English timeline-book/appendix .docx + .txt)
#
# Usage:
#   export PARADIGM_TRANSLATE_URL=http://atlanta1.relaygateway.net:5588
#   bash scripts/export-russian-remote.sh
#
# Two relays (round-robin per translate request — spreads load across nodes):
#   export PARADIGM_TRANSLATE_URL='http://atlanta1.relaygateway.net:5588,http://dallas1.relaygateway.net:5588'
#
#   bash scripts/export-russian-remote.sh http://atlanta1.relaygateway.net:5588
#   bash scripts/export-russian-remote.sh 'http://atlanta1...:5588,http://dallas1...:5588' --probe
#
# Optional:
#   PARADIGM_TRANSLATE_API_KEY — Bearer token
#   PARADIGM_TRANSLATE_TIMEOUT — seconds (default 300)
#   PARADIGM_TRANSLATE_RESUME=1 — skip a pair if *-ru.* exists and is newer than English source
set -euo pipefail
export PYTHONUNBUFFERED=1

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
VENV="$REPO/.venv"
PY="$VENV/bin/python"
PIP="$VENV/bin/pip"

if [[ ! -x "$PY" ]]; then
  echo "No .venv — run: npm run export   (or: python3 -m venv .venv)"
  exit 1
fi

"$PIP" install -q --upgrade python-docx

URL="${PARADIGM_TRANSLATE_URL:-}"
ARGS=()
for a in "$@"; do
  if [[ -z "$URL" && "$a" =~ ^https?:// ]]; then
    URL="$a"
  else
    ARGS+=("$a")
  fi
done

if [[ -z "$URL" ]]; then
  echo "Set PARADIGM_TRANSLATE_URL or pass the relay base URL as the first argument."
  echo "Example: bash scripts/export-russian-remote.sh http://atlanta1.relaygateway.net:5588"
  echo "  Or two relays (comma-separated URL list): .../atlanta...:5588,.../dallas...:5588"
  exit 1
fi

export PARADIGM_TRANSLATE_URL="$URL"
exec "$PY" "$REPO/scripts/translate-export-to-ru-remote.py" "${ARGS[@]}"
