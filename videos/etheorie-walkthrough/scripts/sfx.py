"""Render sfx.json (written by build.mjs) into one synthesized sound-effects track.

All sounds are generated here (no samples, no licensing). Names:
  whoosh  - scene circle-wipe            pop   - card / element appears
  tick    - checkmark / step activates   ding  - success / confirmed
  thud    - error / broken / mismatch    swoosh - short slide
Usage: python3 scripts/sfx.py   ->  assets/audio/sfx.wav
"""
import json
import numpy as np
import soundfile as sf

SR = 48000
rng = np.random.default_rng(3)

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def lowpass(x, alpha):
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])
    return y

def bandsweep(n, f0, f1):
    # noise through a moving one-pole band (cheap, smooth)
    noise = rng.standard_normal(n)
    out = np.zeros(n); lp = 0.0; lp2 = 0.0
    fs = np.geomspace(f0, f1, n)
    for i in range(n):
        a = min(0.99, 2 * np.pi * fs[i] / SR)
        lp += a * (noise[i] - lp)
        lp2 += a * 0.5 * (lp - lp2)
        out[i] = lp - lp2
    return out

def whoosh():
    n = int(0.75 * SR); t = np.arange(n) / SR
    up = np.concatenate([bandsweep(n // 2, 300, 4000), bandsweep(n - n // 2, 4000, 600)])
    e = np.sin(np.pi * np.clip(t / 0.75, 0, 1)) ** 2
    return up * e * 1.4

def swoosh():
    n = int(0.32 * SR); t = np.arange(n) / SR
    return bandsweep(n, 1200, 5000) * np.sin(np.pi * t / 0.32) ** 2 * 1.1

def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 520 + 700 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.035) * 0.9

def tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2600 * t) + 0.5 * rng.standard_normal(n)) * env(n, 0.0005, 0.008) * 0.7

def ding():
    n = int(0.9 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t) + 0.25 * np.sin(2 * np.pi * 2637 * t)
    return s * env(n, 0.003, 0.22) * 0.45

def thud():
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 90 + 120 * np.exp(-t / 0.04)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR)
    buzz = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.15
    return (body + buzz) * env(n, 0.002, 0.08) * 1.0

BANK = {"whoosh": whoosh(), "swoosh": swoosh(), "pop": pop(), "tick": tick(), "ding": ding(), "thud": thud()}

cfg = json.load(open("sfx.json"))
out = np.zeros(int((cfg["total"] + 2) * SR))
for ev in cfg["events"]:
    s = BANK[ev["name"]] * ev.get("gain", 1)
    i = max(int(ev["t"] * SR), 0)
    j = min(i + len(s), len(out))
    out[i:j] += s[: j - i]
out = out[: int(cfg["total"] * SR)]
out = out / max(np.max(np.abs(out)), 1e-6) * 0.8
sf.write("assets/audio/sfx.wav", np.stack([out, out], 1).astype(np.float32), SR)
print(f"sfx: {len(cfg['events'])} events")
