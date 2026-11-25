---
title: "MAGI-2"
category: projects
date: 2026-08-07
tags: [magi, magi-2, magi-2-preview, project]
aliases: ["MAGI-2"]
level: 2
source_sha256: f35d9cc563890a4d8aff7689c00ed212c62b75c7a4f2db5762b478bf67aefe7f
translation: machine
translated_at: '2026-10-24'
---
# MAGI-2 {#magi-2}

**Ligne de développement :** `project:magi-2` · fil `magi-2-preview`  
**Dernier événement :** 2026-08-07 · 1 événement daté depuis le 2026-08-07 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

MAGI-2 Preview est un modèle MoE unifié audio-vidéo de 114 B de paramètres, destiné aux équipes qui génèrent localement, à partir de texte ou d'images, des clips de 10 secondes avec un son synchronisé.

- T2V crée une vidéo à partir de prompts textuels avec un audio conjoint.
- I2V anime une première image pour produire une vidéo avec un audio conjoint.
- Un pipeline en deux étapes génère un aperçu, puis affine la sortie jusqu'en 1080p.

Le modèle utilise 6 B de paramètres actifs par token, environ 307 Go de poids et huit GPU Hopper. Il s'agit d'une version preview ouverte et lourde en infrastructure, et non d'un outil d'API léger.

## Ligne de développement {#development-line}

- **2026-08-07 — Sand AI publie les supports de MAGI-2 preview.** Le modèle compte 114 B de paramètres, dont environ 6 B actifs par token, sur une architecture audio-vidéo unifiée MagiMoE. La documentation du dépôt limite la version à des clips de 10 secondes, à une étape de preview avec un affineur allant jusqu'en 1080p, ainsi qu'à T2V et I2V avec son synchronisé.

## Changements {#what-changed}

2026-08-07 — MAGI-2 Preview devient disponible avec les poids et le code d'inférence. Les sources primaires de Sand AI, publiées le 2026-08-05, précisent l'échelle : 114 B de paramètres, environ 6 B actifs par token, et une architecture audio-vidéo unifiée MagiMoE. La documentation du dépôt limite la version à des clips de 10 secondes, à une étape de preview et un affineur allant jusqu'en 1080p, ainsi qu'à T2V et I2V avec son.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-07, les praticiens doivent considérer MAGI-2 comme un projet de Sand AI en preview publique et consulter le dépôt, la page du modèle et la documentation de l'API v2 liés avant de l'évaluer ou de l'intégrer ; les capacités précises et les conditions d'accès restent à vérifier directement.

1. Préparez un environnement Linux avec Python 3.12, une version récente de CUDA, ffmpeg et huit GPU NVIDIA Hopper, comme l'exige le code d'inférence.
  — <https://github.com/SandAI-org/MAGI-2-preview>
2. Téléchargez l'image Docker ou compilez à partir des sources. Spécifiez le tag d'image correspondant au commit plutôt que d'utiliser `latest`, afin de garantir la reproductibilité.
  — <https://github.com/SandAI-org/MAGI-2-preview>
3. Téléchargez l'ensemble complet des checkpoints depuis sand-ai/MAGI-2-preview dans le dossier ckpt, sans renommer les répertoires.
  — <https://huggingface.co/sand-ai/MAGI-2-preview>
4. Lancez T2V avec un prompt textuel, ou I2V avec un prompt et une première image. La sortie est un clip de 10 secondes ; le 1080p passe par la preview et l'affineur.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Bonnes pratiques {#best-practices}

- Épinglez le tag Docker sur un commit précis et consignez-le avec les résultats, car `latest` évolue.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Conservez le déchargement par étapes par défaut pour la preview et l'affineur en 1080p, car les deux composants et les activations ne tiennent pas ensemble, même sur un GPU de 80 Go.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Utilisez l'expansion structurée du prompt pour la scène complète de 10 secondes lorsqu'un prompt manuel ne précise pas l'action, le cadrage et l'audio.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-05 — MAGI-2 Preview n'est remplacé par aucune version ultérieure distincte et datée dans les sources primaires vérifiées ; la documentation indique que la variante distillée est annoncée pour bientôt.
- 2026-08-07 — L'hypothèse selon laquelle MAGI-2 serait un produit d'API public prêt à l'emploi est obsolète : l'implémentation vérifiée fournit des poids ouverts et un code d'inférence avec des exigences de cluster.

## Points non élucidés {#still-unknown}

- L'URL https://platform.sand.ai/docs/api-v2 n'a renvoyé aucune documentation lisible lors de la vérification ; les fonctionnalités de l'API, les tarifs, les limites et la disponibilité actuelle restent donc non confirmés.
- Les sources primaires vérifiées ne fournissent aucun événement distinct daté après le 2026-08-07 ; les modifications du README actuel ne peuvent pas être datées de manière fiable comme une nouvelle version.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://sand.ai/blog/magi-2-preview | MAGI-2 Preview: Scaling Video Generation Models Efficiently | 2026-09-05 |
| https://github.com/SandAI-org/MAGI-2-preview | SandAI-org/MAGI-2-preview | 2026-09-05 |
| https://huggingface.co/sand-ai/MAGI-2-preview | sand-ai/MAGI-2-preview | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:magi-2`, fil `magi-2-preview`, 1 événement daté, du 2026-08-07 au 2026-08-07.
- **Remarque pratique :** Au 2026-08-07, les praticiens doivent considérer MAGI-2 comme un projet de Sand AI en preview publique et consulter le dépôt, la page du modèle et la documentation de l'API v2 liés avant de l'évaluer ou de l'intégrer ; les capacités précises et les conditions d'accès restent à vérifier directement.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
