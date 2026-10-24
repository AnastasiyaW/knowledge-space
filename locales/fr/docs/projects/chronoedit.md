---
title: "ChronoEdit"
category: projects
date: 2025-11-18
tags: [chronoedit, chronoedit-release-and-adapters, project]
aliases: ["ChronoEdit"]
level: 3
source_sha256: 1b6d4edb567a48210af8048de07a17de04c4888ed08d8e10d0f8538b785e1bc9
translation: machine
translated_at: '2026-10-24'
---
# ChronoEdit {#chronoedit}

**Ligne de développement :** `project:chronoedit` · fil `chronoedit-release-and-adapters`  
**Dernier événement :** 2025-11-18 · 3 datés depuis le 2025-10-31 · **Vérifié le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

ChronoEdit — un éditeur d'images Diffusers destiné aux créateurs et développeurs qui ont besoin qu'une modification d'objet reste plausible dans sa scène.

- Traite l'image source et l'image modifiée comme les extrémités d'une courte vidéo, puis utilise un raisonnement temporel pour guider la modification.
- Prend en charge l'édition à partir d'un prompt, un LoRA de distillation en huit étapes, un LoRA d'upscaling et un LoRA Paint Brush de transformation d'un croquis en objet.
- Le flux de travail de base 14B nécessite environ 34 Go de VRAM avec déchargement du modèle, ou environ 38 Go avec le raisonnement temporel ; l'upscaler est testé jusqu'à 2K.

À utiliser pour des flux de travail d'édition d'images en local sur CUDA, lorsque l'interaction entre objets compte. Ce n'est pas un éditeur de bureau léger.

## Ligne de développement {#development-line}

- **2025-10-31 — le projet ChronoEdit, son code, sa démo et les ressources du modèle 14B ont été liés.** Le 2025-10-31, des liens ont publié la page de recherche ChronoEdit, le dépôt GitHub, l'espace Hugging Face et le modèle ChronoEdit-14B-Diffusers.
- **2025-11-11 — le LoRA Upscaler ChronoEdit 14B Diffusers a été ajouté à la ligne.** Le 2025-11-11, des liens ont publié l'artefact d'accompagnement séparé ChronoEdit-14B-Diffusers-Upscaler-Lora.
- **2025-11-18 — le LoRA Paint Brush ChronoEdit 14B Diffusers a été ajouté à la ligne.** Le 2025-11-18, des liens ont publié l'artefact d'accompagnement séparé ChronoEdit-14B-Diffusers-Paint-Brush-Lora, après le modèle de base et le LoRA Upscaler.

## Ce qui a changé {#what-changed}

ChronoEdit est passé d'un éditeur de base 14B à un pipeline Diffusers amont accompagné de deux LoRA spécialisés.

- 2025-10-31 — le point de contrôle 14B Diffusers, le code source et la démo ont rendu le flux de travail de base utilisable ; le dépôt de NVIDIA date la publication du point de contrôle au 2025-10-29.
- 2025-11-11 — le LoRA Upscaler a ajouté un flux de travail dédié de super-résolution préservant le contenu ; NVIDIA date sa publication au 2025-11-10.
- 2025-11-18 — le LoRA Paint Brush a ajouté l'édition de croquis noirs vers objet ; NVIDIA date sa publication au 2025-11-16 et recommande de l'associer au LoRA de distillation en huit étapes.
- 2026-09-04 — la documentation officielle de Diffusers répertorie le modèle de base 14B et deux LoRA comme ressources ChronoEdit prises en charge.

## Mode d'emploi {#how-to-use-this}

Au 2025-11-18, nous considérons ChronoEdit comme un modèle Diffusers 14B de base accompagné d'adaptateurs LoRA Upscaler et Paint Brush distincts. Vérifiez la documentation primaire pour confirmer la compatibilité et l'usage avant toute exécution.

1. Installez Linux avec Python 3.10, configurez l'environnement du dépôt et téléchargez `nvidia/ChronoEdit-14B-Diffusers`.
  — <https://github.com/nv-tlabs/ChronoEdit>
2. Chargez le point de contrôle de base via `ChronoEditPipeline` dans Diffusers sur CUDA, chargez l'image source et redimensionnez-la à la grille latente prise en charge.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
3. Exécutez l'image avec un prompt décrivant la modification et ce qui doit rester inchangé ; prenez la dernière image générée comme image modifiée.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
4. Pour une édition standard rapide, chargez le LoRA de distillation en huit étapes fourni avec `flow_shift=2.0`, une échelle de guidage de `1.0` et huit étapes d'inférence.
  — <https://github.com/nv-tlabs/ChronoEdit>
5. Pour un agrandissement préservant le contenu, chargez le LoRA Upscaler avec son prompt de super-résolution ; restez à la limite testée de 2K ou en dessous.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
6. Pour une modification d'objet dessiné, chargez Paint Brush avec le LoRA de distillation en huit étapes, fournissez un croquis au crayon noir et décrivez l'objet cible.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora>

## Bonnes pratiques {#best-practices}

- Utilisez l'optimiseur de prompt fourni et le guidage par prompt pour l'édition de base lorsque la mémoire le permet ; le dépôt qualifie cette voie de meilleure pour les résultats.
  — <https://github.com/nv-tlabs/ChronoEdit>
- N'activez le raisonnement temporel que lorsque la cohérence de la scène vaut la mémoire supplémentaire : l'exigence documentée passe d'environ 34 Go à 38 Go de VRAM.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Conservez les réglages du LoRA de distillation à huit étapes, une échelle de guidage de 1.0 et un flow shift de 2.0, plutôt que de le traiter comme un préréglage LoRA quelconque.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Pour le LoRA Upscaler, utilisez son prompt déclencheur préservant le contenu et évitez l'optimiseur de prompt ; la fiche officielle indique qu'il est inutile.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
- Pour le LoRA Paint Brush, utilisez des croquis noirs et combinez-le avec le LoRA de distillation en huit étapes ; les autres couleurs de croquis donnent de moins bons résultats.
  — <https://github.com/nv-tlabs/ChronoEdit>

## Remplacé par {#superseded-by-this}

- 2025-11-10 — le wrapper du dépôt comme unique voie d'inférence est obsolète : ChronoEdit a été intégré à Hugging Face Diffusers.
- 2025-11-10 — l'agrandissement reposant sur le modèle de base seul est remplacé par le flux de travail du LoRA Upscaler, testé jusqu'à 2K.
- 2025-11-16 — l'édition par texte seul pour les croquis est remplacée par le LoRA Paint Brush avec le flux de travail de distillation en huit étapes.

## Points encore inconnus {#still-unknown}

- Aucun guide officiel en chinois simplifié n'a été trouvé ; les indications opérationnelles citées ici sont en anglais.
- Les sources officielles répertorient le modèle de base 14B et deux LoRA, mais ne confirment pas l'existence de points de contrôle plus récents ailleurs.
- L'espace hébergé officiel a renvoyé une erreur interne lors de cette vérification ; la disponibilité de la démo en direct reste non vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://research.nvidia.com/labs/toronto-ai/chronoedit/ | ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://github.com/nv-tlabs/ChronoEdit | nv-tlabs/ChronoEdit — ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/chronoedit | ChronoEdit — Hugging Face Diffusers documentation | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers | nvidia/ChronoEdit-14B-Diffusers | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:chronoedit`, fil `chronoedit-release-and-adapters`, 3 événements datés du 2025-10-31 au 2025-11-18.
- **Note pratique :** Au 2025-11-18, nous considérons ChronoEdit comme un modèle Diffusers 14B de base accompagné d'adaptateurs LoRA Upscaler et Paint Brush distincts. Vérifiez la documentation primaire pour confirmer la compatibilité et les instructions d'utilisation avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus déterminent ce qui est obsolète.
