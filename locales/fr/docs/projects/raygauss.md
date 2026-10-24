---
title: "RayGauss"
category: projects
date: 2024-11-17
tags: [project, raygauss]
aliases: ["RayGauss"]
level: 2
source_sha256: 76eb421bfabca4c925746026bfdaa999f9cbef49afababfe923c61eefbd8a96f
translation: machine
translated_at: '2026-10-24'
---
# RayGauss {#raygauss}

**Ligne de développement :** `project:raygauss` · fil `raygauss`  
**Dernier événement :** 2024-11-17 · 2 événements datés depuis 2024-08-08 · **Consulté le :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

RayGauss est un code et une méthode de synthèse de nouvelles vues destinés aux chercheurs, conçus comme une alternative volumétrique au splatting.

- Entraînement de scènes à partir d'images multi-vues.
- Rendu volumétrique avec des fonctions de base gaussiennes elliptiques, des caractéristiques SH et SG, et un lancer de rayons BVH/OptiX.
- Export PLY de la géométrie de scène.
- Visionneuse GUI pour inspecter les scènes entraînées.

L'article original rapporte 25 FPS sur Blender. Il convient à la reproduction de l'article et à l'expérimentation sur NVIDIA/OptiX, mais ce n'est pas une bibliothèque de production générale.

## Ligne de développement {#development-line}

- **2024-08-08 — Page projet publique de RayGauss référencée.** Champ de radiance paramétrique gaussien avec lancer de rayons volumétrique différentiable, en concurrence avec le splatting.
- **2024-11-17 — Dépôt source de RayGauss référencé.** Le 2024-11-17, le dépôt GitHub public a été lié, sans affirmations vérifiées sur la version du code, son contenu ou le statut de publication.

## Ce qui a changé {#what-changed}

2024-08-08 — RayGauss est publié : un champ de radiance paramétrique gaussien avec lancer de rayons volumétrique différentiable, en concurrence avec le splatting. 2024-11-17 — Le dépôt d'implémentation public est disponible, avec l'installation, l'entraînement, l'évaluation, l'export PLY et la GUI. 2025-09-09 — Les auteurs publient RayGaussX, qui accélère l'entraînement et le rendu de RayGauss sur des scènes réelles.

## Mode d'emploi {#how-to-use-this}

Pour reproduire ou évaluer RayGauss tel qu'il était au 2024-11-17, commencez par la page projet publique et le dépôt GitHub lié, puis vérifiez les affirmations relatives à l'installation, à la version et aux résultats.

1. Installez le pilote NVIDIA, CUDA et OptiX 7.6, clonez le dépôt et créez un environnement conda à partir de environment.yml ; la qualité d'entraînement annoncée nécessite un GPU avec 24 Go de VRAM.
  — <https://github.com/hugobl1/ray_gauss>
2. Préparez la scène selon la structure COLMAP : images et sparse/0 contenant cameras.bin, images.bin et points3D.bin ; les modèles de caméra pris en charge sont SIMPLE_PINHOLE et PINHOLE.
  — <https://github.com/hugobl1/ray_gauss>
3. Lancez l'entraînement d'une scène unique via main_train.py avec une configuration YAML, puis évaluez via main_test.py.
  — <https://github.com/hugobl1/ray_gauss>
4. Exportez la scène entraînée au format PLY via convertpth_to_ply.py et visualisez le résultat dans main_gui.py.
  — <https://github.com/hugobl1/ray_gauss>

## Bonnes pratiques {#best-practices}

- Sous Windows, faites correspondre les versions de cuda-toolkit et pytorch-cuda dans environment.yml avec la version de CUDA installée ; compilez python-optix depuis les sources plutôt que de compter sur un paquet conda.
  — <https://github.com/hugobl1/ray_gauss>
- Pour des comparaisons reproductibles, placez le jeu de données dans dataset/ et exécutez le script fourni nerf_synth.sh ou mip_nerf360.sh.
  — <https://github.com/hugobl1/ray_gauss>
- Ne supposez pas que les 25 FPS annoncés sur Blender se vérifient sur des scènes réelles : le article suivant des auteurs indique que le coût de calcul de RayGauss empêche le rendu en temps réel sur des scènes réelles.
  — <https://arxiv.org/abs/2509.07782>

## Remplacé par {#superseded-by-this}

- 2025-09-09 — Pour les tâches en temps réel sur des scènes réelles, l'hypothèse selon laquelle RayGauss de base serait suffisamment rapide est remplacée par RayGaussX ; l'implémentation de base reste un code distinct pour la méthode originale.

## Points encore inconnus {#still-unknown}

- Aucune source primaire datée et indépendante pour le 2024-11-17 n'apporte de faits propres à cette date, au-delà de la description de l'état actuel du dépôt.
- Aucune version publiée stable ni API prise en charge n'existe dans les sources primaires disponibles ; vérifiez la compatibilité avec la configuration précise de CUDA, OptiX et du pilote.
- event_findings: [{"event_date":"2024-08-08","finding":"La préimpression du 2024-08-06 précise la méthode : la radiance et la densité sont représentées par des fonctions de base gaussiennes avec des harmoniques sphériques et des gaussiennes sphériques, avec une intégration tranche par tranche via un BVH GPU ; 25 FPS sont rapportés sur le jeu de données Blender.","source_url":"https://arxiv.org/abs/2408.03356","source_date":"2024-08-06"}]
- new_events: [{"date":"2025-09-09","finding":"Les auteurs ont présenté RayGaussX : saut de l'espace vide, échantillonnage adaptatif, cohérence accrue des rayons, régularisation d'échelle et un nouveau critère de densification ; l'article rapporte un entraînement 5 à 12 fois plus rapide, un rendu 50 à 80 fois plus rapide, et un gain de PSNR pouvant atteindre 0,56 dB sur des jeux de données réels.","source_url":"https://arxiv.org/abs/2509.07782","source_date":"2025-09-09"}]

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://raygauss.github.io/ | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://arxiv.org/abs/2408.03356 | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://github.com/hugobl1/ray_gauss | hugobl1/ray_gauss | 2026-09-05 |
| https://arxiv.org/abs/2509.07782 | RayGaussX: Accelerating Gaussian-Based Ray Marching for Real-Time and High-Quality Novel View Synthesis | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:raygauss`, fil `raygauss`, 2 événements datés du 2024-08-08 au 2024-11-17.
- **Remarque pratique :** Au 2024-11-17, les praticiens qui évaluent ou tentent de reproduire RayGauss doivent commencer par la page projet publique et le dépôt GitHub lié, puis vérifier indépendamment les affirmations relatives à l'installation, à la version et aux résultats.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
