---
title: "SIMART"
category: projects
date: 2026-05-19
tags: [project, simart, simart-development]
aliases: ["SIMART", "SimArt"]
level: 2
source_sha256: 0e53f8aea05b9cd1a6531a668154119f223fd71413301215cd140abdc467495f
translation: machine
translated_at: '2026-10-24'
---
# SIMART {#simart}

**Ligne de développement :** `project:simart` · fil `simart-development`  
**Dernier événement :** 2026-05-19 · 2 datés depuis le 2026-03-30 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

SIMART est une implémentation de recherche de ByteDance Seed destinée aux praticiens de la 3D et de la robotique qui doivent convertir un maillage monolithique en parties articulées pour des simulateurs. Elle combine un MLLM basé sur Qwen3-VL et un Sparse 3D VQ-VAE. Elle prédit la décomposition en parties, les métadonnées physiques, les types d'articulations, leurs axes et leurs limites, puis produit des fichiers orientés URDF. L'article indique 70 % de tokens géométriques en moins que les voxels denses. Le dépôt est testé avec Python 3.10 et fournit des points de contrôle (checkpoints) locaux plutôt qu'un point d'accès d'inférence hébergé. Utilisez-le comme pipeline de recherche local pour préparer des assets articulés, et validez l'URDF généré avant de vous y fier dans un simulateur.

## Ligne de développement {#development-line}

- **2026-03-30 — Site du projet SIMART référencé.** Le 2026-03-30, le site du projet a établi le premier point d'entrée public. Les éléments disponibles n'identifient aucune version, capacité ou publication spécifique.
- **2026-05-19 — Dépôt Hugging Face de SIMART référencé.** Le 2026-05-19, le dépôt Hugging Face ByteDance-Seed/SimArt est apparu en parallèle de la page du projet. Les éléments disponibles n'établissent ni le contenu du dépôt, ni sa licence, ni le statut exact de la publication.

## Ce qui a changé {#what-changed}

- **2026-03-24** — La prépublication arXiv a introduit la méthode unifiée de SIMART, qui transforme un maillage en asset articulé, le Sparse 3D VQ-VAE et SIMART-Bench, en annonçant une réduction de 70 % des tokens par rapport aux tokens de voxels denses.
- **2026-03-30** — La page du projet a rendu disponibles la présentation de la recherche et une galerie interactive d'assets articulés, décrivant les métadonnées URDF structurées ainsi que les segments décomposés.
- **2026-05-19** — Les liens suivis ont ajouté le dépôt Hugging Face de ByteDance-Seed en parallèle de la page du projet. La fiche de modèle identifie deux groupes de points de contrôle, `simart_mllm/` et `simart_vqvae/`.
- **2026-05-28** — Une mise à jour est apparue sur `ByteDance-Seed/SimArt` sur Hugging Face. La fiche de modèle fournit les poids sans fournisseur d'inférence hébergé.
- **2026-09-05** — Le README public du dépôt GitHub documente l'installation locale, l'alignement des maillages, le prétraitement et l'inférence pour les entrées GLB.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-05-19, les praticiens doivent consulter le dépôt Hugging Face ByteDance-Seed/SimArt lié, en parallèle du site du projet SIMART, pour trouver les ressources du projet ; les éléments datés ne confirment pas quels artefacts sont utilisables.

1. Clonez l'implémentation, créez un environnement Python 3.10 et installez `requirements.txt`.
  — <https://github.com/ByteDance-Seed/SimArt>
2. Téléchargez les deux groupes de points de contrôle depuis le dépôt Hugging Face officiel et placez-les sous `./checkpoints`, ou passez des chemins personnalisés.
  — <https://huggingface.co/ByteDance-Seed/SimArt>
3. Normalisez un maillage `.glb` brut avec `scripts/process_raw_objects.py` ; générez un aperçu pendant le prétraitement.
  — <https://github.com/ByteDance-Seed/SimArt>
4. Exécutez `inference/infer.py --object_path <processed.glb> --debug` pour générer la structure articulée, l'URDF et les visualisations de débogage.
  — <https://github.com/ByteDance-Seed/SimArt>

## Bonnes pratiques {#best-practices}

- Utilisez un système de coordonnées droitier avec +Z vers le haut et une direction avant cohérente ; corrigez les rotations des maillages qui utilisent une autre convention.
  — <https://github.com/ByteDance-Seed/SimArt>
- Générez l'aperçu de normalisation et vérifiez que l'objet est droit et orienté vers l'avant avant l'inférence, car l'orientation influe sur les parties sémantiques comme les poignées ou les pieds avant.
  — <https://github.com/ByteDance-Seed/SimArt>
- Utilisez `--debug` pour inspecter les maillages de parties colorés et les axes d'articulation, puis vérifiez l'URDF produit dans le simulateur cible avant de l'utiliser pour des travaux de politique robotique.
  — <https://github.com/ByteDance-Seed/SimArt>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-24 — Considérer SIMART comme une méthode uniquement théorique est obsolète : le dépôt et la publication des points de contrôle fournissent une voie d'inférence locale.
- 2026-05-28 — Supposer que SIMART est disponible via un fournisseur d'inférence Hugging Face géré n'est pas pris en charge ; la page officielle du modèle indique qu'aucun fournisseur ne le déploie.

## Toujours inconnu {#still-unknown}

- La fiche de modèle Hugging Face officielle n'affiche pas sa propre date de publication ; aucun changement daté indépendamment ne peut donc être attribué spécifiquement à l'événement du 2026-05-19, au-delà de la présence de ce lien de dépôt.
- Le nom est ambigu sur le web plus large : une plateforme de détection et de communication 6G sans rapport s'appelle également SimART. Le projet ByteDance Seed, l'article, le code et les poids cités identifient de manière cohérente le sujet des assets 3D articulés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2603.23386 | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://simart-mllm.github.io/ | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://github.com/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/MinghanQin/activity/all | Activité de Minghan Qin | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:simart`, fil `simart-development`, 2 événements datés du 2026-03-30 au 2026-05-19.
- **Note pratique :** À partir du 2026-05-19, les praticiens doivent consulter le dépôt Hugging Face ByteDance-Seed/SimArt lié, en parallèle du site du projet SIMART, pour trouver les ressources du projet ; les éléments datés ne confirment pas quels artefacts sont utilisables.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
