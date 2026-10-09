"""Generate narration with local Kokoro, one clip per caption line, and write exact timings.

Usage: python3 scripts/voice.py   (run from the project root)
Outputs: assets/audio/voice.wav, timings.json
"""
import json, os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

CACHE = os.path.expanduser("~/.cache/hyperframes/tts")
GAP = 0.4  # silence between lines inside a scene (s)

cfg = json.load(open("script.json"))
k = Kokoro(f"{CACHE}/models/kokoro-v1.0.onnx", f"{CACHE}/voices/voices-v1.0.bin")
sr = 24000
out, t, scenes = [], 0.0, []

def silence(sec):
    return np.zeros(int(round(sec * sr)), dtype=np.float32)

def trim(a, thr=0.004):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    s = max(idx[0] - int(0.02 * sr), 0)
    e = min(idx[-1] + int(0.06 * sr), len(a))
    return a[s:e]

for sc in cfg["scenes"]:
    start = t
    out.append(silence(sc["lead"])); t += sc["lead"]
    lines = []
    for i, text in enumerate(sc["lines"]):
        a, sr = k.create(text, voice=cfg["voice"], speed=cfg["speed"], lang="en-us")
        a = trim(a.astype(np.float32))
        d = len(a) / sr
        lines.append({"text": text, "start": round(t - start, 3), "end": round(t - start + d, 3),
                      "gstart": round(t, 3), "gend": round(t + d, 3)})
        out.append(a); t += d
        if i < len(sc["lines"]) - 1:
            out.append(silence(GAP)); t += GAP
    out.append(silence(sc["tail"])); t += sc["tail"]
    scenes.append({"id": sc["id"], "start": round(start, 3), "duration": round(t - start, 3), "lines": lines})
    print(f'{sc["id"]:10s} {start:7.2f}s  +{t - start:6.2f}s')

audio = np.concatenate(out)
peak = np.max(np.abs(audio))
audio = audio / peak * 0.89  # about -1 dBFS
os.makedirs("assets/audio", exist_ok=True)
sf.write("assets/audio/voice.wav", audio, sr)
json.dump({"total": round(t, 3), "scenes": scenes}, open("timings.json", "w"), indent=2)
print(f"total {t:.2f}s")
