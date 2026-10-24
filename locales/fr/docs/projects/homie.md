---
title: "HOMIE"
category: projects
date: 2026-07-22
tags: [homie, homie-public-project-release, project]
aliases: ["HOMIE"]
level: 2
source_sha256: 8d4da0547c83aa66ac0d43c325dd3db9d948953f977f8f70b3e814de0079cdb1
translation: machine
translated_at: '2026-10-24'
---
# HOMIE {#homie}

**Ligne de développement :** `project:homie` · fil `homie-public-project-release`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

HOMIE est un pipeline open source de génération de vidéos en local, piloté par des images de référence de personnes, de produits, de logos, de cartes OCR et de prises de vue multi-vues.

- Composition multi-sujets : combine plusieurs sujets distincts dans un même clip vidéo.
- Alignement multi-références : utilise plusieurs références d'un même sujet pour améliorer la précision du texte ou la cohérence du point de vue.

Son exécution nécessite Wan2.1-T2V-14B, des poids HOMIE distincts de 37,1 Go et Qwen3-VL-2B-Thinking.

Il s'agit d'une version de recherche pour l'inférence, et non d'un service cloud.

## Ligne de développement {#development-line}

- **2026-07-22 — Parution des ressources publiques du projet HOMIE.** Le 2026-07-22, le projet a relié entre eux son site web, son dépôt GitHub et sa page de modèle sur Hugging Face, homie-r2v-wan2.1. Ces liens donnent accès, au même endroit, à la documentation publique, au code source et à la distribution du modèle. Les affirmations précises sur la version, les capacités et la licence ne sont pas indiquées.

## Ce qui a changé {#what-changed}

2026-07-20 — Le rapport technique de HOMIE est paru sur arXiv, établissant une méthode unifiée de personnalisation vidéo inter-sujets et intra-sujet.

2026-07-21 — Le code d'inférence et les points de contrôle affinés à partir de Wan2.1-T2V-14B ont été publiés.

2026-07-22 — La page du projet, le code et les poids décrivaient un flux de travail local unique ; aucun changement de version distinct n'a été relevé ce jour-là.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-22, commencez par la page du projet, le dépôt source et la page de modèle Hugging Face indiqués. Vérifiez la documentation du projet, les prérequis et la licence avant toute utilisation.

1. Installez l'environnement à l'aide de `set_env.sh`. Cela nécessite PyTorch 2.4.0 ou une version plus récente avec une build CUDA compatible.
  — <https://github.com/YIYANGCAI/HOMIE>
2. Téléchargez Wan-AI/Wan2.1-T2V-14B-Diffusers, les poids `yychai/homie-r2v-wan2.1` et Qwen/Qwen3-VL-2B-Thinking dans les répertoires spécifiés.
  — <https://github.com/YIYANGCAI/HOMIE>
3. Créez un fichier JSONL : les listes externes de `reference_paths` séparent les sujets, et `prompt` décrit la vidéo.
  — <https://github.com/YIYANGCAI/HOMIE>
4. Exécutez `generate_mllm_feature.py`, puis transmettez le JSONL généré contenant les chemins `mllm_feature` à `generate.py`.
  — <https://github.com/YIYANGCAI/HOMIE>

## Bonnes pratiques {#best-practices}

- Ne sautez pas l'extraction des caractéristiques avec Qwen3-VL-2B-Thinking : l'inférence attend un JSONL contenant les chemins `mllm_feature` ajoutés.
  — <https://github.com/YIYANGCAI/HOMIE>
- Commencez par le mode mono-GPU documenté : 832×480, 97 images, 24 ips et un `base_seed` fixe. N'appliquez FSDP et le parallélisme de contexte que sur un nœud multi-GPU adapté.
  — <https://github.com/YIYANGCAI/HOMIE>
- Pour le parallélisme de contexte, utilisez l'exemple documenté de 8×A100 avec `ULYSSES_SIZE=8` et `RING_SIZE=1`. Il s'agit d'une configuration d'exemple, et non d'un minimum matériel officiel.
  — <https://github.com/YIYANGCAI/HOMIE>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Le dépôt ne comporte ni versions publiées ni journal des modifications : le commit ou les poids exacts correspondant à l'entrée du 2026-07-22 ne sont pas établis.
- La VRAM minimale officielle, les durées de génération et les configurations testées autres que l'exemple 8×A100 ne sont pas publiées.
- Le README actuel inclut un scénario de parallélisme de contexte, mais la source ne date pas son ajout ; il n'est donc pas répertorié comme événement daté distinct.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://yiyangcai.github.io/homie-page.github.io/ | HOMIE Demo Page | 2026-09-05 |
| https://github.com/YIYANGCAI/HOMIE | YIYANGCAI/HOMIE — code et instructions d'inférence | 2026-09-05 |
| https://huggingface.co/yychai/homie-r2v-wan2.1 | yychai/homie-r2v-wan2.1 | 2026-09-05 |
| https://arxiv.org/abs/2607.18217 | HOMIE: Human-object Centric Video Personalization via Multimodal Intelligent Enhancement | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:homie`, fil `homie-public-project-release`, 1 événement daté, 2026-07-22 → 2026-07-22.
- **Note pratique :** À partir du 2026-07-22, les praticiens qui évaluent HOMIE doivent commencer par la page du projet, le dépôt source et la page de modèle Hugging Face indiqués, puis valider la documentation du projet, les prérequis et la licence avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
