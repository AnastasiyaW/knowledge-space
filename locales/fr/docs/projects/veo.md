---
title: "Veo"
category: projects
date: 2024-05-14
tags: [google_io_2024, project, veo, veo-development]
aliases: ["Veo", "Veo 3"]
level: 2
source_sha256: 42109440b97fafdd3513c5c6c01950d6bbb2c8606d29b991697ef965d0a65175
translation: machine
translated_at: '2026-10-24'
---
# Veo {#veo}

**Ligne de développement :** `project:veo` · fil `veo-development`  
**Dernier événement :** 2024-05-14 · 1 événement daté depuis le 2024-05-14 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Veo est la famille de modèles de génération vidéo de Google DeepMind, destinée aux cinéastes, aux créateurs et aux utilisateurs de l'API.

- Clips vidéo : génère des clips à partir de texte (text-to-video) et à partir d'image (image-to-video).
- Contrôles de cadre : prend en charge les images de référence, la génération à partir de la première et de la dernière image, ainsi que l'extension.
- Pistes audio : génère des dialogues, des effets sonores et des ambiances synchronisés.

## Ligne de développement {#development-line}

- **2024-05-14 — Présentation de Veo lors de Google I/O 2024.** Le 2024-05-14, Google a présenté Veo lors de Google I/O 2024. Cette date marque le début de la ligne de développement de Veo identifiée et constitue un élément important de son historique public.

## Évolutions {#what-changed}

- 2024-05-14 — Google a présenté Veo comme un modèle vidéo en 1080p, disponible uniquement pour certains créateurs sélectionnés, dans le cadre de la préversion privée VideoFX.
- 2025-05-20 — Veo 3 ajoute l'audio natif. Google a présenté Flow et rendu Veo 3 disponible dans Gemini, Flow et Vertex AI, selon des conditions d'accès annoncées.
- 2025-09-26 — Veo 3 a fait l'objet d'un rapport de recherche en zero-shot couvrant la perception visuelle, la manipulation, la modélisation physique et le raisonnement visuel simple. Il s'agissait d'une preuve de recherche, et non d'un nouveau point d'accès produit.
- 2025-10-15 — Veo 3.1 ajoute l'audio à Ingredients to Video, Frames to Video et Extend dans Flow, avec une meilleure adhérence des invites image-to-video.
- 2026-01-13 — Veo 3.1 Ingredients to Video ajoute la sortie native en 9:16 et les options 1080p/4K dans les flux de travail professionnels pris en charge.

## Mode d'emploi {#how-to-use-this}

À compter du 2024-05-14, les praticiens doivent considérer Veo comme un projet distinct de génération vidéo et suivre séparément ses versions ultérieures, ses changements d'accès et ses capacités de modèle, indépendamment des annonces générales de Google I/O.

1. Créez un client de l'API Gemini, soumettez une requête de génération avec le nom d'un modèle Veo, interrogez l'opération de longue durée, puis téléchargez la vidéo générée.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
2. Rédigez l'invite en précisant le sujet, l'action, le style, la caméra, la composition, la mise au point et l'ambiance. Incluez les dialogues entre guillemets ou des indications sonores explicites lorsque l'audio est important.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
3. Fournissez une image initiale, jusqu'à trois images de référence, ou une première et une dernière image pour un travail image-to-video contrôlé. N'utilisez l'extension que pour un clip généré par Veo.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
4. Téléchargez le résultat rapidement : Google indique une durée de conservation sur ses serveurs de deux jours.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>

## Bonnes pratiques {#best-practices}

- Précisez la position ou le mouvement de la caméra, le cadrage, l'objectif ou la mise au point et l'ambiance, plutôt que de vous appuyer uniquement sur des étiquettes de style.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Utilisez des images de référence pour assurer la cohérence d'un personnage, d'un produit ou d'une scène ; la limite documentée est de trois ressources.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Prévoyez les plans en haute résolution, avec image de référence ou extension, comme des unités de huit secondes ; l'extension est limitée à 720p.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Formulez explicitement les exigences relatives à la parole et aux sons, puis vérifiez les résultats. Google indique que des limitations subsistent quant à un audio parlé naturel et cohérent.
  — <https://deepmind.google/models/veo/>

## Remplacé par cette entrée {#superseded-by-this}

- 2024-05-14 — Veo ne peut plus être décrit avec exactitude comme réservé à la préversion privée VideoFX ; la documentation actuelle l'expose via l'API Gemini et plusieurs produits Google.
- 2024-05-14 — Le positionnement initial « au-delà d'une minute » ne correspond pas à l'unité d'API actuellement documentée, à savoir un clip généré de 4, 6 ou 8 secondes.

## Points encore inconnus {#still-unknown}

- L'élément du 2024-05-14 ne comportait aucune URL ; son rattachement repose donc sur l'annonce Veo de Google faite à la même date, et non sur le document d'origine lié.
- L'élément du 2025-09-26 renvoie vers un projet de recherche sur Veo 3, et non vers une page de sortie de produit. Sa page de publication officielle est datée du 2025-09-24 ; le lien exact entre l'élément du 26 septembre et une révision particulière d'un article n'est pas précisé.
- Le résultat de recherche en zero-shot ne doit pas être considéré comme un flux de travail de production pris en charge, ni comme une preuve que Veo expose des API de segmentation, d'édition ou de raisonnement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.google/innovation-and-ai/products/google-generative-ai-veo-imagen-3/ | New generative media models and tools, built with and for creators | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/ | Fuel your creativity with new generative media models and tools | 2026-09-05 |
| https://deepmind.google/research/publications/203190/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://video-zero-shot.github.io/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/veo-updates-flow/ | Introducing Veo 3.1 and advanced capabilities in Flow | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ | Veo 3.1 Ingredients to Video: More consistency, creativity and control | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/veo?hl=en | Generate videos with Veo 3.1 in Gemini API | 2026-09-05 |
| https://deepmind.google/models/veo/ | Veo 3.1 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:veo`, fil `veo-development`, 1 événement daté, du 2024-05-14 au 2024-05-14.
- **Note pratique :** À compter du 2024-05-14, les praticiens doivent considérer Veo comme un projet distinct de génération vidéo et suivre séparément ses versions ultérieures, ses changements d'accès et ses capacités de modèle, indépendamment des annonces générales de Google I/O.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
