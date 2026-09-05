---
title: Gemini 3.5 Live Translate — Gemini Live Translation
category: projects
date: 2026-06-13
tags: [gemini-3-5-live-translate, gemini-live-translation, gemini_models, project]
aliases: ["Gemini 3.5 Live Translate"]
---

# Gemini 3.5 Live Translate — Gemini Live Translation

**Development line:** `project:gemini-3-5-live-translate` · thread `gemini-live-translation`  
**Last event:** 2026-06-13 · 1 dated since 2026-06-13 · **Researched:** 2026-09-05 · confidence: high

## What it is

Gemini 3.5 Live Translate is Google’s low-latency audio-to-audio translation model for real-time spoken conversations.

- Automatic detection across 70+ languages
- Continuous translated speech
- Optional input and output transcripts

The model remains in preview, accepts audio only, and does not support tools or instructions. Use it as an interpreter pipeline, not as a general-purpose voice agent.

## Development line

- **2026-06-13 — Google presented Gemini 3.5 Live Translate preview.** On 2026-06-13, Google introduced Gemini 3.5 Live Translate as a preview model for real-time translation in Gemini Live. The release provided a Live API guide, an AI Studio Live preview URL, and integration references for LiveKit and Pipecat.

## What changed

- 2026-06-13 — Gemini 3.5 Live Translate became available to developers in public preview through the Gemini Live API and Google AI Studio.
- 2026-08-26 — Google published the Gemini 3.5 Audio model card. It documented Live Translate’s 128K input and 64K output context limits, along with failure modes for voice, language detection, and background noise.

## How to use this

From 2026-06-13, evaluate Gemini 3.5 Live Translate preview through the Gemini Live API or AI Studio. Confirm the LiveKit or Pipecat integration path before adopting it.

1. Create a Gemini API client and open a Live API session with model `gemini-3.5-live-translate-preview`.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
2. Set `response_modalities` to audio and provide `translationConfig.targetLanguageCode` as a BCP-47 target-language code.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
3. Stream 16-bit, 16 kHz, mono, little-endian PCM in roughly 100 ms chunks; consume the returned 24 kHz PCM audio.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
4. Enable input and output transcription when the product needs captions, logging, or a readable translation alongside audio.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>

## Best practices

- Treat it as a continuous translation stream rather than a turn-based agent. Translation mode has no tool, instruction, text-input, image, or video support.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- For browser or mobile clients, use v1beta ephemeral tokens and constrain `translationConfig` server-side unless users must choose the target language themselves.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- Test non-native accents, rapid language switching, long pauses, multi-speaker calls, and noisy rooms before relying on translated audio operationally.
  — <https://deepmind.google/models/model-cards/gemini-3-5-audio/>
- Budget for both streamed input and generated output audio: Google lists an effective paid rate of about $0.0368 per minute.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Superseded by this

- 2026-06-09 — Google planned to replace the prior Google Meet speech-translation limit of five languages and English-centered translation with 70+ languages and 2,000+ language combinations.

## Still unknown

- The current LiveKit and Pipecat pages describe generic Gemini Live integrations, not a documented Gemini 3.5 Live Translate-specific adapter or configuration. Validate that framework path before treating either as translation support.
- Google’s public material establishes public preview for developers, but does not provide a general-availability date for the API model.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/ | Gemini 3.5 Live Translate is here | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/live-api/live-translate | Live translation with Gemini Live API | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3.5-live-translate-preview | Gemini 3.5 Live Translate model reference | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | 2026-09-05 |
| https://deepmind.google/models/model-cards/gemini-3-5-audio/ | Gemini 3.5 Audio (Live Translate, Transcribe, Transcribe Live) model card | 2026-09-05 |
| https://docs.livekit.io/agents/models/realtime/plugins/gemini/ | Gemini Live API plugin | 2026-09-05 |
| https://docs.pipecat.ai/pipecat/features/gemini-live | Building with Gemini Live | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:gemini-3-5-live-translate`, thread `gemini-live-translation`, 1 dated events 2026-06-13 → 2026-06-13.
- **Practical note:** From 2026-06-13, evaluate Gemini 3.5 Live Translate preview through the Gemini Live API or AI Studio and confirm the LiveKit or Pipecat integration path before adopting it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
