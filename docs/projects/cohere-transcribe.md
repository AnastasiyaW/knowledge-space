---
title: Cohere Transcribe
category: projects
date: 2026-03-27
tags: [cohere-transcribe, project]
aliases: ["Cohere Transcribe"]
---

# Cohere Transcribe

**Development line:** `project:cohere-transcribe` · thread `cohere-transcribe`  
**Last event:** 2026-03-27 · 1 dated since 2026-03-27 · **Researched:** 2026-09-05 · confidence: high

## What it is

Cohere Transcribe is an Apache-2.0 Conformer encoder-decoder ASR model for audio-to-text workflows.

- Transcribes 14 languages with the base `cohere-transcribe-03-2026` model.
- Runs locally through Transformers or vLLM, or through Cohere’s transcription API.
- Adds `cohere-transcribe-arabic-07-2026` for Arabic dialects and Arabic-English audio.

## Development line

- **2026-03-27 — Cohere publishes Cohere Transcribe model resources.** On 2026-03-27, Cohere published Cohere Transcribe resources: a blog page, a Hugging Face model repository, and a demonstration space. The linked Model Vault page places the project within Cohere's model-access offering.

## What changed

- 2026-03-27 — `cohere-transcribe-03-2026` entered the product line as a 2B, 14-language open ASR model; Cohere dated the release to 2026-03-26.
- 2026-07-07 — Cohere released the separate 2B `cohere-transcribe-arabic-07-2026` fine-tune for Arabic dialects, Arabic-English speech, and code-switching workloads.

## How to use this

From 2026-03-27, evaluate Cohere Transcribe through Cohere's published model repository and demonstration space, and check the linked Cohere materials for access and deployment terms.

1. Choose `cohere-transcribe-03-2026` for the 14-language base model; choose `cohere-transcribe-arabic-07-2026` when the workload is predominantly Arabic or Arabic-English.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
2. For the hosted route, obtain a Cohere API key and send a multipart request to `POST /v2/audio/transcriptions` with `model`, an ISO-639-1 `language`, and the audio file.
  — <https://docs.cohere.com/reference/create-audio-transcription>
3. Keep hosted input files at 25 MB or below and use FLAC, MP3, MPEG, MPGA, OGG, or WAV.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
4. For local inference, load the base checkpoint with Transformers, pass the audio at 16 kHz and set the language explicitly; use the model card’s long-form chunking path for longer recordings.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
5. For self-hosted production serving, follow Cohere’s vLLM deployment path and call its OpenAI-compatible audio-transcriptions endpoint.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>

## Best practices

- Specify one expected language per request, as the base model lacks automatic language detection and produces inconsistent text on code-switched audio.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Put VAD or a noise gate before the model so silence and low-level room noise do not generate text.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Add a separate diarization and timestamping stage if the application requires speakers or word timing; the base model supplies neither.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Use the Arabic fine-tune rather than the base model for Arabic dialects and Arabic-English speech; Cohere reports gains over the base model on both.
  — <https://cohere.com/blog/transcribe-arabic>

## Superseded by this

- 2026-03-26 — The 2026-07-07 Arabic fine-tune supersedes the 14-language base model for Arabic dialect and Arabic-English transcription; the base model itself remains supported for its broader language set.

## Still unknown

- No first-party Simplified Chinese announcement or Chinese-language usage documentation exists; Mandarin transcription support does not establish localized operating guidance.
- The reported leaderboard and throughput results are vendor-published measurements; we did not independently reproduce them.

## Sources

| source | title | read |
|---|---|---|
| https://cohere.com/blog/transcribe | Introducing Cohere Transcribe: a new state-of-the-art in open-source speech recognition | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-03-2026 | CohereLabs/cohere-transcribe-03-2026 | 2026-09-05 |
| https://huggingface.co/blog/CohereLabs/cohere-transcribe-03-2026-release | Introducing Cohere-transcribe: state-of-the-art speech recognition | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Release Notes | 2026-09-05 |
| https://docs.cohere.com/docs/transcribe | Cohere Transcribe | 2026-09-05 |
| https://docs.cohere.com/reference/create-audio-transcription | Create a transcription | 2026-09-05 |
| https://docs.cohere.com/docs/audio-transcription-quickstart | Audio Transcription - quickstart | 2026-09-05 |
| https://cohere.com/blog/transcribe-arabic | Meet Cohere Transcribe Arabic | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-arabic-07-2026 | CohereLabs/cohere-transcribe-arabic-07-2026 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:cohere-transcribe`, thread `cohere-transcribe`, 1 dated events 2026-03-27 → 2026-03-27.
- **Practical note:** From 2026-03-27, practitioners should evaluate Cohere Transcribe through Cohere's published model repository and demonstration space, while checking the linked Cohere materials for access and deployment terms.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
