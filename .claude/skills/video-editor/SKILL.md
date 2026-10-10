---
name: video-editor
description: Shakil's reusable video editing workflow on HyperFrames. Use for any request in this repo to plan, build, restyle, review, or export a video (talking head, SaaS / product, faceless, explainer, promo), including adding voiceover, music, sound effects and captions. Read before touching anything under videos/.
---

# Video editor (Shakil's workflow)

## FAST PATH (do this when the user says "make a video")

Goal: from request to delivered MP4 with no re-research. Everything needed is already in this repo.

1. `bash kit/setup.sh` (fresh session only, about 1 to 2 min).
2. `kit/new-video.sh <name> promo` (or `dark`, or `premium` for a dark agency-style Fiverr intro). Copies a finished template incl. scenes, scripts, SFX, music.
3. Write `videos/<name>/script.json`: same scene ids, one entry per caption line. Hooks: `library/hooks.md`.
   Keep each scene's line count the same as the template, or re-point its `c[i]` cues.
4. Change the text inside `videos/<name>/compositions/*.html` (graphics catalog: `library/graphics.md`).
5. `PREVIEW=1 kit/make.sh videos/<name>` then Read `snapshots/contact-sheet.jpg`, fix overlaps.
6. `kit/make.sh videos/<name>` (AI voice) or `RECORDING=<file> kit/make.sh videos/<name>` (user's real voice,
   see `library/voice.md`). Output: `videos/<name>/exports/<name>-1080p.mp4`.
7. Send the MP4, update the Log below + root README table, commit, push.

Measured timing (4 CPU cloud box, 4 render workers): a 1:51 video renders in about 2.5 min, so a 60 s video
is about 1.5 min of render. Voice + build + SFX + music take under 30 s. The total is never "instant": the
render is real frame-by-frame capture.

Voice: the user said the FreeVC clone still sounds AI. Default to their own recording when they want "my voice".

This repo turns a brief into a finished MP4 with HyperFrames (HTML + GSAP rendered to video).
Upstream HyperFrames skills live next to this one in `.claude/skills/` (copied, never edited).
This skill is the house layer on top: the workflow, the house rules, the pipeline scripts, and the
two finished projects you can copy as templates.

## House rules (always)

1. **No em dashes** in any script line, caption or on-screen text. Use commas, periods or "and".
   Check before render: `grep -rl "—" videos/<project>/compositions videos/<project>/script.json` must print nothing.
2. **Do not invent** claims, numbers, clients, testimonials, logos or branding. Dummy values are labeled
   `DEMO DATA` / `SYNTHETIC EXAMPLE` on screen. No "100% accurate", no promised revenue lift.
3. Reference PDFs and reference videos are **references only**. Adapt to the project, never copy blindly.
4. Storyboard first, build after approval, then review, fix, export (unless the user says "just make it").
5. Answer the user in short, simple Banglish. Ask only what is needed.

## Workflow (the user's 14 steps, condensed)

1. Brief: company, video type, goal, duration, format, voiceover / music / SFX, colors, font, references, assets, CTA.
2. Pick a template project (below) or start fresh with `npx hyperframes init videos/<name> --non-interactive --example=blank`.
3. Write `script.json` (one entry per caption line, grouped by scene). Show it plus a scene list as the storyboard.
4. After approval: voice, build, sfx, music, check, snapshot, render, loudness normalize (commands below).
5. Review the snapshots and a tile of rendered frames, fix, re-render, deliver `exports/*.mp4`.
6. Commit and push the project folder, including the export and a project `README.md`.

Video type notes:
- **Talking head**: user footage required. Clean cuts, pacing, silence removal, B-roll, captions, graphics, SFX, music.
  Route through `/hyperframes` (talking-head-recut or embedded-captions) and keep footage under `assets/`.
- **SaaS / product**: footage optional. UI animation, motion graphics, typography, product flow, transitions.
- **Faceless / explainer**: everything invented. This is what both template projects are.

## Template projects

| Project | Style | Use when |
| --- | --- | --- |
| `videos/conversion-tracking-portfolio` | **dark-tech**: navy, blue accent, Inter, calm fades, ambient pad | serious / technical / B2B explainer |
| `videos/abu-hanif-fiverr-intro` | **dark premium agency**: particles, glass panels, Inter, blue/cyan, blur transitions, cinematic music, exact 50 s | Fiverr gig intro, high-end SaaS / agency feel |
| `videos/conversion-tracking-promo` | **color-block promo** (after the Outwitly reference): magenta, orange, lime, plum, cream, Montserrat 800, paper cards, asterisk mark, circle wipes, word-highlight captions, upbeat music, SFX | energetic agency / personal-brand promo |

Copy one: `cp -r videos/conversion-tracking-promo videos/<new>` then delete `renders/ snapshots/ exports/`,
rename in `package.json` + `meta.json`, rewrite `script.json`, and rewrite the scene files in `compositions/`.
Design tokens and scene patterns for the promo style: `docs/style-color-block-promo.md`.

## Pipeline (run from the project folder)

```bash
python3 scripts/voice.py      # script.json -> assets/audio/voice.wav + timings.json (exact per-line times)
node scripts/build.mjs        # index.html + captions + injects cues into compositions/*.html (+ sfx.json in promo)
python3 scripts/sfx.py        # promo only: sfx.json -> assets/audio/sfx.wav
python3 scripts/music.py      # music bed sized to timings.json
npx hyperframes lint && npx hyperframes check
npx hyperframes snapshot --at 4,15,30,...   # then Read snapshots/contact-sheet*.jpg
npx hyperframes render --quality high --fps 30 --output renders/video.mp4
ffmpeg -y -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k \
  -movflags +faststart exports/<name>-1080p.mp4
```

How timing works: `voice.py` synthesizes each `script.json` line separately (Kokoro, local), so every
line's start and end are exact. `build.mjs` writes those as `const K = /*CUES*/{c:[...], d, w}/*END*/`
inside each scene file. Scene animation is keyed to `c[i]` (start of line i, scene-local seconds), so
changing the script or voice re-syncs everything automatically. Never hand-edit the CUES block.

Promo-only extras in `build.mjs`:
- Scenes overlap by `WIPE` (0.6 s); each scene circle-wipes in over the previous one (`K.w`).
- Each scene declares its sound effects inline:
  `const SFX = /*SFX*/[["pop","c[1]+0.2", 0.7], ...]/*ENDSFX*/;` (name, scene-local time expression, optional gain).
  A `whoosh` is added automatically at every scene wipe.
  Names: `whoosh` (scene / panel wipe), `swoosh` (card slide), `pop` (element appears), `tick` (check, step),
  `ding` (success), `thud` (error, mismatch, broken).
- Captions are a sub-composition (`compositions/captions.html`) with the spoken word highlighted
  (word times estimated from word length inside each exact line window).

### Audio-only remix (no video re-render)

```bash
ffmpeg -y -i renders/video.mp4 -i assets/audio/voice.wav -i assets/audio/music.wav -i assets/audio/sfx.wav \
  -filter_complex "[1:a]aresample=48000,aformat=channel_layouts=stereo[v];[2:a]aresample=48000,volume=0.16[m];[3:a]aresample=48000,volume=0.3[s];[v][m][s]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart exports/<name>-1080p.mp4
```
Keep the volumes equal to the `data-volume` values in `build.mjs`. Current mix: voice 1.0, music 0.16, sfx 0.3.

## Environment gotchas (cloud sessions)

- CDN (jsdelivr) is blocked for the headless renderer: GSAP is vendored at `assets/gsap.min.js`. Keep it local.
- First render needs `npx hyperframes browser ensure` (downloads Chrome headless shell).
- TTS: `pip install kokoro-onnx soundfile`; the model downloads on the first `npx hyperframes tts "hi" -o /tmp/x.wav`.
  Not signed in to HeyGen, so voices are local Kokoro (`am_michael`). A real recording is better: drop it in as
  `assets/audio/voice.wav`, but then timings must come from transcription (whisper) instead of `voice.py`.
- Fonts that resolve automatically: Inter, Montserrat, JetBrains Mono. Other named fonts need an `@font-face` to a local file.
- `check` contrast warnings on big decorative headlines (orange on magenta) are accepted for the promo style.
- Music and SFX are synthesized in Python (no samples), so there is no licensing issue.

## Using the user's own voice

Best to worst realism:
1. **Real recording of the script.** Put it at `assets/audio/voice.wav`; timings must then come from transcription
   (whisper), not `voice.py`. Most real, no account needed.
2. **Cloud voice clone (HeyGen or ElevenLabs).** Needs an API key and network access to `api.heygen.com` /
   `api.elevenlabs.io` (blocked in the default cloud environment; the user must add the domain under the
   environment's Network access > Allowed domains). HeyGen: `node .claude/skills/media-use/audio/scripts/heygen-voice.mjs clone take.mp3 --name "Shakil"`
   then `heygen-tts.mjs --voice <id>` (returns word timestamps too). Needs 1 to 2 min of clean speech.
3. **Local FreeVC (free, works offline here).** `scripts/clone_voice.py` in `videos/conversion-tracking-promo`
   converts the Kokoro narration line by line into the timbre of `voice-ref/ref.wav` with identical timing,
   so only an audio remix is needed (no video re-render). Measured speaker similarity to the user's recording:
   Kokoro 0.61, FreeVC 0.76 (same person is usually 0.8+). Sounds closer, not identical. Accent and rhythm stay Kokoro's.
   Setup and the ref-cleaning ffmpeg command are in the script header. huggingface.co is blocked here, so
   XTTS / F5 / OpenVoice cannot be downloaded; FreeVC weights come from GitHub releases.

Privacy: the user's raw recording (`voice-ref/`), `voice-clone.wav` and `*myvoice*` exports are git-ignored.
Ask the user before committing any of them.

## Talking-head edit recipe (user sends a raw or captioned clip)

Template: `videos/asad-fiverr-gig` (copy it). Steps:
1. Probe + contact sheet: `ffmpeg -vf "fps=30/<dur>,scale=320:-1,tile=6x5"` and one full frame to find free zones
   (where the person is not, where burned captions and watermarks sit).
2. Timing: whisper is blocked here. If the clip has burned-in captions, OCR them (rapidocr-onnxruntime, see the
   project README). Otherwise ask the user for the script, or use `voice.py --recording` style silence splitting.
3. Footage: video track muted (`assets/footage/raw.mp4`), voice extracted + cleaned to `assets/audio/voice.wav`.
4. Camera in `index.html` root timeline on wrappers (`#ft-zoom` punch-ins, `#ft-frame` split screen), never on the `<video>`.
5. All cards / slides / SFX in one `compositions/overlays.html` at absolute times. Keep cards out of the caption band.
6. Render with `--workers 4`, loudnorm, check a tile of rendered frames.
Never add a claim the speaker did not make; soften absolutes in graphics (speaker said "100% accurate", card says "Accurate tracking").
Client footage and exports stay git-ignored unless the user says to push them.

## Log

- 2026-10-09: Installed HyperFrames skills. Built `conversion-tracking-portfolio` (dark-tech, from the PDF playbook).
- 2026-10-09: Built `conversion-tracking-promo` (color-block promo after the Outwitly reference) with SFX and upbeat music.
- 2026-10-09: Added local voice clone (FreeVC) from the user's 58 s phone recording, `exports/conversion-tracking-promo-myvoice-1080p.mp4` (kept local).
- 2026-10-09: Added `kit/` (setup, new-video, make with 4 render workers, voice.py recording mode) and `library/` (hooks, graphics, voice). User feedback: FreeVC clone still sounds AI, prefer real recording.
- 2026-10-10: Edited `videos/asad-fiverr-gig` (talking-head Fiverr gig, 53.5 s): OCR timing from burned captions, punch-ins, split screen, synced cards, music, SFX. Render 2 min 49 s. Footage kept local.
- 2026-10-10: Built `videos/abu-hanif-fiverr-intro` from the 50 s high-end Fiverr intro PDF brief (dark premium, exact 50.0 s, render 1 min 31 s). Added `premium` template to kit/new-video.sh and a `cinematic` music mode (script.json "music").
