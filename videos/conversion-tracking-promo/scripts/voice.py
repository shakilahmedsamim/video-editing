"""Build the narration track and exact per-line timings from script.json.

Two sources:
  python3 scripts/voice.py                          # AI voice (local Kokoro TTS)
  python3 scripts/voice.py --recording my-take.m4a  # YOUR real voice (most natural)

Recording mode: read script.json top to bottom in ONE take and pause about 1 second after every line
(any phone recording works). The take is cleaned (high-pass, light denoise, loudness), split on the
pauses, and segment N becomes line N. The number of segments must equal the number of lines; the script
searches silence settings until it matches and tells you which line count it found if it cannot.

Outputs: assets/audio/voice.wav, timings.json (same format in both modes, so build.mjs never changes).
"""
import argparse, json, os, re, subprocess, tempfile
import numpy as np
import soundfile as sf

GAP = 0.4  # silence placed between lines inside a scene (s)
SR = 24000

ap = argparse.ArgumentParser()
ap.add_argument("--recording", help="your own read of the whole script, any audio format")
args = ap.parse_args()

cfg = json.load(open("script.json"))
lines_flat = [t for sc in cfg["scenes"] for t in sc["lines"]]

def silence(sec):
    return np.zeros(int(round(sec * SR)), dtype=np.float32)

def trim(a, thr=0.004):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    return a[max(idx[0] - int(0.02 * SR), 0): min(idx[-1] + int(0.06 * SR), len(a))]

def clips_from_tts():
    from kokoro_onnx import Kokoro
    cache = os.path.expanduser("~/.cache/hyperframes/tts")
    k = Kokoro(f"{cache}/models/kokoro-v1.0.onnx", f"{cache}/voices/voices-v1.0.bin")
    out = []
    for text in lines_flat:
        a, sr = k.create(text, voice=cfg.get("voice", "am_michael"), speed=cfg.get("speed", 0.92), lang="en-us")
        assert sr == SR
        out.append(trim(a.astype(np.float32)))
    return out

def clips_from_recording(path):
    tmp = tempfile.mkdtemp()
    clean = f"{tmp}/clean.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-af",
                    "highpass=f=70,afftdn=nf=-25,loudnorm=I=-18:TP=-2", "-ar", str(SR), "-ac", "1", clean], check=True)
    audio, _ = sf.read(clean, dtype="float32")
    want = len(lines_flat)
    tried = []
    for d in (0.6, 0.5, 0.7, 0.45, 0.8, 0.4, 0.9, 1.0):
        for n in (-35, -38, -32, -40, -30):
            r = subprocess.run(["ffmpeg", "-nostats", "-i", clean, "-af", f"silencedetect=n={n}dB:d={d}", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
            starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
            ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
            # speech = gaps between silences
            edges, t = [], 0.0
            for s, e in zip(starts, ends + [None] * (len(starts) - len(ends))):
                if s - t > 0.25:
                    edges.append((t, s))
                t = e if e is not None else len(audio) / SR
            if len(audio) / SR - t > 0.25:
                edges.append((t, len(audio) / SR))
            tried.append(len(edges))
            if len(edges) == want:
                print(f"split take into {want} lines (silence {n} dB, {d} s)")
                return [trim(audio[int(a * SR): int(b * SR)], thr=0.01) for a, b in edges]
    raise SystemExit(f"Could not split the recording into {want} lines (found {sorted(set(tried))}). "
                     "Re-record with a clear ~1 s pause after every line and no long pauses inside a line, "
                     "or add/merge lines in script.json to match.")

clips = clips_from_recording(args.recording) if args.recording else clips_from_tts()

out, t, scenes, i = [], 0.0, [], 0
for sc in cfg["scenes"]:
    start = t
    out.append(silence(sc["lead"])); t += sc["lead"]
    lines = []
    for j, text in enumerate(sc["lines"]):
        a = clips[i]; i += 1
        d = len(a) / SR
        lines.append({"text": text, "start": round(t - start, 3), "end": round(t - start + d, 3),
                      "gstart": round(t, 3), "gend": round(t + d, 3)})
        out.append(a); t += d
        if j < len(sc["lines"]) - 1:
            out.append(silence(GAP)); t += GAP
    out.append(silence(sc["tail"])); t += sc["tail"]
    scenes.append({"id": sc["id"], "start": round(start, 3), "duration": round(t - start, 3), "lines": lines})
    print(f'{sc["id"]:10s} {start:7.2f}s  +{t - start:6.2f}s')

audio = np.concatenate(out)
audio = audio / np.max(np.abs(audio)) * 0.89
os.makedirs("assets/audio", exist_ok=True)
sf.write("assets/audio/voice.wav", audio, SR)
json.dump({"total": round(t, 3), "source": "recording" if args.recording else "tts", "scenes": scenes},
          open("timings.json", "w"), indent=2)
print(f"total {t:.2f}s  ({'your recording' if args.recording else 'Kokoro TTS'})")
