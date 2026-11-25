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

Langswap is a local video dubbing tool for teams that need direct control over media files and models.

Default stack components:
- ASR: transcribes audio with faster-whisper large-v3 and marks speech segments with Silero VAD.
- Translation: translates text using Gemma-4-E2B GGUF.
- Voice cloning TTS: synthesizes speech through OmniVoice.
- Output timing: aligns speech timing and exports SRT subtitle files.

Requirements and limits:
Requires Python 3.12 and an NVIDIA GPU with a CUDA-13 stack. High-stakes content requires manual review.

## Development line

- **2026-06-11 — Langswap surfaced a modular speech translation and dubbing stack.** On 2026-06-11, Langswap linked source paths for a speech-to-text manager, an ASR/VAD client, a Llama.cpp translation client, an OmniVoice TTS client, and FFmpeg. The links also included the main repository and an article on AI dubbing. We cannot confirm from these links whether the referenced files were created or modified on that date.

## What changed

- 2026-06-11 — the sources describe a modular pipeline from video to ASR segments, translation, TTS, and FFmpeg assembly. The available snapshot does not confirm a distinct release on that date.

## How to use this

As of 2026-06-11, treat ASR/VAD, translation, TTS, and FFmpeg as distinct integration points. Verify their runtime behavior and versions before production use.

1. Install Python 3.12, NVIDIA GPU drivers, ffmpeg, and rubberband-cli. Use uv with the gpu extra for the local GPU stack.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
2. Build the Docker image, run it with `--gpus all`, and mount the weights and data directories for a quick start.
  — <https://github.com/langswap-app/langswap>
3. Open Gradio at localhost:7860, upload a video, and choose the target language to produce an MP4 and source and translated SRT files.
  — <https://github.com/langswap-app/langswap>
4. Run `main.py local` for debugging: intermediate JSON saves to `data/<id>`, so restarts skip finished stages.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
5. Enable diarization only when needed, as it requires HF_TOKEN access to pyannote/speaker-diarization-3.1.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>

## Best practices

- Keep VAD ASR as the default unless you need separate forced alignment: faster-whisper provides the text, and Silero VAD marks speech boundaries.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py>
- Rerun failed stages through the local runner instead of reprocessing the whole video: transcript and segment remapping are cached.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py>
- Check text, timecodes, and intonation with a human reviewer before publishing news or film: a human-in-the-loop workflow marks the practical boundary of automation.
  — <https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza>
- Check AGPL-3.0-or-later for the codebase and license terms for downloaded models before commercial or network deployment.
  — <https://github.com/langswap-app/langswap>

## Superseded by this

- 2026-06-24 — no confirmed replacement for SRT exists: PR #12 suggests WebVTT, but remains open and does not change the documented output.

## Still unknown

- We have no dated Git snapshot for 2026-06-11, so we cannot verify a release or exact code state on that date.
- Documentation conflicts on HF_TOKEN: the README lists Gemma as a gated model, while the advanced guide requires the token only for pyannote diarization.
- No independent end-to-end benchmark confirms quality, speed, or hardware compatibility for the current stack.
- Chinese search queries yielded no usable primary or practical sources.
- 2026-06-11: an article published 2026-02-01 notes the limits of modular dubbing: automation speeds up draft work, but precision, culture, and emotion require a human in the loop. This is an opinion piece, not a benchmark.
- 2026-06-24: PR #12 suggests moving subtitle generation from SRT to WebVTT, but the changes are not merged and do not represent a release.

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
