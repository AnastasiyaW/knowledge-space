---
title: "StreamingT2V"
category: projects
date: 2024-04-08
tags: [project, streamingt2v]
aliases: ["StreamingT2V"]
level: 2
source_sha256: c2e1cb1ce78d5477dbccdcfe5da94306b63da449913cd41c264aaead7187ee6b
translation: machine
translated_at: '2026-10-24'
---
# StreamingT2V {#streamingt2v}

**Ligne de développement :** `project:streamingt2v` · fil `streamingt2v`  
**Dernier événement :** 2024-04-08 · 1 événement daté depuis le 2024-04-08 · **Consulté :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

StreamingT2V est une méthode autorégressive de génération de vidéos longues, destinée aux chercheurs et aux praticiens disposant de GPU.

- CAM conserve le contexte à court terme des segments.
- APM préserve l'apparence de la scène.
- Le mélange randomisé affine les segments qui se chevauchent.

Le dépôt exécute une inférence image-vers-vidéo de 200 images avec 60 Go de VRAM par défaut, ou 24 Go en mode plus lent et optimisé pour la mémoire. L'Space hébergé signale actuellement une erreur d'exécution. Utilisez le dépôt local pour la recherche et les expérimentations image-vers-vidéo non commerciales, et non la démo défectueuse ni un service T2V de production actuel.

## Ligne de développement {#development-line}

- **2024-04-08 — Les supports du projet StreamingT2V ont été rendus publics.** Le 2024-04-08, StreamingT2V a publié un site de projet, un dépôt source public et un Space Hugging Face afin de fournir des supports de recherche, du code d'implémentation et un point d'entrée interactif.

## Ce qui a changé {#what-changed}

- 2024-04-08 — Le projet a été publiquement présenté sous le nom StreamingT2V, une méthode autorégressive visant à étendre la génération texte-vers-vidéo grâce à une mémoire par segments et à un affinage.
- 2024-06-30 — Une référence ultérieure a été enregistrée, mais aucune version technique ou modification de modèle accessible de manière indépendante ne peut être rattachée à cette date.
- 2024-08-30 — Le code et les poids du modèle StreamingSVD ont été publiés, rendant disponible une implémentation image-vers-vidéo fondée sur SVD.
- 2024-11-28 — Une version optimisée pour la mémoire a réduit l'exigence documentée de 60 Go à 24 Go de VRAM pour 200 images, avec une vitesse inférieure d'environ 50 %.
- 2025-02-26 — Le travail a été accepté à CVPR 2025.

## Mode d'emploi {#how-to-use-this}

Nous pouvons évaluer le projet à partir de son site, de son dépôt source et de son Space Hugging Face depuis le 2024-04-08. La référence du 2024-06-30 ne suffit pas, à elle seule, à établir un changement supplémentaire dans le flux de travail.

1. Clonez le dépôt, créez un environnement Python 3.9 avec CUDA 11.8 ou une version plus récente, installez ses dépendances et installez FFmpeg.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
2. Exécutez `python inference_i2v.py --input <image-ou-dossier> --output <dossier>` depuis `code` ; les entrées doivent être des images au format 16:9.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
3. Définissez `--num_frames` pour la longueur (200 par défaut), `--out_fps` pour le débit de sortie (24 par défaut), ou `--use_memopt` sur du matériel de 24 Go.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Bonnes pratiques {#best-practices}

- N'utilisez le chemin par défaut que si 60 Go de VRAM sont disponibles pour 200 images ; utilisez `--use_memopt` pour 24 Go de VRAM et prévoyez environ deux fois moins de vitesse.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- N'utilisez le mélange randomisé que si la pression mémoire l'exige ; les mainteneurs recommandent une taille de segment de 38 et un chevauchement de 12 lorsqu'il est activé.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- Considérez le code comme un usage de recherche non commercial, car les dépendances SVD, EMA-VFI et I2VGen-XL incluses imposent cette restriction.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Remplacé par ceci {#superseded-by-this}

- 2024-04-08 — La consigne d'utiliser la démo hébergée liée est obsolète en pratique : le Space Hugging Face PAIR signale actuellement une erreur d'exécution.
- 2024-04-08 — Décrire l'implémentation disponible comme une version générale de texte-vers-vidéo est dépassé : le README maintenu documente l'inférence image-vers-vidéo StreamingSVD et indique StreamingSVD texte-vers-vidéo comme projet futur.

## Toujours inconnu {#still-unknown}

- Les pages X et The source liées au 2024-06-30 n'étaient pas accessibles avec un texte exploitable ; le changement au niveau produit qu'elles revendiquent ne peut donc pas être vérifié.
- Aucune version maintenue plus récente n'a été trouvée après la mise à jour du dépôt de mars 2025 ; la disponibilité actuelle est déduite de l'état du dépôt et du Space, et non d'une exécution locale réussie et vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Picsart-AI-Research/StreamingT2V | Dépôt Picsart-AI-Research/StreamingT2V et README | 2026-09-05 |
| https://streamingt2v.github.io/ | Page de projet StreamingT2V | 2026-09-05 |
| https://arxiv.org/abs/2403.14773 | StreamingT2V: Consistent, Dynamic, and Extendable Long Video Generation from Text | 2026-09-05 |
| https://huggingface.co/spaces/PAIR/StreamingT2V | Space Hugging Face PAIR/StreamingT2V | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:streamingt2v`, fil `streamingt2v`, 1 événement daté du 2024-04-08 au 2024-04-08.
- **Note pratique :** À partir du 2024-04-08, les praticiens pouvaient utiliser le site du projet StreamingT2V, le dépôt source et le Space Hugging Face pour évaluer ou essayer le projet ; la référence du 2024-06-30 ne suffit pas, à elle seule, à établir un changement supplémentaire dans le flux de travail.
- **Confiance :** élevée. Les mentions « remplacé par » datées font autorité pour déterminer ce qui est obsolète.
