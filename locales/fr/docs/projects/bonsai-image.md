---
title: "Bonsai Image 4B — Développement de Bonsai Image"
category: projects
date: 2026-05-29
tags: [bonsai-image, project]
aliases: ["Bonsai Image 4B"]
level: 3
source_sha256: 4d9a8ddb8af72f50f3ec27b5230a0a1ff70bf17d15fcc3cc2e347b0387d819b5
translation: machine
translated_at: '2026-10-24'
---
# Bonsai Image 4B — Développement de Bonsai Image {#bonsai-image-4b-bonsai-image-development}

**Ligne de développement :** `project:bonsai-image` · fil `bonsai-image`  
**Dernier événement :** 2026-05-29 · 1 événement daté depuis le 2026-05-29 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Bonsai Image 4B : une famille de modèles de diffusion text-to-image destinés à une exécution locale. La variante Binary 1-bit privilégie une taille minimale, la variante Ternary privilégie la meilleure qualité, et la variante WebGPU reste expérimentale. Limite : le transformeur ternary occupe 1,21 Go, et l'ensemble complet pour Apple Silicon pèse 3,88 Go. Verdict : pour la génération locale, il faut commencer par le pack low-bit ternary plutôt que par la version FP16.

## Ligne de développement {#development-line}

- **2026-05-29 — Bonsai Image 4B a été rendu accessible via les ressources Hugging Face.** Le 2026-05-29, un enregistrement daté renvoyait les lecteurs vers une collection Hugging Face pour Bonsai Image ainsi que vers un Space WebGPU associé au projet. Cet événement est considéré comme une diffusion et un accès à l'évaluation significatifs, car il identifie des ressources publiques concrètes du projet. Les liens seuls ne permettent pas d'établir qu'une sortie de modèle, une mise à jour ou un benchmark a eu lieu à cette date.

## Évolutions {#what-changed}

2026-05-26 — PrismML a publié Bonsai Image 4B en deux variantes : Binary 1-bit et Ternary. 2026-05-29 — les liens vers la collection de poids et vers la démo WebGPU reflétaient la disponibilité du modèle ; la publication initiale précise la base FLUX.2 Klein 4B, une taille de 0,93 Go pour le diffusion transformer Binary et de 1,21 Go pour le Ternary, ainsi que les chemins d'exécution locaux sur Apple Silicon et CUDA. 2026-06-01 — la collection a ajouté des packs low-bit par plateforme ainsi que des variantes FP16 unpacked ; la version FP16 est destinée à la compatibilité avec Diffusers standard, et non à l'économie de mémoire ou à l'accélération.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-05-29, les praticiens peuvent utiliser la collection Hugging Face et le Space WebGPU liés comme points de départ pour localiser et évaluer Bonsai Image 4B ; ils ne doivent pas déduire le statut de publication, les capacités ou les recommandations d'usage à partir de ces seuls liens.

1. Clonez Bonsai Image Demo et exécutez le setup pour votre plateforme : MLX sur macOS, ou gemlite/HQQ sur Linux ou Windows.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
2. Chargez la variante Ternary par défaut ; choisissez Binary si la taille minimale prime sur la qualité.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
3. Lancez le studio via scripts/serve, ou envoyez des requêtes au backend déjà démarré via send_request, afin de ne pas payer le cold start à chaque image.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
4. Pour une exécution expérimentale dans le navigateur, ouvrez la démo WebGPU, chargez le modèle Ternary, indiquez le prompt et les paramètres ; la page demande un token d'accès Hugging Face.
  — <https://huggingface.co/spaces/webml-community/bonsai-image-webgpu>

## Bonnes pratiques {#best-practices}

- Utilisez Ternary comme variante standard : la démo officielle le recommande pour sa meilleure qualité, avec une augmentation modérée de la taille.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
- Ne choisissez pas les safetensors FP16 unpacked pour gagner en efficacité locale : ils servent de solution de repli pour Diffusers standard et ne conservent pas les avantages du pack low-bit.
  — <https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked>
- Pour la démo dans le navigateur, considérez la compatibilité comme non vérifiée en dehors des Apple M4 Max et M5 Max ; Chrome/Edge propose le flag WebGPU unsafe, uniquement pour les performances.
  — <https://webml-community-bonsai-image-webgpu.static.hf.space/index.html>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-01 — la recommandation d'utiliser FP16 unpacked comme voie principale est obsolète : les fiches officielles recommandent les packs low-bit optimisés pour MLX ou gemlite.

## Points encore inconnus {#still-unknown}

- La publication initiale est datée du 2026-05-26, alors que l'étape enregistrée est du 2026-05-29 ; la date exacte de création de la collection et du Space WebGPU n'est pas confirmée dans les sources consultées.
- Les champs requis event_findings et new_events sont absents du schéma de sortie fourni ; la précision liée à l'événement et la publication antérieure figurent dans evolutions.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://prismml.com/news/bonsai-image-4b | Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices | 2026-09-05 |
| https://huggingface.co/collections/prism-ml/bonsai-image | Bonsai Image - a prism-ml Collection | 2026-09-05 |
| https://huggingface.co/spaces/webml-community/bonsai-image-webgpu | Bonsai Image WebGPU - a Hugging Face Space by webml-community | 2026-09-05 |
| https://webml-community-bonsai-image-webgpu.static.hf.space/index.html | Bonsai image generation WebGPU demo | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-mlx-2bit | prism-ml/bonsai-image-ternary-4B-mlx-2bit | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked | Bonsai Image Ternary 4B — Unpacked FP16 Safetensors | 2026-09-05 |
| https://github.com/PrismML-Eng/Bonsai-image-demo | PrismML-Eng/Bonsai-Image-Demo | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:bonsai-image`, fil `bonsai-image`, 1 événement daté, du 2026-05-29 au 2026-05-29.
- **Note pratique :** À partir du 2026-05-29, les praticiens peuvent utiliser la collection Hugging Face et le Space WebGPU liés comme points de départ pour localiser et évaluer Bonsai Image 4B ; ils ne doivent pas déduire le statut de publication, les capacités ou les recommandations d'usage à partir de ces seuls liens.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
