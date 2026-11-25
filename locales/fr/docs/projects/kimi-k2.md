---
title: "Kimi K2"
category: projects
date: 2025-07-13
tags: [kimi, kimi-k2, kimi-k2-development, project]
aliases: ["Kimi", "Kimi K2"]
level: 3
source_sha256: 68446357ebcae07371922b1587f362c38ace0dbf3bfe64aa92379cfd286b9c1a
translation: machine
translated_at: '2026-10-24'
---
# Kimi K2 {#kimi-k2}

**Ligne de développement :** `project:kimi-k2` · fil `kimi-k2-development`  
**Dernier événement :** 2025-07-13 · 1 événement daté depuis le 2025-07-13 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Kimi K2 est une famille de modèles de langage MoE à poids ouverts, destinée aux développeurs qui ont besoin d'un modèle auto-hébergé pour le texte et l'utilisation d'outils, plutôt que de l'API hébergée actuelle de Kimi.

- Kimi-K2-Base pour la recherche et le fine-tuning.
- Kimi-K2-Instruct pour le chat et les boucles d'agents.
- Chat compatible OpenAI et appel d'outils en local ; l'ancienne API hébergée proposait également une compatibilité avec Anthropic.

## Ligne de développement {#development-line}

- **2025-07-13 — Références de disponibilité publique de Kimi K2.** Le 2025-07-13, des liens officiels vers le projet, le code source, l'éditeur du modèle, le chat web et l'accès mobile enregistraient Kimi K2. Ces références datées marquent une étape de disponibilité publique du projet. La formulation exacte de la publication et les détails de version restent à vérifier à partir des sources de recherche.

## Ce qui a changé {#what-changed}

- 2025-07-13 — Kimi K2 Base et Instruct étaient déjà publics. Les enregistrements officiels datent le modèle initial et la publication de l'API kimi-k2-0711-preview au 2025-07-11 ; le 13 juillet ne correspond donc pas à une version distincte de K2.
- 2025-08-01 — kimi-k2-turbo-preview a ajouté une option hébergée à haut débit, avec une promotion de lancement de 50 % limitée dans le temps.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-07-13, évaluez Kimi K2 à partir des références officielles du projet et des sources plutôt que de résumés tiers. Vérifiez séparément la disponibilité du modèle sur la plateforme développeur avant d'intégrer une API.

1. Choisissez d'abord la voie : conservez K2 uniquement pour un déploiement auto-hébergé existant ou reproductible. Pour une nouvelle intégration hébergée, choisissez un modèle Kimi actuellement listé, car tous les identifiants d'API kimi-k2 sont abandonnés.
  — <https://platform.kimi.ai/docs/models>
2. Pour le chat local ou les agents, partez du point de contrôle officiel Kimi-K2-Instruct plutôt que de Base. Base est le point de contrôle de fondation pour la recherche et le post-entraînement personnalisé.
  — <https://github.com/MoonshotAI/Kimi-K2>
3. Servez les poids K2 avec l'un des moteurs officiellement recommandés : vLLM, SGLang, KTransformers ou TensorRT-LLM.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
4. Utilisez l'interface locale de complétion de chat et lancez Kimi-K2-Instruct avec une température de 0,6. Conservez un prompt système lorsqu'aucune instruction particulière n'est nécessaire.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
5. Pour une boucle d'outils, envoyez les schémas des outils disponibles, exécutez l'appel renvoyé dans votre application, ajoutez son résultat, puis continuez jusqu'à ce que la complétion ne demande plus d'outils.
  — <https://github.com/MoonshotAI/Kimi-K2>
6. Pour un nouvel appel à l'API Kimi, créez une clé API, utilisez l'identifiant de modèle actuel de la liste des modèles, et appelez POST /v1/chat/completions sur https://api.moonshot.ai/v1.
  — <https://platform.kimi.ai/docs/api/chat>

## Bonnes pratiques {#best-practices}

- Indiquez explicitement la tâche, le contexte pertinent, le format de sortie et la longueur cible. Le guide des prompts prévient que le modèle ne peut pas deviner les exigences non énoncées.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Séparez les documents fournis à l'aide de délimiteurs et détaillez les étapes ordonnées pour les travaux en plusieurs phases.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Utilisez des exemples représentatifs lorsque le style ou le schéma de sortie compte. Exigez que les réponses restent dans le matériau de référence fourni lorsqu'un ancrage est nécessaire.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Ne traitez pas l'appel d'outils comme une requête unique : conservez le message d'appel d'outil de l'assistant renvoyé et ajoutez chaque résultat d'outil avant de demander au modèle de continuer.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
- Ne codez pas en dur les anciens noms de préversion de K2 pour un usage hébergé. Ils sont abandonnés et non pris en charge ; migrez et vérifiez à nouveau la liste actuelle des modèles.
  — <https://platform.kimi.ai/docs/models>
- Dimensionnez le trafic API au niveau de l'utilisateur, et non de la clé : la concurrence, les RPM, TPM et TPD sont partagés entre les modèles.
  — <https://platform.moonshot.ai/docs/introduction#text-generation-model>

## Remplacé par {#superseded-by-this}

- 2025-09-05 — kimi-k2-0711-preview comme modèle K2 hébergé actuel pour les nouvelles intégrations ; remplacé par kimi-k2-0905-preview.
- 2026-05-25 — tout identifiant kimi-k2 de type preview, Turbo ou Thinking comme cible d'API hébergée prise en charge ; la série K2 a été abandonnée.
- 2026-08-31 — kimi-k2.5 comme solution de repli d'API prise en charge pour les intégrations de l'ère K2 ; il a été retiré.

## Inconnues restantes {#still-unknown}

- Les liens sources établissent les artefacts publics et les publications de K2, mais pas les affirmations exactes des messages du 2025-07-13 et du 2025-08-01, dont le texte n'est pas disponible.
- Les dates de première source sont contradictoires. Le journal des modifications de la plateforme, l'annonce 0905 et le catalogue de recherche placent la publication initiale de K2 au 2025-07-11, alors que l'aperçu actuel de Kimi Agent indique le 2025-09-05. Cette dernière date peut désigner la mise à jour 0905, mais elle n'y est pas explicitement corrigée.
- Les liens de l'application Kimi de juillet 2025 et la publication du modèle K2 relèvent de surfaces produit liées, mais ils ne prouvent pas quelle version du modèle alimentait chaque client de l'application ce jour-là.
- Les sources officielles retirent K2 de l'API hébergée, mais n'énoncent aucune politique de maintenance ou de sécurité après retrait pour les poids K2 auto-hébergés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/MoonshotAI/Kimi-K2 | Kimi K2 est la série de grands modèles de langage développée par l'équipe Moonshot AI | 2026-09-04 |
| https://moonshotai.github.io/Kimi-K2/ | Kimi K2 : Open Agentic Intelligence | 2026-09-04 |
| https://huggingface.co/moonshotai/Kimi-K2-Instruct | moonshotai/Kimi-K2-Instruct | 2026-09-04 |
| https://platform.moonshot.ai/docs/introduction#text-generation-model | Main Concepts - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/models | Model List - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/api/chat | Chat Completions API - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/guide/prompt-best-practice | Best Practices for Prompts - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/blog/posts/changelog | Kimi Open Platform: New Feature Release Log | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2 | Kimi K2 : Open Agentic Intelligence | 2026-09-04 |
| https://arxiv.org/abs/2507.20534 | Kimi K2 : Open Agentic Intelligence | 2026-09-04 |
| https://platform.kimi.com/blog/posts/kimi-k2-0905 | Kimi K2 模型更新，带来更强的代码能力、更快的 API | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-thinking | Introducing Kimi K2 Thinking | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-5 | Kimi K2.5 : Visual Agentic Intelligence | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-6 | Kimi K2.6 : Advancing Open-Source Coding | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k3 | Kimi K3 : Open Frontier Intelligence | 2026-09-04 |
| https://www.kimi.com/en/blog/ | Kimi Research Blog | Moonshot AI | 2026-09-04 |
| https://github.com/MoonshotAI/kimi-help-center/blob/master/en-US/agent/overview.md | Kimi Agent overview | 2026-09-04 |

## Brief de l'agent {#agent-brief}

- **Sujet :** `project:kimi-k2`, fil `kimi-k2-development`, 1 événement daté du 2025-07-13 au 2025-07-13.
- **Note pratique :** À partir du 2025-07-13, évaluez Kimi K2 à partir des références officielles du projet et des sources plutôt que de résumés tiers. Vérifiez séparément la disponibilité du modèle sur la plateforme développeur avant d'intégrer une API.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
