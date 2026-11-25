---
title: "Hyper-SD"
category: projects
date: 2024-08-28
tags: [hyper-sd, hyper_sd, project]
aliases: ["Hyper-SD"]
level: 2
source_sha256: 4a59d57496f629bdff7207b1e05ee4609fb6e70f505efa08197759c43cd0b356
translation: machine
translated_at: '2026-10-24'
---
# Hyper-SD {#hyper-sd}

**Ligne de développement :** `project:hyper-sd` · fil `hyper-sd`  
**Dernier événement :** 2024-08-28 · 2 datés depuis 2024-04-22 · **Recherché :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Hyper-SD — LoRA distillées et un seul UNet SDXL pour générer en un nombre réduit d'étapes, au lieu de l'échantillonnage multi-étapes habituel. — LoRA à N étapes pour SDXL, SD1.5, SD3 et FLUX.1-dev. — LoRA unifiée pour 1 à 8 étapes pour SDXL et SD1.5. — Exemples ControlNet et workflows ComfyUI prêts à l'emploi pour SDXL/SD1.5. Limite : ce n'est pas un modèle de base universel ; FLUX.1-dev et SD3 nécessitent un accès aux poids de base fermés. Conclusion : ne l'utiliser qu'avec une base prise en charge, nommée avec précision, et ne pas reporter les réglages vers de nouvelles familles de modèles sans vérification.

## Ligne de développement {#development-line}

- **2024-04-22 — Hyper-SD a publié ses premiers modèles publics et des démos interactives.** Le 2024-04-22, Hyper-SD a lancé un site de projet public et un dépôt de modèles, ainsi que des démonstrations interactives de text-to-image XL en une étape et de workflows guidés par scribble. Il s'agissait d'une étape de disponibilité publique du projet. Les ressources liées n'établissent pas à elles seules les détails d'entraînement, les résultats de benchmarks ni les versions exactes des publications.
- **2024-08-28 — Hyper-SD a ajouté des variantes de checkpoints LoRA pour FLUX.1-dev.** Le 2024-08-28, Hyper-SD a ajouté deux variantes de checkpoints LoRA pour FLUX.1-dev, correspondant à une génération en 8 étapes et en 16 étapes. Cela a étendu la ligne d'artefacts publics du projet à un workflow FLUX.1-dev. Les liens datés n'établissent ni la qualité ni la licence de ces checkpoints, ni s'ils ont remplacé les artefacts Hyper-SD antérieurs.

## Ce qui a changé {#what-changed}

Hyper-SD — une évolution allant de l'accélération de SDXL/SD1.5 vers quatre familles de modèles de base précises. — 2024-04-22 : des points d'entrée pratiques sont apparus : le dépôt de poids, Hyper-SDXL one-step text-to-image et Hyper-SD15 Scribble. — 2024-04-30 et 2024-05-13 [trouvé aujourd'hui] : ajout de LoRA CFG-preserved à 8 et 12 étapes pour SDXL et SD1.5, prévues pour un CFG de 5 à 8. — 2024-08-19 [trouvé aujourd'hui] : ajout de LoRA CFG pour SD3 à 4, 8 et 16 étapes. — 2024-08-28 : ajout des LoRA Hyper-FLUX.1-dev à 8 et 16 étapes ; la fiche officielle date leur disponibilité du 2024-08-26. — 2024-11-04 [trouvé aujourd'hui] : l'article a été mis à jour en v3 et accepté à NeurIPS 2024 ; aucun nouveau checkpoint n'est annoncé dans cette entrée. — 2026-09-04 [trouvé aujourd'hui] : la fiche officielle actuelle documente toujours FLUX.1-dev, SD3-Medium, SDXL Base 1.0 et SD v1.5, mais ne revendique la prise en charge d'aucune famille plus récente. Mesure : chacune des LoRA FLUX à 8 et 16 étapes vérifiées pèse 1,39 Go. Conclusion : le champ d'application pratique actuel est l'accélération de ces bases figées, et non un adaptateur général pour les nouveaux modèles de diffusion.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-04-22, les praticiens pouvaient évaluer Hyper-SD via ses ressources publiques de modèles et de démos. À partir du 2024-08-28, les praticiens travaillant avec FLUX.1-dev doivent sélectionner et tester la variante LoRA Hyper-SD à 8 ou 16 étapes, plutôt que de supposer que les anciens artefacts Hyper-SD s'appliquent sans modification.

1. Hyper-SD : choisissez exactement une base prise en charge et une LoRA de la même famille avec le nombre d'étapes voulu ; n'utilisez pas un seul fichier comme universel pour SDXL, SD1.5, SD3 et FLUX.
  — <https://huggingface.co/ByteDance/Hyper-SD>
2. Hyper-SD : pour FLUX.1-dev ou SD3, obtenez d'abord l'accès au modèle de base, puis chargez la LoRA via un pipeline Diffusers compatible, fusionnez-la (fuse) et déplacez le pipeline sur CUDA.
  — <https://huggingface.co/ByteDance/Hyper-SD>
3. Hyper-SD : commencez par les réglages officiels de la famille — pour FLUX.1-dev, utilisez un LoRA scale d'environ 0.125, 8 ou 16 étapes et un guidance de 3.5 ; pour SD3, utilisez un scale de 0.125 et un guidance de 3/5/7 à 4/8/16 étapes.
  — <https://huggingface.co/ByteDance/Hyper-SD>
4. Hyper-SD : pour les LoRA N-step SDXL/SD1.5, réglez DDIM avec timestep spacing trailing ; pour la LoRA unifiée, utilisez TCDScheduler et ajustez le nombre d'étapes avec eta.
  — <https://huggingface.co/ByteDance/Hyper-SD>
5. Hyper-SD : dans ComfyUI, importez le workflow correspondant à la famille de poids ; pour l'UNet SDXL à une étape, installez le custom scheduler fourni dans custom_nodes.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Bonnes pratiques {#best-practices}

- Hyper-SD : reproduisez d'abord la baseline officielle avec un prompt et le nombre d'étapes cible, puis seulement ensuite modifiez le LoRA scale, le CFG ou eta.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD : ne mélangez pas les approches de scheduler — les variantes N-step utilisent DDIM trailing, les variantes unifiées utilisent TCDScheduler.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD : avec ControlNet, conservez la même model family et la même recette de sampler que dans l'exemple officiel, plutôt que de reporter les réglages entre SDXL et SD1.5.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD : pour ComfyUI, prenez le workflow publié comme configuration de départ ; l'UNet SDXL à une étape sans le custom node de scheduler requis ne reproduit pas le mode timestep 800 annoncé.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Remplacé par ceci {#superseded-by-this}

- 2024-04-22 — la présentation de Hyper-SD uniquement comme accélérateur de SDXL/SD1.5 est devenue incomplète après les LoRA officielles pour SD3 du 2024-08-19 et pour FLUX.1-dev du 2024-08-26.
- 2024-04-22 — le report des réglages de la démo one-step vers toutes les bases n'est plus valable : les instructions officielles plus récentes séparent FLUX, SD3, SDXL et SD1.5 selon la LoRA, le scheduler, le CFG et le nombre d'étapes. Aucun checkpoint ancien n'est officiellement marqué comme déprécié.

## Points non confirmés {#still-unknown}

- La prise en charge officielle de Flux.1 Kontext, Flux.2, SD3.5, des checkpoints dérivés de SDXL et des versions actuelles de ComfyUI/Diffusers n'est pas confirmée.
- La fiche actuelle s'arrête à l'annonce de checkpoints du 2024-08-26 ; cela ne prouve pas l'arrêt du projet, mais aucune feuille de route plus récente n'a été trouvée.
- Les Espaces Hugging Face existent, mais leur bon fonctionnement sous la charge actuelle n'a pas été vérifié.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://hyper-sd.github.io/ | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD | ByteDance/Hyper-SD | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SDXL-1Step-T2I | Hyper SDXL 1Step T2I | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SD15-Scribble | Hyper SD15 Scribble | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-8steps-lora.safetensors | Hyper-FLUX.1-dev-8steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-16steps-lora.safetensors | Hyper-FLUX.1-dev-16steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui | ByteDance/Hyper-SD ComfyUI workflows | 2026-09-04 |
| https://arxiv.org/abs/2404.13686 | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:hyper-sd`, fil `hyper-sd`, 2 événements datés du 2024-04-22 au 2024-08-28.
- **Note pratique :** À partir du 2024-04-22, les praticiens pouvaient évaluer Hyper-SD via ses ressources publiques de modèles et de démos. À partir du 2024-08-28, les praticiens travaillant avec FLUX.1-dev doivent sélectionner et tester la variante LoRA Hyper-SD à 8 ou 16 étapes, plutôt que de supposer que les anciens artefacts Hyper-SD s'appliquent sans modification.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
