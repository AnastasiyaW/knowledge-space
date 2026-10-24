---
title: "Holi-Spatial"
category: projects
date: 2026-03-10
tags: [holi-spatial, holi-spatial-development, project]
aliases: ["Holi-Spatial"]
level: 3
source_sha256: b36c0752eaf78d23aa6d7b41cf6ba46c010d363893a539a47c2ee666c29910b9
translation: machine
translated_at: '2026-10-24'
---
# Holi-Spatial {#holi-spatial}

**Ligne de développement :** `project:holi-spatial` · fil `holi-spatial-development`  
**Dernier événement :** 2026-03-10 · 1 événement daté depuis le 2026-03-10 · **Consulté le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

Holi-Spatial est un pipeline public de préparation de données destiné aux équipes de recherche qui ont besoin de 3D Gaussian Splatting, de masques, de boîtes 3D et de contrôle qualité spatial (QA) à partir de scènes ScanNet, ScanNet++ ou DL3DV.

- Profondeur et nuages de points : construit des cartes de profondeur et des nuages de points avec DA3, puis exécute PGSR/3DGS.
- Annotation et contrôle qualité des objets : segmente les objets avec SAM3 et un VLM, remonte les masques en 3D et génère des questions-réponses (QA).
- Export de jeux de données multimodaux : convertit la sortie en jeu de données SFT pour LLaMA-Factory.

12 000 scènes 3DGS optimisées et plus de 4 millions d'annotations spatiales sont mentionnées dans l'article ; le checkpoint disponible HoliSpatial-2M-QA-Qwen3-VL-8B est un modèle BF16 de 9 milliards de paramètres, d'une taille de 17,6 Go.

Il s'agit d'un pipeline hors ligne destiné à la curation et à l'entraînement, utilisant CUDA, des modèles externes et vos propres scènes, et non d'un service 3D interactif.

## Ligne de développement {#development-line}

- **2026-03-10 — Les ressources du projet Holi-Spatial ont été publiées.** Le 2026-03-10, Holi-Spatial a été relié à une page de projet publique, à un dépôt source et à une ressource Hugging Face. Il s'agit d'un point de repère important pour le développement public, bien que les éléments disponibles n'établissent pas le statut exact de publication ni les capacités de la ressource liée.

## Ce qui a changé {#what-changed}

- 2026-03-08 — Publication de l'arXiv v1 : décrit un pipeline automatisé en trois étapes et Holi-Spatial-4M.
- 2026-03-10 — Holi-Spatial a reçu une page de projet publique et un dépôt pour l'annotation spatiale de vidéos, annonçant plus de 13 000 scènes, plus de 1,3 million de QA et plus de 300 000 boîtes 3D.
- 2026-03-19 — La page officielle Hugging Face indique que le jeu de données ScanNetPP a été mis à jour.
- 2026-03-21 — La page officielle Hugging Face indique que le jeu de données ScanNet_v2 a été mis à jour.
- 2026-03-22 — La page officielle Hugging Face indique que HoliSpatial-QA-2M a été mis à jour.
- 2026-03-29 — La page officielle Hugging Face présente HoliSpatial-2M-QA-Qwen3-VL-8B comme un checkpoint 9B mis à jour.
- 2026-04-21 — La page officielle Hugging Face indique que HoliSpatial-3D-Grounding a été mis à jour.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-10, les praticiens devraient utiliser la page de projet, le dépôt et la ressource Hugging Face reliés comme point de départ pour évaluer Holi-Spatial, tout en vérifiant de manière indépendante l'artefact exact, la version et les instructions d'utilisation.

1. Créez un environnement Python compatible CUDA et installez les dépendances avec les deux sous-modules PGSR.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
2. Préparez une scène dans la structure attendue pour ScanNet, ScanNet++ ou DL3DV ; ajoutez la racine de covisibilité pour le QA.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
3. Exécutez DA3 sur une scène via SCENE_DIR d'abord ; vérifiez depth_da3 et pointcloud_da3.ply.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
4. Entraînez PGSR/3DGS, puis générez le maillage et les masques guidés par le maillage.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
5. Démarrez un endpoint vLLM compatible OpenAI, lancez l'annotation des objets et régions avec SAM3, post-traitez les AABB, générez le QA et convertissez-le en dataset.jsonl pour LLaMA-Factory.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>

## Bonnes pratiques {#best-practices}

- Commencez par une seule scène et vérifiez les artefacts intermédiaires : les scripts par lots considèrent une scène comme terminée si un JSON final ou un nuage de points entraîné existe déjà.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- Configurez explicitement CUDA, Depth Anything 3, les ressources SAM3 et un endpoint vLLM compatible OpenAI, plutôt que de vous fier à des dépendances implicites.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- Conservez la vérification par VLM pour les instances limites : le filtrage par confiance augmente la précision, mais peut écarter des objets complexes valides.
  — <https://arxiv.org/abs/2603.07660>
- Ne transférez pas de résultats non vérifiés à des vidéos présentant du flou de mouvement, une occlusion importante, peu de points de vue ou des objets dynamiques : les auteurs signalent ces points comme des limites du pipeline.
  — <https://arxiv.org/abs/2603.07660>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-10 — Les statuts « Data (coming soon) » et « Benchmark (coming soon) » de la page de projet ne reflètent plus la disponibilité : le dépôt indique la publication d'un sous-ensemble de données et d'un checkpoint, et l'organisation Hugging Face héberge désormais quatre jeux de données et un modèle. Cela ne prouve pas la disponibilité de l'intégralité de Holi-Spatial-4M.

## Points encore inconnus {#still-unknown}

- Les dates de mars et avril figurant sur la page de l'organisation Hugging Face sont des dates de dernière mise à jour et non des dates de première publication confirmées : les pages d'historique des commits étaient indisponibles.
- La page de projet indique toujours les données et le benchmark comme « coming soon », alors que le README et Hugging Face présentent des artefacts disponibles. Il reste incertain si cette mention concerne l'intégralité de Holi-Spatial-4M ou si elle est simplement obsolète.
- Le checkpoint ne dispose ni d'une fiche de modèle ni d'un fournisseur d'inférence hébergé ; le modèle exact de prompt, les entrées prises en charge et l'environnement d'exécution recommandé restent non confirmés.
- Ni le dépôt ni la page du modèle n'indiquent de licence explicite pour le code, les jeux de données ou les poids.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://visionary-laboratory.github.io/holi-spatial/ | Holi-Spatial | Holistic Spatial Intelligence | 2026-09-06 |
| https://github.com/Visionary-Laboratory/Holi-Spatial | GitHub - Visionary-Laboratory/Holi-Spatial: Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://arxiv.org/abs/2603.07660 | Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://huggingface.co/Holi-Spatial | Holi-Spatial (Visionary Laboratory) | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B/tree/main | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B at main | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-QA-2M | Holi-Spatial/HoliSpatial-QA-2M | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-3D-Grounding | Holi-Spatial/HoliSpatial-3D-Grounding | 2026-09-06 |

## Résumé pour l'agent {#agent-brief}

- **Sujet :** `project:holi-spatial`, fil `holi-spatial-development`, 1 événement daté du 2026-03-10 au 2026-03-10.
- **Note pratique :** À partir du 2026-03-10, les praticiens devraient utiliser la page de projet, le dépôt et la ressource Hugging Face reliés comme point de départ pour évaluer Holi-Spatial, tout en vérifiant de manière indépendante l'artefact exact, la version et les instructions d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
