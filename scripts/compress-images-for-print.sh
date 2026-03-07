#!/usr/bin/env bash
# Phase H: Image compression for print
# - 800px max width
# - JPEG quality 72
# - Greyscale (optional, for print)
# Usage: ./scripts/compress-images-for-print.sh [main|appendix|all]
# Creates output in media-compressed/ mirror. Does NOT overwrite originals.

set -e
CMD=$(which convert 2>/dev/null || which magick 2>/dev/null || true)
if [ -z "$CMD" ]; then
  echo "ImageMagick (convert or magick) not found. Install with: apt install imagemagick"
  exit 1
fi

SCOPE="${1:-all}"
MEDIA_DIR="media"
OUT_DIR="media-compressed"
MAX_WIDTH=800
QUALITY=72

mkdir -p "$OUT_DIR"

compress_dir() {
  local dir="$1"
  for f in "$dir"/*.{jpg,jpeg,png,webp} 2>/dev/null; do
    [ -f "$f" ] || continue
    rel="${f#$MEDIA_DIR/}"
    out="$OUT_DIR/$rel"
    out="${out%.*}.jpg"
    mkdir -p "$(dirname "$out")"
    echo "  $rel"
    $CMD "$f" -resize "${MAX_WIDTH}x>" -colorspace Gray -quality $QUALITY "$out" 2>/dev/null || \
    $CMD "$f" -resize "${MAX_WIDTH}x>" -quality $QUALITY "$out" 2>/dev/null
  done
}

case "$SCOPE" in
  main)
    for d in "$MEDIA_DIR"/{00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,17}.*; do
      [ -d "$d" ] && compress_dir "$d"
    done
    ;;
  appendix)
    [ -d "$MEDIA_DIR/16.appendix" ] && compress_dir "$MEDIA_DIR/16.appendix"
    ;;
  all)
    find "$MEDIA_DIR" -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' -o -name '*.webp' \) | while read f; do
      rel="${f#$MEDIA_DIR/}"
      out="$OUT_DIR/$rel"
      out="${out%.*}.jpg"
      mkdir -p "$(dirname "$out")"
      echo "  $rel"
      $CMD "$f" -resize "${MAX_WIDTH}x>" -colorspace Gray -quality $QUALITY "$out" 2>/dev/null || \
      $CMD "$f" -resize "${MAX_WIDTH}x>" -quality $QUALITY "$out" 2>/dev/null
    done
    ;;
  *)
    echo "Usage: $0 [main|appendix|all]"
    exit 1
esac

echo "Done. Compressed images in $OUT_DIR/"
