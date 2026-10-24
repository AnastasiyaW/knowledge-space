---
title: "Traitement de podcasts"
category: patterns
tags: [podcast, diarization, transcription, speaker-separation, editing, sommelier, nemo]
level: 3
source_sha256: fa92be475c0a18d8c6c2e92b953ba9f34a8dee1a6329b109fa9cd2bc81359c4f
translation: machine
translated_at: '2026-10-24'
---
# Traitement de podcasts {#podcast-processing}

Les pipelines de traitement de podcasts de bout en bout assurent la diarisation des locuteurs (qui parle et quand), la transcription, la suppression de la musique et du bruit, et la génération de sorties structurées. Le pipeline Sommelier illustre une approche open source moderne combinant plusieurs modèles spécialisés.

## Points clés {#key-facts}

- La diarisation des locuteurs identifie et étiquette les différents locuteurs dans un audio à plusieurs voix
- La diarisation moderne utilise des embeddings neuronaux de locuteurs + du clustering (spectral, agglomératif ou NME-SC)
- Le pipeline Sommelier combine : NeMo Sortformer (diarisation) + Whisper/Parakeet (ASR) + Canary (traduction)
- La séparation de sources (Demucs, UVR5) isole les voix de la musique et du bruit avant la transcription
- pyannote.audio est le framework open source de diarisation le plus populaire
- Pipeline typique d'un podcast : séparer les sources -> diariser -> transcrire -> aligner -> formater

## Pipeline de traitement complet {#full-processing-pipeline}

```text
Raw podcast audio (mixed speakers, music, ads)
  |
  v
1. Source Separation (Demucs / UVR5)
   -> vocals_track.wav (speech only)
   -> music_track.wav (background music, jingles)
   -> noise_track.wav (ambient noise)
  |
  v
2. Voice Activity Detection (Silero VAD / pyannote VAD)
   -> speech segments with timestamps
   -> silence regions marked for potential cuts
  |
  v
3. Speaker Diarization (pyannote / NeMo Sortformer)
   -> speaker labels: Speaker_A [0:00-0:15], Speaker_B [0:15-0:32], ...
   -> overlap regions detected
  |
  v
4. ASR Transcription (Whisper / Parakeet)
   -> text aligned to speaker segments
   -> word-level timestamps via forced alignment
  |
  v
5. Post-Processing
   -> Merge same-speaker consecutive segments
   -> Remove filler words (configurable)
   -> Generate: SRT subtitles, JSON transcript, show notes
```

## Diarisation des locuteurs {#speaker-diarization}

### Pipeline pyannote.audio {#pyannoteaudio-pipeline}

```python
from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="HF_TOKEN"
)

diarization = pipeline("podcast.wav", num_speakers=2)  # or min/max_speakers

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"[{turn.start:.1f}s - {turn.end:.1f}s] {speaker}")
```

### NeMo Sortformer {#nemo-sortformer}

```text
NeMo Sortformer (used in Sommelier):
  - Sort-based diarization: predicts speaker order, not just clusters
  - Handles overlapping speech better than clustering approaches
  - Integrates with NeMo ASR models for joint optimization
  - Scales to 10+ speakers without predefined count
```

## Pipeline Sommelier {#sommelier-pipeline}

Traitement de podcasts open source combinant des modèles parmi les meilleurs de leur catégorie.

```text
Sommelier components:
  1. Source separation - remove music/jingles from speech
  2. NeMo Sortformer - speaker diarization with overlap handling
  3. Whisper / Parakeet - transcription (Parakeet for EN, Whisper for multilingual)
  4. Canary - optional translation to other languages
  5. Post-processor - format output as transcript with speaker labels

Key advantage: each component is replaceable. 
Swap Whisper for Parakeet for better English WER.
Swap pyannote for Sortformer for better overlap handling.
```

## Séparation de sources {#source-separation}

```text
Models for vocal isolation:
  Demucs (Meta) - 4-stem separation (vocals, drums, bass, other)
  UVR5 - multiple architectures, strong vocal isolation
  MDX-Net - competitive with Demucs, different architecture
  
For podcasts, only vocal stem is needed.
Run before ASR to remove background music/jingles.
```

## Formats de sortie {#output-formats}

### Sous-titres SRT avec locuteurs {#srt-subtitles-with-speakers}

```text
1
00:00:01,200 --> 00:00:04,800
[Host] Welcome to the show. Today we're 
talking about machine learning.

2
00:00:05,100 --> 00:00:08,900
[Guest] Thanks for having me. I've been 
working on transformer architectures.
```

### Transcription JSON structurée {#structured-json-transcript}

```json
{
  "speakers": ["Host", "Guest"],
  "segments": [
    {
      "speaker": "Host",
      "start": 1.2,
      "end": 4.8,
      "text": "Welcome to the show. Today we're talking about machine learning.",
      "words": [
        {"word": "Welcome", "start": 1.2, "end": 1.6, "confidence": 0.98},
        {"word": "to", "start": 1.6, "end": 1.7, "confidence": 0.99}
      ]
    }
  ],
  "metadata": {
    "duration": 3600.0,
    "language": "en",
    "num_speakers": 2
  }
}
```

## Pipeline d'édition {#editing-pipeline}

Après la transcription, l'édition basée sur le texte permet de couper l'audio en éditant le texte :

```text
Text-based audio editing workflow:
  1. Transcribe with word-level timestamps
  2. Display transcript in editor UI
  3. User deletes/rearranges text
  4. Map text edits back to audio timestamps
  5. Apply non-destructive audio cuts
  6. Crossfade at edit points (10-50ms) to avoid clicks
  
Tools: Descript (commercial), audapolis (open source)
```

## Pièges à éviter {#gotchas}

- **La diarisation échoue sur des voix similaires** - lorsque deux locuteurs ont des caractéristiques vocales proches (même genre, âge, accent), la diarisation par clustering les fusionne souvent en un seul locuteur. Fournir explicitement `num_speakers` ou utiliser NeMo Sortformer (basé sur l'ordre, et non sur le clustering) aide considérablement
- **La séparation de sources introduit des artefacts dans la parole** - l'isolation vocale de Demucs peut créer une légère coloration métallique dans la voix. Pour les pipelines ASR uniquement, c'est acceptable (le WER reste similaire). Pour un audio destiné à la publication, appliquer une égalisation légère après la séparation
- **Le chevauchement de parole détruit la précision de la transcription** - lorsque deux locuteurs parlent simultanément, la précision de l'ASR chute à 30-50 %. Détecter les chevauchements dans la diarisation, les signaler dans la sortie, et envisager un enregistrement sur piste séparée pour les contenus critiques

## Voir aussi {#see-also}

- [[speech-recognition]] - modèles ASR et détails d'utilisation de Whisper
- [[voice-cloning]] - les techniques de préparation de l'audio de référence recoupent le prétraitement des podcasts
- [[audio-generation]] - génération musicale pour les intros/outros de podcasts
