---
title: "Audio et voix"
description: "Reconnaissance vocale, synthèse vocale, clonage de voix et pipelines d'agents vocaux : comparaisons de modèles, benchmarks de latence et schémas d'intégration en production."
type: MOC
level: 2
source_sha256: 2da8cd2ffe7b18c38fe935ad2667933a39ebbd983382de863a5aa5d05e815c44
translation: machine
translated_at: '2026-10-24'
---
# Audio et voix {#audio-voice}

Les systèmes de traitement de la parole modernes couvrent trois domaines principaux : la reconnaissance de la parole (ASR), la synthèse de voix (TTS) et la conversion ou le clonage de l'identité du locuteur. Les articles de cette section traitent des familles de modèles actuelles (Whisper, Qwen3-ASR, NVIDIA Canary, F5-TTS, CosyVoice), des budgets de latence pour les agents vocaux temps réel, de l'infrastructure de fine-tuning sur GPU loués, et des compromis de déploiement multilingue. Chaque article est une référence dense : diagrammes d'architecture, commandes, benchmarks et pièges d'intégration, et non des tutoriels.

## Parole et reconnaissance {#speech-recognition}
- [[speech-recognition]] - modèles ASR, transcription, évaluation de la prononciation

## Synthèse vocale {#text-to-speech}
- [[tts-models]] - comparaison de modèles TTS, benchmarks de latence, support multilingue
- [[voice-cloning]] - clonage de voix, mixage de voix, benchmarks de naturalité
- [[voice-conversion]] - techniques et pipelines de conversion vocale
- [[audio-generation]] - modèles et workflows de génération audio
- [[audio-flamingo]] - artefacts de compréhension Audio Flamingo 3, Music Flamingo et AF-Next
- [[ace-step-1-5]] - ACE-Step 1.5 base/SFT/turbo et limites matérielles XL

## Applications vocales {#voice-applications}
- [[voice-agent-pipelines]] - pipelines et frameworks d'agents vocaux pour applications temps réel
- [[podcast-processing]] - traitement, transcription et analyse de podcasts

## Références complémentaires {#additional-references}

- [[asr-stt-compression]] - méthodes de compression du cache KV pour l'inférence ASR/TTS et le contexte des LLM en 2026 : TriAttention
- [[audio-omni-unified-model]] - modèle unique pour la compréhension, la génération et l'édition audio via un raisonnement LLM gelé + couche entraînable
- [[lemas-tts-and-speech-editing]] - modèles TTS multilingues open source LEMAS et d'édition de parole au niveau du mot - architecture
- [[tts-fine-tuning-infrastructure]] - comparaison de plateformes de location de GPU et schémas de déploiement pour le fine-tuning et le service de modèles TTS de 2B-4B
- [[voice-design]] - création de voix synthétiques uniques à partir de descriptions textuelles, morphing vocal, benchmarks de naturalité
