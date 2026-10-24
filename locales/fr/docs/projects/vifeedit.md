---
title: "ViFeEdit — Présence publique du projet"
category: projects
date: 2026-03-18
tags: [project, public-project-presence, vifeedit]
aliases: ["ViFeEdit"]
level: 2
source_sha256: b2bdf130d24ca49c35cc3dfab92af1a8dc601339b9c0df7dcaa3a5d8ed65213e
translation: machine
translated_at: '2026-10-24'
---
# ViFeEdit — Présence publique du projet {#vifeedit-public-project-presence}

**Ligne de développement :** `project:vifeedit` · fil `public-project-presence`  
**Dernier événement :** 2026-03-18 · 1 événement daté depuis le 2026-03-18 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

ViFeEdit adapte Wan et d'autres Diffusion Transformers texte-vers-vidéo similaires pour la génération et l'édition de vidéos, sans données d'entraînement vidéo.
- Reparamétrisation de l'attention 3D : sépare l'indépendance spatiale.
- Pipeline à double voie : achemine des embeddings de timestep distincts à travers des paires d'images 2D source et cible.

L'entraînement nécessite en pratique 100 à 250 paires d'images et moins de 20 époques. Nous le considérons comme un workflow de fine-tuning spécifique à une tâche, et non comme un éditeur vidéo clé en main.

## Ligne de développement {#development-line}

- **2026-03-18 — Les ressources publiques du projet ViFeEdit ont été liées.** Le 2026-03-18, nous avons relié la ligne de développement à un dépôt GitHub public et à un lien Hugging Face. Ces liens identifient les ressources du projet. Ils n'établissent ni une publication, ni une version, ni une évolution des capacités, ni un statut de publication.

## Ce qui a changé {#what-changed}

2026-03-16 : la prépublication ViFeEdit a introduit un fine-tuning sans vidéo pour les Diffusion Transformers vidéo, utilisant uniquement des paires d'images 2D.  
2026-03-17 : les auteurs ont publié le code d'entraînement et d'inférence.  
2026-03-18 : le projet est devenu accessible via le dépôt lié. Ce dépôt ajoute les limites pratiques absentes des liens d'événements : 100 à 250 paires d'images par tâche, entraînement limité aux 20 premières époques, et un chemin d'inférence avec post-traitement optionnel.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2026-03-18, nous utilisons le dépôt GitHub lié comme source principale du projet. Nous considérons le lien Hugging Face comme une ressource associée, jusqu'à ce que la recherche confirme son rôle.

1. Clonez le dépôt et installez-le dans un environnement Python isolé avec `pip install -e .`. Réutilisez un environnement Conda DiffSynth uniquement si ses dépendances sont compatibles.
  — <https://github.com/Lexie-YU/ViFeEdit>
2. Créez des paires d'images source et cible, ainsi qu'un fichier `metadata_vife.csv` qui associe chaque prompt cible et chaque image cible à l'image source utilisée comme référence de la vidéo d'inférence.
  — <https://github.com/Lexie-YU/ViFeEdit>
3. Définissez les chemins des données et des sorties dans `train_vife.sh`, exécutez le script, et choisissez un checkpoint parmi les 20 premières époques au lieu d'exécuter les 500 époques configurées.
  — <https://github.com/Lexie-YU/ViFeEdit>
4. Configurez l'exemple d'inférence fourni et exécutez `python inference.py`. N'utilisez `postprocess.py` que si un alignement supplémentaire de la sortie est nécessaire.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Bonnes pratiques {#best-practices}

- Commencez par une modification étroitement définie, avec 100 à 250 paires d'images. Gardez la correspondance source/cible et les noms des métadonnées cohérents, car l'entraînement utilise l'image source comme référence ultérieure de vidéo source.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Considérez les 20 premières époques comme la fenêtre d'entraînement pratique. Évaluez les checkpoints dans cet intervalle avant de prolonger un entraînement.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Épinglez ou vérifiez `transformers==4.55.0`. Si l'installation en mode éditable échoue sur `pkg_resources`, utilisez le drapeau `--no-build-isolation` documenté dans le dépôt plutôt que de modifier les dépendances.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Le dépôt documente le code, la préparation des données et l'inférence, mais n'identifie ni checkpoint ViFeEdit téléchargeable, ni cible de déploiement en production prise en charge.
- Aucune note de version de première partie postérieure au 2026-03-18 n'existe dans les sources utilisées ici.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Lexie-YU/ViFeEdit | Lexie-YU/ViFeEdit — README du dépôt | 2026-09-05 |
| https://arxiv.org/abs/2603.15478 | ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:vifeedit`, fil `public-project-presence`, 1 événement daté du 2026-03-18 au 2026-03-18.
- **Remarque pratique :** Depuis le 2026-03-18, utilisez le dépôt GitHub lié comme source identifiée du projet. Considérez le lien Hugging Face comme une ressource associée, jusqu'à ce que la recherche établisse son rôle exact.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
