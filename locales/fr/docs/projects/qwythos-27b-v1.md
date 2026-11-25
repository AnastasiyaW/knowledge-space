---
title: "Qwythos-27B-v1"
category: projects
date: 2026-08-03
tags: [project, qwythos, qwythos-27b-v1, qwythos-27b-v1-release]
aliases: ["Qwythos-27B-v1"]
level: 2
source_sha256: 20404391aea59556952871101f6d9c9566ab31c161efaf2ad81f630de69199af
translation: machine
translated_at: '2026-10-24'
---
# Qwythos-27B-v1 {#qwythos-27b-v1}

**Ligne de développement :** `project:qwythos-27b-v1` · fil `qwythos-27b-v1-release`  
**Dernier événement :** 2026-08-03 · 1 événement daté depuis le 2026-08-03 · **Recherche :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Qwythos-27B-v1 est un checkpoint bf16 à poids ouverts basé sur Qwen3.5-27B, destiné aux développeurs qui ont besoin d'un modèle local avec appel de fonctions et entrée d'images.

- Fenêtre de contexte : fournit 1 048 576 tokens grâce à YaRN 4.0.
- Tour de vision et prédiction multi-tokens native : conservées depuis l'architecture de base.
- Pipeline de post-entraînement : SFT → DPO → ESFT complets en tant que v1, avant le RL.

La fenêtre native est de 262 144 tokens ; la configuration 1M dégrade la qualité sur les contextes courts.

Le checkpoint convient aux workflows d'agents et d'outils auto-hébergés, mais la tour de vision n'a pas été affinée et les déploiements sensibles nécessitent une revue externe.

## Ligne de développement {#development-line}

- **2026-08-03 — Qwythos-27B-v1 référencé sur Hugging Face.** Des tiers ont publié FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 et un brouillon MTP séparé ; il ne s'agit pas d'un nouveau checkpoint officiel.

## Ce qui a changé {#what-changed}

2026-07-29 — Empero a publié Qwythos-27B-v1 et un ensemble officiel de fichiers GGUF : un modèle de 27B à paramètres complets basé sur Qwen3.5-27B, sous licence Apache-2.0, avec un contexte de 1M, la vision et le MTP. 2026-08-03 — Des portages MLX tiers du Qwythos-27B-v1 de base sont apparus : FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 et un brouillon MTP séparé ; il ne s'agit pas d'un nouveau checkpoint officiel.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-03, les praticiens doivent utiliser la page de modèle Hugging Face liée comme référence enregistrée pour Qwythos-27B-v1, et vérifier sur cette page les détails de la fiche modèle et la disponibilité avant toute utilisation.

1. Pour un déploiement local sur GPU de 24 Go, commencez par le GGUF officiel Q4_K_M ; ajoutez `mmproj-Qwythos-27B-F16.gguf` pour l'entrée d'images.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
2. Pour Transformers, chargez `empero-ai/Qwythos-27B-v1` via `AutoModelForImageTextToText` et utilisez le template de chat intégré.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
3. Pour un service compatible OpenAI, lancez vLLM ou SGLang ; près de 1M de contexte, vLLM exige `VLLM_ALLOW_LONG_MAX_MODEL_LEN=1` et un `--max-model-len` explicite.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
4. Pour l'appel de fonctions, transmettez les définitions dans `tools=[...]` au template de chat intégré et gérez les blocs d'appel d'outil standard.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Bonnes pratiques {#best-practices}

- Pour l'usage agentique et les outils, commencez avec une température de 0,6, top_p 0,95, top_k 20, repetition_penalty 1,05 et un budget d'au moins 16 384 nouveaux tokens.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- Si le contexte 1M n'est pas nécessaire, abaissez le facteur YaRN à 2.0 pour environ 512k, ou revenez à la configuration native 262k pour une meilleure qualité sur les contextes courts.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- Pour les quantifications K-quants, choisissez le GGUF officiel : il conserve le chemin d'état Gated-DeltaNet sensible en Q8_0 ou plus, au lieu de le quantifier avec le reste des poids.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
- Ne servez pas le checkpoint non censuré à des utilisateurs sans politique applicative, revue et contrôles d'accès.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-03 : considérer cette date comme la sortie du Qwythos-27B-v1 de base est obsolète ; l'annonce principale date du 2026-07-29, tandis que le 3 août concerne des conversions MLX tierces.

## Points encore inconnus {#still-unknown}

- La fiche modèle officielle décrit la v1 et les projets pour RL-v2, mais les sources primaires ne confirment pas la sortie de Qwythos-27B-v2 au 2026-09-05.
- La liste du 3 août confirme les conversions MLX tierces, mais ne fournit aucune évaluation indépendante de la qualité, de la compatibilité ni des capacités préservées du modèle original.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/empero-ai/Qwythos-27B-v1 | empero-ai/Qwythos-27B-v1 · Hugging Face | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Aempero-ai%2FQwythos-27B-v1 | Modèles quantifiés pour empero-ai/Qwythos-27B-v1 – Hugging Face | 2026-09-05 |
| https://empero.org/writing/qwythos-27b-the-long-awaited-27b | Qwythos-27B-v1 : le 27B tant attendu — Empero | 2026-09-05 |
| https://huggingface.co/models?other=qwythos | Models – Hugging Face | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:qwythos-27b-v1`, fil `qwythos-27b-v1-release`, 1 événement daté du 2026-08-03 au 2026-08-03.
- **Note pratique :** À partir du 2026-08-03, les praticiens doivent utiliser la page de modèle Hugging Face liée comme référence enregistrée pour Qwythos-27B-v1, et vérifier sur cette page les détails de la fiche modèle et la disponibilité avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
