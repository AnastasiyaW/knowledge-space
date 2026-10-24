---
title: "GPT-5.5"
category: projects
date: 2026-04-23
tags: [gpt-5-5, gpt-5-5-announcement, project]
aliases: ["GPT-5.5"]
level: 3
source_sha256: 449f2aaef4cb530c6f7bb8d84a57e7c44078a4c92a15c5d8377a39f0a2cb17a4
translation: machine
translated_at: '2026-10-24'
---
# GPT-5.5 {#gpt-55}

**Ligne de développement :** `project:gpt-5-5` · fil `gpt-5-5-announcement`  
**Dernier événement :** 2026-04-23 · 1 événement daté depuis le 2026-04-23 · **Consulté le :** 2026-09-06 · confiance : élevée

## Ce que c'est {#what-it-is}

GPT-5.5 — un modèle de l'API OpenAI destiné aux équipes qui développent des agents de programmation, des agents utilisant des outils et des agents pour le travail professionnel.

- Prend en charge Responses et Chat Completions, l'appel de fonctions, les sorties structurées, les outils hébergés, l'utilisation de l'ordinateur (computer use) et MCP.
- Propose l'instantané épinglé `gpt-5.5-2026-04-23`.

Fenêtre de contexte de 1 050 000 tokens ; sortie maximale de 128 000 tokens ; l'offre API Free n'est pas prise en charge. Conservez-le pour une charge de travail épinglée ou évaluée, mais utilisez GPT-6 Astra comme référence pour les nouvelles charges de travail.

## Ligne de développement {#development-line}

- **2026-04-23 — Annonce de GPT-5.5.** Le 2026-04-23, une annonce d'OpenAI a marqué une étape publique majeure pour GPT-5.5. Cette annonce confirme une étape publique datée pour le projet, mais n'établit ni les capacités, ni la disponibilité, ni les tarifs, ni les détails de migration.

## Ce qui a changé {#what-changed}

- **2026-04-23 :** GPT-5.5 a commencé à être déployé dans ChatGPT et Codex pour les formules éligibles, pour la programmation, l'utilisation de l'ordinateur, le travail de bureau et la recherche.
- **2026-04-24 :** GPT-5.5 et GPT-5.5 Pro sont devenus disponibles dans l'API ; des garde-fous de déploiement API ont été ajoutés.
- **2026-05-05 :** GPT-5.5 Instant a remplacé GPT-5.3 Instant comme modèle par défaut de ChatGPT et est apparu dans l'API sous `chat-latest`.
- **2026-05-07 :** GPT-5.5-Cyber a ouvert un aperçu à accès limité destiné aux défenseurs qui sécurisent les infrastructures critiques.
- **2026-05-28 :** GPT-5.5 Instant a reçu une mise à jour de style pour ChatGPT et l'API ; Canvas a été supprimé pour Instant et Thinking.
- **2026-06-09 :** la personnalisation d'Instant a été étendue à ChatGPT Go et Free, la formule Free utilisant un ensemble réduit de conversations passées.
- **2026-06-24 :** ChatGPT a mis à jour Instant pour le contexte multi-tours, les contraintes complexes et les conversations orientées vers la décision.
- **2026-07-06 :** GPT-5.5 Instant Mini a remplacé GPT-5.3 Instant Mini comme solution de repli de ChatGPT après atteinte des limites de débit d'Instant ou d'Auto.

## Comment l'utiliser {#how-to-use-this}

1. Choisissez `gpt-5.5` pour l'alias maintenu, ou `gpt-5.5-2026-04-23` lorsque le comportement doit rester figé ; vérifiez d'abord votre palier d'utilisation de l'API.
  — <https://developers.openai.com/api/docs/models/gpt-5.5>
2. Utilisez l'API Responses pour le raisonnement, l'appel d'outils ou les travaux multi-tours.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
3. Commencez avec `reasoning.effort: medium`. Évaluez `low` pour les travaux sensibles à la latence, et n'augmentez l'effort qu'après une évaluation représentative.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
4. Utilisez les sorties structurées, `previous_response_id` pour l'état de la réponse, et un préfixe de prompt stable pour le trafic répété mis en cache.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
5. Pour un nouveau système, fixez l'objectif de précision avec GPT-6 Astra, puis comparez le coût et la latence avant de conserver GPT-5.5.
  — <https://developers.openai.com/api/docs/guides/model-selection>

## Bonnes pratiques {#best-practices}

- Considérez GPT-5.5 comme une nouvelle famille de modèles. Partez d'une base de prompt neuve et minimale plutôt que de reprendre une ancienne pile de prompts.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Énoncez le résultat attendu, les critères de réussite, les contraintes, les règles de preuve, la forme de la sortie et les conditions d'arrêt. Évitez les instructions procédurales, sauf si le chemin lui-même est imposé.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Utilisez les sorties structurées plutôt que d'intégrer un schéma JSON dans le texte du prompt.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Placez le contenu stable du prompt en premier et le contexte dynamique en dernier. Utilisez `prompt_cache_key` de manière cohérente et contrôlez l'utilisation des tokens mis en cache.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Décrivez dans les descriptions d'outils les entrées, les effets de bord, la sécurité des relances et les modes de défaillance. Conservez `phase` à l'identique si les éléments de l'assistant sont rejoués manuellement.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>

## Remplacé par {#superseded-by-this}

- :{

## Toujours inconnu {#still-unknown}

- La disponibilité, les limites de débit et le sélecteur de modèles de ChatGPT dépendent du compte, de la formule, de la région et du palier API. Nous n'avons vérifié aucun compte cible.
- GPT-5.5, GPT-5.5 Pro, Thinking, Instant, Cyber et Instant Mini sont des variantes ou des modes d'accès distincts. Ne transférez pas les revendications d'accès, de sécurité ou de capacité entre eux.
- La page de lancement en chinois simplifié examinée n'a pas établi de déploiement spécifique à la Chine ni de droit d'accès API régional distinct.
- Les sources consultées ne contiennent aucune date officielle de retrait pour l'alias d'API `gpt-5.5`.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://openai.com/index/introducing-gpt-5-5/ | Introducing GPT-5.5 | 2026-09-06 |
| https://openai.com/index/gpt-5-5-system-card/ | GPT-5.5 System Card | 2026-09-06 |
| https://openai.com/zh-Hans-CN/index/introducing-gpt-5-5/ | 重磅发布 GPT-5.5 | 2026-09-06 |
| https://developers.openai.com/api/docs/models/gpt-5.5 | GPT-5.5 Model | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5 | Model guidance | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/model-selection | Model selection | OpenAI API | 2026-09-06 |
| https://openai.com/index/gpt-5-5-instant/ | GPT-5.5 Instant: smarter, clearer, and more personalized | 2026-09-06 |
| https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/ | Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber | 2026-09-06 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes | 2026-09-06 |

## Fiche pour l'agent {#agent-brief}

- **Sujet :** `project:gpt-5-5`, fil `gpt-5-5-announcement`, 1 événement daté du 2026-04-23 au 2026-04-23.
- **Note pratique :** voir les sections d'utilisation et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés font autorité pour déterminer ce qui est obsolète.
