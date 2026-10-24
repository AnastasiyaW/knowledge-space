---
title: "SpatialClaw"
category: projects
date: 2026-07-01
tags: [nvidia, project, spatialclaw, spatialclaw-development]
aliases: ["SpatialClaw"]
level: 3
source_sha256: f0375e7190c7a73354ed8ea1720707107d70d78235b70374c47c23eb6855c450
translation: machine
translated_at: '2026-10-24'
---
# SpatialClaw {#spatialclaw}

**Ligne de développement :** `project:spatialclaw` · fil `spatialclaw-development`  
**Dernier événement :** 2026-07-01 · 1 événement daté depuis le 2026-07-01 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

SpatialClaw est un framework NVIDIA et KAIST, sans entraînement supplémentaire (training-free), destiné aux équipes qui évaluent des VLM sur des tâches spatiales 3D, multi-vues, vidéo et 4D. L'agent écrit des cellules Python dans un kernel Jupyter persistant, appelle SAM3, Depth Anything 3, des outils de géométrie et NumPy/SciPy, examine les résultats intermédiaires, puis renvoie sa réponse. Mesure : précision moyenne de 59,9 % sur 20 benchmarks, soit 11,2 points de pourcentage au-dessus de SpaceTools-Toolshed dans une comparaison sur Gemma 4-31B. Verdict : il s'agit d'un runtime de recherche reproductible, et non d'une bibliothèque légère pour une application vision classique.

## Ligne de développement {#development-line}

- **2026-07-01 — Références du projet SpatialClaw partagées.** Agent sans entraînement supplémentaire, avec une interface code-as-action, un kernel Python/Jupyter persistant, un serveur GPU de perception, et des exécutions aussi bien sur une seule machine GPU que via SLURM.

## Ce qui a changé {#what-changed}

Le 2026-07-01, le code officiel et le site de SpatialClaw ont été publiés : agent sans entraînement supplémentaire, avec une interface code-as-action, un kernel Python/Jupyter persistant, un serveur GPU de perception, et des exécutions aussi bien sur une seule machine GPU que via SLURM.

Complément à l'événement du 2026-07-01 : le dépôt précise le contenu de la livraison — runtime LangGraph, vérification AST des cellules, boucles de planification et de réflexion, 20 chargeurs de benchmarks, serveur d'outils GPU FastAPI, découverte et répartition de charge vLLM, et gestionnaires de lancement SLURM. L'article officiel du 2026-06-11 rapporte le résultat initial : 59,9 % sur 20 benchmarks et +11,2 points de pourcentage par rapport à un agent spatial récent.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-01, les praticiens peuvent utiliser le site du projet et le dépôt NVlabs comme points de départ primaires et datés pour évaluer SpatialClaw ; ces seuls éléments ne justifient aucun changement de workflow précis.

1. Cloner le dépôt récursivement et lancer le script d'installation officiel ; il crée les environnements de l'agent, CUDA et vLLM.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
2. Préparer un Linux avec GPU NVIDIA, CUDA 12.x, Conda et un accès aux poids SAM3.1 protégés (gated) ; les variantes FP8 de l'article exigent Hopper/H100 ou plus récent, tandis que pour A100/L40S la documentation indique les variantes AWQ/GPTQ.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
3. Copier .env et choisir le backend : vLLM auto-hébergé ou endpoint compatible OpenAI ; renseigner les fichiers JSON de modèle et de jeu de données, puis lancer spatial_agent.entrypoints.run.
  — <https://github.com/NVlabs/SpatialClaw>
4. Pour SLURM, adapter d'abord account, partition et limites de mémoire des configurations de lancement à votre cluster, puis télécharger à l'avance les poids du VLM et de perception sur le login node.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>

## Bonnes pratiques {#best-practices}

- Toujours cloner avec --recursive, ou initialiser les submodules séparément : SAM3, Pi3, Depth-Anything-3 et map-anything sont épinglés à des révisions précises.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
- Avant un lancement SLURM, télécharger tous les poids à l'avance : les tâches de calcul fonctionnent avec HF_HUB_OFFLINE=1, et un artefact local absent fera échouer la tâche avec une erreur LocalEntryNotFoundError.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>
- Ne pas utiliser le chemin de modèle HF comme llm_model lorsque llm_base_url=vllm : indiquer le served_name défini dans models.json ; pour un endpoint externe compatible OpenAI, utiliser l'identifiant de modèle attendu par celui-ci.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- La documentation ne mentionne aucune version (release) ou tag versionné spécifiquement lié au 2026-07-01 ; la date correspond à la disponibilité du projet et du code lors de l'événement indiqué, et non à une GitHub Release confirmée.
- La licence du dépôt est la NVIDIA Source Code License-NC ; son adéquation à un usage commercial doit être vérifiée séparément à partir de son texte intégral.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://spatialclaw.github.io/ | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw | Dépôt NVlabs/SpatialClaw | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md | Installation de SpatialClaw | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md | Exécution des expériences SpatialClaw | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md | Configuration et benchmarks de SpatialClaw | 2026-09-05 |
| https://arxiv.org/abs/2606.13673 | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:spatialclaw`, fil `spatialclaw-development`, 1 événement daté, du 2026-07-01 au 2026-07-01.
- **Note pratique :** À partir du 2026-07-01, les praticiens peuvent utiliser le site du projet et le dépôt NVlabs comme points de départ primaires et datés pour évaluer SpatialClaw ; ces seuls éléments ne justifient aucun changement de workflow précis.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
