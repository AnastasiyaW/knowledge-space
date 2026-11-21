---
title: "Inworld Voice Isolator: inworld-voice-isolator-release — Inworld Voice Isolator Release"
category: "projects"
date: 2026-11-19
tags: ["inworld-voice-isolator", "inworld-voice-isolator-release", "project"]
aliases: ["Inworld Voice Isolator: inworld-voice-isolator-release"]
---

# Inworld Voice Isolator: inworld-voice-isolator-release — Inworld Voice Isolator Release

Inworld Voice Isolator is an open-source speech denoising library that separates voice from background, an alternative to DeepFilterNet and Demucs.

**Development line:** project:inworld-voice-isolator · thread inworld-voice-isolator-release  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: high

## What it is

Inworld Voice Isolator is an open-source neural speech denoising library for post-production engineers and real-time streaming pipelines. It separates vocal tracks from background noise and music. It competes directly with DeepFilterNet and Demucs.

What it does:

- Offline batch processing: works in eight-second chunks.
- Causal streaming: low look-ahead, built for interactive agents.
- Two outputs at once: isolated speech and the residual background audio.
- Natural voice: keeps inflections such as laughter and breathing.

Input is 48 kHz single-channel audio. The models are 58M and 64M parameters. The library suppresses noise and does not synthesize or extend missing frequency bands.

The license is Apache 2.0, so it is a permissive baseline for developers who need low-latency speech cleaning without proprietary cloud dependencies.

## Development line

- **2026-11-19 — Inworld releases open Voice Isolator speech denoising model.** Inworld published Voice Isolator, an open speech-cleaning model. It takes a 48 kHz single-channel input and outputs the voice and the removed background separately. It ships an offline checkpoint (64M parameters) and a realtime checkpoint (58M parameters). The realtime one is causal, with 63 ms latency and 20 ms lookahead. The model was trained on 10,000 hours of speech. It does not restore lost frequency bands.
- **2026-11-19 — Inworld releases open Voice Isolator speech denoising model.** An open speech-cleaning model named Voice Isolator was published with offline (64M parameters) and realtime (58M parameters) checkpoints. It processes 48 kHz mono audio and separates voice from background. It was trained on 10,000 hours of speech. Code and weights are linked on Hugging Face and GitHub.
- **2026-11-19 — other reporting on this date.**
  - The release is under the Apache 2.0 license. The checkpoints are voice-isolator-v1 (64M parameters, offline batching in 8-second chunks) and voice-isolator-v1-realtime (58M parameters, causal streaming). Both keep speech nuance such as breaths and laughs. (2026-11-19) — <https://github.com/inworld-ai/voice-isolator>
  - The realtime variant is causal, with 63 ms latency and 20 ms look-ahead. It is distributed on PyPI as inworld-voice-isolation, with a voice-isolate CLI tool that writes 48 kHz float32 voice and background tracks. (2026-11-19) — <https://github.com/inworld-ai/voice-isolator>

## What changed

The first release comes with two open models: one for batch fidelity, one for causal latency. The offline checkpoint is made for dataset cleaning and media post-production. The streaming variant is made for interactive voice agents. Distribution is an open license, a Python package you install directly, and standard Hugging Face weights, with no gated commercial API.

## How to use this

1. Install with `pip install inworld-voice-isolation`, or clone the GitHub repository and run `pip install -e .`.
  — <https://github.com/inworld-ai/voice-isolator>
2. Clean audio from the terminal with `voice-isolate input_audio.wav clean_output.wav`. It writes 48 kHz `clean_output.wav` and `clean_output_background.wav`.
  — <https://github.com/inworld-ai/voice-isolator>
3. In Python, create `voice_isolation.VoiceIsolator('inworld/voice-isolator')`, load audio with `voice_isolation.load_audio()`, and call `isolate()` on the waveform.
  — <https://github.com/inworld-ai/voice-isolator>

## Best practices

- Use the 64M offline checkpoint (voice-isolator-v1) with 8-second windows for batch post-production and dataset cleaning, so isolation quality is highest.
  — <https://github.com/inworld-ai/voice-isolator>
- Use the causal 58M checkpoint (voice-isolator-v1-realtime) for real-time voice bots and live streams, so latency stays at 63 ms with 20 ms look-ahead.
  — <https://github.com/inworld-ai/voice-isolator>
- Feed single-channel 48 kHz float32 audio. Do not expect spectral restoration: the model isolates the speech that is present and does not rebuild lost high-frequency bands.
  — <https://github.com/inworld-ai/voice-isolator>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Independent benchmarks against other speech enhancement models (such as DeepFilterNet3 or Demucs) are not yet available.
- Field reports and edge cases from production telephony or browser WebRTC setups are still limited after the recent open-source release.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/inworld-ai/voice-isolator | inworld-ai/voice-isolator: Open-source 48kHz speech denoising and voice isolation | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:inworld-voice-isolator, thread inworld-voice-isolator-release, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
