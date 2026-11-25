---
title: "AvatarArtist"
category: projects
date: 2025-04-09
tags: [avatarartist, avatarartist-public-release-and-space, project]
aliases: ["AvatarArtist"]
level: 3
source_sha256: 55308cb8fe0e13d176ff3f046768ba2c552f55e61e8c8e9610bb81205d394c8f
translation: machine
translated_at: '2026-10-24'
---
# AvatarArtist {#avatarartist}

**Ligne de développement :** `project:avatarartist` · fil `avatarartist-public-release-and-space`  
**Dernier événement :** 2025-04-09 · 2 événements datés depuis 2025-03-27 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

AvatarArtist est un pipeline open-domain de conversion d'un portrait en avatar 4D, destiné aux créateurs et aux chercheurs qui ont besoin d'une sortie pilotée par le mouvement.

- conversion de portrait : transforme un portrait en une représentation 4D paramétrique
- rendu d'images : génère les images cibles à partir de l'image de référence et des signaux de pilotage
- accès au pipeline : comprend les chemins d'inférence et de traitement des entrées publiés

## Ligne de développement {#development-line}

- **2025-03-27 — AvatarArtist a lancé sa page de projet publique et son dépôt officiel.** Cela a établi le flux de travail local, code et poids.
- **2025-04-09 — AvatarArtist a été relié à un Hugging Face Space.** Aucune note de version officielle examinée ne prouve une révision du modèle à cette date.

## Évolutions {#what-changed}

AvatarArtist est passé d'une version d'inférence locale à des démonstrations locales et en ligne. Une version de l'entraînement n'est toujours pas documentée.

- 2025-03-26 : le dépôt officiel a annoncé le code d'inférence et les modèles pré-entraînés.
- 2025-03-27 : la page de projet publique et le dépôt officiel ont établi le flux de travail local, code et poids.
- 2025-03-30 : le dépôt officiel a mentionné une version de démonstration Gradio.
- 2025-04-02 : le dépôt officiel a mentionné une version de démonstration en ligne.
- 2025-04-09 : le Hugging Face Space est apparu ; aucune note de version officielle examinée ne prouve une révision du modèle à cette date.
- 2026-09-04 : l'ancienne URL GitHub ant-research redirige vers robbyant-research ; le dépôt indique toujours que le code d'entraînement est en attente.

## Mode d'emploi {#how-to-use-this}

Au 2025-04-09, consultez la page de projet et le dépôt d'AvatarArtist, puis testez le Hugging Face Space associé pour une évaluation hébergée.

1. Commencez par une image de référence de portrait et une source de mouvement de pilotage ; AvatarArtist crée une représentation 4D à partir du portrait et rend les images selon les signaux de pilotage.
  — <https://kumapowerliu.github.io/AvatarArtist/>
2. Clonez le dépôt, créez l'environnement Conda documenté avec Python 3.9, puis installez les dépendances.
  — <https://github.com/robbyant-research/AvatarArtist>
3. Téléchargez les poids KumaPower/AvatarArtist dans `pretrained_model` ; obtenez `faceverse_v3_1.npy` séparément et copiez-le vers les deux chemins FaceVerse documentés.
  — <https://github.com/robbyant-research/AvatarArtist>
4. Exécutez `python3 app.py` avec les données de démonstration d'abord ; pour une sortie contrôlée, exécutez `inference.py` avec l'image, les coefficients FaceVerse, les entrées de mouvement, le chemin de sortie et l'option facultative `--select_img`.
  — <https://github.com/robbyant-research/AvatarArtist>
5. Pour vos propres médias, utilisez le chemin de prétraitement officiel afin que le dossier final `dataset` contienne les dossiers requis pour l'image, les coefficients, le mouvement et le rendu avant l'inférence.
  — <https://github.com/robbyant-research/AvatarArtist>
6. Utilisez le Space dans le navigateur uniquement pour un essai manuel rapide ; sa page consultable était marquée Sleeping et non comme un point de terminaison actif.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Bonnes pratiques {#best-practices}

- Commencez par les données de démonstration fournies et la structure de prétraitement documentée ; seul le dossier final `dataset` est l'entrée du modèle, les autres dossiers sont intermédiaires.
  — <https://github.com/robbyant-research/AvatarArtist>
- Considérez `faceverse_v3_1.npy` comme une configuration requise, et non comme un élément facultatif : les poids seuls ne rendent pas le projet exécutable.
  — <https://github.com/robbyant-research/AvatarArtist>
- Limitez votre travail à l'inférence et au traitement de données publiés ; la liste de tâches officielle indique toujours que la publication du code d'entraînement est en attente.
  — <https://github.com/robbyant-research/AvatarArtist>
- Utilisez le dépôt redirigé robbyant-research pour les nouveaux liens d'installation ; ne conservez l'URL ant-research que pour les références historiques.
  — <https://github.com/ant-research/AvatarArtist>
- Ne considérez pas la fiche du modèle comme une inférence hébergée : elle ne mentionne aucun déploiement via Hugging Face Inference Provider.
  — <https://huggingface.co/KumaPower/AvatarArtist>
- Considérez le Space comme une exploration facultative et non comme une dépendance de production, car l'instantané accessible le montrait en état Sleeping.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Remplacé par {#superseded-by-this}

- 2025-03-27 : utiliser `https://github.com/ant-research/AvatarArtist` comme URL canonique du propriétaire est remplacé par la redirection observée vers `https://github.com/robbyant-research/AvatarArtist` le 2026-09-04.

## Inconnues {#still-unknown}

- Le texte de l'événement daté du 2025-04-09 n'est pas disponible ; nous ne pouvons donc le relier à la démonstration en ligne au-delà du Space associé.
- Nous n'avons pas exécuté le Space de bout en bout pendant l'examen ; son état actuel, le comportement au démarrage à froid et la latence restent non vérifiés.
- Les sources officielles ne fournissent aucune matrice prise en charge pour GPU, VRAM, CUDA ou système d'exploitation.
- Nous n'avons trouvé aucun retour d'expérience de la communauté ; ces pratiques proviennent des exigences officielles et de l'état de distribution.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://kumapowerliu.github.io/AvatarArtist/ | AvatarArtist: Open-Domain 4D Avatarization | 2026-09-04 |
| https://github.com/ant-research/AvatarArtist | AvatarArtist official PyTorch implementation; redirects to robbyant-research | 2026-09-04 |
| https://github.com/robbyant-research/AvatarArtist | AvatarArtist official PyTorch implementation | 2026-09-04 |
| https://huggingface.co/KumaPower/AvatarArtist | KumaPower/AvatarArtist model card | 2026-09-04 |
| https://huggingface.co/spaces/KumaPower/AvatarArtist | KumaPower/AvatarArtist Hugging Face Space | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:avatarartist`, fil `avatarartist-public-release-and-space`, 2 événements datés du 2025-03-27 au 2025-04-09.
- **Note pratique :** Au 2025-04-09, les praticiens doivent consulter la page de projet et le dépôt source d'AvatarArtist, puis utiliser le Hugging Face Space associé comme point d'accès public hébergé lors de l'évaluation du projet.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
