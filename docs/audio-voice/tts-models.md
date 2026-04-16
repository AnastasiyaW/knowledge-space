---
title: Text-to-Speech Models
category: reference
tags: [tts, speech-synthesis, voice, flow-matching, autoregressive, zero-shot, multilingual, diffusion-language-model]
---

# Text-to-Speech Models

Modern TTS has moved from concatenative and parametric approaches to neural end-to-end models. Three dominant architectures: autoregressive (token-by-token, flexible but slow), non-autoregressive / flow-matching (fixed steps, faster inference), and diffusion language models (text to multi-codebook acoustic tokens).

## Key Facts

- Zero-shot TTS = clone any voice from a short reference clip (3-30 sec) without fine-tuning
- Flow matching (FM) models use fixed NFE steps (typically 16-32), making inference time predictable
- Autoregressive (AR) codec models generate audio tokens sequentially, better prosody but variable latency
- Diffusion-based TTS adds gaussian noise to mel-spectrograms and learns to reverse the process
- Diffusion Language Models (OmniVoice) map text directly to multi-codebook acoustic tokens - a third paradigm combining flow-based and AR strengths
- Tokenizer-free architectures (VoxCPM2) skip discrete codec tokens entirely, preserving prosodic nuance that tokenization destroys
- Most modern TTS outputs mel-spectrograms or audio codec tokens, then a vocoder (Vocos, HiFi-GAN) reconstructs waveform
- Sampling rate matters: 16kHz (telephony), 24kHz (standard), 44.1/48kHz (studio quality)
- End-to-end omni-models (Qwen3.5-Omni) combine ASR + TTS + LLM reasoning in a single architecture with real-time conversation support

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
- **VoxCPM2** (2B) - tokenizer-free, 4-stage pipeline (LocEnc -> TSLM -> RALM -> LocDiT), diffusion-AR hybrid on MiniCPM-4 backbone, 30+ languages, 48kHz native with built-in super-resolution, Apache 2.0
- **Orpheus TTS** (Canopy AI) - LLM-native, emotional control via tags
- **Fish Speech** - fast AR codec, good CJK support

### Diffusion Language Model

Maps text directly to multi-codebook acoustic tokens via diffusion process - avoids single-codebook bottleneck of AR models.

```text
Pipeline:
  text -> diffusion_language_model -> multi_codebook_acoustic_tokens
  codec_decoder(multi_codebook_tokens) -> waveform
  
  Key advantage: multi-codebook = richer acoustic representation
  than single-stream AR, while still being faster than flow matching
```

**Key models:**
- **OmniVoice** (k2-fsa) - 600+ languages, RTF 0.025 (40x realtime), zero-shot cross-lingual cloning, noise-robust reference intake, Apache 2.0
- **Voxtral 4B** (Mistral) - 4B params, 9 languages (EN/FR/DE/ES/NL/PT/IT/HI/AR, no RU/ZH), 70ms latency, cloning from 3 sec, captures accent and disfluencies, open weights

### End-to-End Omni-Models

Combined ASR + TTS + LLM reasoning in a single model. Input: audio or text. Output: text + speech simultaneously.

```text
Architecture (Qwen3.5-Omni):
  Input audio/text -> Thinker module (reasoning, MoE)
  Thinker -> Talker module (speech synthesis)
  ARIA alignment: dynamic text-speech synchronization mid-generation
  
  Capabilities: real-time conversation, turn-taking detection,
  mid-conversation control (volume, tempo, emotion)
```

**Key models:**
- **Qwen3.5-Omni** (Alibaba) - Thinker-Talker dual-module, 113 languages ASR / 36 languages TTS / 55 voices, real-time turn-taking, WER 6.24 on seed-hard (vs GPT-Audio 8.19), API only (not open-source), 3 variants: Plus/Flash/Light

### Hybrid / Other

- **XTTS v2** (Coqui) - GPT-based + HiFi-GAN vocoder, proven multilingual (RU + EN), voice cloning from 6 sec
- **Kokoro-82M** - tiny model (82M params), 100x realtime on CPU, English-focused
- **StyleTTS 2** - style diffusion + duration predictor, fast inference
- **Chatterbox** (Resemble AI) - emotion control, cloning from short samples
- **Dia** (Nari Labs) - dialogue-focused, multi-speaker generation

## Model Comparison (2026)

| Model | Params | Languages | Sample Rate | Architecture | Strength |
|-------|--------|-----------|-------------|-------------|----------|
| Fish Audio S2 Pro / OpenAudio S1 | 4B + 400M | 80+ | — | Dual-AR (Slow+Fast) | #1 TTS Arena, 81.88% vs gpt-4o-mini, 15K+ emotion tags |
| VoxCPM2 | 2B | 30+ | 48kHz | Tokenizer-free Diff-AR | Studio quality, voice design, Russian |
| OmniVoice | ? | 600+ | ? | Diffusion LM | Widest language coverage, RTF 0.025 |
| Qwen3.5-Omni | Large | 36 TTS / 113 ASR | ? | Omni (Thinker-Talker) | End-to-end conversation |
| Voxtral 4B | 4B | 9 (no RU/ZH) | ? | Streaming Diff-AR | 68.4% win vs ElevenLabs, 3s cloning |
| Qwen3-TTS | 1.7B / 0.6B | 10 (incl. RU) | ? | Custom codec 12Hz | Voice design, 97ms streaming |
| Dia 1.6B / Dia2 (Nari Labs) | 1B/2B | EN | Apache 2.0 | Dialogue TTS | Multi-speaker dialogue, streaming, up to 2 min |
| Higgs Audio V2 (BosonAI) | 3B | Multi | — | Llama 3.2 based | 75.7% win vs GPT-4o-mini-tts on emotions, multi-speaker |
| IndexTTS-2.5 | ? | CN/EN/JP/ES | — | Custom | 8-dim emotion vector, precise duration (dubbing) |
| NeuTTS Air (Neuphonic) | 748M | Multi | Open | GGUF | Runs on Raspberry Pi, 3s voice cloning |
| LEMAS-TTS | 0.3B | 10 | 24kHz | Flow matching | Multilingual + word-level edit |
| Chatterbox-Turbo | 350M-500M | 23+ (incl. RU) | ? | One-step decoder | MIT, paralinguistic tags |
| Kokoro-82M | 82M | 6 (no RU) | 24kHz | StyleTTS-like | Fastest: 210x RT, CPU |
| XTTS v2 | ~0.5B | 17 (incl. RU) | 24kHz | GPT + vocoder | Proven, stable, RU |
| CosyVoice 3 | ~0.5B | 9 (incl. RU) | 22.05kHz | RL-optimized FM | CER 0.81%, 150ms latency |
| F5-TTS Russian | 0.3B | RU | 24kHz | Flow matching (fine-tuned) | Best open-source RU TTS |
| Spark-TTS | 0.5B | ZH/EN | ? | BiCodec + Qwen2.5 | Chain-of-thought attribute control |
| OuteTTS 1.0 | 0.6B/1B | Multi | ? | AR + DAC encoder | GGUF/EXL2, consumer hardware |

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

## Voice Design (Text-Described Voice Creation)

Some models can create a voice from a text description, no reference audio needed:

```text
VoxCPM2 voice design:
  Input: "A warm female voice, age 30, slight accent, cheerful"
  -> Voice design module generates synthetic speaker embedding
  -> TTS generates speech with described characteristics

OmniVoice attribute control:
  Attributes: gender, age, pitch, dialect, whisper, speaking rate
  -> Fine-grained parametric control over synthetic voice
  -> Can combine: "young female, whispering, fast pace"
```

## Latency Benchmarks (2026)

| Model | First-packet (TTFA) | RTF | Notes |
|-------|---------------------|-----|-------|
| Kokoro 82M | 40-70ms | 0.005 (210x RT) | Fastest, CPU-friendly |
| Qwen3-TTS Flash | 97ms | — | Streaming |
| CosyVoice 3 | 150ms | — | Bi-streaming, lossless |
| Voxtral 4B | 70ms | — | 500-char / 10s input |
| Fish Audio S2 Pro | <100ms | 0.195 | SGLang inference engine |
| VoxCPM2 | — | 0.13 (Nano-VLLM) | RTF 0.30 standard PyTorch |
| Chatterbox-Turbo | ~472ms | 0.499 | One-step decoder tradeoff |

## Russian TTS (Open-Source, Ranked)

| Model | Quality | Notes |
|-------|---------|-------|
| F5-TTS Russian (ESpeech) | Best open-source | Multiple fine-tunes, 10K+ hours |
| ESpeech-TTS-1 RL-V2 | Excellent | Apache 2.0 |
| Qwen3-TTS 1.7B | Strong | 1 of 10 languages |
| CosyVoice 3 | Supported | RL-optimized |
| Chatterbox-ML 500M | Supported | 1 of 23 languages |
| VoxCPM2 2B | Supported | 30+ language model |
| XTTS v2 | Good | 17 languages, proven |
| Silero TTS | Excellent | Purpose-built for Russian |

Resources: [Russian TTS Leaderboard](https://huggingface.co/spaces/ESpeech/open_tts_leaderboard_ru) | [awesome-russian-speech](https://github.com/alphacep/awesome-russian-speech)

## Gotchas

- **Reference audio quality is everything** - noisy, reverberant, or music-contaminated references produce poor clones regardless of model quality. Apply UVR5 or DeepFilterNet denoising before use. Exception: OmniVoice is explicitly noise-robust and accepts noisy samples
- **Multilingual zero-shot has uneven quality** - most models excel at English/Chinese but degrade on lower-resource languages. OmniVoice (600+ langs) and VoxCPM2 (30+ langs) have the widest coverage, but always test target language specifically
- **Flow matching NFE tradeoff is non-linear** - going from 16 to 32 steps improves quality noticeably, but 32 to 64 shows diminishing returns while doubling latency
- **Codec-based models hallucinate under long inputs** - AR models can loop, stutter, or skip words on texts >500 characters. Split long texts into sentence-level chunks
- **API-only models lock you in** - Qwen3.5-Omni offers the best end-to-end experience but is API-only. Plan for fallback to open models (OmniVoice, VoxCPM2) if cost or availability becomes an issue
- **Tokenizer-free vs codec tradeoff** - tokenizer-free models (VoxCPM2) preserve prosodic detail that codec-based models lose during tokenization, but they tend to be larger and slower

## See Also

- [[voice-cloning]] - dedicated coverage of cloning techniques and cross-lingual transfer
- [[voice-design]] - creating unique voice identities from text descriptions, voice mixing (Slerp, Cartesia, VoxMorph)
- [[asr-stt-compression]] - KV cache compression for TTS inference (TriAttention, TurboQuant)
- [[audio-generation]] - music and sound effect generation
- [[speech-recognition]] - ASR models used for TTS evaluation (WER measurement)
