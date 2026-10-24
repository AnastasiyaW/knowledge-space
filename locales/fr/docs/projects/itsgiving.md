---
title: "Itsgiving : itsgiving"
category: "projects"
date: 2026-09-12
tags: ["itsgiving", "project"]
aliases: ["Itsgiving: itsgiving"]
level: 2
source_sha256: 031cd37ad35acf3302daa068c72406eedb9557912a9c1cae2835a3bbe2c13a2f
translation: machine
translated_at: '2026-10-24'
---
# Itsgiving : itsgiving {#itsgiving-itsgiving}

**Ligne de développement :** project:itsgiving · fil itsgiving  
**Dernier événement :** 2026-09-12 · 2 datés depuis le 2026-09-12 · **Recherché le :** 2026-09-12 · confiance : moyenne

## Description {#what-it-is}

ItsGiving est un outil Python de webcam destiné aux participants à des réunions. Il détecte les expressions du visage et les postures des mains et du corps, puis superpose des images ou des GIF correspondants. Il publie le résultat sous forme de caméra virtuelle.

Il comprend 14 réactions intégrées, des ressources et postures personnalisées, ainsi qu'un détecteur v2 calibré. Il nécessite Python 3.11 ou 3.12. Au premier lancement, il télécharge trois modèles MediaPipe représentant environ 15 Mo au total.

Utilisez le script v2 calibré. Le projet documente la v1 comme un comportement hérité à seuils fixes.

## Ligne de développement {#development-line}

- **2026-09-12 — ItsGiving - Face/Gesture-to-Meme Streaming Tool.** Un outil de webcam qui suit le visage et les gestes et affiche des mèmes correspondants dans un flux. Il s'intègre à Zoom, Meet, Discord et Teams.
  - Le projet documente 14 réactions et une sortie de caméra virtuelle pour Zoom, Meet, Teams, Discord et OBS. L'implémentation recommandée est \`its\_giving\_v2.py\`. Elle enregistre une référence de visage neutre de sept secondes et évalue les expressions par rapport à celle-ci. (date non précisée) — <https://github.com/gazijarin/itsgiving>
  - Le projet documente 14 réactions et une sortie de caméra virtuelle pour Zoom, Meet, Teams, Discord et OBS. L'implémentation recommandée est \`its\_giving\_v2.py\`. Elle enregistre une référence de visage neutre de sept secondes et évalue les expressions par rapport à celle-ci. (date non précisée) — <https://github.com/gazijarin/itsgiving>
- **2026-09-12 — ItsGiving Webcam Tool with Face/Gesture Tracking and Meme Integration.** Un outil de webcam qui suit le visage et les gestes et affiche des mèmes correspondants dans un flux. Il s'intègre à Zoom, Meets, Discord et Teams.
  - Le projet documente 14 réactions et une sortie de caméra virtuelle pour Zoom, Meet, Teams, Discord et OBS. L'implémentation recommandée est \`its\_giving\_v2.py\`. Elle enregistre une référence de visage neutre de sept secondes et évalue les expressions par rapport à celle-ci. (date non précisée) — <https://github.com/gazijarin/itsgiving>
  - Le projet documente 14 réactions et une sortie de caméra virtuelle pour Zoom, Meet, Teams, Discord et OBS. L'implémentation recommandée est \`its\_giving\_v2.py\`. Elle enregistre une référence de visage neutre de sept secondes et évalue les expressions par rapport à celle-ci. (date non précisée) — <https://github.com/gazijarin/itsgiving>

## Modifications {#what-changed}

Le dépôt public documente une implémentation v2 calibrée à côté de l'implémentation v1 à seuils fixes. Aucune étape de développement datée séparément, postérieure à la date examinée, n'a été vérifiée.

## Mode d'emploi {#how-to-use-this}

1. Créez un environnement virtuel Python 3.11 ou 3.12 et installez les dépendances épinglées.
  — <https://github.com/gazijarin/itsgiving>
2. Exécutez \`python its\_giving\_v2.py --calibrate\`. Restez neutre pendant la calibration de sept secondes, puis exécutez \`python its\_giving\_v2.py\`.
  — <https://github.com/gazijarin/itsgiving>
3. Installez un pilote de caméra virtuelle pour votre système d'exploitation. Lancez ItsGiving avant l'application de réunion, puis sélectionnez la caméra virtuelle publiée dans les paramètres vidéo de cette application.
  — <https://github.com/gazijarin/itsgiving>

## Bonnes pratiques {#best-practices}

- Ne modifiez pas les versions épinglées des dépendances. Les contraintes de compatibilité documentées entre MediaPipe, NumPy et OpenCV sont liées.
  — <https://github.com/gazijarin/itsgiving>
- Utilisez la v2 et recalibrez si nécessaire. Ses seuils d'expression reposent sur la référence de visage neutre de l'utilisateur.
  — <https://github.com/gazijarin/itsgiving>
- Lors de l'ajout d'une posture, vérifiez l'ordre des postures avant d'abaisser les seuils. La première posture correspondante l'emporte. Utilisez le HUD et un compteur de bras pour ajuster les fausses détections.
  — <https://github.com/gazijarin/itsgiving>
- Testez les réactions avant de les utiliser dans une réunion. La sortie peut se déclencher automatiquement et est visible de tous les participants à l'appel.
  — <https://github.com/gazijarin/itsgiving>

## Remplacé par {#superseded-by-this}

- Rien de marqué comme obsolète pour le moment.

## Inconnues restantes {#still-unknown}

- La page du dépôt public n'est pas datée. Elle corrobore les entrées du 2026-09-12 examinées, mais elle n'établit pas l'heure exacte de publication et ne montre pas laquelle des deux entrées du même jour correspond à une modification distincte du projet.
- L'URL VK examinée n'a pas pu être récupérée publiquement pendant cette recherche.
- Aucune source utile en chinois simplifié sur ce projet précis n'a été trouvée.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/gazijarin/itsgiving | gazijarin/itsgiving — It's giving... | 2026-09-13 |

## Résumé pour l'agent {#agent-brief}

- **Sujet :** project:itsgiving, fil itsgiving, 2 événements datés du 2026-09-12 au 2026-09-12.
- **Note pratique :** voir les sections sourcées sur l'usage et les bonnes pratiques ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
