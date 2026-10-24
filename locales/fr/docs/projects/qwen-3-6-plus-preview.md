---
title: "Qwen 3.6 Plus Preview — Disponibilité publique du modèle"
category: projects
date: 2026-03-31
tags: [project, public-model-availability, qwen, qwen-3-6-plus-preview]
aliases: ["Qwen 3.6 Plus Preview"]
level: 2
source_sha256: 11f18cc766d92b7128b3c2ff5b8dadaf0aaa14a51ee1f58ac6f4998cb1d37510
translation: machine
translated_at: '2026-10-24'
---
# Qwen 3.6 Plus Preview — Disponibilité publique du modèle {#qwen-36-plus-preview-public-model-availability}

**Ligne de développement :** `project:qwen-3-6-plus-preview` · fil `public-model-availability`  
**Dernier événement :** 2026-03-31 · 1 événement daté depuis le 2026-03-31 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Qwen 3.6 Plus Preview est un modèle en préversion hébergé par Qwen, disponible sous l'identifiant `qwen/qwen3.6-plus-preview:free` sur OpenRouter.

- Codage agentique, développement front-end et raisonnement général.
- Fenêtre de contexte de 1 000 000 de tokens.
- OpenRouter le présente comme gratuit, mais les prompts et les complétions peuvent être utilisés pour améliorer le modèle.

## Ligne de développement {#development-line}

- **2026-03-31 — Signal de disponibilité sur OpenRouter pour Qwen 3.6 Plus Preview.** Le 2026-03-31, l'enregistrement reliait Qwen 3.6 Plus Preview à une URL OpenRouter marquée comme point de terminaison gratuit. Il propose d'enregistrer ce signal daté de disponibilité publique, et non un lancement vérifié du modèle : les éléments disponibles n'établissent ni l'opérateur, ni les capacités, ni les conditions, ni le fait que le point de terminaison était en service à cette date.

## Évolutions {#what-changed}

2026-03-31 — Qwen 3.6 Plus Preview est devenu accessible via OpenRouter en tant que point de terminaison gratuit en préversion ; OpenRouter indique la date de sortie au 2026-03-30. 2026-04-03 — un signalement communautaire non résolu indiquait que le modèle était indisponible via l'API internationale DashScope, malgré sa disponibilité sur Qwen Chat et sur l'outil en ligne de commande gratuit Qwen Code.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-31, les praticiens devraient considérer Qwen 3.6 Plus Preview comme une option possible de point de terminaison gratuit sur OpenRouter, uniquement après avoir vérifié la disponibilité et les conditions actuelles ; cet enregistrement n'établit aucune affirmation sur les capacités ou la provenance du modèle.

1. Créez une clé d'API OpenRouter, puis envoyez une requête standard compatible OpenAI vers `POST /api/v1/chat/completions` avec le modèle `qwen/qwen3.6-plus-preview:free`.
  — <https://openrouter.ai/docs/api_reference/overview>
2. Commencez par une tâche d'évaluation bornée, comme la revue d'un dépôt ou l'analyse d'un long document ; ne soumettez pas de données confidentielles, car la page du modèle indique que les prompts et les complétions peuvent être collectés pour amélioration.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
3. En cas d'échec lié au quota, inspectez le point de terminaison de la clé et respectez l'en-tête `Retry-After` ; utilisez un backoff exponentiel pour les réponses 429.
  — <https://openrouter.ai/docs/api_reference/limits>

## Bonnes pratiques {#best-practices}

- Traitez ceci comme un chemin d'évaluation en préversion : fixez l'identifiant exact du modèle et conservez les sorties de tests représentatifs avant d'en faire une dépendance.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- N'envoyez pas de prompts ou de complétions sensibles via ce point de terminaison, car OpenRouter indique qu'ils peuvent être collectés pour améliorer le modèle.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- Mettez en place un backoff et une surveillance des quotas pour les requêtes vers les modèles gratuits ; la capacité des fournisseurs et les limites de la plateforme peuvent renvoyer des erreurs 429.
  — <https://openrouter.ai/docs/api_reference/limits>

## Remplacé par cet enregistrement {#superseded-by-this}

- 2026-03-31 : l'hypothèse selon laquelle la date de sortie était définitivement le 31 mars est corrigée par la page actuelle du modèle sur OpenRouter, qui indique le 30 mars 2026.
- 2026-03-31 : considérer Qwen 3.6 Plus Preview comme une version locale ou à poids ouverts de Qwen n'est pas étayé ; le mode d'accès vérifié est la fiche hébergée sur OpenRouter.

## Inconnues {#still-unknown}

- Aucune fiche modèle, aucun rapport de benchmark, aucun nombre de paramètres, aucune spécification d'architecture, aucun tarif après la préversion ni aucune déclaration officielle de disponibilité n'a été trouvé pour ce modèle précis.
- L'affirmation de disponibilité sur DashScope du 3 avril est le témoignage d'un utilisateur dans un ticket GitHub de Qwen, et non une confirmation des mainteneurs.
- La page OpenRouter actuelle reste accessible et désigne le modèle comme gratuit, mais une page publique ne prouve à elle seule ni la capacité, ni le routage chez les fournisseurs, ni l'adéquation à un trafic de production.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://openrouter.ai/qwen/qwen3.6-plus-preview:free | Qwen3.6 Plus Preview - API Pricing & Providers | OpenRouter | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/overview | OpenRouter API Reference - Complete Documentation | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/limits | API Credit & Rate Limits - Handle 402 and 429 Errors | 2026-09-05 |
| https://github.com/QwenLM/Qwen3/issues/1838 | Qwen3.6 Plus - International API Access? · Issue #1838 · QwenLM/Qwen3 | 2026-09-05 |
| https://www.ithome.com/0/934/546.htm | 阿里通义千问 Qwen 3.6 Plus 免费预览版上线 OpenRouter | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:qwen-3-6-plus-preview`, fil `public-model-availability`, 1 événement daté du 2026-03-31 au 2026-03-31.
- **Note pratique :** À partir du 2026-03-31, les praticiens devraient considérer Qwen 3.6 Plus Preview comme une option possible de point de terminaison gratuit sur OpenRouter, uniquement après avoir vérifié la disponibilité et les conditions actuelles ; cet enregistrement n'établit aucune affirmation sur les capacités ou la provenance du modèle.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
