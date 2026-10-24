---
title: "Langswap — Pile de traduction de la parole et de doublage"
category: projects
date: 2026-06-11
tags: [langswap, project, speech-translation-and-dubbing-stack]
aliases: ["Langswap"]
level: 3
source_sha256: a2d4878caac2568fc6a01c09f35d9ed1a0974b73fbe5b083deab010b5dedf984
translation: machine
translated_at: '2026-10-24'
---
# Langswap — Pile de traduction de la parole et de doublage {#langswap-speech-translation-and-dubbing-stack}

**Ligne de développement :** `project:langswap` · fil `speech-translation-and-dubbing-stack`  
**Dernier événement :** 2026-06-11 · 1 événement daté depuis le 2026-06-11 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Langswap est un outil local de doublage vidéo destiné aux équipes qui ont besoin d'un contrôle direct sur les fichiers multimédias et les modèles.

Composants de la pile par défaut :
- ASR : transcrit l'audio avec faster-whisper large-v3 et marque les segments de parole avec Silero VAD.
- Traduction : traduit le texte à l'aide de Gemma-4-E2B GGUF.
- Clonage vocal TTS : synthétise la parole avec OmniVoice.
- Synchronisation en sortie : aligne la synchronisation de la parole et exporte des fichiers de sous-titres SRT.

Prérequis et limites :
Nécessite Python 3.12 et un GPU NVIDIA avec une pile CUDA-13. Les contenus à forts enjeux nécessitent une relecture manuelle.

## Ligne de développement {#development-line}

- **2026-06-11 — Langswap a fait apparaître une pile modulaire de traduction et de doublage de la parole.** Le 2026-06-11, Langswap a référencé les chemins sources d'un gestionnaire de reconnaissance vocale, d'un client ASR/VAD, d'un client de traduction Llama.cpp, d'un client TTS OmniVoice et de FFmpeg. Les liens incluaient également le dépôt principal et un article sur le doublage par IA. Nous ne pouvons pas confirmer, à partir de ces liens, si les fichiers référencés ont été créés ou modifiés à cette date.

## Ce qui a changé {#what-changed}

- 2026-06-11 — les sources décrivent un pipeline modulaire allant de la vidéo aux segments ASR, à la traduction, au TTS et à l'assemblage FFmpeg. L'instantané disponible ne confirme pas de version distincte à cette date.

## Mode d'emploi {#how-to-use-this}

À compter du 2026-06-11, considérez l'ASR/VAD, la traduction, le TTS et FFmpeg comme des points d'intégration distincts. Vérifiez leur comportement à l'exécution et leurs versions avant toute utilisation en production.

1. Installez Python 3.12, les pilotes GPU NVIDIA, ffmpeg et rubberband-cli. Utilisez uv avec l'extra gpu pour la pile GPU locale.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
2. Construisez l'image Docker, lancez-la avec `--gpus all` et montez les répertoires des poids et des données pour un démarrage rapide.
  — <https://github.com/langswap-app/langswap>
3. Ouvrez Gradio à l'adresse localhost:7860, importez une vidéo et choisissez la langue cible pour produire un fichier MP4 ainsi que les fichiers SRT source et traduit.
  — <https://github.com/langswap-app/langswap>
4. Exécutez `main.py local` pour le débogage : le JSON intermédiaire est enregistré dans `data/<id>`, de sorte que les redémarrages ignorent les étapes déjà terminées.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
5. Activez la diarisation uniquement si nécessaire, car elle requiert un accès HF_TOKEN à pyannote/speaker-diarization-3.1.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>

## Bonnes pratiques {#best-practices}

- Conservez l'ASR VAD comme configuration par défaut, sauf si vous avez besoin d'un alignement forcé séparé : faster-whisper fournit le texte et Silero VAD marque les limites de la parole.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py>
- Relancez les étapes en échec via le runner local plutôt que de retraiter l'intégralité de la vidéo : la transcription et la remise en correspondance des segments sont mises en cache.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py>
- Faites vérifier le texte, les codes temporels et l'intonation par un relecteur humain avant toute publication d'actualités ou de films : un flux de travail avec intervention humaine définit la limite pratique de l'automatisation.
  — <https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza>
- Vérifiez la licence AGPL-3.0-or-later du code source ainsi que les conditions de licence des modèles téléchargés avant tout déploiement commercial ou réseau.
  — <https://github.com/langswap-app/langswap>

## Remplacé par {#superseded-by-this}

- 2026-06-24 — aucun remplacement confirmé du SRT n'existe : la PR n° 12 suggère WebVTT, mais elle reste ouverte et ne modifie pas la sortie documentée.

## Points encore inconnus {#still-unknown}

- Nous ne disposons pas d'instantané Git daté du 2026-06-11 ; nous ne pouvons donc pas vérifier une version ni l'état exact du code à cette date.
- La documentation est contradictoire au sujet de HF_TOKEN : le README indique que Gemma est un modèle à accès restreint, tandis que le guide avancé n'exige le jeton que pour la diarisation pyannote.
- Aucun benchmark indépendant de bout en bout ne confirme la qualité, la vitesse ou la compatibilité matérielle de la pile actuelle.
- Les requêtes de recherche en chinois n'ont donné aucune source primaire ou pratique exploitable.
- 2026-06-11 : un article publié le 2026-02-01 souligne les limites du doublage modulaire : l'automatisation accélère le travail de premier jet, mais la précision, la culture et l'émotion exigent un humain dans la boucle. Il s'agit d'un article d'opinion, non d'un benchmark.
- 2026-06-24 : la PR n° 12 suggère de remplacer la génération de sous-titres SRT par WebVTT, mais ces modifications ne sont pas fusionnées et ne constituent pas une version.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/langswap-app/langswap | langswap — dépôt GitHub | 2026-09-05 |
| https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md | langswap — guide avancé | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py | Source de SpeechToTextManager | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py | Source du client ASR VAD | 2026-09-05 |
| https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza | Озвучка машиной : quels sont les problèmes du doublage par IA | 2026-09-05 |
| https://github.com/langswap-app/langswap/pull/12 | Pull request n° 12 : proposition SRT vers WebVTT | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:langswap`, fil `speech-translation-and-dubbing-stack`, 1 événement daté du 2026-06-11 au 2026-06-11.
- **Note pratique :** À compter du 2026-06-11, les praticiens qui évaluent Langswap doivent considérer l'ASR/VAD, la traduction, le TTS et FFmpeg comme des points d'intégration distincts dans son flux de travail de doublage vocal, et vérifier leur comportement à l'exécution et leurs versions avant de s'y fier.
- **Confiance :** moyenne. Les mentions « Remplacé par » datées font foi pour ce qui est obsolète.
