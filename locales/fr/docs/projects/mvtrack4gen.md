---
title: "MVTrack4Gen"
category: projects
date: 2026-06-26
tags: [mvtrack4gen, mvtrack4gen-development, project]
aliases: ["MVTrack4Gen"]
level: 2
source_sha256: 3b9506e4f3e23238e10313f9d33578f4e8465a7ead506337c213277910b507be
translation: machine
translated_at: '2026-10-24'
---
# MVTrack4Gen {#mvtrack4gen}

**Ligne de développement :** `project:mvtrack4gen` · fil `mvtrack4gen-development`  
**Dernier événement :** 2026-06-26 · 1 événement daté depuis le 2026-06-26 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

MVTrack4Gen entraîne des modèles de diffusion conditionnés par la caméra au moyen du suivi de points multi-vues, pour la génération de vidéos à point de vue nouveau. Il cible ReCamMaster et ReDirector sans reconstruction 3D à l'inférence.

- Tête de suivi auxiliaire : extrait les caractéristiques d'attention et applique une perte de correspondance.
- Entrées : vidéo source, points de requête et trajectoire de caméra cible.

Le code et les modèles pré-entraînés ne sont pas encore publiés.

## Ligne de développement {#development-line}

- **2026-06-26 — Page du projet MVTrack4Gen liée.** Le cadre fournit un suivi de points multi-vues pour la génération à point de vue nouveau, et non la génération de texte ni le suivi autonome. Nous l'entraînons sur deux backbones, ReCamMaster et ReDirector, et l'évaluons sur DAVIS et iPhone.

## Ce qui a changé {#what-changed}

2026-06-26 — La page du projet a été mise en ligne. MVTrack4Gen est un cadre de suivi de points multi-vues pour la génération à point de vue nouveau, et non un générateur de texte ni un outil de suivi autonome. Il s'entraîne au-dessus de deux backbones, ReCamMaster et ReDirector, et s'évalue sur DAVIS et iPhone.

2026-06-24 — La version v1 de l'article arXiv 2606.26087 a publié la méthode sous forme de prépublication.

2026-06-26 — Le dépôt GitHub officiel ne contient qu'un README indiquant « Code Coming Soon ». Les poids, les instructions d'installation et les artefacts de publication ne sont pas disponibles.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-26, utilisez la page du projet MVTrack4Gen comme référence de départ pour ce projet ; la documentation disponible ne justifie pas de modification plus précise du flux de travail technique.

1. Faites correspondre la tâche aux entrées : vidéo de référence monoculaire, points de requête et trajectoire de caméra cible, car la méthode génère des vues nouvelles plutôt que de suivre une vidéo générique.
  — <https://cvlab-kaist.github.io/MVTrack4Gen/>
2. Lisez l'article pour reproduire le cadre d'entraînement sur un backbone conditionné par la caméra pris en charge, car il n'existe pas encore de script de lancement officiel.
  — <https://arxiv.org/abs/2606.26087>
3. Surveillez le dépôt officiel pour le code et les modèles pré-entraînés, et évitez toute intégration en production tant qu'ils ne sont pas disponibles.
  — <https://github.com/cvlab-kaist/MVTrack4Gen>

## Bonnes pratiques {#best-practices}

- N'appliquez MVTrack4Gen que lorsque la trajectoire de caméra cible est connue et qu'une cohérence temporelle inter-vues est requise, car il ne remplace pas un suivi vidéo général.
  — <https://cvlab-kaist.github.io/MVTrack4Gen/>
- Testez la cohérence géométrique et la précision de la caméra sur vos propres scènes dynamiques, car les résultats de l'article ne couvrent que DAVIS et iPhone.
  — <https://cvlab-kaist.github.io/MVTrack4Gen/>
- Ne figez pas les dépendances ni les poids avant la publication officielle, car le dépôt ne contient ni code ni modèles pré-entraînés.
  — <https://github.com/cvlab-kaist/MVTrack4Gen>

## Remplacé par cela {#superseded-by-this}

- 2026-06-26 — La disponibilité immédiate du code source est remplacée : au 2026-09-05, le dépôt indique toujours que le code et les modèles pré-entraînés sont à venir.

## Points encore inconnus {#still-unknown}

- Le code officiel, les modèles pré-entraînés, la licence, les exigences matérielles et un flux d'inférence reproductible ne sont pas encore publiés.
- La prépublication arXiv est datée du 2026-06-24, mais aucune source primaire ne confirme l'heure exacte de mise en ligne de la page du projet ou du dépôt GitHub.
- Les constats d'événements et les entrées du schéma des nouveaux événements ne sont pas distincts ; leurs détails vérifiés sont intégrés dans la section « Ce qui a changé ».

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://cvlab-kaist.github.io/MVTrack4Gen/ | MVTrack4Gen — Multi-View Point Tracking as Geometric Supervision for 4D Video Generation | 2026-09-05 |
| https://arxiv.org/abs/2606.26087 | MVTrack4Gen: Multi-View Point Tracking as Geometric Supervision for 4D Video Generation | 2026-09-05 |
| https://github.com/cvlab-kaist/MVTrack4Gen | cvlab-kaist/MVTrack4Gen | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:mvtrack4gen`, fil `mvtrack4gen-development`, 1 événement daté du 2026-06-26 au 2026-06-26.
- **Note pratique :** À partir du 2026-06-26, les praticiens doivent utiliser la page du projet MVTrack4Gen comme référence de départ pour ce projet ; la documentation disponible ne justifie pas de modification plus précise du flux de travail technique.
- **Confiance :** élevée. Les mentions datées de remplacement ci-dessus font foi pour ce qui est devenu obsolète.
