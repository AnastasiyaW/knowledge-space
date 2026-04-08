---
title: Voice Cloning
category: techniques
tags: [voice-cloning, speaker-embedding, cross-lingual, zero-shot, safety, tts]
---

# Voice Cloning

Voice cloning reproduces a target speaker's voice characteristics (timbre, pitch, rhythm) from a reference audio sample. Modern zero-shot approaches need only 5-30 seconds of clean audio, eliminating the need for hours of training data per speaker.

## Key Facts

- Zero-shot cloning extracts a speaker embedding from reference audio and conditions TTS generation on it
- Speaker embeddings are typically 256-512 dimensional vectors from models like ECAPA-TDNN, WavLM, or Resemblyzer
- Cross-lingual cloning preserves voice identity while generating speech in a language the speaker never recorded
- Fine-tuned cloning (speaker adaptation) produces higher quality but requires 1-5 hours of target audio + GPU training
- Quality depends heavily on: reference audio cleanliness, recording conditions, speaker consistency in reference

## Approaches

### Zero-Shot (No Training)

Extract speaker embedding from reference, inject into TTS decoder. No fine-tuning required.

```text
Reference audio (5-30 sec)
  -> Speaker encoder (ECAPA-TDNN / WavLM)
  -> Speaker embedding (256-512 dim vector)
  -> TTS decoder conditioned on embedding + text
  -> Generated speech in target voice
```

**Models supporting zero-shot cloning:**
- LEMAS-TTS, F5-TTS, CosyVoice 2 (flow matching)
- XTTS v2, VoxCPM2, Fish Speech (autoregressive)
- OmniVoice - 600+ languages, tag control for emotions

### Speaker Adaptation (Fine-Tuning)

Fine-tune a base TTS model on target speaker data. Higher quality, but requires compute.

```text
Base TTS model + 1-5 hours of target speaker audio
  -> Fine-tune decoder layers (freeze encoder)
  -> Speaker-specific model checkpoint
  -> Generate with text input only (no reference needed at inference)
```

Typically 500-2000 training steps, 10-30 minutes on a single GPU.

### Voice Design (Text-Described)

Multiple models now support generating a voice from a text description rather than audio reference.

```text
VoxCPM2 voice design:
  "A warm, deep male voice with slight British accent, age 40-50"
  -> Voice design module (built into tokenizer-free pipeline)
  -> Synthetic speaker embedding
  -> TTS generation at 48kHz studio quality

OmniVoice attribute-based design:
  Attributes: gender=male, age=40-50, pitch=low, dialect=british, style=warm
  -> Parametric attribute control (not free-text)
  -> Can specify: whisper, shouting, specific dialect
  -> Works across 600+ languages
```

**Comparison:**
- VoxCPM2: free-text description, more flexible, 30+ languages
- OmniVoice: attribute-based, more predictable results, 600+ languages

## Cross-Lingual Cloning

The speaker's voice identity transfers across languages they never spoke. Quality varies by language distance.

```text
Quality hierarchy for cross-lingual transfer:
  Same language family (EN -> DE):     High quality
  Same script (EN -> FR):              Good quality  
  Different family (EN -> ZH):         Moderate quality
  Low-resource target (EN -> Swahili): Lower quality
```

**Key challenge:** prosody patterns are language-specific. A cloned English speaker in Mandarin may sound foreign in rhythm even if timbre is perfect. VoxCPM2 and OmniVoice specifically optimize for this.

**Cloning from minimal reference (2026 state of the art):**

| Model | Min Reference | Languages | Cross-Lingual | Notes |
|-------|--------------|-----------|---------------|-------|
| OmniVoice | Few seconds | 600+ | Yes, zero-shot | Noise-robust intake |
| VoxCPM2 | Short clip | 30+ | Yes | Diffusion-AR preserves emotion |
| Voxtral 4B | 3 seconds | 9 | Limited | Captures accent + disfluencies |
| Qwen3.5-Omni | Voice upload | 36 TTS | Yes, 20 languages tested | WER 1.87 across languages, cosine sim 0.79 |

Qwen3.5-Omni achieves the best measured cloning fidelity (WER 1.87 across 20 languages) but is API-only.

## Emotion and Style Control

Modern cloning models support tag-based emotion injection:

```text
Tag-controlled generation (OmniVoice, Orpheus):
  Input: "I can't believe it! [surprise] This is amazing [joy]"
  Tags: [laugh], [surprise], [sadness], [whisper], [shouting]
  
  The model generates speech with corresponding emotional inflection
  at tagged positions, while maintaining target speaker's voice identity.
```

## Reference Audio Preparation

```text
Optimal reference characteristics:
  Duration:    10-30 seconds (sweet spot for most models)
  Content:     Natural speech, varied intonation, no music/effects
  Quality:     Clean recording, low noise floor, no reverb
  Format:      WAV 16-bit, 24kHz+ sample rate, mono
  Speaker:     Single speaker, consistent voice (no whispering then shouting)

Preprocessing pipeline:
  1. Source separation (UVR5 / Demucs) - remove background music
  2. Noise reduction (DeepFilterNet / RNNoise) - reduce ambient noise
  3. Trim silence (ffmpeg silenceremove) - remove dead air
  4. Normalize loudness (ffmpeg loudnorm) - consistent level
  5. Resample to model's expected rate (usually 24kHz)
```

## Voice Mixing: Creating Novel Voice Identities

Modern TTS models expose speaker embeddings as vectors. Mixing embeddings creates voices that don't correspond to any real person.

### Linear Interpolation (Cartesia Sonic)

Cartesia Sonic uses 192-dimensional speaker embeddings (floats -1 to 1):

```python
import numpy as np

def mix_voices(embedding_a: np.ndarray, embedding_b: np.ndarray, 
               weight_a: float = 0.5) -> np.ndarray:
    """Linear interpolation between two speaker embeddings."""
    weight_b = 1.0 - weight_a
    return weight_a * embedding_a + weight_b * embedding_b

# Via Cartesia API:
import requests

new_voice = requests.post("https://api.cartesia.ai/voices", json={
    "name": "Custom Mix",
    "embedding": mix_voices(voice_a_embedding, voice_b_embedding, 0.6).tolist()
}).json()
```

**Warning:** Perception does NOT change linearly with interpolation coefficient. A 50/50 mix may require non-equal weights (e.g. 0.7/0.3) to achieve perceptually balanced output. Use prototype embeddings (speed/emotion controls) to fine-tune characteristics.

### Spherical Linear Interpolation (Slerp) - Research Method

Slerp preserves vector magnitude on the high-dimensional hypersphere, minimizing artifacts compared to linear interpolation. Used in VoxMorph (ICASSP 2026):

```python
def slerp(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Spherical linear interpolation between two embedding vectors."""
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    
    dot = np.clip(np.dot(a_norm, b_norm), -1.0, 1.0)
    theta = np.arccos(dot)
    
    if np.abs(theta) < 1e-6:
        return a  # vectors nearly identical
    
    return (np.sin((1 - t) * theta) * a + np.sin(t * theta) * b) / np.sin(theta)
```

**VoxMorph advantage:** Disentangles prosody embedding (rhythm, pitch) from timbre embedding (vocal tract, formants). Can mix speaking style from speaker A with voice texture from speaker B independently. Input: 5 seconds per source speaker, zero-shot.

### INSIDE Method (Novel Identity Generation)

Selects pairs of nearby speaker embeddings and computes intermediate identities via Slerp. Creates voices that "fill gaps" in embedding space between real speakers. Validated: +5.24% speaker verification improvement, +13.44% gender classification gain.

## What Makes Synthetic Voices Sound Unnatural

The most common naturalness failures and which models address them:

| Problem | Symptom | Best Solutions |
|---------|---------|---------------|
| Flat prosody | Monotone regardless of content | Sesame CSM (context-aware), Fish S2 (15K+ tags) |
| Missing micro-pauses | Uniform word spacing | Sesame CSM (natural umms/uhhs), VoxCPM2 (tokenizer-free) |
| Absent breathing | No breath intakes between sentences | Orpheus TTS (`<sigh>`, natural breathing) |
| Emotion flatness | Same intonation for joke vs tragedy | Fish S2 Pro (sub-word emotion), IndexTTS-2.5 (8D vector) |
| Pitch range compression | Narrower pitch than humans | VoxCPM2 48kHz (no tokenization loss), CosyVoice 3 (RL) |
| Context ignorance | Words read, not understood | Sesame CSM (conversational context modeling) |
| Robotic transitions | "Concatenated" word boundaries | RL-aligned models (Fish S2, CosyVoice 3) |

**Practical workarounds:**
- Inject commas, ellipses, micro-pause markers to guide prosody
- Use model-specific tags (`[laugh]`, `[excited]`, `[whisper]`) for expression
- Provide conversational history for context-aware models (Sesame CSM)
- RL-aligned post-training improves naturalness without architecture changes

## Naturalness Benchmarks (2026)

| Model | MOS | Win Rate | Notes |
|-------|-----|----------|-------|
| Sesame CSM | 4.7 | near-human (without context) | English only |
| Cartesia Sonic 2 | 4.7 | — | ~90ms TTFB |
| Orpheus TTS | 4.6 | — | Llama-3B based |
| Fish S2 Pro (EN) | 4.50 exp / 4.21 nat | Bradley-Terry 3.07 #1 | vs all major competitors |
| Fish S2 Pro (ZH) | 4.94 exp / 4.40 nat | — | Strongest in Chinese |
| Human speech | ~4.5-4.8 | Reference | Varies by recording |

**Key trend:** Quality gap between top open-source and commercial TTS shrunk from ~1.0 MOS (2023) to 0.1-0.2 MOS (2026). Fish S2 Pro beats gpt-4o-mini-tts on EmergentTTS-Eval (81.88% win rate). Voxtral beats ElevenLabs Flash v2.5 in blind tests.

## Safety and Ethics

- **Consent**: voice cloning without speaker consent is illegal in many jurisdictions
- **Deepfake detection**: generated speech can be detected via spectral analysis, watermarking (AudioSeal by Meta), or artifact detection
- **Watermarking**: some models (LEMAS, CosyVoice) embed inaudible watermarks in generated audio
- **Rate limiting**: production deployments should limit cloning requests per user/API key
- **Speaker verification**: pair cloning APIs with speaker verification to confirm the uploader is the voice owner

## Gotchas

- **Short references degrade on rare phonemes** - a 5-second clip may not contain enough phonetic diversity. The model invents missing sounds, sometimes inconsistently. Use 15-30 sec references with diverse content. Exception: Voxtral 4B is specifically designed for 3-second references
- **Background noise in reference transfers to output** - even small amounts of room reverb or air conditioning hum get encoded in the speaker embedding and appear in all generated speech. Always denoise first. Exception: OmniVoice explicitly handles noisy reference samples
- **Cross-lingual accent bleed** - if the reference audio is in English, generated Chinese speech often has an English-accented rhythm. Providing reference audio in the target language (even a few seconds) dramatically improves results
- **API-only cloning = vendor lock-in** - Qwen3.5-Omni has the best measured cloning quality but is API-only. Build fallback paths to open models (OmniVoice, VoxCPM2) for production systems

## See Also

- [[tts-models]] - model architectures and comparison table
- [[voice-conversion]] - changing voice identity in existing recordings
- [[speech-recognition]] - ASR for transcription-based alignment in cloning pipelines
