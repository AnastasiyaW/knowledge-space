---
title: Audio & Voice
description: Speech recognition, text-to-speech, voice cloning, and voice agent pipelines — model comparisons, latency benchmarks, and production integration patterns.
type: MOC
---

# Audio & Voice

Modern speech systems span three core areas: recognizing spoken language (ASR), synthesizing voices (TTS), and converting or cloning speaker identity. Articles here cover current model families (Whisper, Qwen3-ASR, NVIDIA Canary, F5-TTS, CosyVoice), latency budgets for real-time voice agents, fine-tuning infrastructure on rented GPUs, and multilingual deployment trade-offs. Each piece is a dense reference: architecture diagrams, commands, benchmarks, and integration gotchas — not tutorials.

## Speech & Recognition
- [[speech-recognition]] - ASR models, transcription, pronunciation assessment

## Text-to-Speech
- [[tts-models]] - TTS model comparison, latency benchmarks, multilingual support
- [[voice-cloning]] - Voice cloning, voice mixing, naturalness benchmarks
- [[voice-conversion]] - Voice conversion techniques and pipelines
- [[audio-generation]] - Audio generation models and workflows
- [[audio-flamingo]] - Audio Flamingo 3, Music Flamingo, and AF-Next understanding artifacts
- [[ace-step-1-5]] - ACE-Step 1.5 base/SFT/turbo and XL hardware bounds

## Voice Applications
- [[voice-agent-pipelines]] - Voice agent pipelines and frameworks for real-time applications
- [[podcast-processing]] - Podcast processing, transcription, and analysis

## Additional References

- [[asr-stt-compression]] - KV cache compression methods for ASR/TTS inference and LLM context in 2026: TriAttention
- [[audio-omni-unified-model]] - Single model for audio understanding, generation, and editing via frozen LLM reasoning + trainable
- [[lemas-tts-and-speech-editing]] - LEMAS open-source multilingual TTS and word-level speech editing models - architecture
- [[tts-fine-tuning-infrastructure]] - GPU rental platform comparison and deployment patterns for fine-tuning and serving 2B-4B TTS models
- [[voice-design]] - Creating unique synthetic voices from text descriptions, voice morphing, naturalness benchmarks
