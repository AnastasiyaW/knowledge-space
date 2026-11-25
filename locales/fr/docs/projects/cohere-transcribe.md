---
title: "Cohere Transcribe"
category: projects
date: 2026-03-27
tags: [cohere-transcribe, project]
aliases: ["Cohere Transcribe"]
level: 2
source_sha256: b52cdcdcfa2e2a807e37e60a66673cdb8891845d5f8b0eb44ec1160074a1612c
translation: machine
translated_at: '2026-10-24'
---
# Cohere Transcribe {#cohere-transcribe}

**Ligne de développement :** `project:cohere-transcribe` · fil `cohere-transcribe`  
**Dernier événement :** 2026-03-27 · 1 événement daté depuis le 2026-03-27 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Cohere Transcribe est un modèle ASR encodeur-décodeur Conformer sous licence Apache-2.0, destiné aux flux de travail audio-vers-texte.

- Transcrit 14 langues avec le modèle de base `cohere-transcribe-03-2026`.
- S'exécute localement via Transformers ou vLLM, ou via l'API de transcription de Cohere.
- Ajoute `cohere-transcribe-arabic-07-2026` pour les dialectes arabes et l'audio arabe-anglais.

## Ligne de développement {#development-line}

- **2026-03-27 — Cohere publie les ressources de son modèle Cohere Transcribe.** Le 2026-03-27, Cohere a publié les ressources de Cohere Transcribe : une page de blog, un dépôt de modèle sur Hugging Face et un espace de démonstration. La page Model Vault liée situe le projet dans l'offre d'accès aux modèles de Cohere.

## Changements {#what-changed}

- 2026-03-27 — `cohere-transcribe-03-2026` intègre la gamme de produits comme modèle ASR ouvert de 2B paramètres couvrant 14 langues ; Cohere date la publication du 2026-03-26.
- 2026-07-07 — Cohere publie le fine-tune séparé `cohere-transcribe-arabic-07-2026` de 2B paramètres, destiné aux dialectes arabes, à la parole arabe-anglaise et aux charges de travail avec alternance de code.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-27, évaluez Cohere Transcribe via le dépôt de modèles publié par Cohere et l'espace de démonstration, et vérifiez les documents Cohere associés pour les conditions d'accès et de déploiement.

1. Choisissez `cohere-transcribe-03-2026` pour le modèle de base couvrant 14 langues ; choisissez `cohere-transcribe-arabic-07-2026` lorsque la charge de travail est majoritairement en arabe ou en arabe-anglais.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
2. Pour la solution hébergée, obtenez une clé API Cohere et envoyez une requête multipart à `POST /v2/audio/transcriptions` avec `model`, un `language` au format ISO-639-1 et le fichier audio.
  — <https://docs.cohere.com/reference/create-audio-transcription>
3. Limitez les fichiers d'entrée hébergés à 25 Mo maximum et utilisez les formats FLAC, MP3, MPEG, MPGA, OGG ou WAV.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
4. Pour l'inférence locale, chargez le checkpoint de base avec Transformers, fournissez l'audio à 16 kHz et définissez explicitement la langue ; pour les enregistrements longs, utilisez le chemin de découpage en segments décrit dans la fiche du modèle.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
5. Pour un service de production auto-hébergé, suivez le chemin de déploiement vLLM de Cohere et appelez son endpoint de transcription audio compatible OpenAI.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>

## Bonnes pratiques {#best-practices}

- Spécifiez une seule langue attendue par requête, car le modèle de base ne dispose pas de détection automatique de la langue et produit des textes incohérents sur un audio à alternance de code.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Placez une détection d'activité vocale (VAD) ou un noise gate en amont du modèle pour que les silences et le bruit ambiant de faible niveau ne génèrent pas de texte.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Ajoutez une étape distincte de diarisation et d'horodatage si l'application exige l'identification des locuteurs ou le timing des mots ; le modèle de base ne fournit ni l'un ni l'autre.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Utilisez le fine-tune arabe plutôt que le modèle de base pour les dialectes arabes et la parole arabe-anglaise ; Cohere annonce des gains par rapport au modèle de base sur ces deux cas.
  — <https://cohere.com/blog/transcribe-arabic>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-26 — Le fine-tune arabe du 2026-07-07 remplace le modèle de base à 14 langues pour la transcription des dialectes arabes et de l'arabe-anglais ; le modèle de base reste pris en charge pour son éventail plus large de langues.

## Points inconnus {#still-unknown}

- Il n'existe aucune annonce officielle en chinois simplifié ni de documentation d'usage en chinois ; la prise en charge de la transcription en mandarin n'établit pas de consignes d'exploitation localisées.
- Les résultats publiés au classement et en débit sont des mesures communiquées par le fournisseur ; nous ne les avons pas reproduits de manière indépendante.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://cohere.com/blog/transcribe | Introducing Cohere Transcribe: a new state-of-the-art in open-source speech recognition | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-03-2026 | CohereLabs/cohere-transcribe-03-2026 | 2026-09-05 |
| https://huggingface.co/blog/CohereLabs/cohere-transcribe-03-2026-release | Introducing Cohere-transcribe: state-of-the-art speech recognition | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Notes de version | 2026-09-05 |
| https://docs.cohere.com/docs/transcribe | Cohere Transcribe | 2026-09-05 |
| https://docs.cohere.com/reference/create-audio-transcription | Créer une transcription | 2026-09-05 |
| https://docs.cohere.com/docs/audio-transcription-quickstart | Transcription audio - démarrage rapide | 2026-09-05 |
| https://cohere.com/blog/transcribe-arabic | Meet Cohere Transcribe Arabic | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-arabic-07-2026 | CohereLabs/cohere-transcribe-arabic-07-2026 | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:cohere-transcribe`, fil `cohere-transcribe`, 1 événement daté du 2026-03-27 au 2026-03-27.
- **Note pratique :** À partir du 2026-03-27, les praticiens doivent évaluer Cohere Transcribe via le dépôt de modèles publié par Cohere et l'espace de démonstration, tout en vérifiant les documents Cohere associés pour les conditions d'accès et de déploiement.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
