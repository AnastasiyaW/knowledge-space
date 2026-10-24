---
title: "MosaicMem"
category: projects

tags: [mosaicmem, mosaicmem-development, project]
aliases: ["MosaicMem"]
level: 2
source_sha256: fc2d3384d0f6cbf82ac66266a29d2d78e2948a3920ffa2b976b771ead86c2d26
translation: machine
translated_at: '2026-10-24'
---
# MosaicMem {#mosaicmem}

**Ligne de développement :** `project:mosaicmem` · fil `mosaicmem-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

MosaicMem : une architecture de recherche pour les video world models, qui stocke des patchs vidéo en 3D et les restitue au point de vue voulu ; la navigation, l'édition de la mémoire, les événements dynamiques et le rollout auto-régressif sont annoncés. La longueur de navigation présentée atteint deux minutes ; au 5 septembre 2026, le code sur la page du projet est toujours marqué « Coming ». Ce n'est donc pas un outil prêt à être déployé.

## Ligne de développement {#development-line}

- L'événement daté n'est pas encore rédigé ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-03-19 — la page MosaicMem a été publiée et le préprint arXiv:2603.17117 du 17 mars 2026 a été présenté : la méthode combine des patchs 3D avec latent-conditioning, PRoPE et l'alignement de la mémoire ; les auteurs la comparent à GEN3C et Context-as-Memory.

Complément à l'événement du 2026-03-19 : le préprint a été déposé sur arXiv le 17 mars 2026, et la fiche d'auteur sur Hugging Face Papers est datée du 19 mars 2026. La limite pratique indiquée sur la page du projet est une navigation de recherche allant jusqu'à deux minutes, et non la publication d'un SDK ou de poids.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-19, cette seule fiche n'entraîne aucune modification de workflow prise en charge. Les praticiens doivent considérer la page MosaicMem liée comme une piste pour des recherches futures, et non comme une preuve de capacité, de publication ou de recommandation d'adoption.

1. Utilisez la page du projet et le préprint comme spécification de la méthode : préparez un générateur vidéo avec accès à la pose de caméra, à la représentation des patchs et au conditionnement ; la page ne fournit ni code officiel prêt à l'emploi, ni poids, ni API.
  — <https://mosaicmem.github.io/mosaicmem/>
2. Implémentez ou évaluez le schéma comme un pipeline de recherche : lift des patchs en 3D, retrieval pour la vue cible, patch-and-compose, puis génération avec PRoPE et alignment.
  — <https://arxiv.org/abs/2603.17117>

## Bonnes pratiques {#best-practices}

- Ne présentez pas MosaicMem comme une bibliothèque de production finalisée : le projet officiel indique que le code paraîtra plus tard ; la reproductibilité exige une implémentation propre ou une future publication officielle.
  — <https://mosaicmem.github.io/mosaicmem/>
- Évaluez séparément la préservation de la géométrie lors du retour de la caméra et la capacité à générer de la dynamique : c'est précisément le compromis que la méthode cherche à améliorer par rapport aux baselines à mémoire explicite et implicite.
  — <https://arxiv.org/abs/2603.17117>

## Ce qui le remplace {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Le code officiel, les poids, la licence, les besoins en calcul et un workflow pratique reproductible ne sont pas publiés sur la page du projet consultée.
- Aucun événement officiel ultérieur daté, modifiant le statut de la méthode après le 19 mars 2026, n'a été trouvé.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://mosaicmem.github.io/mosaicmem/ | MosaicMem | 2026-09-05 |
| https://arxiv.org/abs/2603.17117 | MosaicMem: Hybrid Spatial Memory for Controllable Video World Models | 2026-09-05 |
| https://huggingface.co/papers/2603.17117 | Paper page - MosaicMem: Hybrid Spatial Memory for Controllable Video World Models | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:mosaicmem`, fil `mosaicmem-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-03-19, cette seule fiche n'entraîne aucune modification de workflow prise en charge ; les praticiens doivent considérer la page MosaicMem liée comme une piste pour des recherches futures, et non comme une preuve de capacité, de publication ou de recommandation d'adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
