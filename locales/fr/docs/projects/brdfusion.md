---
title: "BRDFusion"
category: projects
date: 2026-06-22
tags: [brdfusion, project]
aliases: ["BRDFusion"]
level: 2
source_sha256: 2a4b0c4597278df792d184bc9095cdb87748dc3d48b34fe2bd429ed7b2e6e003
translation: machine
translated_at: '2026-10-24'
---
# BRDFusion {#brdfusion}

**Ligne de développement :** `project:brdfusion` · fil `brdfusion`  
**Dernier événement :** 2026-06-22 · 1 événement daté depuis le 2026-06-22 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

BRDFusion est un pipeline de recherche ouvert qui transforme une vidéo urbaine en scène 3D Gaussian/PBR contrôlable. Il se rapproche davantage d'UrbanIR complété par un raffinement par diffusion que d'un générateur vidéo généraliste.

- Géométrie, matériaux et éclairage HDR : ils sont reconstruits à partir de la vidéo.
- Nouvelles vues et rééclairage : les deux sont rendus via PBR.
- Vidéo rendue : les images sont raffinées avec DiffusionRenderer.
- Modifications de scène : prise en charge de la simulation nocturne, des lumières locales, des phares et des modifications d'objets dynamiques.

Testé sous Ubuntu 22.04 avec une RTX A6000 ; Gen. Render peut dépasser 24 Go de VRAM.
Nous l'utilisons pour la recherche reproductible et la simulation de scènes de conduite sur une pile GPU Linux, et non comme un flux de travail léger reposant sur un seul modèle.

## Ligne de développement {#development-line}

- **2026-06-22 — Les ressources du projet BRDFusion ont été publiées.** Le 2026-06-22, BRDFusion a rendu accessibles sa page de projet, son dépôt source et sa collection de points de contrôle. Cette publication rend publics les artefacts d'implémentation et de modèle afin que les chercheurs puissent les trouver et les utiliser.

## Ce qui a changé {#what-changed}

- 2026-06-15 — La version v1 sur arXiv a présenté la méthode hybride physique-génération de BRDFusion pour le rendu inverse et direct de scènes urbaines.
- 2026-06-22 — La page de projet, le code public et les ressources de points de contrôle pré-entraînés ont été liés comme une version de recherche utilisable.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-22, nous pouvons évaluer ou reproduire le projet en partant de la page de projet BRDFusion, du dépôt source et de la collection de points de contrôle liés.

1. Vérifiez les prérequis documentés en matière de Linux, de compilateur, de CUDA et de GPU avant l'installation ; le projet utilise des environnements `brdfusion` et `cosmos-predict1` séparés.
  — <https://github.com/shigon255/BRDFusion>
2. Clonez le dépôt récursivement, construisez les deux environnements Conda, authentifiez-vous auprès de Hugging Face pour obtenir les poids de DiffusionRenderer, et fournissez l'asset SMPL requis.
  — <https://github.com/shigon255/BRDFusion>
3. Téléchargez une scène prétraitée fournie ainsi que le point de contrôle correspondant à une seule caméra, décompressez-les sous `ckpt/`, puis exécutez `bash scripts/stage_ckpt.sh`.
  — <https://github.com/shigon255/BRDFusion>
4. Exécutez `tools/run_pipeline.py` avec `--stage render` pour obtenir la sortie PBR ; utilisez la scène, la caméra, la plage d'images et la cible de rendu correspondantes pour l'option `--stage gen_render`.
  — <https://github.com/shigon255/BRDFusion>
5. Pour le rééclairage ou les modifications de scène, définissez les variables d'environnement ou les spécifications JSON documentées, puis invoquez `scripts/applications/render.sh` sur un point de contrôle préparé.
  — <https://github.com/shigon255/BRDFusion>

## Bonnes pratiques {#best-practices}

- Commencez par les données fournies et les points de contrôle pré-entraînés pour l'inférence ou l'évaluation, avant de tenter l'entraînement ou un nouveau prétraitement de scènes Waymo.
  — <https://github.com/shigon255/BRDFusion>
- Ne téléchargez que le sous-ensemble de scènes nécessaire à une expérience ; l'entraînement, le rendu et les métriques s'effectuent par scène.
  — <https://github.com/shigon255/BRDFusion>
- Gardez identiques le jeu de données, la scène ou le chemin, le réglage de caméra, la plage d'images et la cible de rendu entre le rendu et Gen. Render.
  — <https://github.com/shigon255/BRDFusion>
- Utilisez `--dry_run` pour inspecter les commandes sélectionnées et le manifeste du pipeline avant les opérations coûteuses ; les sorties des étapes existantes sont ignorées sauf si `--rerun_existing` est fourni.
  — <https://github.com/shigon255/BRDFusion>
- Utilisez `NO_PBR=1` et `PRINT_CMD=1` pour vérifier la géométrie, les trajectoires de caméra ou les commandes générées avant un rendu d'application complet.
  — <https://github.com/shigon255/BRDFusion>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- Nous n'avons trouvé aucune note de version primaire datée concernant une modification du code ou des points de contrôle le 2026-06-22 lui-même ; cette date établit l'événement de mise en ligne des liens, mais pas une version amont distincte.
- Le dépôt documente 35 commits sans historique de commits daté dans les ressources de recherche disponibles ; nous ne pouvons donc pas attribuer les capacités actuelles du README à un événement de développement postérieur au 22 juin.
- Le code source est sous licence MIT, tandis que la fiche des points de contrôle est étiquetée `License: other` ; les conditions d'utilisation des points de contrôle et des composants tiers inclus doivent être examinées avant tout déploiement commercial.
- Nous n'avons trouvé aucune reproduction indépendante, aucune mesure de performance à l'exécution, ni aucune preuve de déploiement en production.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://shigon255.github.io/brdfusion-page/ | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — page de projet | 2026-09-05 |
| https://github.com/shigon255/BRDFusion | shigon255/BRDFusion — dépôt source officiel et guide d'utilisation | 2026-09-05 |
| https://huggingface.co/Shigon/BRDFusion_checkpoints | Shigon/BRDFusion_checkpoints — points de contrôle pré-entraînés officiels | 2026-09-05 |
| https://arxiv.org/abs/2606.17049 | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — arXiv v1, soumis le 2026-06-15 | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:brdfusion`, fil `brdfusion`, 1 événement daté du 2026-06-22 au 2026-06-22.
- **Note pratique :** À partir du 2026-06-22, utilisez la page de projet BRDFusion, le dépôt source et la collection de points de contrôle liés pour évaluer ou reproduire le projet.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
