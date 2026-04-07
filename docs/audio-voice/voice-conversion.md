---
title: Voice Conversion
category: techniques
tags: [voice-conversion, real-time, rvc, so-vits, singing-voice, speaker-identity]
---

# Voice Conversion

Voice conversion (VC) transforms the speaker identity in existing audio while preserving linguistic content, prosody, and timing. Unlike voice cloning (which generates new speech from text), VC works on existing recordings - the input is audio, not text.

## Key Facts

- Voice conversion operates on existing audio: input speech -> output speech with different voice identity
- Key distinction from TTS cloning: VC preserves the original timing, intonation, and emotion
- RVC (Retrieval-based Voice Conversion) is the dominant open-source approach, based on VITS + retrieval
- Real-time VC achievable at <20ms latency on GPU, enabling live voice changing
- Singing voice conversion (SVC) is a major application - apply any singer's voice to a recording
- VC models typically need 10-30 minutes of target speaker training data

## Architecture

### RVC (Retrieval-based Voice Conversion)

```text
RVC pipeline:
  Input audio
    -> Pitch extraction (RMVPE / CREPE / Harvest)
    -> Content encoder (HuBERT / ContentVec) -> content features
    -> FAISS index retrieval -> find similar features from target speaker
    -> Blend retrieved features with encoder output (index_rate: 0.0-1.0)
    -> VITS decoder (conditioned on target speaker embedding)
    -> Pitch-shifted, voice-converted output
    
Training: 10-30 min of target speaker audio, ~20 min on GPU
Inference: real-time capable on modern GPU
```

### SO-VITS-SVC

Specialized for singing voice conversion.

```text
SO-VITS-SVC pipeline:
  Input singing audio
    -> Content encoder (ContentVec)
    -> F0 (pitch) extraction and explicit pitch curve
    -> VITS decoder with speaker conditioning
    -> Output: same melody, different voice
    
Key difference from RVC: explicit pitch modeling makes it
better for singing where pitch accuracy is critical.
Training: 1-4 hours of target singer audio recommended.
```

## Real-Time Voice Conversion

```text
Requirements for real-time VC (<50ms latency):
  - GPU: RTX 3060+ for comfortable real-time
  - Buffer size: 128-512 samples (3-11ms at 44.1kHz)
  - Lookahead: minimal (adds latency but improves quality)
  - Model: RVC with ONNX export or TensorRT optimization
  
Practical latency breakdown:
  Audio capture:     ~5ms (WASAPI/ASIO)
  Feature extraction: ~3ms (HuBERT on GPU)
  Conversion:        ~5ms (VITS decoder on GPU)
  Audio output:      ~5ms (WASAPI/ASIO)
  Total:             ~18ms (imperceptible)
```

### Streaming Pipeline

```python
# Conceptual real-time VC pipeline
import sounddevice as sd
import numpy as np

BLOCK_SIZE = 512  # ~11ms at 44.1kHz
SAMPLE_RATE = 44100

def callback(indata, outdata, frames, time, status):
    # indata: captured microphone audio
    audio_chunk = indata[:, 0]
    
    # Extract content features (HuBERT)
    features = content_encoder(audio_chunk)
    
    # Extract pitch (RMVPE)
    f0 = pitch_extractor(audio_chunk)
    
    # Convert voice identity
    converted = vits_decoder(features, f0, target_speaker_embedding)
    
    outdata[:, 0] = converted

stream = sd.Stream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=1,
    callback=callback
)
```

## Voice Conversion vs Voice Cloning

| Aspect | Voice Conversion | Voice Cloning (TTS) |
|--------|-----------------|-------------------|
| Input | Audio recording | Text |
| Preserves | Timing, prosody, emotion | Nothing (generates from scratch) |
| Output timing | Same as input | Model-determined |
| Use case | Change speaker in existing audio | Generate new speech |
| Training data | 10-30 min target speaker | 5 sec (zero-shot) to hours |
| Real-time | Yes (with optimization) | Depends on model |
| Singing | Excellent (SVC models) | Poor (TTS models can't sing well) |

## Training a VC Model

```text
RVC training workflow:
  1. Collect 10-30 min of clean target speaker audio
  2. Preprocess: denoise, normalize, segment into 5-15s clips
  3. Extract features: HuBERT content features + pitch (F0)
  4. Build FAISS index from target speaker features
  5. Train VITS decoder: 200-500 epochs, ~20 min on RTX 3090
  6. Test: convert a sample, check for artifacts
  
Quality tips:
  - More diverse training data (different emotions, speeds) = better model
  - Clean audio matters more than quantity
  - Pitch extraction method: RMVPE > CREPE > Harvest (quality vs speed)
```

## Applications

- **Singing voice**: apply any singer's timbre to your own recordings
- **Dubbing**: replace voice actor identity while keeping original performance timing
- **Privacy**: anonymize speaker identity in recordings
- **Accessibility**: convert speech to a voice the listener finds easier to understand
- **Live streaming**: real-time voice changing for content creators

## Gotchas

- **Pitch range mismatch causes artifacts** - converting a deep male voice to a high female voice (or vice versa) produces warbling and robotic artifacts at pitch extremes. Keep source and target within 1 octave of each other, or use explicit pitch shifting as a preprocessing step
- **RVC index_rate is a critical but poorly documented parameter** - at 0.0, no retrieval is used (pure encoder output, less like target). At 1.0, full retrieval (more like target but can sound choppy). Sweet spot is typically 0.3-0.6 depending on how different source and target voices are
- **Background music bleeds through conversion** - VC models are trained on clean speech. Music/noise in input passes through unchanged or creates artifacts. Always separate vocals first (Demucs/UVR5), convert, then remix

## See Also

- [[voice-cloning]] - text-to-speech based voice cloning, complementary approach
- [[tts-models]] - TTS architectures that share components with VC (VITS, HuBERT)
- [[audio-generation]] - music generation, relevant for SVC applications
