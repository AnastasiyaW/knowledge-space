---
title: "Laminar"
category: projects

tags: [laminar, laminar-development, project]
aliases: ["Laminar"]
level: 3
source_sha256: a6a945feac985cfd2f98fa1c309efc8dde00c215491e73926a668d1d4b096995
translation: machine
translated_at: '2026-10-24'
---
# Laminar {#laminar}

**Ligne de développement :** `project:laminar` · fil `laminar-development`  
**Dernier événement :** - · 0 événement daté depuis - · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Laminar est une plateforme d'observabilité native OpenTelemetry destinée aux développeurs d'agents, et une alternative à Langfuse ou Helicone plutôt qu'une passerelle LLM.

- Traçage : tracer les appels LLM et les appels d'outils.
- Sessions navigateur : inspecter les exécutions interactives.
- Évaluations : exécuter des jeux de données d'évaluation.
- Signaux : détecter les défaillances récurrentes.
- SQL : interroger directement les données d'exécution.
- Points d'arrêt : rejouer une exécution en échec.

L'auto-hébergement nécessite une pile multi-services. Les Signaux nécessitent une clé d'API Google Generative AI.

## Ligne de développement {#development-line}

- Nous n'avons pas encore rédigé la chronologie datée ; ce que nous savons figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-03-16 — Laminar a annoncé un tour de table d'amorçage (seed) de 3 millions de dollars et a positionné le produit autour du débogage et de la supervision d'agents de longue durée : vues de transcription des traces, rejeu des sessions navigateur, débogueur pas à pas, Signaux, analyse SQL et jeux de données d'évaluation.
- 2026-03-18 — Le financement annoncé était de 3 millions de dollars, mené par Atlantic.vc avec la participation de Y Combinator, AAL.vc, Ben Sigelman et Ant Wilson ; le périmètre du produit était l'observabilité des agents et non la sortie d'un modèle.
- 2026-07-09 — La version v0.2.1 a ajouté une interface Clusters remaniée, un chemin de base configurable pour le frontend, des métadonnées d'expiration des clés d'API, la connexion CLI dans l'intégration, et des modifications de l'alerting des Signaux.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-18, n'apportez encore aucune modification d'implémentation ou d'adoption ; vérifiez d'abord l'annonce Laminar liée, l'état du dépôt et la référence du modèle.

1. Créez un projet et une clé d'API de projet, installez le SDK TypeScript, et appelez Laminar.initialize au démarrage de l'application, avant tout appel de modèle.
  — <https://github.com/lmnr-ai/lmnr>
2. Encapsulez les points d'entrée des agents et les fonctions applicatives significatives avec observe afin que la trace contienne le flux de travail et non seulement un span racine.
  — <https://github.com/lmnr-ai/lmnr>
3. Pour Python, installez lmnr avec uniquement les instrumentations requises par l'application, initialisez-le une fois tôt au démarrage, et fournissez LMNR_PROJECT_API_KEY via l'environnement.
  — <https://github.com/lmnr-ai/lmnr-python>
4. Choisissez l'hébergement géré pour le chemin le plus court, ou l'auto-hébergement avec Docker Compose ; utilisez la configuration Compose complète pour les charges de production.
  — <https://github.com/lmnr-ai/lmnr>
5. Examinez les traces et les Signaux, puis utilisez l'éditeur SQL intégré pour transformer les observations de production en jeux de données et exécuter des évaluations sur ceux-ci.
  — <https://laminar.sh/blog/2026-03-16-laminar-launch>

## Bonnes pratiques {#best-practices}

- Initialisez le SDK une seule fois, tôt au démarrage, plutôt qu'à chaque requête ou appel d'outil.
  — <https://github.com/lmnr-ai/lmnr-python>
- Conservez la conception de spans OpenTelemetry existante et dirigez son exportateur OTLP vers Laminar au lieu de dupliquer l'instrumentation.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>
- N'utilisez la pile Docker Compose allégée que pour des démarrages rapides ou un usage léger ; utilisez l'hébergement géré ou docker-compose-full.yml en production.
  — <https://github.com/lmnr-ai/lmnr>
- Ne considérez pas Laminar comme un remplacement des fonctions de passerelle telles que le routage entre fournisseurs, la mise en cache des réponses ou la limitation de débit.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-16 — La description de lancement initiale est incomplète pour la planification du déploiement : le projet actuel comprend les changements de la version v0.2.1, notamment les chemins de base configurables du frontend et les métadonnées d'expiration des clés d'API.

## Toujours inconnu {#still-unknown}

- Le lien court Hugging Face fourni n'a pas pu être récupéré ; nous ne l'avons donc pas utilisé comme preuve.
- Le schéma omettait les champs event_findings et new_events ; nous avons intégré leurs faits étayés dans Ce qui a changé.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://laminar.sh/ | Laminar — Open-source observability for AI agents | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr | lmnr-ai/lmnr — Laminar open-source observability platform | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr-python | lmnr-ai/lmnr-python — Laminar Python SDK | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/releases | lmnr-ai/lmnr releases | 2026-09-05 |
| https://laminar.sh/blog/2026-03-16-laminar-launch | Laminar raised $3M to build observability for long-running agents | 2026-09-05 |
| https://startuprise.co.uk/laminar-raises-3m-seed-round-led-by-atlantic-vc-to-expand-ai-agent-observability/ | Laminar Raises $3M Seed Round Led by Atlantic.vc To Expand AI Agent Observability | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx | Migrate from Helicone to Laminar | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:laminar`, fil `laminar-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-03-18, n'apportez encore aucune modification d'implémentation ou d'adoption ; vérifiez d'abord l'annonce Laminar liée, l'état du dépôt et la référence du modèle.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
