---
title: "Qwen2.5-Coder"
category: projects
date: 2024-11-12
tags: [project, qwen, qwen2-5-coder, qwen2-5-coder-launch]
aliases: ["Qwen2.5-Coder"]
level: 2
source_sha256: 7ceb0f41f470ef60dba2cbb23a93162ba9edb0e2104adff127c525b8a4816c40
translation: machine
translated_at: '2026-10-24'
---
# Qwen2.5-Coder {#qwen25-coder}

**Ligne de développement :** `project:qwen2-5-coder` · fil `qwen2-5-coder-launch`  
**Dernier événement :** 2024-11-12 · 2 événements datés depuis le 2024-11-12 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Qwen2.5-Coder est une famille de six LLM de code, en versions de base et ajustées aux instructions, allant de 0,5B à 32B, destinés à la complétion, au chat, à la réparation de code et au fine-tuning.

- Génération : génère du code.
- Raisonnement : raisonne sur des tâches de programmation.
- Réparation : corrige les bogues dans le code.
- Fill-in-the-middle : complète le code entre un préfixe et un suffixe.

Le contexte atteint jusqu'à 128K, mais la configuration standard fixe 32K.
La famille convient aux tâches locales et auto-hébergées, mais Qwen oriente le nouveau développement agentique vers Qwen3-Coder.

## Ligne de développement {#development-line}

- **2024-11-12 — Qwen a publié la famille de modèles Qwen2.5-Coder.** Aux tailles 1,5B et 7B déjà disponibles, Qwen a ajouté 0,5B, 3B, 14B et 32B, en versions base et instruct.
- **2024-11-12 — Qwen a mis à disposition une expérience Qwen2.5-Coder Artifacts.** Aux tailles 1,5B et 7B déjà disponibles, Qwen a ajouté 0,5B, 3B, 14B et 32B, en versions base et instruct.

## Évolutions {#what-changed}

2024-11-12 — Qwen a ouvert la gamme complète Qwen2.5-Coder : aux tailles 1,5B et 7B déjà disponibles, Qwen a ajouté 0,5B, 3B, 14B et 32B, en versions base et instruct. 2025-07-22 — Qwen a publié Qwen3-Coder comme génération suivante pour le codage agentique ; le dépôt original Qwen2.5-Coder redirige désormais vers celui-ci.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-11-12, les praticiens pouvaient évaluer Qwen2.5-Coder à travers sa collection de modèles publiée, sa démo, son dépôt et son expérience Artifacts, plutôt que de se limiter à une interface de chat générique.

1. Pour les tâches interactives, choisissez une variante instruct de taille adaptée, chargez le tokenizer et le modèle via Transformers, puis construisez la requête avec apply_chat_template.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
2. Pour une API auto-hébergée, servez le checkpoint choisi avec vLLM ; le serveur expose un point de terminaison /v1/chat/completions compatible OpenAI.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
3. Pour la complétion ou le FIM, utilisez le modèle de base ; pour un dialogue normal, utilisez Instruct plutôt que la version base.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Bonnes pratiques {#best-practices}

- N'utilisez pas les modèles de base pour la conversation sans post-entraînement spécifique ; choisissez Instruct pour un assistant.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>
- Activez YaRN uniquement lorsqu'un contexte supérieur à 32K est réellement nécessaire : la mise à l'échelle statique peut dégrader les requêtes courtes.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
- Mettez Transformers à jour vers au moins la version 4.37, sinon le chargement de l'architecture Qwen2 échoue avec KeyError.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Remplacé par {#superseded-by-this}

- 2025-07-22 — Qwen3-Coder est devenu la ligne actuelle de Qwen pour le codage agentique ; Qwen2.5-Coder reste un ensemble de checkpoints disponibles, mais son dépôt GitHub original redirige vers Qwen3-Coder.

## Points encore inconnus {#still-unknown}

- L'état actuel de l'espace public Qwen2.5-Coder-Artifacts est suspendu ; son historique de disponibilité et son aptitude à fonctionner comme produit opérationnel restent non confirmés.
- La licence du modèle 3B diffère : elle utilise la Qwen Research License, tandis que 0,5B, 1,5B, 7B, 14B et 32B utilisent Apache 2.0.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://qwenlm.github.io/blog/qwen2.5-coder-family/ | Qwen2.5-Coder Series: Powerful, Diverse, Practical. | 2026-09-05 |
| https://arxiv.org/abs/2409.12186 | Qwen2.5-Coder Technical Report | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-7B | Qwen/Qwen2.5-Coder-7B model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct | Qwen/Qwen2.5-Coder-32B-Instruct model card | 2026-09-05 |
| https://github.com/QwenLM/Qwen2.5-Coder | QwenLM/Qwen2.5-Coder repository redirect | 2026-09-05 |
| https://qwenlm.github.io/blog/qwen3-coder/ | Qwen3-Coder: Agentic Coding in the World | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:qwen2-5-coder`, fil `qwen2-5-coder-launch`, 2 événements datés du 2024-11-12 au 2024-11-12.
- **Note pratique :** À partir du 2024-11-12, les praticiens pouvaient évaluer Qwen2.5-Coder à travers sa collection de modèles publiée, sa démo, son dépôt et son expérience Artifacts, plutôt que de se limiter à une interface de chat générique.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
