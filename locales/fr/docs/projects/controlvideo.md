---
title: "ControlVideo"
category: projects
date: 2023-07-09
tags: [controlvideo, project]
aliases: ["ControlVideo"]
level: 3
source_sha256: 68cdf0c098a5efcbda64b2b0bbc059823725f487d03aacbce98357588a5339ed
translation: machine
translated_at: '2026-10-24'
---
# ControlVideo {#controlvideo}

**Ligne de développement :** `project:controlvideo` · fil `controlvideo`  
**Dernier événement :** 2023-07-09 · 2 événements datés depuis 2023-05-23 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

ControlVideo génère une nouvelle vidéo SD 1.5 conditionnée par une vidéo source et un prompt textuel.

- Conditions par image : extrait les signaux ControlNet, y compris la profondeur, les contours et la pose.
- Cohérence entre images : ajoute une attention inter-images complète et un lissage entrelacé.
- Longues séquences : inclut un échantillonneur vidéo hiérarchique optionnel.

## Ligne de développement {#development-line}

- **2023-05-23 — Le dépôt GitHub de ControlVideo apparaît.** Le 2023-05-23, nous suivons le dépôt GitHub comme point d'entrée du code source du projet. Cette date indique le moment où nous avons vu le dépôt, et non sa publication initiale confirmée.
- **2023-07-09 — Une démo Hugging Face Space apparaît aux côtés du dépôt.** Le 2023-07-09, nous ajoutons la démo Hugging Face Space à côté du dépôt GitHub. Le lien donne accès à une démo interactive, bien que la date exacte de lancement et les fonctionnalités d'origine restent non vérifiées.

## Évolutions {#what-changed}

Les publications de ControlVideo se sont déroulées par étapes :
- 2023-05-23 : l'article a été publié.
- 2023-05-25 : le code source a été publié dans le dépôt officiel.
- 2023-05-28 : une démo Replicate a été ajoutée.
- 2023-07-09 : le Space de fffiloni est apparu à côté du dépôt officiel.
- 2023-07-11 : la prise en charge de ControlNet 1.1 a été ajoutée.
- 2023-07-16 : l'auteur a fait un lien vers une démo Hugging Face.
- 2026-09-04 : le Space de fffiloni est en pause, et le Space Yabo lié par l'auteur échoue avec une erreur d'exécution liée à la limite de stockage. Aucun des deux ne fonctionne comme démo navigateur documentée.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-07-09, évaluez ControlVideo à partir du dépôt de code ou du Hugging Face Space lié, et vérifiez la compatibilité en local.

1. Créez un environnement Python 3.10 isolé et installez les dépendances épinglées.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
2. Téléchargez Stable Diffusion v1.5, les poids ControlNet requis et les poids RIFE FlowNet dans les chemins de checkpoints documentés.
  — <https://github.com/YBYBZhang/ControlVideo>
3. Choisissez une condition prise en charge par la version de ControlNet ciblée ; pour la v10, passez des clés telles que depth_midas, canny ou openpose avec les checkpoints correspondants.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
4. Exécutez la commande de référence inference.sh avec une vidéo source et un prompt, en commençant par 15 images et 512×512.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
5. Ajoutez --is_long_video après la réussite de l'exécution courte pour activer l'échantillonneur hiérarchique sur les séquences plus longues.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>

## Bonnes pratiques {#best-practices}

- Isolez les dépendances épinglées avant toute mise à jour. Torch 1.13.1+cu116, Diffusers 0.14.0, Transformers 4.26.1 et xFormers 0.0.16 forment une pile de reproductibilité héritée.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
- Alignez --condition, --version et les chemins de checkpoints. Le code associe v10 et v11 à des clés de condition distinctes.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Spécifiez depth_midas plutôt que l'option générique depth du README. Le script inference.sh et l'association v10 exigent depth_midas.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
- Gardez la largeur et la hauteur des images divisibles par 32. Commencez les tests avec 15 images et 512×512, et fixez la graine pour comparer les itérations.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Vérifiez les fichiers source_video.mp4 et la vidéo de condition générés avant d'évaluer la qualité des sorties. Le pipeline écrit ces deux fichiers avant l'échantillonnage des images.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Évitez la démo navigateur liée par l'auteur pour un travail actif. Le Space hébergé plante avec une erreur d'exécution liée à la limite de stockage.
  — <https://huggingface.co/spaces/Yabo/ControlVideo>

## Remplacé par {#superseded-by-this}

- 2023-07-09 : l'exécution du Hugging Face Space de fffiloni est obsolète, car il est en pause depuis le 2026-09-04.
- 2023-07-16 : l'exécution du Hugging Face Space Yabo lié par l'auteur est obsolète, car il échoue avec une erreur d'exécution liée à la limite de stockage.
- L'argument --condition depth du README de 2023 est obsolète sur master. Passez une clé associée, telle que depth_midas, avec la --version correspondante.

## Points encore inconnus {#still-unknown}

- La compatibilité au-delà de la pile 2023 épinglée reste non vérifiée, car nous n'avons effectué aucun test dans un environnement CUDA et Python 2026 propre.
- Les instructions d'installation en chinois simplifié restent non vérifiées, car les recherches n'ont trouvé aucune documentation officielle.
- Le texte original du message du 2023-07-09 n'est pas disponible ; nous vérifions donc les liens enregistrés plutôt que l'affirmation initiale.
- Le projet ControlVideo de THU, référencé sous arXiv:2305.17098, est une méthode distincte d'édition vidéo texte-vers-vidéo en one-shot, et non le projet sans entraînement suivi ici.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/YBYBZhang/ControlVideo | ControlVideo — implémentation PyTorch officielle | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt | ControlVideo requirements.txt — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py | ControlVideo inference.py — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh | ControlVideo inference.sh — master | 2026-09-04 |
| https://arxiv.org/abs/2305.13077 | ControlVideo: Training-free Controllable Text-to-Video Generation | 2026-09-04 |
| https://huggingface.co/spaces/fffiloni/ControlVideo | ControlVideo — Space Hugging Face par fffiloni | 2026-09-04 |
| https://huggingface.co/spaces/Yabo/ControlVideo | ControlVideo — Space Hugging Face par Yabo | 2026-09-04 |
| https://ml.cs.tsinghua.edu.cn/controlvideo/ | ControlVideo: Adding Conditional Control for One Shot Text-to-Video Editing | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:controlvideo`, fil `controlvideo`, 2 événements datés du 2023-05-23 au 2023-07-09.
- **Note pratique :** À partir du 2023-07-09, évaluez ControlVideo à partir du dépôt de code et du Hugging Face Space, mais testez les dépendances locales indépendamment.
- **Confiance :** moyenne. Les éléments remplacés ci-dessus identifient les voies obsolètes.
