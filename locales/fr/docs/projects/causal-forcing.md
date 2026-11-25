---
title: "Causal Forcing++"
category: projects
date: 2026-05-16
tags: [causal-forcing, causal_forcing, project]
aliases: ["Causal Forcing++"]
level: 2
source_sha256: 822add77089fb85e34b6515892dfba2d61831de1ea5de65210d2f9ac7fd6f762
translation: machine
translated_at: '2026-10-24'
---
# Causal Forcing++ {#causal-forcing}

**Ligne de développement :** `project:causal-forcing` · fil `causal-forcing`  
**Dernier événement :** 2026-05-16 · 1 événement daté depuis le 2026-05-16 · **Recherché le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Causal Forcing++ est un pipeline de recherche et une publication de modèle image par image destinés à la génération de vidéo à partir de texte et de vidéo à partir d'image à faible latence.

- Distillation par cohérence causale : remplace les trajectoires d'ODE causales précalculées avant la DMD asymétrique.
- Points de contrôle de référence : fournit des modèles image par image à 1 étape et à 2 étapes.
- Gains de performance : dépasse le Causal Forcing par blocs à 4 étapes dans les benchmarks de l'article, sans garantie de production.

## Ligne de développement {#development-line}

- **2026-05-16 — Les ressources publiques du projet Causal Forcing++ ont été enregistrées.** Le 2026-05-16, nous avons enregistré les liens vers le site, le dépôt source et le dépôt Hugging Face. Ces liens signalent des ressources publiques du projet, mais ne confirment aucune version, aucun résultat technique ni aucun flux d'utilisation précis.

## Ce qui a changé {#what-changed}

2026-05-16 — Causal Forcing++ a livré la distillation par cohérence causale, avec des points de contrôle ouverts image par image à 1 étape et à 2 étapes. L'historique du dépôt date la publication au 2026-05-15, soit après la soumission de la version 1 de l'article le 2026-05-14.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-05-16, les praticiens peuvent évaluer Causal Forcing++ via les emplacements liés du projet, du code source et du modèle. L'enregistrement daté seul ne justifie aucune affirmation précise sur le déploiement ou les performances.

1. Créez un environnement Python 3.10, puis installez les requirements, CLIP, FlashAttention et le paquet en mode éditable.
  — <https://github.com/thu-ml/Causal-Forcing>
2. Téléchargez un modèle de base Wan2.1 ainsi que `causal-forcing++/framewise-1step.pt` ou `framewise-2step.pt` depuis le dépôt de modèles.
  — <https://github.com/thu-ml/Causal-Forcing>
3. Exécutez `inference.py` avec les configurations image par image à 1 ou 2 étapes correspondantes et `--use_ema`. Utilisez le chemin image par image avec une image initiale pour l'I2V.
  — <https://github.com/thu-ml/Causal-Forcing>

## Bonnes pratiques {#best-practices}

- Testez l'inférence avec les points de contrôle publiés avant de lancer le pipeline d'entraînement en trois étapes.
  — <https://github.com/thu-ml/Causal-Forcing>
- Passez l'entraînement de BF16 à FP32 si la causal-CD ou la DMD diverge ou produit des images floues.
  — <https://github.com/thu-ml/Causal-Forcing>
- N'utilisez pas le modèle de base au-delà de 81 images ; utilisez Rolling Forcing pour les vidéos de l'ordre de la minute.
  — <https://github.com/thu-ml/Causal-Forcing>

## Remplacé par cette version {#superseded-by-this}

- 2026-05-15 — Causal Forcing++ remplace l'étape 2 basée sur l'ODE causale lors de l'initialisation de modèles à peu d'étapes sans sauvegarder les trajectoires ODE appariées.
- 2026-05-15 — Les points de contrôle image par image à 1 étape et à 2 étapes remplacent l'hypothèse selon laquelle Causal Forcing ne fonctionne que comme modèle par blocs à 4 étapes.

## Points encore inconnus {#still-unknown}

- Aucun journal d'événements distinct ni flux d'événements structuré n'est fourni pour la publication.
- La documentation officielle ne couvre que le code de recherche et les points de contrôle, sans guides de déploiement en production vérifiés ni configuration matérielle requise.

## Sources {#sources}

| Source | Titre | Consulté le |
|---|---|---|
| https://thu-ml.github.io/CausalForcing.github.io/ | Page du projet Causal Forcing | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing | Dépôt officiel thu-ml/Causal-Forcing et README | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing/commits/main | Historique des commits de Causal-Forcing | 2026-09-05 |
| https://huggingface.co/zhuhz22/Causal-Forcing/tree/main | Fichiers du modèle zhuhz22/Causal-Forcing | 2026-09-05 |
| https://arxiv.org/abs/2605.15141 | Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:causal-forcing`, fil `causal-forcing`, 1 événement daté du 2026-05-16 au 2026-05-16.
- **Note pratique :** À partir du 2026-05-16, les praticiens peuvent évaluer Causal Forcing++ via les emplacements liés du projet, du code source et du modèle ; l'enregistrement daté seul ne justifie aucune affirmation précise sur l'implémentation ou les performances.
- **Confiance :** élevée. Les remplacements datés ci-dessus indiquent ce qui est obsolète.
