---
title: "GPT-4"
category: projects
tags: [announcements, gpt-4, gpt-4-development, gpt_4_architecture, project]
aliases: ["GPT-4"]
level: 3
source_sha256: dcb23f62395c34ce6cc9e19384bb7372296fd187d7f0f9df9ab7499e603c5e4c
translation: machine
translated_at: '2026-10-24'
---
# GPT-4 {#gpt-4}

**Ligne de développement :** `project:gpt-4` · fil `gpt-4-development`  
**Événements :** 1 daté, 2023-03-09 → 2023-03-09 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

GPT-4 est un modèle OpenAI ancien, conservé pour maintenir les intégrations API existantes limitées au texte.

- Texte : accepte et renvoie du texte.
- Streaming : prend en charge le streaming.
- Fine-tuning : prend en charge le fine-tuning.
- Chat Completions : interface documentée.

Fenêtre de contexte de 8 192 tokens ; 30 $ en entrée et 60 $ en sortie par million de tokens ; les images, l'audio, la vidéo, l'appel de fonctions et les Structured Outputs ne sont pas pris en charge.

Ne le conservez que lorsque la compatibilité est mesurée ; utilisez un modèle plus récent pour les nouveaux développements.

## Ligne de développement {#development-line}

- **2023-03-09 — Prévision avant sortie pour GPT-4.** Le 2023-03-09, Microsoft Allemagne a annoncé que GPT-4 était attendu la semaine suivante et qu'il serait multimodal. Cette déclaration était une affirmation préalable à la sortie concernant les capacités attendues, et non une confirmation de la publication.

## Évolutions {#what-changed}

GPT-4 est passé d'une sortie générale à un rôle de modèle ChatGPT retiré et d'API héritée.

- 2023-03-09 : des informations préalables à la sortie prévoyaient un lancement multimodal imminent.
- 2023-03-14 : OpenAI a annoncé GPT-4 avec une entrée texte et image et une sortie texte. L'accès public s'est ouvert avec le texte, tandis que l'entrée image est restée en alpha limitée.
- 2023-06-22 : une entrée d'architecture ne comporte aucune URL, il est donc impossible de vérifier un changement d'architecture.
- 2023-07-06 : l'accès API est devenu généralement disponible pour les développeurs payants, avec la recommandation d'utiliser Chat Completions plutôt que l'ancienne API Completions.
- 2025-04-30 : OpenAI a retiré GPT-4 de ChatGPT et l'a remplacé par GPT-4o, tout en laissant l'API active.
- 2026-09-04 : la page individuelle du modèle indique `gpt-4` comme modèle par défaut ancien, tandis que le catalogue classe GPT-4 comme Deprecated.

Les limites d'utilisation documentées restent une fenêtre de contexte de 8 192 tokens et 30 $/60 $ par million de tokens de texte.

Considérez GPT-4 comme un modèle API hérité pour la compatibilité, et non comme un choix pour ChatGPT.

## Mode d'emploi {#how-to-use-this}

Considérez les informations du 2023-03-09 comme préliminaires tant que la documentation primaire ne confirme pas les capacités de sortie.

1. Évitez ChatGPT pour GPT-4, car OpenAI l'y a retiré le 2025-04-30 ; voir les [notes de version de ChatGPT](https://help.openai.com/en/articles/6825453). Utilisez-le uniquement lorsque les intégrations API existantes nécessitent un comportement hérité mesuré.
2. Envoyez une requête `GET /v1/models/gpt-4` authentifiée avant le déploiement pour consulter les identifiants de modèle visibles et les dates d'arrêt via l'[API Models](https://developers.openai.com/api/reference/resources/models).
3. Publiez des messages texte ordonnés avec le modèle défini sur `gpt-4` via le point de terminaison documenté `POST /v1/chat/completions`, comme décrit dans [Chat Completions](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions).
4. Exécutez des évaluations spécifiques à la tâche avant de conserver ou de remplacer GPT-4, en décidant selon le coût, les fonctionnalités et les scores de benchmark issus des [bonnes pratiques d'évaluation](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## Bonnes pratiques {#best-practices}

- Exécutez en continu des évaluations spécifiques à la tâche et calibrez les scores automatisés par un jugement humain, en suivant les [bonnes pratiques d'évaluation](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
- Maintenez une relecture humaine pour les sorties à forts enjeux et fournissez aux relecteurs les documents sources pour vérifier les réponses, conformément aux [bonnes pratiques de sécurité](https://developers.openai.com/api/docs/guides/safety-best-practices).
- Évitez de concevoir des workflows GPT-4 autour des images, de l'audio, des outils ou des Structured Outputs, car la [référence du modèle GPT-4](https://developers.openai.com/api/docs/models/gpt-4) les répertorie comme non pris en charge.
- Gardez les clés API hors du code source, séparez les environnements de préproduction et de production, et configurez des alertes de dépense avant le début du trafic, comme décrit dans les [bonnes pratiques de production](https://developers.openai.com/api/docs/guides/production-best-practices).

## Remplacé par {#superseded-by-this}

- 2023-03-09 : considérer les prévisions préalables à la sortie comme une disponibilité confirmée a été remplacé par le lancement d'OpenAI du 2023-03-14.
- 2023-03-14 : la recommandation de sélectionner GPT-4 dans ChatGPT est devenue obsolète le 2025-04-30, lorsque ChatGPT l'a remplacé par GPT-4o.
- 2023-03-14 : considérer l'entrée image comme une capacité de l'API est obsolète, car elle est restée en alpha limitée au lancement et la page actuelle de `gpt-4` la répertorie comme non prise en charge.
- 2023-07-06 : la recommandation de disponibilité générale est périmée, car la documentation actuelle qualifie GPT-4 d'ancien, le classe comme Deprecated dans le catalogue et exige une vérification du compte.

## Toujours inconnu {#still-unknown}

- L'entrée `gpt_4_architecture` du 2023-06-22 ne comporte ni URL ni texte public, il est donc impossible de vérifier une affirmation sur l'architecture.
- L'entrée du 2023-03-09 et les routes distinctes `openai_gpt4` / `gpt4_development` sont en conflit dans le registre ; on ne sait pas s'il s'agit de routes en double ou de sujets distincts.
- La documentation officielle se contredit : la page de détail de GPT-4 indique un alias `gpt-4` par défaut, alors que le catalogue classe GPT-4 comme Deprecated. Une vérification authentifiée de l'API Models est nécessaire pour confirmer l'accès.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.heise.de/news/GPT-4-is-coming-next-week-and-it-will-be-multimodal-says-Microsoft-Germany-7540972.html | GPT-4 is coming next week and it will be multimodal, says Microsoft Germany — Heise (accès actuel redirigé) | 2026-09-04 |
| https://openai.com/index/gpt-4-research/ | GPT-4 — OpenAI | 2026-09-04 |
| https://community.openai.com/t/gpt-4-api-general-availability-and-deprecation-of-older-models-in-the-completions-api/289518 | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI Developer Community | 2026-09-04 |
| https://openai.com/index/gpt-4-api-general-availability/ | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI | 2026-09-04 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes — OpenAI Help Center | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-4 | GPT-4 Model — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/all | All models — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/reference/resources/models | Models — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions | Completions — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/evaluation-best-practices | Evaluation best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/safety-best-practices | Safety best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/production-best-practices | Production best practices — OpenAI API | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:gpt-4`, fil `gpt-4-development`, 1 événement daté 2023-03-09 → 2023-03-09.
- **Note pratique :** Au 2023-03-09, considérez les informations de tiers sur une sortie multimodale de GPT-4 comme préliminaires tant que la documentation primaire ne confirme pas la disponibilité.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
