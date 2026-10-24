---
title: "Conversion vocale"
category: techniques
tags: [voice-conversion, real-time, rvc, so-vits, singing-voice, speaker-identity]
level: 3
source_sha256: 4225d0ff96ffc6c342d20aecedb98621aa6ab89fe7a0664239e9d7a0c481b923
translation: machine
translated_at: '2026-10-24'
---
# Conversion vocale {#voice-conversion}

La conversion vocale (VC, *voice conversion*) transforme l'identité du locuteur dans un audio existant tout en préservant le contenu linguistique, la prosodie et le timing. Contrairement au clonage vocal (qui génère une nouvelle parole à partir d'un texte), la VC travaille sur des enregistrements existants : l'entrée est un audio, et non un texte.

## Points clés {#key-facts}

- La conversion vocale opère sur un audio existant : parole d'entrée -> parole de sortie avec une identité vocale différente
- Différence essentielle avec le clonage par TTS : la VC préserve le timing, l'intonation et l'émotion d'origine
- RVC (Retrieval-based Voice Conversion) est l'approche open-source dominante, basée sur VITS + recherche par retrieval
- Conversion vocale en temps réel possible avec une latence inférieure à 20 ms sur GPU, ce qui permet de modifier la voix en direct
- La conversion de voix chantée (SVC) est une application majeure : appliquer la voix de n'importe quel chanteur à un enregistrement
- Les modèles de VC nécessitent généralement 10 à 30 minutes de données d'entraînement pour le locuteur cible

## Architecture {#architecture}

### RVC (Retrieval-based Voice Conversion) {#rvc-retrieval-based-voice-conversion}

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

### SO-VITS-SVC {#so-vits-svc}

Spécialisé dans la conversion de voix chantée.

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

## Conversion vocale en temps réel {#real-time-voice-conversion}

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

### Pipeline de streaming {#streaming-pipeline}

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

## Conversion vocale vs clonage vocal {#voice-conversion-vs-voice-cloning}

| Aspect | Conversion vocale | Clonage vocal (TTS) |
|--------|-----------------|-------------------|
| Entrée | Enregistrement audio | Texte |
| Préserve | Timing, prosodie, émotion | Rien (génération à partir de zéro) |
| Timing de sortie | Identique à l'entrée | Déterminé par le modèle |
| Cas d'usage | Changer de locuteur dans un audio existant | Générer une nouvelle parole |
| Données d'entraînement | 10 à 30 min pour le locuteur cible | 5 s (zero-shot) à plusieurs heures |
| Temps réel | Oui (avec optimisation) | Dépend du modèle |
| Chant | Excellent (modèles SVC) | Médiocre (les modèles TTS ne chantent pas bien) |

## Entraîner un modèle de VC {#training-a-vc-model}

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

## Applications {#applications}

- **Voix chantée** : appliquer le timbre de n'importe quel chanteur à vos propres enregistrements
- **Doublage** : remplacer l'identité du comédien de doublage tout en conservant le timing de la performance d'origine
- **Confidentialité** : anonymiser l'identité du locuteur dans les enregistrements
- **Accessibilité** : convertir la parole vers une voix que l'auditeur trouve plus facile à comprendre
- **Streaming en direct** : modification vocale en temps réel pour les créateurs de contenu

## Pièges à éviter {#gotchas}

- **Un écart de tessiture provoque des artefacts** - convertir une voix masculine grave vers une voix féminine aiguë (ou l'inverse) produit des vibrato instables et des artefacts robotiques aux extrêmes de hauteur. Maintenez la source et la cible à moins d'une octave l'une de l'autre, ou utilisez un décalage de hauteur explicite comme étape de prétraitement
- **Le paramètre index_rate de RVC est critique mais mal documenté** - à 0.0, aucun retrieval n'est utilisé (sortie brute de l'encodeur, moins proche de la cible). À 1.0, retrieval complet (plus proche de la cible mais peut sonner haché). La valeur optimale se situe généralement entre 0.3 et 0.6, selon l'écart entre les voix source et cible
- **La musique de fond traverse la conversion** - les modèles de VC sont entraînés sur de la parole propre. La musique ou le bruit présents en entrée passent inchangés ou créent des artefacts. Séparez toujours d'abord les voix (Demucs/UVR5), convertissez, puis remixez

## Voir aussi {#see-also}

- [[voice-cloning]] - clonage vocal basé sur le TTS, approche complémentaire
- [[tts-models]] - architectures TTS partageant des composants avec la VC (VITS, HuBERT)
- [[audio-generation]] - génération musicale, pertinente pour les applications SVC
