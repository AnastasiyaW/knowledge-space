---
title: "Gemini"
category: projects
date: 2026-08-14
tags: [gemini, gemini-development, project]
aliases: ["Gemini", "Gemini 1.5", "Gemini 3.7 Flash"]
level: 3
source_sha256: e5d207f43ce4282113d7bb6283d6dbfba5cab00c756546d63f12c491955a40bb
translation: machine
translated_at: '2026-10-24'
---
# Gemini {#gemini}

**Ligne de développement :** `project:gemini` · fil `gemini-development`  
**Dernier événement :** 2026-08-14 · 6 entrées datées depuis 2024-02-16 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

Gemini est la famille de modèles de Google pour le chat, le texte, le code, les images, l'audio, la vidéo et les intégrations API.

- Application Gemini : chat manuel et tâches du quotidien.
- AI Studio : prototypage de prompts et génération de code.
- API Gemini : intégration backend dans les applications.
- API Live : interfaces vocales et visuelles en streaming.

L'accès à l'application grand public, aux clés API, aux niveaux tarifaires, à l'API Live et aux fonctionnalités macOS est indépendant, et l'API Live reste en Preview. Nous prototypons dans AI Studio, nous figeons un identifiant de modèle stable en production, et nous vérifions son niveau tarifaire et son cycle de vie.

## Ligne de développement {#development-line}

- **2024-02-16 — Google publie une annonce sur le développement du modèle Gemini.** Le 2024-02-16, Google a référencé un article officiel de la rubrique Technology & AI concernant Gemini en tant que modèle de nouvelle génération. Il s'agit d'une annonce de première partie sur le développement du modèle Gemini. Le lien fourni ne suffit pas à établir le périmètre exact des fonctionnalités ou de la disponibilité.
- **2024-12-12 — Une interface Live liée à Gemini apparaît dans Google AI Studio.** Le 2024-12-12, une page Live de Google AI Studio a été référencée pour la ligne Gemini. Cela indique une surface d'interaction en direct liée à Gemini dans l'environnement développeur. L'URL fournie ne permet pas d'établir le modèle, l'API ou le statut de lancement précis.
- **2026-03-03 — Gemini 3.1 Flash-Lite Preview apparaît avec sa documentation tarifaire.** Le 2026-03-03, Google AI Studio a référencé Gemini 3.1 Flash-Lite Preview avec la documentation officielle des tarifs de cette préversion nommée. Il s'agit d'une étape importante en matière de disponibilité et de tarification pour la ligne de modèles destinée aux développeurs Gemini. Les liens fournis ne permettent pas d'établir les quotas, les régions ou le statut de version finale.
- **2026-04-10 — L'application Gemini annonce des capacités de modèles 3D et de graphiques.** Le 2026-04-10, Google a référencé une annonce officielle de l'application Gemini concernant les modèles 3D et les graphiques, ainsi que l'application Gemini elle-même. Cela consigne une évolution de capacités dans la surface applicative Gemini. Les URL seules ne permettent pas d'établir comment la capacité a été implémentée ni quels comptes l'ont reçue.
- **2026-04-16 — Gemini obtient une surface produit spécifique à Mac.** Le 2026-04-16, Google a référencé une page Gemini dédiée à Mac. Cela consigne une extension de la surface de bureau du produit Gemini. L'URL fournie ne permet pas d'établir les versions exactes de macOS prises en charge, le périmètre du déploiement ou l'ensemble des fonctionnalités.
- **2026-08-14 — Google présente Gemini 3.7 Flash pour AI Studio.** Le 2026-08-14, Google a référencé une annonce officielle présentant Gemini 3.7 Flash, ainsi qu'une URL de prompt AI Studio sélectionnant ce modèle. Il s'agit d'une étape importante en matière de sortie de modèle et de disponibilité pour les développeurs. Les liens fournis ne permettent pas d'établir le statut final du modèle, ses limites ou sa disponibilité régionale.

## Ce qui a changé {#what-changed}

- 2024-02-16 : Gemini 1.5 Pro introduit l'architecture MoE, un contexte standard de 128K et une préversion limitée allant jusqu'à 1M de tokens via AI Studio et Vertex AI.
- 2024-12-12 : Gemini 2.0 introduit la Multimodal Live API pour le streaming audio et vidéo en temps réel ; l'URL historique d'AI Studio Live exige désormais une connexion, tandis que l'API Live actuelle fonctionne sur WebSocket avec état et reste en Preview.
- 2026-03-03 : Gemini 3.1 Flash-Lite passe en préversion pour les tâches à haute fréquence, la traduction, la modération et le traitement de données ; Google a ensuite retiré le point de terminaison de préversion.
- 2026-04-10 : L'application Gemini ajoute la génération de simulations interactives et de modèles directement dans le chat, avec des paramètres de visualisation configurables.
- 2026-04-16 : Gemini pour macOS ajoute un accès au bureau avec raccourcis clavier et contexte d'écran ; il nécessite une machine Apple Silicon sous macOS 15+ dans un pays pris en charge.
- 2026-08-14 : Gemini 3.7 Flash, annoncé par Google le 13 août, devient le modèle Flash pour les workflows de code et d'agents.
- Constaté le 2026-09-04 : Gemini 3.8 Flash a été lancé le 2 septembre et constitue le Flash stable actuel ; Gemini 3.7 Flash reste entièrement pris en charge, mais la liste des modèles le marque désormais comme appartenant à la génération précédente.

## Comment l'utiliser {#how-to-use-this}

Suivez Gemini par surface produit au 2026-08-14. Utilisez l'interface Live d'AI Studio pour les workflows en direct (2024-12-12). Chiffrez et évaluez Gemini 3.1 Flash-Lite Preview avant adoption (2026-03-03). Sélectionnez Gemini 3.7 Flash dans AI Studio lorsqu'il est disponible (2026-08-14), et considérez les fonctionnalités de l'application Gemini et de Mac comme des surfaces produit distinctes.

1. Ouvrez l'application Gemini, connectez-vous avec un compte Google et démarrez un chat avec du texte ou des fichiers joints pour des tâches ponctuelles.
  — <https://gemini.google.com/app>
2. Installez Gemini pour macOS sur Mac uniquement si l'appareil est équipé d'Apple Silicon, fonctionne sous macOS Sequoia 15.0+ et si le pays prend en charge l'application Gemini.
  — <https://gemini.google/mac/>
3. Ouvrez Google AI Studio pour prototyper : choisissez une interface de prompt, testez le modèle, ajustez les paramètres et les réglages de sécurité, et ajoutez des outils.
  — <https://ai.google.dev/gemini-api/docs/ai-studio-quickstart>
4. Utilisez Get code après le prototypage, créez ou importez un projet Cloud, et générez une clé d'authentification API pour l'intégration backend.
  — <https://ai.google.dev/gemini-api/docs/api-key>
5. Sélectionnez un point de terminaison stable dans la liste des modèles avant le déploiement ; évaluez gemini-3.8-flash pour les nouvelles tâches de code et d'agents, plutôt que de revenir par défaut à l'ancien point de terminaison 3.7.
  — <https://ai.google.dev/gemini-api/docs/models>
6. Utilisez le chemin distinct de l'API Live sur WebSocket pour un dialogue vocal ou visuel en temps réel ; utilisez des jetons éphémères pour les configurations client-serveur.
  — <https://ai.google.dev/gemini-api/docs/live-api>

## Bonnes pratiques {#best-practices}

- Épinglez les charges de production sur un identifiant de modèle stable précis plutôt que sur les alias latest ou experimental : latest change automatiquement, et les points de terminaison expérimentaux imposent des limites plus strictes sans stabilité contractuelle.
  — <https://ai.google.dev/gemini-api/docs/models>
- Rédigez des instructions courtes et directes pour Gemini 3 ; ne reprenez pas les techniques verbeuses de prompt engineering des modèles antérieurs.
  — <https://ai.google.dev/gemini-api/docs/gemini-3>
- Activez Structured Output pour un JSON Schema complexe plutôt que de vous fier à « reply in JSON » ; ajoutez des exemples cohérents pour un formatage reproductible.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Placez la question après le matériel de référence dans les appels à long contexte, omettez le contexte inutile et mettez en cache les fichiers ou données réutilisés.
  — <https://ai.google.dev/gemini-api/docs/long-context>
- Gardez la clé API hors de Git et du code client ; faites transiter les appels de production web et mobile par un backend et restreignez la clé.
  — <https://ai.google.dev/gemini-api/docs/api-key>
- Consultez le tableau tarifaire avant d'estimer les coûts : les offres gratuites et payantes diffèrent par leurs limites, leurs fonctionnalités et le traitement des contenus, si bien que les tarifs annoncés au lancement ne constituent pas une estimation valable.
  — <https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview>

## Remplacé par ceci {#superseded-by-this}

- 2024-02-16 — L'accès anticipé à Gemini 1.5 Pro avec un contexte de base de 128K et une préversion limitée à 1M est un contexte historique, et non une recommandation actuelle de sélection de modèle.
- 2026-03-03 — Le point de terminaison `gemini-3.1-flash-lite-preview` a été arrêté le 2026-05-25 ; son remplaçant direct était `gemini-3.1-flash-lite`. Ce remplaçant affiche désormais une date d'arrêt au 2027-05-07, avec `gemini-3.5-flash-lite` comme successeur recommandé suivant.
- Constaté le 2026-09-04 — Décrire Gemini 3.7 Flash comme le Flash le plus récent est obsolète : `gemini-3.8-flash` a été publié le 2026-09-02. `gemini-3.7-flash` reste entièrement pris en charge, mais il s'agit désormais de l'option stable de la génération précédente.

## Toujours inconnu {#still-unknown}

- Gemini couvre plusieurs surfaces produit distinctes : application grand public, application macOS, AI Studio, API Gemini et API Live. L'accès à l'une ne confirme ni les quotas, ni les niveaux tarifaires, ni les fonctionnalités d'une autre.
- L'URL historique d'AI Studio Live redirige vers une invite de connexion. Nous ne pouvons pas vérifier l'interface ou les paramètres exacts de décembre 2024 sans session active ; une annonce officielle du 11 décembre 2024 et la documentation actuelle confirment le lancement séparément.
- La page produit Gemini pour macOS indique les prérequis et les limites, mais ne donne aucune date de lancement ; elle ne permet pas de vérifier indépendamment la date du 2026-04-16.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#sundar-note | Notre modèle de nouvelle génération : Gemini 1.5 | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/ | Google présente Gemini 2.0 : un nouveau modèle d'IA pour l'ère agentique | 2026-09-04 |
| https://aistudio.google.com/live | Connexion - Comptes Google | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview | Цены на API Gemini Developer | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ | Gemini 3.1 Flash-Lite : conçu pour l'intelligence à grande échelle | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-app/3d-models-charts/ | L'application Gemini peut désormais générer des simulations et des modèles interactifs. | 2026-09-04 |
| https://gemini.google.com/app | Google Gemini | 2026-09-04 |
| https://gemini.google/mac/ | Gemini pour macOS : assistant IA natif et automatisation Mac | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ | Présentation de Gemini 3.7 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models | Modèles | API Gemini | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/deprecations?hl=en | Dépréciations de Gemini | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/latest-model | Nouveautés de Gemini 3.8 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/ai-studio-quickstart | Démarrage rapide de Google AI Studio | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/api-key | Utiliser les clés API Gemini | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Stratégies de conception de prompts | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/long-context | Contexte long | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/gemini-3 | Guide développeur Gemini 3 | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/live-api | Présentation de l'API Gemini Live | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:gemini`, fil `gemini-development`, 6 événements datés du 2024-02-16 au 2026-08-14.
- **Note pratique :** Au 2026-08-14, les praticiens doivent suivre Gemini par surface produit : utiliser l'interface Live d'AI Studio pour les workflows en direct (2024-12-12), évaluer et chiffrer Gemini 3.1 Flash-Lite Preview avant adoption (2026-03-03), et sélectionner Gemini 3.7 Flash dans AI Studio lorsqu'il est disponible (2026-08-14), tout en considérant les fonctionnalités de l'application Gemini et de Mac comme des surfaces produit distinctes.
- **Confiance :** élevée. Les mentions « remplacé par » datées font foi pour ce qui est obsolète.
