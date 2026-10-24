---
title: "RealityScan — Lancement et sortie de la photogrammétrie mobile"
category: projects
date: 2022-12-05
tags: [mobile-photogrammetry-launch-and-release, project, realityscan, realityscan_beta_launch]
aliases: ["RealityScan"]
level: 2
source_sha256: dc4c6666a73a7a7f2b5b83e9e3d20934902e59c9250a01ef11514013b1c2046e
translation: machine
translated_at: '2026-10-24'
---
# RealityScan — Lancement et sortie de la photogrammétrie mobile {#realityscan-mobile-photogrammetry-launch-and-release}

**Ligne de développement :** `project:realityscan` · fil `mobile-photogrammetry-launch-and-release`  
**Dernier événement :** 2022-12-05 · 2 datés depuis 2022-04-04 · **Recherché :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

RealityScan est un outil destiné aux créateurs d'assets 3D : l'application mobile capture un objet avec une série de photos et traite le modèle dans le cloud, tandis que la version de bureau travaille à partir de photos et de scans laser. La version mobile nécessite iOS 16+ ou Android 7+ avec ARCore ; la version de bureau est gratuite jusqu'à 1 M$ de chiffre d'affaires annuel. Verdict : pour une capture rapide d'objets, la version mobile convient ; pour une prise de vue précise et de grands jeux de données, il faut RealityScan Desktop.

## Ligne de développement {#development-line}

- **2022-04-04 — RealityScan Beta Was Introduced.** Une bêta mobile limitée de RealityScan a démarré : 10 000 places TestFlight, traitement de photos en modèle 3D et export via Sketchfab.
- **2022-12-05 — RealityScan Reached Public Availability.** L'application est sortie de la bêta en version gratuite pour iOS/iPadOS ; à la date de sortie, Android n'était pas encore pris en charge.

## Ce qui a changé {#what-changed}

2022-04-04 : une bêta mobile limitée de RealityScan a démarré — 10 000 places TestFlight, traitement de photos en modèle 3D et export via Sketchfab. 2022-12-05 : l'application est sortie de la bêta en version gratuite pour iOS/iPadOS ; à la date de sortie, Android n'était pas encore pris en charge. 2023-06-20 : la version mobile est devenue disponible sur Android et a reçu un workflow pas à pas ; Epic a annoncé plus de 200 000 téléchargements de la version iOS. 2024-06-24 : RealityScan Mobile 1.5 a ajouté le téléchargement local des modèles, la publication facultative sur Sketchfab et l'export OBJ sur iOS ou GLB sur Android. 2025-06-17 : le logiciel professionnel RealityCapture a été renommé RealityScan ; RealityScan 2.0 est devenu le produit de bureau, et l'application téléphone s'appelle désormais RealityScan Mobile. 2026-06-24 : RealityScan 2.2 a ajouté la reconstruction accélérée matériellement sur les AMD Radeon et Ryzen AI Max pris en charge sous Windows.

## Comment l'utiliser {#how-to-use-this}

À partir du 2022-12-05, les praticiens pouvaient considérer RealityScan comme une option de photogrammétrie mobile accessible au public, et non plus seulement comme une bêta récemment annoncée.

1. Vérifiez la compatibilité de l'appareil : iOS 16+ ou Android 7+ avec ARCore, puis installez l'application et connectez-vous avec un compte Epic Games.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US>
2. Créez un projet en Augmented Reality Mode et faites le tour de l'objet en plusieurs arcs à différentes hauteurs ; la limite de capture est de 300 images.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
3. Examinez le nuage de points, limitez la reconstruction region, lancez le traitement et attendez le statut Processed.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
4. Ouvrez View/Edit Scan, recadrez le résultat et exportez le modèle sur l'appareil ou envoyez-le sur Sketchfab.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
5. Pour le traitement sur ordinateur, installez la version souhaitée depuis l'onglet RealityScan dans Epic Games Launcher.
  — <https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan>

## Bonnes pratiques {#best-practices}

- Gardez l'objet dans le cadre à au moins 50 % et assurez une couverture à fort recouvrement sur tous les côtés accessibles : les zones invisibles dans plusieurs images n'apparaîtront pas dans le modèle.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Ne basculez pas vers une autre application pendant le téléchargement et l'analyse initiale, afin de ne pas interrompre le workflow de capture.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Avant le traitement, supprimez l'arrière-plan et les points superflus de la reconstruction region : tout ce qui se trouve hors de la zone n'est pas reconstruit.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Pour une capture contrôlée, utilisez le Camera Control Mode et conservez des réglages de lumière et de flash constants pendant une même session.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US>

## Remplacé par ceci {#superseded-by-this}

- 2022-04-04 : la bêta TestFlight limitée et la promesse d'un futur accès anticipé iOS ont été remplacées par l'application mobile publique.
- 2022-12-05 : le statut réservé à iOS est devenu obsolète après la sortie Android du 2023-06-20.
- 2022-12-05 : l'export obligatoire via Sketchfab est devenu obsolète avec RealityScan Mobile 1.5 du 2024-06-24, qui a ajouté le téléchargement local des modèles.
- 2025-06-17 : le nom RealityCapture, utilisé comme nom actuel du produit de bureau, a été remplacé par RealityScan ; l'ancien nom n'est plus conservé que pour les versions et licences héritées.

## Toujours inconnu {#still-unknown}

- Le schéma de réponse défini ne comporte pas les champs event_findings et new_events ; les données complémentaires sur les événements ont donc été intégrées dans what_changed et supersedes.
- Les événements du 2022-04-04 et du 2022-12-05 appartiennent à la même ligne mobile de RealityScan ; le RealityScan de bureau n'existe sous ce nom qu'depuis le renommage de RealityCapture en 2025.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://www.capturingreality.com/introducing-realityscan | Introducing RealityScan: Now in Limited Beta | 2026-09-05 |
| https://habr.com/ru/news/t/703566/ | Scanner 3D mobile RealityScan d'Epic Games sorti de la bêta et disponible sur l'App Store | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-free-to-download-on-ios/717656 | RealityScan is now free to download on iOS | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-available-for-android-devices/1204921 | RealityScan is now available for Android devices! | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-1-5-0-release-notes/1914888 | RealityScan 1.5.0 Release Notes | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-20-new-release-brings-powerful-new-features-to-a-rebranded-realitycapture | RealityScan 2.0: New release brings powerful new features to a rebranded RealityCapture | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-2-2-is-here-with-full-amd-gpu-support-download-today | RealityScan 2.2 is here with full AMD GPU support—download today | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US | RealityScan System Requirements and Setup | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide | RealityScan Step by Step Guide | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US | RealityScan Mobile 1.6 Release Notes | 2026-09-05 |
| https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan | Getting RealityScan | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:realityscan`, fil `mobile-photogrammetry-launch-and-release`, 2 événements datés du 2022-04-04 au 2022-12-05.
- **Note pratique :** à partir du 2022-12-05, les praticiens pouvaient considérer RealityScan comme une option de photogrammétrie mobile accessible au public, et non plus seulement comme une bêta récemment annoncée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
