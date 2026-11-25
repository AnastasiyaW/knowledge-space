---
title: "TAPTR"
category: projects
date: 2024-12-13
tags: [project, taptr, taptr-public-availability]
aliases: ["TAPTR"]
level: 2
source_sha256: 99641a2dd85ca9c57142055db335cf230f0c90f3e710da4c883d57e0231ad7d8
translation: machine
translated_at: '2026-10-24'
---
# TAPTR {#taptr}

**Ligne de développement :** `project:taptr` · fil `taptr-public-availability`  
**Dernier événement :** 2024-12-13 · 2 événements datés depuis 2024-08-01 · **Consulté le :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

TAPTR est une approche fondée sur les transformeurs pour le Tracking Any Point, destinée aux développeurs d'outils vidéo, de reconstruction 3D et de suivi de masques.

- Entrée par points et régions : accepte des points ou une région englobante dans une image.
- Suivi de trajectoires : renvoie les trajectoires de points et les indicateurs de visibilité sur l'ensemble de la vidéo.
- Contexte spatio-temporel : TAPTRv3 ajoute un contexte spatial et temporel, avec récupération après les changements de plan.

La Space de démonstration plus ancienne, issue de la sélection initiale, est arrêtée.
Utilisez le code officiel de la version dont vous avez besoin plutôt que cette Space de démonstration.

## Ligne de développement {#development-line}

- **2024-08-01 — Ressources du projet TAPTR et démonstrations spécifiques à certaines tâches ajoutées.** Le 2024-08-01, une mise à jour a référencé le site du projet, le dépôt source et des démonstrations en ligne pour le montage vidéo et le suivi de trajectoires.
- **2024-12-13 — Une Space Hugging Face TAPTR a été ajoutée.** Le 2024-12-13, une mise à jour a référencé une Space Hugging Face nommée TAPTR, avec une référence source, comme point d'accès hébergé.

## Ce qui a changé {#what-changed}

- 2024-08-01 — TAPTRv1 était disponible sous forme d'implémentation ouverte de type DETR pour le suivi de points ; le code officiel avait été publié le 2024-07-16.
- 2024-12-13 — Une Space Hugging Face tierce est apparue pour TAPTR, plutôt qu'une publication officielle de modèle ; à la date de la relecture, la Space est arrêtée.
- 2026-02-10 — Le code de TAPTRv3 a été publié en tant que version actuelle pour les vidéos longues.

## Comment l'utiliser {#how-to-use-this}

À partir du 2024-08-01, les praticiens pouvaient trouver le code source public de TAPTR et les démonstrations spécifiques à certaines tâches via les liens du projet ; à partir du 2024-12-13, ils pouvaient également évaluer la Space Hugging Face référencée, après avoir vérifié sa propriété et sa version.

1. Ouvrez le dépôt officiel et sélectionnez v1, v2 ou v3 ; pour les nouvelles tâches sur vidéos longues, commencez par v3.
  — <https://github.com/IDEA-Research/TAPTR>
2. Suivez le README de votre version, fournissez des points ou une région échantillonnée dans la première image, puis enregistrez les coordonnées prédites avec leurs indicateurs de visibilité.
  — <https://github.com/IDEA-Research/TAPTR>
3. Pour le montage vidéo, échantillonnez des points à l'intérieur de la région à éditer et utilisez leurs trajectoires pour transférer la région d'une image à l'autre.
  — <https://arxiv.org/abs/2407.16291>

## Bonnes pratiques {#best-practices}

- Choisissez TAPTRv3 pour les clips longs et les changements de plan : il utilise Visibility-aware Long-Temporal Attention, Context-aware Cross Attention et une mise en correspondance globale pour détecter les changements de plan.
  — <https://taptr.github.io/>
- Ne bâtissez pas de flux de travail autour de la Space HYeungLee/TAPTR : elle est arrêtée à la date de la relecture.
  — <https://huggingface.co/spaces/HYeungLee/TAPTR>
- N'utilisez pas TAPTRv2 par défaut pour les vidéos longues : les auteurs signalent des performances insatisfaisantes de la v2 sur des durées importantes.
  — <https://github.com/IDEA-Research/TAPTR>

## Remplacé par {#superseded-by-this}

- 2024-07-24 — TAPTRv2 a remplacé le volume de coûts de TAPTRv1 par Attention-based Position Update ; choisir v1 pour la qualité maximale est obsolète.
- 2024-11-27 / 2026-02-10 — TAPTRv3 remplace v2 pour les vidéos longues : v2 reposait sur une modélisation de type RNN et peinait à extraire des caractéristiques sur de longues séquences ; le code de v3 a été publié le 2026-02-10.

## Points encore inconnus {#still-unknown}

- Les commandes d'installation exactes et les noms de tags de version du dépôt officiel n'ont pas été confirmés sur GitHub ; consultez le README de votre version avant tout déploiement.
- La Space Hugging Face de l'événement du 2024-12-13 est une démonstration tierce, et non une interface TAPTR officielle vérifiée.
- Deux entrées concernent la famille TAPTR, mais la première correspond à la publication de v1 et à ses démonstrations, tandis que la seconde est une Space tierce ; il s'agit de types d'événements distincts, et non de deux publications de modèles.
- Les liens vers les sources d'origine n'ont pas été utilisés comme preuves, le texte des messages n'étant pas disponible.
- L'article sur TAPTRv3 est paru le 2024-11-27, mais le code officiel n'a été publié que le 2026-02-10 ; avant cette date, il ne s'agissait pas d'une implémentation accessible.
- Les métriques de référence actuelles de v3 n'ont pas été agrégées : les sources revendiquent des performances à l'état de l'art, mais le choix des jeux de données exige une évaluation reproductible.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/IDEA-Research/TAPTR | IDEA-Research/TAPTR — implémentation officielle et chronologie des publications | 2026-09-05 |
| https://taptr.github.io/ | Page du projet TAPTR — vue d'ensemble de v1 à v3 | 2026-09-05 |
| https://huggingface.co/spaces/HYeungLee/TAPTR | Space Hugging Face HYeungLee/TAPTR | 2026-09-05 |
| https://arxiv.org/abs/2407.16291 | TAPTRv2: Attention-based Position Update Improves Tracking Any Point | 2026-09-05 |
| https://arxiv.org/abs/2411.18671 | TAPTRv3: Spatial and Temporal Context Foster Robust Tracking of Any Point in Long Video | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:taptr`, fil `taptr-public-availability`, 2 événements datés du 2024-08-01 au 2024-12-13.
- **Note pratique :** À partir du 2024-08-01, les praticiens pouvaient trouver le code source public de TAPTR et les démonstrations spécifiques à certaines tâches via ses liens de projet ; à partir du 2024-12-13, ils pouvaient également évaluer la Space Hugging Face référencée, en vérifiant d'abord sa propriété et sa version.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
