# Conversion Tracking portfolio video

Final export: `exports/conversion-tracking-portfolio-1080p.mp4` (1920x1080, 30 fps, H.264, AAC, -16 LUFS).

## Rebuild

```bash
python3 scripts/voice.py      # script.json -> assets/audio/voice.wav + timings.json (Kokoro TTS)
python3 scripts/music.py      # ambient bed sized to the narration
node scripts/build.mjs        # index.html + captions, injects line cue times into compositions/*.html
npx hyperframes check
npx hyperframes render --quality high --fps 30 --output renders/video.mp4
ffmpeg -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k \
  -movflags +faststart exports/conversion-tracking-portfolio-1080p.mp4
```

Edit narration in `script.json` (one entry per caption line). Scene visuals live in `compositions/<scene>.html`
and key their animation to the line cues, so they re-sync automatically after a voice change.
