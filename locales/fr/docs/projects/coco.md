---
title: "CoCo"
category: projects
date: 2026-03-15
tags: [coco, coco-development, project]
aliases: ["CoCo"]
level: 2
source_sha256: e0be841f620b3fffa7a82c0e9225701a872c9ab6b2565e74309673e749dd205c
translation: machine
translated_at: '2026-10-24'
---
# CoCo {#coco}

**Ligne de développement :** `project:coco` · fil `coco-development`  
**Dernier événement :** 2026-03-15 · 1 événement daté depuis le 2026-03-15 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

CoCo est un flux de travail de recherche qui transforme des prompts textuels en code Python et Matplotlib exécutable décrivant une scène. Il effectue le rendu d'une ébauche dans un bac à sable, vérifie la mise en page par rapport au prompt, puis affine l'ébauche pour obtenir une image finale. Il vise les mises en page structurées, les relations spatiales et le texte dense. Sur trois benchmarks, il rapporte un ensemble d'entraînement de 10K paires ébauche–image finale, ainsi que des gains de 68,83 %, 54,8 % et 41,23 % par rapport à la génération directe. Il s'agit d'une référence de recherche, et non d'un paquet d'inférence prêt à l'emploi.

## Ligne de développement {#development-line}

- **2026-03-15 — Ressources publiques du projet CoCo référencées.** Le 2026-03-15, CoCo a été référencé via des ressources de projet liées sur GitHub et Hugging Face. Cela crée un point de référence public daté pour le code du projet et les éléments liés au modèle.

## Modifications {#what-changed}

- 2026-03-15 — CoCo est apparu avec son code et un lien vers un modèle Hugging Face. Le dépôt décrit la méthode code → ébauche → affinage, mais ne fournit aucune commande d'inférence documentée à destination des utilisateurs finaux.
- 2026-08-06 — arXiv v2 est devenue la version actuelle de l'article et a enregistré l'acceptation à ECCV 2026.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-15, commencez par le dépôt GitHub et la page Hugging Face liés pour localiser les ressources publiques. Examinez directement les fichiers source avant de les utiliser.

1. Partez de la description de la méthode du dépôt : générez à partir d'un prompt du code Matplotlib exécutable décrivant la mise en page de la scène, effectuez le rendu de l'ébauche, puis utilisez-la comme plan intermédiaire pour l'affinage de l'image.
  — <https://github.com/micky-li-hd/CoCo>
2. Traitez le bac à sable fourni comme du code de recherche : il exécute le Python fourni via un appel `exec`. Ne l'exécutez donc que dans un environnement isolé, et ne lui soumettez jamais de code non fiable.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>
3. Utilisez l'article pour la conception de l'entraînement et de l'évaluation ; la page Hugging Face publique ne comporte ni fiche de modèle, ni statistiques de téléchargement suivies, ni fournisseur d'inférence hébergé.
  — <https://arxiv.org/abs/2603.08652>

## Bonnes pratiques {#best-practices}

- Utilisez une ébauche exécutable lorsque la planification basée uniquement sur le prompt perd en précision spatiale ou structurelle ; vérifiez l'ébauche avant de lancer la génération de l'image finale.
  — <https://arxiv.org/abs/2603.08652>
- Isolez l'exécution du code et limitez-la dans le temps : le bac à sable fourni effectue une vérification du code dangereux et applique un délai d'expiration, mais exécute tout de même le Python généré.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-06 — arXiv v1 (2026-03-09) n'est plus la version actuelle de l'article ; utilisez la v2 lorsque vous citez l'article.

## Points encore inconnus {#still-unknown}

- La page Hugging Face ne comporte ni fiche de modèle ni données de téléchargement suivies, et le dépôt ne contient qu'un README, des figures et le code du bac à sable. Une configuration d'inférence publique reproductible, le contenu des points de contrôle, les exigences matérielles et la licence ne sont pas documentés dans les sources consultées.
- Le dépôt annonce la publication de l'article le 2026-03-09, alors que l'événement daté est du 2026-03-15. Les sources internes consultées ne permettent pas de déterminer ce qui a changé précisément le 2026-03-15.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/micky-li-hd/CoCo | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation — dépôt officiel | 2026-09-05 |
| https://huggingface.co/mickyhimself/CoCo | mickyhimself/CoCo — page du modèle Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2603.08652 | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation | 2026-09-05 |
| https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py | CoCo sandbox.py | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:coco`, fil `coco-development`, 1 événement daté du 2026-03-15 au 2026-03-15.
- **Note pratique :** à partir du 2026-03-15, les praticiens doivent utiliser le dépôt GitHub et la page Hugging Face liés comme points de départ pour localiser les ressources publiques de CoCo ; leur contenu et leur pertinence nécessitent tout de même un examen au niveau du code source.
- **Confiance :** moyenne. Les remplacements datés font foi pour déterminer ce qui est obsolète.
