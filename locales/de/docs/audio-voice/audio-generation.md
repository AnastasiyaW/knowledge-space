---
title: "Audiogenerierung"
category: reference
tags: [music-generation, sound-effects, ace-step, video-to-audio, diffusion, audio-synthesis]
level: 3
source_sha256: 224b7dcef1ce0fc97cbeee769ea8950ba97346998de9234c36a730fdb31f3876
translation: machine
translated_at: '2026-10-24'
---
# Audiogenerierung {#audio-generation}

Audiogenerierung umfasst Musiksynthese, die Erstellung von Soundeffekten und die Synchronisation von Audio mit Video (Video-to-Audio). Das Feld verwendet dieselben Diffusions- und Transformer-Architekturen wie die Bildgenerierung, jedoch angewendet auf Mel-Spektrogramme oder Audio-Codec-Tokens.

## Wichtige Fakten {#key-facts}

- Musikgenerierungsmodelle erzeugen entweder Mel-Spektrogramme oder diskrete Audio-Tokens und dekodieren diese anschließend zu einer Wellenform
- Die DiT-Architektur (Diffusion Transformer) dominiert die aktuelle Musikgenerierung (ACE-Step, Stable Audio)
- Video-to-Audio-(V2A-)Modelle erzeugen synchronisierte Soundeffekte aus Videobildern
- Die meisten Musikmodelle erzeugen Clips fester Länge (30 s bis 3 min), keine vollständigen Songs
- Liedtext-konditionierte Generierung ist ein aktives Forschungsfeld – die Erzeugung von Gesangsstimmen, die einem Text und einer Melodie folgen
- Der VRAM-Bedarf reicht von 4 GB (kleine Modelle) bis 24 GB+ (Generierung in voller Qualität)

## Musikgenerierungsmodelle {#music-generation-models}

### ACE-Step {#ace-step}

Groß angelegte Musikgenerierung mit DiT-Architektur.

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

### Weitere Musikmodelle {#other-music-models}

| Modell | Parameter | Ansatz | Steuerung | Ausgabe |
|-------|--------|----------|---------|--------|
| ACE-Step 1.5 XL | 4B | DiT-Diffusion | Text + Stil | Stereo-Musik |
| Stable Audio 2.0 | ~1B | Latente Diffusion | Text + Timing | 44,1 kHz Stereo, bis zu 3 min |
| MusicGen (Meta) | 1,5B–3,3B | AR-Codec (EnCodec) | Text + Melodie | 32 kHz Mono, 30 s |
| Udio | Proprietär | Unbekannt | Text + Stil | Vollständige Songs mit Gesang |
| Suno v3 | Proprietär | Unbekannt | Text + Liedtext | Vollständige Songs mit Gesang |

## Generierung von Soundeffekten {#sound-effect-generation}

Modelle, die nicht-musikalische Audioinhalte erzeugen (Schritte, Explosionen, Umgebungsgeräusche, UI-Sounds).

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

### PrismAudio {#prismaudio}

Video-to-Audio mit Chain-of-Thought-Reasoning.

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

## Audio-Verarbeitungspipeline {#audio-processing-pipeline}

### Generierung und Nachbearbeitung {#generation-post-processing}

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

### Kombination mit Video {#combining-with-video}

```text
Video + generated audio alignment:
  1. Extract video features (frame embeddings, motion, scene cuts)
  2. Generate audio conditioned on video features
  3. Time-stretch audio to match video duration exactly
  4. Apply cross-fade at scene boundaries
  5. Mix with dialogue/music tracks
  
Tools: ffmpeg for muxing, pyrubberband for time-stretching
```

## Evaluation {#evaluation}

- **FAD** (Fréchet Audio Distance) – analog zu FID bei Bildern, misst die Ähnlichkeit der Verteilungen
- **KL-Divergenz** – zwischen den Merkmalsverteilungen von generiertem und Referenzaudio
- **CLAP-Score** – Ähnlichkeit zwischen Audio und Text (vergleichbar mit CLIP für Audio), misst die Prompt-Treue
- **MOS** – Hörtests mit Probanden, nach wie vor der Goldstandard
- **Onset-Genauigkeit** – für V2A, misst die zeitliche Übereinstimmung von Klangereignissen mit dem Video

## Stolpersteine {#gotchas}

- **Musikgenerierung erzeugt Loops, keine Kompositionen** – die meisten Modelle erzeugen repetitive Muster, die nach 30–60 Sekunden wie eine Schleife klingen. Für längere Stücke sollten überlappende Segmente erzeugt und überblendet werden (Crossfade) oder Modelle verwendet werden, die gezielt für die Struktur ausgelegt sind (ACE-Step SFT)
- **Codec-Artefakte bei niedriger Bitrate** – Modelle, die EnCodec/DAC mit niedrigen Bitraten (1,5 kbps) verwenden, erzeugen metallische, wässrige Artefakte. Verwenden Sie immer die höchste Codec-Bitrate, die der VRAM zulässt
- **V2A-Synchronisation verschlechtert sich bei schneller Bewegung** – Video-to-Audio-Modelle haben Schwierigkeiten mit schnellen visuellen Ereignissen (Explosionen, schnelle Schnitte). Erzeugte Geräusche hinken um 100–300 ms hinterher. Eine manuelle Korrektur der Ausrichtung ist oft nötig

## Siehe auch {#see-also}

- [[tts-models]] – Sprachgenerierung, teilt Diffusions- und Codec-Architekturen
- [[podcast-processing]] – Audiobearbeitung und Verarbeitungspipelines
- [[voice-conversion]] – Techniken zur Echtzeit-Audioverarbeitung
