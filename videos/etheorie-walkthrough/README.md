# eTheorie event tracking walkthrough (Apple-style screen walkthrough)

Brief: `PROMPT.md` (from the client zip) + 17 real screenshots (1568x734).
Output: `exports/etheorie-walkthrough-1080p.mp4` (1920x1080, 30 fps, about 3:52).

Everything is data-driven from `steps.json`: one entry per segment (intro, events, chapter cards, 18 steps, outro).
A step lists its screenshot, click points (with an optional outline box, or `hover`), highlight rects
(`pan` for a slow downward pan, `short` for quick row pulses without moving the camera), breadcrumb, action line,
"Show your client" line and the Say line. `scroll: true` adds a scroll-in motion for no-click steps.

Look: #F5F5F7 background, Inter, screenshot in an 18 px rounded card with soft shadow, step badge + breadcrumb
above, two-line caption below, one accent colour #0071E3 for ripple, outline and spotlight. Spotlight dims the
rest to 40 percent. Soft click on every click, very quiet ambient pad, calm Kokoro voice (af_heart).

Privacy: `scripts/mask.py` blurs container IDs, the Meta account name and number, date pickers, the TikTok pixel
date and the GA4 footer year (the brief forbids showing IDs and dates). Client screenshots, VO and exports are
git-ignored.

## Rebuild

```bash
python3 scripts/mask.py <folder with 01_..17_ jpgs>     # -> assets/shots/
python3 scripts/voice.py                                 # -> assets/audio/vo/<id>.wav + vo.json
node scripts/build.mjs                                   # -> compositions/*.html, index.html, sfx.json, timings.json
python3 scripts/sfx.py && python3 scripts/music.py
npx hyperframes lint
npx hyperframes render --quality high --fps 30 --workers 4 --output renders/video.mp4
ffmpeg -y -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart exports/etheorie-walkthrough-1080p.mp4
```
`build.mjs` refuses to build if any on-screen or spoken text contains an en dash, em dash, quote or bracket.
