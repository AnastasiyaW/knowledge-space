---
title: "ATI : Any Trajectory Instruction"
description: "ATI ajoute un contrôle du mouvement d'objet, de zone locale et de caméra fondé sur des trajectoires à son workflow image-vers-vidéo basé sur Wan2.1 ; préserver les limites du modèle publié, du checkpoint et de l'éditeur localhost."
category: models
tags: [video-generation, trajectory-control, camera-motion, object-motion, wan2.1, bytedance]
aliases: ["Any Trajectory Instruction"]
level: 2
source_sha256: 3ea3a8ff458dfca565fec3085f33723645859c13a62c17231e465aad5fecdd09
translation: machine
translated_at: '2026-10-24'
---
# ATI : Any Trajectory Instruction {#ati-any-trajectory-instruction}

**Périmètre vérifié : 2026-09-04.** ATI est l'extension de contrôle par trajectoires publiée par ByteDance pour la génération image-vers-vidéo. Elle représente les mouvements d'objet, de zone locale et de caméra sous forme de trajectoires, puis injecte le signal de mouvement obtenu dans le workflow image-vers-vidéo de Wan2.1. L'implémentation officielle est une intégration spécifique basée sur Wan2.1, et non un module de contrôle générique pour tous les modèles vidéo.

## Ce qu'elle contrôle {#what-it-controls}

ATI utilise des trajectoires de points pour exprimer plusieurs intentions de mouvement via une interface unique :

- **mouvement d'objet** — trajectoires ancrées sur le sujet ou sur une zone locale ;
- **mouvement local** — déplacement dirigé pour des zones choisies de l'image ;
- **mouvement de caméra** — trajectoires coordonnées, comme un panoramique ou un zoom ;
- **transfert de mouvement** — extraire des pistes d'une vidéo source et les appliquer à une nouvelle image de première frame.

Le résultat dépend toujours du modèle de base, de la première frame, du prompt, du placement des trajectoires et de la vitesse de mouvement. Un chemin tracé est une instruction, et non une garantie que les parties occultées ou ambiguës de l'image resteront physiquement cohérentes.

## Limites d'exécution publiées {#published-runtime-boundary}

Le dépôt officiel repose sur l'implémentation Wan2.1. Son guide d'installation exige le modèle original `Wan2.1-I2V-14B-480P`, un checkpoint ATI distinct, ainsi que la copie du VAE original, de l'encodeur de texte et des autres composants requis dans l'emplacement du checkpoint ATI. Conservez ces artefacts et leurs révisions ensemble dans un enregistrement d'exécution immuable.

Avant utilisation, vérifiez :

1. la révision du dépôt ATI et l'environnement Wan2.1 correspondant ;
2. la complétude du checkpoint et les chemins locaux ;
3. le format YAML/d'entrée utilisé par l'exemple actuel ou le wrapper d'API ;
4. la mémoire GPU disponible, la durée de la vidéo, la résolution et l'emplacement de sortie ;
5. une petite fixture de trajectoire connue avant un lot de rendu plus important.

Un support ComfyUI communautaire existe via des nœuds tiers. Traitez-le comme une intégration distincte, avec ses propres contrôles de version, de sécurité et de sortie ; il ne constitue pas une preuve interchangeable pour le dépôt amont.

## Sécurité de l'éditeur de trajectoires {#trajectory-editor-safety}

Le projet amont demande explicitement aux opérateurs d'exécuter son éditeur interactif de trajectoires en localhost. N'exposez pas directement cette interface de développement à un réseau non fiable. Si un workflow distant est nécessaire, placez devant elle une authentification, une surface de téléversement contrainte, une isolation par tâche, des limites de ressources et des reçus de tâche conservés.

## Contrôles d'acceptation {#acceptance-checks}

Pour chaque sortie, vérifiez si le sujet visé a bien bougé, si les zones statiques sont restées stables, si le mouvement de caméra demandé a eu lieu, et si le résultat produit des artefacts à la taille de lecture finale. Conservez l'image source, le fichier de trajectoire, le prompt, les révisions de base et d'ATI, les réglages, la sortie et le résultat de la revue. Relancez une fixture bornée après toute mise à jour d'ATI ou de Wan.

Le dépôt ATI est sous licence Apache-2.0, mais le modèle de base Wan, les checkpoints et tout wrapper communautaire peuvent avoir des conditions distinctes. Vérifiez la licence et les conditions d'accès actuelles de chaque artefact.

## Références {#references}

- [Dépôt officiel ATI](https://github.com/bytedance/ATI)
- [Article ATI](https://arxiv.org/abs/2505.22944)
- [Collection de checkpoints ATI](https://huggingface.co/bytedance-research/ATI)
- [Community ComfyUI Wan Video Wrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper)
