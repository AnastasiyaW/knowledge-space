---
title: Speech Recognition
category: reference
tags: [asr, whisper, parakeet, qwen3-asr, streaming, transcription, multilingual, speech-to-text, edge-asr]
---

# Speech Recognition

Automatic Speech Recognition (ASR) converts spoken audio to text. As of early 2026, the field has moved past Whisper dominance - Qwen3-ASR, NVIDIA Canary-Qwen, and Voxtral Realtime all significantly outperform Whisper on accuracy and/or speed. Whisper large-v3 remains a reliable baseline but has not been updated.

## Key Facts

- **Qwen3-ASR** (Jan 2026) is the new open-source SOTA for multilingual ASR - 52 languages, Apache 2.0, trained on ~40M hours
- **MAI-Transcribe-1** (Apr 2026) is the new commercial SOTA - 3.8% WER on FLEURS top-25 languages, proprietary
- Whisper large-v3 remains viable but has not received a v4 update - the ecosystem has moved past it
- Streaming ASR is now production-ready with Voxtral Realtime (13 langs) and Nemotron Speech (EN, <24ms)
- Edge ASR viable at <1GB RAM with Moonshine v2 (27M params, 50ms) and Parakeet.cpp (pure C++)
- SALM (Speech-Augmented Language Model) architecture combines ASR encoder + LLM decoder for transcription + reasoning in one model

## Model Comparison

| Model | Architecture | Params | Languages | Streaming | Key WER | Strength |
|-------|-------------|--------|-----------|-----------|---------|----------|
| Qwen3-ASR 1.7B | AuT + Qwen3 LLM | 1.7B | 52 | Yes (dynamic) | TEDLIUM 4.50 | Best open multilingual |
| MAI-Transcribe-1 | Enc-Dec Transformer | ? | 25 | No | FLEURS 3.8% | Best commercial accuracy |
| Canary-Qwen 2.5B | FastConformer + Qwen3 | 2.5B | EN (+LLM) | No | LS-Clean 1.6% | ASR + summarization/QA |
| Voxtral Realtime 4B | LM + encoder | 4B | 13 | Yes (80ms-2.4s) | Near offline quality | Configurable latency |
| Whisper large-v3 | Enc-Dec Transformer | 1.55B | 100+ | No | LS 2.7% | Most languages, stable |
| Parakeet-TDT-V3 | FastConformer-TDT | 0.6B | 25 EU | Yes | RTFx ~2000 | Fastest open EN ASR |
| Canary-1B-V2 | Multi-task CTC | 1B | 25 EU (incl. RU) | No | 10x faster than 3x larger | Translation built-in |
| Nemotron Speech | Cache-Aware Conformer | 0.6B | EN | Yes (<24ms) | 7.2-7.8% | 560 streams/H100 |
| Moonshine v2 Tiny | Ergodic Streaming Enc | 27M | EN | Yes (50ms) | On-par 6x size | Edge, <500MB RAM |
| Fun-ASR-Nano | End-to-end | ? | 31 (Asia focus) | Yes | 93% in noise | Chinese dialects/accents |
| Whisper.cpp | GGML Whisper | 1.55B | 100+ | Chunked | ~3% | CPU/edge deployment |

## Qwen3-ASR (Recommended Open-Source, 2026)

Best open-source multilingual ASR as of early 2026. Apache 2.0. Trained on ~40M hours of pseudo-labeled data.

```text
Architecture:
  AuT (Audio Transformer) encoder -> learned projector -> Qwen3 LLM decoder
  
  0.6B variant: AuT 180M params (hidden 896) + Qwen3 decoder
  1.7B variant: AuT 300M params (hidden 1024) + Qwen3 decoder

Key benchmarks (1.7B):
  TEDLIUM (EN): 4.50 WER  (vs GPT-4o 7.69, Whisper-lv3 6.84)
  WenetSpeech (ZH): 4.97  (vs GPT-4o 15.30, Whisper-lv3 9.86)
  Language ID (30 langs): 97.9% (vs Whisper-lv3 94.1%)

Streaming: dynamic flash attention, window 1s-8s
Latency (0.6B): 92ms TTFT, 2000x throughput at concurrency 128
Long audio: up to 20 minutes per pass
VRAM: ~2GB (0.6B), ~6GB (1.7B)
```

Also released: Qwen3-ForcedAligner-0.6B for text-speech alignment in 11 languages.

## Whisper Usage (Legacy Baseline)

### Basic Transcription

```python
import whisper

model = whisper.load_model("large-v3")
result = model.transcribe("audio.mp3", language="en")

print(result["text"])
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
```

### Faster-Whisper (Production)

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", beam_size=5, vad_filter=True)

print(f"Detected language: {info.language} ({info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### Word-Level Timestamps

```python
# Faster-Whisper word timestamps
segments, _ = model.transcribe("audio.mp3", word_timestamps=True)
for segment in segments:
    for word in segment.words:
        print(f"  {word.start:.2f}s - {word.end:.2f}s: '{word.word}' (p={word.probability:.2f})")
```

## Streaming ASR

As of 2026, native streaming ASR is production-ready in multiple languages.

```text
Native streaming models (recommended):
  1. Voxtral Realtime 4B - 13 languages (incl. EN/ZH/RU), configurable latency
     At 480ms: competitive with Whisper + ElevenLabs Scribe v2
     At 960ms: surpasses both
     At 2400ms: within 1% of offline quality
     Open-source, Apache 2.0, ~8-10GB VRAM

  2. Nemotron Speech Streaming 600M - English only, <24ms final transcripts
     Cache-Aware FastConformer-RNNT, chunk sizes 80-1120ms
     560 concurrent streams on single H100 at 320ms chunk
     3x throughput vs traditional buffered streaming

  3. Qwen3-ASR 0.6B - 52 languages, streaming via dynamic flash attention
     Window sizes 1s-8s, 92ms TTFT
     Best multilingual streaming option

  4. Moonshine v2 - 27M-medium params, edge streaming
     50ms (Tiny) to 258ms (Medium) latency
     <1GB memory, designed for edge processors

Legacy approaches (still valid for Whisper):
  5. Chunked Whisper - split into overlapping 30s chunks
     Latency: chunk_duration + inference (2-5 sec)
  
  6. VAD + Whisper - transcribe complete utterances
     Latency: utterance_end + inference
```

### VAD-Assisted Pipeline

```python
# Silero VAD + Faster-Whisper pipeline
import torch
from faster_whisper import WhisperModel

vad_model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils

wav = read_audio('audio.wav', sampling_rate=16000)
speech_timestamps = get_speech_timestamps(wav, vad_model, sampling_rate=16000)
# Each timestamp = a speech segment to transcribe independently
```

## WhisperX - Enhanced Alignment

WhisperX adds forced phoneme alignment for precise word boundaries, essential for speech editing and subtitle generation.

```text
WhisperX pipeline:
  1. Whisper transcription (batch mode for speed)
  2. VAD-based segmentation (cut on silence)
  3. Forced alignment via wav2vec2 / MMS alignment model
  4. Speaker diarization (optional, via pyannote)
  
Output: word-level timestamps with <50ms accuracy
```

## Multilingual ASR Selection Guide

Best model per language combination (open-source, 2026):

| Target | Best Model | Fallback | Notes |
|--------|-----------|----------|-------|
| ZH + EN + RU | Qwen3-ASR 1.7B | Voxtral Realtime | Qwen3 destroys Whisper on Chinese |
| EN only | Canary-Qwen 2.5B | Parakeet-TDT V3 | 1.6% WER + LLM reasoning mode |
| EN streaming | Nemotron Speech | Voxtral Realtime | <24ms, 560 streams/H100 |
| Multi streaming | Voxtral Realtime | Qwen3-ASR 0.6B | 13 langs, configurable latency |
| Chinese dialects | Fun-ASR-Nano | Qwen3-ASR | 7 dialects, 26 accents |
| Edge / mobile | Moonshine v2 Tiny | Sherpa-ONNX | 27M params, <500MB RAM |
| Commercial SOTA | MAI-Transcribe-1 | Qwen3.5-Omni ASR | 3.8% WER FLEURS, API only |

## Language-Specific Notes

- **Russian**: Qwen3-ASR and Voxtral Realtime both support RU. Canary-1B-V2 includes RU in its 25 European languages. Whisper still viable for RU-only
- **Chinese**: Qwen3-ASR is the clear winner - WER 4.97 on WenetSpeech vs Whisper's 9.86. Fun-ASR-Nano excels at Chinese dialects (Wu, Cantonese, Hokkien, etc.)
- **Code-switching** (mixing languages): Qwen3-ASR and Fun-ASR-Nano handle free language switching better than Whisper
- **Accented speech**: Fun-ASR-Nano covers 26 Chinese regional accent varieties. For other languages, Whisper's diverse training data still provides reasonable accent robustness

## On-Device / Edge ASR

```text
Deployment options (2026):
  Moonshine v2 Tiny:  27M params, <500MB RAM, 50ms latency
  Parakeet.cpp:       Pure C++, no Python/ONNX, Metal GPU 27ms/10s audio
  Sherpa-ONNX:        Android/iOS/HarmonyOS/RPi/RISC-V, 12 languages
  Qwen3-ASR 0.6B:     MLX port for Apple Silicon (mlx-qwen3-asr)
  whisper.cpp:         CPU/Metal, still viable for Whisper models

Edge deployment guidelines:
  - INT4/INT8 quantization essential for mobile
  - Streaming architectures reduce memory 40%+ vs standard transformers
  - Tiny/Base variants: <500MB RAM target
```

## Pronunciation Assessment

Open-source pronunciation scoring remains a gap. Proprietary APIs (Azure Speech, SpeechSuper) dominate.

Best open-source path: Qwen3-ASR + forced alignment (Qwen3-ForcedAligner-0.6B) + goodness-of-pronunciation scoring.

Available resources:
- **SpeechOcean762** - public dataset (5000 EN sentences with quality scores)
- **Kaldi GOP** - Goodness of Pronunciation metric, mature
- **Qwen3-ForcedAligner-0.6B** - text-speech alignment in 11 languages, building block for pronunciation scoring

## Gotchas

- **Whisper hallucinates on silence** - if input contains long silent segments, Whisper generates phantom text (repeated phrases, random words). Always apply VAD filtering before transcription (`vad_filter=True` in faster-whisper). Newer models (Qwen3-ASR, Voxtral) are more robust to this
- **30-second window boundary cuts words** - Whisper's fixed 30s context window can split words at boundaries. Native streaming models (Voxtral Realtime, Nemotron) avoid this entirely with sliding-window architectures
- **Language detection is per-file, not per-segment** - Whisper detects language once for the entire audio. Qwen3-ASR has per-segment language ID with 97.9% accuracy across 30 languages
- **Timestamp accuracy varies by speech rate** - word timestamps from Whisper cross-attention are approximate (+-200ms). For precise alignment, use WhisperX forced alignment or Qwen3-ForcedAligner
- **Whisper is no longer the best choice for most tasks** - as of early 2026, Qwen3-ASR outperforms Whisper on accuracy for supported languages, Voxtral Realtime beats it on streaming, and Moonshine v2 beats it on edge. Whisper's advantage is only language count (100+ vs 52)
- **VRAM vs accuracy tradeoff shifted** - Qwen3-ASR 0.6B at ~2GB VRAM outperforms Whisper large-v3 at ~10GB on Chinese. Check benchmarks before defaulting to larger models

## See Also

- [[podcast-processing]] - full pipeline using ASR + diarization + editing
- [[tts-models]] - TTS models that use ASR for quality evaluation
- [[voice-cloning]] - WhisperX alignment used in speech editing workflows
