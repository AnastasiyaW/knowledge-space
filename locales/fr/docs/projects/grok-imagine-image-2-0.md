---
title: "Grok Imagine Image 2.0 — génération d'images Grok Imagine"
category: projects
date: 2026-08-10
tags: [grok, grok-imagine-image, grok-imagine-image-2-0, project]
aliases: ["Grok Imagine Image 2.0"]
level: 2
source_sha256: 3c951526db903196636baa4584cf38f75f6879e486fb93d0ac496ef10b60bab4
translation: machine
translated_at: '2026-10-24'
---
# Grok Imagine Image 2.0 — génération d'images Grok Imagine {#grok-imagine-image-20-grok-imagine-image-generation}

**Ligne de développement :** `project:grok-imagine-image-2-0` · fil `grok-imagine-image`  
**Dernier événement :** 2026-08-10 · 1 événement daté depuis le 2026-08-10 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Grok Imagine Image 2.0 est un modèle xAI de génération et de modification d'images, disponible dans Grok et dans l'API. Fonctionnalités : texte-vers-image, modification selon une instruction, jusqu'à cinq images de référence, résolutions 1K/2K et traitement par lots. Prix de l'API : à partir de 0,04 $ par image ; pour un résultat reproductible, fixez explicitement `quality`. Verdict : adapté aux maquettes itératives et au compositing, mais le défaut de qualité modifie désormais le coût et le résultat.

## Ligne de développement {#development-line}

- **2026-08-10 — Grok Imagine Image 2.0 a été présenté dans une entrée d'actualité produit de xAI.** Le modèle est devenu disponible en tant que Quality Mode dans Grok et sous `grok-imagine-image-2.0` dans l'API.

## Ce qui a changé {#what-changed}

2026-08-10 — cet événement correspond à la sortie générale, mais l'annonce officielle est datée du 2026-08-07 : le modèle est devenu disponible en tant que Quality Mode dans Grok et sous `grok-imagine-image-2.0` dans l'API. 2026-08-28 — `quality=auto` est devenu une valeur admise, et la valeur par défaut est passée de `medium` à `auto` ; actuellement, auto sélectionne Low pour la génération et Medium pour la modification. La limite de références est également passée de trois à cinq, et les proportions 21:9 et 5:2 ont été ajoutées. 2026-09-02 — le retrait de `grok-imagine-image-quality` a été annoncé pour le 2026-11-02 : ses requêtes seront traitées par Image 2.0 avec `quality=low` ; Image 1.0 n'est pas concerné.

À la date de l'événement, 2026-08-10, une précision officielle supplémentaire s'applique : la sortie initiale a eu lieu le 2026-08-07, et non le 2026-08-10 ; le périmètre de la sortie comprend grok.com/imagine, iOS, Android et l'API.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-10, les praticiens qui évaluent Grok Imagine doivent considérer Image 2.0 comme une étape datée de la ligne de produits et consulter les pages xAI et Grok liées ; ils doivent en outre vérifier séparément les fonctionnalités, l'accès et la disponibilité avant de s'y fier.

1. Ouvrez Grok Imagine et sélectionnez Quality Mode pour la génération ou la modification interactive.
  — <https://x.ai/news/grok-imagine-image-2>
2. Pour l'API, créez une clé dans xAI Console et appelez le modèle `grok-imagine-image-2.0`.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
3. Pour une nouvelle image, envoyez le prompt à `POST /v1/images/generations` ; précisez le nombre de résultats, le ratio d'aspect et la résolution.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
4. Pour une retouche, envoyez l'URL ou le data URI base64 de l'image source à `POST /v1/images/edits` et décrivez la modification souhaitée.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
5. Pour le compositing, transmettez jusqu'à cinq images sources dans une seule requête d'édition.
  — <https://docs.x.ai/developers/model-capabilities/imagine>

## Bonnes pratiques {#best-practices}

- Transmettez explicitement `quality=low` ou `quality=medium` : `auto` est devenu le défaut le 2026-08-28 et choisit une qualité différente pour la génération et pour la modification.
  — <https://docs.x.ai/developers/release-notes>
- Fixez le slug `grok-imagine-image-2.0` dans les nouvelles intégrations ; ne planifiez pas de nouveaux travaux sur `grok-imagine-image-quality`, qui sera retiré le 2026-11-02.
  — <https://docs.x.ai/developers/release-notes>
- Comptez séparément les images en entrée : une modification facture à la fois l'image d'entrée et le résultat généré.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
- Pour de grands ensembles indépendants, utilisez la Batch API prise en charge par le modèle plutôt que de dépasser la limite de six requêtes par seconde sur l'API en temps réel.
  — <https://docs.x.ai/developers/models/grok-imagine-image-2.0>

## Ce qui est désormais obsolète {#superseded-by-this}

- 2026-08-28 : l'hypothèse précédente selon laquelle un `quality` omis équivaut à `medium` n'est plus valable ; désormais, c'est `auto`.
- 2026-09-02 : pour les nouvelles intégrations, la recommandation d'utiliser `grok-imagine-image-quality` devient obsolète ; son retrait est fixé au 2026-11-02.

## Points encore inconnus {#still-unknown}

- La page officielle grok.com/imagine n'a pas fourni de texte exploitable lors de la vérification ; les tarifs précis et la disponibilité géographique de l'interface grand public ne sont donc pas confirmés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://x.ai/news/grok-imagine-image-2 | Imagine Image 2.0 | SpaceXAI | 2026-09-05 |
| https://docs.x.ai/developers/model-capabilities/imagine | Imagine Overview | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/models/grok-imagine-image-2.0 | Grok Imagine Image 2.0 | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/release-notes | Release Notes | SpaceXAI Docs | 2026-09-05 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:grok-imagine-image-2-0`, fil `grok-imagine-image`, 1 événement daté, du 2026-08-10 au 2026-08-10.
- **Remarque pratique :** À partir du 2026-08-10, les praticiens qui évaluent Grok Imagine doivent considérer Image 2.0 comme une étape datée de la ligne de produits et consulter les pages xAI et Grok liées ; ils doivent en outre vérifier séparément les fonctionnalités, l'accès et la disponibilité avant de s'y fier.
- **Confiance :** élevée. Les mentions datées « désormais obsolète » font foi pour ce qui est obsolète.
