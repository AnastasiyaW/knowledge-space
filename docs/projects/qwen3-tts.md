---
title: Qwen3-TTS
category: projects
date: 2026-08-06
tags: [project, qwen3-tts, qwen3-tts-release-and-distribution, qwen3_tts]
aliases: ["Qwen3-TTS"]
---

# Qwen3-TTS

**Development line:** `project:qwen3-tts` · thread `qwen3-tts-release-and-distribution`  
**Last event:** 2026-08-06 · 2 dated since 2025-09-23 · **Researched:** 2026-09-04 · confidence: high

## What it is

Qwen3-TTS is an open-weight speech synthesis series for developers, built to replace cloud TTS APIs such as ElevenLabs. It provides CustomVoice for preset timbres, VoiceDesign for text descriptions, and Base for audio reference cloning.

- 10 languages across speech synthesis
- Base: 3-second cloning from reference audio
- Generation: streaming and batch modes
- CustomVoice: up to 9 preset timbres

Claimed minimum end-to-end latency is 97 ms; open-weight options are 0.6B and 1.7B. It is a practical choice for local multilingual TTS when we can run Python and PyTorch or run the Base model through a compatible GGUF runtime.

## Development line

- **2025-09-23 — Qwen linked an official Qwen3-TTS demo and Qwen TTS documentation.** Multi-timbre, multilingual, and dialect speech synthesis; the primary official publication is dated 2025-09-21.
- **2026-08-06 — ggml-org published a GGUF distribution of Qwen3-TTS-12Hz-1.7B-Base.** On 2026-08-06, the dated link recorded a GGUF distribution of Qwen3-TTS-12Hz-1.7B-Base on Hugging Face. This was a downstream distribution step rather than an upstream Qwen model release, but it materially expanded the local-runtime deployment path for the project.

## What changed

- **2025-09-23** — Qwen3-TTS-Flash anchored the API direction for multi-timbre, multilingual, and dialect speech synthesis; the initial official publication is dated 2025-09-21.
- **2025-12-04** — Flash expanded to 49 timbres, 10 languages, and 9 dialects; this was an API update rather than a local weight release.
- **2025-12-22** — Qwen added API models Qwen3-TTS-VD-Flash for voice design and Qwen3-TTS-VC-Flash for cloning from a three-second sample.
- **2026-01-22** — Qwen released the Apache-2.0 open-weight series with Tokenizer-12Hz, 0.6B Base/CustomVoice, and 1.7B Base/CustomVoice/VoiceDesign; this made local deployment and fine-tuning supported upstream workflows.
- **2026-08-06** — ggml-org published GGUF quantizations of Qwen3-TTS-12Hz-1.7B-Base for llama.cpp-compatible local runtimes; this is downstream packaging for the Base model rather than a new upstream Qwen variant.

## How to use this

From 2025-09-23, practitioners evaluating Qwen3-TTS should begin with the linked official demo and Qwen TTS documentation; from 2026-08-06, practitioners seeking local deployment can also evaluate the linked GGUF distribution.

1. Pick CustomVoice for a preset timbre, VoiceDesign for a prompt-based timbre, or Base for voice cloning; for local runs, select 0.6B for lower requirements or 1.7B for quality.
  — <https://github.com/QwenLM/Qwen3-TTS>
2. Create a clean Python 3.12 environment and install `qwen-tts`; load the model with `Qwen3TTSModel.from_pretrained`.
  — <https://github.com/QwenLM/Qwen3-TTS>
3. For CustomVoice, pass text, language, speaker, and optional instruct; for VoiceDesign, supply text and a natural-language voice description; for Base, provide reference audio and its transcript.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
4. For a lighter local path for 1.7B Base only, run the GGUF release through llama.cpp, such as `llama serve -hf ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q4_K_M`.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Best practices

- Use a clean Python environment so TTS dependencies do not conflict with existing projects; enable FlashAttention 2 only on compatible hardware with float16/bfloat16.
  — <https://github.com/QwenLM/Qwen3-TTS>
- Set the known language explicitly instead of Auto; use the native language of the selected timbre for best CustomVoice quality.
  — <https://github.com/QwenLM/Qwen3-TTS>
- Do not expose the Base web UI and microphone over plain HTTP: require HTTPS and a valid certificate for remote access in production.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
- Do not treat GGUF as an equivalent for the full family: the published package covers only Base and supplies separate Q4_K_M, Q8_0, and BF16 quantizations.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Superseded by this

- 2026-01-22: Treating Qwen3-TTS purely as the Qwen3-TTS-Flash API is obsolete for local use; Apache-2.0 weights for 0.6B/1.7B and source code are published.
- 2026-08-06: GGUF Base does not replace upstream CustomVoice or VoiceDesign; use the `qwen-tts` package and official checkpoints for those tasks.

## Still unknown

- Response structure lacks dedicated `event_findings` and `new_events` fields; we folded their facts into the dated `what_changed` line.
- The exact creation date of the GGUF repository was not visible on the model page; 2026-08-06 remains the recorded date of the linked event, with package details verified against the card.
- We have not verified DashScope API pricing, regional availability, or current rate limits; these can drift independently of the open-weight release.

## Sources

| source | title | read |
|---|---|---|
| https://qwen.ai/blog?from=home.latest-research-list | Qwen3-TTS-Flash: Multi-timbre, Multi-lingual and Multi-dialect Speech Synthesis | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-1128 | Qwen3-TTS Update! 49 Timbres + 10 Languages + 9 Dialects | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign | Qwen3-TTS Steps Up: Voice Cloning and Voice Design! | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3tts-0115 | Qwen3-TTS Family Is Now Open Sourced: Voice Design, Clone, and Generation | 2026-09-05 |
| https://github.com/QwenLM/Qwen3-TTS | QwenLM/Qwen3-TTS | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base | Qwen/Qwen3-TTS-12Hz-1.7B-Base | 2026-09-05 |
| https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-tts`, thread `qwen3-tts-release-and-distribution`, 2 dated events 2025-09-23 → 2026-08-06.
- **Practical note:** From 2025-09-23, practitioners evaluating Qwen3-TTS should begin with the linked official demo and Qwen TTS documentation; from 2026-08-06, practitioners seeking local deployment can also evaluate the linked GGUF distribution.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.