---
title: "PowerPaint"
category: projects
date: 2024-07-21
tags: [powerpaint, project]
aliases: ["PowerPaint"]
level: 2
source_sha256: 94a5edbe5069756a3a5ef6c13f601ab344923e7e0fb47fe390dd2d7e10da051f
translation: machine
translated_at: '2026-10-24'
---
# PowerPaint {#powerpaint}

**Ligne de développement :** `project:powerpaint` · fil `powerpaint`  
**Dernier événement :** 2024-07-21 · 2 événements datés depuis 2023-12-12 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

PowerPaint est un système d'inpainting basé sur Stable Diffusion, permettant d'éditer les zones masquées d'une image.

- Insertion d'objets guidée par le texte, pour ajouter des éléments à partir de prompts textuels.
- Suppression d'objets sans prompt, avec prompts négatifs optionnels pour effacer des objets.
- Outpainting d'image, pour étendre les limites du canevas.
- Insertion d'objets guidée par la forme, pour adapter les éléments ajoutés au contour d'un masque.

## Ligne de développement {#development-line}

- **2023-12-12 — PowerPaint devient publiquement disponible.** Le 2023-12-12, le projet est lancé sur son site web, dans une implémentation MMagic et sur une page d'application OpenXLab.
- **2024-07-21 — Lien vers le dépôt OpenMMLab autonome.** Le 2024-07-21, PowerPaint renvoie les utilisateurs vers le dépôt autonome open-mmlab/PowerPaint. Ces liens marquent ce changement sans montrer de modifications du code ni des modèles.

## Changements {#what-changed}

- 2023-12-12 — L'article de PowerPaint introduit des prompts de tâche apprenables, afin qu'un seul modèle gère le remplissage de contexte, l'insertion et la suppression d'objets, ainsi que le guidage par forme.
- 2023-12-18 — Les poids Stable v1 remplacent la version précédente.
- 2023-12-22 — Les mainteneurs corrigent l'erreur de chargement de ControlNet dans le chemin de la démo.
- 2024-04-06 — Le réentraînement avec BrushNet produit PowerPaint v2 tout en conservant les couches d'attention croisée des prompts de tâche.
- 2024-04-07 — Le code et les poids de PowerPaint v2 sont publiés.
- 2024-05-22 — Les poids PowerPaint v2-1 remplacent les poids initiaux de la v2 pour corriger des problèmes d'entraînement.
- 2024-07-21 — Le dépôt public est disponible, mais son changelog n'enregistre aucune publication séparée de modèle le 21 juillet.

## Mode d'emploi {#how-to-use-this}

Du 2023-12-12 au 2024-07-21, le projet fonctionne via son site, MMagic et OpenXLab ; à partir du 2024-07-21, utilisez le dépôt OpenMMLab autonome.

1. Clonez le dépôt, créez un environnement Conda avec Python 3.9 et installez les dépendances épinglées.
  — <https://github.com/open-mmlab/PowerPaint>
2. Installez Git LFS, puis téléchargez le point de contrôle PowerPaint v2 dans un répertoire local de points de contrôle.
  — <https://github.com/open-mmlab/PowerPaint>
3. Lancez l'interface Gradio v2 avec `python app.py --share --version ppt-v2 --checkpoint_dir checkpoints/ppt-v2`.
  — <https://github.com/open-mmlab/PowerPaint>
4. Importez une image, peignez le masque d'édition, choisissez l'onglet de la tâche et ne saisissez du texte que pour l'insertion d'objets ou le guidage par forme.
  — <https://github.com/open-mmlab/PowerPaint>
5. Laissez le prompt vide pour la suppression ou l'outpainting ; définissez les taux d'expansion horizontal et vertical pour l'outpainting.
  — <https://github.com/open-mmlab/PowerPaint>

## Bonnes pratiques {#best-practices}

- Laissez le prompt vide pour la suppression d'objets ; ajoutez un prompt négatif et augmentez Guidance Scale à 10 ou plus si des objets indésirables apparaissent.
  — <https://github.com/open-mmlab/PowerPaint>
- Réglez le degré d'ajustement (fitting degree) entre 0,5 et 0,6 lorsque l'objet peut s'écarter du masque, et entre 0,8 et 0,95 pour épouser fidèlement la forme du masque.
  — <https://github.com/open-mmlab/PowerPaint>
- Utilisez les poids v2-1 plutôt que la version initiale v2, car les mainteneurs ont publié la v2-1 spécifiquement pour corriger des problèmes d'entraînement.
  — <https://github.com/open-mmlab/PowerPaint>

## Remplacé par {#superseded-by-this}

- 2023-12-22 — Les anciennes indications sur la démo ControlNet sont obsolètes, car la logique de chargement a été corrigée.
- 2024-05-22 — Les poids initiaux de PowerPaint v2 sont remplacés par la v2-1, qui corrige les problèmes d'entraînement.

## Points inconnus {#still-unknown}

- Le dépôt ne comporte aucune version étiquetée correspondant à une publication distincte du 2024-07-21 ; cette date peut refléter un déplacement du dépôt plutôt qu'une mise à jour du modèle.
- La documentation couvre l'installation locale et l'interface Gradio, mais omet les limites de mémoire GPU, la prise en charge des systèmes d'exploitation et la compatibilité avec Diffusers.
- Ni la page originale du projet ni le point d'accès de la démo OpenXLab n'ont fourni de détails techniques exploitables lors de cette vérification.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2312.03594 | A Task is Worth One Word: Learning with Task Prompts for High-Quality Versatile Image Inpainting | 2026-09-04 |
| https://github.com/open-mmlab/mmagic | MMagic — OpenMMLab generative-image and video toolbox | 2026-09-04 |
| https://github.com/open-mmlab/PowerPaint | open-mmlab/PowerPaint | 2026-09-04 |
| https://huggingface.co/JunhaoZhuang/PowerPaint_v2 | JunhaoZhuang/PowerPaint_v2 | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:powerpaint`, fil `powerpaint`, 2 événements datés du 2023-12-12 au 2024-07-21.
- **Note pratique :** Du 2023-12-12, les praticiens pouvaient trouver PowerPaint via son site, MMagic et OpenXLab ; à partir du 2024-07-21, consultez le dépôt OpenMMLab autonome.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
