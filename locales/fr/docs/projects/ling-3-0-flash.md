---
title: "Ling-3.0-flash — Disponibilité du modèle"
category: projects
date: 2026-07-27
tags: [ling-3-0-flash, ling_flash, model-availability, project]
aliases: ["Ling-3.0-flash"]
level: 3
source_sha256: 7121a3985c41133c59f10051dd5643a8471687d65ba1184e90e6f611a9ff88da
translation: machine
translated_at: '2026-10-24'
---
# Ling-3.0-flash — Disponibilité du modèle {#ling-30-flash-model-availability}

**Ligne de développement :** `project:ling-3-0-flash` · fil `model-availability`  
**Dernier événement :** 2026-07-27 · 1 événement daté depuis le 2026-07-27 · **Recherche effectuée le :** 2026-09-08 · confiance : élevée

## Présentation {#what-it-is}

Ling-3.0-flash est un MoE de génération de texte d'Ant Group, destiné aux équipes qui développent des agents de codage, utilisant des outils ou travaillant sur de longs contextes.

- Architecture MoE hybride linéaire native, avec raisonnement et appels d'outils.
- La route OpenRouter expose un contexte de 262 144 tokens et jusqu'à 32 768 tokens en sortie.

124 Md de paramètres au total, environ 5,1 Md actifs par token ; la route OpenRouter est uniquement textuelle. Elle convient aux charges de travail d'agents, mais nous devons conserver la validation JSON et l'exécution des outils dans l'application.

## Ligne de développement {#development-line}

- **2026-07-27 — Ling-3.0-flash a reçu une référence datée sur OpenRouter.** Le 2026-07-27, une entrée a été liée à la page publique du modèle Ling-3.0-flash d'InclusionAI sur OpenRouter. Elle fournit une référence publique datée pour ce modèle, mais n'établit ni sa date de lancement, ni ses capacités, ni sa disponibilité actuelle en service.

## Ce qui a changé {#what-changed}

- 2026-07-23 — Ant Ling v2.0.0 a rendu Ling-3.0-flash disponible dans le chat et via les API compatibles OpenAI et Anthropic, avec un bouton de réflexion approfondie.
- 2026-07-24 — L'annonce officielle de la version a ajouté une période d'accès gratuit limité sur Ant Ling et OpenRouter.
- 2026-07-27 — Ant Ling v2.0.1 a ajouté le module Explore ; il ne s'agissait ni d'une version du modèle Ling-3.0-flash, ni d'un changement de référencement chez le fournisseur.
- 2026-08-02 — Le dépôt officiel des poids de base a été initialisé et alimenté.
- 2026-08-04 — Les dépôts officiels des poids FP8 et INT4 ont été initialisés et alimentés.

## Mode d'emploi {#how-to-use-this}

1. Envoyez une requête Chat Completions compatible OpenAI à OpenRouter avec l'identifiant exact du modèle `inclusionai/ling-3.0-flash`, une clé Bearer et `messages`.
  — <https://openrouter.ai/docs/quickstart>
2. Maintenez le total prompt plus completion dans la limite actuelle de 262 144 tokens ; plafonnez la complétion à 32 768 tokens ou moins selon la charge de travail.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
3. Pour l'usage d'outils, envoyez `tools` et `tool_choice`, exécutez l'appel renvoyé dans le client, ajoutez son résultat, puis effectuez la requête de modèle suivante.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
4. Pendant un pilote en production, envoyez `X-OpenRouter-Metadata: enabled` et conservez les métadonnées de routage renvoyées afin de voir le fournisseur sélectionné et les tentatives de repli.
  — <https://openrouter.ai/docs/guides/features/router-metadata>

## Bonnes pratiques {#best-practices}

- Considérez les prix, la disponibilité et les chiffres des fournisseurs sur OpenRouter comme des observations ponctuelles, et non comme une propriété fixe du modèle ; vérifiez-les à nouveau avant tout engagement budgétaire ou de latence.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Ne vous appuyez pas sur `response_format` pour obtenir un JSON strict sur la route OpenRouter actuelle : sa page de modèle indique que le JSON n'est pas garanti. Validez la sortie analysée dans l'application.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Gardez l'exécution des outils sous le contrôle du client : le modèle propose un appel, tandis que l'application l'exécute et renvoie son résultat.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
- Pour une charge de travail avec schéma JSON strict, utilisez uniquement un endpoint qui annonce actuellement la prise en charge des sorties structurées, et exigez les paramètres supportés dans les préférences de routage.
  — <https://openrouter.ai/docs/guides/features/structured-outputs>
- Pour l'auto-hébergement, partez de la configuration d'échantillonnage recommandée par l'éditeur (`temperature=0.6`, `top_p=0.95`, `top_k=20`) et de sa configuration de parseur propre au runtime, plutôt que de la copier aveuglément vers une autre passerelle.
  — <https://huggingface.co/inclusionAI/Ling-3.0-flash>

## Remplacé par cette version {#superseded-by-this}

- 2026-07-27 — Considérer la date d'événement liée à OpenRouter comme la date de lancement de Ling-3.0-flash ; le journal officiel place le lancement du modèle au 2026-07-23, et la modification du 27 juillet concerne Explore.
- 2026-08-03 — Accès API gratuit pendant la période de lancement ; l'annonce officielle en fixait la fin à 23h00, heure de Pékin, de sorte que ce n'est plus une indication tarifaire en vigueur.

## Inconnues restantes {#still-unknown}

- Aucune preuve archivée de première mise en ligne n'établit qu'OpenRouter a d'abord exposé ce modèle le 2026-07-27 ; le lien daté prouve seulement une observation à cette date.
- L'ensemble actuel des fournisseurs, les prix, le routage et la matrice des fonctionnalités sur OpenRouter sont volatils et n'ont pas été reportés rétrospectivement sur l'événement de juillet.
- Ling-3.0-flash-VL est un modèle multimodal distinct, portant un nom à part ; les sources consultées n'établissent pas qu'il s'agit d'une mise à jour de point de contrôle de ce modèle textuel.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://openrouter.ai/models/inclusionai/ling-3.0-flash | URL du modèle OpenRouter fournie avec l'événement daté | 2026-09-08 |
| https://openrouter.ai/inclusionai/ling-3.0-flash | Ling 3.0 Flash - Tarifs API et benchmarks | OpenRouter | 2026-09-08 |
| https://developer.ant-ling.com/en/docs/getting-started/changelog/ | Journal des modifications | Ant Ling | 2026-09-08 |
| https://developer.ant-ling.com/zh-CN/blogs/ling-3.0-flash-release | Ling-3.0-flash：智以密胜 | Ant Ling | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash | inclusionAI/Ling-3.0-flash | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash/commits/main | Validations · inclusionAI/Ling-3.0-flash | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-fp8/commits/main | Validations · inclusionAI/Ling-3.0-flash-fp8 | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-int4/commits/main | Validations · inclusionAI/Ling-3.0-flash-int4 | Hugging Face | 2026-09-08 |
| https://openrouter.ai/docs/quickstart | Guide de démarrage rapide OpenRouter | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/tool-calling | Appels d'outils et de fonctions - Utiliser des outils avec OpenRouter | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/router-metadata | Métadonnées de routage - Inspecter les décisions de routage à chaque réponse | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/structured-outputs | Sorties structurées - Réponses JSON typées des modèles d'IA | 2026-09-08 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:ling-3-0-flash`, fil `model-availability`, 1 événement daté du 2026-07-27 au 2026-07-27.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
