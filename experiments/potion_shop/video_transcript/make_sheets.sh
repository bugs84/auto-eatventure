#!/bin/bash
# Download a YouTube gameplay video and cut it into contact sheets for
# reading by (sub)agents: 1 frame per second, 296 px wide, the video time
# burnt in, 4x2 frames per sheet (sheet N = seconds 8*(N-1) .. 8*N-1).
# Also 443 px frames (frames/NNNNN.jpg = second NNNNN-1) for a closer look.
# Usage: make_sheets.sh URL OUT_DIR [FORMAT]   (FORMAT default 248 = 1080p
# vp9 video only; see `yt-dlp -F URL`)
set -euo pipefail
URL=$1
OUT=$2
FORMAT=${3:-248}
YTDLP=~/.local/bin/yt-dlp
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
mkdir -p "$OUT/sheets" "$OUT/frames"
cd "$OUT"
[ -f video.webm ] || [ -f video.mp4 ] || \
  "$YTDLP" -q -f "$FORMAT" -o 'video.%(ext)s' "$URL"
VIDEO=$(ls video.* | head -1)
ffmpeg -v error -y -i "$VIDEO" -vf "fps=1,scale=296:-2,\
drawtext=fontfile=$FONT:text='%{eif\:t\:d}s':x=4:y=4:fontsize=22:\
fontcolor=yellow:box=1:boxcolor=black,tile=4x2" -q:v 3 sheets/%04d.jpg
ffmpeg -v error -y -i "$VIDEO" -vf "fps=1,scale=443:-2" -q:v 3 \
  frames/%05d.jpg
echo "sheets: $(ls sheets | wc -l), frames: $(ls frames | wc -l)"
