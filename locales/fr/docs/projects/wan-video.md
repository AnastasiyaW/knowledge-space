---
title: "Wan Video"
category: projects
date: 2025-09-01
tags: [project, wan-video, wan-video-development, wan_video]
aliases: ["Wan 2.2", "Wan Video"]
level: 2
source_sha256: 839278044f2b89af3a796d607088173f82d36c9a03a47c669ec8ee9b7fe91fe8
translation: machine
translated_at: '2026-10-24'
---
# Wan Video {#wan-video}

**Ligne de développement :** `project:wan-video` · fil `wan-video-development`  
**Dernier événement :** 2025-09-01 · 2 entrées datées depuis 2025-04-23 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Wan Video est une famille de modèles open source d'Alibaba dédiée à la génération et à la transformation de vidéos.

- T2V : génère une vidéo à partir de prompts textuels.
- I2V : anime des images fixes en vidéo.
- TI2V : génère une vidéo à partir d'entrées combinant texte et image.
- Speech-to-video : génère une vidéo pilotée par un signal audio de parole.
- Animation et remplacement de personnages : anime des silhouettes humaines et remplace des personnages dans une vidéo.

TI2V-5B fonctionne en 720p sur un seul GPU disposant de 24 Go de VRAM ; les modèles A14B nécessitent au minimum 80 Go de VRAM en mode mono-GPU. Il s'agit d'une pile locale pratique pour la génération vidéo contrôlée, où le poids du modèle et la VRAM déterminent le chemin d'exécution.

## Ligne de développement {#development-line}

- **2025-04-23 — Wan Video a ouvert un flux public de création vidéo.** Le 2025-04-23, une page officielle de wan.video renvoyait les utilisateurs vers une interface de création vidéo. La page seule ne permet pas de savoir s'il s'agissait d'un lancement, d'une mise à jour ou d'un outil préexistant.
- **2025-09-01 — Wan 2.2 a reçu un LoRA de caméra en orbite.** Le 2025-09-01, un dépôt Hugging Face a publié un LoRA Wan 2.2 I2V 14B pour les mouvements de caméra en orbite. Le dépôt ne précise ni le statut officiel ni la compatibilité avec les environnements testés.

## Changements {#what-changed}

Le 2025-04-23, l'URL menait à l'interface web de Wan. L'adresse actuelle redirige directement vers le générateur, mais les sources ne rattachent pas cette date à une sortie indépendante de modèle. Le 2025-09-01, un LoRA communautaire pour les mouvements de caméra en orbite sur Wan2.2-I2V-A14B est apparu. L'historique des commits du dépôt montre que les fichiers ont été ajoutés le 2025-08-20 ; le 1er septembre n'est donc pas la date de sortie de cet adaptateur.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-04-23, les praticiens peuvent considérer Wan Video comme un flux public de création vidéo ; à partir du 2025-09-01, ils peuvent évaluer un LoRA spécialisé Wan 2.2 I2V 14B pour les plans en orbite lorsque le mouvement de caméra en orbite est nécessaire, après avoir vérifié la compatibilité.

1. Choisissez TI2V-5B pour un modèle 720p unique couvrant T2V et I2V sur un GPU de 24 Go de VRAM ; téléchargez le checkpoint et exécutez `generate.py` avec `--task ti2v-5B`.
  — <https://github.com/Wan-Video/Wan2.2>
2. Utilisez Wan2.2-I2V-A14B pour de l'I2V en 480p ou 720p avec une image d'entrée et un prompt ; la résolution cible définit la surface en pixels, tandis que le rapport d'aspect provient de l'image d'entrée.
  — <https://github.com/Wan-Video/Wan2.2>
3. Chargez les deux adaptateurs dans Diffusers au-dessus de `Wan-AI/Wan2.2-I2V-A14B` pour contrôler l'orbite de la caméra, puis rattachez-les au pipeline I2V.
  — <https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora>
4. Fournissez à Diffusers une image de référence ainsi que les caractéristiques de pose et de visage extraites pour l'animation de personnages ; une vidéo brute n'est pas une entrée valide du pipeline.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Bonnes pratiques {#best-practices}

- Commencez par TI2V-5B si vous disposez d'un seul GPU grand public ; prévoyez au moins 80 Go de VRAM ou un cluster distribué pour A14B.
  — <https://github.com/Wan-Video/Wan2.2>
- Activez `--offload_model True`, `--convert_model_dtype` et `--t5_cpu` en cas d'erreurs OOM, pour échanger de la vitesse d'exécution contre une moindre consommation mémoire.
  — <https://github.com/Wan-Video/Wan2.2>
- Choisissez délibérément l'expansion des prompts : Qwen en local évite les appels externes, alors que DashScope exige une clé API et une dépendance distante.
  — <https://github.com/Wan-Video/Wan2.2>
- Extrayez les points clés de pose et les caractéristiques faciales avec les scripts de prétraitement par défaut pour Wan-Animate ; ne transmettez jamais directement des fichiers vidéo bruts.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Remplacé par {#superseded-by-this}

- 2025-07-28 : Wan2.2 a remplacé Wan2.1 comme base open source principale pour les nouvelles tâches T2V, I2V et TI2V ; Wan2.1 reste maintenu pour VACE et FLF2V.
- 2025-09-19 : Wan2.2-Animate-14B a remplacé les pipelines externes comme voie officielle de Wan pour l'animation et le remplacement de personnages.

## Points restant inconnus {#still-unknown}

- La source primaire n'explique pas ce qui a changé dans l'interface web le 2025-04-23.
- Orbit Shot LoRA est un adaptateur tiers et non une version officielle de Wan ; sa fiche modèle indique Text-to-Image alors qu'il cible Wan2.2 I2V.
- Les journaux de test ne vérifient pas la compatibilité exacte entre les deux fichiers LoRA et des versions précises de Diffusers ou des wrappers d'interface.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://wan.video/wanxiang/videoCreation | Wan AI : modèle de référence de génération vidéo par IA | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora | ostris/wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora/commits/main | Historique des commits de wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.1 | Wan2.1 | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 | 2026-09-05 |
| https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan | Pipelines Wan — documentation Diffusers | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:wan-video`, fil `wan-video-development`, 2 événements datés du 2025-04-23 au 2025-09-01.
- **Note pratique :** À partir du 2025-04-23, les praticiens peuvent considérer Wan Video comme un flux public de création vidéo ; à partir du 2025-09-01, ils peuvent évaluer un LoRA spécialisé Wan 2.2 I2V 14B pour les plans en orbite lorsque le mouvement de caméra en orbite est nécessaire, après avoir vérifié la compatibilité.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
