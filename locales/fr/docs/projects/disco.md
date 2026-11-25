---
title: "DisCO"
category: projects
date: 2023-07-11
tags: [disco, disco-development, project]
aliases: ["DISCO", "DisCO", "DisCo"]
level: 2
source_sha256: dd67efdc71b4f62d2263e33773838623a598703526afbe5120b80c538daa7f01
translation: machine
translated_at: '2026-10-24'
---
# DisCO {#disco}

**Ligne de développement :** `project:disco` · fil `disco-development`  
**Dernier événement :** 2023-07-11 · 3 événements datés depuis 2022-10-20 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

DisCO regroupe trois implémentations de recherche spécialisées par tâche, destinées aux praticiens de l'image, et non un outil unique déployable.

- DISCO colorise des images en niveaux de gris à l'aide d'ancres de couleur globales.
- Portrait DisCO corrige la perspective faciale de gros plans par inversion de 3D-GAN.
- Dance DisCo combine un premier plan de référence, un arrière-plan et une pose cible pour générer des images ou des vidéos de personnes.

## Ligne de développement {#development-line}

- **2022-10-20 — Apparition de la page projet et de la démo publique de DisCO.** Disentangled Image Colorization via Global Anchors a établi un flux de travail de colorisation SIGGRAPH Asia 2022, avec code, points de contrôle et démo hébergée.
- **2023-02-26 — Présentation de Portrait DisCO sur un site de projet.** Portrait Distortion Correction with Perspective-Aware 3D GANs est apparu comme projet distinct, destiné à corriger la déformation des portraits en gros plan. Le dépôt indique une acceptation à l'IJCV le 2024-01-03 et une publication du code d'inversion le 2025-02-04, tandis que le système complet et la démo Hugging Face restent à faire (TODO).
- **2023-07-11 — Publication du projet de danse DisCo, avec code et démo en ligne.** Disentangled Control for Referring Human Dance Generation in Real World est apparu comme projet distinct de génération de danse contrôlée par la pose. Le dépôt indique une mise à jour du module temporel le 2023-11-30, une acceptation à CVPR 2024 le 2024-04-08, et IDOL comme amélioration de DisCo le 2024-07-15.

## Ce qui a changé {#what-changed}

- 2022-10-20 — DISCO : Disentangled Image Colorization via Global Anchors a établi un flux de travail de colorisation SIGGRAPH Asia 2022, avec code, points de contrôle et démo hébergée.
- 2023-02-26 — DisCO : Portrait Distortion Correction with Perspective-Aware 3D GANs est apparu comme projet distinct, destiné à corriger la déformation des portraits en gros plan. Le dépôt indique une acceptation à l'IJCV le 2024-01-03 et une publication du code d'inversion le 2025-02-04, tandis que le système complet et la démo Hugging Face restent à faire (TODO).
- 2023-07-11 — DisCo : Disentangled Control for Referring Human Dance Generation in Real World est apparu comme projet distinct de génération de danse contrôlée par la pose. Le dépôt indique une mise à jour du module temporel le 2023-11-30, une acceptation à CVPR 2024 le 2024-04-08, et IDOL comme amélioration de DisCo le 2024-07-15.

Ces dates ne forment pas une seule ligne de développement. Les trois projets ont des auteurs, des tâches, des modèles, des dépôts et des circuits de publication différents.

## Mode d'emploi {#how-to-use-this}

Au 2023-07-11, consultez les pages publiques de projet propres à chaque tâche et vérifiez les capacités à partir du code ou de la démo en ligne liés, plutôt que de considérer le nom comme un outil unique et inchangé.

1. Pour la colorisation en niveaux de gris, clonez le dépôt, créez l'environnement Python 3.8 / PyTorch / CUDA documenté, téléchargez un point de contrôle dans `checkpoints`, placez les images dans `data`, puis exécutez le script d'inférence fourni.
  — <https://github.com/MenghanXia/DisentangledColorization>
2. Pour la correction de perspective des portraits, initialisez EG3D et Deep3DFaceRecon, téléchargez le point de contrôle FFHQ, créez l'environnement Conda fourni, définissez les chemins d'entrée et de modèles dans `example_configs/config.py`, exécutez le prétraitement, puis lancez le script de correction.
  — <https://github.com/lightChaserX/DisCO>
3. Pour l'édition d'images de danse, téléchargez le point de contrôle de fine-tuning et la dépendance SD Image Variations, définissez leurs chemins dans le notebook Jupyter fourni, puis lancez-le sur un GPU local.
  — <https://github.com/Wangt-CN/DisCo>

## Bonnes pratiques {#best-practices}

- Pour la colorisation DISCO, conservez l'inférence par défaut en 256×256, sauf si vous avez validé un autre paramétrage : les auteurs considèrent la sortie en résolution originale avec `--no_resize` comme instable. Utilisez des chemins absolus et fixez `--seed` lors de la comparaison de résultats.
  — <https://github.com/MenghanXia/DisentangledColorization>
- Pour Portrait DisCO, validez la chaîne de dépendances EG3D et Deep3DFaceRecon avant de traiter des images, et considérez le code d'inversion publié comme plus restreint qu'un produit public complet, car le système complet et la démo hébergée figurent encore comme TODO.
  — <https://github.com/lightChaserX/DisCO>
- Pour Dance DisCo, utilisez le notebook local documenté pour un premier flux de travail sur image ; pour un fine-tuning spécifique aux personnes, préparez les masques et les squelettes avec Grounded-SAM et OpenPose, puis ajustez d'abord le taux d'apprentissage et le dégel des couches U-Net.
  — <https://github.com/Wangt-CN/DisCo>

## Ce qui est rendu obsolète {#superseded-by-this}

- 2022-10-20 — utiliser l'Space de colorisation DISCO hébergé comme flux de travail par défaut est obsolète, car sa page signale actuellement une erreur d'exécution. Utilisez plutôt le chemin du dépôt local.
- 2023-02-26 — l'attente antérieure d'une future publication du code de Portrait DisCO est remplacée par la publication du code d'inversion du 2025-02-04. Ne la confondez pas avec une publication du système complet ou de la démo hébergée.
- 2023-07-11 — considérer le point d'accès Gradio lié comme un flux de travail Dance DisCo actuel et vérifié est obsolète, car il n'a pas pu être récupéré le 2026-09-04. Utilisez le flux de travail local du dépôt tant qu'un point d'accès hébergé n'a pas été confirmé de manière indépendante.
- 2023-07-11 — considérer toutes les occurrences de « DisCO » comme des versions d'un même projet est obsolète. Les trois entrées sont des projets indépendants qui partagent un nom.

## Points encore inconnus {#still-unknown}

- La clé `disco` regroupe trois projets indépendants. Aucune source primaire n'établit un mainteneur commun, un calendrier de publication, une API, un poids de modèle ou une relation de succession.
- Le point d'accès Gradio actuel de Dance DisCo n'a pas pu être récupéré pendant la recherche ; cela ne prouve pas un retrait définitif.
- Nous n'avons exécuté aucun dépôt et n'avons téléchargé aucun point de contrôle : la compatibilité avec les versions actuelles de CUDA, PyTorch et des dépendances n'est pas vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://menghanxia.github.io/projects/disco.html | DISCO: Disentangled Image Colorization via Global Anchors | 2026-09-04 |
| https://huggingface.co/spaces/menghanxia/disco | Disco - a Hugging Face Space by menghanxia | 2026-09-04 |
| https://github.com/MenghanXia/DisentangledColorization | MenghanXia/DisentangledColorization | 2026-09-04 |
| https://portrait-disco.github.io/ | DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs | 2026-09-04 |
| https://github.com/lightChaserX/DisCO | lightChaserX/DisCO | 2026-09-04 |
| https://disco-dance.github.io/ | DisCo: Disentangled Control for Referring Human Dance Generation in Real World | 2026-09-04 |
| https://github.com/Wangt-CN/DisCo | Wangt-CN/DisCo | 2026-09-04 |
| https://5e42cfd7d54823fd8a.gradio.live/ | Point d'accès de la démo Gradio de DisCo | 2026-09-04 |
| https://7b2faca424cdb265fc.gradio.live/ | Point d'accès de la démo Gradio de la page projet DisCo | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:disco`, fil `disco-development`, 3 événements datés du 2022-10-20 au 2023-07-11.
- **Note pratique :** Au 2023-07-11, les praticiens qui suivent la lignée DisCO doivent rechercher les pages publiques de projet propres à chaque tâche et valider une capacité revendiquée à partir du code ou de la démo en ligne liés, plutôt que de considérer le seul nom comme un outil unique et inchangé.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
