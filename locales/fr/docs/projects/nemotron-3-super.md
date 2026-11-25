---
title: "Nemotron 3 Super"
category: projects
date: 2026-03-12
tags: [llm_releases, nemotron-3-super, project]
aliases: ["Nemotron 3 Super"]
level: 3
source_sha256: a745d6398d81451ba8c56f9358c5aab8a14a7f8cbe70ffc96ebf6c682ef1fe3d
translation: machine
translated_at: '2026-10-24'
---
# Nemotron 3 Super {#nemotron-3-super}

**Ligne de développement :** `project:nemotron-3-super` · fil `nemotron-3-super`  
**Dernier événement :** 2026-03-12 · 1 daté depuis le 2026-03-12 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Nemotron 3 Super est un modèle MoE hybride Mamba-Transformer ouvert de NVIDIA, destiné aux équipes qui construisent des systèmes agentiques, de la programmation et des usages à long contexte. Capacités : raisonnement, appel d'outils, code, contexte jusqu'à 1 million de tokens. Mesures : 120 B paramètres au total, dont 12 B actifs ; les poids en BF16 occupent 247 GB. Verdict : adapté au service ou à l'intégration par API de grandes tâches agentiques, mais pas à un GPU local unique et courant.

## Ligne de développement {#development-line}

- **2026-03-12 — NVIDIA a annoncé Nemotron 3 Super.** 120B/12B actifs, Mamba-Transformer hybride Latent MoE avec MTP, fenêtre de 1M tokens, poids, jeux de données et recettes ouverts ; l'annonce initiale est datée du 2026-03-11, donc la date de l'événement correspond à l'apparition du lien et non à la date de publication par NVIDIA. Complément à cette étape : NVIDIA indique du RL dans 21 configurations d'environnements et plus de 1,2 million de rollouts.

## Ce qui a changé {#what-changed}

2026-03-12 — publication de NVIDIA-Nemotron-3-Super-120B-A12B : 120B/12B actifs, Mamba-Transformer hybride Latent MoE avec MTP, fenêtre de 1M tokens, poids, jeux de données et recettes ouverts ; l'annonce initiale est datée du 2026-03-11, donc la date de l'événement correspond à l'apparition du lien et non à la date de publication par NVIDIA. Complément à cette étape : NVIDIA indique du RL dans 21 configurations d'environnements et plus de 1,2 million de rollouts. 2026-03-25 — NVIDIA a signalé des corrections concernant force_nonempty_content en streaming et l'appel d'outils avec le parser qwen3coder dans vLLM et TensorRT-LLM ; pour anyOf, un appel d'outil doit renvoyer un objet et non une chaîne. Il s'agit d'une modification ultérieure distincte, et non d'une partie du lancement du 12 mars.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-12, les praticiens qui évaluent des modèles de raisonnement agentique devraient ajouter Nemotron 3 Super à leur liste restreinte d'évaluation et consulter les ressources liées (modèle et cookbook) pour juger de l'adéquation au déploiement ; cette branche non recherchée n'établit aucune conclusion sur les benchmarks ni sur les licences.

1. Pour un prototype local, téléchargez le checkpoint BF16 via Transformers avec trust_remote_code=True, ou lancez un serveur vLLM avec le nom du modèle ; interrogez-le via l'API compatible OpenAI /v1/chat/completions.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main>
2. Pour le codage agentique via OpenRouter, définissez le modèle nvidia/nemotron-3-super-120b-a12b:free et limitez le contexte et la sortie dans la configuration de l'agent.
  — <https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html>
3. Pour un entraînement ou une adaptation reproductible, utilisez le dépôt Nemotron, uv sync et le pipeline par étapes pretrain, SFT, RL et eval sur un cluster Slurm.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md>

## Bonnes pratiques {#best-practices}

- Pour Hopper, choisissez le checkpoint FP8 publié, et pour Blackwell, le NVFP4 ; ne transférez pas les attentes de performance de l'un à l'autre sans mesure sur votre propre matériel.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md>
- Si vous utilisez le parser d'outils qwen3coder ou le streaming, figez les versions corrigées : vLLM 0.18.0 ou une version TensorRT-LLM/NIM compatible, puis vérifiez la structure de l'appel d'outil anyOf dans un test d'intégration.
  — <https://github.com/NVIDIA-NeMo/Nemotron/discussions/124>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-25 — l'hypothèse antérieure selon laquelle force_nonempty_content en streaming fonctionne et que les appels anyOf de qwen3coder ont toujours une structure d'objet est obsolète : des versions de serveur corrigées sont nécessaires.
- 2026-03-12 — l'ancien Nemotron Super n'est plus la référence de performance ; il est remplacé par Nemotron 3 Super. NVIDIA annonce un débit supérieur à 5×, mais ce n'est pas une garantie universelle pour une autre configuration.

## Points restant inconnus {#still-unknown}

- Le schéma de réponse ne contient pas les champs event_findings et new_events requis par la tâche ; leurs faits sont conservés respectivement dans what_changed, en complément de l'événement du 2026-03-12, et comme date distincte du 2026-03-25.
- La disponibilité, les limites et les conditions de la voie gratuite d'OpenRouter n'ont pas été vérifiées au moment de l'utilisation ; elles peuvent changer.
- Le score PinchBench de 85,6 % est une affirmation de NVIDIA sur un benchmark précis, et non une garantie indépendante de qualité dans votre environnement agentique.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/ | Introducing Nemotron 3 Super: An Open Hybrid Mamba-Transformer MoE for Agentic Reasoning | 2026-09-05 |
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main | nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | 2026-09-05 |
| https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html | Nemotron 3 Super with Agentic Coding Tools | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md | Nemotron 3 Super Training Recipe | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md | Nemotron 3 Super Quantization | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/discussions/124 | Nemotron 3 Super Improvements and Fixes | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:nemotron-3-super`, fil `nemotron-3-super`, 1 événement daté du 2026-03-12 au 2026-03-12.
- **Note pratique :** À partir du 2026-03-12, les praticiens qui évaluent des modèles de raisonnement agentique devraient ajouter Nemotron 3 Super à leur liste restreinte d'évaluation et consulter les ressources liées (modèle et cookbook) pour juger de l'adéquation au déploiement ; cette branche non recherchée n'établit aucune conclusion sur les benchmarks ni sur les licences.
- **Confiance :** élevée. Les entrées « Remplacé par ceci » datées font autorité pour ce qui est obsolète.
