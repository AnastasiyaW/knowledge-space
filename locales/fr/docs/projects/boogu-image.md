---
title: "Boogu-Image"
category: projects
date: 2026-06-18
tags: [boogu-image, boogu-image-development, boogu_image, project]
aliases: ["Boogu-Image"]
level: 3
source_sha256: 85cddaee9ee3f72d6c4071bfa65d71fe8bc0dc28988b1d03cec2c0f9b7bfd612
translation: machine
translated_at: '2026-10-24'
---
# Boogu-Image {#boogu-image}

**Ligne de développement :** `project:boogu-image` · fil `boogu-image-development`  
**Dernier événement :** 2026-06-18 · 1 événement daté depuis le 2026-06-18 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Boogu-Image est une famille de checkpoints ouverts à vocation de recherche, destinée aux équipes qui ont besoin d'un équivalent local de la combinaison Qwen-Image et ComfyUI. — Base : text-to-image, typographie dense en chinois et en anglais, fine-tuning. — Turbo : text-to-image en 3 à 4 étapes, axé en priorité sur le photoréalisme. — Edit et Edit-Turbo : édition d'image à partir d'une instruction textuelle. Ordre de grandeur : les variantes principales comptent 10 milliards de paramètres ; Base et Edit sont annoncés pour 1K, 1.5K et 2K, Turbo pour 1K uniquement. Verdict : convient à une intégration de recherche ou locale, mais pas comme API payante clé en main ni comme service de production sans protections et validations propres.

## Ligne de développement {#development-line}

- **2026-06-18 — Les ressources publiques du projet Boogu-Image ont été liées.** Aucune version officielle distincte n'a été trouvée à cette date ; les points d'entrée publics menaient déjà à la famille 0.1, au code, aux poids et à la démo.

## Ce qui a changé {#what-changed}

2026-06-16 : sortie de Boogu-Image-0.1-Base, -Edit et de la variante Turbo en quatre étapes. 2026-06-17 : apparition de ComfyUI-Boogu ; ce chemin est devenu legacy par la suite, après la prise en charge native dans ComfyUI. 2026-06-18 : aucune version officielle distincte n'a été trouvée à cette date ; les points d'entrée publics menaient déjà à la famille 0.1, au code, aux poids et à la démo. 2026-06-25 : Turbo a reçu le hotfix-20260625 pour les artefacts liés aux rapports d'aspect différents et aux artefacts d'arrière-plan, sans nouvelles fonctionnalités. 2026-06-30 : sortie de la variante image-to-image Edit-Turbo en quatre étapes. 2026-07-08 : Edit-Turbo a reçu un hotfix pour la dégradation de la qualité et la suppression peu efficace d'objets ; la révision 1K est recommandée. 2026-07-16 : publication du rapport technique Boogu-Image-0.1. 2026-07-22 : ajout d'un chemin de serving en ligne via vLLM-Omni. 2026-07-23 : une branche npu a fait apparaître un backend initial pour NPU.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-18, les praticiens doivent utiliser le site du projet, le dépôt, l'organisation Hugging Face, les démos et la galerie liés comme points d'entrée initiaux pour évaluer Boogu-Image.

1. Choisir Base pour le texte dense, la contrôlabilité et la résolution 2K ; Turbo pour un T2I photoréaliste rapide ; Edit ou Edit-Turbo pour modifier une image à partir d'une instruction.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
2. Créer un environnement Python 3.10 propre avec des versions de PyTorch/CUDA compatibles, installer les dépendances du projet et télécharger le checkpoint voulu dans le répertoire local models/ via la CLI Hugging Face.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
3. Pour le T2I en local, définir le même device dans la variable d'environnement et dans l'argument CLI, puis lancer inference.py avec le chemin vers Base ou Turbo, l'instruction et output_image_path.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
4. Pour l'édition, utiliser un checkpoint compatible Edit et fournir l'image d'entrée avec l'instruction textuelle ; pour un workflow portable, considérer qu'une seule image de référence constitue la limite sûre actuelle.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>
5. Dans ComfyUI, mettre à jour l'installation principale, télécharger les fichiers repackagés de Comfy-Org et construire le workflow à partir des nœuds standard Load Diffusion Model, Load CLIP avec type boogu, Load VAE et TextEncodeBooguEdit pour l'édition.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
6. Pour le serving API, lancer vLLM-Omni avec --omni sur Base ou Edit et vérifier la réponse avec un seed fixe ; le démarrage documenté pour Base requiert un seul GPU A100/H100 avec 40 Go de VRAM ou plus.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>

## Bonnes pratiques {#best-practices}

- Ne pas installer le ComfyUI-Boogu legacy sans raison particulière : la documentation actuelle recommande les nœuds natifs de ComfyUI et les modèles repackagés.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
- Pour une typographie bilingue dense, commencer par Base en 2K ; pour un T2I photoréaliste, choisir Turbo par défaut.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Pour Edit-Turbo, utiliser hotfix-1k-20260708 plutôt que le checkpoint d'origine : les auteurs qualifient la version 1K de plus stable.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Commencer par le pipeline par défaut : le prompt-tuning est présenté comme une voie de recherche facultative, moins robuste qu'une exécution standard.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Ne pas activer plusieurs modes d'offload en même temps ; obtenir d'abord une exécution stable sans accélération par cache, et désactiver torch.compile en cas d'images noires.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Ne pas utiliser en production sans vos propres contrôles de modération, de validation et de conformité : le projet limite explicitement la publication à un usage de recherche.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>

## Remplacé par ce document {#superseded-by-this}

- 2026-06-18 : l'interprétation de cette date comme date de lancement est obsolète ; le journal officiel date Base, Edit et Turbo du 2026-06-16.
- 2026-06-25 : la révision d'origine de Turbo doit être remplacée par hotfix-20260625 en cas de problèmes d'artefacts liés au rapport d'aspect ou à l'arrière-plan.
- 2026-07-08 : la version d'origine d'Edit-Turbo doit être remplacée par hotfix-1k-20260708 ; un hotfix 1.5K existe, mais la version 1K est recommandée comme plus stable.
- 2026-06-17 : l'installation du custom node legacy ComfyUI-Boogu n'est plus la voie recommandée ; le workflow natif de ComfyUI fait foi.

## Toujours inconnu {#still-unknown}

- Le README officiel publie à la fois le code et les poids sous Apache-2.0 et qualifie Boogu-Image-0.1 de research project rather than an official model release ; la portée pratique de cette formulation pour un usage commercial n'est pas précisée.
- La page d'accueil officielle décrit Boogu-Image-0.1-Pro comme une cinquième variante, mais aucun checkpoint distinct ni annonce datée de Pro n'a été trouvé dans la liste de modèles Hugging Face vérifiée.
- La documentation diverge sur le nombre d'images de référence : la note de version initiale et la recette vLLM en fixent une, alors que le guide d'inférence général décrit plusieurs chemins ; tant qu'un test reproductible distinct n'a pas été réalisé, une seule référence reste la limite portable sûre.
- Les documents primaires ont été vérifiés, mais la réplication indépendante des résultats annoncés aux arènes et aux benchmarks n'a pas été effectuée.
- Les données n'indiquent pas l'existence de deux projets distincts portant le nom Boogu-Image : les liens et les surfaces officielles actuelles mènent à une seule famille 0.1.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://boogu.org/ | Boogu-Image-0.1 — page officielle du projet | 2026-09-05 |
| https://github.com/boogu-project/Boogu-Image | boogu-project/Boogu-Image | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md | README de Boogu-Image | 2026-09-05 |
| https://huggingface.co/Boogu | Boogu sur Hugging Face | 2026-09-05 |
| https://huggingface.co/Boogu/Boogu-Image-0.1-Edit-Turbo/tree/hotfix-1k-20260708 | Boogu-Image-0.1-Edit-Turbo hotfix-1k-20260708 | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md | Guide d'inférence Boogu | 2026-09-05 |
| https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md | README de ComfyUI-Boogu | 2026-09-05 |
| https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md | Recette vLLM-Omni pour Boogu-Image | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:boogu-image`, fil `boogu-image-development`, 1 événement daté du 2026-06-18 au 2026-06-18.
- **Note pratique :** Au 2026-06-18, les praticiens doivent utiliser le site du projet, le dépôt, l'organisation Hugging Face, les démos et la galerie liés comme points d'entrée initiaux pour évaluer Boogu-Image.
- **Confiance :** moyenne. Les entrées datées de la section « Remplacé par ce document » font foi pour déterminer ce qui est obsolète.
