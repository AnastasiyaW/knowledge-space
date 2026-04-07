---
title: Speech Recognition
category: reference
tags: [asr, whisper, parakeet, streaming, transcription, multilingual, speech-to-text]
---

# Speech Recognition

Automatic Speech Recognition (ASR) converts spoken audio to text. The field has converged on encoder-decoder transformer architectures, with Whisper as the dominant open model family and specialized alternatives for streaming and specific languages.

## Key Facts

- Whisper (OpenAI) is the de facto standard open ASR model - encoder-decoder transformer trained on 680K hours of web audio
- Whisper large-v3 handles 100+ languages with word-level timestamps via cross-attention
- Faster-Whisper uses CTranslate2 for 4x speedup over original PyTorch implementation
- Parakeet (NVIDIA NeMo) achieves lower WER than Whisper on English benchmarks, CTC + RNN-T architecture
- Canary (NVIDIA) extends Parakeet to multilingual with translation capabilities
- Streaming ASR requires chunked processing - models like Whisper are not natively streaming

## Model Comparison

| Model | Architecture | Languages | Streaming | WER (LibriSpeech) | Strength |
|-------|-------------|-----------|-----------|-------------------|----------|
| Whisper large-v3 | Enc-Dec Transformer | 100+ | No | 2.7% | Universal, robust |
| Whisper large-v3-turbo | Distilled Enc-Dec | 100+ | No | 3.0% | 8x faster than v3 |
| Faster-Whisper | CTranslate2 Whisper | 100+ | Chunked | 2.7% | Production speed |
| Parakeet-TDT 1.1B | CTC + Transducer | EN | Yes | 1.5% | Best English WER |
| Canary-1B | Multi-task CTC | 4+ | No | 2.1% | Translation built-in |
| Whisper.cpp | GGML Whisper | 100+ | Chunked | ~3% | CPU/edge deployment |

## Whisper Usage

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

Whisper is not natively streaming - it processes fixed 30-second windows. For real-time applications:

```text
Approaches to streaming:
  1. Chunked processing - split audio into overlapping chunks, transcribe each
     Latency: chunk_duration + inference_time (typically 2-5 sec)
     
  2. VAD + Whisper - use Voice Activity Detection to find speech segments, 
     transcribe complete utterances
     Latency: utterance_end + inference_time
     
  3. Native streaming models - Parakeet-TDT, Conformer-Transducer
     Latency: ~200ms, but English-only for best quality
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

## Language-Specific Notes

- **Russian**: Whisper large-v3 handles well, but specialized models (Vosk, Silero) can be faster for RU-only deployments
- **Chinese**: Whisper works but FunASR (Alibaba) and Paraformer outperform for Mandarin
- **Code-switching** (mixing languages): Whisper handles reasonably, but quality drops at switch points
- **Accented speech**: Whisper is robust to accents due to diverse training data, but WER increases 2-5x for heavy accents

## Gotchas

- **Whisper hallucinates on silence** - if input contains long silent segments, Whisper generates phantom text (repeated phrases, random words). Always apply VAD filtering before transcription (`vad_filter=True` in faster-whisper)
- **30-second window boundary cuts words** - Whisper's fixed 30s context window can split words at boundaries, producing garbled segments. Use overlapping windows or VAD-based segmentation to avoid mid-word cuts
- **Language detection is per-file, not per-segment** - Whisper detects language once for the entire audio. For multilingual recordings, force segment-level language detection or use WhisperX with explicit language per segment
- **Timestamp accuracy varies by speech rate** - word timestamps from Whisper cross-attention are approximate (+-200ms). For precise alignment (subtitles, speech editing), use WhisperX forced alignment

## See Also

- [[podcast-processing]] - full pipeline using ASR + diarization + editing
- [[tts-models]] - TTS models that use ASR for quality evaluation
- [[voice-cloning]] - WhisperX alignment used in speech editing workflows
