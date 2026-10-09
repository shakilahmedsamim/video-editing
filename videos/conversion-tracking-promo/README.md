# Conversion Tracking promo (color-block style)

Final export: `exports/conversion-tracking-promo-1080p.mp4` (1920x1080, 30 fps, H.264, AAC, -16 LUFS, 2:12).

Same script and voice as `../conversion-tracking-portfolio`, restyled after the Outwitly agency promo reference:
saturated color-block scenes (magenta / orange / lime / plum / cream), heavy Montserrat headlines, floating
white "paper" cards, rotating asterisk mark, circle-wipe transitions, word-highlight captions,
upbeat synthesized music and synthesized sound effects.

## Rebuild

```bash
python3 scripts/voice.py      # script.json -> assets/audio/voice.wav + timings.json
node scripts/build.mjs        # index.html, compositions/captions.html, cue injection, sfx.json
python3 scripts/sfx.py        # sfx.json -> assets/audio/sfx.wav
python3 scripts/music.py      # upbeat bed sized to the narration
npx hyperframes check
npx hyperframes render --quality high --fps 30 --output renders/video.mp4
ffmpeg -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k \
  -movflags +faststart exports/conversion-tracking-promo-1080p.mp4
```

Audio-only change (music, sfx levels)? Skip the video render and remix onto `renders/video.mp4`
(see `.claude/skills/video-editor/SKILL.md`, "Audio-only remix").

## Scenes (compositions/)

| Scene | Look | Content |
| --- | --- | --- |
| hook | magenta, then orange panel wipe | Wrong conversion data? 48 vs 31 cards, lead not recorded, where does the data break |
| intro | cream | Hi, I'm Shakil Ahmed Samim, orange role pill, Website > GTM > Analytics / Ads / CRM |
| stack | lime | The tracking stack, 10 paper tool cards |
| problems | plum + 4 color panels | Lost click IDs, Double purchases, Events sent too early, Missing lead data, own diagnosis |
| method | cream | My workflow, orange highlight slides over Audit > Trace > Implement > Validate > Document, QA checklist + payload |
| evidence | magenta | Evidence, not guesses, 4-step proof ladder, QA documentation card |
| cta | orange, then magenta end card | Sound familiar? 3 pains, name, role, button, shakilas.com/portfolio |
