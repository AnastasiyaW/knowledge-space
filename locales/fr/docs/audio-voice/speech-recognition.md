---
title: "Reconnaissance vocale"
category: reference
tags: [asr, whisper, parakeet, qwen3-asr, streaming, transcription, multilingual, speech-to-text, edge-asr]
level: 4
source_sha256: 8d1ab5119e8fb8851aed2e004eca1ee32dce2be7ca11320783099c9d11c5b084
translation: machine
translated_at: '2026-10-24'
---
# Reconnaissance vocale {#speech-recognition}

La reconnaissance automatique de la parole (ASR, Automatic Speech Recognition) convertit un signal audio parlé en texte. Début 2026, le domaine a dépassé la domination de Whisper : Qwen3-ASR, Canary-Qwen de NVIDIA et Voxtral Realtime surpassent nettement Whisper en précision et/ou en vitesse. Whisper large-v3 reste une référence fiable, mais n'a pas été mis à jour.

## Faits clés {#key-facts}

- **Qwen3-ASR** (janv. 2026) est le nouveau SOTA open source pour l'ASR multilingue : 52 langues, Apache 2.0, entraîné sur ~40M d'heures
- **MAI-Transcribe-1** (avr. 2026) est le nouveau SOTA commercial : 3,8 % de WER sur les 25 langues principales de FLEURS, propriétaire
- Whisper large-v3 reste viable, mais n'a pas reçu de mise à jour v4 : l'écosystème l'a dépassé
- Le streaming ASR est désormais prêt pour la production avec Voxtral Realtime (13 langues) et Nemotron Speech (EN, <24 ms)
- L'ASR embarqué est viable avec moins de 1 Go de RAM grâce à Moonshine v2 (27M de paramètres, 50 ms) et Parakeet.cpp (C++ pur)
- L'architecture SALM (Speech-Augmented Language Model) combine un encodeur ASR et un décodeur LLM pour la transcription et le raisonnement dans un seul modèle

## Comparatif des modèles {#model-comparison}

| Modèle | Architecture | Paramètres | Langues | Streaming | WER de référence | Points forts |
|-------|-------------|--------|-----------|-----------|---------|----------|
| Qwen3-ASR 1.7B | AuT + LLM Qwen3 | 1,7B | 52 | Oui (dynamique) | TEDLIUM 4,50 | Meilleur open multilingue |
| MAI-Transcribe-1 | Transformer enc-dec | ? | 25 | Non | FLEURS 3,8 % | Meilleure précision commerciale |
| Canary-Qwen 2.5B | FastConformer + Qwen3 | 2,5B | EN (+LLM) | Non | LS-Clean 1,6 % | ASR + résumé/QA |
| Voxtral Realtime 4B | LM + encodeur | 4B | 13 | Oui (80 ms à 2,4 s) | Qualité proche du mode hors ligne | Latence configurable |
| Whisper large-v3 | Transformer enc-dec | 1,55B | 100+ | Non | LS 2,7 % | Le plus de langues, stable |
| Parakeet-TDT-V3 | FastConformer-TDT | 0,6B | 25 langues européennes | Oui | RTFx ~2000 | ASR anglais open le plus rapide |
| Canary-1B-V2 | CTC multi-tâches | 1B | 25 langues européennes (dont RU) | Non | 10x plus rapide que des modèles 3x plus grands | Traduction intégrée |
| Nemotron Speech | Conformer à cache conscient du streaming | 0,6B | EN | Oui (<24 ms) | 7,2-7,8 % | 560 flux/H100 |
| Moonshine v2 Tiny | Encodeur de streaming ergodique | 27M | EN | Oui (50 ms) | Équivalent à des modèles 6x plus gros | Embarqué, <500 Mo de RAM |
| Fun-ASR-Nano | De bout en bout | ? | 31 (axé Asie) | Oui | 93 % en bruit | Dialectes et accents chinois |
| Whisper.cpp | Whisper GGML | 1,55B | 100+ | Par segments | ~3 % | Déploiement CPU/embarqué |

## Qwen3-ASR (open source recommandé, 2026) {#qwen3-asr-recommended-open-source-2026}

Meilleur ASR multilingue open source début 2026. Licence Apache 2.0. Entraîné sur ~40M d'heures de données pseudo-étiquetées.

```text
Architecture:
  AuT (Audio Transformer) encoder -> learned projector -> Qwen3 LLM decoder
  
  0.6B variant: AuT 180M params (hidden 896) + Qwen3 decoder
  1.7B variant: AuT 300M params (hidden 1024) + Qwen3 decoder

Key benchmarks (1.7B):
  TEDLIUM (EN): 4.50 WER  (vs GPT-4o 7.69, Whisper-lv3 6.84)
  WenetSpeech (ZH): 4.97  (vs GPT-4o 15.30, Whisper-lv3 9.86)
  Language ID (30 langs): 97.9% (vs Whisper-lv3 94.1%)

Streaming: dynamic flash attention, window 1s-8s
Latency (0.6B): 92ms TTFT, 2000x throughput at concurrency 128
Long audio: up to 20 minutes per pass
VRAM: ~2GB (0.6B), ~6GB (1.7B)
```

Publié également : Qwen3-ForcedAligner-0.6B, pour l'alignement texte-parole dans 11 langues.

## Utilisation de Whisper (référence historique) {#whisper-usage-legacy-baseline}

### Transcription de base {#basic-transcription}

```python
import whisper

model = whisper.load_model("large-v3")
result = model.transcribe("audio.mp3", language="en")

print(result["text"])
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
```

### Faster-Whisper (production) {#faster-whisper-production}

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", beam_size=5, vad_filter=True)

print(f"Detected language: {info.language} ({info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### Horodatage au niveau du mot {#word-level-timestamps}

```python
# Faster-Whisper word timestamps
segments, _ = model.transcribe("audio.mp3", word_timestamps=True)
for segment in segments:
    for word in segment.words:
        print(f"  {word.start:.2f}s - {word.end:.2f}s: '{word.word}' (p={word.probability:.2f})")
```

## Streaming ASR {#streaming-asr}

En 2026, le streaming ASR natif est prêt pour la production dans plusieurs langues.

```text
Native streaming models (recommended):
  1. Voxtral Realtime 4B - 13 languages (incl. EN/ZH/RU), configurable latency
     At 480ms: competitive with Whisper + ElevenLabs Scribe v2
     At 960ms: surpasses both
     At 2400ms: within 1% of offline quality
     Open-source, Apache 2.0, ~8-10GB VRAM

  2. Nemotron Speech Streaming 600M - English only, <24ms final transcripts
     Cache-Aware FastConformer-RNNT, chunk sizes 80-1120ms
     560 concurrent streams on single H100 at 320ms chunk
     3x throughput vs traditional buffered streaming

  3. Qwen3-ASR 0.6B - 52 languages, streaming via dynamic flash attention
     Window sizes 1s-8s, 92ms TTFT
     Best multilingual streaming option

  4. Moonshine v2 - 27M-medium params, edge streaming
     50ms (Tiny) to 258ms (Medium) latency
     <1GB memory, designed for edge processors

Legacy approaches (still valid for Whisper):
  5. Chunked Whisper - split into overlapping 30s chunks
     Latency: chunk_duration + inference (2-5 sec)
  
  6. VAD + Whisper - transcribe complete utterances
     Latency: utterance_end + inference
```

### Pipeline avec VAD {#vad-assisted-pipeline}

```python
# Silero VAD + Faster-Whisper pipeline
import torch
from faster_whisper import WhisperModel

vad_model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils

wav = read_audio('audio.wav', sampling_rate=16000)
speech_timestamps = get_speech_timestamps(wav, vad_model, sampling_rate=16000)
# Each timestamp = a speech segment to transcribe independently
```

## WhisperX : alignement amélioré {#whisperx-enhanced-alignment}

WhisperX ajoute un alignement phonémique forcé pour des frontières de mots précises, indispensable pour l'édition de la parole et la génération de sous-titres.

```text
WhisperX pipeline:
  1. Whisper transcription (batch mode for speed)
  2. VAD-based segmentation (cut on silence)
  3. Forced alignment via wav2vec2 / MMS alignment model
  4. Speaker diarization (optional, via pyannote)
  
Output: word-level timestamps with <50ms accuracy
```

## Guide de sélection de l'ASR multilingue {#multilingual-asr-selection-guide}

Meilleur modèle par combinaison de langues (open source, 2026) :

| Cible | Meilleur modèle | Solution de repli | Remarques |
|--------|-----------|----------|-------|
| ZH + EN + RU | Qwen3-ASR 1.7B | Voxtral Realtime | Qwen3 écrase Whisper en chinois |
| EN uniquement | Canary-Qwen 2.5B | Parakeet-TDT V3 | 1,6 % de WER + mode raisonnement LLM |
| EN en streaming | Nemotron Speech | Voxtral Realtime | <24 ms, 560 flux/H100 |
| Multi en streaming | Voxtral Realtime | Qwen3-ASR 0.6B | 13 langues, latence configurable |
| Dialectes chinois | Fun-ASR-Nano | Qwen3-ASR | 7 dialectes, 26 accents |
| Edge / mobile | Moonshine v2 Tiny | Sherpa-ONNX | 27M de paramètres, <500 Mo de RAM |
| SOTA commercial | MAI-Transcribe-1 | Qwen3.5-Omni ASR | 3,8 % de WER sur FLEURS, API uniquement |

## Remarques par langue {#language-specific-notes}

- **Russe** : Qwen3-ASR et Voxtral Realtime prennent tous deux en charge le RU. Canary-1B-V2 inclut le RU parmi ses 25 langues européennes. Whisper reste viable pour le russe seul
- **Chinois** : Qwen3-ASR est le grand gagnant, avec un WER de 4,97 sur WenetSpeech contre 9,86 pour Whisper. Fun-ASR-Nano excelle sur les dialectes chinois (wu, cantonais, hokkien, etc.)
- **Alternance de langues** (mélange de langues dans une même phrase) : Qwen3-ASR et Fun-ASR-Nano gèrent mieux les changements de langue libres que Whisper
- **Parole accentuée** : Fun-ASR-Nano couvre 26 variétés d'accents régionaux chinois. Pour les autres langues, la diversité des données d'entraînement de Whisper offre une robustesse aux accents raisonnable

## ASR embarqué / en périphérie {#on-device-edge-asr}

```text
Deployment options (2026):
  Moonshine v2 Tiny:  27M params, <500MB RAM, 50ms latency
  Parakeet.cpp:       Pure C++, no Python/ONNX, Metal GPU 27ms/10s audio
  Sherpa-ONNX:        Android/iOS/HarmonyOS/RPi/RISC-V, 12 languages
  Qwen3-ASR 0.6B:     MLX port for Apple Silicon (mlx-qwen3-asr)
  whisper.cpp:         CPU/Metal, still viable for Whisper models

Edge deployment guidelines:
  - INT4/INT8 quantization essential for mobile
  - Streaming architectures reduce memory 40%+ vs standard transformers
  - Tiny/Base variants: <500MB RAM target
```

## Évaluation de la prononciation {#pronunciation-assessment}

Le scoring de prononciation open source reste un point faible. Les API propriétaires (Azure Speech, SpeechSuper) dominent.

Meilleure voie open source : Qwen3-ASR + alignement forcé (Qwen3-ForcedAligner-0.6B) + scoring GOP (goodness of pronunciation).

Ressources disponibles :
- **SpeechOcean762** : jeu de données public (5000 phrases en anglais avec scores de qualité)
- **Kaldi GOP** : métrique Goodness of Pronunciation, mature
- **Qwen3-ForcedAligner-0.6B** : alignement texte-parole dans 11 langues, brique de base pour le scoring de prononciation

## Pièges courants {#gotchas}

- **Whisper hallucine sur le silence** : si l'entrée contient de longs segments silencieux, Whisper génère du texte fantôme (phrases répétées, mots aléatoires). Appliquez toujours un filtrage VAD avant la transcription (`vad_filter=True` dans faster-whisper). Les modèles récents (Qwen3-ASR, Voxtral) sont plus robustes face à ce problème
- **La fenêtre de 30 secondes coupe les mots** : la fenêtre de contexte fixe de 30 s de Whisper peut couper des mots aux frontières. Les modèles de streaming natifs (Voxtral Realtime, Nemotron) évitent totalement ce problème grâce à des architectures à fenêtre glissante
- **La détection de langue se fait par fichier, pas par segment** : Whisper détecte la langue une seule fois pour l'ensemble de l'audio. Qwen3-ASR propose une identification de langue par segment, avec une précision de 97,9 % sur 30 langues
- **La précision des horodatages varie avec le débit de parole** : les horodatages de mots issus de l'attention croisée de Whisper sont approximatifs (±200 ms). Pour un alignement précis, utilisez l'alignement forcé de WhisperX ou Qwen3-ForcedAligner
- **Whisper n'est plus le meilleur choix pour la plupart des tâches** : début 2026, Qwen3-ASR surpasse Whisper en précision pour les langues prises en charge, Voxtral Realtime le bat en streaming, et Moonshine v2 le bat en embarqué. L'avantage de Whisper se limite au nombre de langues (100+ contre 52)
- **Le compromis VRAM/précision a changé** : Qwen3-ASR 0.6B, avec ~2 Go de VRAM, surpasse Whisper large-v3 (~10 Go) en chinois. Consultez les benchmarks avant d'opter par défaut pour des modèles plus grands

## Voir aussi {#see-also}

- [[podcast-processing]] : pipeline complet combinant ASR, diarisation et montage
- [[tts-models]] : modèles TTS qui utilisent l'ASR pour l'évaluation de la qualité
- [[voice-cloning]] : alignement WhisperX utilisé dans les workflows d'édition de la parole
- [[asr-stt-compression]] : compression du cache KV pour l'inférence ASR/TTS (TriAttention, TurboQuant)
