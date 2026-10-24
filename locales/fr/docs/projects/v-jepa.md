---
title: "V-JEPA"
category: projects
date: 2026-03-20
tags: [project, v-jepa]
aliases: ["V-JEPA"]
level: 2
source_sha256: 78a744eb9d05bf488c78c7d804b5fbd19279d2f16eabc5dbf7515509d3c5f4d4
translation: machine
translated_at: '2026-10-24'
---
# V-JEPA {#v-jepa}

**Ligne de développement :** `project:v-jepa` · fil `v-jepa`  
**Dernier événement :** 2026-03-20 · 1 événement daté depuis le 2026-03-20 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

V-JEPA est une famille de modèles PyTorch de Meta destinés aux développeurs en video understanding et en robotique. — elle extrait des représentations à partir de vidéos sans annotation manuelle ; — elle prédit des actions et des états dans un espace latent ; — V-JEPA 2-AC ajoute une planification conditionnée par les actions pour les manipulateurs ; — V-JEPA 2.1 est orientée vers des features denses, cohérentes dans l'espace et dans le temps. La gamme 2.1 comprend ViT-B (80 M paramètres), ViT-L (300 M), ViT-g (1 B) et ViT-G (2 B), à 384 px. Verdict : pour les nouvelles tâches de segmentation, d'estimation de profondeur, de suivi et de features vidéo, il convient de commencer avec V-JEPA 2.1 ; 2-AC n'est nécessaire que pour reproduire la boucle de robotique de recherche.

## Ligne de développement {#development-line}

- **2026-03-20 — V-JEPA a été liée au dépôt V-JEPA 2.** Famille d'encodeurs denses vidéo/image avec Dense Predictive Loss, deep self-supervision et multimodal tokenizers ; l'annonce initiale dans le README est datée du 2026-03-16, l'article a été publié le 2026-03-15.

## Ce qui a changé {#what-changed}

2026-03-20 — V-JEPA 2.1 était disponible dans le dépôt V-JEPA : famille d'encodeurs denses vidéo/image avec Dense Predictive Loss, deep self-supervision et multimodal tokenizers ; l'annonce initiale dans le README est datée du 2026-03-16, l'article a été publié le 2026-03-15. 2025-06-11 — Meta a présenté V-JEPA 2, un video world model de 1,2 B paramètres, ainsi que V-JEPA 2-AC : une variante conditionnée par les actions, affinée sur moins de 62 heures de vidéos non annotées de DROID, pour du pick-and-place en zero-shot. 2026-03-15 — l'article V-JEPA 2.1 a ajouté quatre tailles de checkpoints, de 80 M à 2 B, et a annoncé une amélioration des tâches denses, notamment 0,307 RMSE sur NYUv2 et 77,7 % sur Something-Something-V2.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-03-20, les praticiens doivent considérer le dépôt facebookresearch/vjepa2 lié comme la référence d'implémentation documentée de cette ligne V-JEPA ; les seules preuves consignées ne justifient pas de recommandations opérationnelles au-delà de cela.

1. Installez PyTorch, timm et einops ; pour une exécution locale, une version de PyTorch avec CUDA est préférable.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
2. Chargez le préprocesseur et le backbone 2.1 souhaité via torch.hub ; pour une ressource plus légère, commencez par vjepa2_1_vit_base_384, pour une qualité maximale, par gigantic.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
3. Faites passer vos vidéos dans l'encodeur et entraînez une tête légère ou un linear probe pour votre tâche en aval ; la démo fournie montre l'inférence sur une vidéo.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
4. Pour une expérience de robotique, utilisez V-JEPA 2-AC avec des image goals et du model-predictive control ; il s'agit d'un checkpoint conditionné par les actions distinct, et non d'un encodeur 2.1 classique.
  — <https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/>

## Bonnes pratiques {#best-practices}

- Privilégiez V-JEPA 2.1 pour les représentations denses : la version modifie explicitement l'objectif et le tokenizer afin d'améliorer la cohérence spatio-temporelle, et ne se contente pas d'agrandir le modèle.
  — <https://arxiv.org/abs/2603.14482>
- Adaptez la taille du checkpoint à la tâche et aux ressources : les variantes 2.1 de 80 M, 300 M, 1 B et 2 B sont disponibles à 384 px.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
- Sous macOS, remplacez decord au préalable : le paquet de base ne prend pas en charge macOS, et les auteurs n'imposent pas un fork recommandé unique.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>

## Ce qui est rendu caduc {#superseded-by-this}

- 2026-03-15 — pour les nouvelles tâches de représentation dense vidéo/image, l'ancienne V-JEPA 2 n'est pas le point de départ à privilégier : V-JEPA 2.1 a été publiée précisément pour améliorer les features denses et cohérentes dans le temps.
- 2026-03-15 — V-JEPA 2.1 ne doit pas être considérée comme un nouveau checkpoint de robotique conditionné par les actions : V-JEPA 2-AC reste une branche de post-entraînement distincte de V-JEPA 2.

## Points encore inconnus {#still-unknown}

- Le dépôt officiel ne publie pas de GitHub Releases ; la datation de l'étape du 2026-03-20 est confirmée par la présence de V-JEPA 2.1 dans le dépôt, mais les dates initiales de l'article et du README sont respectivement le 2026-03-15 et le 2026-03-16.
- Les instructions officielles indiquent PyTorch Hub pour V-JEPA 2.1, mais l'exemple Transformers du README ne mentionne que les dépôts V-JEPA 2 ; la prise en charge de la 2.1 par cette voie n'est pas confirmée par le README.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/facebookresearch/vjepa2 | facebookresearch/vjepa2 — dépôt officiel | 2026-09-05 |
| https://github.com/facebookresearch/vjepa2/blob/main/README.md | README du dépôt V-JEPA 2 | 2026-09-05 |
| https://arxiv.org/abs/2603.14482 | V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning | 2026-09-05 |
| https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/ | Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning | 2026-09-05 |
| https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/ | V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:v-jepa`, fil `v-jepa`, 1 événement daté, du 2026-03-20 au 2026-03-20.
- **Remarque pratique :** Depuis le 2026-03-20, les praticiens doivent considérer le dépôt facebookresearch/vjepa2 lié comme la référence d'implémentation documentée de cette ligne V-JEPA ; les seules preuves consignées ne justifient pas de recommandations opérationnelles au-delà de cela.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
