---
title: Langswap — Speech Translation and Dubbing Stack
category: projects
date: 2026-06-11
tags: [langswap, project, speech-translation-and-dubbing-stack]
aliases: ["Langswap"]
---

# Langswap — Speech Translation and Dubbing Stack

**Development line:** `project:langswap` · thread `speech-translation-and-dubbing-stack`  
**Last event:** 2026-06-11 · 1 dated since 2026-06-11 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Langswap is a local video dubbing tool for teams that need control over files and models. It handles ASR, translation, voice-cloning TTS, timing, and SRT files.

The default stack uses:
- faster-whisper large-v3 with Silero VAD for transcription and voice detection
- Gemma-4-E2B GGUF for translation
- OmniVoice for voice cloning and synthesis

It requires Python 3.12 and an NVIDIA GPU with a CUDA-13-compatible stack. Sensitive content requires manual review.

## Development line

- **2026-06-11 — Langswap organized a modular speech translation and dubbing stack.** On 2026-06-11, Langswap linked source paths for a speech-to-text manager, an ASR/VAD client, a Llama.cpp translation client, an OmniVoice TTS client, and FFmpeg support. The dated link set included the project repository and an article about AI dubbing. The available links do not show whether files were added or changed on 2026-06-11.

## What changed

2026-06-11 — The source files describe a modular pipeline from video to ASR segments, translation, TTS, and FFmpeg assembly. The available snapshot does not prove a standalone release on 2026-06-11.

## How to use this

As of 2026-06-11, treat ASR/VAD, translation, TTS, and FFmpeg as distinct integration points. Verify their runtime behavior and versions before relying on them.

1. Install Python 3.12, an NVIDIA GPU, ffmpeg, and rubberband-cli. For a local GPU stack, use uv and extra gpu.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
2. For a fast start, build the Docker image, run it with --gpus all, and mount the weights and data directories.
  — <https://github.com/langswap-app/langswap>
3. Open Gradio at localhost:7860, upload a video, and set the target language. Output includes MP4 video and original and translated SRT files.
  — <https://github.com/langswap-app/langswap>
4. Run main.py local for debugging. Intermediate JSON files save to data/<id>, so reruns skip finished stages.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
5. Enable diarization only when needed. It requires access to pyannote/speaker-diarization-3.1 via HF_TOKEN.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>

## Best practices

- Keep VAD ASR as the default unless you need forced alignment. faster-whisper provides text, while Silero VAD marks speech segment boundaries.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py>
- On failure, rerun the failed stage through the local runner instead of reprocessing the whole video. The stack caches transcripts and segment remapping.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py>
- Review text, timecodes, and delivery manually before publishing news, film, or high-stakes video. An analysis describes human-in-the-loop editing as the working boundary of automation.
  — <https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza>
- Verify AGPL-3.0-or-later for the codebase and individual licenses for downloaded models before commercial or network deployment.
  — <https://github.com/langswap-app/langswap>

## Superseded by this

- 2026-06-24 — There is no confirmed replacement for SRT. PR #12 proposes WebVTT, but it remains open and does not change the documented output.

## Still unknown

- No dated Git snapshot exists for 2026-06-11, so we cannot confirm a release or the exact code state on that date.
- Documentation conflicts on HF_TOKEN: the README lists Gemma as an example of a gated model, while the advanced guide requires the token only for pyannote diarization.
- No independent live end-to-end testing confirms the quality, speed, or compatibility of the stack.
- Chinese search channels yielded no usable primary or practical source.
- 2026-06-11 — An analysis published 2026-02-01 clarifies the practical limits of this modular setup: automation speeds up draft dubbing, but accuracy, cultural nuance, and emotion need a human in the loop. This is an authorial analysis rather than an independent benchmark.
- 2026-06-24 — PR #12 proposes switching subtitle generation from SRT to WebVTT. The changes are not merged, so this is not a current release.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/langswap-app/langswap | langswap — GitHub repository | 2026-09-05 |
| https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md | langswap — advanced guide | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py | SpeechToTextManager source | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py | VAD ASR client source | 2026-09-05 |
| https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza | Машинальная озвучка: в чем заключаются проблемы ИИ-дубляжа | 2026-09-05 |
| https://github.com/langswap-app/langswap/pull/12 | Pull request #12: SRT-to-WebVTT proposal | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:langswap`, thread `speech-translation-and-dubbing-stack`, 1 dated events 2026-06-11 → 2026-06-11.
- **Practical note:** As of 2026-06-11, practitioners assessing Langswap should treat ASR/VAD, translation, TTS, and FFmpeg as distinct integration points in its speech-dubbing workflow, and verify their runtime behavior and versions before relying on them.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
