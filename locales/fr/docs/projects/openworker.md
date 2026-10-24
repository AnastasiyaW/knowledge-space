---
title: "OpenWorker — Introduction au projet"
category: projects
date: 2026-08-05
tags: [openworker, project, project-introduction]
aliases: ["OpenWorker"]
level: 1
source_sha256: 4cbf9c27a12925f94c0e57bc421b1a33c9e47dc6358eaa9364e9ce933dd2c2fb
translation: machine
translated_at: '2026-10-24'
---
# OpenWorker — Introduction au projet {#openworker-project-introduction}

**Ligne de développement :** `project:openworker` · fil `project-introduction`  
**Dernier événement :** 2026-08-05 · 1 événement daté depuis le 2026-08-05 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

OpenWorker est un assistant IA de bureau sous licence MIT, doté d'un serveur d'agent Python local et d'une interface graphique Tauri/React. Il prend en charge les modèles fournis par l'utilisateur (bring-your-own models) et plus de 25 intégrations.

- Documents et rapports : génération à partir de fichiers, de Slack et d'automatisations.
- Garde-fous : approbation requise pour les actions risquées.

Le statut est celui d'une bêta ouverte. La version Windows n'est pas signée avec Authenticode.

## Ligne de développement {#development-line}

- **2026-08-05 — OpenWorker a été mentionné publiquement via son dépôt GitHub.** Le 2026-08-05, le lien enregistré pointait vers le dépôt GitHub d'OpenWorker et vers la page biographique d'Andrew Ng. Cela établit un point de référence public daté pour le projet. Les liens seuls ne confirment ni une version, ni un ensemble de fonctionnalités, ni un statut opérationnel.

## Ce qui a changé {#what-changed}

2026-08-05 — Le lien enregistré pointait vers un dépôt OpenWorker autonome. La source primaire ne montre aucune version ni annonce datée de ce jour.

2026-08-24 — La v0.2.0 a ajouté les compétences (skills), la mémoire inter-sessions, trois coworkers de sécurité et l'approbation automatique assistée par un reviewer. Elle a également amélioré la configuration MCP et corrigé des bogues d'approbation et de sécurité.

2026-08-25 — La v0.2.1 a ajouté Ox Alpha via OpenRouter au sélecteur de modèles, avec un contexte de 1 M de tokens et l'appel d'outils.

## Mode d'emploi {#how-to-use-this}

Partez du dépôt GitHub d'OpenWorker tel qu'il était le 2026-08-05. Considérez les capacités et le statut des versions comme non vérifiés tant que nous n'avons pas inspecté les éléments du dépôt.

1. Installez la version macOS ou Windows, ouvrez l'application et connectez une clé API de fournisseur ou un Ollama local.
  — <https://github.com/andrewyng/openworker>
2. N'accordez l'accès aux dossiers que dans le mode requis, puis décrivez le résultat attendu en langage courant. Par défaut, les artefacts sont enregistrés dans un espace de travail temporaire.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
3. Créez une automatisation pour les tâches récurrentes. Elle ne s'exécute que tant que l'application reste ouverte ; activez donc le lancement à la connexion pour une exécution en arrière-plan.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
4. Connectez un serveur MCP via Manage → Integrations, puis définissez les contrôles d'approbation pour ses outils.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>

## Bonnes pratiques {#best-practices}

- Commencez avec un dossier délimité, et approuvez les commandes shell et les écritures en dehors des répertoires accordés. Ne confondez pas une configuration local-first avec l'absence totale de transfert de données vers le fournisseur de modèle choisi.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
- Gardez un humain dans la boîte d'approbation pour les automatisations sans surveillance, afin que ces exécutions n'approuvent pas elles-mêmes leurs effets de bord.
  — <https://github.com/andrewyng/openworker>
- Attendez-vous à un avertissement SmartScreen sous Windows, car les versions actuelles ne sont pas signées numériquement.
  — <https://github.com/andrewyng/openworker>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-24 — OpenWorker n'est plus seulement un assistant de bureau générique : la v0.2.0 a ajouté les compétences, la mémoire de projet, des coworkers de sécurité et un reviewer d'approbation automatique.
- 2026-08-25 — La liste de modèles d'origine est obsolète : la v0.2.1 a ajouté Ox Alpha via OpenRouter, avec un contexte annoncé de 1 M de tokens.

## Toujours inconnu {#still-unknown}

- Le schéma de réponse omet les champs event_findings et new_events ; les nouveaux faits datés figurent donc dans what_changed.
- Aucune source primaire publiée le 2026-08-05 n'a été trouvée qui apporte un détail vérifiable à l'étape elle-même.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/andrewyng/openworker | andrewyng/openworker — README | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases/tag/v0.2.0 | OpenWorker v0.2.0 — GitHub Release | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases | OpenWorker releases — GitHub | 2026-09-05 |
| https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md | OpenWorker quickstart — aisuite documentation | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:openworker`, fil `project-introduction`, 1 événement daté du 2026-08-05 au 2026-08-05.
- **Note pratique :** Au 2026-08-05, partez du dépôt GitHub d'OpenWorker. Considérez ses capacités et son statut de version comme non vérifiés tant que nous n'avons pas examiné les éléments du dépôt.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
