---
title: "Lucida"
category: projects
date: 2026-07-21
tags: [lucida, lucida-development, project]
aliases: ["Lucida"]
level: 2
source_sha256: 294112d318599a234887dcbcdfef65d084c7d1b1081d507c2cc39f669b6c7694
translation: machine
translated_at: '2026-10-24'
---
# Lucida {#lucida}

**Ligne de développement :** `project:lucida` · fil `lucida-development`  
**Dernier événement :** 2026-07-21 · 1 daté depuis le 2026-07-21 · **Recherché :** 2026-09-05 · confiance : élevée

## Description {#what-it-is}

Lucida est un modèle MIT de segmentation et de matting alpha destiné aux utilisateurs pour qui RMBG-2.0 ou un suppresseur d'arrière-plan classique perd les détails semi-transparents et fins.

Fonctionnalités : sortie RGBA, exécution locale en Python, en CLI ou via HTTP, Transformers et ComfyUI.

Mesure : le test publié sur 203 images donne un MAE moyen de 0,0257 pour les poids v7 actuels.

Verdict : choisissez-la pour le texte, les imprimés, le camouflage et les illustrations ; pour les structures fines, les scènes complexes et les cheveux, les concurrents mesurés restent plus performants.

## Ligne de développement {#development-line}

- **2026-07-21 — Les ressources de développement de Lucida ont été liées.** Ajout de la catégorie print-design/sticker, MAE moyen passé à 0,0257 sur 203 images, et le modèle est apparu dans la collection officielle de modèles ComfyUI.

## Modifications {#what-changed}

2026-07-13 — sortie de Lucida v1.0 : première version publique avec des poids MIT, prise en charge de Transformers et test sur 191 images dans huit catégories. 2026-07-18 — la v1.1 a ajouté un entraînement sur 9 426 paires pour préserver les parties opaques des objets transparents et les objets coupés par le bord du cadre ; le MAE de transparence s'est dégradé de 0,0376 à 0,0403. 2026-07-21 — à ce stade, la version actuelle était Lucida v1.2 du 2026-07-20 : ajout de la catégorie print-design/sticker, MAE moyen passé à 0,0257 sur 203 images, et le modèle est apparu dans la collection officielle de modèles ComfyUI. 2026-07-23 — la v1.3 a publié la v13 avec une perte pour la propreté de l'arrière-plan et une « soupe » de points de contrôle ; le MAE moyen annoncé était de 0,0250. 2026-07-24 — les poids v13 ont été retirés en raison d'une régression sur les illustrations réelles multicouches ; le modèle sert de nouveau les poids v7, et la v14 est désignée comme étant en cours de travail.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-21, les praticiens doivent considérer le dépôt GitHub de Lucida, la page de modèle Hugging Face et les Spaces de démonstration et de présentation liés comme points de départ datés pour évaluer ou reproduire le projet, tout en vérifiant indépendamment les versions et les capacités.

1. Installez le projet avec Python 3.12+ via uv et exécutez `uv run bgr remove input.jpg -o output.png --model lucida` ; enregistrez le résultat en PNG pour ne pas perdre le canal alpha.
  — <https://github.com/egeorcun/lucida>
2. Pour Python, chargez `egeorcun/lucida` via `AutoModelForImageSegmentation` ou un pipeline avec `trust_remote_code=True` ; convertissez l'entrée en RGB.
  — <https://huggingface.co/egeorcun/lucida>
3. Pour ComfyUI, téléchargez `lucida.safetensors` dans `ComfyUI/models/background_removal/` et ouvrez le workflow joint Remove Background (BiRefNet).
  — <https://github.com/egeorcun/lucida>
4. Pour un essai rapide sans installation locale, téléversez une image dans la démonstration Gradio fonctionnant sur ZeroGPU.
  — <https://huggingface.co/spaces/egeorcun/lucida-demo>

## Bonnes pratiques {#best-practices}

- Utilisez 1024×1024 pour l'inférence : c'est la résolution recommandée et utilisée pour l'entraînement ; redimensionnez ensuite l'alpha à la taille d'origine.
  — <https://github.com/egeorcun/lucida>
- Pour les cadres complexes à plusieurs objets, les structures fines et les cheveux, comparez le résultat avec InSPyReNet ou RMBG-2.0, plutôt que de supposer un avantage universel de Lucida.
  — <https://github.com/egeorcun/lucida>
- N'adoptez pas la v13 : les poids publiés ont été ramenés à la v7 après une régression constatée sur de vraies images en couches.
  — <https://github.com/egeorcun/lucida/releases>
- Avant toute utilisation commerciale, évaluez vous-même le risque de licence : une partie des jeux de données d'entraînement est indiquée comme réservée à la recherche, alors que le code et les poids sont publiés sous licence MIT.
  — <https://github.com/egeorcun/lucida>

## Éléments remplacés {#superseded-by-this}

- 2026-07-18 : la v1.0 est remplacée par la v1.1 pour les objets transparents avec parties opaques et les objets au bord du cadre.
- 2026-07-20 : la v1.1 est remplacée par la v1.2/v7 pour les tâches de print-design et d'art de type sticker.
- 2026-07-24 : la recommandation d'utiliser la v13 est obsolète ; les poids publiés sont revenus à la v7 en raison d'une régression sur les illustrations multicouches.

## Points non élucidés {#still-unknown}

- La publication complète du 2026-07-21 ne contient pas de texte ; sa thèse exacte n'a donc pas pu être reconstituée. Le lien de cette étape avec la v1.2 est établi à partir du release primaire le plus proche, du 2026-07-20, et des références au même dépôt, aux mêmes poids et à la même démonstration.
- Le schéma de réponse ne contient pas de champs distincts event_findings et new_events ; leurs informations sont intégrées à la chronologie de what_changed.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/egeorcun/lucida | egeorcun/lucida — README | 2026-09-05 |
| https://huggingface.co/egeorcun/lucida | egeorcun/lucida — carte du modèle Hugging Face | 2026-09-05 |
| https://huggingface.co/spaces/egeorcun/lucida-demo | Lucida — démo de suppression d'arrière-plan | 2026-09-05 |
| https://github.com/egeorcun/lucida/releases | egeorcun/lucida — releases GitHub | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:lucida`, fil `lucida-development`, 1 événement daté du 2026-07-21 au 2026-07-21.
- **Note pratique :** À partir du 2026-07-21, les praticiens doivent considérer le dépôt GitHub de Lucida, la page de modèle Hugging Face et les Spaces de présentation et de démonstration liés comme points de départ datés pour évaluer ou reproduire le projet, tout en vérifiant indépendamment les versions et les capacités.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
