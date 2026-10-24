---
title: "LiveEdit"
category: projects
date: 2026-06-30
tags: [liveedit, project]
aliases: ["LiveEdit"]
level: 2
source_sha256: 3fb8c2dfe7bc5339018baee3e702091ac08c05660d3ed74953010d8d587b47d1
translation: machine
translated_at: '2026-10-24'
---
# LiveEdit {#liveedit}

**Ligne de développement :** `project:liveedit` · fil `liveedit`  
**Dernier événement :** 2026-06-30 · 1 daté depuis le 2026-06-30 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

LiveEdit est un éditeur vidéo-à-vidéo guidé par texte, destiné aux environnements Linux et NVIDIA. Il repose sur Wan2.1-T2V-1.3B et s'exécute localement, et non sous forme de service hébergé.

- Édition vidéo-à-vidéo à partir d'invites textuelles appliquées à un flux d'entrée.
- Traitement causal par segments afin de préserver l'arrière-plan et les sections non modifiées.
- Mise en cache autorégressive des masques pour les clips courts, et un chemin étendu pour les longues vidéos.

## Ligne de développement {#development-line}

- **2026-06-30 — Les ressources du projet LiveEdit ont été rendues publiques.** La page officielle du projet, le dépôt de code et les points de contrôle des modèles étaient déjà en ligne. Les chronologies des auteurs situent les instructions relatives au code et aux points de contrôle au 2026-06-24, et la prépublication v1 au 2026-06-25 ; le 2026-06-30 n'est donc pas une date de publication par les auteurs.

## Modifications {#what-changed}

- **2026-06-30 :** Les points d'accès officiels du projet, des sources et des modèles de LiveEdit étaient déjà publics. Les auteurs ont publié les instructions relatives au code et aux points de contrôle le 2026-06-24, et la prépublication v1 le 2026-06-25 ; il ne s'agit donc pas d'une date de publication par les auteurs.
- **2026-07-13 :** arXiv a mis à jour l'article vers la v2, sans publication associée de code ou de points de contrôle.
- **2026-08-05 :** Les auteurs ont documenté l'inférence sur longue vidéo utilisant des puits d'attention glissants (rolling attention sinks) et un RoPE relatif à la fenêtre.

## Mode d'emploi {#how-to-use-this}

1. Sous Linux avec un GPU NVIDIA, créez l'environnement Python 3.10 documenté. Installez les dépendances et FlashAttention. L'inférence sur un seul GPU fonctionne ; les scripts d'entraînement nécessitent torchrun multi-GPU.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
2. Téléchargez Wan-AI/Wan2.1-T2V-1.3B ainsi que le point de contrôle ar-forcing_002000.pt documenté, dans les chemins attendus par le dépôt.
  — <https://huggingface.co/cp-cp/LiveEdit>
3. Créez un fichier JSON contenant instruction et source_path. Exécutez infer-local-ar-forcing.sh pour le chemin V2V documenté.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
4. Exécutez infer-token-pruning.sh avec --save_mask pour inspecter le cache. Exécutez infer-local-ar-forcing-long.sh pour des clips plus longs.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Utilisez le point de contrôle ar-forcing_002000.pt documenté (2 000 étapes) avec le script fourni. Tous les fichiers de poids du dépôt ne disposent pas d'une procédure autonome.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- En mode longue vidéo, gardez SINK_SIZE inférieur à LOCAL_ATTN_SIZE, et testez avec la longueur de clip cible. Les auteurs notent que la qualité de sortie se dégrade au-delà de l'horizon d'entraînement sur séquences courtes.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- Enregistrez les visualisations de masques pendant l'élagage des tokens afin de pouvoir inspecter les régions que le cache réutilise.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Points encore inconnus {#still-unknown}

- L'entrée du 2026-06-30 ne fournit que sa date et les URL officielles ; l'affirmation sous-jacente n'est pas disponible.
- Aucune exécution indépendante n'a reproduit les 12,66 FPS annoncés, ni n'a établi un seuil minimal de VRAM pour LiveEdit. Ce débit est un chiffre rapporté par les auteurs.
- Le nom LiveEdit est partagé : qizhou000/LiveEdit est un projet distinct, un modèle vision-langage d'édition de connaissances présenté à CVPR 2025. Le dépôt cp-cp, le point de contrôle Hugging Face, le site du projet et la prépublication arXiv identifient le projet d'édition vidéo décrit ici.
- Les dates du 2026-06-24 et du 2026-08-05 proviennent des journaux du README des auteurs, et non d'un suivi indépendant des publications ni de tests de qualité tiers.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://live-edit.github.io/ | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | ECCV 2026 | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit | GitHub - cp-cp/LiveEdit: LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit/blob/main/README.md | README.md · cp-cp/LiveEdit at main | 2026-09-06 |
| https://huggingface.co/cp-cp/LiveEdit | cp-cp/LiveEdit · Hugging Face | 2026-09-06 |
| https://arxiv.org/abs/2606.26740 | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/qizhou000/LiveEdit | qizhou000/LiveEdit: Lifelong Knowledge Editing for Vision Language Models with Low-Rank Mixture-of-Experts | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:liveedit`, fil `liveedit`, 1 événement daté du 2026-06-30 au 2026-06-30.
- **Note pratique :** Utilisez les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus déterminent ce qui est obsolète.
