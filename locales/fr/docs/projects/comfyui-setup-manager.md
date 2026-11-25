---
title: "ComfyUI Setup Manager"
category: projects
date: 2026-07-23
tags: [comfyui-setup-manager, comfyui-setup-manager-development, comfyui_setup_manager, project]
aliases: ["ComfyUI Setup Manager"]
level: 2
source_sha256: 9adf979f8cb1f960ef8ac2b9b6c88314f648ad8c148b03a9c3e15ec6c237509e
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Setup Manager {#comfyui-setup-manager}

**Ligne de développement :** `project:comfyui-setup-manager` · fil `comfyui-setup-manager-development`  
**Dernier événement :** 2026-07-23 · 1 daté depuis le 2026-07-23 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI Setup Manager est une TUI et une CLI en terminal permettant de gérer des installations isolées de ComfyUI.

- Cycle de vie des installations : installe, lance, inspecte, met à jour, répare, exporte et recrée les copies de travail de ComfyUI.
- Isolation de l'environnement : sépare la copie de travail, l'environnement virtuel et les nœuds personnalisés pour chaque installation.
- Bibliothèques d'actifs partagées : partage les répertoires de modèles et de workflows entre les copies de travail afin d'éviter les fichiers en double.
- Profils de configuration : exporte et reconstruit les installations à l'aide de fichiers de reconstruction portables `.comfyuisetup`.

Version actuelle indiquée dans le README : 0.8.8.

À utiliser pour la maintenance reproductible de plusieurs installations ComfyUI, et non comme remplacement de ComfyUI Desktop, ni comme garantie que des nœuds incompatibles peuvent coexister.

## Ligne de développement {#development-line}

- **2026-07-23 — Le dépôt ComfyUI Setup Manager a été cité publiquement.** Le 2026-07-23, une référence publique renvoyait au dépôt GitHub de ComfyUI Setup Manager. Cela établit une référence publique datée au projet, mais n'établit pas à elle seule une version, une modification de fonctionnalité ou une activité du dépôt.

## Modifications {#what-changed}

2026-07-23 — ComfyUI Setup Manager est apparu comme projet GitHub autonome permettant de reconstruire et de maintenir des installations de ComfyUI ; le dépôt référencé est désormais en version 0.8.8.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-23, évaluez le dépôt lors des tests d'outils pour ComfyUI ; ses capacités et sa sûreté restent non vérifiées.

1. Vérifiez les prérequis : Python 3.10+, Git, un accès Internet et des droits d'écriture ; sous Windows, vérifiez WinGet si Python ou Git peuvent manquer.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
2. Installez avec `install.ps1` sous Windows, `install.cmd` dans l'invite de commandes, ou `./install.sh` sous Linux, WSL2 et macOS.
  — <https://github.com/badgids/comfyui-setup-manager>
3. Exécutez `./comfyui-setup-manager`, sélectionnez Setup & Install, choisissez un profil et examinez l'installation ; équivalent en CLI : `install run --profile vanilla-comfyui --target /path/to/ComfyUI --repository-mode official`.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
4. Avant de créer plusieurs installations, configurez un répertoire externe de modèles et un répertoire de workflows, puis appliquez-les à chaque copie de travail gérée.
  — <https://github.com/badgids/comfyui-setup-manager>
5. Avant une mise à jour, exécutez `updates check` ; n'utilisez `updates run --strategy safe` qu'après avoir examiné le rapport de vérification préalable.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>

## Bonnes pratiques {#best-practices}

- Considérez un export `.comfyuisetup` exact comme un manifeste de reconstruction, et non comme une sauvegarde des modèles, des environnements virtuels ou de l'ensemble de la copie de travail ; vérifiez l'ABI de Python, de l'accélérateur et de PyTorch avant toute réutilisation sur une autre machine.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md>
- Utilisez une bibliothèque externe unique de modèles et de workflows pour éviter de dupliquer les gros checkpoints entre les installations stables, expérimentales et de développement.
  — <https://github.com/badgids/comfyui-setup-manager>
- Pour une utilisation non surveillée, demandez une sortie JSON ou YAML, créez un plan avant toute modification, inspectez les codes de sortie et n'analysez pas la TUI.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>
- Commencez par une installation non critique : des exigences réellement incompatibles entre nœuds personnalisés peuvent encore nécessiter des installations distinctes de ComfyUI.
  — <https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- Aucune version ni aucun commit datés, publiés par le projet lui-même, ne confirment ce qui a changé précisément le 2026-07-23 ; les capacités ultérieures ne peuvent pas être rattachées à cette date sans preuve.
- Les notes de version décrivent les ensembles de fonctionnalités de 0.8.0 à 0.8.7, mais n'indiquent pas les dates de publication.
- Le dépôt du projet décrit la version 0.8.8, mais la page des notes de version ne fournit aucune preuve datée de publication pour la 0.8.8.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/badgids/comfyui-setup-manager | ComfyUI Setup Manager README | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md | Getting started | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md | Automation and AI agent use | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md | Portable setup profiles | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/RELEASE_NOTES.md | Release notes | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/ | I built a setup manager because backing up entire ComfyUI installs was getting ridiculous | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui-setup-manager`, fil `comfyui-setup-manager-development`, 1 événement daté du 2026-07-23 au 2026-07-23.
- **Note pratique :** Au 2026-07-23, évaluez le dépôt lors des tests d'outils de configuration pour ComfyUI ; ses capacités et sa sûreté restent non vérifiées.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
