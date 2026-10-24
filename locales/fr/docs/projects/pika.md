---
title: "Pika"
category: projects
date: 2025-02-07
tags: [pika, pika-product-development, pika_camera_control, pikadditions, project]
aliases: ["Pika", "Pika AI Selves"]
level: 2
source_sha256: 54ba5be063a88d54812abc8698646f3f8df01697d239a59acc6925f0458c389f
translation: machine
translated_at: '2026-10-24'
---
# Pika {#pika}

**Ligne de développement :** `project:pika` · fil `pika-product-development`  
**Dernier événement :** 2025-02-07 · 2 événements datés depuis 2023-09-12 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Pika : une plateforme cloud pour les créateurs de vidéos courtes, concurrente de Runway en text-to-video, image-to-video et video-to-video. Fonctionnalités : Pika 2.5, Pikaframes, Pikascenes, Pikadditions, Pikaswaps, Pikatwists et Pikaffects. Limite dans la grille tarifaire actuelle : vidéos principales de 5 ou 10 secondes, Pikaframes jusqu'à 25 secondes. Verdict : adapté aux générations rapides et aux transformations spectaculaires, mais ne remplace pas le compositing image par image ni un montage long.

## Ligne de développement {#development-line}

- **2023-09-12 — Développement du contrôle de caméra Pika enregistré.** Zoom, panoramique et rotation ; les directions de panoramique peuvent être combinées, mais les types de mouvement non.
- **2025-02-07 — Pika Additions est entré dans la gamme de produits de Pika.** Le 2025-02-07, une URL officielle de Pika a désigné une fonctionnalité nommée, Pika Additions. Le lien daté n'établit ni son fonctionnement, ni sa disponibilité, ni l'étendue de son déploiement ; cet événement n'enregistre donc que l'apparition de cette fonctionnalité nommée.

## Ce qui a changé {#what-changed}

2023-09-12 — La version Discord a reçu le paramètre -camera : zoom, panoramique et rotation ; les directions de panoramique peuvent être combinées, mais les types de mouvement non. 2023-11-29 — Pika 1.0 a fait passer le produit d'un bot Discord à une nouvelle interface web et à un nouveau modèle de génération et d'édition vidéo dans des styles 3D, anime, dessin animé et cinématographique. 2025-02-07 — Pikadditions a ajouté l'insertion video-to-video d'une personne ou d'un objet dans une vidéo existante ; une source datée indépendante indique un lancement le 6 février 2025. 2026-02-28 — Le contenu de la publication X associée n'a pas pu être vérifié : la page n'a pas fourni de texte. Il n'est pas possible de relier de manière fiable à cette date un modèle ou une version précis. 2025-04-10 — Pikaframes a reçu des transitions et des transformations entre cinq images au maximum, pour une durée totale allant jusqu'à 25 secondes. 2025-04-24 — Pikatwists est apparu, permettant de décrire par texte la transformation d'une vidéo. 2025-05-01 — De nouveaux Pikaffects sont apparus ; la prise en charge d'une entrée vidéo est signalée dans l'historique de l'application le 9 mai 2025. 2026-01-26 — L'historique de l'application a enregistré Pika 2.5 ; la page tarifaire actuelle le présente comme modèle disponible pour le text-to-video et l'image-to-video.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-09-12 et du 2025-02-07, les praticiens doivent suivre le contrôle de caméra et Pika Additions comme deux domaines de capacités distincts de Pika, et vérifier le comportement actuel ainsi que l'accès avant de s'appuyer sur l'un ou l'autre dans un flux de travail de production.

1. Connectez-vous à Pika et choisissez un mode : text-to-video, image-to-video, Pikaframes, Pikadditions, Pikaswaps, Pikatwists ou Pikaffects.
  — <https://pika.art/pricing>
2. Pour Pikadditions, chargez la vidéo source, éventuellement une image de référence de l'objet, puis décrivez l'ajout par texte ; l'API accepte les résolutions 720p ou 1080p et des durées de 5 ou 10 secondes.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
3. Pour l'API, téléversez d'abord le fichier média local via un presigned upload, puis transmettez l'URL renvoyée dans la requête de génération.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
4. Conservez l'identifiant de la tâche asynchrone, interrogez-la jusqu'à completed ou failed, et ne demandez l'URL du résultat qu'ensuite.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Bonnes pratiques {#best-practices}

- Pour un mouvement contrôlé dans le mode Discord historique, placez -camera sans espace avant le tiret ; utilisez zoom, pan ou rotate et ne combinez pas des types de mouvement incompatibles.
  — <https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml>
- Pour l'API, définissez un Idempotency-Key pour une requête reproductible et ne modifiez pas le corps de la requête lorsque la clé est réutilisée.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Ne considérez pas un état queued ou running comme une vidéo prête : traitez completed et failed comme des états terminaux, et gérez une réponse 429 en respectant Retry-After.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Ne choisissez pas Pikadditions pour la rotoscopie image par image, le compositing au pixel près ou la vidéo de longue durée ; la documentation classe explicitement ces tâches comme inadaptées.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Remplacé par ceci {#superseded-by-this}

- 2023-09-12 — L'ancienne syntaxe Discord -camera est historique et ne décrit pas le produit web actuel.
- 2023-11-29 — Pika 1.0 et son ancienne expérience web ont été remplacés par les gammes ultérieures, dont Pika 2.5 dans la grille tarifaire actuelle.
- 2025-02-07 — La première description de Pikadditions comme seule nouveauté est obsolète : la gamme actuelle comprend aussi Pikascenes, Pikaswaps, Pikatwists, Pikaffects et Pikaframes.

## Toujours inconnu {#still-unknown}

- La publication X du 2026-02-28 n'a pas fourni de texte lors de la vérification ; son contenu, le modèle précis et l'ampleur du changement sont inconnus.
- Les références de 2023 à Discord et à The source n'ont pas pu être consultées de manière indépendante ; le contrôle de caméra et Pika 1.0 sont confirmés par des sources secondaires datées.
- Le sujet Pika AI Selves n'est confirmé par aucune source disponible comme produit ou fonctionnalité distincte de Pika ; il s'agit peut-être d'une appellation distincte dans les messages d'origine.
- Les champs distincts demandés event_findings et new_events ne sont pas prévus par le schéma de réponse imposé ; leurs faits sont conservés dans la chronologie de what_changed.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml | Pika Labs推出影像控制新功能,-camera提升视觉丰富度 | 2026-09-05 |
| https://petapixel.com/2023/11/28/generative-video-startup-pika-labs-launches-version-1-0-raises-55-million-in-funding/ | Generative Video Startup Pika Labs Launches Version 1.0, Raises $55 Million in Funding | 2026-09-05 |
| https://pika.art/blog | Blog | Pika | 2026-09-05 |
| https://pika.art/pikadditions | Pika | 2026-09-05 |
| https://www.tomsguide.com/ai/ai-image-video/pika-labs-launches-pikadditions-to-add-anything-and-anyone-to-any-video-heres-how | Pika Labs launches 'Pikadditions' to add anything and anyone to any video — here's how | 2026-09-05 |
| https://mcp.pika.art/models/pika/pikadditions/video-to-video | Pikadditions | Pika API | 2026-09-05 |
| https://pika.art/pricing | Subscription Pricing | Pika | 2026-09-05 |
| https://apps.apple.com/us/app/pika-ai-video/id6680155400?platform=vision | Pika - AI Video App - App Store | 2026-09-05 |
| https://x.com/pika_labs/status/2027549433261658534 | x.com | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:pika`, fil `pika-product-development`, 2 événements datés du 2023-09-12 au 2025-02-07.
- **Note pratique :** À partir du 2023-09-12 et du 2025-02-07, les praticiens doivent suivre le contrôle de caméra et Pika Additions comme deux domaines de capacités distincts de Pika, et vérifier le comportement actuel ainsi que l'accès avant de s'appuyer sur l'un ou l'autre dans un flux de travail de production.
- **Confiance :** moyenne. Les mentions « Remplacé par ceci » datées font autorité pour ce qui est obsolète.
