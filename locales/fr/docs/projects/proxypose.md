---
title: "ProxyPose"
category: projects
date: 2026-07-11
tags: [project, proxypose, proxypose-development]
aliases: ["ProxyPose"]
level: 2
source_sha256: 22cb6a9630aae978ded512d5855c4943d40a035d058a65b45155b19db39146e2
translation: machine
translated_at: '2026-10-24'
---
# ProxyPose {#proxypose}

**Ligne de développement :** `project:proxypose` · fil `proxypose-development`  
**Dernier événement :** 2026-07-11 · 1 événement daté depuis 2026-07-11 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

ProxyPose est une méthode et une implémentation ouverte destinées aux chercheurs en vision par ordinateur qui ont besoin d'une trajectoire 6-DoF d'une surface ou d'un objet local à partir d'une vidéo monoculaire. Fonctionnalités : vidéo RGB et un point dans la première image ; génération d'une vidéo proxy avec un polyèdre coloré ; reconstruction de la pose par PnP géométrique ; application à des objets, à la caméra et à des visages. Limite : les mouvements rapides, les surfaces réfléchissantes et pauvres en texture peuvent provoquer une dérive (drift) ou rendre les images proxy floues. Verdict : pratique pour une évaluation de recherche reproductible sur GPU, à condition d'accepter une étape générative et de vérifier les résultats.

## Ligne de développement {#development-line}

- **2026-07-11 — Ressources publiques du projet ProxyPose publiées.** Le 2026-07-11, ProxyPose a été présenté à travers des liens vers le projet, le code source et une ressource Hugging Face. Il s'agit d'un événement public important de la ligne de développement, car il établit une présence du projet facilement repérable, même si les affirmations techniques et le statut de publication des ressources liées n'ont pas été vérifiés de manière indépendante.

## Ce qui a changé {#what-changed}

2026-07-11 — publication de la page du projet, du code source et des poids de ProxyPose pour le suivi de pose 6-DoF par traduction vidéo-vidéo.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-11, les praticiens doivent utiliser la page du projet, le dépôt et la ressource Hugging Face liés comme points de départ pour évaluer ProxyPose, tout en considérant que cet événement, uniquement documenté par des liens, n'est pas vérifié en ce qui concerne les capacités techniques et les détails de publication.

1. Cloner le dépôt, créer un environnement Python 3.10, installer PyTorch CUDA 12.1, PyTorch3D et le paquet ProxyPose.
  — <https://github.com/ruihangzhang97/proxypose>
2. Ouvrir l'annotator local avec la commande `proxypose-annotate --input-video ...`, sélectionner un point dans la première image et enregistrer un JSON contenant les coordonnées.
  — <https://github.com/ruihangzhang97/proxypose>
3. Si nécessaire, estimer la distance focale avec Depth Anything 3 ; sinon, un FOV horizontal fixe de 45° est utilisé.
  — <https://github.com/ruihangzhang97/proxypose>
4. Lancer `proxypose-infer` avec la vidéo, le JSON des points et le chemin de sortie ; pour un modèle plus petit, passer la configuration Wan2.1-T2V-1.3B.
  — <https://github.com/ruihangzhang97/proxypose>

## Bonnes pratiques {#best-practices}

- Commencer avec le modèle 14B pour la qualité, et choisir le 1.3B pour des expérimentations rapides ou une VRAM limitée ; le LoRA et le modèle de base doivent correspondre à la taille choisie.
  — <https://github.com/ruihangzhang97/proxypose>
- Utiliser la focale estimée par Depth Anything 3 lorsque la précision géométrique prime sur la rapidité de mise en route.
  — <https://github.com/ruihangzhang97/proxypose>
- Vérifier manuellement les trajectoires sur les scènes rapides, réfléchissantes et pauvres en texture : ces cas sont signalés comme sources de dérive et de dégradation de la détection des contours.
  — <https://ruihangzhang97.github.io/proxypose/>

## Remplacé par cet élément {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- La date d'ajout, dans le dépôt, de la prise en charge actuelle de Wan2.1-T2V-1.3B n'est pas confirmée par l'historique des commits disponible ; elle n'a donc pas été enregistrée comme événement daté distinct.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ruihangzhang97.github.io/proxypose/ | ProxyPose — 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose | Dépôt officiel de ProxyPose et guide d'installation | 2026-09-05 |
| https://arxiv.org/abs/2607.06555 | ProxyPose: 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose/issues/2 | Issue #2 : Demande de variante ProxyPose pour Wan2.1-T2V-1.3B | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:proxypose`, fil `proxypose-development`, 1 événement daté du 2026-07-11 au 2026-07-11.
- **Note pratique :** Au 2026-07-11, les praticiens doivent utiliser la page du projet, le dépôt et la ressource Hugging Face liés comme points de départ pour évaluer ProxyPose, tout en considérant que cet événement, uniquement documenté par des liens, n'est pas vérifié en ce qui concerne les capacités techniques et les détails de publication.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
