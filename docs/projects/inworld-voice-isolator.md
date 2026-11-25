---
title: "Inworld Voice Isolator: inworld-voice-isolator-release — Inworld Voice Isolator Release"
category: "projects"
date: 2026-11-19
tags: ["inworld-voice-isolator", "inworld-voice-isolator-release", "project"]
aliases: ["Inworld Voice Isolator: inworld-voice-isolator-release"]
---

# Inworld Voice Isolator: inworld-voice-isolator-release — Inworld Voice Isolator Release

**Development line:** project:inworld-voice-isolator · thread inworld-voice-isolator-release  
**Last event:** 2026-11-19 · 1 dated since 2026-11-19 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Inworld Voice Isolator is an Apache-2.0 Python package for engineers cleaning recorded or live speech before transcription, playback, or dataset curation.

- Foreground voice: isolates speech from background noise.
- Background track: writes the removed background audio separately.
- Processing modes: offers offline and causal streaming checkpoints.

The offline checkpoint has 64M parameters; the realtime checkpoint has 58M parameters, 63 ms algorithmic latency, and 20 ms lookahead for single-channel 48 kHz audio. It is neither a target-speaker selector nor a restoration model.

Use it for speech cleanup when preserving the recorded voice matters; evaluate another tool for severely degraded audio, target-speaker extraction, or lost-bandwidth repair.

## Development line

- **2026-11-19 — Inworld releases open Voice Isolator speech denoising model.** Inworld published Voice Isolator, an open speech-cleaning model that takes a 48 kHz single-channel input and outputs the voice and the removed background separately. It ships offline (64M parameters) and realtime (58M parameters) checkpoints. The realtime variant is causal with 63 ms latency and 20 ms lookahead. The model was trained on 10,000 hours of speech and does not restore lost frequency bands.
  - The dated launch post identifies Voice Isolator as Inworld's first open-source model, released with Apache-2.0 code and weights. It also reports vendor VIBE scores of 0.768 for offline and 0.718 for realtime; VIBE is private, so these are vendor benchmark results rather than independent validation. (2026-11-18) — <https://inworld.ai/blog/introducing-voice-isolator>

## What changed

Inworld released Voice Isolator v1 with two Apache-2.0 checkpoints for offline and streaming 48 kHz denoising; no later dated version is verified.

## How to use this

1. Install the package with `pip install inworld-voice-isolation`; weights download on first use.
  — <https://github.com/inworld-ai/voice-isolator>
2. For a 48 kHz mono recording, run `voice-isolate input.wav clean.wav`; it writes the isolated voice and, by default, a separate background residual.
  — <https://github.com/inworld-ai/voice-isolator>
3. For streaming, create `VoiceIsolator(..., mode="streaming", lookahead_frames=2)`, push 20 ms chunks to a session, then flush it when the source ends.
  — <https://github.com/inworld-ai/voice-isolator>

## Best practices

- Test representative difficult recordings against a baseline before deployment. One practitioner reported word hallucinations on a very noisy sample and preferred Demucs for that case.
  — <https://www.reddit.com/r/LocalLLaMA/comments/1xzqpzu/new_voice_isolation_model_from_inworld/>

## What practitioners say

- One practitioner reported that a very noisy sample produced hallucinated words and preferred Demucs for severely degraded audio. (2026-11-18)
  — <https://www.reddit.com/r/LocalLLaMA/comments/1xzqpzu/new_voice_isolation_model_from_inworld/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No independent benchmark or controlled evaluation was found for the vendor-reported VIBE scores.
- No later dated release beyond the initial v1 launch was verified.
- No qualifying Simplified-Chinese primary or practitioner source was verified.

## Sources

| source | title | read |
|---|---|---|
| https://inworld.ai/blog/introducing-voice-isolator | Introducing Voice Isolator: open-source 48 kHz denoising | 2026-11-25 |
| https://github.com/inworld-ai/voice-isolator | inworld-ai/voice-isolator | 2026-11-25 |
| https://huggingface.co/inworld/voice-isolator | inworld/voice-isolator | 2026-11-25 |
| https://www.reddit.com/r/LocalLLaMA/comments/1xzqpzu/new_voice_isolation_model_from_inworld/ | New voice isolation model from Inworld | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:inworld-voice-isolator, thread inworld-voice-isolator-release, 1 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
