---
title: Audio Generation
category: reference
tags: [music-generation, sound-effects, ace-step, video-to-audio, diffusion, audio-synthesis]
---

# Audio Generation

Audio generation covers music synthesis, sound effect creation, and video-to-audio synchronization. The field uses the same diffusion and transformer architectures as image generation but applied to mel-spectrograms or audio codec tokens.

## Key Facts

- Music generation models produce either mel-spectrograms or discrete audio tokens, then decode to waveform
- DiT (Diffusion Transformer) architecture dominates recent music generation (ACE-Step, Stable Audio)
- Video-to-audio (V2A) models generate synchronized sound effects from video frames
- Most music models generate fixed-length clips (30s-3min), not full songs
- Lyrics-conditioned generation is an active frontier - generating singing voices that follow text + melody
- VRAM requirements range from 4GB (small models) to 24GB+ (full-quality generation)

## Music Generation Models

### ACE-Step

Large-scale music generation using DiT architecture.

```text
ACE-Step 1.5 XL:
  Architecture:  4B parameter DiT (Diffusion Transformer)
  Variants:      xl-base, xl-sft, xl-turbo
  VRAM:          >= 12GB (with CPU offload)
  Output:        Stereo audio, variable length
  Control:       Text prompt + optional style tags
  
  xl-turbo uses fewer diffusion steps for faster generation
  xl-sft is fine-tuned on curated high-quality music
```

### Other Music Models

| Model | Params | Approach | Control | Output |
|-------|--------|----------|---------|--------|
| ACE-Step 1.5 XL | 4B | DiT diffusion | Text + style | Stereo music |
| Stable Audio 2.0 | ~1B | Latent diffusion | Text + timing | 44.1kHz stereo, up to 3min |
| MusicGen (Meta) | 1.5B-3.3B | AR codec (EnCodec) | Text + melody | 32kHz mono, 30s |
| Udio | Proprietary | Unknown | Text + style | Full songs with vocals |
| Suno v3 | Proprietary | Unknown | Text + lyrics | Full songs with vocals |

## Sound Effect Generation

Models that generate non-musical audio (footsteps, explosions, ambience, UI sounds).

```text
Common approaches:
  1. Text-to-audio diffusion (AudioLDM 2, Tango)
     Input: "rain on a tin roof with distant thunder"
     Output: matching audio clip
     
  2. Video-to-audio (PrismAudio, V2A-Mapper)
     Input: video frames
     Output: synchronized sound effects
     
  3. Retrieval + neural blending
     Input: text description
     Process: retrieve similar sounds from library, blend/modify with neural model
```

### PrismAudio

Video-to-audio with Chain-of-Thought reasoning.

```text
PrismAudio (518M params):
  Pipeline:
    1. Video frames -> visual encoder -> scene understanding
    2. Chain-of-Thought: "I see a person walking on gravel,
       then a door opening. Sound should be: footsteps on 
       gravel (0-2s), door creak (2-3s), indoor ambience (3-5s)"
    3. CoT description -> audio diffusion model -> synchronized audio
    
  SOTA on Video-to-Audio benchmarks
  Key insight: explicit reasoning about sound sources improves sync quality
```

## Audio Processing Pipeline

### Generation + Post-Processing

```python
# Typical audio generation post-processing
import torchaudio
import torch

# After model generates raw audio:
# 1. Loudness normalization
transform = torchaudio.transforms.Loudness(sample_rate=44100)

# 2. High-pass filter to remove sub-bass rumble
# 3. Limiter to prevent clipping
# 4. Fade in/out to avoid clicks

# For music: additional mastering chain
# - EQ (parametric equalization)
# - Compression (dynamic range)  
# - Stereo widening
# - Final limiting to -1dBFS
```

### Combining with Video

```text
Video + generated audio alignment:
  1. Extract video features (frame embeddings, motion, scene cuts)
  2. Generate audio conditioned on video features
  3. Time-stretch audio to match video duration exactly
  4. Apply cross-fade at scene boundaries
  5. Mix with dialogue/music tracks
  
Tools: ffmpeg for muxing, pyrubberband for time-stretching
```

## Evaluation

- **FAD** (Frechet Audio Distance) - analogous to FID for images, measures distribution similarity
- **KL divergence** - between generated and reference audio feature distributions
- **CLAP score** - audio-text similarity (like CLIP for audio), measures prompt adherence
- **MOS** - human listening tests, still the gold standard
- **Onset accuracy** - for V2A, measures temporal alignment of sound events with video

## Gotchas

- **Music generation produces loops, not compositions** - most models generate repetitive patterns that sound like a loop after 30-60 seconds. For longer pieces, generate overlapping segments and crossfade, or use models specifically designed for structure (ACE-Step SFT)
- **Audio codec artifacts at low bitrate** - models using EnCodec/DAC at low bitrates (1.5kbps) produce metallic, watery artifacts. Always use the highest codec bitrate your VRAM allows
- **V2A sync degrades on fast motion** - video-to-audio models struggle with rapid visual events (explosions, fast cuts). Generated sounds lag by 100-300ms. Manual alignment correction is often needed

## See Also

- [[tts-models]] - speech generation, shares diffusion and codec architectures
- [[podcast-processing]] - audio editing and processing pipelines
- [[voice-conversion]] - real-time audio processing techniques
