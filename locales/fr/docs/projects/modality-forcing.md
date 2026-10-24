---
title: "Modality Forcing — Prédiction de profondeur"
category: projects
date: 2026-06-15
tags: [depth-prediction, depth_prediction, modality-forcing, project]
aliases: ["Modality Forcing"]
level: 2
source_sha256: d469bcbca0989b9a33f26b2cfa793d884c94cbd61561d158291d0decf3ebbd70
translation: machine
translated_at: '2026-10-24'
---
# Modality Forcing — Prédiction de profondeur {#modality-forcing-depth-prediction}

**Ligne de développement :** `project:modality-forcing` · fil `depth-prediction`  
**Dernier événement :** 2026-06-15 · 1 événement daté depuis le 2026-06-15 · **Consulté le :** 2026-09-08 · confiance : moyenne

## Présentation {#what-it-is}

Modality Forcing est une recette de post-entraînement et un point de contrôle BF16 FluxRGBD publié, destinés aux personnes qui ont besoin d'un seul modèle pour la génération texte vers RGB-D, l'image vers profondeur relative, ou la profondeur vers image.

- Génération texte vers RGB, profondeur et nuage de points : génération conjointe en une seule passe.
- Image vers profondeur : prédiction de profondeur relative à partir d'une image.
- Profondeur vers image : génération RGB à partir de la profondeur et du texte.

Le point de contrôle publié est flux_rgbd_9b_v2, soit 12 B de paramètres au total, avec un encodeur Qwen3-8B séparé ; sa profondeur est relative et non une profondeur métrique calibrée. Utilisez-le pour des expériences RGB-D et des flux de travail d'actifs, et non pour la métrologie ou un déploiement commercial sous la licence publique des poids.

## Ligne de développement {#development-line}

- **2026-06-15 — Les ressources de prédiction de profondeur de Modality Forcing ont été liées.** Le 2026-06-15, une référence datée a relié le site du projet, le dépôt source, l'espace Hugging Face et la page du modèle Hugging Face de Modality Forcing. Il s'agit d'un point de référence public important pour la ligne de développement de prédiction de profondeur du projet, même si les liens fournis n'établissent ni une version précise, ni un numéro de version, ni un résultat technique.

## Évolutions {#what-changed}

- 2026-06-11 — La version v1 sur arXiv a introduit la recette de post-entraînement Modality Forcing : un DiT unique avec des flux RGB et profondeur bruités indépendamment, pour l'inférence conjointe RGB-D, image vers profondeur et profondeur vers image.
- 2026-06-12 — bartduis/modality_forcing a rendu disponibles les poids publics flux_rgbd_9b_v2, les fichiers de l'autoencodeur FLUX.2, la fiche du modèle et le mode d'emploi dans sa version publique initiale.
- 2026-06-15 — Les archives de première main disponibles datent l'article et le premier artefact de modèle public du 11 au 12 juin, et n'identifient aucune version technique distincte à cette date.

## Mode d'emploi {#how-to-use-this}

1. Vérifiez d'abord le point de contrôle et la licence : bartduis/modality_forcing est le modèle par défaut ; les poids publiés sont sous licence CC BY-NC 4.0.
  — <https://huggingface.co/bartduis/modality_forcing>
2. Clonez le dépôt, utilisez Python 3.10+ et un GPU CUDA disposant d'au moins 48 Go de mémoire, installez exactement un extra CUDA uv correspondant au pilote, puis vérifiez torch.cuda.is_available().
  — <https://github.com/Duisterhof/modality-forcing>
3. Exécutez uv run scripts/joint.py --prompt "..." pour écrire une image RGB, une carte de profondeur et un nuage de points colorié dans outputs.
  — <https://github.com/Duisterhof/modality-forcing>
4. Utilisez scripts/i2d.py avec une image pour obtenir une profondeur relative, ou scripts/d2i.py avec une carte de profondeur .npy ou monocanal 16 bits plus un texte pour générer du RGB.
  — <https://github.com/Duisterhof/modality-forcing>
5. Considérez depth_raw.npy et le nuage exporté comme des sorties à échelle relative ; utilisez la carte de profondeur pour la composition ou la visualisation, et non pour une mesure calibrée.
  — <https://github.com/Duisterhof/modality-forcing>

## Bonnes pratiques {#best-practices}

- Choisissez un extra PyTorch compatible avec le pilote et vérifiez la visibilité du GPU ; un simple uv sync omet PyTorch.
  — <https://github.com/Duisterhof/modality-forcing>
- Conservez le point de contrôle publié à sa résolution d'entraînement de 512 pixels ; évitez une entrée locale non carrée pour l'image vers profondeur lorsque l'étirement modifierait la géométrie.
  — <https://github.com/Duisterhof/modality-forcing>
- Utilisez torch.compile uniquement pour un échantillonnage local répété : la première exécution entraîne un coût de compilation, puis les noyaux mis en cache sont réutilisés.
  — <https://github.com/Duisterhof/modality-forcing>
- Considérez la profondeur issue de l'image vers profondeur et de la profondeur vers image comme une échelle relative ; n'inférez pas de distances métriques à partir de leurs valeurs brutes ni de leurs nuages de points.
  — <https://github.com/Duisterhof/modality-forcing>
- Pour des trajectoires de débruitage personnalisées, privilégiez le RGB avant la profondeur lorsque la cohérence de la profondeur est l'objectif ; l'article rapporte une meilleure qualité de profondeur pour cette direction.
  — <https://arxiv.org/html/2606.13676v1>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Le texte privé de l'événement du 2026-06-15 n'est pas disponible ; son énoncé visé ne peut donc pas être reconstitué, qu'il s'agisse d'une annonce d'article ou d'une référence à une publication d'artefact.
- Le README actuel du dépôt arrondit la plage de mise à l'échelle contrôlée à 300M–3B, alors que la v1 sur arXiv indique 370M–3,3B ; aucune des deux sources n'explique s'il s'agit d'un arrondi ou d'une révision.
- Les affirmations de précision proviennent de l'évaluation des auteurs dans la v1 sur arXiv ; aucune validation indépendante en production, sur la profondeur métrique, sur la cohérence vidéo ou sur le débit n'a été trouvée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/html/2606.13676v1 | Modality Forcing for Scalable Spatial Generation (arXiv v1) | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing/commit/1da410587ea9f76d3b56602af625cd77b0e650ba | Initial public release · bartduis/modality_forcing at 1da4105 | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing | bartduis/modality_forcing · Hugging Face | 2026-09-08 |
| https://github.com/Duisterhof/modality-forcing | Duisterhof/modality-forcing · GitHub | 2026-09-08 |

## Fiche pour l'agent {#agent-brief}

- **Sujet :** `project:modality-forcing`, fil `depth-prediction`, 1 événement daté du 2026-06-15 au 2026-06-15.
- **Remarque pratique :** Voir les sections sourcées d'usage et de bonnes pratiques ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
