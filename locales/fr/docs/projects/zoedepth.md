---
title: "ZoeDepth"
category: projects
date: 2023-03-01
tags: [project, zoedepth, zoedepth-public-release]
aliases: ["ZoeDepth"]
level: 2
source_sha256: 3c9bfc5f8d8603bcc4ffdc447c9315dfa6f83bee40dea409655305e6c77920ef
translation: machine
translated_at: '2026-10-24'
---
# ZoeDepth {#zoedepth}

**Ligne de développement :** `project:zoedepth` · fil `zoedepth-public-release`  
**Dernier événement :** 2023-03-01 · 1 événement daté depuis le 2023-03-01 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

ZoeDepth est un modèle PyTorch d'estimation de profondeur monoculaire qui convertit une image RGB unique en une carte de profondeur absolue. ZoeD-M12-N, ZoeD-M12-K et ZoeD-M12-NK couvrent les modes intérieur, extérieur et mixte NYU+KITTI. L'architecture combine un pré-entraînement de profondeur relative sur 12 jeux de données avec un affinage métrique, et la version NK achemine automatiquement chaque domaine vers sa tête métrique correspondante. L'échelle métrique reste une estimation à partir d'une seule caméra, et Intel n'assure plus la maintenance du dépôt source. Pour des pipelines historiques reproductibles, utilisez le point de contrôle Transformers plutôt que d'attendre des correctifs dans le dépôt.

## Ligne de développement {#development-line}

- **2023-03-01 — Les ressources publiques du projet ZoeDepth sont devenues disponibles.** Le 2023-03-01, ZoeDepth était référencé via son dépôt GitHub, un notebook Google Colab et deux Hugging Face Spaces. Les liens datés montrent une étape d'accès public couvrant le code source, un notebook exécutable et des démonstrations hébergées. Ils n'établissent ni une version précise du modèle, ni un résultat de benchmark, ni une formulation de publication.

## Changements {#what-changed}

- 2023-03-01 — ZoeDepth est devenu disponible via le dépôt officiel, Colab et les démonstrations ; les poids publiés comprenaient ZoeD-M12-N, ZoeD-M12-K et ZoeD-M12-NK à deux têtes.
- 2023-07-09 — Aucune nouvelle version ou aucun nouveau modèle confirmé n'est apparu : le lien renvoie vers un article antérieur sur ZoeDepth.
- 2024-07-08 — Hugging Face Transformers a intégré ZoeDepth, offrant une voie standard de chargement et d'inférence via le pipeline depth-estimation.
- Statut actuel — Intel a déclaré le dépôt d'origine non pris en charge ; le point de contrôle Intel/zoedepth-nyu-kitti reste disponible dans Transformers.

## Mode d'emploi {#how-to-use-this}

À partir du 2023-03-01, les praticiens pouvaient évaluer ZoeDepth via son dépôt, son notebook Colab ou les démonstrations Hugging Face hébergées, avant de l'intégrer à leur propre flux de travail.

1. Installez des paquets PyTorch et Transformers compatibles, puis chargez Intel/zoedepth-nyu-kitti via pipeline("depth-estimation") pour une image unique.
  — <https://huggingface.co/Intel/zoedepth-nyu-kitti>
2. Pour la pile ZoeDepth d'origine, chargez ZoeD_N, ZoeD_K ou ZoeD_NK via torch.hub ; choisissez N pour l'intérieur NYU, K pour l'extérieur KITTI et NK pour les contextes mixtes.
  — <https://github.com/isl-org/ZoeDepth>
3. Passez une image RGB et enregistrez la carte de profondeur numérique ; n'utilisez pas les visualisations en couleurs comme données métriques brutes.
  — <https://github.com/isl-org/ZoeDepth>

## Bonnes pratiques {#best-practices}

- Utilisez le point de contrôle Transformers publié et fixez les versions des dépendances pour les nouveaux pipelines d'inférence : le dépôt source officiel ne reçoit plus de mises à jour.
  — <https://github.com/isl-org/ZoeDepth>
- Adaptez le modèle au domaine des données : N est entraîné sur NYU, K sur KITTI, et NK utilise deux têtes métriques pour les scènes intérieures et extérieures.
  — <https://arxiv.org/abs/2302.12288>
- Testez le chargement du modèle et lancez une inférence de test avant tout traitement par lots ; le dépôt fournit sanity_hub.py et sanity.py pour cette vérification.
  — <https://github.com/isl-org/ZoeDepth>

## Remplacé par {#superseded-by-this}

- 2023-02-27 : les instructions torch.hub d'origine ne constituent plus la seule voie de démarrage depuis l'intégration Transformers du 2024-07-08.
- Recommandation actuelle de ne pas considérer le dépôt source comme activement maintenu : Intel a explicitement annoncé la fin du développement, des correctifs et des nouvelles versions.

## Points restants inconnus {#still-unknown}

- Aucune version autonome n'est confirmée pour le 2023-07-09 : le lien disponible renvoie vers un article antérieur plutôt que vers une nouvelle version de ZoeDepth.
- La précision de la profondeur métrique sur des caméras personnalisées et des domaines hors NYU et KITTI nécessite une validation locale par vérité terrain.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/isl-org/ZoeDepth | isl-org/ZoeDepth — implémentation officielle et avis de maintenance | 2026-09-05 |
| https://github.com/isl-org/ZoeDepth/releases | Versions de ZoeDepth — v1.0 initiale | 2026-09-05 |
| https://arxiv.org/abs/2302.12288 | ZoeDepth: Zero-shot Transfer by Combining Relative and Metric Depth | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.48.0/model_doc/zoedepth | Hugging Face Transformers — documentation de ZoeDepth | 2026-09-05 |
| https://huggingface.co/Intel/zoedepth-nyu-kitti | Fiche modèle Intel/zoedepth-nyu-kitti | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:zoedepth`, fil `zoedepth-public-release`, 1 événement daté du 2023-03-01 au 2023-03-01.
- **Remarque pratique :** À partir du 2023-03-01, les praticiens pouvaient évaluer ZoeDepth via son dépôt, son notebook Colab ou les démonstrations Hugging Face hébergées, avant de l'intégrer à leur propre flux de travail.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
