#!/usr/bin/env bash
# ── install-libreoffice-toc-macro.sh ───────────────────────────────────
# Copy UpdateIndexes macro to LibreOffice user profile for TOC page numbers.
# Run once (or idempotently) before export.
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MACRO_SRC="$REPO_DIR/scripts/libreoffice/Standard"

# Find LibreOffice user profile (apt, snap)
find_lo_profile() {
  if [[ -n "${LIBREOFFICE_USER_PROFILE:-}" && -d "$LIBREOFFICE_USER_PROFILE" ]]; then
    echo "$LIBREOFFICE_USER_PROFILE"
    return
  fi
  # Snap: ~/snap/libreoffice/current/.config/libreoffice/4/user
  # Apt:  ~/.config/libreoffice/4/user
  for base in "$HOME/snap/libreoffice/current/.config" "$HOME/.config"; do
    [[ -d "$base" ]] || continue
    for dir in "$base"/libreoffice/*/user; do
      [[ -d "$dir" ]] && { echo "$dir"; return; }
    done
  done
  return 1
}

PROFILE="$(find_lo_profile 2>/dev/null)" || true
if [[ -z "$PROFILE" ]]; then
  echo "LibreOffice user profile not found — macro will be installed on first LO run."
  exit 0
fi

DEST="$PROFILE/basic/Standard"
mkdir -p "$DEST"
cp -a "$MACRO_SRC"/Module1.xba "$MACRO_SRC"/script.xlb "$DEST/"
echo "Installed UpdateIndexes macro to $DEST"
