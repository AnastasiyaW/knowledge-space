---
title: "ControlNet pour SDXL — Publications de modèles ControlNet SDXL"
category: projects
date: 2023-08-14
tags: [controlnet-sdxl, controlnet_sdxl, project, sdxl-controlnet-model-releases]
aliases: ["ControlNet Depth for SDXL", "ControlNet OpenPose for SDXL", "ControlNet for SDXL"]
level: 2
source_sha256: 041923eb31f3a46ff3a079f89c0c69bb63dac9f5586b63dbcd57ceeb4d1073b7
translation: machine
translated_at: '2026-10-24'
---
# ControlNet pour SDXL — Publications de modèles ControlNet SDXL {#controlnet-for-sdxl-sdxl-controlnet-model-releases}

**Ligne de développement :** `project:controlnet-sdxl` · fil `sdxl-controlnet-model-releases`  
**Dernier événement :** 2023-08-14 · 3 événements datés depuis 2023-08-10 · **Recherche :** pas encore · confiance : non recherché

## Présentation {#what-it-is}

ControlNet pour SDXL adapte les modèles de conditionnement à SDXL. Nous n'avons pas encore mené de recherche sur l'état actuel ; cette page ne contient donc que la ligne datée et la note pratique ci-dessous, rien de plus.

## Ligne de développement {#development-line}

- **2023-08-10 — Diffusers a publié un exemple et un modèle ControlNet SDXL.** Le 2023-08-10, Hugging Face Diffusers a fait référence à un exemple ControlNet spécifique à SDXL et au dépôt de modèle diffusers/controlnet-sdxl-1.0. Il s'agissait d'une étape de développement publique visant à adapter les workflows ControlNet à SDXL. Le lien Reddit associé constitue un contexte complémentaire, et non un événement distinct.
- **2023-08-14 — Un modèle ControlNet OpenPose pour SDXL a été référencé.** Le 2023-08-14, le dépôt de modèle thibaud/controlnet-openpose-sdxl-1.0 a été référencé. Il fournit une option ControlNet SDXL pour le contrôle de pose OpenPose, enrichissant l'ensemble des modèles ControlNet SDXL disponibles.
- **2023-08-14 — Un modèle ControlNet de profondeur pour SDXL a été référencé.** Le 2023-08-14, le dépôt de modèle diffusers/controlnet-depth-sdxl-1.0 a été référencé. Il ajoute un point de contrôle ControlNet SDXL pour le conditionnement par profondeur, offrant une modalité de contrôle distincte à côté du modèle OpenPose.

## Comment l'utiliser {#how-to-use-this}

À la date du 2023-08-14, choisissez les points de contrôle ControlNet spécifiques à SDXL selon le signal de contrôle, plutôt que de supposer qu'un point de contrôle ControlNet antérieur convient à SDXL. Utilisez OpenPose pour le guidage de pose et la profondeur pour le guidage par profondeur.

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

Nous n'avons pas recherché l'état actuel. La ligne de développement datée ci-dessus n'a pas encore été vérifiée auprès de sources de premier plan.

## Sources {#sources}

| source |
|---|
| https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md |
| https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0 |
| https://huggingface.co/diffusers/controlnet-sdxl-1.0 |
| https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0 |
| https://www.reddit.com/r/StableDiffusion/comments/15n6lso/comment/jvki53u/ |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:controlnet-sdxl`, fil `sdxl-controlnet-model-releases`, 3 événements datés du 2023-08-10 au 2023-08-14.
- **Note pratique :** À la date du 2023-08-14, les praticiens pouvaient choisir les points de contrôle ControlNet spécifiques à SDXL selon le signal de contrôle, notamment OpenPose pour le guidage de pose et la profondeur pour le guidage par profondeur, plutôt que de supposer qu'un point de contrôle ControlNet antérieur était approprié pour SDXL.
- **Confiance :** non recherché. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
