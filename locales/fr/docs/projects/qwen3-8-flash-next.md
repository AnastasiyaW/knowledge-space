---
title: "Qwen3.8-Flash-Next — Qwen"
category: projects
date: 2026-08-26
tags: [project, qwen, qwen3-8-flash-next]
aliases: ["Qwen3.8-Flash-Next"]
level: 3
source_sha256: 378eb01d21d8440e184eb41b127e3da6ac667a4eb078bd415d68b7676c742a1f
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.8-Flash-Next — Qwen {#qwen38-flash-next-qwen}

**Ligne de développement :** `project:qwen3-8-flash-next` · fil `qwen`  
**Dernier événement :** 2026-08-26 · 1 événement daté depuis le 2026-08-26 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Qwen3.8-Flash-Next : modèle MoE multimodal ouvert destiné aux développeurs qui ont besoin de vision+texte, de codage et de scénarios agentiques. — s'exécute via Transformers, vLLM, SGLang, TokenSpeed et llama.cpp; — utilise Gated DeltaNet, Qwen Sparse Attention, Gated Residual et des embeddings n-gram. 125B paramètres pour le modèle principal, 51B paramètres de tables d'embeddings n-gram et 6B paramètres actifs par token; l'exemple officiel de service définit un contexte de 262 144 tokens. Choix pratique pour les expérimentations avec des poids ouverts; pour une API managée en production, le Qwen3.8-Flash officiel est positionné séparément.

## Ligne de développement {#development-line}

- **2026-08-26 — Les ressources du projet Qwen3.8-Flash-Next ont été documentées.** Modèle MoE multimodal et aperçu précoce de l'architecture Qwen4.

## Ce qui a changé {#what-changed}

2026-08-26 — publication des poids ouverts de Qwen3.8-Flash-Next : modèle MoE multimodal et aperçu précoce de l'architecture Qwen4. 2026-08-31 — parution d'un rapport technique avec des ablations d'architecture, une évaluation de l'efficacité et de la stabilité de l'entraînement.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-26, les praticiens doivent vérifier Qwen3.8-Flash-Next via le dépôt source lié, les ressources d'hébergement de modèles et la démo avant de choisir un checkpoint ou une voie de déploiement.

1. Pour un prototype image+texte, chargez `Qwen/Qwen3.8-Flash-Next` via le pipeline Transformers `image-text-to-text` ou via `AutoProcessor` et `AutoModelForMultimodalLM`.
  — <https://huggingface.co/Qwen/Qwen3.8-Flash-Next>
2. Pour une API auto-hébergée compatible OpenAI, lancez vLLM; l'exemple officiel utilise tensor parallelism 4, `--max-model-len 262144`, reasoning parser `qwen3` et tool-call parser `qwen3_coder`.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
3. Si vous n'avez pas besoin de maintenir l'infrastructure pour les poids ouverts, utilisez Qwen Cloud : le Qwen3.8-Flash géré actuel est compatible avec les API OpenAI et Anthropic.
  — <https://www.qwencloud.com/>

## Bonnes pratiques {#best-practices}

- Pour lancer des tool calls, activez simultanément le reasoning parser `qwen3` et le tool-call parser `qwen3_coder`; sans eux, la recette de service officielle pour ce mode n'est pas fournie.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Sur Apple Silicon, utilisez mlx-vlm ou une quantification MLX prête à l'emploi; pour llama.cpp, choisissez des poids GGUF compatibles plutôt que le checkpoint source.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Ne reportez pas la limite de 262K de l'exemple auto-hébergé sur le modèle managé : Qwen Cloud annonce pour Qwen3.8-Flash un contexte de 1M.
  — <https://www.qwencloud.com/>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Pour l'événement du 2026-08-26 : le dépôt officiel date la sortie du 2026-08-26 et précise que les poids ouverts de Qwen3.8-Flash-Next sont publiés — un modèle MoE multimodal de 125B paramètres avec 6B paramètres actifs par token; source_date=2026-08-26; source_url=https://github.com/QwenLM/Qwen3.8-Flash-Next.
- Nouvel événement : 2026-08-31 — le rapport technique décrit 14 benchmarks de pré-entraînement : le modèle devance le prédécesseur 397B-A17B sur huit, et reste derrière sur les autres d'au plus 2,6 points, avec environ un tiers des paramètres actifs, un tiers des tokens d'entraînement et environ un neuvième des FLOPs; source_date=2026-08-31; source_url=https://arxiv.org/abs/2608.30320.
- La fiche modèle actuelle désigne Qwen3.8-Flash comme version production basée sur Flash-Next, avec 1M de contexte et des tools intégrés, mais n'indique pas la date de cette transition; elle ne peut pas être rattachée à l'événement du 2026-08-26 ni formalisée comme un supersedes daté.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/QwenLM/Qwen3.8-Flash-Next | QwenLM/Qwen3.8-Flash-Next | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-Flash-Next | Fiche modèle Qwen/Qwen3.8-Flash-Next | 2026-09-05 |
| https://arxiv.org/abs/2608.30320 | On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability | 2026-09-05 |
| https://www.qwencloud.com/ | QwenCloud — AI-Native Models, Tools & Apps Platform | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:qwen3-8-flash-next`, fil `qwen`, 1 événement daté du 2026-08-26 au 2026-08-26.
- **Note pratique :** Au 2026-08-26, les praticiens doivent vérifier Qwen3.8-Flash-Next via le dépôt source lié, les ressources d'hébergement de modèles et la démo avant de choisir un checkpoint ou une voie de déploiement.
- **Confiance :** élevée. Les supersedes datés ci-dessus font foi pour ce qui est obsolète.
