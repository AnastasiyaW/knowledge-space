---
title: "IGGT4D"
category: projects
date: 2026-07-22
tags: [iggt4d, project]
aliases: ["IGGT4D"]
level: 2
source_sha256: 13e8a151b22e2973817a863f35541c025f4cd630ead0ca6475126f96d49a7851
translation: machine
translated_at: '2026-10-24'
---
# IGGT4D {#iggt4d}

**Ligne de développement :** `project:iggt4d` · fil `iggt4d`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

IGGT4D traite séquentiellement les images d'une vidéo pour prédire conjointement la caméra, la géométrie, les identités persistantes des objets et les masques d'instances.

- Reconstruction 4D en flux continu
- Estimation de pose
- Suivi d'objets
- Segmentation à vocabulaire ouvert

Le point de contrôle de 1B de paramètres exige d'accepter les conditions d'accès sur Hugging Face ; le jeu de données, le benchmark, ainsi que le code d'entraînement et d'évaluation ne sont pas encore publiés.
Il convient à des expériences d'inférence sur des séquences d'images personnalisées, mais pas à un entraînement ou à un benchmarking reproductibles.

## Ligne de développement {#development-line}

- **2026-07-22 — Le site GitHub Pages d'IGGT4D a été lié.** Modèle causal en flux continu qui unifie la géométrie de la scène et les identités persistantes des objets.

## Ce qui a changé {#what-changed}

2026-07-22 — IGGT4D a été présenté comme *Streaming 4D Instance-Grounded Geometry Transformer* : un modèle causal en flux continu qui unifie la géométrie de la scène et les identités persistantes des objets.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-22, les praticiens devraient considérer le site GitHub Pages d'IGGT4D mentionné ici comme un point de référence du projet, tout en vérifiant ses indications spécifiques ou son statut de publication avant de s'y fier.

1. Clonez le dépôt officiel et créez un environnement Conda avec Python 3.10.
  — <https://github.com/HorizonRobotics/IGGT4D>
2. Installez PyTorch ; le README donne l'exemple de PyTorch 2.8.0 avec CUDA 12.8, puis installez le paquet avec `pip install -e .`.
  — <https://github.com/HorizonRobotics/IGGT4D>
3. Acceptez les conditions d'accès au point de contrôle sur Hugging Face, téléchargez-le et enregistrez-le sous `checkpoints/model.safetensors`.
  — <https://huggingface.co/HorizonRobotics/IGGT4D>
4. Exécutez `python streaming_infer.py` pour la démonstration, ou passez `--image-dir` et `--output-dir` pour une séquence personnalisée d'images RGB.
  — <https://github.com/HorizonRobotics/IGGT4D>
5. Si nécessaire, activez `--camera` pour fournir des paramètres de caméra externes, et enregistrez les résultats avec `--save-npy` ou `--save-ply`.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Bonnes pratiques {#best-practices}

- Conservez le mode en flux continu par défaut pour les longues séquences ; `--mode full` correspond à la variante hors ligne à attention complète.
  — <https://github.com/HorizonRobotics/IGGT4D>
- Ne prévoyez pas d'entraînement, d'évaluation ou de comparaison sur le benchmark officiel avant sa publication : le dépôt indique ces éléments comme des artefacts en attente.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Pour l'événement du 2026-07-22, la source principale sur arXiv indique que la soumission de l'article date du 2026-07-21 à 16 h 00 min 01 s UTC ; cela confirme le titre, les dix auteurs et l'échelle d'InsScene4D-147K, mais ne fournit pas de publication distincte datée du 2026-07-22.
- La date exacte à laquelle le code d'inférence et le point de contrôle sont devenus disponibles n'est pas précisée dans les pages principales consultées ; nous ne l'avons donc pas ajoutée comme événement daté distinct.
- La page publique du projet indique que le jeu de données et le benchmark seront publiés ultérieurement, et le dépôt attend également le code d'entraînement et d'évaluation.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://iggt4d.github.io/ | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://arxiv.org/abs/2607.19228 | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://github.com/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D | 2026-09-05 |
| https://huggingface.co/HorizonRobotics/IGGT4D | Carte du modèle HorizonRobotics/IGGT4D | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:iggt4d`, fil `iggt4d`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Note pratique :** À partir du 2026-07-22, les praticiens devraient considérer le site GitHub Pages d'IGGT4D mentionné ici comme un point de référence du projet, tout en vérifiant ses indications spécifiques ou son statut de publication avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
