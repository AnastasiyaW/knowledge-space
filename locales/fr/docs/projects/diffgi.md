---
title: "DiffGI"
category: projects

tags: [diffgi, diffgi-development, project]
aliases: ["DiffGI"]
level: 2
source_sha256: ff47887e79fd345f0feb02a665accc0f9a7b1950daa01497851f880c98f6a635
translation: machine
translated_at: '2026-10-24'
---
# DiffGI {#diffgi}

**Ligne de développement :** `project:diffgi` · fil `diffgi-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

DiffGI est une méthode de recherche image-vers-3D pour les vêtements et le mobilier à ossature aux surfaces fines et ouvertes. — remplace la carte d'occupation binaire par un TSDF 2D continu ; — reconstruit le maillage via Marching Squares différentiable et utilise un DiffGI-VAE avec diffusion latente ; — les auteurs rapportent 1,21 s et 3,22 Go de VRAM sur une RTX 4070 12 Go, ou 8,52 s sur un CPU MacBook M4. Verdict : aujourd'hui, il s'agit d'un article et d'une page projet destinés à la recherche ou à une implémentation personnelle, et non d'un outil d'inférence publié.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-15 : DiffGI est paru sous forme d'arXiv v1 — méthode à TSDF 2D continu, Differentiable Marching Squares, DiffGI-VAE et diffusion latente basée sur un transformer. 2026-08-06 : la page projet renvoyait à la v1 déjà publiée ; aucune révision d'article, publication de modèle ou publication de code exécutable distincte n'est confirmée à cette date.

## Comment l'utiliser {#how-to-use-this}

1. Utilisez aujourd'hui DiffGI comme référence technique pour votre propre implémentation si vous avez besoin de surfaces fines non fermées, et non comme un modèle prêt à télécharger et à exécuter.
  — <https://arxiv.org/abs/2607.13365>
2. Avant de planifier une inférence locale, vérifiez le code source officiel de la démo : les URL des modèles sont restées des espaces réservés et le pipeline n'est pas connecté ; il n'existe donc ni commandes d'installation ni exécution reproductible.
  — <https://github.com/EJShim/diffgi/blob/main/docs/demo/index.html>

## Bonnes pratiques {#best-practices}

- DiffGI : conservez 1,21 s et 3,22 Go comme benchmark des auteurs pour une RTX 4070 12 Go, et non comme une promesse de performance ni comme une exigence matérielle pour un autre workflow.
  — <https://ejshim.github.io/diffgi/>
- DiffGI : ne planifiez pas l'intégration comme un paquet open source prêt à l'emploi — le dépôt officiel est décrit comme une page projet statique, et le code de démo publié n'exécute pas d'inférence.
  — <https://github.com/EJShim/diffgi>
- DiffGI : avant toute mise en production, vérifiez séparément la topologie, les UV charts et l'aptitude du maillage à la simulation en aval ; les résultats de l'article ne remplacent pas votre propre validation de l'asset.
  — <https://arxiv.org/abs/2607.13365>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Aucun checkpoint officiel, paquet d'implémentation, fiche modèle, licence, guide d'installation ni workflow reproductible n'était disponible dans les sources officielles consultées.
- Aucun artefact primaire daté indépendamment pour le 2026-08-06 ne documente une révision d'article, une publication de code ou de modèle distincte.
- Les chiffres de qualité, de latence et de mémoire rapportés sont des résultats publiés par les auteurs ; aucune reproduction indépendante ni validation de simulation en production n'a été trouvée.
- Une recherche ciblée en chinois n'a trouvé aucune note de version, documentation ni tutoriel en chinois émanant des auteurs pour DiffGI.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://arxiv.org/abs/2607.13365 | DiffGI: Differentiable Geometry Images for High-Fidelity Thin-Shell 3D Generation — arXiv 2607.13365 | 2026-09-07 |
| https://ejshim.github.io/diffgi/ | DiffGI: Differentiable Geometry Images for High-Fidelity Thin-Shell 3D Generation | 2026-09-07 |
| https://github.com/EJShim/diffgi | EJShim/diffgi — dépôt de la page projet DiffGI | 2026-09-07 |
| https://github.com/EJShim/diffgi/blob/main/docs/demo/index.html | Source de la démo WebGPU de DiffGI | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:diffgi`, fil `diffgi-development`, 0 événement daté - → -.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, limites comprises.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
