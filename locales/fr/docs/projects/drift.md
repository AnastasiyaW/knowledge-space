---
title: "DRIFT — Ressources du projet"
category: projects
date: 2026-06-04
tags: [drift, project, project-resources]
aliases: ["DRIFT"]
level: 2
source_sha256: c2824fae4f4cda62c846a3db71bbe7cdf94ba32257f6613a6592ce27003585a9
translation: machine
translated_at: '2026-10-24'
---
# DRIFT — Ressources du projet {#drift-project-resources}

**Ligne de développement :** `project:drift` · fil `project-resources`  
**Dernier événement :** 2026-06-04 · 1 événement daté depuis le 2026-06-04 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

DRIFT est un cadre ouvert, centré sur les affirmations, destiné aux trajectoires d'agents de recherche approfondie. Il localise les segments où une affirmation non vérifiée ou contradictoire devient nuisible.

Il comprend Claim Keeper, Support Seeker et Dependency Tracer. TELBench fournit 1 000 tâches de trajectoires vérifiées par des experts, issues de 2 790 exécutions collectées.

Il s'agit d'un outil reproductible permettant de comparer des audits de trajectoires et d'analyser des défaillances, et non d'une couche de supervision prête à l'emploi pour un agent en cours d'exécution.

## Ligne de développement {#development-line}

- **2026-06-04 — La page du projet DRIFT et le dépôt ont été liés.** Le 2026-06-04, un message daté a renvoyé vers la page du projet DRIFT et son dépôt GitHub. Ce message inscrit ces deux ressources dans la ligne de développement. Il n'établit ni une publication, ni une version, ni une modification technique, ni un lancement du projet.

## Ce qui a changé {#what-changed}

2026-06-04 — DRIFT et TELBench ont été présentés comme des artefacts ouverts pour la localisation des erreurs au niveau des segments dans les trajectoires d'agents de recherche approfondie.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-04, évaluez DRIFT à l'aide de la page du projet et du dépôt GitHub liés. Cet événement n'établit ni une installation ni une modification du workflow.

1. Clonez le dépôt et installez le paquet en mode éditable.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
2. Téléchargez TELBench chiffré depuis Hugging Face et déchiffrez-le avec le script fourni ; le script vérifie le hachage SHA-256.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
3. Configurez l'API Chat Completions ou Responses compatible OpenAI, via des arguments ou un fichier d'environnement. Exécutez `drift --setting drift` sur les trajectoires au format JSONL.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
4. Transmettez `summary.json` à `drift-eval`. Le rapport fournit la précision, le rappel et le F1 macro/micro, l'exactitude du premier erreur, ainsi que les identifiants manquants ou en trop.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Bonnes pratiques {#best-practices}

- Exécutez d'abord `bare` sur les mêmes entrées et avec le même modèle, puis exécutez `drift`. Cette comparaison, voulue par les auteurs, isole l'effet du pipeline centré sur les affirmations par rapport au modèle de base.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Vérifiez la somme de contrôle de TELBench déchiffré. Ne versionnez pas dans Git les artefacts téléchargés, la clé ou les JSONL déchiffrés.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Ne transmettez au modèle ni les étiquettes de référence, ni les annotations, ni les métadonnées, ni les sorties du juge, ni les notes manuelles. L'évaluation n'accepte que la question et le texte brut des segments, dans leur ordre.
  — <https://huggingface.co/datasets/NJU-LINK/TELBench>
- Conservez `--reasoning-effort low` pour l'API Responses, sauf si une mesure justifie un changement. Il s'agit de la valeur par défaut du projet pour les prompts ne produisant que du JSON.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Remplacé par cette entrée {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points non élucidés {#still-unknown}

- Les sources primaires publiques confirment la soumission de l'article le 1er juin 2026 et sa révision v2 le 2 juin. Elles n'enregistrent pas de publication distincte de DRIFT le 4 juin. La date du 4 juin reste la date de l'événement, et non une date de publication confirmée.
- Il n'existe aucun journal des modifications primaire daté après le 4 juin 2026 permettant de nommer des changements ultérieurs du code ou du jeu de données.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://nju-link.github.io/DRIFT/ | DRIFT | Claim-Centric Trajectory Auditing | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT | Dépôt NJU-LINK/DRIFT | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md | Guide d'utilisation de DRIFT | 2026-09-05 |
| https://huggingface.co/datasets/NJU-LINK/TELBench | Fiche du jeu de données NJU-LINK/TELBench | 2026-09-05 |
| https://arxiv.org/abs/2606.02060 | Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization in Agent Trajectories | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:drift`, fil `project-resources`, 1 événement daté, du 2026-06-04 au 2026-06-04.
- **Note pratique :** À partir du 2026-06-04, les praticiens qui évaluent DRIFT doivent utiliser la page du projet et le dépôt GitHub liés comme ressources primaires disponibles ; ces éléments ne permettent pas d'établir une modification de l'installation ou du workflow.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
