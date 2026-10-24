---
title: "ComfyUI Video Tiler"
category: projects
date: 2026-08-05
tags: [comfyui-video-tiler, comfyui_video_tiler, project]
aliases: ["ComfyUI Video Tiler"]
level: 2
source_sha256: 978bf7298dd26378230e24bc64f18d5035c285f9eceadc31a1dd9fde823d4e79
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Video Tiler {#comfyui-video-tiler}

**Ligne de développement :** `project:comfyui-video-tiler` · fil `comfyui-video-tiler`  
**Dernier événement :** 2026-08-05 · 1 événement daté depuis le 2026-08-05 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

ComfyUI Video Tiler découpe un lot vidéo de type IMAGE en tuiles qui se chevauchent, traite ces tuiles via un workflow d'upscale, puis les fusionne sans grille visible. Il cible les workflows LTX 2.3 et MiniMax H3.

- Les slicers variables et fixes découpent les images.
- La fusion avec feathering adoucit les jointures entre tuiles sans grille visible.
- Les tâches de tuiles sur disque économisent la mémoire entre les exécutions.
- L'alignement de référence et la correspondance des couleurs préservent la cohérence entre les tuiles.
- La détection audio et la temporisation des samplers suivent le rythme du clip.

Le mode disque réduit la mémoire des tuiles en cache, mais l'IMAGE fusionnée finale nécessite toujours de la RAM ou de la VRAM. Utilisez-le pour un workflow d'upscale par tuiles déjà éprouvé avec son modèle cible, et non comme pipeline vidéo généraliste.

## Ligne de développement {#development-line}

- **2026-08-05 — Le dépôt ComfyUI Video Tiler a été référencé.** Le 2026-08-05, le lien enregistré renvoyait au dépôt GitHub de ComfyUI Video Tiler. Cet enregistrement établit la référence publique du projet, mais n'établit ni version, ni ensemble de fonctionnalités, ni consignes d'installation.

## Ce qui a changé {#what-changed}

- **2026-08-05** — Le pack a été enregistré dans le Comfy Registry et a reçu des workflows d'exemple LTX 2.3 et MiniMax H3, des workflows à tampon disque et des nœuds de temporisation des samplers. L'historique du dépôt identifie sept commits ce jour-là, dont l'enregistrement dans le registry, `disk buffered workflows`, les deux exemples spécifiques aux modèles et `timer nodes added`.
- **2026-08-07** — Les workflows d'exemple ont été mis à jour.
- **2026-08-08** — La fusion disque a été découplée et un aperçu des tuiles a été ajouté, ce qui permet un chemin d'assemblage et de revue indépendant, basé sur un dossier, après le traitement des tuiles.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-05, nous considérons le dépôt GitHub lié comme la référence confirmée du projet. Vérifiez la documentation et la compatibilité actuelles avant toute utilisation.

1. Installez dans `ComfyUI/custom_nodes` avec `git clone https://github.com/maDcaDDie2000/comfyui-video-tiler`, puis redémarrez ComfyUI ; les nœuds standard apparaissent sous Video Tiler et les nœuds disque sous Video Tiler/Disk.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
2. Pour un clip qui tient en mémoire, connectez l'un des slicers au workflow d'upscale, puis transmettez la liste de tuiles traitées et le `tile_config` inchangé à Video Tile Merge.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
3. Pour un traitement en VRAM limitée, créez un Disk Job, traitez et sauvegardez chaque tuile indexée, puis utilisez Disk Folder Merge avec le dossier de tâche terminé ou le manifeste, et envoyez ses sorties IMAGE/audio vers un encodeur vidéo.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Bonnes pratiques {#best-practices}

- Gardez `tile_config` associé au slicer qui l'a créé ; utilisez le chevauchement et le feathering pour éviter les jointures franches.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Utilisez le traitement avec tampon disque lorsque les tuiles traitées ne peuvent pas rester en cache, mais prévoyez la mémoire nécessaire à l'IMAGE finale fusionnée à pleine taille.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Utilisez les workflows LTX 2.3 ou MiniMax H3 fournis comme point de départ ; les autres piles de modèles sortent du périmètre principal testé du pack.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Remplacé par ces éléments {#superseded-by-this}

- 2026-08-05 — Les workflows de tuiles à tampon disque remplacent les consignes purement en mémoire pour le matériel contraint.
- 2026-08-08 — La fusion et l'aperçu indépendants basés sur un dossier remplacent la fusion disque limitée au graphe connecté, lorsque c'est pertinent.

## Points encore inconnus {#still-unknown}

- Le dépôt ne publie pas de tags de version formels dans les sources consultées ; les modifications d'août 2026 sont donc identifiées par la date des commits et non par une version publiée.
- Le schéma de sortie ne comporte pas de champs dédiés aux conclusions d'événements ni aux nouveaux événements ; `what_changed` enregistre leur contenu requis.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/maDcaDDie2000/comfyui-video-tiler | Dépôt ComfyUI Video Tiler et README | 2026-09-05 |
| https://github.com/maDcaDDie2000/comfyui-video-tiler/commits/main | Historique des commits de ComfyUI Video Tiler | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui-video-tiler`, fil `comfyui-video-tiler`, 1 événement daté du 2026-08-05 au 2026-08-05.
- **Note pratique :** Au 2026-08-05, les praticiens peuvent considérer le dépôt GitHub lié comme la référence confirmée du projet, tout en vérifiant sa documentation et sa compatibilité actuelles avant utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
