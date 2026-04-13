---
title: "Voice Design and Voice Mixing"
description: "Creating unique synthetic voices from text descriptions, voice morphing, naturalness benchmarks, and cross-language voice identity. Covers Qwen3-TTS VoiceDesign, VoxMorph, Cartesia embeddings, MOS scores."
---

# Voice Design and Voice Mixing

Creating a synthetic voice identity without cloning a specific person. Two approaches: text description-based voice design, and voice mixing (interpolating between existing voice embeddings). As of 2026, multiple open-source models support voice design; quality gap to commercial APIs has narrowed to 0.1-0.2 MOS.

## Voice Design from Text Descriptions

### Qwen3-TTS VoiceDesign

Control via `instruct` parameter. 7 controllable dimensions: gender, age (specific years), pitch, speaking pace, emotional tone, timbre characteristics, scenario.

```python
# Example prompt (15-40 words optimal)
voice_description = """
A young adult woman, around 25 years old. Low-pitched voice with a 
deliberate, steady pace. Calm and professional tone, suitable for 
audiobook narration.
"""
```

**5 principles:**
1. Be specific ("deep, crisp, fast-paced" not "nice voice")
2. Use multiple dimensions simultaneously
3. Be objective (physical qualities, not feelings)
4. Be original (no celebrity imitation)
5. Sweet spot: 15-40 words, information-dense

**NOT controllable**: accent (requires reference audio for most models).

### OmniVoice (Structured Attribute Control)

```text
Attributes (one per category, freely combinable):
  Gender:  male / female
  Age:     child / teenager / young adult / middle-aged / elderly
  Pitch:   very low / low / medium / high / very high
  Style:   normal / whisper
  EN accent: american / british / australian / indian / chinese /
              canadian / korean / portuguese / russian / japanese
  CN dialect: Sichuan / Shaanxi / Henan / ... (regional)
```

Unique: **accent selection** in text form - most models require reference audio for accent.

### VoxCPM2 (Tokenizer-Free, April 2026)

Text-based voice design with tokenizer-free diffusion-AR architecture. Avoids quantization artifacts from codec tokenization, preserving prosodic nuance. 48kHz native output, 30+ languages, Apache 2.0.

### Parler-TTS

Free-form text description, no reference audio required at all. Less precise than structured control but requires zero audio assets.

```python
# parler-tts usage
description = "a warm female voice with slight British accent, speaking slowly and clearly"
input_ids = tokenizer(description, return_tensors="pt").input_ids
prompt_ids = tokenizer(text, return_tensors="pt").input_ids
generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)
```

## Voice Mixing / Blending

### Cartesia Sonic (Production API)

192-dimensional voice embeddings. Linear interpolation in API or playground.

```python
# Voice mixing via Cartesia API
new_voice = w1 * voice_a_embedding + w2 * voice_b_embedding
# Note: perception is non-linear - 50/50 mix may need non-equal weights
# Use prototype embeddings to add speed/emotion characteristics
```

**MOS 4.7** (Sonic 2), ~90ms TTFB. Commercial only.

### VoxMorph (Research, ICASSP 2026)

Disentangles voice into **prosody embedding** (rhythm, pitch) + **timbre embedding** (vocal tract, formants). Mixes independently using **Slerp** (spherical linear interpolation).

```text
Method:
  speaker_a (5 sec) -> prosody_embedding, timbre_embedding
  speaker_b (5 sec) -> prosody_embedding, timbre_embedding
  
  Slerp on hypersphere:
  new_voice = Slerp(timbre_a, timbre_b, α) + Slerp(prosody_a, prosody_b, β)
  
  Result: voice texture of speaker A + speaking style of speaker B
```

Zero-shot (no retraining). 2.6x quality improvement over prior methods, 73% reduction in intelligibility errors. `github.com/Bharath-K3/VoxMorph`

### INSIDE Method (APSIPA 2025)

Creates novel speaker identities that "fill gaps" between real speakers in embedding space.

```text
Select nearby speaker pairs → compute Slerp intermediates
→ novel identity between them
+5.24% speaker verification improvement
+13.44% gender classification gain
```

### Slerp vs Linear Interpolation

**Always prefer Slerp** for voice embeddings. Linear interpolation of high-dimensional vectors changes vector magnitude, causing artifacts. Slerp travels along the hypersphere surface:

```python
import numpy as np

def slerp(v0, v1, t):
    """Spherical linear interpolation."""
    dot = np.clip(np.dot(v0, v1), -1.0, 1.0)
    theta = np.arccos(dot) * t
    relative = v1 - v0 * dot
    relative /= np.linalg.norm(relative)
    return v0 * np.cos(theta) + relative * np.sin(theta)
```

## What Makes Voices Unnatural

| Problem | Cause | Best Solutions |
|---------|-------|---------------|
| Flat prosody / monotone | TTS "averages" pitch variation | Sesame CSM (context-aware), Fish S2 (15K+ tags), Orpheus |
| Missing micro-pauses | Uniform word spacing | VoxCPM2 (tokenizer-free timing), Sesame CSM |
| No breathing | TTS omits intake breaths | Orpheus (`<sigh>` tags), Chatterbox (`[cough]`, `[laugh]`) |
| Emotion flatness | Prosody ignores meaning | Fish S2 Pro (sub-word tags), IndexTTS-2.5 (8D emotion vector) |
| Context ignorance | No understanding of WHY | Sesame CSM (conversational context modeling) |
| Pitch range compression | Narrower than human | VoxCPM2 (48kHz, no tokenization loss) |

**Workaround techniques:**
- Inject commas, ellipses, micro-pause markers to guide prosody
- Use SSML or model-specific tags for emphasis/pause/breathing
- Provide conversational context (Sesame CSM)
- RL alignment post-training: Fish S2, CosyVoice 3

## Naturalness Benchmarks (MOS, 2026)

| Model | MOS | Method |
|-------|-----|--------|
| Sesame CSM | 4.7 | CMOS (Expresso dataset) - context-aware |
| Cartesia Sonic 2 | 4.7 | Industry benchmark |
| Orpheus TTS | 4.6 | Reported |
| Fish Audio S2 Pro (EN) | 4.50 expressiveness | Internal eval |
| Fish Audio S2 Pro (CN) | 4.94 expressiveness | Internal eval - strongest for Chinese |
| Human speech (ref) | 4.5-4.8 | Varies by recording |

**Quality gap shrinkage**: 2023: top open-source ~1.0 MOS below ElevenLabs. 2026: 0.1-0.2 MOS gap. Multiple open-source models now match or exceed ElevenLabs.

**Human preference win rates:**
- Fish S2 Pro: #1 TTS Arena (Bradley-Terry 3.07)
- Voxtral 4B: 68.4% vs ElevenLabs Flash v2.5 (blind test)
- Chatterbox-Turbo: 63.75% preference over ElevenLabs

## Controllable Voice Characteristics by Model

| Characteristic | Qwen3-TTS | OmniVoice | VoxCPM2 | Fish S2 |
|---------------|-----------|-----------|---------|---------|
| Gender | Yes | Yes | Yes | Via ref audio |
| Age (specific years) | Yes | 5 categories | Yes | Via ref audio |
| Pitch | Yes | 5 levels | Yes | Via tags |
| Speaking pace | Yes | No | Yes | Via tags |
| Emotion | Yes | No | Yes | 15K+ tags |
| Accent | **No** | EN accents + CN dialects | Unknown | Via ref audio |
| Whisper | Unknown | Yes | Unknown | `[whisper]` |
| Breathing/laughs | No | No | No | Partial |

## Cross-Language Voice Identity

Maintaining the same voice identity across languages:

```text
Workflow:
  1. Create voice in English first (most training data, strongest base)
  2. Test same description/embedding in target language (RU, CN)
  3. If inconsistent: Voxtral 4B for cross-lingual identity preservation
     (preserves accent, inflection, intonation across language switch)
```

**For RU+CN+EN**: Qwen3-TTS is the only model combining voice design + all three languages + competitive quality.

## Gotchas

- **Accent cannot be designed from text in most models.** Only OmniVoice offers structured accent selection. For all others, capture accent through reference audio from a native speaker with the desired accent
- **Non-linear perception of mixing weights.** A 50/50 blend of two voices rarely sounds like "50% each" - it may sound 80% like one voice. Tune weights iteratively and perceptually, not mathematically
- **Short text descriptions lose specificity.** Descriptions under 10 words produce generic voices. Under 15 words, model defaults dominate. Use 15-40 words and specify multiple dimensions (age + pitch + pace + emotional tone)
- **Voice design is not stable across inference runs.** Unlike voice cloning (deterministic with same reference), text-described voices vary between generations. Save the exact prompt AND generation parameters if reproducibility matters

## See Also

- [[tts-models]] - model comparison including voice design capabilities
- [[voice-cloning]] - cloning from reference audio
- [[voice-agent-pipelines]] - integrating TTS into real-time voice systems
- [[speech-recognition]] - ASR models for evaluation (WER measurement)
