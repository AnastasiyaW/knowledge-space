---
title: Text-to-Speech Models
category: reference
tags: [tts, speech-synthesis, voice, flow-matching, autoregressive, zero-shot, multilingual]
---

# Text-to-Speech Models

Modern TTS has moved from concatenative and parametric approaches to neural end-to-end models. Two dominant architectures: autoregressive (token-by-token, flexible but slow) and non-autoregressive / flow-matching (fixed steps, faster inference, deterministic length).

## Key Facts

- Zero-shot TTS = clone any voice from a short reference clip (5-30 sec) without fine-tuning
- Flow matching (FM) models use fixed NFE steps (typically 16-32), making inference time predictable
- Autoregressive (AR) codec models generate audio tokens sequentially, better prosody but variable latency
- Diffusion-based TTS adds gaussian noise to mel-spectrograms and learns to reverse the process
- Most modern TTS outputs mel-spectrograms or audio codec tokens, then a vocoder (Vocos, HiFi-GAN) reconstructs waveform
- Sampling rate matters: 16kHz (telephony), 24kHz (standard), 44.1/48kHz (studio quality)

## Architecture Families

### Flow Matching (F5-TTS lineage)

Non-autoregressive, fixed-step generation. Reference audio + text -> masked mel-spectrogram -> flow matching fills the mask.

```text
Pipeline:
  reference_audio -> mel_spectrogram -> [MASK target region]
  text -> phoneme_encoder -> duration_predictor -> alignment
  flow_matching(masked_mel, text_embedding, NFE=32) -> full_mel
  vocoder(full_mel) -> waveform
```

**Key models:**
- **F5-TTS** - foundational flow-matching TTS, high quality, multilingual
- **LEMAS-TTS** (0.3B) - F5-TTS based, 10 languages including Russian, 150K+ hours training data
- **CosyVoice 2** (Alibaba) - streaming-capable flow matching, Mandarin-focused

### Autoregressive Codec

Generate discrete audio tokens left-to-right, then decode with codec decoder.

```text
Pipeline:
  text -> LLM backbone -> audio_codec_tokens (e.g. EnCodec, DAC)
  codec_decoder(tokens) -> waveform
```

**Key models:**
- **VoxCPM2** (2B) - diffusion-AR hybrid on MiniCPM-4 backbone, 30+ languages, 48kHz
- **Orpheus TTS** (Canopy AI) - LLM-native, emotional control via tags
- **Fish Speech** - fast AR codec, good CJK support

### Hybrid / Other

- **XTTS v2** (Coqui) - GPT-based + HiFi-GAN vocoder, proven multilingual (RU + EN), voice cloning from 6 sec
- **Kokoro-82M** - tiny model (82M params), 100x realtime on CPU, English-focused
- **StyleTTS 2** - style diffusion + duration predictor, fast inference
- **Chatterbox** (Resemble AI) - emotion control, cloning from short samples
- **Dia** (Nari Labs) - dialogue-focused, multi-speaker generation

## Model Comparison

| Model | Params | Languages | Sample Rate | Architecture | Strength |
|-------|--------|-----------|-------------|-------------|----------|
| LEMAS-TTS | 0.3B | 10 | 24kHz | Flow matching | Multilingual + word-level edit |
| VoxCPM2 | 2B | 30+ | 48kHz | Diffusion-AR | Studio quality |
| XTTS v2 | ~0.5B | 17 | 24kHz | GPT + vocoder | Proven, stable |
| Kokoro-82M | 82M | EN mainly | 24kHz | StyleTTS-like | Speed, CPU-friendly |
| F5-TTS | 0.3B | Multi | 24kHz | Flow matching | Base for many forks |
| CosyVoice 2 | ~0.5B | Multi | 22.05kHz | Flow matching | Streaming support |
| Fish Speech | ~0.5B | Multi | 44.1kHz | AR codec | Fast, good CJK |

## Inference Parameters

```text
Common TTS parameters:
  NFE steps (flow matching): 16-32, higher = better quality, slower
  CFG strength: 1.0-3.0, controls adherence to text vs naturalness
  Temperature: 0.5-1.0, controls variation in AR models
  Speed: 0.8-1.2x, pitch-preserving time stretch
  Top-k / Top-p: AR sampling parameters, same as LLM text generation
```

## Speech Editing

LEMAS-Edit and VoiceCraft enable word-level editing - replace specific words in a recording without regenerating the entire utterance. Two backends:

- **Flow-matching backend**: faster, 10 languages
- **AR codec backend**: 7 languages, requires WhisperX + MMS alignment for word boundaries

## Evaluation Metrics

- **MOS** (Mean Opinion Score) - human rating 1-5, gold standard but expensive
- **MUSHRA** - multi-stimulus comparison test, better for comparing models
- **WER** (Word Error Rate) - transcribe generated speech, compare to input text
- **Speaker similarity** - cosine similarity of speaker embeddings between reference and generated
- **PESQ / POLQA** - perceptual quality, correlates with MOS

## Gotchas

- **Reference audio quality is everything** - noisy, reverberant, or music-contaminated references produce poor clones regardless of model quality. Apply UVR5 or DeepFilterNet denoising before use
- **Multilingual zero-shot has uneven quality** - most models excel at English/Chinese but degrade on lower-resource languages. Always test target language specifically
- **Flow matching NFE tradeoff is non-linear** - going from 16 to 32 steps improves quality noticeably, but 32 to 64 shows diminishing returns while doubling latency
- **Codec-based models hallucinate under long inputs** - AR models can loop, stutter, or skip words on texts >500 characters. Split long texts into sentence-level chunks

## See Also

- [[voice-cloning]] - dedicated coverage of cloning techniques and cross-lingual transfer
- [[audio-generation]] - music and sound effect generation
- [[speech-recognition]] - ASR models used for TTS evaluation (WER measurement)
