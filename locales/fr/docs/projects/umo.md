---
title: "UMO"
category: projects
date: 2026-03-19
tags: [project, umo]
aliases: ["UMO"]
level: 2
source_sha256: 18ed5bffa0287f6c6b69508c3c897bdf5ce9c44e6f09f2c28d8ceef2724ae0b7
translation: machine
translated_at: '2026-10-24'
---
# UMO {#umo}

**Ligne de développement :** `project:umo` · fil `umo`  
**Dernier événement :** 2026-03-19 · 1 événement daté depuis le 2026-03-19 · **Consulté le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

UMO est un cadre de recherche destiné aux équipes qui construisent des pipelines de mouvement humain en 3D. Il affine HY-Motion-Lite au lieu de livrer un outil de mouvement téléchargeable.

- Génération de mouvement : génère du mouvement humain conditionné par du texte.
- Contrôle du mouvement : complète, édite et contrôle un mouvement source au moyen des opérations de préservation, de génération et d'édition.
- Encodage des tâches : encode des trajectoires, des obstacles et des réactions entre deux personnes sous forme de tâches conditionnées par du texte.

## Ligne de développement {#development-line}

- **2026-03-19 — Le site public du projet UMO et le dépôt source ont été rendus accessibles.** Les auteurs ont présenté UMO comme une méthode unifiée de recherche sur le mouvement humain en 3D, accompagnée de démonstrations qualitatives et d'un dépôt lié. Ce dépôt n'est pas une implémentation exécutable à ce jour.

## Ce qui a changé {#what-changed}

2026-03-19 : Les auteurs ont présenté UMO comme une méthode unifiée de recherche sur le mouvement humain en 3D, accompagnée de démonstrations qualitatives et d'un dépôt lié. Ce dépôt n'est pas une implémentation exécutable à ce jour. 2026-08-17 : La liste préliminaire des articles acceptés à ECCV a ajouté une entrée de type poster pour UMO (#96, Poster Session 3). Cela a modifié le statut de publication, mais pas la disponibilité du code, des poids ou de l'API.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-19, partez du site projet UMO et du dépôt GitHub liés pour la documentation et l'inspection du code source.

1. Déterminez si la cible concerne le mouvement humain squelettique en 3D plutôt que la génération d'images ou de vidéos : les tâches évaluées incluent la génération texte-vers-mouvement, l'inpainting, l'édition par instruction, la géométrie sérialisée en texte et les réactions.
  — <https://arxiv.org/html/2603.15975v1>
2. Utilisez l'article et les démonstrations des auteurs pour faire correspondre une expérience de recherche à une description ou une modification en langage naturel, à une trajectoire structurée ou à une contrainte spatiale textuelle.
  — <https://oliver-cong02.github.io/UMO.github.io/>
3. Vérifiez le dépôt officiel pour le code et les artefacts de modèle avant de planifier l'implémentation. Aucune procédure officielle d'installation ni d'inférence n'est publiée actuellement.
  — <https://github.com/Oliver-Cong02/UMO>

## Bonnes pratiques {#best-practices}

- Ne remplacez pas HY-Motion non modifié par UMO pour les tâches d'inpainting ou de géométrie : l'article indique que la réutilisation en zero-shot ou sans entraînement échoue nettement.
  — <https://arxiv.org/html/2603.15975v1>
- Considérez les paramètres d'étude mentionnés dans l'article (entraînement sur 4×B200, 100k pas, solveur d'Euler à 50 pas et CFG 2.0) comme des réglages expérimentaux, et non comme une configuration minimale publiée.
  — <https://arxiv.org/html/2603.15975v1>
- Vérifiez le titre de l'article et le dépôt lié aux auteurs avant d'agir sur le nom UMO. ByteDance utilise le même nom pour un projet distinct de personnalisation d'images.
  — <https://github.com/bytedance/UMO>

## Remplacé par cette entrée {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Aucun journal des modifications officiel ni instantané immuable n'établit l'action de lancement exacte du 2026-03-19. Cette date est donc considérée comme la fenêtre de publication du projet et du dépôt, et non comme une date prouvée de publication du code ou du modèle.
- Les sources officielles ne fournissent ni point de contrôle, ni licence, ni instructions d'installation, ni CLI/API, ni contrat de fichiers d'entrée, ni configuration matérielle minimale pour UMO.
- Le nom générique UMO est aussi utilisé par un projet ByteDance sans rapport de personnalisation d'images. Les noms d'auteurs, le titre de l'article et le dépôt Oliver-Cong02 identifient ce travail comme le projet de mouvement humain.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2603.15975 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — fiche arXiv v1 | 2026-09-06 |
| https://arxiv.org/html/2603.15975v1 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — version HTML complète de l'article | 2026-09-06 |
| https://oliver-cong02.github.io/UMO.github.io/ | UMO — page projet des auteurs et démonstrations qualitatives | 2026-09-06 |
| https://github.com/Oliver-Cong02/UMO | Oliver-Cong02/UMO — page d'accueil officielle du dépôt | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026/AcceptedPapers | Liste préliminaire des articles acceptés à ECCV 2026 | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026 | Annonces de la conférence ECCV 2026 | 2026-09-06 |
| https://github.com/bytedance/UMO | bytedance/UMO — projet sans rapport de personnalisation d'images portant le même nom | 2026-09-06 |

## Briefing agent {#agent-brief}

- **Sujet :** `project:umo`, fil `umo`, 1 événement daté du 2026-03-19 au 2026-03-19.
- **Note pratique :** Au 2026-03-19, les praticiens doivent utiliser le site projet UMO et le dépôt GitHub liés comme points de départ pour la documentation et l'inspection du code source.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
