#!/usr/bin/env bash
# Download all 86 MLS photos for 1279 Lancashire Dr (MLS #41144292) at full size.
# Run this on a machine with normal internet access:
#     bash download-photos.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p photos
n=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  n=$((n+1))
  out=$(printf "photos/%02d.jpg" "$n")
  if [ -s "$out" ]; then echo "skip $out"; continue; fi
  echo "get  $out"
  curl -fsSL -A "Mozilla/5.0" -o "$out" "$url" || echo "FAILED $url"
  sleep 0.3
done < photo-urls.txt
echo "Done. $(ls -1 photos/*.jpg 2>/dev/null | wc -l) files in photos/"
