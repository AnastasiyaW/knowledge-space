---
title: "Attention linéaire causale par blocs"
description: "L'attention linéaire causale par blocs est le mécanisme d'entraînement de SANA-Video pour les longues vidéos, doté d'un état d'attention cumulatif de taille fixe ; ce n'est pas un module générique à brancher sur un tuilage d'images arbitraire ou sur des DiT."
category: architectures
tags: [sana-video, causal, kv-cache, temporal, linear-attention, long-video, diffusion-transformer]
aliases: ["BCLA", "Causal Linear Attention", "SANA-Video Attention"]
level: 2
source_sha256: 4154c0bd82035ea27bb0c4c5cffe1fe5adbc8954862c42d75bc516a323eba0a4
translation: machine
translated_at: '2026-10-24'
---
# Attention linéaire causale par blocs {#block-causal-linear-attention}

**Périmètre vérifié : 2026-09-04.** L'attention linéaire causale par blocs est le mécanisme de contexte long décrit pour SANA-Video. Elle découpe une vidéo en blocs ordonnés de façon causale et transmet un état d'attention linéaire cumulatif de taille fixe depuis les blocs précédents vers les blocs suivants. C'est un composant d'architecture entraîné, et non une recette de post-traitement applicable à des tuiles d'images arbitraires.

## Ce qu'utilise réellement SANA-Video {#what-sana-video-actually-uses}

SANA-Video étend la famille [[SANA]] de DiT linéaires à la vidéo, avec une gestion des positions temporelles et un Mix-FFN causal. Pour la génération de longues vidéos, l'article reformule l'attention linéaire causale afin qu'un bloc ait besoin de l'état d'attention cumulatif et des résumés de clés issus des blocs précédents, plutôt que d'un cache KV par token qui croît.

Le cache de taille constante fait partie d'une conception plus large et couplée :

- un objectif de diffusion autorégressive par blocs ordonnés ;
- un état d'attention linéaire causale accumulé sur les blocs précédents ;
- une gestion des positions temporelles à l'intérieur du modèle ;
- un Mix-FFN causal qui conserve également la dernière image du bloc précédent pour la convolution temporelle ;
- des procédures d'entraînement et de post-entraînement qui apprennent au modèle à fonctionner avec cet état.

La taille fixe du cache réduit la croissance mémoire associée à un cache de tokens long classique. Elle ne prouve pas à elle seule la qualité temporelle, ne rend pas causal un DiT générique, et ne dispense pas d'une évaluation aux frontières de blocs.

## Ne pas généraliser au tuilage d'images sans preuve {#do-not-generalize-it-to-image-tiling-without-evidence}

Le matériel source porte sur la génération de longues vidéos. Il ne valide ni un flux de travail à tuiles d'images balayées par lignes, ni une synthèse d'images haute résolution sans couture, ni un argument générique d'état causal pour des modèles de diffusion arbitraires.

Une implémentation qui injecte un état cumulatif dans un modèle d'image non modifié constitue une nouvelle expérimentation de recherche. Elle nécessite ses propres preuves d'entraînement et de compatibilité, son propre schéma de positions, son ordre de blocs et sa validation visuelle ; elle ne doit pas être présentée comme un comportement de SANA-Video.

## Contrat d'intégration {#integration-contract}

1. Choisir une version officielle de SANA et lire la documentation correspondante du modèle et de la configuration.
2. Utiliser ensemble le modèle, le VAE, le noyau d'attention, l'ordre des blocs et le point de contrôle déclarés par l'implémentation.
3. Garder une isolation d'état explicite : un flux de génération ne doit jamais réutiliser un cache provenant d'un autre prompt, d'une autre graine ou d'une autre vidéo.
4. Conserver les révisions du modèle et de la configuration, le prompt, la graine, le calendrier des blocs, la politique de gestion de l'état, la sortie et les journaux.
5. Tester de courts clips avant d'augmenter la durée, puis inspecter les frontières de blocs, la continuité du mouvement, l'identité des sujets et le respect du prompt.

La famille SANA évolue rapidement. Les versions ultérieures introduisent une attention hybride linéaire/softmax et des conceptions à résidus d'attention ; leurs performances ou leur API ne doivent donc pas être reportées rétroactivement sur le mécanisme original d'attention causale par blocs.

## Critères d'acceptation {#acceptance-checks}

| Question | Preuve |
|---|---|
| L'architecture prévue est-elle réellement active ? | configuration officielle correspondante, point de contrôle et trace d'exécution |
| Le cache est-il isolé et ordonné correctement ? | reçu d'état par exécution et rejeu déterministe |
| Les transitions sont-elles stables ? | revue séquentielle autour de chaque frontière de bloc généré |
| Le gain d'efficacité annoncé est-il réel pour cette version ? | mémoire et latence mesurées sur le matériel déclaré et la durée donnée |
| Fait-il mieux qu'une base plus simple ? | comparaison à même prompt avec une base non causale ou à contexte plus court |

## Références {#references}

- [Dépôt officiel de SANA](https://github.com/NVlabs/Sana)
- [Article SANA-Video](https://arxiv.org/abs/2509.24695)
- [Documentation de SANA-Video](https://nvlabs.github.io/Sana/docs/sana_video/)
- [Documentation de SANA-Video 2.0](https://nvlabs.github.io/Sana/docs/sana_video2/)
