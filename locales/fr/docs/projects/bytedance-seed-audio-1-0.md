---
title: "Seed Audio 1.0 — Seed Audio"
category: projects
date: 2026-07-22
tags: [bytedance-seed-audio-1-0, project, seed-audio]
aliases: ["Seed Audio 1.0"]
level: 2
source_sha256: dc904428bbc6bfbd8a2103794ab9af11e7ed8a885e38bad742d12bc32f543104
translation: machine
translated_at: '2026-10-24'
---
# Seed Audio 1.0 — Seed Audio {#seed-audio-10-seed-audio}

**Ligne de développement :** `project:bytedance-seed-audio-1-0` · fil `seed-audio`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Seed Audio 1.0 est un modèle audio de ByteDance destiné aux créateurs de vidéos, de jeux, de publicités et de podcasts.

- Parole et dialogues à partir d'un prompt, avec des références de voix ou d'image.
- Effets sonores et ambiances générés dans le même passage.

L'API externe confirmée limite les entrées à trois références audio de 30 secondes chacune. Le matériel officiel annonce jusqu'à deux minutes d'audio en un seul passage.

Le modèle constitue une alternative à la synthèse vocale (TTS) et à la création sonore manuelle pour les ébauches de scènes audio. La responsabilité des droits sur les références de voix incombe à l'utilisateur.

## Ligne de développement {#development-line}

- **2026-07-22 — Page produit de Seed Audio 1.0 et parcours d'activation BytePlus.** Le 2026-07-22, des liens publics ont relié la page produit officielle de Seed Audio 1.0 à un parcours d'activation dans la console BytePlus Voice. Ensemble, ces liens officiels datés marquent une étape de mise à disposition publique et d'intégration du produit pour le projet. Ils ne permettent pas d'établir le libellé exact de l'annonce, l'ensemble des fonctionnalités, la disponibilité ni le périmètre de la publication.

## Changements {#what-changed}

2026-07-22 — Seed Audio 1.0 est devenu accessible via BytePlus en tant que modèle unique pour la parole, les effets sonores et l'ambiance. L'annonce officielle est datée du 2026-07-20 ; la date du 22 juillet correspond donc à l'apparition dans le flux et non à l'annonce primaire.

2026-07-20 — ByteDance a présenté le modèle comme un générateur complet de scènes sonores. La durée des silences de la parole est configurable jusqu'à 100 ms. Un seul passage peut produire jusqu'à deux minutes d'audio, avec possibilité de continuation.

## Mode d'emploi {#how-to-use-this}

Nous pouvons évaluer Seed Audio 1.0 via Seed et BytePlus Voice à la date du 2026-07-22. Vérifiez l'éligibilité à l'activation, la disponibilité et les capacités avant de vous appuyer dessus.

1. Activez Seed Audio dans BytePlus via la console et créez un projet.
  — <https://console.byteplus.com/voice/new/setting/activate?projectName=default>
2. Décrivez la scène en un seul prompt : personnages, répliques, émotion, environnement et sons clés. Définissez les points d'entrée des répliques si nécessaire.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
3. Pour les appels programmatiques, transmettez le prompt requis, nommez les références audio @Audio1 à @Audio3 et enregistrez l'URL du résultat.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Bonnes pratiques {#best-practices}

- N'utilisez que des références de voix autorisées. La documentation officielle limite explicitement le clonage vocal aux échantillons autorisés.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
- Ne bloquez pas l'application en attendant les requêtes asynchrones. Interrogez la file d'attente ou utilisez un webhook.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>
- Conservez la clé d'API côté serveur, et non dans le navigateur ou l'application cliente.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Remplacé par ceci {#superseded-by-this}

- 2026-07-20 : les scènes audio ne nécessitent plus d'assembler la parole, les effets et l'ambiance sous forme de clips isolés. Seed Audio 1.0 les traite dans un seul prompt de scène, mais les résultats et les droits sur les voix sources doivent toujours être vérifiés.

## Points inconnus {#still-unknown}

- La page produit officielle n'a fourni aucune spécification technique lors de la vérification, et la console BytePlus nécessite un accès interactif. Les tarifs actuels, les régions disponibles et le contrat exact de l'API BytePlus restent non confirmés.
- L'entrée est datée du 2026-07-22, alors que le matériel primaire de ByteDance est daté du 2026-07-20. L'écart de deux jours n'est pas expliqué.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://seed.bytedance.com/en/seedaudio1_0 | ByteDance Seed — page produit Seed Audio 1.0 | 2026-09-05 |
| https://console.byteplus.com/voice/new/setting/activate?projectName=default | BytePlus Voice — activation de Seed Audio | 2026-09-05 |
| https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model | From Speech to Audio Creation | Introducing the Seed Audio 1.0 Audio Creation Model | 2026-09-05 |
| https://fal.ai/models/bytedance/seed-audio-1.0/api | Seed Audio 1.0 Text to Audio API Docs | fal | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:bytedance-seed-audio-1-0`, fil `seed-audio`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Note pratique :** Au 2026-07-22, les praticiens peuvent considérer Seed Audio 1.0 comme une voie produit officielle à évaluer via Seed et BytePlus Voice, en vérifiant l'éligibilité à l'activation, la disponibilité et les capacités avant de s'y fier.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
