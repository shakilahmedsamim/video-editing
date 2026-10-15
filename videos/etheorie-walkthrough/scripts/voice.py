"""One narration clip per segment (the Say line), local Kokoro TTS. Writes assets/audio/vo/<id>.wav and vo.json.
Usage: python3 scripts/voice.py   (or --recording-dir DIR with <id>.wav files recorded by a person)
"""
import json, os, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
cfg = json.load(open("steps.json"))
C = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(f"{C}/models/kokoro-v1.0.onnx", f"{C}/voices/voices-v1.0.bin")
os.makedirs("assets/audio/vo", exist_ok=True)
out = {}
for s in cfg["segments"]:
    if not s.get("say"):
        continue
    a, sr = k.create(s["say"], voice=cfg["voice"], speed=cfg["speed"], lang="en-us")
    idx = np.where(np.abs(a) > 0.004)[0]
    a = a[max(idx[0] - 480, 0): idx[-1] + 1440].astype(np.float32)
    a = a / np.max(np.abs(a)) * 0.89
    sf.write(f"assets/audio/vo/{s['id']}.wav", a, sr)
    out[s["id"]] = round(len(a) / sr, 3)
    print(f"{s['id']:7s} {out[s['id']]:6.2f}s")
json.dump(out, open("vo.json", "w"), indent=1)
print("total VO", round(sum(out.values()), 1), "s")
