---
title: "ComfyUI Mobile Frontend"
category: projects
date: 2026-08-12
tags: [comfyui-mobile-frontend, comfyui_mobile_frontend, project]
aliases: ["ComfyUI Mobile Frontend"]
level: 2
source_sha256: 9dacca8e72a92a77e5539af874666fcd66b14cf2c8cbb157a31a3ce5335dd39b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Mobile Frontend {#comfyui-mobile-frontend}

**Ligne de développement :** `project:comfyui-mobile-frontend` · fil `comfyui-mobile-frontend`  
**Dernier événement :** 2026-08-12 · 1 événement daté depuis le 2026-08-12 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI Mobile Frontend est un nœud personnalisé destiné aux personnes qui utilisent ComfyUI et souhaitent modifier des workflows, surveiller les files d'attente et gérer les sorties depuis un téléphone ou une tablette.

- Interface navigateur servie à l'adresse `/mobile`.
- Éditeur de workflows pour appareils tactiles.
- Suivi des files d'attente et de l'historique.
- Visionneuse des sorties et des médias.

La prise en charge des nœuds personnalisés est incomplète, et le projet se déclare lui-même expérimental. La dernière version publiée trouvée est la v3.2.5, datée du 2026-08-25. Utilisez-la sur un serveur ComfyUI personnel et de confiance, après avoir testé les workflows et les nœuds dont vous avez besoin.

## Ligne de développement {#development-line}

- **2026-08-12 — Des références publiques sur ComfyUI Mobile Frontend ont été partagées.** Le 2026-08-12, la ligne de développement de ComfyUI Mobile Frontend a été reliée à son dépôt GitHub et au site web de CueForge. Cela crée un point de repère public daté pour le projet, sans que les liens partagés ne documentent pour autant une version, un ensemble de fonctionnalités ou un autre jalon précis.

## Ce qui a changé {#what-changed}

2026-08-12 — La v3.1.3 a amélioré la navigation dans les sorties, les contrôles de workflow et la gestion des wildcards.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-08-12, les praticiens pouvaient utiliser le dépôt GitHub et le site web de CueForge comme points de départ lors de l'évaluation de ComfyUI Mobile Frontend ; ne déduisez aucune capacité, version ou statut de publication particulier de ce seul événement.

1. Installez-le via ComfyUI-Manager, auteur `cosmicbuffalo`, ou clonez le dépôt dans le répertoire `custom_nodes` de ComfyUI.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
2. Redémarrez ComfyUI, puis ouvrez `http://<ip-serveur>:8188/mobile` ; utilisez l'option `--listen` de ComfyUI pour y accéder depuis un autre appareil du réseau local.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
3. Chargez un workflow ; si des nœuds sont manquants, utilisez la boîte de dialogue pour ouvrir le Custom Nodes Manager filtré sur les types de nœuds manquants.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md>

## Bonnes pratiques {#best-practices}

- Testez les workflows exacts reposant sur des nœuds personnalisés dont vous avez besoin avant de vous fier à l'interface mobile, car la prise en charge automatique de tous les nœuds personnalisés n'est pas disponible.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
- N'exposez pas un serveur ComfyUI à des clients non fiables ; placez-le derrière une authentification, un VPN ou un reverse proxy. Désactivez le couplage CueForge avec `COMFYUI_MOBILE_APP_PUSH=0` si vous ne le souhaitez pas.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md>

## Remplacé par {#superseded-by-this}

- 2026-08-16 — La v3.2.0 a remplacé les consignes d'interface uniquement en anglais en ajoutant le chinois simplifié, le chinois traditionnel, le japonais et le coréen.
- 2026-08-25 — La v3.2.5 a remplacé la v3.2.4 comme dernière version publiée, en ajoutant la prise en charge d'un socket de progression cadencé par le client et une correction pour le combo de sous-graphes.

## Points inconnus {#still-unknown}

- CueForge est un client iOS distinct, et non une version du nœud personnalisé. Sa page officielle consultée annonce une disponibilité prochaine sur l'App Store, mais aucun document de lancement daté émanant de l'éditeur n'a été trouvé.
- Le journal des modifications de la branche principale, tel que consulté, indique la v3.2.5 comme « Unreleased », alors que la page Releases officielle présente la v3.2.5 comme la dernière version publiée, datée du 2026-08-25 ; utilisez la page des versions pour choisir la version publiée.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend | Dépôt ComfyUI Mobile Frontend | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases | Versions de ComfyUI Mobile Frontend | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.0.0 | Version v3.0.0 | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.1.0 | Version v3.1.0 — Une nouvelle grosse mise à jour d'ergonomie | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md | Guide utilisateur ComfyUI Mobile | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md | Ce que ce nœud personnalisé envoie à CueForge | 2026-09-05 |
| https://cueforge.dev/ | CueForge — ComfyUI sur iPhone | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:comfyui-mobile-frontend`, fil `comfyui-mobile-frontend`, 1 événement daté du 2026-08-12 au 2026-08-12.
- **Note pratique :** Depuis le 2026-08-12, les praticiens pouvaient utiliser le dépôt GitHub et le site web de Cueforge comme points de départ lors de l'évaluation de ComfyUI Mobile Frontend ; aucune capacité, version ou statut de publication particulier ne doit être déduit de ce seul événement.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
