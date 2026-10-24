---
title: "MeshAnything"
category: projects
date: 2024-08-06
tags: [meshanything, meshanything-development, project]
aliases: ["MeshAnything", "MeshAnything V2"]
level: 4
source_sha256: 33570e5dd2edac2d4399ea50472df30d1bb88e36d76e28ffa56823d8e0492eb4
translation: machine
translated_at: '2026-10-24'
---
# MeshAnything {#meshanything}

**Ligne de développement :** `project:meshanything` · fil `meshanything-development`  
**Dernier événement :** 2024-08-06 · 2 événements datés depuis 2024-06-17 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

MeshAnything V2 est un modèle local de post-traitement destiné aux artistes techniques et aux ingénieurs de pipelines 3D qui ont besoin d'un maillage triangulaire compact à partir d'une forme 3D dense, plutôt qu'un générateur d'actifs 3D à partir d'un prompt.

- Prend en entrée un maillage fourni ou un nuage de points avec normales, et prédit un maillage au style d'artiste aligné sur cette forme.
- S'intègre après la reconstruction, le scan, le SDS ou tout autre générateur de maillages denses ; la V2 expose également du code local pour Gradio, la CLI, la tokenisation et l'entraînement.

## Ligne de développement {#development-line}

- **2024-06-17 — Les ressources publiques du projet MeshAnything ont été référencées.** Un vocabulaire de maillage VQ-VAE associé à un transformeur à décodeur seul a transformé une forme 3D fournie en un maillage triangulaire à faible nombre de faces, au style d'artiste.
- **2024-08-06 — Les ressources publiques de MeshAnything V2 ont été référencées.** Le 2024-08-06, le fil MeshAnything a relayé une page de projet V2, un dépôt source V2 distinct et un Hugging Face Space, avec un renvoi vers l'élément antérieur du fil. Cela marque un point de développement ultérieur à l'ère V2, mais les liens n'indiquent ni les modifications exactes, ni le comportement du modèle, ni son état de disponibilité.

## Changements {#what-changed}

- 2024-06-17 — MeshAnything a rendu disponible le remaillage autorégressif conditionné par la forme : un vocabulaire de maillage VQ-VAE associé à un transformeur à décodeur seul a transformé une forme 3D fournie en un maillage triangulaire à faible nombre de faces, au style d'artiste.
- 2024-08-06 — MeshAnything V2 a remplacé la tokenisation face par face par l'Adjacent Mesh Tokenization, ce qui réduit la longueur des séquences d'environ moitié et double la limite documentée, passant de 800 à 1600 faces.
- 2025-04-28 — Le dépôt officiel V2 a ajouté un commit d'entraînement ; sa documentation actuelle couvre les données Objaverse prétraitées, un encodeur de points Michelangelo, ainsi que l'entraînement et l'évaluation multi-GPU.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-08-06, nous traitons MeshAnything V2 comme une ligne de ressources versionnée distincte. Consultez sa page de projet dédiée, son dépôt et son Hugging Face Space plutôt que de supposer que les ressources du 2024-06-17 décrivent la V2.

1. Clonez le dépôt officiel V2 et construisez son environnement local testé : Ubuntu 22.04, CUDA 11.8, Python 3.10.13, PyTorch 2.1.1, FlashAttention et Gradio.
  — <https://github.com/buaacyw/MeshAnythingV2>
2. Téléchargez les poids du modèle officiel Yiwen-ntu/MeshAnythingV2 pour l'inférence locale ; la fiche du modèle identifie le dépôt de la bibliothèque et indique un modèle de 0,5 milliard de paramètres.
  — <https://huggingface.co/Yiwen-ntu/MeshAnythingV2>
3. Fournissez soit un maillage dense en entrée, soit un nuage de points N×6 au format .npy contenant les coordonnées et les normales. Pour une requête textuelle ou d'image, utilisez d'abord un système amont pour produire le maillage dense, puis transmettez son OBJ à MeshAnything.
  — <https://github.com/buaacyw/MeshAnythingV2>
4. Pour un maillage qui ne provient pas de Marching Cubes, lancez main.py avec --mc ; commencez avec la résolution par défaut de 128 et n'utilisez --mc_level 8 que lorsqu'une géométrie délicate nécessite un prétraitement à 256.
  — <https://github.com/buaacyw/MeshAnythingV2>
5. Lancez l'inférence en CLI avec main.py ou une interface locale avec app.py, puis vérifiez le résultat par rapport à la limite de 1600 faces et aux exigences de topologie en aval.
  — <https://github.com/buaacyw/MeshAnythingV2>
6. Pour l'entraînement, obtenez le split Objaverse prétraité et le point d'contrôle de l'encodeur de points Michelangelo, puis utilisez les commandes accelerate documentées d'entraînement et d'évaluation à huit processus.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Bonnes pratiques {#best-practices}

- Utilisez un maillage net et de haute qualité issu de la reconstruction, du scan, du SDS ou d'un générateur de maillages denses ; les recommandations officielles avertissent qu'une géométrie feed-forward faible peut manquer de détails de forme pour le budget de faces.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Normalisez l'entrée dans une boîte englobante unitaire et conservez la direction haute à +Y avant l'inférence.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Utilisez le prétraitement Marching Cubes pour les maillages qui ne proviennent pas de Marching Cubes ; n'augmentez la résolution qu'après avoir comparé le temps de prétraitement supplémentaire au gain de topologie.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Restez dans le plafond documenté de 1600 faces plutôt que d'attendre une sortie détaillée à haute densité de polygones.
  — <https://github.com/buaacyw/MeshAnythingV2>
- N'automatisez pas les appels vers le Space officiel V2 : il est en pause ; utilisez le dépôt et les poids téléchargés pour une voie locale reproductible.
  — <https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2>
- Considérez l'utilisation sous la licence S-Lab du dépôt officiel comme non commerciale tant que les auteurs n'auront pas clarifié l'étiquette de licence contradictoire de la fiche du modèle.
  — <https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt>
- Avant l'entraînement, vérifiez le nom du fichier extrait : le README mentionne training_requirements.txt, alors que la liste des fichiers du dépôt affiche training_requirement.txt.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Remplacé par ceci {#superseded-by-this}

- 2024-08-06 — Les recommandations de MeshAnything V1 limitaient les maillages générés à moins de 800 faces ; le modèle officiel V2 à 1600 faces remplace cette limite de capacité pour les nouvelles exécutions V2.
- 2025-04-28 — L'affirmation selon laquelle la V2 n'aurait pas de voie d'entraînement officielle est obsolète : le commit d'entraînement du dépôt et ses instructions actuelles en fournissent une.
- 2026-09-04 — Utiliser le Gradio Space V2 hébergé comme voie d'accès actuelle est obsolète : le Space officiel est en pause.

## Toujours inconnu {#still-unknown}

- Le dépôt officiel V2 autorise un usage non commercial, tandis que la fiche officielle du modèle sur Hugging Face indique une licence MIT pour le modèle ; nous ne savons pas quelle licence régit l'usage commercial des poids.
- La documentation officielle est testée sur Ubuntu 22.04 et CUDA 11.8, mais la compatibilité avec les pilotes actuels et une exécution d'inférence réussie n'ont pas été reproduites de manière indépendante ici.
- La documentation n'établit pas la préservation des UV, des matériaux, des squelettes ou de l'étanchéité (watertightness), ni la préparation à l'animation ; validez ces exigences sur des actifs représentatifs avant adoption.
- Aucune version V3 ni aucune version fonctionnelle postérieure à 2025 n'a été identifiée sur les points de terminaison officiels consultés ; cela ne prouve pas qu'un successeur non publié n'existe pas.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://buaacyw.github.io/mesh-anything/ | Page du projet MeshAnything | 2026-09-04 |
| https://github.com/buaacyw/MeshAnything | Dépôt officiel MeshAnything | 2026-09-04 |
| https://arxiv.org/abs/2406.10163 | MeshAnything: Artist-Created Mesh Generation with Autoregressive Transformers | 2026-09-04 |
| https://buaacyw.github.io/meshanything-v2/ | Page du projet MeshAnything V2 | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2 | Dépôt officiel MeshAnything V2 | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2/commits/main | Historique des commits de MeshAnything V2 | 2026-09-04 |
| https://arxiv.org/abs/2408.02555 | MeshAnything V2: Artist-Created Mesh Generation With Adjacent Mesh Tokenization | 2026-09-04 |
| https://huggingface.co/Yiwen-ntu/MeshAnythingV2 | Fiche du modèle Yiwen-ntu/MeshAnythingV2 | 2026-09-04 |
| https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2 | Space Yiwen-ntu/MeshAnythingV2 | 2026-09-04 |
| https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt | Licence S-Lab 1.0 pour MeshAnything V2 | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:meshanything`, fil `meshanything-development`, 2 événements datés du 2024-06-17 au 2024-08-06.
- **Note pratique :** À partir du 2024-08-06, les praticiens doivent traiter MeshAnything V2 comme une ligne de ressources versionnée distincte et consulter sa page de projet dédiée, son dépôt et son Hugging Face Space plutôt que de supposer que les ressources du 2024-06-17 décrivent la V2.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
