#!/usr/bin/env bash
# Start a new video from a template project.
#   kit/new-video.sh <name> [promo|dark|premium]
#     promo   = color-block promo (videos/conversion-tracking-promo)   [default]
#     dark    = dark-tech explainer (videos/conversion-tracking-portfolio)
#     premium = dark premium agency intro, particles, glass, 50 s (videos/abu-hanif-fiverr-intro)
# Then: edit videos/<name>/script.json and the scene files in videos/<name>/compositions/, run kit/make.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:?usage: kit/new-video.sh <name> [promo|dark|premium]}"
case "${2:-promo}" in
  promo) SRC="$ROOT/videos/conversion-tracking-promo" ;;
  dark)  SRC="$ROOT/videos/conversion-tracking-portfolio" ;;
  premium) SRC="$ROOT/videos/abu-hanif-fiverr-intro" ;;
  *) echo "style must be promo, dark or premium"; exit 1 ;;
esac
DST="$ROOT/videos/$NAME"
[ -e "$DST" ] && { echo "$DST already exists"; exit 1; }
mkdir -p "$DST"
(cd "$SRC" && tar cf - --exclude=renders --exclude=snapshots --exclude=exports --exclude=voice-ref \
  --exclude=assets/audio --exclude=node_modules .) | (cd "$DST" && tar xf -)
mkdir -p "$DST/assets/audio"
# kit scripts are the source of truth (promo build/sfx/music; dark keeps its own build/music)
cp "$ROOT/kit/scripts/voice.py" "$ROOT/kit/scripts/clone_voice.py" "$DST/scripts/"
if [ "${2:-promo}" = promo ]; then cp "$ROOT/kit/scripts/"{build.mjs,sfx.py,music.py} "$DST/scripts/"; fi
# premium keeps its own dark build.mjs (particles, glass, blue captions); music.py reads "music" from script.json
node -e "for (const f of ['package.json','meta.json']) { const p='$DST/'+f, j=require(p); j.name='$NAME'; if (j.id) j.id='$NAME'; require('fs').writeFileSync(p, JSON.stringify(j,null,2)+'\n'); }"
rm -f "$DST/README.md" "$DST/BRIEF.md" "$DST/timings.json" "$DST/sfx.json"
echo "created videos/$NAME from $(basename "$SRC")"
echo "next: edit script.json + compositions/*.html, then  kit/make.sh videos/$NAME"
