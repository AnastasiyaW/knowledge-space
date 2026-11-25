---
title: "Hunyuan3D-WorldClaw"
category: projects
date: 2026-08-10
tags: [hunyuan3d, hunyuan3d-worldclaw, project]
aliases: ["Hunyuan3D-WorldClaw"]
level: 2
source_sha256: b871baeb7c96da57552c290b96e2a2d4ceae4cb28ffb389e77943521aaa79db0
translation: machine
translated_at: '2026-10-24'
---
# Hunyuan3D-WorldClaw {#hunyuan3d-worldclaw}

**Ligne de développement :** `project:hunyuan3d-worldclaw` · fil `hunyuan3d-worldclaw`  
**Dernier événement :** 2026-08-10 · 1 événement daté depuis le 2026-08-10 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Hunyuan3D-WorldClaw est un cadre de recherche destiné aux artistes techniques et aux équipes de construction de mondes qui ont besoin de maillages 3D éditables pour le terrain et les objets, plutôt que d'une scène rendue unique.

- Transforme une consigne ouverte (*prompt*) en régions, terrain, actifs, matériaux et relations spatiales.
- Construit un terrain sémantique et sensible aux régions, et ajoute sélectivement des maillages texturés modifiables indépendamment.
- Utilise des agents fondés sur le rendu pour affiner la géométrie, l'apparence, l'échelle, la pose et le contact avec le sol.

## Ligne de développement {#development-line}

- **2026-08-10 — Page du projet Hunyuan3D-WorldClaw enregistrée.** Le 2026-08-10, Hunyuan3D-WorldClaw a publié un lien vers sa page de projet. La page confirme la date et l'URL du projet, mais ne fournit aucun détail sur la publication, les capacités, la gestion des versions, l'auteurat ou l'état opérationnel. Nous n'enregistrons que la référence publique datée du projet.

## Ce qui a changé {#what-changed}

- 2026-08-05 — La v1 sur arXiv a présenté WorldClaw comme un cadre agentique global-vers-régional pour des mondes 3D explicites et éditables.
- 2026-08-07 — Le README officiel a annoncé la publication de l'article et de la page du projet.
- 2026-08-10 — Le dépôt GitHub officiel a débuté avec un README et des images de projet ; cette publication n'a ajouté ni installation, ni code d'inférence, ni paquet de modèle.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-10, évaluez le projet à partir de la page liée. Les documents publics ne permettent pas encore de formuler une recommandation précise d'adoption ou de flux de travail.

1. Utilisez l'article comme référence architecturale : convertissez la consigne en spécification structurée, établissez d'abord le terrain global, puis ne générez et ne placez les détails que dans les régions sélectionnées.
  — <https://arxiv.org/html/2608.05248>
2. Exécutez la pile vous-même pour une reproduction interne ; la configuration rapportée combine Claude Opus 4.8, GPT-Image-2, SAM3, SAM3D, Hunyuan3D et Blender 5.1.1.
  — <https://arxiv.org/html/2608.05248>
3. Consultez l'arborescence officielle du dépôt avant de planifier un déploiement ; l'arborescence publique actuelle ne contient que les ressources du projet, `.gitignore` et `README.md`.
  — <https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/tree/main>
4. Consultez la page officielle des Releases pour une distribution exécutable ; elle ne liste actuellement aucune release.
  — <https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/releases>

## Bonnes pratiques {#best-practices}

- Conservez une spécification de scène structurée unique comme interface sémantique et spatiale partagée entre la planification, la génération du terrain et la génération régionale d'objets.
  — <https://arxiv.org/html/2608.05248>
- Construisez le terrain global avant le détail local des objets, afin que la génération régionale conserve le contexte du terrain et la structure spatiale globale.
  — <https://arxiv.org/html/2608.05248>
- Effectuez le rendu, l'inspection, la correction et un nouveau rendu de la qualité des maillages d'objets, de leur pose, de leur échelle et de leur contact avec le terrain ; vérifiez explicitement les objets flottants, les pénétrations et les appuis instables.
  — <https://arxiv.org/html/2608.05248>
- Budgétisez séparément le nombre d'objets et les itérations de raffinement : la latence et le calcul augmentent avec les deux, ce qui rend l'approche inefficace pour les scènes plus simples.
  — <https://arxiv.org/html/2608.05248>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues {#still-unknown}

- Aucun guide d'installation public officiel, aucun poids de modèle, aucun paquet d'inférence, aucune API ni aucune licence logicielle n'est disponible sur les pages du projet ; cela n'exclut pas un accès futur ou privé.
- Aucune reproduction indépendante de la qualité de bout en bout, du débit, de la latence ou du coût n'existe ; l'article ne fournit que des démonstrations qualitatives et sa propre configuration expérimentale.
- L'implémentation actuelle basée sur Blender n'est pas un environnement d'exécution complet pour mondes de jeu : l'article identifie comme exigences supplémentaires les systèmes d'exécution procéduraux, la navigation, la physique et l'interaction.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://tencent-hunyuan.github.io/Hunyuan3D-WorldClaw/ | WorldClaw — Génération agentique de mondes 3D ouverts à grande échelle | 2026-09-05 |
| https://arxiv.org/abs/2608.05248 | WorldClaw: Agentic 3D Open-World Generation at Scale — v1 sur arXiv | 2026-09-05 |
| https://arxiv.org/html/2608.05248 | WorldClaw: Agentic 3D Open-World Generation at Scale — article en HTML | 2026-09-05 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/main/README.md | README officiel de Hunyuan3D-WorldClaw | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/tree/main | Tencent-Hunyuan/Hunyuan3D-WorldClaw — arborescence actuelle de main | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/commit/bf7b10f7930821b32504ecdd1a02ce42ea7833e0 | Commit initial : README et ressources de l'article WorldClaw | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw/releases | Releases — Tencent-Hunyuan/Hunyuan3D-WorldClaw | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:hunyuan3d-worldclaw`, fil `hunyuan3d-worldclaw`, 1 événement daté du 2026-08-10 au 2026-08-10.
- **Note pratique :** Au 2026-08-10, utilisez la page de projet Hunyuan3D-WorldClaw liée pour évaluer le projet ; les éléments disponibles ne permettent pas de formuler une recommandation d'adoption ou de flux de travail plus précise.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
