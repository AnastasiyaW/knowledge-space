---
title: "ComfyUI_StarNodes"
category: projects
date: 2026-07-18
tags: [comfyui-starnodes, project]
aliases: ["ComfyUI_StarNodes"]
level: 3
source_sha256: 91b9704ed78359f74eed1503cf5d90ec1b00e3469a586a1557f6d0be38d17364
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI_StarNodes {#comfyui_starnodes}

**Ligne de développement :** `project:comfyui-starnodes` · fil `comfyui-starnodes`  
**Dernier événement :** 2026-07-18 · 1 événement daté depuis le 2026-07-18 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI_StarNodes est une suite de nœuds personnalisés sous licence MIT, destinée aux praticiens de ComfyUI qui ont besoin de workflows de démarrage, d'échantillonnage, de traitement d'image et de vidéo dans une seule extension.

- Paramètres de démarrage pour Flux, SDXL et Qwen
- Samplers, LoRA, inpainting, upscaling, sauvegarde PSD, wildcards et outils de débogage
- Outils vidéo, y compris les workflows LTX

Le README annonce 100 nœuds, `pyproject.toml` indique la version 2.7.1, et GitHub Releases ne contient aucune release. Le paquet couvre un large périmètre, mais des workflows reproductibles exigent de figer une révision et de tester les nœuds individuellement.

## Ligne de développement {#development-line}

- **2026-07-18 — Référence au dépôt GitHub de ComfyUI_StarNodes.** Le 2026-07-18, nous avons référencé le lien vers le dépôt GitHub de ComfyUI_StarNodes. Les éléments disponibles identifient le dépôt du projet, mais n'établissent ni release, ni modification de fonctionnalité, ni version, ni état d'installation. Cette entrée d'historique consigne uniquement la référence datée au dépôt.

## Modifications {#what-changed}

- **2024-11-20** — La v1.7.0 a intégré les StarBetaNodes vérifiés dans le paquet principal, y compris l'édition Qwen/WAN et des utilitaires.
- **2026-04-10** — La v2.0.0 a ajouté neuf nœuds intégrés pour la vidéo LTX et ACE Step, supprimé huit nœuds hérités et allégé les dépendances.
- **2026-07-10** — Une publication publique affirmait l'existence de la v2.1.1 avec une visionneuse de panorama à 360 degrés et un workflow mis à jour ; les artefacts de commit ou de registre sont absents.
- **2026-07-18** — Seul le lien vers le dépôt est documenté pour cette date, sans modification, version ni SHA confirmés.
- **2026-07-19** — Une publication publique affirmait les mises à jour v2.3.6 et v2.3.7 avec des améliorations de performance, de nouveaux nœuds, des mises à jour d'interface et des correctifs de compatibilité ; les artefacts de release principaux sont absents.

## Mode d'emploi {#how-to-use-this}

Considérez le dépôt ComfyUI_StarNodes lié comme une source de projet à inspecter en date du 2026-07-18, et non comme une preuve de release vérifiée ou de procédure d'installation validée.

1. Recherchez `Starnodes` dans ComfyUI Manager, installez le paquet et redémarrez ComfyUI. Si le paquet n'apparaît pas dans la liste, passez à l'installation manuelle.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
2. Pour une installation manuelle, clonez le dépôt dans `ComfyUI/custom_nodes`, installez `requirements.txt` et redémarrez ComfyUI.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
3. Installez les dépendances directement dans l'environnement Python de votre installation ComfyUI active, puis vérifiez le journal de démarrage à la recherche d'erreurs d'import après le redémarrage.
  — <https://docs.comfy.org/installation/install_custom_node>
4. Recherchez des nœuds avec `star` et commencez par un exemple pertinent : Start(t) Settings pour initialiser un graphe, Save Image+ ou PSD Saver pour la sortie, et Star Wildcards Advanced pour les données de prompt.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Examinez le dépôt et ses dépendances avant l'installation. ComfyUI recommande d'installer des nœuds personnalisés uniquement depuis des sources de confiance et de comprendre ce qu'ils font.
  — <https://docs.comfy.org/installation/install_custom_node>
- Enregistrez un instantané avant toute mise à jour, afin que Manager puisse restaurer la configuration des nœuds au prochain lancement.
  — <https://docs.comfy.org/manager/legacy-ui>
- Privilégiez une version empaquetée plutôt que la version nightly pour les graphes de production, car la documentation de Manager signale que nightly est moins stable.
  — <https://docs.comfy.org/manager/legacy-ui>
- Commencez par l'exemple JSON fourni pour la tâche visée plutôt que de migrer l'intégralité du graphe de production d'un seul coup.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Remplacé par ceci {#superseded-by-this}

- :{
- claim
- obsolete_since
- source_url
- claim

## Points encore inconnus {#still-unknown}

- Aucune seconde source primaire datée ne relie le 2026-07-18 à une modification, un commit, un tag ou une version précise.
- La valeur 2.7.1 dans `pyproject.toml` est une version de manifeste, et non une GitHub Release confirmée ni une publication vérifiée dans un registre.
- L'historique GitHub accessible s'arrête à un instantané d'avril 2026, alors que les fichiers actuels du dépôt portent des métadonnées postérieures ; la chronologie exacte des commits après avril n'est pas confirmée.
- Les publications des 10 et 19 juillet renvoient au même dépôt, mais aucun artefact primaire indépendant ne confirme leur auteur ni les versions annoncées.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/Starnodes2024/ComfyUI_StarNodes | Dépôt ComfyUI_StarNodes | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md | README de ComfyUI_StarNodes | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/pyproject.toml | pyproject.toml de ComfyUI_StarNodes | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/CHANGELOG.md | Journal des modifications de ComfyUI_StarNodes | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/commits/main | Historique des commits de ComfyUI_StarNodes | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/releases | Releases de ComfyUI_StarNodes | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1usx5f3/starnodes_211_panorama_update/ | Starnodes 2.1.1 Panorama Update | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1v0u5mt/starnodes_double_feature_updates_v236_v237_are/ | STARNODES Double Feature: Updates v2.3.6 & v2.3.7 are LIVE! | 2026-09-06 |
| https://docs.comfy.org/installation/install_custom_node | How to Install Custom Nodes in ComfyUI | 2026-09-06 |
| https://docs.comfy.org/manager/legacy-ui | Managing custom nodes with ComfyUI-Manager (legacy UI) | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui-starnodes`, fil `comfyui-starnodes`, 1 événement daté du 2026-07-18 au 2026-07-18.
- **Remarque pratique :** Au 2026-07-18, les praticiens doivent considérer le dépôt ComfyUI_StarNodes lié comme la source du projet à investiguer, et non comme une preuve de release vérifiée ou de procédure d'installation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
