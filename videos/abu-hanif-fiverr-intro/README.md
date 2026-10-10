# Abu Hanif Fiverr intro (dark premium agency style)

Brief: `Fiverr_50s_High_End_Intro_Video_Prompt.pdf` (Abu Hanif, Google Ads & Conversion Tracking Specialist).
Final export: `exports/abu-hanif-fiverr-intro-1080p.mp4` (1920x1080, 30 fps, H.264, AAC, -16 LUFS, exactly 50.0 s).

Look: near-black navy, drifting particle field, glass panels, Inter, blue / cyan accents, blue word-highlight captions,
blur-through scene transitions, slow camera push on every scene, cinematic music mode, restrained UI SFX.
Portrait: the client's real photo (`assets/img/abu-hanif-cutout.png`, background removed with rembg `u2net_human_seg`,
alpha eroded 2 px + 1.2 px blur to kill the white fringe) stays on the right side for the WHOLE video as its own layer
(`compositions/portrait.html`, mounted under every scene): blur-in entrance, gentle float, breathing glow, slow dashed ring,
a spinning cyan arc, a ring pulse on every scene change and a soft zoom spotlight during the name reveal and the CTA.
All scene content lives in the left column (x 140 to 1080). Bottom + side mask fade on the photo. Photo and export are git-ignored (client data). Stats come from the brief.
Dashboard numbers in the hook are labeled DEMO DATA, the outcome chart is labeled ILLUSTRATIVE.

| Scene | Time | Visual |
| --- | --- | --- |
| hook | 0.0 to 3.7 | headline mask reveal, campaign dashboard with count-up, click stream where most signals break |
| problem | 3.7 to 11.8 | Ads > Website > GTM > GA4 > CRM, warning badges, then links repair, checks, data pulses |
| intro | 11.8 to 16.8 | name left (letter reveal from blur), portrait spotlight, floating tool chips |
| expertise | 16.8 to 27.2 | hub "Your data" with 6 nodes, SVG lines draw, pulses flow to the hub |
| proof | 27.2 to 35.5 | 3 glass stat cards flip up with count-up (5+, 200+, $500K+), sparkline draws |
| outcome | 35.5 to 42.1 | tangled red signals clear into a clean rising line and funnel bars, 3 kinetic lines |
| cta | 42.1 to 50.0 | chips fly into the portrait, text left, "Let's work together.", button with light sweep |

## Rebuild

```bash
python3 scripts/voice.py      # speed 1.06, GAP 0.32, cta tail tuned so total is exactly 50.0 s
node scripts/build.mjs && python3 scripts/sfx.py && python3 scripts/music.py   # music: "cinematic" in script.json
npx hyperframes lint
npx hyperframes render --quality high --fps 30 --workers 4 --output renders/video.mp4
ffmpeg -y -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart exports/abu-hanif-fiverr-intro-1080p.mp4
```
To hit an exact length: run voice.py, read the total, add the difference to the last scene's `tail`, run it again.

## Portrait cutout (reuse for any client photo)

```bash
pip install "rembg[cpu]"     # model downloads from GitHub releases (works in the cloud box)
python3 -c "from rembg import remove,new_session; from PIL import Image; remove(Image.open('in.jpg'), session=new_session('u2net_human_seg'), alpha_matting=True).save('cut.png')"
```
Then crop to bbox, resize to about 1100 px, erode alpha (MinFilter 5) and blur 1.2 px. CSS mask:
`linear-gradient(180deg,#000 62%,transparent 96%), linear-gradient(90deg,transparent 2%,#000 16%,#000 84%,transparent 98%)` with `mask-composite: intersect`.

`scripts/build.mjs` mounts `compositions/portrait.html` automatically when it exists and injects the scene start times.
`exports/*-share.mp4` is a smaller copy (CRF 21) for chat / Fiverr upload limits.

## 4K export

```bash
npx hyperframes render --resolution landscape-4k --quality high --fps 30 --workers 4 --output renders/video-4k.mp4   # ~12 min here
ffmpeg -y -i renders/video-4k.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart exports/abu-hanif-fiverr-intro-4k.mp4
# under-30 MB 4K copy for chat: 2-pass H.264 at 4300k
ffmpeg -y -i exports/abu-hanif-fiverr-intro-4k.mp4 -c:v libx264 -preset slow -b:v 4300k -pass 1 -an -f null /dev/null
ffmpeg -y -i exports/abu-hanif-fiverr-intro-4k.mp4 -c:v libx264 -preset slow -b:v 4300k -maxrate 8M -bufsize 16M -pass 2 -c:a aac -b:a 160k -movflags +faststart exports/abu-hanif-fiverr-intro-4k-share.mp4
```
The composition stays 1920x1080; Chrome renders at 2x DPR. Use source images at least 2x their on-screen size
(the portrait cutout is 2000 px for a 720 px slot).
