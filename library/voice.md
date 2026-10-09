# Voice options

Tested on 2026-10-09 with Shakil's 58 s phone recording (only about 17 s of actual speech).

| Option | How | Sounds like you? | Notes |
| --- | --- | --- | --- |
| **Your own recording** (recommended) | `RECORDING=take.m4a kit/make.sh videos/<name>` | 100%, it is you | Read script.json top to bottom in one take, pause about 1 s after every line. voice.py cleans it, splits on the pauses and times the video to it. Tested end to end. |
| HeyGen voice clone | `heygen-voice.mjs clone` then `heygen-tts.mjs --voice <id>` (media-use skill) | very close | Needs HeyGen API key and network access to `api.heygen.com` (blocked in the default cloud environment, add it under Network access > Allowed domains). 1 to 2 min clean sample. |
| ElevenLabs voice clone | API with `xi-api-key` | very close | Needs key + `api.elevenlabs.io` allowed. |
| Local FreeVC (`kit/scripts/clone_voice.py`) | converts the Kokoro voice into your timbre | partly (similarity 0.76, user said it still sounds AI) | Free and offline, but rhythm and accent stay the AI's. Use only as a placeholder. |
| Kokoro TTS (default) | `kit/make.sh videos/<name>` | no | Male `am_michael`, speed 0.92. Fast placeholder for drafts. |

## Recording tips (for the recording option and for any clone)

- Quiet room, phone 15 to 20 cm from the mouth, same distance the whole time, no music or fan.
- One take of the full script, clear 1 s pause between lines, no long pauses inside a line.
- If a line goes wrong, pause, then repeat the whole line, and delete the bad one later (or tell Claude which).
- m4a, mp3 or wav are all fine.
