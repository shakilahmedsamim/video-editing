"""Synthesize an original music bed sized to timings.json. Style from script.json "music":
  "pop" (default): upbeat light pop, 100 BPM, C G Am F.
  "cinematic": darker tech / motivational, 92 BPM, Am F C G, soft pad, softer drums.

Kick on every beat, soft clap on 2 and 4, offbeat hats, plucked chords (C G Am F), sub bass.
No samples, no licensing. Usage: python3 scripts/music.py -> assets/audio/music.wav
"""
import json
import numpy as np
import soundfile as sf

SR = 44100
STYLE = json.load(open("script.json")).get("music", "pop") if __import__("os").path.exists("script.json") else "pop"
BPM = 92 if STYLE == "cinematic" else 100
total = json.load(open("timings.json"))["total"]
n = int(total * SR)
beat = 60 / BPM
rng = np.random.default_rng(11)
out = np.zeros(n + SR * 2)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def add(sig, t):
    i = int(t * SR); j = min(i + len(sig), len(out))
    if i < len(out):
        out[i:j] += sig[: j - i]

def decay(sec, d):
    t = np.arange(int(sec * SR)) / SR
    return t, np.exp(-t / d)

t, e = decay(0.35, 0.09)
kick = np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-t / 0.03)) / SR) * e
t, e = decay(0.2, 0.05)
clap = rng.standard_normal(len(t)) * e * 0.35
t, e = decay(0.06, 0.012)
hat = np.diff(rng.standard_normal(len(t) + 1)) * e * 0.12

def pluck(m, sec=0.45):
    t, e = decay(sec, 0.16)
    f = hz(m)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)) * e * 0.16

def bass(m, sec):
    t = np.arange(int(sec * SR)) / SR
    a = np.minimum(1, t / 0.01) * np.minimum(1, (sec - t) / 0.05)
    return np.sin(2 * np.pi * hz(m) * t) * a * 0.35

prog = [(60, [60, 64, 67, 72]), (55, [55, 59, 62, 67]), (57, [57, 60, 64, 69]), (53, [53, 57, 60, 65])]
if STYLE == "cinematic":
    prog = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (60, [60, 64, 67, 72]), (55, [55, 59, 62, 67])]

def pad(notes, sec):
    t = np.arange(int(sec * SR)) / SR
    a = np.minimum(1, t / 1.2) * np.minimum(1, (sec - t) / 1.0)
    return sum(np.sin(2 * np.pi * hz(m) * t) + 0.3 * np.sin(2 * np.pi * hz(m) * 1.003 * t) for m in notes) * a * 0.05
bars = int(total / (4 * beat)) + 2
for b in range(bars):
    root, ch = prog[b % 4]
    t0 = b * 4 * beat
    for k in range(4):
        add(kick * 0.8, t0 + k * beat)
        add(hat, t0 + k * beat + beat / 2)
        if k in (1, 3):
            add(clap * (0.45 if STYLE == "cinematic" else 1), t0 + k * beat)
    add(bass(root - 24, 4 * beat * 0.95), t0)
    if STYLE == "cinematic":
        add(pad([n - 12 for n in ch[:3]], 4 * beat + 1.0), t0)
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]  # eighth-note arpeggio
    for k, idx in enumerate(pattern):
        add(pluck(ch[idx]) * (0.7 if STYLE == "cinematic" else 1), t0 + k * beat / 2)

out = out[:n]
tt = np.arange(n) / SR
out *= np.clip(np.minimum(tt / 1.5, (total - tt) / 3.0), 0, 1)
out = np.tanh(out * 1.2)
out = out / np.max(np.abs(out)) * 0.6
sf.write("assets/audio/music.wav", np.stack([out, out], 1).astype(np.float32), SR)
print("music", STYLE, round(total, 2), "s @", BPM, "bpm")
