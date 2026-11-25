---
title: "Modly"
category: projects
date: 2026-03-20
tags: [modly, modly-development, project]
aliases: ["Modly"]
level: 3
source_sha256: 88849578927894f9003807ef17b681fb74abdfdb219680502df9005b96bb2a6c
translation: machine
translated_at: '2026-10-24'
---
# Modly {#modly}

**Ligne de développement :** `project:modly` · fil `modly-development`  
**Dernier événement :** 2026-03-20 · 1 événement daté depuis le 2026-03-20 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Modly est une alternative locale aux outils cloud de conversion image vers 3D, comme Meshy, destinée aux créateurs qui exécutent des modèles sur leur propre matériel.

- Génération de maillages 3D à partir d'une image ou d'une invite textuelle.
- Extensions de modèles et de traitements, notamment Hunyuan3D 2, TripoSG et Trellis.
- Application de bureau avec workflows par nœuds, export de maillages et CLI locale.

## Ligne de développement {#development-line}

- **2026-03-20 — Référence au dépôt GitHub de Modly.** Le 2026-03-20, la ligne de développement de Modly a été reliée au dépôt GitHub public github.com/lightningpixel/modly. Ce lien établit une référence de dépôt datée, sans identifier de version, de commit, de fonctionnalité ou de changement opérationnel particulier.

## Changements {#what-changed}

- 2026-03-20 — Modly a été enregistré à son dépôt GitHub public ; aucun artefact daté de première partie couvrant exactement le périmètre fonctionnel de ce jour n'a été récupéré.
- 2026-03-26 — Modly Beta v0.2.1 a révisé le système d'extensions, la gestion des extensions de confiance et le mécanisme de mise à jour.
- 2026-04-03 — Modly Beta v0.3.0 a fait évoluer le produit vers des workflows basés sur des nœuds et une page Models centrée sur les extensions.
- 2026-04-21 — Modly Beta v0.3.2 a ajouté l'exécution headless via `/workflow-runs` et Python embarqué.
- 2026-04-22 — Modly Beta v0.3.3 a ajouté un nœud de workflow de remaillage.
- 2026-06-21 — Modly Beta v0.4.0 a ajouté la CLI pour agents, l'installation d'extensions locales, des travaux sur Apple Silicon, des contrôles de transformation et la visualisation de splats gaussiens.
- 2026-07-16 — Modly Beta v0.4.1 a ajouté des nœuds d'itération de workflow, des sorties de traitements audio, un navigateur de workflows et un packaging Apple Silicon.
- 2026-08-28 — Modly Beta v0.4.2 est devenue la dernière bêta étiquetée, corrigeant la validation des extensions et le comportement du sélecteur, les arguments JSON de la CLI, les E/S UTF-8 des sous-processus sous Windows et le placement de la collecte des exécutions de workflow.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-20, utilisez le dépôt GitHub référencé comme point de départ pour la vérification au niveau du code source de Modly ; ne déduisez pas de versions, de capacités ou de instructions d'utilisation à partir de ce seul lien.

1. Vérifiez que le modèle cible et la plateforme conviennent à la machine ; le site officiel recommande un GPU NVIDIA compatible CUDA disposant d'au moins 6 Go de VRAM, puis téléchargez l'installateur de la bêta courante.
  — <https://modly3d.app/>
2. Installez une extension de modèle officielle depuis la page Models en utilisant « Install from GitHub », puis téléchargez sa variante de modèle.
  — <https://github.com/lightningpixel/modly>
3. Construisez un graphe de base : Image → Generate Mesh → Add to Scene ; sélectionnez-le dans Generate, exécutez-le et consultez Settings/Logs/Errors en cas d'échec.
  — <https://github.com/lightningpixel/modly>
4. Prévisualisez le maillage et exportez-le en GLB, OBJ, STL ou PLY pour le DCC, le moteur ou le trancheur cible.
  — <https://modly3d.app/>
5. Pour l'automatisation, lancez l'application de bureau, exécutez `python tools/modly-cli/agent.py health`, inspectez les modèles, puis utilisez `generate --image ... --output ...` et conservez l'identifiant d'exécution renvoyé pour le suivi d'état ou l'annulation.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>

## Bonnes pratiques {#best-practices}

- Commencez par le plus petit workflow connecté et vérifiez chaque connexion avant de lancer la génération ; conservez la vue du maillage et lisez le panneau d'erreurs/journaux intégré au lieu de reconstruire le graphe après un échec.
  — <https://github.com/lightningpixel/modly>
- Utilisez une image d'entrée propre et isolée ou une invite précise, puis sélectionnez la variante de modèle installée selon le compromis vitesse/fidélité, plutôt que de supposer qu'un seul modèle convient à toutes les tâches.
  — <https://modly3d.app/>
- Pour un usage scripté, privilégiez les commandes canoniques `health`, `model` et `workflow-run` ; considérez `/generate/*` et les assistants ComfyUI expérimentaux comme des chemins de compatibilité ou d'expérimentation, et non comme un repli silencieux.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>
- Ne considérez pas les installateurs de bureau ni la configuration standard des extensions comme une prise en charge de Jetson : le guide Jetson décrit une voie non prise en charge nécessitant une version de PyTorch compilée pour Jetson, un épinglage de NumPy et un contournement pour la suppression de l'arrière-plan.
  — <https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md>

## Remplacé par {#superseded-by-this}

- Le workflow de l'ère pré-v0.3, centré sur la page de modèles, est remplacé par l'architecture de workflows par nœuds et d'extensions à partir du 2026-04-03.
- L'ancienne surface d'automatisation `/generate/*` n'est plus qu'un mécanisme de compatibilité ; l'automatisation canonique est le contrat workflow-run introduit par la ligne v0.4 le 2026-06-21.
- Modly Beta v0.4.1 n'est plus la dernière bêta étiquetée ; v0.4.2 l'a remplacée le 2026-08-28.

## Points encore inconnus {#still-unknown}

- Aucune note de version, étiquette ou instantané archivé du dépôt de première partie récupéré ne fixe le périmètre fonctionnel exact de Modly au 2026-03-20 ; les versions ultérieures sont donc conservées comme événements distincts.
- Les recommandations matérielles de première partie ne forment pas encore une matrice de prise en charge unique : le site produit recommande NVIDIA CUDA avec 6 Go de VRAM, le dépôt liste Apple Silicon sous macOS, et le guide Jetson décrit explicitement un contournement non pris en charge.
- Une recherche ciblée en chinois a trouvé une couverture secondaire, mais aucune documentation officielle en chinois ni registre de versions de Modly.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/lightningpixel/modly | GitHub - lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases | Versions · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases/tag/v0.2.1 | Notes de version Modly Beta v0.2.1 · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/tags | Étiquettes · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md | Modly CLI SKILL.md | 2026-09-05 |
| https://modly3d.app/ | Modly — Générateur local gratuit de modèles 3D par IA | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md | Exécuter Modly en mode headless sur un NVIDIA Jetson | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:modly`, fil `modly-development`, 1 événement daté du 2026-03-20 au 2026-03-20.
- **Note pratique :** À partir du 2026-03-20, utilisez le dépôt GitHub référencé comme point de départ pour la vérification au niveau du code source de Modly ; ne déduisez pas de versions, de capacités ou d'instructions d'utilisation à partir de ce seul lien.
- **Confiance :** moyenne. Les mentions de remplacement datées font foi pour ce qui est obsolète.
