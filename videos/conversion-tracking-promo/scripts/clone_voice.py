"""Re-voice the narration in the user's own voice with local FreeVC (free, offline after first download).

Takes assets/audio/voice.wav (Kokoro, exact timings in timings.json), converts every caption line to the
timbre of voice-ref/ref.wav, and writes assets/audio/voice-clone.wav with identical timing, so the video
does not need re-timing or re-rendering (remix audio only).

Setup once:  pip install torch torchaudio torchcodec coqui-tts "transformers>=4.57,<5" librosa
Prepare ref: ffmpeg -i my-recording.m4a -af "highpass=f=80,afftdn=nf=-25,silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-40dB,loudnorm=I=-20" -ar 16000 -ac 1 voice-ref/ref.wav
Usage:       COQUI_TOS_AGREED=1 python3 scripts/clone_voice.py
"""
import json, os, tempfile
import numpy as np, librosa, soundfile as sf
from TTS.api import TTS

REF = "voice-ref/ref.wav"
T = json.load(open("timings.json"))
voice, sr = sf.read("assets/audio/voice.wav", dtype="float32")

def median_f0(y, s):
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=s)
    return float(np.nanmedian(f0))

ref16, _ = librosa.load(REF, sr=16000)
shift = 12 * np.log2(median_f0(ref16, 16000) / median_f0(librosa.resample(voice[: sr * 20], orig_sr=sr, target_sr=16000), 16000))
print(f"pitch shift {shift:+.2f} semitones")

vc = TTS("voice_conversion_models/multilingual/vctk/freevc24")
out = np.zeros_like(voice)
tmp = tempfile.mkdtemp()
for sc in T["scenes"]:
    for ln in sc["lines"]:
        a, b = int(ln["gstart"] * sr), int(ln["gend"] * sr)
        seg = librosa.resample(voice[a:b], orig_sr=sr, target_sr=16000)
        seg = librosa.effects.pitch_shift(seg, sr=16000, n_steps=shift)
        sf.write(f"{tmp}/s.wav", seg, 16000)
        vc.voice_conversion_to_file(source_wav=f"{tmp}/s.wav", target_wav=REF, file_path=f"{tmp}/o.wav")
        o, osr = sf.read(f"{tmp}/o.wav", dtype="float32")
        o = librosa.resample(o, orig_sr=osr, target_sr=sr)
        n = b - a
        o = o[:n] if len(o) >= n else np.pad(o, (0, n - len(o)))
        fade = min(240, n // 4)
        o[:fade] *= np.linspace(0, 1, fade); o[-fade:] *= np.linspace(1, 0, fade)
        out[a:b] = o
        print(f'{ln["gstart"]:7.2f}  {ln["text"][:60]}', flush=True)
out = out / np.max(np.abs(out)) * 0.89
sf.write("assets/audio/voice-clone.wav", out, sr)
print("wrote assets/audio/voice-clone.wav")
