---
title: "UPAL"
category: projects
date: 2026-08-24
tags: [project, upal, upal-development]
aliases: ["UPAL"]
level: 2
source_sha256: f3b3e8c50e66c233f25e57c02cb878ee8e7aa04a85e3a650c93565be30709856
translation: machine
translated_at: '2026-10-24'
---
# UPAL {#upal}

**Ligne de développement :** `project:upal` · fil `upal-development`  
**Dernier événement :** 2026-08-24 · 1 événement daté depuis le 2026-08-24 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

UPAL est un extracteur de caractéristiques PyTorch autonome destiné aux praticiens de la vision par ordinateur (CV) et du SLAM. Il combine, dans un même réseau, la détection de points, la détection de lignes et des descripteurs locaux.

- points-clés à precision sub-pixel et scores de confiance ;
- descripteurs L2-normalisés de dimension 128 ;
- cartes de chaleur des points-clés et champs de distance aux lignes, avec un post-traitement `points_lsd` fourni pour les segments.

## Ligne de développement {#development-line}

- **2026-08-24 — Référence au dépôt GitHub d'UPAL.** Le dépôt est devenu public, mais aucun commit, tag ou release de l'auteur principal ne correspond à cette date ; elle n'établit donc pas une nouvelle version.

## Ce qui a changé {#what-changed}

2026-08-20 : la v1 sur arXiv a présenté UPAL comme un extracteur de caractéristiques point-ligne à backbone partagé, avec code public. Les auteurs rapportaient une accélération d'environ 4× et une empreinte mémoire 10× plus faible qu'ALIKED + DeepLSD. 2026-08-24 : le dépôt d'UPAL est devenu public, mais aucun commit, tag ou release de l'auteur principal ne correspond à cette date ; elle n'établit donc pas une nouvelle version.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-24, partez du dépôt GitHub d'UPAL pour toute recherche sur le projet, car les éléments disponibles ne permettent pas de donner de consignes opérationnelles plus précises.

1. Clonez le dépôt, créez un environnement Python 3.10+ et installez le paquet avec `pip install -e .`.
  — <https://github.com/francois141/upal>
2. Initialisez les sous-modules récursivement et installez `third_party/points_lsd`. Pour CUDA, installez la version de PyTorch correspondante avant de compiler cette extension.
  — <https://github.com/francois141/upal>
3. Exécutez `demo_inference.py`, `demo_match_points.py` et `demo_match_lines.py` pour tester les chemins supportés d'inférence, d'appariement de points et d'appariement de lignes.
  — <https://github.com/francois141/upal>
4. Pour utiliser UPAL dans une application, chargez `weights/upal.tar`, passez un tenseur normalisé dans `[0,1]` de forme `B×1×H×W` ou `B×3×H×W`, puis récupérez les points-clés, les descripteurs, les cartes de chaleur et le champ de distance aux lignes.
  — <https://github.com/francois141/upal>

## Bonnes pratiques {#best-practices}

- Installez une version de PyTorch compatible CUDA avant de compiler `points_lsd`, car le chemin des lignes dépend de ce sous-module natif.
  — <https://github.com/francois141/upal>
- Testez les trois démonstrations fournies avant toute intégration, car l'inférence, l'appariement de points et l'appariement de lignes sont des chemins supportés distincts.
  — <https://github.com/francois141/upal>
- Ne généralisez pas le chiffre de vitesse à d'autres déploiements : le résultat publié de 70 ms a été obtenu sur 500 images 800×800 traitées séquentiellement, avec un batch size de un, sur une RTX 2080 Ti.
  — <https://arxiv.org/html/2608.19894v1>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Nous n'avons trouvé aucun commit, tag ou release de l'auteur principal daté du 2026-08-24 ; nous ne pouvons donc pas considérer cette date comme une publication de version.
- Le dépôt documente l'inférence autonome et les démonstrations, mais pas un service de production supporté, un flux d'entraînement ou une matrice de systèmes d'exploitation.
- Nous n'avons trouvé aucun retour vérifié de la communauté sur l'installation ; les compilations sur les environnements cibles et les performances restent donc non testées.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/francois141/upal | GitHub - francois141/upal : détecteur unifié de points et de lignes | 2026-09-05 |
| https://arxiv.org/abs/2608.19894 | Caractéristiques locales point-ligne unifiées et efficaces | 2026-09-05 |
| https://arxiv.org/html/2608.19894v1 | Caractéristiques locales point-ligne unifiées et efficaces — arXiv HTML v1 | 2026-09-05 |
| https://www.x-techcon.com/article/178188.html | Nouvelle direction d'optimisation SLAM : UPAL unifie les caractéristiques point-ligne, 4× plus rapide et 10× moins de mémoire | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:upal`, fil `upal-development`, 1 événement daté du 2026-08-24 au 2026-08-24.
- **Remarque pratique :** Au 2026-08-24, partez du dépôt GitHub d'UPAL pour toute recherche sur le projet, car les éléments disponibles ne permettent pas de donner de consignes opérationnelles plus précises.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
