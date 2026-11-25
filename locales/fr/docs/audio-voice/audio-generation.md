---
title: "Génération audio"
category: reference
tags: [music-generation, sound-effects, ace-step, video-to-audio, diffusion, audio-synthesis]
level: 3
source_sha256: 224b7dcef1ce0fc97cbeee769ea8950ba97346998de9234c36a730fdb31f3876
translation: machine
translated_at: '2026-10-24'
---
# Génération audio {#audio-generation}

La génération audio couvre la synthèse musicale, la création d'effets sonores et la synchronisation vidéo-audio. Ce domaine utilise les mêmes architectures de diffusion et de transformeurs que la génération d'images, mais appliquées aux mel-spectrogrammes ou aux tokens de codecs audio.

## Points clés {#key-facts}

- Les modèles de génération musicale produisent soit des mel-spectrogrammes, soit des tokens audio discrets, puis décodent vers une forme d'onde
- L'architecture DiT (Diffusion Transformer) domine la génération musicale récente (ACE-Step, Stable Audio)
- Les modèles video-to-audio (V2A) génèrent des effets sonores synchronisés à partir des images vidéo
- La plupart des modèles musicaux génèrent des extraits de durée fixe (30 s à 3 min), et non des morceaux complets
- La génération conditionnée par les paroles est un front de recherche actif : générer des voix chantées qui suivent un texte et une mélodie
- Les besoins en VRAM vont de 4 Go (petits modèles) à 24 Go et plus (génération en qualité maximale)

## Modèles de génération musicale {#music-generation-models}

### ACE-Step {#ace-step}

Génération musicale à grande échelle utilisant l'architecture DiT.

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

### Autres modèles musicaux {#other-music-models}

| Modèle | Paramètres | Approche | Contrôle | Sortie |
|-------|--------|----------|---------|--------|
| ACE-Step 1.5 XL | 4B | Diffusion DiT | Texte + style | Musique stéréo |
| Stable Audio 2.0 | ~1B | Diffusion latente | Texte + temporalité | 44,1 kHz stéréo, jusqu'à 3 min |
| MusicGen (Meta) | 1,5B-3,3B | AR sur codec (EnCodec) | Texte + mélodie | 32 kHz mono, 30 s |
| Udio | Propriétaire | Inconnue | Texte + style | Morceaux complets avec voix |
| Suno v3 | Propriétaire | Inconnue | Texte + paroles | Morceaux complets avec voix |

## Génération d'effets sonores {#sound-effect-generation}

Modèles qui génèrent des sons non musicaux (pas de pas, explosions, ambiances, sons d'interface).

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

Video-to-audio avec raisonnement en chaîne de pensée (Chain-of-Thought).

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

## Pipeline de traitement audio {#audio-processing-pipeline}

### Génération et post-traitement {#generation-post-processing}

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

### Combinaison avec la vidéo {#combining-with-video}

```text
Video + generated audio alignment:
  1. Extract video features (frame embeddings, motion, scene cuts)
  2. Generate audio conditioned on video features
  3. Time-stretch audio to match video duration exactly
  4. Apply cross-fade at scene boundaries
  5. Mix with dialogue/music tracks
  
Tools: ffmpeg for muxing, pyrubberband for time-stretching
```

## Évaluation {#evaluation}

- **FAD** (Frechet Audio Distance) : analogue du FID pour les images, mesure la similarité des distributions
- **Divergence KL** : entre les distributions de caractéristiques audio générées et de référence
- **Score CLAP** : similarité audio-texte (comme CLIP pour l'audio), mesure le respect du prompt
- **MOS** : tests d'écoute humains, toujours la référence absolue
- **Précision des attaques (onset accuracy)** : pour le V2A, mesure l'alignement temporel des événements sonores avec la vidéo

## Pièges à éviter {#gotchas}

- **La génération musicale produit des boucles, non des compositions** : la plupart des modèles génèrent des motifs répétitifs qui sonnent comme une boucle après 30 à 60 secondes. Pour des pièces plus longues, générez des segments qui se chevauchent et utilisez un fondu enchaîné (crossfade), ou utilisez des modèles conçus spécifiquement pour la structure (ACE-Step SFT)
- **Artefacts du codec audio à faible débit** : les modèles utilisant EnCodec ou DAC à bas débit (1,5 kbps) produisent des artefacts métalliques et aqueux. Utilisez toujours le débit de codec le plus élevé que votre VRAM permet
- **La synchronisation V2A se dégrade sur les mouvements rapides** : les modèles video-to-audio peinent sur les événements visuels rapides (explosions, coupes rapides). Les sons générés accusent un retard de 100 à 300 ms. Une correction d'alignement manuelle est souvent nécessaire

## Voir aussi {#see-also}

- [[tts-models]] : génération de la parole, partage les architectures de diffusion et de codec
- [[podcast-processing]] : édition audio et pipelines de traitement
- [[voice-conversion]] : techniques de traitement audio en temps réel
