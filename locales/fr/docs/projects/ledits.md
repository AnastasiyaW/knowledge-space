---
title: "LEDITS"
category: projects
date: 2023-12-03
tags: [ledits, ledits-development, project]
aliases: ["LEDITS", "LEDITS++"]
level: 3
source_sha256: a4211dc7eccce2b28451d39f784dbc13643455f220f87387a5208d1f17a23643
translation: machine
translated_at: '2026-10-24'
---
# LEDITS {#ledits}

**Ligne de développement :** `project:ledits` · fil `ledits-development`  
**Dernier événement :** 2023-12-03 · 2 événements datés depuis 2023-07-04 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

LEDITS est un pipeline d'édition d'images permettant de modifier des images réelles à l'aide de prompts textuels sémantiques, plutôt qu'au moyen d'une simple passe img2img générique.

- Inversion : inverse l'image d'entrée avant l'édition.
- Guidage : applique un ou plusieurs prompts de concept.
- Masquage : utilise des masques implicites pour restreindre les modifications aux régions pertinentes.
- Intégration : expose les pipelines Stable Diffusion et SDXL dans Diffusers.

L'espace Space d'origine de LEDITS est en pause, et l'implémentation Diffusers ne garantit pas une inversion parfaite. Utilisez LEDITS++ en local pour les éditions sémantiques avec Stable Diffusion ou SDXL ; utilisez l'implémentation des auteurs lorsque la fidélité de l'inversion constitue le livrable.

## Ligne de développement {#development-line}

- **2023-07-04 — La démo publique de LEDITS et le Hugging Face Space ont été liés.** Le 2023-07-04, le fil de développement de LEDITS a renvoyé vers une démo web publique, le Hugging Face Space et le dépôt editing-images/ledits. Ces liens n'établissent ni le périmètre de la version, ni la version du modèle, ni les capacités.
- **2023-12-03 — La démo publique de LEDITS++ et le Hugging Face Space ont été liés.** Le 2023-12-03, le fil a renvoyé vers une démo publique de LEDITS++, le Hugging Face Space et le dépôt editing-images/leditsplusplus. Il renvoyait également vers LEDITS. Ces liens ne confirment pas la relation technique exacte entre LEDITS et LEDITS++.

## Évolutions {#what-changed}

- 2023-07-04 — LEDITS a combiné l'inversion DDPM Edit-Friendly et le guidage sémantique SEGA pour l'édition d'images réelles sur Stable Diffusion v1.5.
- 2023-12-03 — LEDITS++ a introduit l'inversion SDE-DPM-Solver++, le masquage implicite par édition et les éditions simultanées natives.

## Mode d'emploi {#how-to-use-this}

Au 2023-12-03, distinguez les artefacts publics d'origine de LEDITS des artefacts LEDITS++ liés séparément, et consultez le Hugging Face Space ou le dépôt correspondant à la variante que vous comptez utiliser.

1. Choisissez `LEditsPPPipelineStableDiffusion` pour Stable Diffusion ou `LEditsPPPipelineStableDiffusionXL` pour SDXL, puis chargez un checkpoint de base compatible sur CUDA.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
2. Appelez `invert(image=...)` pour chaque nouvelle image source avant d'invoquer le pipeline d'édition ; l'édition utilise toujours la dernière inversion.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
3. Utilisez `source_prompt` uniquement lorsque l'inversion guidée est utile ; un prompt source vide désactive ce guidage.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
4. Passez une ou plusieurs valeurs `editing_prompt` et alignez `reverse_editing_direction`, `edit_guidance_scale` et `edit_threshold` sur ces prompts ; la direction contrôle si chaque concept est accentué ou atténué.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
5. Inspectez la reconstruction par inversion et le résultat d'édition ; si une inversion exacte est requise, utilisez le dépôt des auteurs plutôt que l'implémentation Diffusers.
  — <https://github.com/ml-research/ledits_pp>

## Bonnes pratiques {#best-practices}

- Utilisez un `torch.Generator` avec graine lorsque vous comparez des changements de paramètres, afin que l'inversion soit déterministe.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Considérez `skip` comme un contrôle de l'intensité d'édition : des valeurs plus faibles produisent des modifications plus marquées sur l'image d'entrée.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Réglez `edit_threshold` selon l'emprise de l'édition : une valeur plus petite pour des changements sur l'ensemble de l'image, comme un transfert de style, et une valeur proportionnelle à la région concernée pour les éditions locales.
  — <https://arxiv.org/html/2311.16711v1>
- Conservez par défaut le masque d'intersection implicite ; ajoutez `user_mask` uniquement lorsque le masque automatique ne correspond pas à la région voulue.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Pour la reproduction de recherche ou une exigence stricte de fidélité de reconstruction, privilégiez l'implémentation des auteurs, car son README indique que Diffusers ne garantit pas une inversion parfaite.
  — <https://github.com/ml-research/ledits_pp>

## Remplacé par ce qui suit {#superseded-by-this}

- 2023-07-04 — Utiliser l'ancien Gradio Space de LEDITS comme point d'entrée opérationnel est obsolète : le Space est en pause ; conservez-le comme code historique plutôt que comme flux de travail fiable.
- 2023-12-03 — Un usage limité à la démo hébergée est obsolète : depuis le 2024-03-15, Diffusers fournit des API de pipeline LEDITS++ pour Stable Diffusion et SDXL.
- 2023-12-03 — Considérer le résultat de reconstruction parfaite de l'article comme une garantie générale de la bibliothèque est obsolète : les auteurs indiquent que l'implémentation Diffusers ne garantit pas une inversion parfaite.

## Points encore inconnus {#still-unknown}

- Les sources primaires ne présentent pas explicitement LEDITS++ comme un remplacement versionné de la démo LEDITS de 2023 ; elles sont traitées ici comme des travaux étroitement liés, et non comme une lignée de versions de produit avérée.
- Le Space de LEDITS++ est affiché comme « Running on Zero », mais aucune génération d'image n'a été exécutée lors de cette vérification ; cela ne prouve pas une disponibilité fiable de l'hébergement.
- Aucune évaluation croisée actuelle face à des éditeurs d'images généralistes plus récents n'a été identifiée ; ce document ne prétend donc pas que LEDITS++ reste la meilleure solution en dehors de son intégration Stable Diffusion et SDXL.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/html/2307.00522 | LEDITS: Real Image Editing with DDPM Inversion and Semantic Guidance | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits | Space LEDITS | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits/tree/main | Arborescence des sources du Space LEDITS | 2026-09-04 |
| https://arxiv.org/html/2311.16711v1 | LEDITS++: Limitless Image Editing using Text-to-Image Models, arXiv v1 | 2026-09-04 |
| https://leditsplusplus-project.static.hf.space/index.html | Page du projet LEDITS++ | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus | Space LEDITS++ | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus/tree/main | Arborescence des sources du Space LEDITS++ | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp | API du pipeline LEDITS++ de Diffusers | 2026-09-04 |
| https://github.com/ml-research/ledits_pp | ml-research/ledits_pp, implémentation officielle | 2026-09-04 |
| https://huggingface.co/papers/2311.16711 | Page de l'article sur Hugging Face pour LEDITS++ | 2026-09-04 |
| https://huggingface.co/posts/sayakpaul/117997091400234 | Billet de version Diffusers 0.27.0 | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:ledits`, fil `ledits-development`, 2 événements datés du 2023-07-04 au 2023-12-03.
- **Note pratique :** Au 2023-12-03, les praticiens doivent distinguer les artefacts publics d'origine de LEDITS des artefacts LEDITS++ liés séparément, et consulter le Hugging Face Space ou le dépôt correspondant à la variante qu'ils comptent utiliser.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
