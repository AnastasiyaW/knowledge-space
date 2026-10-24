---
title: "GUSH3R"
category: projects
date: 2026-07-08
tags: [gush3r, gush3r-development, project]
aliases: ["GUSH3R"]
level: 2
source_sha256: b46195a6b42b6ef02ed50225ecf45f67a5d7e611eb4b4cb64d2c35bc33c592c0
translation: machine
translated_at: '2026-10-24'
---
# GUSH3R {#gush3r}

**Ligne de développement :** `project:gush3r` · fil `gush3r-development`  
**Dernier événement :** 2026-07-08 · 1 daté depuis le 2026-07-08 · **Recherché le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

GUSH3R est un code de recherche dédié au rendu en nouveaux points de vue de personnes en mouvement dans une scène, à partir d'une vidéo monoculaire. Il remplace un pipeline distinct combinant AnySplat pour l'arrière-plan et LHM pour les humains.

- Gaussiennes de scène statique : reconstruit l'arrière-plan.
- Gaussiennes humaines dynamiques : reconstruit les personnes en mouvement.
- Rendu partagé dans l'espace métrique : unifie la géométrie de l'arrière-plan et celle des humains.
- Traitement causal des images : traite les images de façon causale et peut utiliser des mises à jour récurrentes TTT3R.

Le point de contrôle fusionné téléchargeable pèse 4,87 Go, et l'inférence nécessite en outre des ressources SMPL/SMPL-X sous licence distincte.

Nous pouvons l'utiliser pour la reproduction de travaux de recherche et pour des expériences vidéo contrôlées. Ce n'est pas un pipeline de capture robuste pour la production, car les erreurs de pose, de caméra, de détection et d'identités occultées se propagent au résultat.

## Ligne de développement {#development-line}

- **2026-07-08 — Ressources publiques du projet GUSH3R liées.** Le 2026-07-08, la ligne de développement de GUSH3R a été associée à une page de projet publique, à un dépôt de code source et à une ressource Hugging Face. Ces liens donnent un accès public au projet, sans établir d'autres détails techniques.

## Ce qui a changé {#what-changed}

2026-07-08 — La première version publique de recherche de GUSH3R associe du code, un point de contrôle d'inférence fusionné `gush3r.pth` et une page de projet. L'arXiv v1 associé, soumis le 2026-07-06, désigne la méthode sous le nom de Gaussian-Unified Scene Human 3D Reconstruction. La version ajoute une représentation 3D à base de gaussiennes, en passe unique et en flux, pour les scènes statiques et les humains dynamiques. Elle annonce 1,70 FPS sur son benchmark mono-humain et 1,45 FPS sur son benchmark multi-humains BEDLAM.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-08, nous pouvons évaluer GUSH3R à travers la page de projet, le dépôt source et la ressource Hugging Face liés. Leur contenu n'a pas été analysé dans le cadre de cette revue.

1. Cloner le dépôt, créer l'environnement Python 3.10 recommandé, installer PyTorch pour CUDA 12.1, les dépendances, PyTorch3D et le rastériseur de gaussiennes.
  — <https://github.com/abkeito/GUSH3R>
2. Télécharger `checkpoints/gush3r.pth` depuis le dépôt du modèle, obtenir les ressources SMPL et SMPL-X sous licence, puis exécuter l'assistant fourni pour les modèles de corps.
  — <https://github.com/abkeito/GUSH3R>
3. Exécuter `infer.py` sur une vidéo monoculaire ; commencer avec `--max_frames 3`, puis inspecter `outputs/<name>/render.mp4`.
  — <https://github.com/abkeito/GUSH3R>

## Bonnes pratiques {#best-practices}

- Exécuter le test de fumée sur trois images avant une séquence complète, et utiliser `--subsample` pour réduire la charge de la séquence pendant le diagnostic.
  — <https://github.com/abkeito/GUSH3R>
- Examiner manuellement les sorties en cas d'association d'identités, d'occlusion sévère entre personnes, de flou de mouvement, de changements de pose importants, de visages, de mains et de textures de vêtements.
  — <https://arxiv.org/html/2607.05243v1>
- Contrôler la complexité cumulée de l'arrière-plan avec `--bg_gaussian_max`, le seuil de masque et la taille des voxels, plutôt que de laisser la scène croître sans limite.
  — <https://github.com/abkeito/GUSH3R>

## Remplacé par cet élément {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Inconnues restantes {#still-unknown}

- Aucune version officielle ultérieure, reproduction de benchmark, exigence d'inférence propre à un matériel particulier ni politique de support en production maintenue n'a été trouvée dans les documents de première main examinés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://abkeito.github.io/gush3r-page/ | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://github.com/abkeito/GUSH3R | abkeito/GUSH3R | 2026-09-05 |
| https://huggingface.co/abkeito/GUSH3R/tree/main | fichiers du modèle abkeito/GUSH3R | 2026-09-05 |
| https://arxiv.org/abs/2607.05243 | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://arxiv.org/html/2607.05243v1 | article GUSH3R, version HTML | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:gush3r`, fil `gush3r-development`, 1 événement daté du 2026-07-08 au 2026-07-08.
- **Note pratique :** À partir du 2026-07-08, les praticiens peuvent utiliser la page de projet, le dépôt source et la ressource Hugging Face liés comme points d'entrée publics datés pour évaluer GUSH3R ; leur contenu n'a pas été analysé dans cette revue.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
