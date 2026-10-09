#!/usr/bin/env bash
# One command: script.json + compositions/ -> exports/<name>-1080p.mp4
#
#   kit/make.sh videos/<name>                         # AI voice (Kokoro)
#   RECORDING=take.m4a kit/make.sh videos/<name>      # your own recorded voice
#   CHECK=1 kit/make.sh videos/<name>                 # also run the full `hyperframes check` (slower)
#   PREVIEW=1 kit/make.sh videos/<name>               # stop after snapshots (no render), for a quick look
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
cd "${1:?usage: kit/make.sh videos/<name>}"
NAME="$(node -p "require('./package.json').name")"
t0=$(date +%s)
step() { printf '\n== %s (%ss)\n' "$1" "$(( $(date +%s) - t0 ))"; }

step "voice"
if [ -n "${RECORDING:-}" ]; then python3 scripts/voice.py --recording "$RECORDING"; else python3 scripts/voice.py 2>&1 | grep -v -i warn; fi
step "build"
node scripts/build.mjs
step "sfx + music"
[ -f scripts/sfx.py ] && python3 scripts/sfx.py
python3 scripts/music.py

step "rules"
if grep -rl $'—' compositions script.json; then echo "Em dash found in the files above. Remove it."; exit 1; fi
npx hyperframes lint | tail -1
[ -n "${CHECK:-}" ] && npx hyperframes check | tail -3

if [ -n "${PREVIEW:-}" ]; then
  step "snapshots"
  TOTAL=$(node -p "require('./timings.json').total")
  AT=$(node -p "Array.from({length:8},(_,i)=>((i+0.5)*$TOTAL/8).toFixed(1)).join(',')")
  rm -rf snapshots && npx hyperframes snapshot --at "$AT" | tail -1
  echo "Look at snapshots/contact-sheet.jpg"; exit 0
fi

step "render"
npx hyperframes render --quality high --fps 30 --workers "${WORKERS:-4}" --output renders/video.mp4 | grep -E "rendered in|Failed" || true
step "loudness"
mkdir -p exports
ffmpeg -v error -y -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k \
  -movflags +faststart "exports/$NAME-1080p.mp4"
step "done"
ls -la "exports/$NAME-1080p.mp4"
