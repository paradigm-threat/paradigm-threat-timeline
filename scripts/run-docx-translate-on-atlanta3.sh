#!/usr/bin/env bash
# Upload an English DOCX to atlanta3 and translate it to Russian using Argos in-process
# (LibreTranslate venv on the server — same models, NO HTTP /translate API).
#
# Default input: export/timeline-book.docx (override with first arg).
#
# Stays running after you disconnect: uses nohup on the remote host and writes a log.
#
# Prereqs (local):  ssh + scp, key auth to the server
# Prereqs (remote): sudo -u relay; python-docx is installed automatically (pip in venv).
#
# Env:
#   PARADIGM_ARGOS_SSH_HOST   default atlanta3.relaygateway.net
#   PARADIGM_ARGOS_SSH_USER   default ari
#   PARADIGM_ARGOS_SSH_KEY    default ~/.ssh/id_ed25519_relay_gateway
#   PARADIGM_ARGOS_WORKERS    optional; passed as --workers N to the Python script
#
# Other ways to survive SSH loss (run manually on server if you prefer):
#   tmux new -d -s docxru 'sudo -u relay /opt/libretranslate/venv/bin/python3 ... 2>&1 | tee /tmp/docx-argos.log'
#   screen -dmS docxru bash -lc '...'
#   systemd-run --scope --unit=pt-docx-ru --collect=no sudo -u relay ...   # logs in journalctl
#
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${PARADIGM_ARGOS_SSH_HOST:-atlanta3.relaygateway.net}"
USER="${PARADIGM_ARGOS_SSH_USER:-ari}"
KEY="${PARADIGM_ARGOS_SSH_KEY:-$HOME/.ssh/id_ed25519_relay_gateway}"

SCRIPT_LOCAL="$REPO/scripts/translate_docx_argos_on_server.py"
IN_LOCAL="${1:-$REPO/export/timeline-book.docx}"
STEM="$(basename "$IN_LOCAL" .docx)"
OUT_NAME="${STEM}-ru.docx"

SSH=(ssh -i "$KEY" -o BatchMode=yes -o StrictHostKeyChecking=accept-new)
SCP=(scp -i "$KEY" -o BatchMode=yes -o StrictHostKeyChecking=accept-new)

if [[ ! -f "$SCRIPT_LOCAL" ]]; then
  echo "Missing $SCRIPT_LOCAL" >&2
  exit 1
fi
if [[ ! -f "$IN_LOCAL" ]]; then
  echo "Input DOCX not found: $IN_LOCAL" >&2
  echo "Usage: $0 [path/to/english.docx]" >&2
  exit 1
fi
if [[ ! -r "$KEY" ]]; then
  echo "SSH key not readable: $KEY" >&2
  exit 1
fi

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
WORKER_EXTRA=()
if [[ -n "${PARADIGM_ARGOS_WORKERS:-}" ]]; then
  WORKER_EXTRA=(--workers "$PARADIGM_ARGOS_WORKERS")
fi

REMOTE_TMP="/tmp/pt-docx-argos-$RUN_ID"

echo "Host: $USER@$HOST"
echo "Remote job dir: $REMOTE_TMP  (under /tmp so user relay can read/write)"
echo "Input (local):  $IN_LOCAL"
echo "Output (remote): $REMOTE_TMP/$OUT_NAME"
echo ""

"${SSH[@]}" "$USER@$HOST" "mkdir -p '$REMOTE_TMP' && chmod 1777 '$REMOTE_TMP'"
"${SCP[@]}" "$SCRIPT_LOCAL" "$USER@$HOST:$REMOTE_TMP/translate_docx_argos_on_server.py"
"${SCP[@]}" "$IN_LOCAL" "$USER@$HOST:$REMOTE_TMP/in.docx"
"${SSH[@]}" "$USER@$HOST" "chmod a+rX '$REMOTE_TMP' && chmod a+r '$REMOTE_TMP/'*"

# Remote: install python-docx once, then nohup Argos translate (survives SSH disconnect).
"${SSH[@]}" "$USER@$HOST" bash -s "$REMOTE_TMP" "$OUT_NAME" "${WORKER_EXTRA[@]}" <<'REMOTE_SCRIPT'
set -euo pipefail
REMOTE_TMP="$1"
OUT_NAME="$2"
shift 2
cd "$REMOTE_TMP"
LOG="$PWD/translate.log"
PY="/opt/libretranslate/venv/bin/python3"
SCRIPT="$PWD/translate_docx_argos_on_server.py"
if [[ ! -x "$PY" ]]; then
  echo "Missing LibreTranslate venv at $PY" >&2
  exit 1
fi
echo "Installing python-docx into LibreTranslate venv (if needed)…"
sudo -u relay "$PY" -m pip install -q python-docx
echo "Starting background translate (nohup)…"
nohup sudo -u relay "$PY" "$SCRIPT" ./in.docx "./$OUT_NAME" "$@" >>"$LOG" 2>&1 &
echo $! >"$PWD/translate.pid"
echo "Remote wrapper PID $(cat translate.pid); translator runs as child of nohup — see translate.log"
echo "Log file: $LOG"
REMOTE_SCRIPT

echo ""
echo "Detached on server. Monitor:"
echo "  ${SSH[*]} $USER@$HOST 'tail -f $REMOTE_TMP/translate.log'"
echo "Fetch result when done:"
echo "  ${SCP[*]} $USER@$HOST:$REMOTE_TMP/$OUT_NAME \"$REPO/export/$OUT_NAME\""
echo "Then post-process RU DOCX (TL;DR→Кратко, book/appendix fixes):"
echo "  python3 \"$REPO/scripts/postprocess_ru_docx.py\""
echo "  # or: python3 \"$REPO/scripts/postprocess_ru_docx.py\" \"$REPO/export/$OUT_NAME\" --book|--appendix"
