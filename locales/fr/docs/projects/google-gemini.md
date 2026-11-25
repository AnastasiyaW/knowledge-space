---
title: "Gemini"
category: projects
date: 2026-07-22
tags: [gemini, gemini-app, gemini-gems, gemini-product-development, google-gemini, project]
aliases: ["Gemini", "Google Gemini"]
level: 3
source_sha256: ce252c4cf2fd525d123c2533549a65e9ac37ed8108c55429969039e487c48dc0
translation: machine
translated_at: '2026-10-24'
---
# Gemini {#gemini}

**Ligne de développement :** `project:google-gemini` · fil `gemini-product-development`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Gemini est la famille de produits de Google pour le chat, les fichiers, le code et l'intégration de modèles dans des applications.
- Gemini Apps : conversation, pièces jointes et choix du modèle.
- Gems : instructions enregistrées pour des tâches répétitives.
- Gemini API et AI Studio : appels multimodaux, sorties structurées et outils.

Les identifiants et statuts des modèles disponibles évoluent ; le catalogue actuel inclut `gemini-3.8-flash`, tandis que `gemini-3.6-flash` reste listé. Utilisez un Gem pour les routines personnelles, et l'API avec un choix de modèle explicite et des contrôles de réponse pour les produits.

## Ligne de développement {#development-line}

- **2026-07-22 — Gemini 3.6 Flash a été associé aux variantes Flash mises à jour.** Une page Google liée datée du 2026-07-21 présentait Gemini 3.6 Flash, 3.5 Flash-Lite et un pilote limité de 3.5 Flash Cyber ; 3.6 et 3.5 Flash-Lite sont devenus disponibles via Gemini API et AI Studio.

## Ce qui a changé {#what-changed}

- 2024-05-14 — Gemini Apps : Gemini Advanced a reçu Gemini 1.5 Pro avec une fenêtre de contexte d'un million de tokens et l'envoi de fichiers.
- 2024-05-14 — Gems : Google a présenté en avant-première des versions personnalisables de Gemini, marquées « bientôt » plutôt que comme un lancement public confirmé.
- 2024-05-14 — Gemini API : Google a introduit Gemini 1.5 Flash pour les tâches à haute fréquence, tandis que Gemini 1.5 Pro a gagné un contexte allant jusqu'à 2 millions de tokens et le traitement audio dans l'API et AI Studio.
- 2024-12-20 — AI Studio : une nouvelle URL de chat est apparue sans préciser le modèle, la version ou la sortie, de sorte que le changement précis n'est pas confirmé.
- 2026-07-22 — Gamme Flash : une page Google liée datée du 2026-07-21 présentait Gemini 3.6 Flash, 3.5 Flash-Lite et un pilote limité de 3.5 Flash Cyber ; 3.6 et 3.5 Flash-Lite sont devenus disponibles via Gemini API et AI Studio.
- 2026-09-04 — Catalogue actuel : Gemini API liste `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash` et `gemini-3.5-flash-lite` ; 3.6 n'est plus le seul choix actuel.

3.5 Flash Cyber n'est pas devenu un modèle public d'API ; Google décrit un pilote destiné aux gouvernements et aux partenaires de confiance via CodeMender. Choisissez une version dans le catalogue actuel pour les nouvelles intégrations, et non à partir d'un ancien lien AI Studio.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-22, considérez Gemini 3.6 Flash comme un candidat de modèle dans AI Studio, et vérifiez ses capacités, son déploiement et sa tarification dans la mise à jour officielle du modèle liée avant de l'adopter.

1. Pour les tâches personnelles, ouvrez Gemini Apps, connectez-vous, choisissez un modèle, joignez un fichier ou une image si nécessaire, puis envoyez le prompt.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
2. Pour les rôles répétitifs, ouvrez Explore Gems → New Gem. Définissez le nom, ajoutez des instructions couvrant le rôle, la tâche, le contexte et le format, testez dans l'aperçu, puis enregistrez.
  — <https://support.google.com/gemini/answer/15235603>
3. Pour les intégrations, créez un projet et une clé API dans AI Studio. Stockez la clé dans une variable d'environnement, installez le SDK, et effectuez le premier appel à l'API Interactions depuis Python, JavaScript ou REST.
  — <https://ai.google.dev/gemini-api/docs/get-started>
4. Avant la mise en production, figez un identifiant de modèle exact issu du catalogue en ligne dans la configuration. La documentation actuelle commence par `gemini-3.8-flash`.
  — <https://ai.google.dev/gemini-api/docs/models?hl=en>
5. Lorsque les réponses nécessitent des données récentes, connectez Google Search. Lorsque vous appelez des systèmes internes, déclarez une fonction, exécutez-la dans l'application et renvoyez le résultat au modèle.
  — <https://ai.google.dev/gemini-api/docs/tools>

## Bonnes pratiques {#best-practices}

- Énoncez explicitement l'objectif, les contraintes, le format et le contexte ; utilisez plusieurs exemples cohérents lorsque le style ou la classification est important.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Pour Gemini 3.x, conservez d'abord les valeurs par défaut de temperature, top-p et top-k ; documentez et testez chaque modification, car un réglage peut dégrader le raisonnement complexe ou provoquer des boucles.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Utilisez les Structured Outputs pour les formats finaux figés, et le Function Calling pour les actions ; vérifiez la sémantique et les règles métier du schéma JSON.
  — <https://ai.google.dev/gemini-api/docs/structured-output>
- Vérifiez les réponses de Gemini Apps avant toute décision professionnelle ; la documentation d'aide avertit explicitement que l'application peut commettre des erreurs.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
- Choisissez un palier avant d'envoyer des données de travail ; Google indique que le contenu de l'offre Free sert à entraîner les produits alors que l'offre Paid ne le fait pas, donc vérifiez les conditions de votre équipe et de votre contrat.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Remplacé par ceci {#superseded-by-this}

- 2024-05-14 : « Gems coming soon » est obsolète ; la documentation d'aide actuelle explique comment créer, tester et enregistrer des Gems.
- 2024-05-14 : démarrer une nouvelle intégration API avec Gemini 1.5 Flash ou 1.5 Pro est obsolète ; le catalogue actuel de Gemini API se concentre sur la série 3.x et liste Gemini 3.8 Flash.
- 2026-07-22 : Gemini 3.6 Flash et 3.5 Flash-Lite restent disponibles, mais 3.6 Flash n'est plus le modèle Flash le plus récent ; le catalogue contient aussi 3.7 et 3.8 Flash.
- 2024-12-20 : la nouvelle URL de chat AI Studio est un point d'entrée, et non une recommandation de version stable de modèle.

## Toujours inconnu {#still-unknown}

- Le texte exact des deux entrées du 2024-05-14 n'est pas disponible ; les annonces officielles de ce jour confirment l'orientation, et non le texte intégral.
- L'entrée du 2024-12-20 ne fournit qu'une nouvelle URL de chat AI Studio, sans préciser de modèle, de version ou de sortie.
- Gemini Apps, Gems et Gemini API sont des surfaces différentes d'une même famille, et non des projets distincts ; la disponibilité dépend du compte, du palier, de la région et du modèle.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://blog.google/products-and-platforms/products/gemini/google-gemini-update-may-2024/ | Get more done with Gemini: Try 1.5 Pro and more intelligent features | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-gemini-update-flash-ai-assistant-io-2024/ | Gemini breaks new ground with a faster model, longer context, AI agents and more | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models?hl=en | Models | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/get-started | Getting started | Gemini API | Google AI for Developers | 2026-09-04 |
| https://support.google.com/gemini/answer/13275745?hl=en | Use Gemini Apps | 2026-09-04 |
| https://support.google.com/gemini/answer/15235603 | Tips for creating custom Gems | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/tools | Using tools with Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/structured-output | Structured outputs | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | Gemini API | Google AI for Developers | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:google-gemini`, fil `gemini-product-development`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Note pratique :** À partir du 2026-07-22, les praticiens doivent considérer Gemini 3.6 Flash comme un candidat de sélection de modèle dans AI Studio, et vérifier ses capacités, son déploiement et sa tarification dans la mise à jour officielle du modèle liée avant de l'adopter.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
