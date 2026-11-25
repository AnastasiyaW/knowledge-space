---
title: "WAN 2.2 — WAN"
category: projects
date: 2025-07-28
tags: [project, wan, wan-2-2]
aliases: ["WAN 2.2"]
level: 2
source_sha256: 390a85cc8790999d45e8b971692e9f7079d6e301291c826ed04a3f142134aa12
translation: machine
translated_at: '2026-10-24'
---
# WAN 2.2 — WAN {#wan-22-wan}

**Ligne de développement :** `project:wan-2-2` · fil `wan`  
**Dernier événement :** 2025-07-28 · 2 événements datés depuis le 2025-07-28 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

WAN 2.2 est une gamme de modèles ouverts de diffusion vidéo destinés aux développeurs et aux créateurs : text-to-video, image-to-video, text-image-to-video, speech-to-video et animation de personnage. Limite : TI2V-5B est annoncé pour une résolution 720p à 24 fps ; T2V-A14B, dans l'exemple officiel mono-GPU, nécessite au moins 80 Go de VRAM. Verdict : pour du 720p sur du matériel limité, il est plus pratique de commencer par TI2V-5B, et de choisir A14B pour T2V/I2V lorsqu'on dispose d'un accès à une VRAM nettement plus importante.

## Ligne de développement {#development-line}

- **2025-07-28 — Publication officielle sur les réseaux sociaux de WAN enregistrée.** T2V-A14B, I2V-A14B et TI2V-5B ; le même jour, des intégrations dans ComfyUI, Diffusers et Space pour TI2V-5B sont apparues. Précision sur l'événement : A14B est une série MoE à deux experts, avec 27B de paramètres au total et environ 14B de paramètres actifs par étape ; TI2V-5B combine T2V et I2V grâce à un VAE avec une compression de 16×16×4.
- **2025-07-28 — Référence à la collection de modèles WAN enregistrée.** T2V-A14B, I2V-A14B et TI2V-5B ; le même jour, des intégrations dans ComfyUI, Diffusers et Space pour TI2V-5B sont apparues. Précision sur l'événement : A14B est une série MoE à deux experts, avec 27B de paramètres au total et environ 14B de paramètres actifs par étape ; TI2V-5B combine T2V et I2V grâce à un VAE avec une compression de 16×16×4.

## Modifications {#what-changed}

2025-07-28 — publication du code d'inférence et des poids de WAN 2.2 : T2V-A14B, I2V-A14B et TI2V-5B ; le même jour, des intégrations dans ComfyUI, Diffusers et Space pour TI2V-5B sont apparues. Précision sur l'événement : A14B est une série MoE à deux experts, avec 27B de paramètres au total et environ 14B de paramètres actifs par étape ; TI2V-5B combine T2V et I2V grâce à un VAE avec une compression de 16×16×4. 2025-08-26 — ajout de Wan2.2-S2V-14B : génération de vidéo à partir d'une image et d'un audio, avec poids, code et rapport technique. 2025-09-05 — ajout de la prise en charge de la synthèse vocale CosyVoice pour speech-to-video. 2025-09-19 — ajout de Wan2.2-Animate-14B pour l'animation et le remplacement de personnage à partir du mouvement et de l'expression. 2025-11-13 — Wan2.2-Animate-14B intégré à Diffusers. Ces nouvelles étapes élargissent la famille ; elles ne précisent pas l'événement du 2025-07-28.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2025-07-28, les praticiens doivent consulter la collection de modèles officielle Wan-AI sur Hugging Face ainsi que la mise à jour officielle de WAN citée lorsqu'ils recherchent les artefacts de WAN 2.2 ; les seuls liens datés disponibles n'établissent pas à eux seuls l'existence d'un modèle, d'une capacité ou d'une modification de workflow particulière.

1. Clonez le dépôt officiel, installez les dépendances avec PyTorch 2.4 ou une version ultérieure, puis téléchargez le checkpoint voulu via la CLI Hugging Face.
  — <https://github.com/Wan-Video/Wan2.2>
2. Pour text-to-video, choisissez Wan2.2-T2V-A14B ; pour image-to-video, I2V-A14B ; pour le mode mixte T2V/I2V en 720p, TI2V-5B.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
3. Lancez generate.py avec le `--task`, le `--ckpt_dir`, la taille et le prompt correspondants ; pour le multi-GPU, utilisez le lancement documenté avec torchrun, FSDP et Ulysses.
  — <https://github.com/Wan-Video/Wan2.2>

## Bonnes pratiques {#best-practices}

- Commencez par un lancement de base sans extension du prompt, puis ajoutez l'extension uniquement si nécessaire ; le projet officiel prend en charge DashScope et Qwen en local.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
- En cas de manque de mémoire, activez `--offload_model True`, `--convert_model_dtype` et, si besoin, `--t5_cpu` ; ce sont les mesures officiellement recommandées contre les OOM.
  — <https://github.com/Wan-Video/Wan2.2>
- Pour speech-to-video, installez le fichier supplémentaire requirements_s2v.txt ; ne partez pas du principe que le requirements.txt de base contient CosyVoice.
  — <https://github.com/Wan-Video/Wan2.2>

## Remplacé par ce qui suit {#superseded-by-this}

- 2025-07-28 — considérer Wan 2.1 comme la gamme ouverte de base actuelle de Wan n'est plus valable pour les tâches T2V, I2V et TI2V : WAN 2.2 l'a remplacée en tant que gamme principale suivante publiée.
- 2025-11-13 — la recommandation précédente d'utiliser Wan2.2-Animate-14B uniquement via son code propre est obsolète pour les utilisateurs de Diffusers : une intégration officiellement documentée est désormais disponible.

## Points non élucidés {#still-unknown}

- Le corps du message X n'était pas accessible lors de la vérification ; il n'est donc pas possible d'attribuer de façon fiable à ce message une affirmation plus précise que la date et l'URL de l'événement source.
- La page Hugging Face répertoriant les modèles reflète l'état actuel de l'organisation, mais ne donne pas la date de publication initiale de chaque checkpoint.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/Wan-Video/Wan2.2 | Wan-Video/Wan2.2 — dépôt officiel et guide d'utilisation | 2026-09-05 |
| https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B | Wan-AI/Wan2.2-T2V-A14B — fiche officielle du modèle | 2026-09-05 |
| https://huggingface.co/Wan-AI/models | Wan-AI — collection de modèles Hugging Face | 2026-09-05 |
| https://x.com/Alibaba_Wan/status/1949332715071037862 | Message X officiel d'Alibaba Wan lié à l'événement du 2025-07-28 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:wan-2-2`, fil `wan`, 2 événements datés du 2025-07-28 au 2025-07-28.
- **Note pratique :** Depuis le 2025-07-28, les praticiens doivent consulter la collection de modèles officielle Wan-AI sur Hugging Face ainsi que la mise à jour officielle de WAN citée lorsqu'ils recherchent les artefacts de WAN 2.2 ; les seuls liens datés disponibles n'établissent pas à eux seuls l'existence d'un modèle, d'une capacité ou d'une modification de workflow particulière.
- **Confiance :** moyenne. Les entrées datées de remplacement ci-dessus font foi pour ce qui est obsolète.
