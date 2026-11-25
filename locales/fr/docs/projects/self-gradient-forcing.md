---
title: "Self Gradient Forcing"
category: projects
date: 2026-07-24
tags: [project, self-gradient-forcing, self-gradient-forcing-development, self_gradient_forcing]
aliases: ["Self Gradient Forcing"]
level: 2
source_sha256: 2dcb78d6c268b7b354d36306549df95cc123d0316db21fd361432994ad847dd5
translation: machine
translated_at: '2026-10-24'
---
# Self Gradient Forcing {#self-gradient-forcing}

**Ligne de développement :** `project:self-gradient-forcing` · fil `self-gradient-forcing-development`  
**Dernier événement :** 2026-07-24 · 1 événement daté depuis le 2026-07-24 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Self Gradient Forcing (SGF) est une méthode d'entraînement pour les modèles de diffusion vidéo autorégressifs. Elle rejoue le contexte auto-généré échantillonné afin que les pertes sur les images futures entraînent la mémoire KV causale, sans conserver les gradients à travers l'ensemble de la séquence de génération.

- Code et points de contrôle : construit sur les fondations Wan2.1 T2V 1.3B et 14B, dans les configurations framewise et chunkwise.
- Horizon : fenêtre d'entraînement de 5 secondes rapportée, avec des démonstrations et une évaluation s'étendant à 60 et 240 secondes.

Il faut l'utiliser comme implémentation de recherche pour l'extrapolation vidéo à long horizon, et non comme générateur vidéo hébergé prêt à l'emploi.

## Ligne de développement {#development-line}

- **2026-07-24 — Les ressources du projet Self Gradient Forcing ont été liées.** Le 2026-07-24, la page du projet, le dépôt GitHub et la page du modèle sur Hugging Face ont été ajoutés. Ils regroupent au même endroit la présentation du projet, le code et les poids du modèle. Ces liens ne permettent pas de savoir s'il s'agit d'une première publication, d'une mise à jour ou d'une autre étape technique.

## Ce qui a changé {#what-changed}

- 2026-07-22 — l'article a introduit une reconstruction en deux passes bornée, pour combler l'écart de gradient sur le contexte historique dans Self Forcing à cache gelé.
- 2026-07-23 — les auteurs ont publiquement diffusé l'article, le code d'inférence et d'entraînement, ainsi que les points de contrôle des modèles.
- 2026-07-24 — la page du projet, le dépôt et la collection de modèles liés ont rendu la publication facilement trouvable, en précisant les versions framewise et chunkwise plutôt qu'un point de contrôle générique unique.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-24, les utilisateurs peuvent s'appuyer sur la page du projet, le dépôt GitHub et la page Hugging Face liés pour retrouver la présentation publique, l'implémentation et les ressources de modèle de Self Gradient Forcing.

1. Créez un environnement Python 3.10, installez les dépendances du dépôt ainsi que FlashAttention, puis installez le projet en mode développement.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
2. Exécutez scripts/download_weights.sh ; il récupère les bases Wan2.1 T2V 1.3B/14B, les initialisations Causal-Forcing, les points de contrôle SGF et les prompts.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
3. Choisissez le mode de version correspondant et exécutez bash scripts/infer_self_gradient_forcing.sh framewise ou chunkwise ; utilisez la configuration et le point de contrôle correspondants.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
4. Pour l'entraînement ou l'adaptation, lancez le script d'entraînement framewise ou chunkwise correspondant et conservez la séparation rollout/reconstruction définie par SGF.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Bonnes pratiques {#best-practices}

- Évaluez le comportement à long horizon séparément des courts clips : l'article considère VBench sur 5 secondes comme un contrôle de cohérence et concentre la comparaison principale sur l'extrapolation à 60 et 240 secondes, où les erreurs de mémoire s'accumulent.
  — <https://arxiv.org/abs/2607.20368>
- Gardez la version, la configuration et le point de contrôle alignés : les variantes framewise et chunkwise utilisent des géométries de cache différentes et ne sont pas interchangeables.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
- Utilisez les poids EMA pour les points de contrôle publiés ou entraînés, sauf si vous comparez délibérément les poids bruts du générateur.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Remplacé par cette méthode {#superseded-by-this}

- 2026-07-22 — Self Forcing à cache gelé est remplacé par SGF uniquement pour le chemin de gradient du contexte manquant : SGF conserve la génération série sans gradient, mais reconstruit le calcul échantillonné afin que les pertes futures entraînent l'écriture en mémoire. Il ne s'agit pas d'une dépréciation générale de tous les workflows Self Forcing.

## Points encore inconnus {#still-unknown}

- Résultats indépendants : aucune reproduction externe ne couvre la qualité, le coût de calcul ou la compatibilité ; les gains annoncés à long horizon restent rapportés par les auteurs.
- Support en production : les documents de publication n'établissent pas de politique de support stable en production ni de service d'inférence maintenu.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2607.20368 | Self Gradient Forcing: Native Long Video Extrapolation | 2026-09-05 |
| https://github.com/zhuang2002/Self_Gradient_Forcing | zhuang2002/Self_Gradient_Forcing | 2026-09-05 |
| https://huggingface.co/JunhaoZhuang/Self_Gradient_Forcing | JunhaoZhuang/Self_Gradient_Forcing | 2026-09-05 |
| https://zhuang2002.github.io/SelfGradientForcing/ | Self Gradient Forcing: Native Long Video Extrapolation project page | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:self-gradient-forcing`, fil `self-gradient-forcing-development`, 1 événement daté du 2026-07-24 au 2026-07-24.
- **Note pratique :** Au 2026-07-24, les utilisateurs pouvaient s'appuyer sur la page du projet, le dépôt GitHub et la page Hugging Face liés pour retrouver la présentation publique, l'implémentation et la ressource de modèle de Self Gradient Forcing.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
