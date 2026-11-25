---
title: "Seoul World Model — Publication du projet"
category: projects
date: 2026-03-17
tags: [project, public-project-release, seoul-world-model]
aliases: ["Seoul World Model"]
level: 2
source_sha256: d50b3371a7fdeb72425cefacfce1bb8b4903e1112f86966eeabba123da7b9747
translation: machine
translated_at: '2026-10-24'
---
# Seoul World Model — Publication du projet {#seoul-world-model-public-project-release}

**Ligne de développement :** `project:seoul-world-model` · fil `public-project-release`  
**Dernier événement :** 2026-03-17 · 1 événement daté depuis le 2026-03-17 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Seoul World Model (SWM) est un modèle de monde de recherche. Il génère une vidéo de parcours à partir de coordonnées, de trajectoires de caméra et de scripts textuels, en récupérant des images de rue de Séoul depuis un index spatial.

- Le conditionnement par récupération (retrieval-augmented) préserve la géométrie des lieux et l'apparence visuelle.
- Le mouvement de caméra libre permet des trajectoires arbitraires et des modifications textuelles de la scène.
- Virtual Lookahead Sink réancre la génération vidéo sur les prochains points de passage du parcours.

Au 2026-09-05, les poids, le code d'inférence, les données synthétiques et le code d'interpolation n'ont pas encore été publiés ; nous ne pouvons donc pas le déployer.

## Ligne de développement {#development-line}

- **2026-03-17 — Enregistrement de la publication du projet Seoul World Model et des références de code.** Le 2026-03-17, le projet a publié des liens vers un site web public de présentation et vers un dépôt GitHub, établissant ainsi sa page de présentation officielle et son dépôt source.

## Ce qui a changé {#what-changed}

2026-03-17 — Seoul World Model a été lancé en tant que projet officiel « Grounding World Simulation Models in a Real-World Metropolis ». Le dépôt a annoncé la publication future des poids, du code d'inférence, des données synthétiques et des outils de préparation des vidéos d'entraînement.

Complément à l'événement du 2026-03-17 : la prépublication du 2026-03-16 désigne le système sous le nom de Seoul World Model (SWM) et le décrit comme un fine-tuning d'un modèle de monde vidéo pré-entraîné. Elle précise des données d'entraînement comprenant 440 000 images de rue de Séoul, des vidéos de conduite réelles et des données urbaines synthétiques.
  — <https://arxiv.org/abs/2603.15583>

Nouvel événement du 2026-03-16 : les auteurs ont publié la prépublication intitulée Grounding World Simulation Models in a Real-World Metropolis. L'article définit la méthode centrale : la récupération géoréférencée, l'appariement inter-temporel, les trajectoires synthétiques et Virtual Lookahead Sink.
  — <https://arxiv.org/abs/2603.15583>

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-17, utilisez le site web du projet Seoul World Model et le dépôt GitHub associé pour évaluer le projet, plutôt que des republications non vérifiées.

1. Consultez le dépôt officiel avant de planifier vos expériences : il ne fournit actuellement ni téléchargement de modèles ni instructions d'inférence.
  — <https://github.com/naver-ai/seoul-world-model>
2. Utilisez la page du projet et l'article comme spécifications de reproduction de recherche : les entrées du système sont la position géographique initiale, la trajectoire de caméra, le prompt textuel et les références locales d'images de rue.
  — <https://seoul-world-model.github.io/>
3. Ne revendiquez ni reproductibilité ni maturité pour la production tant que les auteurs n'ont pas publié les poids, le code d'inférence et les données.
  — <https://github.com/naver-ai/seoul-world-model>

## Bonnes pratiques {#best-practices}

- Mesurez l'ancrage géographique séparément du réalisme visuel : dans les ablations, moins d'images de référence a réduit le mPSNR alors que FID et FVD ne montraient pas de dégradation nette.
  — <https://arxiv.org/abs/2603.15583>
- Pour les longs parcours, récupérez des références en avant le long de la trajectoire plutôt que de vous fier uniquement à l'image initiale : c'est la méthode Virtual Lookahead Sink décrite dans l'article.
  — <https://arxiv.org/abs/2603.15583>
- Ne considérez pas une publication annoncée comme un outil disponible : le dépôt indique toujours que les poids et le code arriveront plus tard.
  — <https://github.com/naver-ai/seoul-world-model>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- Le dépôt officiel ne contient qu'un README et aucune GitHub Releases. Les auteurs n'ont pas annoncé de dates de publication pour les poids, le code d'inférence, les données synthétiques ou le code d'interpolation.
- Les chiffres des jeux de données divergent selon les sources. La page du projet cite 1,2 million de panoramas et 10 000 vidéos synthétiques, tandis que l'article précise 440 000 images de rue pour le fine-tuning. Les auteurs n'ont pas publié le jeu de données préparé ni les configurations d'entraînement exactes.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://seoul-world-model.github.io/ | Seoul World Model: Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model | naver-ai/seoul-world-model | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model/releases | Releases · naver-ai/seoul-world-model | 2026-09-05 |
| https://arxiv.org/abs/2603.15583 | Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:seoul-world-model`, fil `public-project-release`, 1 événement daté du 2026-03-17 → 2026-03-17.
- **Note pratique :** À partir du 2026-03-17, les praticiens devraient utiliser le site web du projet Seoul World Model ainsi que le dépôt GitHub associé comme point de départ pour évaluer et obtenir le projet, plutôt que de s'appuyer sur une republication non vérifiée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
