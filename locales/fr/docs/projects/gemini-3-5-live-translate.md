---
title: "Gemini 3.5 Live Translate — Traduction Gemini Live"
category: projects
date: 2026-06-13
tags: [gemini-3-5-live-translate, gemini-live-translation, gemini_models, project]
aliases: ["Gemini 3.5 Live Translate"]
level: 2
source_sha256: dd37c852c2cf4e4e468500bd56f82e994196e32a988cb45333b6f9f326a9d837
translation: machine
translated_at: '2026-10-24'
---
# Gemini 3.5 Live Translate — Traduction Gemini Live {#gemini-35-live-translate-gemini-live-translation}

**Ligne de développement :** `project:gemini-3-5-live-translate` · fil `gemini-live-translation`  
**Dernier événement :** 2026-06-13 · 1 événement daté depuis le 2026-06-13 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Gemini 3.5 Live Translate est le modèle de traduction audio-vers-audio à faible latence de Google, destiné aux conversations orales en temps réel.

- Détection automatique parmi plus de 70 langues
- Parole traduite en continu
- Transcriptions optionnelles de l'entrée et de la sortie

Le modèle reste en préversion, n'accepte que l'audio et ne prend en charge ni les outils ni les instructions. Utilisez-le comme un pipeline d'interprétation, et non comme un agent vocal généraliste.

## Ligne de développement {#development-line}

- **2026-06-13 — Google a présenté la préversion de Gemini 3.5 Live Translate.** Le 2026-06-13, Google a introduit Gemini 3.5 Live Translate en tant que modèle en préversion pour la traduction en temps réel dans Gemini Live. La version fournissait un guide de l'API Live, une URL de préversion Live dans AI Studio, ainsi que des références d'intégration pour LiveKit et Pipecat.

## Ce qui a changé {#what-changed}

- 2026-06-13 — Gemini 3.5 Live Translate est devenu accessible aux développeurs en préversion publique, via l'API Gemini Live et Google AI Studio.
- 2026-08-26 — Google a publié la fiche modèle de Gemini 3.5 Audio. Elle documente les limites de contexte de Live Translate, soit 128K en entrée et 64K en sortie, ainsi que les modes de défaillance liés à la voix, à la détection de langue et au bruit de fond.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-13, évaluez la préversion de Gemini 3.5 Live Translate via l'API Gemini Live ou AI Studio. Vérifiez le chemin d'intégration LiveKit ou Pipecat avant de l'adopter.

1. Créez un client de l'API Gemini et ouvrez une session de l'API Live avec le modèle `gemini-3.5-live-translate-preview`.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
2. Définissez `response_modalities` sur audio et renseignez `translationConfig.targetLanguageCode` avec un code de langue cible au format BCP-47.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
3. Diffusez du PCM 16 bits, 16 kHz, mono, little-endian, par blocs d'environ 100 ms ; consommez l'audio PCM 24 kHz renvoyé.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
4. Activez la transcription de l'entrée et de la sortie lorsque le produit a besoin de sous-titres, de journalisation ou d'une traduction lisible en complément de l'audio.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>

## Bonnes pratiques {#best-practices}

- Traitez-le comme un flux de traduction continu plutôt que comme un agent fonctionnant par tours de parole. Le mode traduction ne prend en charge ni outils, ni instructions, ni saisie de texte, ni image, ni vidéo.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- Pour les clients navigateur ou mobile, utilisez des jetons éphémères v1beta et contraignez `translationConfig` côté serveur, sauf si les utilisateurs doivent eux-mêmes choisir la langue cible.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- Testez les accents non natifs, les changements de langue rapides, les longues pauses, les appels à plusieurs locuteurs et les environnements bruyants avant de vous appuyer opérationnellement sur l'audio traduit.
  — <https://deepmind.google/models/model-cards/gemini-3-5-audio/>
- Prévoyez un budget pour l'audio d'entrée diffusé et l'audio de sortie généré : Google indique un tarif payant effectif d'environ 0,0368 $ par minute.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Remplacé par cette version {#superseded-by-this}

- 2026-06-09 — Google prévoyait de remplacer l'ancienne limite de traduction vocale de Google Meet, soit cinq langues avec une traduction centrée sur l'anglais, par plus de 70 langues et plus de 2 000 combinaisons linguistiques.

## Points non élucidés {#still-unknown}

- Les pages actuelles de LiveKit et Pipecat décrivent des intégrations génériques de Gemini Live, et non un adaptateur ou une configuration documentés et propres à Gemini 3.5 Live Translate. Validez ce chemin d'intégration avant de considérer l'un ou l'autre comme prenant en charge la traduction.
- Les documents publics de Google établissent la préversion publique pour les développeurs, mais ne fournissent aucune date de disponibilité générale pour le modèle d'API.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/ | Gemini 3.5 Live Translate est disponible | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/live-api/live-translate | Traduction en direct avec l'API Gemini Live | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3.5-live-translate-preview | Référence du modèle Gemini 3.5 Live Translate | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/pricing | Tarification de l'API Gemini Developer | 2026-09-05 |
| https://deepmind.google/models/model-cards/gemini-3-5-audio/ | Gemini 3.5 Audio (Live Translate, Transcribe, Transcribe Live) fiche modèle | 2026-09-05 |
| https://docs.livekit.io/agents/models/realtime/plugins/gemini/ | Plugin de l'API Gemini Live | 2026-09-05 |
| https://docs.pipecat.ai/pipecat/features/gemini-live | Développer avec Gemini Live | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:gemini-3-5-live-translate`, fil `gemini-live-translation`, 1 événement daté du 2026-06-13 au 2026-06-13.
- **Note pratique :** À partir du 2026-06-13, évaluez la préversion de Gemini 3.5 Live Translate via l'API Gemini Live ou AI Studio, et vérifiez le chemin d'intégration LiveKit ou Pipecat avant de l'adopter.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
