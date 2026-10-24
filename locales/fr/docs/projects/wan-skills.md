---
title: "WAN"
category: "projects"
date: 2026-09-26
tags: ["project", "wan", "wan-skills", "wan-video-generation"]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
level: 2
source_sha256: 843f0d7a364cd697f2a450a59c1ac122a9d34804322cf52522e7a6fad9bbfeb5
translation: machine
translated_at: '2026-10-24'
---
# WAN {#wan}

**Ligne de développement :** project:wan-skills · fil wan-video-generation  
**Dernier événement :** 2026-09-26 · 6 entrées datées depuis 2025-09-23 · **Consulté le :** 2026-09-26 · confiance : faible

## Ce que c'est {#what-it-is}

WAN Skills est un paquet GitHub d'Alibaba Wan destiné aux développeurs d'agents. Il comprend une compétence de génération et d'édition d'images wan2.7 ainsi qu'une compétence de génération de PPTX. Il fournit des scripts d'appel d'API, des utilitaires d'envoi de fichiers et de consultation de l'état des tâches, ainsi que des instructions de référence. Le dépôt public recense actuellement deux répertoires de compétences. Utilisez-le pour l'intégration côté agent avec les API Wan. Il ne montre pas que le produit web de WAN a publié une marketplace d'effets vidéo.

## Ligne de développement {#development-line}

- **2025-09-23 — Alibaba Wan 2.5 apparaît comme modèle texte-vers-vidéo sur WaveSpeed.** Le 2025-09-23, une route de modèle WaveSpeed identifiait Alibaba Wan 2.5 comme offre texte-vers-vidéo. Les praticiens disposaient ainsi d'une route hébergée et nommée pour la génération vidéo avec cette version de WAN.
- **2025-10-01 — Des ressources Wan 2.2 Lightning apparaissent pour des workflows texte-vers-vidéo en quatre étapes.** Le 2025-10-01, les ressources liées identifiaient une variante Dyno Wan 2.2 Lightning à quatre étapes, un artefact ComfyUI FP8 correspondant et une page de workflow. Ensemble, elles indiquent une voie d'inférence plus rapide et prête à l'emploi pour la génération texte-vers-vidéo avec Wan 2.2.
- **2026-04-17 — Mise à jour de WAN.** Wan-skills était publiquement signalé comme mis à jour, avec deux répertoires de compétences documentés : wan2.7-image-skill et wan-pptx-generator.
- **2026-07-31 — WAN expose une route de playground temps réel.** Le 2026-07-31, le site WAN Create comprenait une route de playground de laboratoire intitulée realtime. Cela indique un point d'entrée interactif en temps réel pour WAN, distinct d'un lien de téléchargement de modèle ou de workflow par lots.
- **2026-09-26 — WAN lance une fonctionnalité de compétences sur sa plateforme.** WAN lance une fonctionnalité de plateforme appelée « skills » composée de préréglages de manipulation vidéo, en référence à des effets issus à l'origine de Pika. Le lancement est présenté comme actuel alors qu'il repose sur les effets de l'année précédente.
- **2026-09-26 — WAN lance une fonctionnalité skills sur sa plateforme.** WAN a lancé des skills (préréglages de manipulation vidéo) sur sa plateforme. Les effets sont décrits comme venant de l'année précédente et sont désormais rebaptisés compétences. Cela marque une nouvelle étape de développement pour le projet WAN.

## Ce qui a changé {#what-changed}

Les éléments publics ne permettent pas de vérifier de façon indépendante un changement daté de la fonctionnalité web de WAN citée. Le dépôt Wan-skills documenté séparément a été mis à jour pour la dernière fois le 2026-04-17 et expose des compétences d'intégration d'agents, et non les préréglages de plateforme annoncés.

## Comment l'utiliser {#how-to-use-this}

1. Créez un compte Alibaba Cloud, activez ModelStudio et créez une clé d'API DashScope.
  — <https://github.com/Wan-Video/Wan-skills>
2. Définissez DASHSCOPE\_API\_KEY et sélectionnez l'URL de base DashScope correspondant à la région visée.
  — <https://github.com/Wan-Video/Wan-skills>
3. Clonez Wan-skills et installez le répertoire de compétences requis dans l'agent IA, par exemple skills/wan2.7-image-skill.
  — <https://github.com/Wan-Video/Wan-skills>
4. Pour les travaux d'image, fournissez une consigne textuelle et, éventuellement, des URL d'images. Le script fourni soumet une tâche asynchrone wan2.7-image et vérifie son état.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Bonnes pratiques {#best-practices}

- Choisissez explicitement le point de terminaison régional DashScope au lieu de vous fier à une région de déploiement non précisée.
  — <https://github.com/Wan-Video/Wan-skills>
- Traitez la génération d'image comme asynchrone et conservez l'identifiant de tâche jusqu'à ce que l'état atteigne un résultat final.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- La page web WAN citée n'a renvoyé aucun contenu accessible lors de l'examen. La publication annoncée du 2026-09-26 sur la plateforme, son périmètre de manipulation vidéo, son nombre de préréglages et tout lien avec les effets de Pika n'ont pas pu être vérifiés.
- Les éléments publics attestent d'un projet GitHub officiel nommé Wan-skills, qui documente l'intégration par API d'agents IA pour la création d'images, l'édition d'images et la génération de PPTX. Ils n'établissent pas qu'il s'agisse du même produit que la page de compétences create.wan.video citée.
- Les deux entrées examinées du même jour peuvent décrire un seul changement de page de plateforme indisponible plutôt que deux publications distinguables.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://create.wan.video/lab/skill | WAN Skills | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills | Wan-Video/Wan-skills | 2026-09-27 |
| https://github.com/wan-video | Wan-Video sur GitHub | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py | image-generation-editing.py | 2026-09-27 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** project:wan-skills, fil wan-video-generation, 6 événements datés du 2025-09-23 au 2026-09-26.
- **Remarque pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** faible. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
