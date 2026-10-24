---
title: "OpenPose Studio for ComfyUI — Développement du projet"
category: projects
date: 2026-07-28
tags: [comfyui-openpose-studio, comfyui_openpose_studio, project, project-development]
aliases: ["OpenPose Studio for ComfyUI"]
level: 2
source_sha256: f4301fc023d765bed1ddb90fa6a9f056b7d624069c88849372d9ccb1b1f01733
translation: machine
translated_at: '2026-10-24'
---
# OpenPose Studio for ComfyUI — Développement du projet {#openpose-studio-for-comfyui-project-development}

**Ligne de développement :** `project:comfyui-openpose-studio` · fil `project-development`  
**Dernier événement :** 2026-07-28 · 1 événement daté depuis le 2026-07-28 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

OpenPose Studio for ComfyUI est un éditeur de poses intégré à ComfyUI, destiné à l'artiste qui veut corriger le squelette, les mains ou le JSON, plutôt que d'accepter tel quel le résultat du pose-estimator. Fonctionnalités : corps COCO-18, édition point par point des mains, galerie et fusion de poses JSON, entrée DWPose et sorties IMAGE/JSON/KPS. Limite : les points du visage sont conservés et rendus, mais ne sont pas éditables individuellement. Verdict : c'est une alternative pratique à un éditeur OpenPose autonome lorsque le contrôle de la pose est déjà nécessaire dans le graphe ComfyUI.

## Ligne de développement {#development-line}

- **2026-07-28 — dépôt ComfyUI-OpenPose-Studio référencé.** L'éditeur de mains dispose désormais d'un espace de travail plus grand, et les références d'arrière-plan ainsi que les guides ont été corrigés pour le mode agrandi.

## Ce qui a changé {#what-changed}

Le 2026-07-28, l'état le plus proche disponible était OpenPose Studio 2.0.2 : l'éditeur de mains a gagné un espace de travail plus grand, et les références d'arrière-plan et les guides ont été corrigés pour le mode agrandi. Le 2026-07-29, la version 2.1.0 a ajouté un aperçu de la pose sélectionnée dans Gallery, 14 gestes de main et des outils de restauration et de suppression des points de main. Le 2026-07-30, la version 2.1.1 a ajouté la localisation en hindi. Le 2026-08-08, la version 2.2.0 a ajouté l'insertion d'une main manquante par glisser-déposer, le choix de l'orientation de la paume et une notification de mise à jour. Le 2026-08-14, la version 2.3.0 a ajouté une interface tactile adaptative et une Gallery mobile compacte.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-28, les praticiens doivent considérer ComfyUI-OpenPose-Studio comme un projet à évaluer à partir de son dépôt GitHub associé ; les données disponibles ne permettent pas encore de formuler une recommandation plus précise d'installation ou de flux de travail.

1. Dans l'Extension Manager de ComfyUI, ouvrez le Nodes Manager, recherchez `openpose-studio`, installez l'extension et redémarrez ComfyUI.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
2. Ajoutez le nœud `image > OpenPose Studio`, ouvrez l'éditeur via l'aperçu, sélectionnez une pose depuis un préréglage ou la Gallery, puis faites glisser les points clés.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
3. Cliquez sur Apply ; connectez `image` aux nœuds image suivants, et `kps` à un nœud compatible ControlNet/OpenPose.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
4. Pour corriger le résultat du détecteur, connectez la sortie du DWPose Estimator à l'entrée facultative `pose_keypoint`, puis affinez les points dans l'éditeur.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Bonnes pratiques {#best-practices}

- Avant l'import, vérifiez le JSON : il faut des coordonnées numériques et une structure contenant `pose_keypoints_2d` ; pour le corps, 18 points clés sont attendus.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Pour des poses de dimensions différentes, mettez-les d'abord à l'échelle de la résolution cible : Pose Merger n'aligne pas automatiquement la résolution de la collection.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Si l'éditeur ou l'aperçu n'apparaît pas, redémarrez complètement ComfyUI, effectuez un rechargement forcé de la page et vérifiez la console du navigateur ainsi que le journal de démarrage.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Utilisez les images d'arrière-plan comme référence temporaire : elles sont conservées pendant la session ComfyUI, mais ne sont pas enregistrées dans le workflow.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Remplacé par cette évolution {#superseded-by-this}

- 2026-07-29 : l'ancienne Gallery, sans aperçu de la pose sélectionnée ni les 14 gestes de main intégrés, est remplacée par le comportement de la version 2.1.0.
- 2026-08-08 : l'ancienne méthode manuelle d'ajout des mains manquantes est remplacée par l'insertion prise en charge par glisser-déposer sur le canevas, dans la version 2.2.0.
- 2026-08-14 : l'ancienne mise en page orientée bureau est remplacée par les vues tactiles adaptatives de la version 2.3.0.

## Points non élucidés {#still-unknown}

- Pour l'événement du 2026-07-28, aucune version ni aucun commit distinct portant exactement cette date n'a été trouvé. La version 2.0.2, dernière version confirmée, est datée du 2026-07-27 dans le changelog de l'auteur ; ses détails sont donc présentés comme une précision de l'événement, et non comme une nouvelle étape du 2026-07-28.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/andreszs/ComfyUI-OpenPose-Studio | andreszs/ComfyUI-OpenPose-Studio — dépôt | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/CHANGELOG.md | Changelog d'OpenPose Studio | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md | Documentation d'OpenPose Studio | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-openpose-studio`, fil `project-development`, 1 événement daté du 2026-07-28 au 2026-07-28.
- **Note pratique :** Au 2026-07-28, les praticiens doivent considérer ComfyUI-OpenPose-Studio comme un projet à évaluer à partir de son dépôt GitHub associé ; les données disponibles ne permettent pas encore de formuler une recommandation plus précise d'installation ou de flux de travail.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
