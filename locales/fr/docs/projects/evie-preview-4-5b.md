---
title: "EVIE-Preview-4.5B"
category: projects
date: 2026-08-18
tags: [evie-preview-4-5b, project, tencent/evie-preview-4.5b]
aliases: ["EVIE-Preview-4.5B"]
level: 2
source_sha256: ce9f47e87fd123f85a3ff14b8bd82ece33428129b5b58994dd8d7d93f14c9d7f
translation: machine
translated_at: '2026-10-24'
---
# EVIE-Preview-4.5B {#evie-preview-45b}

**Ligne de développement :** `project:evie-preview-4-5b` · fil `evie-preview-4-5b`  
**Dernier événement :** 2026-08-18 · 1 événement daté depuis le 2026-08-18 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

EVIE-Preview-4.5B est un modèle ouvert de 4,54B pour la recherche multilingue dans des scans, tableaux, graphiques et documents. Fonctionnalités : requête textuelle sur des images de pages ; recherche par MaxSim late-interaction ; requêtes en anglais, français, allemand, italien, espagnol, portugais et chinois. Limite : le point de contrôle BF16 occupe 8,5 GB, et un index de 1 million de pages nécessite 179,2 GiB avec 768 tokens visuels. Verdict : adapté à la recherche de documents visuels auto-hébergée, si l'équipe est prête à stocker un index multi-vecteurs et à exécuter une inférence CUDA.

## Ligne de développement {#development-line}

- **2026-08-18 — Références publiques datées pour EVIE-Preview-4.5B.** Point de contrôle de 4,54B pour la recherche de documents visuels, basé sur Qwen3.5-4B, avec des vecteurs de tokens de 128 dimensions et une licence Apache-2.0.

## Ce qui a changé {#what-changed}

2026-08-18 — publication d'EVIE-Preview-4.5B : point de contrôle de 4,54B pour la recherche de documents visuels, basé sur Qwen3.5-4B, avec des vecteurs de tokens de 128 dimensions et une licence Apache-2.0.

## Mode d'emploi {#how-to-use-this}

À compter du 2026-08-18, les praticiens peuvent commencer leur évaluation à partir des pages GitHub et Hugging Face liées d'EVIE-Preview-4.5B, en vérifiant directement auprès de ces sources les capacités, la licence et les conditions d'utilisation avant leur adoption.

1. Installez `colpali-engine>=0.3.15` et `accelerate` ; pour une exécution reproductible, utilisez les dépendances du dépôt.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
2. Chargez `ColQwen3_5` avec l'identifiant `tencent/EVIE-Preview-4.5B` en BF16 sur CUDA, ainsi que le processeur `ColQwen3_5Processor`.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
3. Avant de traiter les requêtes, activez l'attention bidirectionnelle pour les couches full-attention, et avant chaque forward de requête, réinitialisez `model.rope_deltas = None` ; calculez ensuite les scores MaxSim via `processor.score`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>
4. Pour une vérification par lots des pages, utilisez `infer.py` avec les arguments répétables `--query` et `--image`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>

## Bonnes pratiques {#best-practices}

- Commencez avec 768 tokens visuels par page : c'est le budget d'entraînement du modèle et une option d'index plus économique.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- N'utilisez pas les masques causaux standard : le code publié bascule explicitement les couches full-attention en mode bidirectionnel, sans quoi les résultats ne correspondent pas aux scores annoncés.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- Vérifiez la qualité sur vos propres documents et requêtes : les résultats annoncés concernent ViDoRe, et non un corpus d'entreprise quelconque.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- La date exacte et le contenu des modifications ultérieures du dépôt Hugging Face ne sont pas confirmés par une source primaire datée ; elles ne sont donc pas incluses dans new_events.
- Les affirmations de leadership sur ViDoRe proviennent de la model card ; cette fiche ne comporte pas de vérification indépendante de la reproduction des résultats.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Tencent/EVIE-Preview-4.5B | Tencent/EVIE-Preview-4.5B — code source et instructions de lancement | 2026-09-05 |
| https://huggingface.co/tencent/EVIE-Preview-4.5B | tencent/EVIE-Preview-4.5B — model card, paramètres, résultats et quick start | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:evie-preview-4-5b`, fil `evie-preview-4-5b`, 1 événement daté du 2026-08-18 au 2026-08-18.
- **Note pratique :** À compter du 2026-08-18, les praticiens peuvent commencer leur évaluation à partir des pages GitHub et Hugging Face liées d'EVIE-Preview-4.5B, en vérifiant directement auprès de ces sources les capacités, la licence et les conditions d'utilisation avant leur adoption.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font référence pour ce qui est obsolète.
