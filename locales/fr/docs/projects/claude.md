---
title: "Claude"
category: projects
date: 2023-11-22
tags: [claude, claude-product-development, project]
aliases: ["Claude", "Claude 2.1"]
level: 3
source_sha256: a8a04f472bec5ade180774636412dabe07dbd67f03a8bc9e6c372eed999d5d8f
translation: machine
translated_at: '2026-10-24'
---
# Claude {#claude}

**Ligne de développement :** `project:claude` · fil `claude-product-development`  
**Dernier événement :** 2023-11-22 · 2 événements datés depuis 2023-05-12 · **Consulté le :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Claude est la famille de modèles d'Anthropic destinée aux utilisateurs de chat, aux développeurs d'applications et aux équipes logicielles.

- Texte et images : accepte du texte et des images, et renvoie du texte.
- Capacités : prend en charge les tâches multilingues, la vision, l'utilisation d'outils et les flux de travail à long contexte.
- Surfaces : fonctionne via le chat, l'API Messages et Claude Code pour le travail sur les dépôts.

## Ligne de développement {#development-line}

- **2023-05-12 — Claude étend ses fenêtres de contexte à 100K tokens.** Claude est passé de 9K à 100K tokens dans la version 100K-context afin que les prompts puissent contenir des documents entiers et des bases de code complètes. L'article officiel est daté du 2023-05-11.
- **2023-11-22 — Claude 2.1 introduit une fenêtre de contexte de 200K tokens.** Claude 2.1 porte la limite à 200K tokens, ajoute les system prompts et l'utilisation d'outils en bêta, et réduit les fausses affirmations. L'article officiel est daté du 2023-11-21.

## Ce qui a changé {#what-changed}

Claude — la ligne de développement datée :

- 2023-05-12 : La version 100K-context fait passer Claude de 9K à 100K tokens afin que les prompts puissent contenir des documents et des bases de code entiers. L'article officiel est daté du 2023-05-11.
- 2023-11-22 : Claude 2.1 porte la limite à 200K tokens, ajoute les system prompts et l'utilisation d'outils en bêta, et réduit les taux de fausses affirmations. L'article officiel est daté du 2023-11-21.
- 2026-09-04 (constaté aujourd'hui) : La documentation actuelle décrit une famille de modèles avec entrée texte et images, utilisation d'outils, limites propres à chaque modèle, et une plage de contexte de 200K à 1M tokens.

## Mode d'emploi {#how-to-use-this}

À partir du 2023-05-12, les praticiens pouvaient envisager Claude pour les flux de travail nécessitant jusqu'à 100K tokens de contexte. À partir du 2023-11-22, Claude 2.1 a étendu cette enveloppe de planification à 200K tokens.

1. Choisissez la surface : utilisez Claude.ai pour le chat, la Console et l'API pour une application, ou Claude Code pour une tâche sur un dépôt.
  — <https://docs.anthropic.com/en/docs/about-claude/models/overview>
2. Pour l'intégration via l'API, créez un compte Claude Console et une clé API, exportez-la sous le nom ANTHROPIC_API_KEY, puis installez le SDK pris en charge.
  — <https://docs.anthropic.com/en/docs/get-started>
3. Choisissez un modèle actuel en fonction des capacités, de la latence, du coût, de l'effort et de l'évaluation de votre tâche avant tout déploiement en production.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
4. Effectuez un appel à l'API Messages avec le modèle sélectionné, une limite max_tokens et le message utilisateur ; ajoutez des outils, des fichiers ou des fonctionnalités de gestion du contexte uniquement si la tâche le nécessite.
  — <https://docs.anthropic.com/en/docs/get-started>
5. Pour le travail sur une base de code, installez Claude Code sur une surface prise en charge, lancez-le dans le répertoire du projet et examinez les actions de fichiers et de commandes qu'il exécute.
  — <https://code.claude.com/docs/en/overview>

## Bonnes pratiques {#best-practices}

- Définissez des critères de réussite précis et mesurables ainsi qu'un jeu d'évaluation avant de modifier les prompts ou les modèles.
  — <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- Énoncez directement la tâche, le contexte, les contraintes, le format de sortie et les étapes ordonnées. Ajoutez des exemples pertinents lorsque la cohérence de la sortie est importante.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Pour les entrées de plus de 20K tokens, placez les documents longs avant la requête, structurez clairement les documents multiples et demandez des citations justificatives avant la synthèse.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Considérez le choix du modèle et l'effort comme des leviers de performance au même titre que le prompting ; utilisez les évaluations pour arbitrer entre capacité, latence et coût.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Figez les identifiants de modèle pour la reproductibilité et suivez leur cycle de vie. Les identifiants sans date à partir de la génération 4.6 sont des instantanés figés, et non des alias mobiles.
  — <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>

## Ce qui est rendu obsolète {#superseded-by-this}

- 2023-05-12 : Considérer 100K tokens comme le plafond opérationnel de contexte de Claude est obsolète ; les modèles actuels vont de 200K à 1M tokens en entrée.
- 2023-11-22 : Appliquer les recommandations relatives à Claude 2.1 est obsolète ; le modèle d'API claude-2.1 a été retiré le 2025-07-21.
- 2023-11-22 : Considérer l'utilisation d'outils comme une capacité réservée à la bêta est obsolète ; la documentation des modèles actuels la répertorie comme capacité prise en charge.
- Les hypothèses sur les alias antérieurs à la 4.6 sont obsolètes pour les identifiants de modèle actuels sans date : chaque identifiant actuel désigne un instantané figé du modèle.

## Points restants inconnus {#still-unknown}

- Les deux événements datés ne constituent pas une chronologie complète des versions entre 2023 et aujourd'hui ; la documentation actuelle n'est utilisée que comme instantané en direct.
- Les dates d'événements fournies sont décalées d'un jour par rapport aux dates des articles officiels : 2023-05-12 contre 2023-05-11, et 2023-11-22 contre 2023-11-21.
- La disponibilité selon l'offre, la région, la plateforme et la tarification peuvent varier selon le compte et évoluer après cet instantané ; vérifiez-les dans la Console avant tout déploiement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.anthropic.com/index/100k-context-windows | Introducing 100K context windows | Anthropic | 2026-09-04 |
| https://www.anthropic.com/index/claude-2-1 | Introducing Claude 2.1 | Anthropic | 2026-09-04 |
| https://docs.anthropic.com/en/docs/about-claude/models/overview | Models overview | Claude Platform Docs | 2026-09-04 |
| https://docs.anthropic.com/en/docs/get-started | Get started with Claude | Claude Platform Docs | 2026-09-04 |
| https://code.claude.com/docs/en/overview | Overview | Claude Code Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Choosing the right model | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Define success criteria and build evaluations | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting best practices | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | Model IDs and versioning | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations | Claude Platform Docs | 2026-09-04 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:claude`, fil `claude-product-development`, 2 événements datés du 2023-05-12 au 2023-11-22.
- **Note pratique :** À partir du 2023-05-12, les praticiens pouvaient envisager Claude pour les flux de travail nécessitant jusqu'à 100K tokens de contexte ; à partir du 2023-11-22, Claude 2.1 a étendu cette enveloppe de planification à 200K tokens.
- **Confiance :** élevée. Les mises à jour datées ci-dessus font foi pour ce qui est obsolète.
