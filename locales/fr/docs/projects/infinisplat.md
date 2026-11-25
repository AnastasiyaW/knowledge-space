---
title: "InfiniSplat"
category: projects
date: 2026-08-07
tags: [infinisplat, infinisplat-public-availability, project]
aliases: ["InfiniSplat"]
level: 2
source_sha256: 41056d020f2d3d30c583657b9cf9c4c4180d109f639fc1e6f261b047a0fccba9
translation: machine
translated_at: '2026-10-24'
---
# InfiniSplat {#infinisplat}

**Ligne de développement :** `project:infinisplat` · fil `infinisplat-public-availability`  
**Dernier événement :** 2026-08-07 · 1 événement daté depuis le 2026-08-07 · **Recherche :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

InfiniSplat transforme une image RGB unique, ou une paire RGB-profondeur alignée, en une scène de Gaussiennes 3D pour le rendu de nouveaux points de vue. Il propose un mode RGB seul et un mode guidé par capteur de profondeur. Le flux de travail publié est fondé sur une seule image et non sur une reconstruction multi-vues. Utilisez-le pour obtenir rapidement une sortie de type photo spatiale, et non pour une capture de scène métrique à partir d'images quelconques.

## Ligne de développement {#development-line}

- **2026-08-07 — Les ressources publiques du projet InfiniSplat ont été documentées.** Le point de contrôle `infinisplat_rgb.ckpt` gère les entrées RGB seules, et `infinisplat_lidar.ckpt` gère une entrée RGB plus profondeur alignée. La méthode utilise des supports guidés par la géométrie et un décodage implicite de Gaussiennes conditionné par la requête.

## Ce qui a changé {#what-changed}

- 2026-08-03 — La v1 sur arXiv a présenté InfiniSplat : Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis.
- 2026-08-04 — La v2 sur arXiv a révisé l'article.
- 2026-08-07 — Le code publié et la démo ont mis à disposition deux points de contrôle complets : `infinisplat_rgb.ckpt` pour les entrées RGB seules et `infinisplat_lidar.ckpt` pour une entrée RGB plus profondeur alignée. La méthode utilise des supports guidés par la géométrie et un décodage implicite de Gaussiennes conditionné par la requête.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-07, nous pouvons utiliser la page du projet InfiniSplat, le dépôt et l'espace Hugging Face liés pour examiner l'implémentation et tester l'interface avant adoption.

1. Créez l'environnement Python 3.10 documenté, installez les dépendances PyTorch pour CUDA 12.8, puis téléchargez les deux points de contrôle.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md>
2. Lancez l'inférence RGB seule sur une image ou un répertoire avec `python -m src.demo.infer_batch_images --input PATH`.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/README.md>
3. Pour une reconstruction guidée par la profondeur, fournissez des fichiers RGB et de profondeur spatialement alignés, avec des noms de base identiques, et utilisez `--mode lidar`.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
4. Utilisez le PLY exporté comme artefact de référence. Vous pouvez éventuellement installer gsplat pour les rendus MP4 ou splat-transform pour les fichiers HTML interactifs.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Bonnes pratiques {#best-practices}

- Fournissez les paramètres intrinsèques de la caméra ou la distance focale lorsqu'ils sont connus. Sinon, le programme d'exécution revient à une distance focale fixe équivalente à 30 mm pour un capteur plein format.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Utilisez une profondeur alignée sur l'image RGB, exprimée en profondeur et non en disparité. Les valeurs décodées valides doivent être finies et strictement comprises entre 1 et 100.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Évitez `--overwrite` lorsque les sorties sont déjà valides. Le programme d'exécution ignore les artefacts terminés et ne crée que les artefacts demandés manquants.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Remplacé par {#superseded-by-this}

- 2026-08-04 — La v2 sur arXiv remplace la prépublication v1 du 2026-08-03.
- 2026-08-07 — Considérer InfiniSplat comme un flux de travail d'inférence publié à deux modes, et non seulement comme un article ou un aperçu.

## Inconnues restantes {#still-unknown}

- Aucune version InfiniSplat datée postérieure au 2026-08-07 n'a été vérifiée. La page du projet présente un aperçu non daté d'InfiniSplat V2 multi-vues ; nous ne le considérons pas comme un successeur publié.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://arxiv.org/abs/2608.02437 | InfiniSplat: Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis | 2026-09-05 |
| https://zju3dv.github.io/InfiniSplat/ | Page du projet InfiniSplat | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/README.md | README d'InfiniSplat | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md | Guide d'installation d'InfiniSplat | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md | Guide d'inférence d'InfiniSplat | 2026-09-05 |
| https://huggingface.co/spaces/PLUS-WAVE/InfiniSplat | Démo hébergée PLUS-WAVE InfiniSplat | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:infinisplat`, fil `infinisplat-public-availability`, 1 événement daté du 2026-08-07 au 2026-08-07.
- **Note pratique :** À partir du 2026-08-07, nous pouvons utiliser la page du projet InfiniSplat, le dépôt et l'espace Hugging Face liés pour examiner l'implémentation et tester l'interface avant adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
