---
title: "Mistral Small 4 — Mistral Small"
category: projects
date: 2026-03-17
tags: [mistral-small, mistral-small-4, project]
aliases: ["Mistral Small 4"]
level: 2
source_sha256: fc77fefb86f9dd93541b002b7b0cdf46135bfeafd755ba14b6ad07d97066b7f1
translation: machine
translated_at: '2026-10-24'
---
# Mistral Small 4 — Mistral Small {#mistral-small-4-mistral-small}

**Ligne de développement :** `project:mistral-small-4` · fil `mistral-small`  
**Dernier événement :** 2026-03-17 · 1 événement daté depuis le 2026-03-17 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Mistral Small 4 combine le suivi d'instructions, un raisonnement configurable, l'appel d'outils, une sortie JSON et une entrée texte plus image avec une sortie texte. Il compte 119 Md de paramètres au total, 6,5 Md actifs par jeton, et une fenêtre de contexte de 256k jetons. Verdict : à utiliser lorsque la consolidation prime sur une infrastructure minimale ; l'éditeur indique, pour un auto-hébergement, un minimum de quatre HGX H100, deux HGX H200 ou un DGX B200.

## Ligne de développement {#development-line}

- **2026-03-17 — Le dépôt Mistral Small 4 119B 2603 Eagle a été lié sur Hugging Face.** Le 2026-03-17, l'enregistrement a noté un lien vers le dépôt Hugging Face de Mistral Small 4 119B 2603 Eagle. Le nom du dépôt identifie un artefact de modèle Mistral Small 4 et ses étiquettes de variante 119B, 2603 et Eagle. Ce lien daté n'établit à lui seul ni le statut de publication, ni les capacités, ni la licence, ni les conditions d'accès.

## Ce qui a changé {#what-changed}

2026-03-17 — Le dépôt Mistral-Small-4-119B-2603 Eagle a rendu disponible la tête de décodage spéculatif entraînée pour le modèle de base 119B A6B. 2026-03-16 — Mistral a annoncé le modèle de base Mistral Small 4 : une voie de succession unifiée pour les charges de travail d'instructions, de raisonnement, multimodales et de codage agentique, publié sous licence Apache 2.0.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-17, les praticiens doivent utiliser le dépôt Hugging Face lié comme artefact précis à examiner pour la variante Mistral Small 4 119B 2603 Eagle, puis vérifier sa fiche modèle, ses conditions d'accès et son statut de publication avant toute adoption.

1. Installer la pile de service spécifiée par la fiche modèle : vLLM, Transformers depuis la branche main et mistral_common 1.10.0 ou plus récent.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
2. Servir le modèle de base avec vLLM, activer les analyseurs d'outils et de raisonnement Mistral, et attacher la tête Eagle via le décodage spéculatif de vLLM lorsque la complexité supplémentaire de service est justifiée.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
3. Pour les requêtes ordinaires, définir reasoning_effort à none ; pour les tâches difficiles, le définir à high via le client compatible OpenAI ou l'API Mistral.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>

## Bonnes pratiques {#best-practices}

- Utiliser reasoning_effort="high" avec une température de 0,7 pour les prompts complexes ; garder le raisonnement désactivé et ajuster la température entre 0,0 et 0,7 pour les tâches courantes.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Considérer le dépôt Eagle comme un compagnon de décodage spéculatif du modèle de base, et non comme le modèle applicatif autonome.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Dimensionner l'auto-hébergement selon le plancher d'accélérateurs documenté avant de choisir ce modèle ; son nombre de paramètres actifs ne supprime pas ses besoins en mémoire pour les poids de base.
  — <https://mistral.ai/news/mistral-small-4/?id=MistralSmall4>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-16 — La recommandation de choisir des modèles distincts Mistral Small pour les instructions, Magistral pour le raisonnement, Pixtral pour le multimodal et Devstral pour le codage, pour ces quatre grandes classes de capacités, est remplacée pour les déploiements où un seul point de terminaison Mistral Small 4 répond aux exigences.

## Points encore inconnus {#still-unknown}

- L'événement du 17 mars fourni lie le dépôt Eagle, tandis que l'annonce officielle de Mistral et la page de cycle de vie datent la publication du modèle de base au 16 mars 2026. La page du dépôt consultée aujourd'hui n'expose pas de date de création du dépôt ; l'heure exacte de sa publication reste donc non vérifiée.
- L'article de publication de Mistral donne 6 Md de paramètres actifs par jeton (8 Md en incluant les couches d'embedding et de sortie), alors que la fiche modèle Eagle indique 6,5 Md actifs. Cette réponse conserve le chiffre de la fiche modèle pour l'artefact de service actuel et ne considère pas cet écart comme résolu de façon indépendante.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle | mistralai/Mistral-Small-4-119B-2603-eagle | 2026-09-05 |
| https://mistral.ai/news/mistral-small-4/?id=MistralSmall4 | Présentation de Mistral Small 4 | 2026-09-05 |
| https://legal.mistral.ai/ai-governance/models/mistral-small-4/ | Mistral Small 4 — Cycle de vie du modèle | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:mistral-small-4`, fil `mistral-small`, 1 événement daté du 2026-03-17 au 2026-03-17.
- **Note pratique :** Au 2026-03-17, les praticiens doivent utiliser le dépôt Hugging Face lié comme artefact précis à examiner pour la variante Mistral Small 4 119B 2603 Eagle, puis vérifier sa fiche modèle, ses conditions d'accès et son statut de publication avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
