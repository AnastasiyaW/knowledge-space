---
title: "Flux2-Klein-9B-Consistency"
category: projects
date: 2026-03-13
tags: [flux2-klein-9b-consistency, flux2-klein-9b-consistency-releases, lora_releases, project]
aliases: ["Flux2-Klein-9B-Consistency"]
level: 2
source_sha256: 3a558395c18179aa744aba75df8accb316aa78ce4d3036e4674b5458aa8b52f9
translation: machine
translated_at: '2026-10-24'
---
# Flux2-Klein-9B-Consistency {#flux2-klein-9b-consistency}

**Ligne de développement :** `project:flux2-klein-9b-consistency` · fil `flux2-klein-9b-consistency-releases`  
**Dernier événement :** 2026-03-13 · 1 entrée datée depuis le 2026-03-13 · **Consultée le :** 2026-09-05 · confiance : medium

## Présentation {#what-it-is}

Flux2-Klein-9B-Consistency est un LoRA image-to-image pour le modèle de base black-forest-labs/FLUX.2-klein-9B.

- Préservation de la composition et des détails de l'image source lors d'une édition sémantique.
- Réduction du décalage de couleur et de la sursaturation dans la V2.

L'adaptateur n'est pas un modèle 9B indépendant ; les conditions de licence du modèle de base s'appliquent séparément. Utilisez la V2 pour l'édition contrôlée d'images source, et non comme générateur généraliste.

## Ligne de développement {#development-line}

- **2026-03-13 — Ressource Flux2-Klein-9B-Consistency liée.** Le 2026-03-13, la ligne Flux2-Klein-9B-Consistency a été reliée à une ressource Hugging Face publiée par dx8152 ainsi qu'à une vidéo YouTube. Ces liens marquent une étape de disponibilité publique sans établir les capacités du modèle, les détails de version ni le flux de travail prévu.

## Modifications {#what-changed}

- 2026-03-13 — Publication de l'adaptateur Consistency pour FLUX.2 Klein 9B ; une entrée tierce datée du 2026-03-06 précisait le graphe de workflow et CFG=1.
- 2026-04-17 — Ajout de Flux2-Klein-9B-consistency-V2.safetensors pour corriger la dominante de couleur, les détails excessifs et la sursaturation de la V1. Le fichier V2 fait 331 Mo, avec un SHA-256 de 61db2017ce420b97bd5ef11984e5a894c90003a6bbf0dc9473f8d7b9ebb3ff93.

## Mode d'emploi {#how-to-use-this}

Consultez le dépôt Hugging Face de dx8152 ainsi que la vidéo liée du 2026-03-13 pour évaluer l'adéquation avant adoption.

1. Installez les versions actuelles de diffusers, transformers et accelerate ; chargez le modèle de base black-forest-labs/FLUX.2-klein-9B en bfloat16 sur CUDA.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
2. Chargez les poids de l'adaptateur via load_lora_weights("dx8152/Flux2-Klein-9B-Consistency") et transmettez l'image source avec les instructions d'édition.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
3. Pour ComfyUI en local, placez le modèle 9B de base, l'encodeur de texte Qwen 3 8B et le VAE flux2 dans leurs répertoires respectifs, puis appliquez le LoRA dans un workflow d'édition d'image.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Bonnes pratiques {#best-practices}

- Privilégiez la V2 à la V1 : elle corrige le décalage de couleur, les détails bruités et la sursaturation.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
- Commencez à une intensité de 0,3 à 0,5 lorsque vous combinez avec des LoRA d'éclairage : cela préserve les détails mais atténue le changement d'éclairage.
  — <https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880>
- Testez avec votre version du modèle de base et votre workflow : les retours d'utilisateurs divergent, avec de mauvais résultats signalés sur les variantes FP8 et GGUF.
  — <https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/>

## Remplacé par {#superseded-by-this}

- 2026-04-17 — La V1 est obsolète dès lors que la neutralité des couleurs, la netteté des détails et la maîtrise de la saturation importent.

## Points non établis {#still-unknown}

- Les journaux primaires ne confirment pas la date exacte de mise en ligne de la V1 ; les enregistrements du 2026-03-06 confirment le modèle de base, l'objectif et CFG=1 pour la publication du 2026-03-13.
- La vidéo JXMbbbdfnSg était illisible : son contenu n'a donc pas été retenu comme preuve.
- Aucun benchmark indépendant et reproductible ne confirme les gains de cohérence revendiqués ; les retours d'utilisateurs divergent sur la qualité et la compatibilité.
- Le dépôt de l'adaptateur indique Apache-2.0, alors que la documentation de BFL spécifie la FLUX Non-Commercial License pour le 9B Base ; vérifiez les poids du modèle de base avant tout usage commercial.

## Sources {#sources}

| source | titre | consultée |
|---|---|---|
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency | dx8152/Flux2-Klein-9B-Consistency | 2026-09-05 |
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency/commit/ab936d843fea26adb9fac23132d7fc834c529ed7 | Ajout de Flux2-Klein-9B-consistency-V2.safetensors | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1rm3g3j/dx8152_flux_2_klein_9b_consistency_lora/ | LoRA Consistency de DX8152 pour Flux 2 Klein 9b | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | Guide ComfyUI Flux.2 Klein | 2026-09-05 |
| https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880 | Lighting Angle Change workflow! | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/ | Corriger l'effet « plastique » dans Flux.2 Klein 9B avec le LoRA Consistency | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:flux2-klein-9b-consistency`, fil `flux2-klein-9b-consistency-releases`, 1 événement daté du 2026-03-13 au 2026-03-13.
- **Note pratique :** Au 2026-03-13, les praticiens doivent considérer Flux2-Klein-9B-Consistency comme une ressource dx8152 publiquement liée, et examiner sa page Hugging Face ainsi que la vidéo liée avant de décider si elle convient à leur workflow ; ses capacités et sa compatibilité restent non vérifiées.
- **Confiance :** medium. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
