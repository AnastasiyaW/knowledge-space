---
title: "Marionette — Publication publique du projet"
category: projects
date: 2026-08-18
tags: [alayalab/marionette, marionette, project, public-project-release]
aliases: ["Marionette"]
level: 2
source_sha256: 7443d47d719be856ace9191e4f22c7ee834104de7222aa3a0c872346f19f68ac
translation: machine
translated_at: '2026-10-24'
---
# Marionette — Publication publique du projet {#marionette-public-project-release}

**Ligne de développement :** `project:marionette` · fil `public-project-release`  
**Dernier événement :** 2026-08-18 · 1 événement daté depuis le 2026-08-18 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Marionette : pipeline d'Alaya Lab destiné aux chercheurs sur les world models. ActionGPT et PoseGPT prédisent un état articulé de dimension 276, un bridge déterministe rend la géométrie, et Wan2.2-Fun-5B-Control, fine-tuné, génère la vidéo RGB.

- contrôle : substitution du token d'action ou de la racine de trajectoire au niveau de l'état ;
- exécution : deux environnements Python distincts pour le stage 1 et le stage 2 ;
- limites : une seule espèce de monstre, des scans de lieux précis et une licence de recherche non commerciale.

Ordre de grandeur : le checkpoint d'observation publié pèse 10,0 Go, et le modèle de base tiers nécessaire fait environ 23 Go.

Verdict : il s'agit d'un pipeline de recherche reproductible, et non d'un moteur de jeu universel ni d'un service de génération vidéo prêt à l'emploi.

## Ligne de développement {#development-line}

- **2026-08-18 — Les ressources publiques du projet Marionette ont été liées.** Le 2026-08-18, la ligne de développement de Marionette était représentée par des liens vers sa page de projet, son dépôt source, sa page de modèle sur Hugging Face et l'espace de world model hébergé. Il s'agit d'une étape publique importante, car elle relie la documentation, le code, la distribution des modèles et une démonstration exécutable.

## Évolutions {#what-changed}

2026-08-13 — publication de la page de projet, du code d'inférence, des ressources d'exécution et des démonstrations de contrôlabilité ; le pipeline complet en trois étapes est devenu disponible pour une exécution locale. 2026-08-14 — publication sur arXiv de l'article « Marionette: Predicting World States, Rendering Geometry, Painting Appearance » ; il y présente l'architecture et les résultats annoncés pour le contrôle de l'état. 2026-08-18 — les documents du projet, le dépôt, les poids Hugging Face et la démonstration ont été regroupés dans une même publication ; la fiche des poids précise le nom exact du modèle de base, les dimensions des checkpoints, les paramètres d'inférence et les limites.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-18, les praticiens doivent utiliser la page de projet, le dépôt, la page de modèle Hugging Face et l'espace hébergé liés comme point de départ pour évaluer Marionette. Les capacités, la licence et les étapes de reproduction nécessitent tout de même une recherche sur les sources avant toute adoption.

1. Cloner le dépôt, télécharger les poids de Marionette ainsi que le modèle de base tiers, puis lancer `bash run_demo.sh`.
  — <https://huggingface.co/AlayaLab/Marionette>
2. Pour une exécution séparée, créer un environnement de rendu pour le stage 1 et un environnement Wan pour le stage 2 ; lancer `run_stage1_render.sh`, puis `run_stage2_wan.sh`.
  — <https://github.com/AlayaLab/Marionette>
3. Conserver le checkpoint d'observation et son prompt en une paire indissociable ; les paramètres publiés sont 704×1280, 40 steps, guidance 6.0, des chunks de 81 frames et 30 fps.
  — <https://huggingface.co/AlayaLab/Marionette>

## Bonnes pratiques {#best-practices}

- Ne pas regrouper les stages 1 et 2 dans un même environnement : le rendu nécessite Python 3.12 et EGL, tandis que l'étape de diffusion requiert torch, diffusers et decord.
  — <https://github.com/AlayaLab/Marionette>
- Fixer `TORCH_SEED` pour garantir la reproductibilité de l'étape de dynamique ; comparer les résultats sur une même machine, en vérifiant l'égalité des artefacts reproductibles, et non à l'aide d'un hash vidéo portable.
  — <https://github.com/AlayaLab/Marionette>
- Ne pas transférer les identifiants d'action d'un checkpoint à l'autre : leur signification dépend du dictionnaire propre à chaque jeu d'entraînement.
  — <https://huggingface.co/AlayaLab/Marionette>
- Ne pas appliquer le modèle à une nouvelle géométrie sans un nouveau scan de terrain, et ne pas l'interpréter comme un modèle général de mouvement de personnages.
  — <https://huggingface.co/AlayaLab/Marionette>

## Remplacé par cette version {#superseded-by-this}

- 2026-08-13 — le statut de la feuille de route « pretrained weights uploading » est devenu obsolète : la fiche de modèle AlayaLab/Marionette recense désormais les checkpoints publiés et les instructions de téléchargement.

## Points encore inconnus {#still-unknown}

- L'espace Hugging Face `hugging-apps/marionette-world-model` a renvoyé une erreur interne lors de la vérification ; son comportement en production et son statut de maintenance ne sont donc pas vérifiés.
- Le schéma de réponse fourni ne contient ni champ `event_findings` ni champ `new_events`. L'ajout spécifique au 2026-08-18 est donc consigné dans `what_changed` ; les évolutions distinctes datées du 2026-08-13 et du 2026-08-14 y figurent également.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://alayalab.github.io/Marionette/ | Marionette — Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |
| https://github.com/AlayaLab/Marionette | AlayaLab/Marionette repository | 2026-09-05 |
| https://huggingface.co/AlayaLab/Marionette | AlayaLab/Marionette — weights model card | 2026-09-05 |
| https://arxiv.org/abs/2608.14530 | Marionette: Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:marionette`, fil `public-project-release`, 1 événement daté, du 2026-08-18 au 2026-08-18.
- **Note pratique :** À partir du 2026-08-18, les praticiens doivent utiliser la page de projet, le dépôt, la page de modèle Hugging Face et l'espace hébergé liés comme point de départ pour évaluer Marionette ; les capacités, la licence et les étapes de reproduction nécessitent tout de même une recherche sur les sources avant toute adoption.
- **Confiance :** élevée. Les mentions de remplacement datées font foi pour déterminer ce qui est obsolète.
