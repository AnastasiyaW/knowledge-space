---
title: "LUNA"
category: projects

tags: [luna, luna-development, project]
aliases: ["LUNA"]
level: 2
source_sha256: 568556b67211e6b8db1f11a7711b4cfce0d6e19c3be95d0a21ccca2e68a6ff5e
translation: machine
translated_at: '2026-10-24'
---
# LUNA {#luna}

**Ligne de développement :** `project:luna` · fil `luna-development`  
**Dernier événement :** - · 0 événement daté depuis · **Recherché le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

LUNA est un modèle de recherche permettant de générer des avatars humains 3D animables à partir de N=4 images sans pose et d'un signal de pilotage.

- Représentation 3D par Gaussiennes : remplace le Linear Blend Skinning par une transformation directe.
- Contrôle de pilotage 2D : anime l'avatar à partir d'une vidéo RGB, de points-clés ou d'un croquis.

La page publique présente des résultats visuels, mais ne fournit ni code, ni poids, ni configuration reproductible. Il s'agit d'un matériau pour l'évaluation de recherche, et non d'un outil finalisé.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Modifications {#what-changed}

2026-07-01 — LUNA: Learning Universal 3D Human Animation Beyond Skinning a introduit un modèle sans LBS pour l'animation de Gaussiennes 3D utilisant plusieurs types de contrôle 2D.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2026-07-01, considérez le site LUNA associé comme une piste de découverte non vérifiée, et non comme un historique de développement du projet validé, tant que le matériel associé et la publication d'origine n'ont pas été examinés.

1. Vérifiez l'entrée requise : N=4 images sans pose d'un même sujet et un signal de pilotage 2D parmi RGB, points-clés ou croquis.
  — <https://penghtyx.github.io/LUNA/>
2. Utilisez la page du projet et l'article pour évaluer la méthode et les résultats ; vérifiez la présence de code officiel, de poids et de licence avant de planifier une intégration.
  — <https://arxiv.org/abs/2606.31981>

## Bonnes pratiques {#best-practices}

- Ne transposez pas les résultats de démonstration en production sans tests locaux sur les sujets cibles, les vêtements, les angles de caméra et les signaux de pilotage.
  — <https://penghtyx.github.io/LUNA/>
- Respectez la limite N=4 : le pipeline publié reconstruit les Gaussiennes 3D canoniques uniquement à partir de 4 images multi-vues.
  — <https://penghtyx.github.io/LUNA/>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour le moment.

## Points encore inconnus {#still-unknown}

- La page publique ne renvoie vers aucun dépôt officiel, aucun poids de modèle, aucune licence, aucune exigence matérielle ni aucune instruction d'exécution ; les sources actuelles ne permettent pas de confirmer si ces éléments sont publiés.
- Les modifications substantielles de la version arXiv v2 du 2026-09-01 restent non vérifiées : les métadonnées confirment la mise à jour, mais ne fournissent aucun journal des modifications.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://penghtyx.github.io/LUNA/ | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://arxiv.org/abs/2606.31981 | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://rawalkhirodkar.github.io/ | Rawal Khirodkar — Publications | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:luna`, fil `luna-development`, 0 événement daté - → -.
- **Note pratique :** Depuis le 2026-07-01, considérez le site LUNA associé comme une piste de découverte non vérifiée, et non comme un historique de développement du projet validé, tant que le matériel associé et la publication d'origine n'ont pas été examinés.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
