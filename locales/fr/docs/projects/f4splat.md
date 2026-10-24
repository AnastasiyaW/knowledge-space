---
title: "F⁴Splat"
category: projects
tags: [f4splat, f4splat-development, project]
aliases: ["F⁴Splat"]
level: 2
source_sha256: 3e67e3562f2422099d822c54795715b6bb2ca32836a1311db89e47d14402df9b
translation: machine
translated_at: '2026-10-24'
---
# F⁴Splat {#f4splat}

**Ligne de développement :** `project:f4splat` · fil `f4splat-development`  
**Événements :** 2 datés, du 2026-03-30 au 2026-07-24 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

F⁴Splat est un cadre de recherche 3DGS destiné aux développeurs, qui synthétise des vues novatrices à partir d'images éparses non calibrées. Il s'agit d'une alternative en code à AnySplat pour la recherche CUDA, et non d'un service cloud finalisé ni d'un scanner 3D universel.

- Prédiction de la caméra et des paramètres : prédit les poses de caméra, les paramètres des Gaussiennes et les cartes de scores de densification.
- Allocation des primitives : répartit les primitives gaussiennes selon la complexité de la scène et les recouvrements entre vues.
- Mise à l'échelle du budget : modifie le budget gaussien cible à l'inférence, sans réentraînement.

La démonstration locale accepte 2 à 16 images ; les poids publiés couvrent ACID 2 vues et RealEstate10K 2 et 24 vues.

## Ligne de développement {#development-line}

- **2026-03-30 — Publication de la page de projet F⁴Splat.** F⁴Splat est apparu sur sa page de projet publique le 2026-03-30. Une référence aux graphiques à niveaux de détail encadrait l'annonce dans le développement du rendu. La page ne donnait aucune affirmation technique précise ni d'état de publication.
- **2026-07-24 — Lien vers le dépôt GitHub de F⁴Splat.** La ligne de développement a relié le dépôt GitHub de F⁴Splat le 2026-07-24, en complément de l'annonce de mars. Cela a ouvert l'accès public au code source. La publication ne précisait pas quel code, quelle version ni quelles modifications d'implémentation apparaissaient à cette date.

## Évolutions {#what-changed}

- **2026-03-30 :** La page de projet décrivait la méthode. Au lieu d'une répartition uniforme des pixels ou des voxels vers des Gaussiennes, le modèle alloue les primitives selon la densité prédite.
- **2026-06-30 :** Le commit officiel « Release public code » a ajouté 181 fichiers comprenant la démonstration, l'entraînement, l'évaluation et le code source. La méthode est devenue un flux de travail local reproductible.
- **2026-07-24 :** Le lien pointait vers le dépôt officiel, mais la source n'enregistrait aucune modification technique distincte ce jour-là. La version de code confirmée la plus proche reste celle du 30 juin.
- **2026-09-03 :** L'article arXiv est passé à la version v3. La page ne décrit pas les différences ; nous ne pouvons donc pas affirmer l'existence de nouvelles fonctionnalités ni de résultats modifiés à la suite de cette révision.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-24, consultez la page de projet F⁴Splat pour le contexte et le dépôt GitHub lié pour l'accès aux sources. Considérez les capacités précises et l'état des versions comme non vérifiés, dans l'attente de travaux de recherche.

1. Clonez le dépôt, créez un environnement Python 3.11, installez PyTorch 2.8.0 pour CUDA 12.8, puis installez les dépendances du projet.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
2. Téléchargez le point de contrôle du Hub correspondant au jeu de données cible et au nombre de vues de contexte : `acid-2view`, `re10k-2view` ou `re10k-24view`.
  — <https://huggingface.co/Knowing/F4Splat>
3. Exécutez `python demo/app.py`, importez 2 à 16 images et sélectionnez un budget gaussien pour comparer les rendus.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
4. Pour les expériences, préparez le jeu de données au format de fragments PyTorch avec `index.json`, puis exécutez les scripts d'entraînement ou d'évaluation fournis en indiquant l'identifiant GPU et le chemin du point de contrôle.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Bonnes pratiques {#best-practices}

- Faites correspondre la roue PyTorch à la version de CUDA installée en premier. Si CUDA n'est pas en version 12.8, installez d'abord la version de PyTorch correspondante, avant les autres dépendances.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Choisissez les points de contrôle selon le jeu de données et le nombre de vues de contexte. Ne considérez pas les poids publiés comme un modèle universel pour des scènes quelconques.
  — <https://huggingface.co/Knowing/F4Splat>
- Évaluez le budget gaussien d'après le nombre réel de primitives. La démonstration produit une vidéo en interpolation seule et annote les résultats avec le nombre effectif de Gaussiennes, exprimé en milliers.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Respectez les licences et les conditions d'accès de RealEstate10K, DL3DV et ACID lors de l'entraînement.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-30 : considérer F⁴Splat uniquement comme un article ou une page de projet est obsolète. Le code source officiel est disponible, avec les scripts de démonstration, d'entraînement et d'évaluation.
- 2026-09-03 : citez arXiv v3 plutôt que v1/v2 dans les citations de recherche actuelles. Cette révision ne démontre aucune modification des capacités à l'exécution.

## Inconnues {#still-unknown}

- Le texte de la source primaire n'était pas lisible : une éventuelle annonce de publication distincte pour le 2026-07-24 n'a donc pas pu être extraite.
- La prépublication arXiv v3 du 2026-09-03 ne comporte aucune note de modification : les différences avec les versions v1/v2 ne sont pas confirmées.
- Les documents officiels ne fournissent aucune évaluation indépendante de la qualité sur des captures d'utilisateurs, ni de vitesse d'exécution ou d'utilisation de la mémoire GPU.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://mlvlab.github.io/F4Splat/ | F⁴Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat | mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commits/main | Commits · mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commit/127ed096c1ab7c4aa65431dc659bc08592adbb22 | Publication du code public · mlvlab/F4Splat@127ed09 | 2026-09-04 |
| https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md | README de F4Splat | 2026-09-04 |
| https://huggingface.co/Knowing/F4Splat | Knowing/F4Splat | 2026-09-04 |
| https://arxiv.org/abs/2603.21304 | F4Splat: Feed-Forward Predictive Densification for Feed-Forward 3D Gaussian Splatting | 2026-09-04 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:f4splat`, fil `f4splat-development`, 2 événements datés du 2026-03-30 au 2026-07-24.
- **Remarque pratique :** Au 2026-07-24, consultez la page de projet F⁴Splat pour le contexte et le dépôt GitHub lié pour l'accès aux sources, en considérant les capacités précises et l'état des versions comme non vérifiés dans l'attente de travaux de recherche.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
