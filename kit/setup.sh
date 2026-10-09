#!/usr/bin/env bash
# One-time setup for a fresh cloud session (about 1 to 2 minutes). Safe to re-run.
set -euo pipefail
pip install --quiet kokoro-onnx soundfile librosa 2>&1 | grep -v -i warn || true
npx --yes hyperframes browser ensure >/dev/null
# warm the Kokoro model download (~330 MB) so the first video does not wait on it
npx --yes hyperframes tts "ready" -o /tmp/hf-warm.wav >/dev/null 2>&1 || true
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
echo "setup ok"
# Optional, only for the local voice clone (kit/scripts/clone_voice.py), ~3 GB:
#   pip install torch torchaudio torchcodec coqui-tts "transformers>=4.57,<5" "setuptools<81" resemblyzer
