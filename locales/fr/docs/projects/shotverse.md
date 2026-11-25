---
title: "ShotVerse"
category: projects
date: 2026-03-14
tags: [project, shotverse, shotverse-development]
aliases: ["ShotVerse"]
level: 2
source_sha256: 59a59037327e56418feeb432e0c84d81cc6c8db3eb43155fc5482b4146e11c33
translation: machine
translated_at: '2026-10-24'
---
# ShotVerse {#shotverse}

**Ligne de développement :** `project:shotverse` · fil `shotverse-development`  
**Dernier événement :** 2026-03-14 · 1 événement daté depuis le 2026-03-14 · **Recherche effectuée le :** 2026-09-06 · confiance : élevée

## Présentation {#what-it-is}

ShotVerse est un système de recherche destiné aux créateurs et aux chercheurs qui ont besoin de trajectoires de caméra explicites et cohérentes sur plusieurs plans.

- Le Planner transforme une description globale et des descriptions par plan en trajectoires de caméra.
- Le Controller génère une vidéo multi-plans à partir de texte et de trajectoires.

ShotVerse-Bench rapporte 20 500 clips et 12 millions d'images ; les expériences assemblent des scènes de 2 à 4 plans de 249 images chacun. Au 2026-09-06, il s'agit d'une spécification de méthode et d'un benchmark, et non d'un outil installable : le dépôt officiel indique encore que les poids, le code d'inférence, le jeu de données et l'entraînement sont des livraisons à venir.

## Ligne de développement {#development-line}

- **2026-03-14 — Des références publiques du projet ShotVerse ont été partagées.** Le 2026-03-14, ShotVerse a été référencé avec des liens vers son site web de projet, son dépôt GitHub et une destination Hugging Face. Ensemble, ces liens établissent un point de référence public daté pour le projet et ses ressources associées.

## Ce qui a changé {#what-changed}

2026-03-14 — ShotVerse a été présenté comme une méthode de recherche pour le contrôle explicite de la caméra dans la vidéo multi-plans. Les documents primaires datés ne confirment pas de version publique exploitable à cette date.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-14, utilisez le site web et le dépôt GitHub de ShotVerse comme points de départ pour les ressources publiques du projet. La destination Hugging Face indiquée nécessite une vérification séparée avant utilisation.

1. Lisez l'article actuel et associez votre tâche à son entrée : une description globale plus des descriptions par plan, et non un prompt texte unique.
  — <https://arxiv.org/abs/2603.11421>
2. Consultez la page du projet et les exemples Prompt Details pour évaluer les mouvements de caméra et la structure de montage.
  — <https://shotverse.github.io/>
3. Vérifiez le dépôt avant d'envisager une adoption : les pipelines officiels d'installation et d'inférence n'existent pas encore, les paramètres de l'article ne constituent donc pas une recette exécutable.
  — <https://github.com/Songlin1998/ShotVerse>

## Bonnes pratiques {#best-practices}

- Conservez l'entrée à deux niveaux pour la reproduction de la recherche : un contexte de scène global et une description distincte pour chaque plan, car le Planner attend cette structure.
  — <https://arxiv.org/html/2603.11421v1>
- Considérez les métriques, la pile Qwen3-VL-2B/HoloCine et l'entraînement sur 96 H20 comme une configuration expérimentale, et non comme un flux de travail utilisateur vérifié.
  — <https://arxiv.org/html/2603.11421v1>
- N'intégrez pas ShotVerse dans un pipeline de production avant l'arrivée des artefacts officiels : un dépôt public ne signifie pas qu'un modèle est disponible.
  — <https://github.com/Songlin1998/ShotVerse>

## Remplacé par {#superseded-by-this}

- 2026-08-24 — La version v2 sur arXiv remplace la v1 du 2026-03-12 comme version actuelle de l'article. Cela ne rétrodate pas le statut du 2026-03-14 et ne prouve pas la publication du code ou des poids.

## Points toujours inconnus {#still-unknown}

- Nous n'avons trouvé aucune preuve d'archive primaire attestant de l'existence du site ou du dépôt actuel au 2026-03-14.
- Nous n'avons trouvé aucune exécution indépendante reproductible, aucune licence de modèle, aucun point de contrôle, aucun jeu de données public ni aucune pratique utilisateur vérifiée.
- Les requêtes de recherche en chinois ont renvoyé des synthèses d'agrégateurs plutôt que de la documentation primaire ou des retours d'expérience.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (arXiv v1) | 2026-09-06 |
| https://arxiv.org/html/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (texte intégral arXiv v1) | 2026-09-06 |
| https://arxiv.org/abs/2603.11421 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (notice arXiv actuelle) | 2026-09-06 |
| https://shotverse.github.io/ | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation | 2026-09-06 |
| https://github.com/Songlin1998/ShotVerse | GitHub - Songlin1998/ShotVerse | 2026-09-06 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:shotverse`, fil `shotverse-development`, 1 événement daté du 2026-03-14 au 2026-03-14.
- **Note pratique :** Au 2026-03-14, considérez le site web de ShotVerse et le dépôt GitHub associé comme points de départ pour les ressources publiques du projet. La destination Hugging Face indiquée nécessite une vérification séparée avant utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
