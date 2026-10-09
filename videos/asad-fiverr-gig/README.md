# Asad Fiverr gig video (talking-head edit)

Input: 51 s talking-head clip (1280x720, 60 fps) with burned-in cyan captions and a Fiverr watermark.
Output: `exports/asad-fiverr-gig-1080p.mp4` (1920x1080, 30 fps, H.264, AAC, -16 LUFS, 53.5 s).

Client footage, so `assets/footage/`, `assets/audio/voice.wav` and `exports/` are git-ignored (kept local).

## What the edit adds (color-block promo style)

- Punch-in zooms on key words, slow push-ins, a split-screen beat (footage shrinks into a rounded frame on magenta).
- Cards synced to the speech: name lower-third, services, 7+ years stat, who I help, visibility and sales,
  full lime slide "Data-driven digital marketing strategy", "How I work" 5 steps with a sliding highlight,
  one-stop solution, Message me button with cursor click, intro session checklist, end card.
- Voice cleanup (high-pass, low-pass, compressor, loudness), upbeat synthesized music at 0.12, 40 synthesized SFX.

## How the timing was found

Whisper and online speech-to-text are blocked in the cloud box, so the burned-in captions were read with OCR:

```bash
pip install rapidocr-onnxruntime   # models ship inside the wheel
ffmpeg -i in.mp4 -vf "fps=10,crop=1280:200:0:500" f/%05d.png   # caption band only
# python: RapidOCR() on every frame, merge identical consecutive text -> transcript-ocr.json (start, end, text)
```

## Rebuild

```bash
ffmpeg -i <source>.mp4 -an -c:v copy assets/footage/raw.mp4
ffmpeg -i <source>.mp4 -vn -af "highpass=f=80,lowpass=f=10000,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-18:TP=-2" -ar 48000 -ac 1 assets/audio/voice.wav
node scripts/build-sfx.mjs && python3 scripts/sfx.py && python3 scripts/music.py
npx hyperframes lint
npx hyperframes render --quality high --fps 30 --workers 4 --output renders/video.mp4
ffmpeg -y -i renders/video.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart exports/asad-fiverr-gig-1080p.mp4
```

Camera moves live in `index.html` (root timeline); every card, slide and SFX time lives in `compositions/overlays.html`.
