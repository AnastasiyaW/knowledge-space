---
title: "DeerFlow 2.0 — Plateformes d'agents"
category: projects
date: 2026-03-12
tags: [agent-platforms, agent_platforms, deerflow, project]
aliases: ["DeerFlow 2.0"]
level: 2
source_sha256: b40bcbf24f406b167f38042128f94b65137551db85639691ed6901e26e2c2dc4
translation: machine
translated_at: '2026-10-24'
---
# DeerFlow 2.0 — Plateformes d'agents {#deerflow-20-agent-platforms}

**Ligne de développement :** `project:deerflow` · fil `agent-platforms`  
**Dernier événement :** 2026-03-12 · 1 événement daté depuis le 2026-03-12 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

DeerFlow 2.0 — un runtime open source destiné aux équipes qui ont besoin d'un harnais d'agents plutôt que d'un framework réservé à la recherche.

- Délégation à des sous-agents : planifie le travail et le délègue à des sous-agents.
- Environnement d'exécution : combine mémoire, compétences/outils et système de fichiers en bac à sable.
- Prise en charge des modèles : prend en charge plusieurs fournisseurs de modèles et un déploiement auto-hébergé.

La Gateway utilise par défaut un seul worker. Un fonctionnement multi-worker nécessite la pile de persistance partagée et d'événements documentée. Utilisez-la pour un déploiement Docker de confiance, géré par un opérateur, et non comme point d'accès exposé sur Internet par défaut.

## Ligne de développement {#development-line}

- **2026-03-12 — DeerFlow 2.0 a été présenté via son site officiel, son espace de travail et son dépôt.** Le 2026-03-12, DeerFlow 2.0 a relié sa présence publique et son code source à son site officiel, à son espace de travail et au dépôt GitHub de Bytedance. Les ressources liées établissent une présence publique et un code source, sans affirmer une version particulière, un ensemble de fonctionnalités ou un changement de disponibilité.

## Ce qui a changé {#what-changed}

2026-03-12 — aucun artefact de publication de DeerFlow 2.0 n'est vérifié pour cette date. Des retours de la communauté décrivaient des erreurs d'outils pouvant interrompre les flux d'agents. D'autres signalaient qu'un checkpointer Postgres personnalisé était ignoré par `make dev/start`. Aucun de ces retours ne prouve un comportement livré ni une nouvelle version.

## Mode d'emploi {#how-to-use-this}

1. Clonez le dépôt et exécutez `make setup` pour choisir un fournisseur de modèles, une recherche optionnelle et les paramètres de bac à sable/Bash/écriture de fichiers ; cela crée `config.yaml` et `.env`.
  — <https://github.com/bytedance/deer-flow>
2. Exécutez `make doctor`, puis utilisez `make docker-init` et `make docker-start` pour le développement avec Docker ; l'application locale est servie sur `localhost:2026`.
  — <https://github.com/bytedance/deer-flow>
3. Utilisez `make check`, `make install` et `make dev` pour le développement local ; sous Windows, exécutez les scripts locaux via Git Bash plutôt que via PowerShell ou cmd natifs.
  — <https://github.com/bytedance/deer-flow>
4. Considérez l'espace de travail public comme une démonstration : l'état de démonstration observé ne comporte aucune tâche à faire, validez donc la planification sur une instance auto-hébergée.
  — <https://deerflow.tech/workspace/>

## Bonnes pratiques {#best-practices}

- Utilisez Linux avec Docker pour un service persistant ; la taille de serveur de départ documentée est de 8 vCPU, 16 Go de RAM et 40 Go de SSD libres.
  — <https://github.com/bytedance/deer-flow>
- Conservez `GATEWAY_WORKERS=1` sauf si Postgres, le pont de flux Redis, les heartbeats de propriété des exécutions et les événements d'exécution adossés à la base de données sont configurés.
  — <https://github.com/bytedance/deer-flow>
- Limitez d'abord la Gateway à la boucle locale (loopback). Avant toute exposition à distance, créez un compte administrateur et ajoutez une liste d'autorisation d'adresses IP, une authentification préalable au niveau du reverse proxy et un isolement réseau.
  — <https://github.com/bytedance/deer-flow>
- Utilisez Docker/AIO, Kubernetes ou E2B lorsque l'accès shell nécessite une frontière de système de fichiers applicable ; Bash sur l'hôte avec le bac à sable local est réservé aux workflows entièrement fiables.
  — <https://github.com/bytedance/deer-flow>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-02-14 — Considérer la branche active `main` comme le framework DeerFlow 1.x d'origine n'est plus valable pour les nouveaux travaux, selon l'instruction du mainteneur d'utiliser main avec la nouvelle version. La branche historique reste maintenue séparément.
- 2026-06-25 — La version immuable `v2.0.0` (`7e7f041`) remplace le statut de sélection des RC comme base de publication formelle de la 2.0. Cela ne certifie pas rétroactivement l'ensemble de fonctionnalités du 12 mars.

## Inconnues restantes {#still-unknown}

- L'événement comporte des liens, mais aucun texte source public ni instantané figé de mars ; il est donc impossible de rattacher à la date du 2026-03-12 un commit, un tag ou un ensemble de fonctionnalités exact de DeerFlow 2.0.
- Aucune source de première main datée de mars n'établit la liste exacte des modèles pris en charge ; les recommandations actuelles sur les modèles sont des indications courantes, et non des preuves de mars.
- `bytedance/deerflow` est la clé de sujet fournie, alors que le slug officiel du dépôt est `bytedance/deer-flow`.
- Nous n'avons exécuté aucune instance auto-hébergée durant cette recherche ; les énoncés d'exploitation actuels ne relèvent que de la documentation.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/bytedance/deer-flow | GitHub - bytedance/deer-flow | 2026-09-07 |
| https://deerflow.tech/ | DeerFlow | 2026-09-07 |
| https://deerflow.tech/workspace/ | DeerFlow workspace | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/824 | Release Plan of DeerFlow 2.0 · Issue #824 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1109 | Tool-call failure should degrade to error ToolMessage instead of aborting conversation · Issue #1109 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1118 | checkpointer not working with "make start" command · Issue #1118 | 2026-09-07 |
| https://deerflow.tech/blog/posts | All Posts | 2026-09-07 |
| https://github.com/bytedance/deer-flow/releases/tag/v2.0.0 | DeerFlow 2.0.0 released | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:deerflow`, fil `agent-platforms`, 1 événement daté du 2026-03-12 au 2026-03-12.
- **Note pratique :** voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne.
