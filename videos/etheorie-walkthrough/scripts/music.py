"""Synthesize a quiet, original ambient pad bed (no licensing issues) matching timings.json.

Usage: python3 scripts/music.py
Output: assets/audio/music.wav
"""
import json
import numpy as np
import soundfile as sf

sr = 44100
total = json.load(open("timings.json"))["total"]
n = int(total * sr)
t = np.arange(n) / sr
rng = np.random.default_rng(7)

# A minor, F, C, G  (root-position triads, low register), 8 s per chord
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
seg = 8.0
out = np.zeros(n)
for ci in range(int(np.ceil(total / seg)) + 1):
    notes = chords[ci % 4]
    s0 = ci * seg - 1.5
    s1 = s0 + seg + 3.0  # overlap for crossfade
    a, b = max(int(s0 * sr), 0), min(int(s1 * sr), n)
    if a >= b:
        continue
    tt = t[a:b] - s0
    env = np.sin(np.pi * np.clip(tt / (seg + 3.0), 0, 1)) ** 1.5
    for m in notes + [notes[0] - 12]:
        f = hz(m)
        for det in (-0.12, 0.12):
            ph = rng.uniform(0, 2 * np.pi)
            out[a:b] += env * (np.sin(2 * np.pi * f * (1 + det / 100) * tt + ph)
                               + 0.25 * np.sin(2 * np.pi * 2 * f * tt + ph))

# gentle one-pole low-pass
y = np.zeros_like(out); alpha = 0.06
for i in range(1, n):
    y[i] = y[i - 1] + alpha * (out[i] - y[i - 1])
# slow tremolo and master fades
y *= 1 + 0.08 * np.sin(2 * np.pi * 0.11 * t)
fade = np.minimum(1, t / 2.5) * np.minimum(1, (total - t) / 4.0)
y *= np.clip(fade, 0, 1)
y = y / np.max(np.abs(y)) * 0.5
sf.write("assets/audio/music.wav", np.stack([y, y], 1).astype(np.float32), sr)
print("music", total)
