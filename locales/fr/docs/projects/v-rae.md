---
title: "V-RAE"
category: projects
date: 2026-08-24
tags: [project, v-rae, v-rae-development, v_rae]
aliases: ["V-RAE"]
level: 2
source_sha256: e3e1d290506a725f34bd02117467adb62419500dd2a66b710c9bce7603808030
translation: machine
translated_at: '2026-10-24'
---
# V-RAE {#v-rae}

**Ligne de développement :** `project:v-rae` · fil `v-rae-development`  
**Dernier événement :** 2026-08-24 · 1 événement daté depuis le 2026-08-24 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

V-RAE est une base de code de recherche et un ensemble de points de contrôle pour la reconstruction et la génération de vidéos. Il associe des encodeurs DINOv3, SigLIP2, V-JEPA2.1 ou EUPE gelés à un regroupement temporel et à un décodeur vidéo.

- Reconstruction vidéo à partir de représentations gelées.
- Génération conditionnée par classe sur des benchmarks vidéo.
- Prédiction de trames futures sans mise à jour des poids de l'encodeur.

Les meilleurs résultats de génération rapportés sont 117,86 gFVD sur UCF101 et 19,16 sur Kinetics-600. Le code est orienté recherche et nécessite Linux, NVIDIA CUDA, FFmpeg, Python 3.10+ ainsi que les poids d'encodeur correspondants.

## Ligne de développement {#development-line}

- **2026-08-24 — Les ressources du projet V-RAE ont été liées.** Le 2026-08-24, le projet a publié des liens d'entrée vers son site web, son dépôt GitHub et sa page de modèle Hugging Face, sans détails de publication distincts ni capacités vérifiées.

## Changements {#what-changed}

- 2026-08-13 — L'article V-RAE a été soumis sur arXiv, définissant l'approche d'auto-encodeur de représentations et le diagnostic de cohérence temporelle tFVD.
- 2026-08-14 — L'implémentation officielle a commencé avec une première publication (release) sur GitHub.
- 2026-08-19 — Le dépôt a ajouté des manifestes de données, des résultats visuels et un correctif pour les configurations incohérentes.
- 2026-08-24 — Les points d'entrée publics couvraient la page du projet, l'implémentation officielle et le dépôt des points de contrôle ; aucune source de première main ne prouve une publication distincte de code ou de modèle à cette date.
- 2026-08-26 — Le dépôt a mis à jour les résultats visuels au format GIF.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-24, considérez le site web de V-RAE, le dépôt GitHub et la page de modèle Hugging Face liés comme des points de départ pour consulter la documentation du projet, le code source et la disponibilité des modèles ; les versions exactes et les conditions d'utilisation restent à vérifier.

1. Clonez l'implémentation, créez un environnement Python 3.10, installez FFmpeg et les dépendances de paquets épinglées.
  — <https://github.com/V-RAE/V-RAE>
2. Téléchargez le dépôt des points de contrôle V-RAE dans `ckpts`, puis téléchargez les poids des encodeurs gelés correspondant à la variante choisie.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
3. Placez les clips d'entrée dans `assets/sample1.mp4` à `assets/sample3.mp4`, puis exécutez `python sampling.py dino`, `siglip`, `vjepa` ou `eupe` ; comparez les résultats dans `outputs/<variant>/`.
  — <https://github.com/V-RAE/V-RAE>

## Bonnes pratiques {#best-practices}

- Associez chaque point de contrôle V-RAE à ses poids d'encodeur gelés correspondants ; les points de contrôle sont des fichiers PyTorch personnalisés destinés à la base de code officielle.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
- Utilisez Linux avec un GPU NVIDIA, un pilote compatible CUDA, FFmpeg et Python 3.10 ou plus récent ; vérifiez CUDA et TorchCodec avant l'inférence.
  — <https://github.com/V-RAE/V-RAE>
- Considérez les chiffres publiés comme des résultats de recherche propres à une tâche : rFVD mesure la reconstruction, gFVD la génération et tFVD la cohérence temporelle ; ne les comparez pas comme un score de qualité universel unique.
  — <https://github.com/V-RAE/V-RAE>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-19 — Les configurations initiales du dépôt ont été remplacées par le correctif documenté pour les configurations incohérentes.

## Toujours inconnu {#still-unknown}

- Aucun enregistrement de publication de première main daté n'existe pour le 2026-08-24 lui-même ; l'article lié et la publication initiale du dépôt sont antérieurs à cette date.
- Le hub de modèles ne présente pas de révision datée sur la page consultée, ce qui laisse non vérifiée la date de publication originale des points de contrôle.
- Aucun point d'accès d'inférence hébergé ni guide de déploiement en production n'existe ; la fiche du modèle indique qu'aucun Inference Provider ne le déploie.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/V-RAE/V-RAE | README de l'implémentation officielle V-RAE/V-RAE | 2026-09-05 |
| https://huggingface.co/Guomh0707/V-RAE-Models | Fiche du modèle Guomh0707/V-RAE-Models | 2026-09-05 |
| https://arxiv.org/abs/2608.13556 | V-RAE: Rethinking Video Latent Spaces for Generation | 2026-09-05 |
| https://github.com/V-RAE/V-RAE/commits/main/ | Historique des commits V-RAE/V-RAE | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:v-rae`, fil `v-rae-development`, 1 événement daté du 2026-08-24 au 2026-08-24.
- **Note pratique :** Au 2026-08-24, les praticiens doivent considérer le site web de V-RAE, le dépôt GitHub et la page de modèle Hugging Face liés comme points de départ pour vérifier la documentation du projet, le code source et la disponibilité des modèles ; les versions exactes et les conditions d'utilisation restent à vérifier.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
