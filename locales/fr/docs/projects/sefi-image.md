---
title: "SeFi-Image"
category: projects
date: 2026-06-26
tags: [project, sefi-image, sefi-image-development]
aliases: ["SeFi-Image"]
level: 2
source_sha256: bf8faae64e0c1fc49f36b6c746c29d59b46b6e819c96e4ef72bbc9814368a218
translation: machine
translated_at: '2026-10-24'
---
# SeFi-Image {#sefi-image}

**Ligne de développement :** `project:sefi-image` · fil `sefi-image-development`  
**Dernier événement :** 2026-06-26 · 1 événement daté depuis 2026-06-26 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

SeFi-Image sépare les flux de latents sémantiques et de texture, de sorte que la structure soit débruitée avant le détail. Il propose les modèles Base 1B, 2B et 5B, un modèle RL 5B, ainsi que les modèles Turbo 1B, 2B et 5B. Les modèles Base et RL utilisent 50 étapes avec un guidage de 4.0 ; Turbo utilise par défaut quatre étapes avec un guidage de 1.0. Nous l'exploitons pour de la recherche locale contrôlée, et non pour un déploiement commercial ou une inférence hébergée.

## Ligne de développement {#development-line}

- **2026-06-26 — Les ressources officielles du projet SeFi-Image ont été liées.** Le 2026-06-26, un message de la ligne de développement a relié le site web du projet, le dépôt source et la page Hugging Face. Les éléments disponibles confirment ces liens, mais n'indiquent aucune version, aucun modèle ni aucune étape technique précise.

## Ce qui a changé {#what-changed}

2026-06-26 — La version 3 de l'arXiv a présenté SeFi-Image comme une famille publique de modèles texte-vers-image à diffusion sémantique d'abord (T2I), avec des échelles 1B, 2B et 5B et des variantes Turbo distillées par DMD2.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-26, nous utilisons le site web du projet, le dépôt GitHub et la page Hugging Face référencés pour évaluer SeFi-Image.

1. Acceptez les conditions d'accès aux points de contrôle, puis choisissez un point de contrôle : Base pour l'analyse ou le réglage fin, RL pour une génération orientée vers l'alignement, ou Turbo pour une génération rapide.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
2. Installez l'environnement d'exécution du dépôt sous Python 3.11 avec PyTorch correspondant à la version CUDA locale, puis installez Diffusers, Transformers, Accelerate, Safetensors, Hugging Face Hub, OmegaConf et Pillow.
  — <https://github.com/jmliu206/SeFi-Image>
3. Exécutez `inference.py` avec un identifiant de point de contrôle, un prompt, un répertoire de sortie et une graine ; utilisez un point de contrôle Base tel que `SeFi-Image/SeFi-Image-5B-Base` pour le parcours par défaut à 50 étapes.
  — <https://github.com/jmliu206/SeFi-Image>
4. Pour une génération à faible latence, sélectionnez un point de contrôle Turbo et réglez quatre étapes avec un guidage de 1.0.
  — <https://github.com/jmliu206/SeFi-Image>
5. Pour un flux de travail Diffusers standard, chargez un point de contrôle `-diffusers` avec `SeFiPipeline` ou `DiffusionPipeline` en BF16 sur CUDA.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers>

## Bonnes pratiques {#best-practices}

- Conservez Turbo à 4, 8 ou 10 étapes de débruitage et un guidage de 1.0 ; le projet documente quatre étapes comme valeur par défaut.
  — <https://github.com/jmliu206/SeFi-Image>
- Utilisez les points de contrôle Base comme point de départ pour le réglage fin et l'analyse ; réservez Turbo à la génération rapide et RL à une sortie plus fortement orientée vers l'alignement.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
- Considérez les poids publiés comme des supports de recherche sous licence CC BY-NC 4.0, à accès restreint ; appliquez une supervision humaine, une modération, une validation et des contrôles de conformité avant tout usage plus large.
  — <https://github.com/jmliu206/SeFi-Image>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points restant inconnus {#still-unknown}

- Les sources ne fournissent pas de journal des modifications daté décrivant les différences substantielles entre les versions 3, 4 et 5 de l'arXiv.
- Aucune source de première main n'établit une option de service en production ; les fiches Hugging Face Diffusers examinées indiquent qu'aucun Inference Provider ne déploie les modèles.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://jmliu206.github.io/sefi-web/ | SeFi-Image | Semantic-First Diffusion | 2026-09-05 |
| https://github.com/jmliu206/SeFi-Image | GitHub - jmliu206/SeFi-Image | 2026-09-05 |
| https://huggingface.co/SeFi-Image | Organisation SeFi-Image sur Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.22568 | SeFi-Image: A Text-to-Image Foundation Model with Semantic-First Diffusion | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base | SeFi-Image/SeFi-Image-5B-Base | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers | SeFi-Image/SeFi-Image-5B-turbo-diffusers | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:sefi-image`, fil `sefi-image-development`, 1 événement daté du 2026-06-26 au 2026-06-26.
- **Note pratique :** Au 2026-06-26, utilisez le site web du projet, le dépôt GitHub et la page Hugging Face référencés comme points de départ pour évaluer SeFi-Image.
- **Confiance :** élevée. Les mentions de remplacement datées ci-dessus font foi pour ce qui est obsolète.
