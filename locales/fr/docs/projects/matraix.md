---
title: "MatrAIx"
category: projects
date: 2026-08-11
tags: [matraix, persona-8b-public-documentation, project]
aliases: ["MatrAIx"]
level: 2
source_sha256: f4527e46e74cd04f6722540083af2ec2fa4e44d324d176dbb438ff6d5e7a4628
translation: machine
translated_at: '2026-10-24'
---
# MatrAIx {#matraix}

**Ligne de développement :** `project:matraix` · fil `persona-8b-public-documentation`  
**Dernier événement :** 2026-08-11 · 1 événement daté depuis le 2026-08-11 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

MatrAIx exécute des agents LLM dotés de profils utilisateurs sur des tâches de type Survey, AI Chatbot, Web et App.

- 1 290 attributs catégoriels de persona.
- Persona 1M public, avec 599 847 enregistrements ancrés et 400 000 enregistrements synthétiques.
- 1 010 tâches couvrant plus de 25 domaines.

Nous l'utilisons pour générer et soumettre à des tests de charge des hypothèses, et non pour remplacer des études auprès de personnes réelles. Il convient aux évaluations reproductibles de produits et d'agents, à condition que les résultats ne soient pas considérés comme une validation humaine.

## Ligne de développement {#development-line}

- **2026-08-11 — MatrAIx Persona 8B a été publiquement mentionné avec un guide de démarrage rapide du Playground visuel.** Le périmètre pratique couvre Survey, AI Chatbot, Web et OS-app. Les exécutions réelles nécessitent des clés API de fournisseurs de modèles. Web et OS-app nécessitent Docker.

## Ce qui a changé {#what-changed}

2026-08-04 — MatrAIx a publié son rapport technique. Persona 8B annonce 8,3 milliards d'enregistrements, un Playground avec quatre environnements et 18 189 trajectoires d'évaluation terminées. 2026-08-11 — MatrAIx était disponible sous forme de Playground ouvert et de bibliothèque de tâches. Le périmètre pratique couvre Survey, AI Chatbot, Web et OS-app. Les exécutions réelles nécessitent des clés API de fournisseurs de modèles, et Docker est requis pour Web et OS-app. Remarque sur l'étape du 2026-08-11 : la version initiale est MatrAIx-Persona-8B, et non un modèle d'inférence Persona-8B autonome. Son jeu de données public est Persona 1M, et non les 8,3 milliards de personas annoncés. Nouvelles étapes datées : le 2026-07-31, ouverture du Playground et de la bibliothèque de tâches ; le 2026-08-01, publication de Persona 1M ; le 2026-08-04, publication du rapport sur arXiv.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-11, les praticiens doivent commencer l'évaluation ou la prise en main de MatrAIx Persona 8B à partir de son dépôt et du guide de démarrage rapide du Playground visuel.

1. Installez Python 3.12, uv et Docker. Sous Windows, utilisez WSL2, car PowerShell et cmd natifs ne prennent pas en charge les vérificateurs de tâches.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
2. Clonez le dépôt, créez un environnement uv et installez le paquet principal avec Playground, Rewardkit et Harbor-LangSmith.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
3. Vérifiez l'environnement avec un smoke test Survey et Chat sans Docker, puis exécutez le smoke test Harbor pour Web et OS-app avec Docker.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
4. Pour les évaluations réelles, définissez une clé API de fournisseur compatible, choisissez une tâche et un persona, générez une recette de job et exécutez-la avec `matraix run`. Récupérez les résultats avec `matraix results`.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B/blob/main/docs/quickstart.md#10-playground--play-tasks-visually>
5. Pour une cohorte plutôt qu'un smoke test, téléchargez Persona 1M et définissez-le comme jeu de données dans le Playground ou la CLI.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>

## Bonnes pratiques {#best-practices}

- Commencez par les smoke tests dev-sample pour vérifier la configuration, et non pour tirer des conclusions sur les populations d'utilisateurs.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Pour la recherche, utilisez Persona 1M plutôt que l'échantillon local d'environ 200 personas. Figez la recette, le modèle et la cohorte afin que l'exécution soit reproductible.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Considérez la simulation comme une génération d'hypothèses et un test de charge, puis confirmez les décisions produit importantes avec des données d'utilisateurs réels.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Ne planifiez pas d'évaluations Web et OS-app sans Docker. Sous Windows, conservez le dépôt sur le système de fichiers WSL2 plutôt que dans /mnt/c.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Les sources officielles ne montrent aucune version distincte datée exactement du 2026-08-11. Cette étape reflète l'état de la documentation et du dépôt disponible à cette date, et non une version formelle.
- Aucune validation pratique indépendante ne confirme que les résultats de simulation prédisent le comportement des utilisateurs dans un produit donné.
- Le dépôt évolue sans GitHub Releases. Aucune version publiée ne garantit la compatibilité d'un commit donné avec les futures API des fournisseurs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://matraix.ai/ | MatrAIx — Simuler avant la réalité | 2026-09-05 |
| https://github.com/MatrAIx-ai/MatrAIx-Persona-8B | Dépôt MatrAIx-Persona-8B | 2026-09-05 |
| https://github.com/MatrAIx-ai/MatrAIx-Persona-8B/blob/main/docs/quickstart.md#10-playground--play-tasks-visually | Guide de démarrage rapide MatrAIx | 2026-09-05 |
| https://arxiv.org/abs/2608.04205 | MatrAIx : simuler le monde avec 8,3 milliards d'agents persona | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:matraix`, fil `persona-8b-public-documentation`, 1 événement daté du 2026-08-11 au 2026-08-11.
- **Note pratique :** Au 2026-08-11, les praticiens doivent commencer l'évaluation ou la prise en main de MatrAIx Persona 8B à partir de son dépôt et du guide de démarrage rapide du Playground visuel.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
