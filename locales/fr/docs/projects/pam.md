---
title: "PAM — Publication publique"
category: projects
date: 2026-03-26
tags: [pam, project, public-release]
aliases: ["PAM"]
level: 2
source_sha256: d9d5407255bb8648daa7ae9079cf1e45092923135a0671b060043777dfb36868
translation: machine
translated_at: '2026-10-24'
---
# PAM — Publication publique {#pam-public-release}

**Ligne de développement :** `project:pam` · fil `public-release`  
**Dernier événement :** 2026-03-26 · 1 événement daté depuis le 2026-03-26 · **Consulté le :** 2026-09-06 · confiance : moyenne

## Description {#what-it-is}

PAM est un pipeline de recherche destiné aux équipes qui créent des données d'interaction main-objet à partir de simulations.

- Pose construit une trajectoire à partir des poses MANO de départ et d'arrivée, de la pose 6-DoF de l'objet et du maillage de l'objet.
- Appearance génère la première image à partir de la profondeur, de la segmentation et des points clés de la main.
- Motion transforme les conditions et la première image choisie en un clip vidéo.

Les auteurs rapportent 301,1 s pour 40 images et un pic de 41,4 Go sur NVIDIA H20. Il s'agit d'un générateur hors ligne de données HOI synthétiques, et non d'un point de terminaison vidéo qui ne reçoit qu'un prompt.

## Ligne de développement {#development-line}

- **2026-03-26 — Les ressources publiques du projet PAM ont été mises à disposition.** Le site du projet, le code et la collection de poids ont été liés entre eux. La source primaire confirme qu'aucune nouvelle publication de code ou de poids n'a eu lieu ce jour-là.

## Modifications {#what-changed}

- 2025-12-04 — PAM : Hugging Face a ajouté un checkpoint de mouvement à conditions complètes en quatre parties pour OakInk2.
- 2026-03-23 — PAM : arXiv v1 a présenté l'approche en trois étapes pose–apparence–mouvement.
- 2026-03-25 — PAM : arXiv v2 a publié des résultats sur DexYCB et OAKINK2, avant la date de la première mention.
- 2026-03-26 — PAM : Le site du projet, le code et la collection de poids ont été liés entre eux, mais la source primaire confirme qu'aucune nouvelle publication de code ou de poids n'a eu lieu ce jour-là.
- 2026-04-02 — PAM : arXiv v3 a mis à jour la fiche ; le commentaire de la fiche indique l'acceptation à CVPR 2026.

## Mode d'emploi {#how-to-use-this}

1. Vérifiez d'abord l'adéquation à la tâche : PAM prend en entrée la géométrie et les poses HOI simulées, et non un prompt textuel unique.
  — <https://arxiv.org/html/2603.22193v2>
2. Choisissez et figez un artefact propre à un jeu de données, comme `dexycb_all_cond` ou `oakink2_all_cond`, plutôt que de traiter la racine du Hub comme un checkpoint unique.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
3. Déployez l'environnement à partir de `environment.yaml`, utilisez CUDA 12.1 et installez `manopth`, comme l'exige le code officiel.
  — <https://github.com/GasaiYU/PAM>
4. Préparez DexYCB ou OakInk2 : vidéo, profondeur avec masque de premier plan, segmentation, points clés de la main, légendes et listes de fichiers.
  — <https://github.com/GasaiYU/PAM>
5. Pour le passage simulation vers réel, fournissez les RGB, normales, profondeurs, segmentations et points clés GraspXL rendus, générez et sélectionnez la première image, puis lancez l'étape de mouvement via `testing/evaluation_sim.py`.
  — <https://github.com/GasaiYU/PAM>

## Bonnes pratiques {#best-practices}

- Ne prenez pas l'exemple Diffusers généré automatiquement, qui n'utilise qu'un prompt, sur le Hub comme recette vérifiée : utilisez des artefacts distincts et les conditions d'entrée du pipeline des auteurs.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
- Conservez les trois conditions : profondeur, segmentation et points clés de la main. L'étude d'ablation des auteurs montre que le meilleur résultat est obtenu en les combinant.
  — <https://arxiv.org/html/2603.22193v2>
- Vérifiez la géométrie et filtrez la première image avant l'étape de mouvement : des erreurs de contact et une mauvaise image de référence se traduisent par une vidéo physiquement invraisemblable et un scintillement temporel.
  — <https://arxiv.org/html/2603.22193v3>
- Prévoyez l'exécution comme une charge de travail lourde hors ligne : une passe complète de 40 images a pris 301,1 s sur H20 dans l'article, et l'étape d'apparence a atteint 41,4 Go.
  — <https://arxiv.org/html/2603.22193v3>

## Remplacé par cette version {#superseded-by-this}

- 2026-04-02 — arXiv v1 (2026-03-23) et v2 (2026-03-25) sont remplacés par la v3 actuelle pour la citation et pour vérifier le statut de l'article.

## Points non établis {#still-unknown}

- La source primaire ne fournit aucun horodatage vérifiable de l'état du site du projet, du dépôt GitHub et de l'arborescence complète du Hugging Face au 2026-03-26 ; nous ne pouvons pas qualifier cette date de publication de code ou de poids.
- Une licence distincte pour les poids et la fiche modèle de l'auteur sur le Hub ne sont pas confirmées ; la licence Apache-2.0 du code source ne prouve pas les conditions applicables à chaque checkpoint.
- Aucune réplication indépendante vérifiée sur le code actuel n'existe ; les métriques et les chiffres de ressources restent donc des résultats des auteurs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/html/2603.22193v2 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v2 | [2603.22193v2] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/html/2603.22193v3 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v3 | [2603.22193v3] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://github.com/GasaiYU/PAM | GitHub - GasaiYU/PAM: PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/tree/main | GasaiYU/PAM at main | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/commit/1253ebb77e4b9ad9506aed5a770bfa2b1ffbc1a9 | Upload folder using huggingface_hub · GasaiYU/PAM at 1253ebb | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:pam`, fil `public-release`, 1 événement daté du 2026-03-26 au 2026-03-26.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
