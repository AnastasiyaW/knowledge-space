---
title: "RiGS — Référence du dépôt"
category: projects
date: 2026-07-25
tags: [project, repository-reference, rigs]
aliases: ["RiGS"]
level: 2
source_sha256: 0a0e9de8234db679f9d9bd936a2eda29c3a09092887519aed925fce0d5952027
translation: machine
translated_at: '2026-10-24'
---
# RiGS — Référence du dépôt {#rigs-repository-reference}

**Ligne de développement :** `project:rigs` · fil `repository-reference`  
**Dernier événement :** 2026-07-25 · 1 événement daté depuis le 2026-07-25 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

RiGS fournit la base de code pour le Gaussian Splatting 4D tenant compte de la rigidité (Rigid-aware 4D Gaussian Splatting) :
- Primitives : sépare les scènes en composantes gaussiennes statiques, rigides et transitoires.
- Préparation des données : génère les entrées via ViPE et TAPIR/BootsTAPIR.
- Flux de travail : entraîne, évalue, rend et affiche les scènes dans un visualiseur.

Nécessite Python 3.10 et une pile compatible CUDA 12.x. Code de recherche sans paquets de version.

## Ligne de développement {#development-line}

- **2026-07-25 — Le dépôt du projet RiGS a été référencé.** Le 2026-07-25, la ligne de projet a été reliée au dépôt GitHub de RiGS. Cette référence atteste de la disponibilité publique, sans affirmer quoi que ce soit sur les fonctionnalités, le statut de publication ou le contenu du dépôt.

## Ce qui a changé {#what-changed}

2026-07-25 — Le dépôt d'implémentation de RiGS est devenu accessible. Les documents sources indiquent que la méthode opère sur une vidéo monoculaire unique et utilise des composantes statiques, rigides et transitoires à des échelles de temps de mouvement distinctes.

2026-05-22 — Date antérieure : les auteurs ont publié l'article RiGS sur arXiv (v1), décrivant des masques dynamiques par objet et une supervision par flot de scène.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-25, utilisez le dépôt GitHub de RiGS lié comme référence source datée pour cette ligne de projet, tout en vérifiant séparément son contenu actuel.

1. Clonez le dépôt avec son sous-module ViPE, créez un environnement conda Python 3.10, installez les dépendances et le paquet ViPE local, puis téléchargez le point de contrôle TAPIR/BootsTAPIR.
  — <https://github.com/ladvu/RiGS>
2. Préparez la vidéo et les images, extrayez via ViPE la profondeur, les poses, les intrinsèques, le flot optique, la cohérence du flot et les masques statiques, puis construisez les trajectoires TAPIR.
  — <https://github.com/ladvu/RiGS>
3. Lancez src/main.py avec les chemins de données et un nom d'expérience ; utilisez --eval_step, --render_video ou run_viewer.py pour inspecter les résultats des points de contrôle.
  — <https://github.com/ladvu/RiGS>

## Bonnes pratiques {#best-practices}

- Clonez avec --recursive, ou initialisez les sous-modules manuellement ensuite ; le prétraitement monoculaire ne fonctionnera pas sans eux.
  — <https://github.com/ladvu/RiGS>
- Faites correspondre les versions de PyTorch, de la boîte à outils CUDA et du pilote aux dépendances figées avant l'entraînement, car le dépôt cible CUDA 12.x.
  — <https://github.com/ladvu/RiGS>
- Inspectez les visualisations de prétraitement et générez les trajectoires TAPIR avant la reconstruction : le pipeline requiert à la fois les sorties ViPE et les trajectoires 2D.
  — <https://github.com/ladvu/RiGS>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- GitHub ne publie pas de versions, de sorte que le dépôt ne fournit ni historique de versions numérotées ni chemin d'installation par paquet.
- Les pages principales disponibles n'exposent pas d'enregistrement daté de création du dépôt ou de commits permettant de relier indépendamment la publication du code précisément au 2026-07-25 ; cette date reste l'événement daté fourni pour le lien vers le dépôt.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/ladvu/RiGS | ladvu/RiGS — implémentation officielle et instructions d'utilisation | 2026-09-05 |
| https://arxiv.org/abs/2605.23672 | RiGS: Rigid-aware 4D Gaussian Splatting from a Single Monocular Video | 2026-09-05 |
| https://ladvu.github.io/RiGS/ | Page du projet RiGS | 2026-09-05 |
| https://github.com/ladvu/RiGS/releases | Versions de RiGS | 2026-09-05 |

## Fiche pour agents {#agent-brief}

- **Sujet :** `project:rigs`, fil `repository-reference`, 1 événement daté du 2026-07-25 au 2026-07-25.
- **Note pratique :** À partir du 2026-07-25, les praticiens doivent utiliser le dépôt GitHub de RiGS lié comme référence source datée pour cette ligne de projet, tout en vérifiant séparément son contenu actuel.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
