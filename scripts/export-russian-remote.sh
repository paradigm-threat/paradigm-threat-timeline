#!/usr/bin/env bash
# Russian DOCX + TXT export via remote relay (slow — run separately from export.sh).
# Prerequisite: npm run export  (English timeline-book/appendix .docx + .txt)
#
# Usage:
#   bash scripts/export-russian-remote.sh
#     (defaults to atlanta3 relay if PARADIGM_TRANSLATE_URL unset)
#
#   export PARADIGM_TRANSLATE_URL=http://atlanta3.relaygateway.net:5588
#   bash scripts/export-russian-remote.sh
#
# Multiple relays (comma-separated — round-robin per translate request):
#   export PARADIGM_TRANSLATE_URL='http://atlanta3.relaygateway.net:5588,http://dfw1.relaygateway.net:5588'
#
#   bash scripts/export-russian-remote.sh http://atlanta3.relaygateway.net:5588
#   bash scripts/export-russian-remote.sh 'http://atlanta3...:5588,http://dfw1...:5588' --probe
#
# Optional:
#   PARADIGM_TRANSLATE_API_KEY — Bearer token
#   PARADIGM_TRANSLATE_TIMEOUT — seconds (default 300)
#   PARADIGM_TRANSLATE_WORKERS — parallel paragraph jobs for relay mode (default 4)
#   PARADIGM_TRANSLATE_RETRIES / PARADIGM_TRANSLATE_BACKOFF / PARADIGM_TRANSLATE_BACKOFF_MAX — relay retries
#   PARADIGM_TRANSLATE_RESUME=1 — skip a pair if *-ru.* exists and is newer than English source
set -euo pipefail
export PYTHONUNBUFFERED=1

# Default relays when env and CLI omit URLs (comma-separated, no trailing slashes).
DEFAULT_PARADIGM_TRANSLATE_URLS='http://atlanta3.relaygateway.net:5588'

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
  URL="$DEFAULT_PARADIGM_TRANSLATE_URLS"
  echo "PARADIGM_TRANSLATE_URL not set — using default relay list:"
  echo "  $URL"
fi

export PARADIGM_TRANSLATE_URL="$URL"
exec "$PY" "$REPO/scripts/translate-export-to-ru-remote.py" "${ARGS[@]}"
