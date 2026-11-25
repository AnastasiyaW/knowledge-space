---
title: "MolmoMotion"
category: projects
date: 2026-06-18
tags: [molmomotion, molmomotion-model-availability, project]
aliases: ["MolmoMotion"]
level: 2
source_sha256: a4044eb146c0dcff85aec1f5dc7d04420041619d4135ab8d389fe88076ff5a6f
translation: machine
translated_at: '2026-10-24'
---
# MolmoMotion {#molmomotion}

**Ligne de développement :** `project:molmomotion` · fil `molmomotion-model-availability`  
**Dernier événement :** 2026-06-18 · 1 événement daté depuis le 2026-06-18 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

MolmoMotion est un modèle de 4B basé sur Molmo 2, destiné aux chercheurs qui conçoivent la planification robotique ou la génération vidéo guidée par trajectoires.

- Chemins de points 3D : prévoit des trajectoires attachées aux objets.
- Conditionnement : conditionné par l'historique RGB, des points de requête 2D/3D et une action.
- Variantes de modèle : fournit des variantes AR et flow-matching.

Le checkpoint H3-F30 nécessite trois images et prédit 30 images futures, soit environ deux secondes à 15 images/s.
Utilisez-le pour des expériences de prévision de mouvement 3D, et non comme modèle texte-vidéo ni comme politique de robot à lui seul.

## Ligne de développement {#development-line}

- **2026-06-18 — Ressource de modèle MolmoMotion-4B-H3-F30 enregistrée.** Le checkpoint autorégressif de 4B prend trois images d'historique et prédit 30 positions 3D futures par point de requête.

## Ce qui a changé {#what-changed}

2026-06-18 — MolmoMotion-4B-H3-F30 est devenu disponible : le checkpoint autorégressif de 4B prend trois images d'historique et prédit 30 positions 3D futures par point de requête.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-18, suivez MolmoMotion-4B-H3-F30 comme une ressource de modèle MolmoMotion identifiable séparément. Vérifiez sa fiche de modèle avant de vous appuyer sur ses capacités, sa licence ou ses exigences de déploiement.

1. Installez le dépôt officiel dans un environnement Python 3.11 avec l'extra de visualisation.
  — <https://github.com/allenai/molmo-motion>
2. Téléchargez et chargez `allenai/MolmoMotion-4B-H3-F30` avec `MolmoMotionProcessor` et `MolmoMotion` ; exécutez le modèle interne en bf16 sur CUDA.
  — <https://github.com/allenai/molmo-motion>
3. Fournissez trois images RGB ordonnées de la plus ancienne à t0, les coordonnées 2D des points à t0, l'historique des points 3D dans le repère caméra à t0, une description de l'action et un horizon futur de 30.
  — <https://github.com/allenai/molmo-motion>
4. Appelez `predict_trajectory` et exploitez `future_3d` comme un tenseur de 8 x 30 x 3 de coordonnées en mètres dans le repère caméra ; affichez les trajectoires ou transmettez-les à un système aval.
  — <https://github.com/allenai/molmo-motion>

## Bonnes pratiques {#best-practices}

- Choisissez H3-F30 pour une entrée vidéo ordinaire ; choisissez H1-F32 uniquement lorsqu'il n'existe qu'une seule image-clé de requête.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Considérez les trajectoires comme un guidage pour la planification ou la génération, et affinez le modèle pour une tâche robotique aval plutôt que de présenter le prédicteur de base comme une politique déployable.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Utilisez le contrat d'entrée officiel du démarrage rapide ; l'historique 3D des points de requête doit être exprimé dans le repère caméra à t0.
  — <https://github.com/allenai/molmo-motion>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Nous n'avons trouvé aucune version ultérieure datée et officielle après l'événement du checkpoint du 2026-06-18 dans les sources consultées. Le dépôt public documente H1-F32 et les familles de modèles, mais n'établit pas de date de sortie ultérieure pour ceux-ci.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/allenai/MolmoMotion-4B-H3-F30 | fiche de modèle allenai/MolmoMotion-4B-H3-F30 | 2026-09-05 |
| https://github.com/allenai/molmo-motion | dépôt officiel allenai/molmo-motion | 2026-09-05 |
| https://allenai.org/blog/molmo-motion | MolmoMotion : prévision de mouvement 3D en 3D guidée par le langage | 2026-09-05 |
| https://arxiv.org/abs/2606.18558 | MolmoMotion : prévision de trajectoires de points en 3D avec instruction en langage naturel | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:molmomotion`, fil `molmomotion-model-availability`, 1 événement daté du 2026-06-18 au 2026-06-18.
- **Note pratique :** Au 2026-06-18, suivez MolmoMotion-4B-H3-F30 comme une ressource de modèle MolmoMotion identifiable séparément, et vérifiez sa fiche de modèle avant de vous appuyer sur ses capacités, sa licence ou ses exigences de déploiement.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité sur ce qui est obsolète.
