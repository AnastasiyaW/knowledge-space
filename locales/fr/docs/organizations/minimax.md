---
title: "MiniMax"
category: organizations
date: 2025-12-27
tags: [minimax, minimax-models-and-products, minimax_models, organization]
aliases: ["MiniMax"]
level: 3
source_sha256: fef8ae2b00f124b6f62e25f22198d5a3b6fbdecbb197aed2e13d683c6c1d8a32
translation: machine
translated_at: '2026-10-24'
---
# MiniMax {#minimax}

**Ligne de développement :** `organization:minimax` · fil `minimax-models-and-products`  
**Dernier événement :** 2025-12-27 · 3 événements datés depuis 2025-06-18 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

MiniMax fournit des modèles et services d'IA. Les développeurs disposent d'une API compatible avec le SDK Anthropic, ainsi que de services vidéo et vocaux ; les créateurs disposent des produits Hailuo et Audio, distincts.

- M3 : langage, utilisation d'outils, entrée image/vidéo et fenêtre de contexte de 1M de tokens.
- H3 : génération de vidéo à partir de texte, d'image, de première/dernière image et de références multimodales.
- Speech 2.8 : synthèse, clonage et conception de voix.

## Ligne de développement {#development-line}

- **2025-06-18 — MiniMax a rendu visibles les ressources du modèle MiniMax-M1.** Le 2025-06-18, MiniMax a publié un lien vers une collection Hugging Face pour MiniMax-M1 ainsi que vers un dépôt GitHub pour ce modèle. Le même ensemble de liens datés pointait vers Hailuo Create et MiniMax Agent, plaçant le modèle à côté des interfaces vidéo et agent.
- **2025-06-22 — MiniMax a publiquement rendu visible son produit Audio.** La parole reste une ligne d'API distincte, avec synthèse, clonage et conception de voix ; l'accès à la musique a sensiblement changé.
- **2025-12-27 — MiniMax a rendu visible M2.1 via des voies d'accès hébergées et locales.** Le 2025-12-27, MiniMax a publié un lien vers sa page d'actualités sur MiniMax-M2.1 et vers son dépôt de modèle Hugging Face. L'ensemble de ressources daté pointait également vers MiniMax Agent, une référence d'API texte compatible Anthropic, OpenRouter et Ollama, et listait plusieurs voies d'accès pour M2.1.

## Ce qui a changé {#what-changed}

2024-10-10 — Un événement MiniMax n'a conservé ni texte ni URL ; il ne permet donc aucune affirmation historique fondée sur une source. La référence primaire la plus proche de MiniMax est Video-01, publié le 2024-08-31, avec génération de texte en vidéo et d'image en vidéo en 720p/25 ips, pour une durée allant jusqu'à six secondes. Il s'agit d'un contexte, et non d'une confirmation du changement du 10 octobre.

2025-06-18 — MiniMax M1 et Hailuo 02 sont entrés dans le registre. M1 était un modèle de raisonnement à attention hybride et à poids ouverts, avec 456 Md de paramètres au total, 45,9 Md de paramètres actifs et un contexte de 1M. Hailuo 02 ajoutait des options vidéo 1080p natives.

2025-06-20 — Hailuo Video Agent est entré en bêta avec des modèles vidéo prédéfinis comme Étape 1. Les étapes autonomes ultérieures relevaient d'une feuille de route, et non de capacités vérifiées.

2025-06-22 — Un point d'accès MiniMax Audio est apparu, mais la page ne mentionne aucun détail de publication daté. La parole reste une ligne d'API distincte, avec synthèse, clonage et conception de voix ; l'accès à la musique a sensiblement changé.

2025-12-27 — M2.1 est entré dans le registre comme modèle M2 à poids ouverts, orienté agents, destiné au codage multilingue, à l'utilisation d'outils, au suivi d'instructions et aux tâches de longue durée. La note de version de MiniMax est datée du 2025-12-23, tandis que ses notes de version des modèles indiquent le 2025-12-22.

Constaté aujourd'hui — M3 a été publié le 2026-06-01 comme modèle de langage actuel à contexte de 1M. H3 a été publié en open source le 2026-08-03 comme ligne vidéo multimodale. L'accès à l'API Music a changé le 2026-08-20 pour les nouveaux utilisateurs.

## Mode d'emploi {#how-to-use-this}

Au 2025-12-27, évaluez les modèles MiniMax selon chaque voie listée — MiniMax Agent, l'API texte, OpenRouter ou Ollama — plutôt que de supposer qu'une seule interface couvre tous les produits.

1. Choisissez d'abord l'interface actuelle : M3 pour le langage, le codage, l'utilisation d'outils ou les usages API multimodaux ; H3 pour la vidéo ; Speech 2.8 pour la voix. Ne partez pas des noms historiques M2.1 ou Hailuo.
  — <https://platform.minimax.io/docs/guides/models-intro>
2. Créez une clé API à la consommation sur la plateforme MiniMax pour accéder aux modèles de langage, vidéo, vocaux et d'image.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
3. Pour les intégrations de langage, définissez `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` dans le SDK Anthropic, utilisez la clé API MiniMax et appelez `MiniMax-M3`.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
4. Pour l'appel d'outils, ajoutez à l'historique la réponse complète de l'assistant — blocs de réflexion, de texte et d'utilisation d'outils — avant d'envoyer les résultats des outils et le tour suivant.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
5. Pour la vidéo H3, créez une tâche asynchrone, conservez le `task_id`, interrogez le statut et récupérez l'URL de sortie une fois la tâche réussie. Choisissez les entrées et la durée dans la plage de 4 à 15 secondes.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
6. Pour la parole, utilisez le T2A synchrone pour un audio court et interactif, et la synthèse asynchrone pour les textes longs. Ne démarrez pas une nouvelle intégration de l'API Music ; utilisez plutôt MiniMax Audio ou le modèle ouvert Music 3.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Bonnes pratiques {#best-practices}

- Considérez la compatibilité Anthropic comme un sous-ensemble documenté : l'API ignore `top_k`, les séquences d'arrêt, les serveurs MCP, la gestion du contexte et les conteneurs, au lieu de les émuler.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Utilisez la réflexion adaptative de M3 pour les raisonnements complexes, et désactivez-la pour une latence faible ; conservez les blocs de réflexion inchangés entre les tours d'utilisation d'outils.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Utilisez M3 — et non M2.x — pour les entrées image ou vidéo, et estimez le nombre de tokens avant d'envoyer de grosses requêtes multimodales.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Considérez M2.1, Hailuo 02/2.3 et les anciens modèles Speech comme héritage, nécessitant une décision explicite de compatibilité ou de migration.
  — <https://platform.minimax.io/docs/guides/models-intro>
- Traitez la génération vidéo comme un flux de travail par tâches plutôt que comme un appel synchrone : conservez les identifiants de tâche, interrogez le statut et gérez proprement l'annulation ou la suppression.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
- Si un déploiement nécessite les poids locaux de M2.1, servez-les via SGLang ou vLLM et examinez la licence MIT modifiée avant toute mise en production.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M2.1>
- Vérifiez l'éligibilité du compte avant de construire des flux de travail musicaux : les nouveaux utilisateurs ne peuvent pas accéder aux API Music payantes, et les points d'accès gratuits sont abandonnés.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Remplacé par {#superseded-by-this}

- 2024-08-31 / 2024-10-10 — Les limites de Video-01 (720p, 25 ips, jusqu'à six secondes) sont obsolètes. H3 couvre les entrées multimodales, des sorties de 4 à 15 secondes, 24 ips et une résolution allant jusqu'à 2K.
- 2025-06-18 — M1 comme modèle hébergé par défaut à contexte de 1M est historique. MiniMax présente M3 comme modèle de langage actuel à contexte de 1M ; M1 relève de l'archive ou de poids ouverts à auto-hébergement.
- 2025-06-20 — L'Étape 1 en bêta de Hailuo Video Agent et la feuille de route des Étapes 2 et 3 sont historiques. Vérifiez les fonctionnalités actuelles par rapport à H3 et à la documentation API, plutôt que de supposer que la feuille de route a été livrée.
- 2025-12-27 — Choisir M2.1 comme modèle phare est obsolète. Il reste compatible avec l'API et téléchargeable, mais MiniMax le classe parmi les modèles hérités.
- 2025-06-22 — Démarrer un flux de travail avec l'API Music à partir des anciennes indications de MiniMax Audio est obsolète : à partir du 2026-08-20, les API Music payantes sont fermées aux nouveaux utilisateurs et les points d'accès gratuits sont abandonnés.

## Toujours inconnu {#still-unknown}

- L'événement du 2024-10-10 n'a conservé ni lien ni texte. La page Video-01 du 2024-08-31 constitue un contexte, et non une preuve du changement d'octobre.
- Les liens `https://hailuoai.video/create`, `https://agent.minimax.io/` et `https://www.minimax.io/audio` ont renvoyé des coquilles JavaScript lors de la récupération, ce qui laisse non vérifiés l'expérience utilisateur grand public actuelle et la disponibilité.
- La publication X du 2025-06-20 n'était pas lisible. Une annonce officielle d'Hailuo Video Agent existe pour le même jour, mais la correspondance exacte n'est pas vérifiée.
- La date de publication de M2.1 varie selon les sources : 2025-12-27 dans l'événement daté, 2025-12-23 dans l'article de publication et 2025-12-22 dans les notes de version de l'API.
- `minimax` et `minimax_models` mêlent histoire de l'entreprise et lignées de modèles. Ces deux éléments sont liés, mais ne forment pas un cycle de vie unique pour un seul produit.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.minimax.io/news/video-01 | MiniMax publie officiellement le modèle de génération vidéo Video-01 | 2026-09-04 |
| https://huggingface.co/collections/MiniMaxAI/minimax-m1-68502ad9634ec0eeac8cf094 | MiniMax-M1 - une collection de MiniMaxAI | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-M1 | MiniMax-AI/MiniMax-M1 | 2026-09-04 |
| https://www.minimax.io/news/minimax-hailuo-02 | MiniMax Hailuo 02, qualité de premier plan, rapport coût-efficacité record | 2026-09-04 |
| https://www.minimax.io/news/video-agent | Présentation de Hailuo Video Agent en bêta, création vidéo sans intervention | 2026-09-04 |
| https://www.minimax.io/news/minimax-m21 | MiniMax M2.1 : programmation multilingue nettement améliorée, conçue pour des tâches complexes du monde réel | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Modèles - notes de version de la documentation de l'API MiniMax | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-M2.1 | MiniMaxAI/MiniMax-M2.1 | 2026-09-04 |
| https://platform.minimax.io/docs/guides/models-intro | Modèles - documentation de l'API MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/api-overview | Vue d'ensemble de l'API - documentation de l'API MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/text-anthropic-api | SDK Anthropic - documentation de l'API MiniMax | 2026-09-04 |
| https://www.minimax.io/models/text/m3 | MiniMax M3 - frontière du codage et des agents, contexte de 1M, multimodal | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Intelligence générale ouverte : MiniMax H3 est désormais open source | 2026-09-04 |

## Fiche pour agents {#agent-brief}

- **Sujet :** `organization:minimax`, fil `minimax-models-and-products`, 3 événements datés du 2025-06-18 au 2025-12-27.
- **Note pratique :** Au 2025-12-27, les praticiens doivent évaluer l'usage des modèles MiniMax selon la voie explicitement listée — MiniMax Agent, l'API texte, OpenRouter ou Ollama — plutôt que de supposer qu'une seule interface couvre tous les produits MiniMax.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
