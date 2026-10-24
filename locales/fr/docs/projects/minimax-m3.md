---
title: "MiniMax M3"
category: projects
date: 2026-06-13
tags: [minimax-m3, project]
aliases: ["MiniMax M3"]
level: 2
source_sha256: 4e7e7b61809a0b7c4c9e0926ff6911fbda821a3cd619a13c1294c0e433dbb829
translation: machine
translated_at: '2026-10-24'
---
# MiniMax M3 {#minimax-m3}

**Ligne de développement :** `project:minimax-m3` · fil `minimax-m3`  
**Dernier événement :** 2026-06-13 · 1 daté depuis le 2026-06-13 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

MiniMax M3 est un modèle MoE multimodal natif à poids ouverts, destiné aux développeurs qui créent des agents de programmation, des outils d'analyse de documents et de dépôts, ainsi que des workflows à entrée d'images ou de vidéos.

- Entrée texte, image et vidéo.
- API hébergées compatibles Anthropic et compatibles OpenAI.
- Service local via SGLang, vLLM, Transformers, KTransformers ou Unsloth.

Contexte de 1M de tokens ; environ 428B de paramètres au total et 23B de paramètres activés ; le point de contrôle officiel sur Hugging Face est en BF16, sous la licence minimax-community.

Commencez par l'API hébergée ; n'auto-hébergez qu'après avoir dimensionné le matériel et la capacité de contexte.

## Ligne de développement {#development-line}

- **2026-06-13 — publication des ressources publiques du projet, du modèle et de l'API MiniMax M3.** Le 2026-06-13, MiniMax M3 a été relié à un dépôt GitHub public, à une page de modèle Hugging Face et à la documentation de génération de texte de MiniMax. Ces liens relient les surfaces de la source du projet, de la distribution du modèle et de la documentation d'utilisation.

## Ce qui a changé {#what-changed}

- 2026-06-01 — MiniMax M3 lancé dans MiniMax Code, Token Plan et l'API ; MiniMax a indiqué que les poids suivraient dans un délai de dix jours.
- 2026-06-13 — le dépôt GitHub public, le point de contrôle Hugging Face et la documentation de l'API ont été listés ensemble ; l'historique GitHub en amont ne montre aucune modification du modèle ou de la documentation datée séparément à cette date.
- 2026-06-18 — KTransformers a été ajouté aux options de déploiement local documentées.
- 2026-06-22 — un tutoriel Unsloth a été ajouté aux options de déploiement local documentées.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-13, évaluez MiniMax M3 à partir de son dépôt lié, de sa page de modèle Hugging Face et de sa documentation de génération de texte avant de décider de l'adopter.

1. Créez une clé d'API ou d'abonnement MiniMax et sélectionnez `MiniMax-M3` comme modèle.
  — <https://platform.minimax.io/docs/guides/text-generation>
2. Pour le chemin d'API recommandé, envoyez une requête Anthropic Messages à `https://api.minimax.io/anthropic/v1/messages` ; utilisez le point de terminaison `/v1` compatible OpenAI uniquement lorsque votre client l'exige.
  — <https://platform.minimax.io/docs/guides/text-generation>
3. Réglez `thinking` sur `adaptive` pour les charges de travail mixtes, `enabled` pour un raisonnement délibéré, ou `disabled` lorsque la latence et le débit sont plus importants.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
4. Pour l'inférence locale, téléchargez `MiniMaxAI/MiniMax-M3` et servez-le avec un runtime pris en charge, comme SGLang ou vLLM.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M3>

## Bonnes pratiques {#best-practices}

- Commencez par les paramètres d'échantillonnage officiels : `temperature=1.0` et `top_p=0.95`.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
- Traitez la fenêtre de contexte de 1M comme une cible de déploiement et non comme un réglage automatique : choisissez l'accélérateur, le dtype, le parallélisme, le cache et le contexte maximal en fonction du profil de trafic réel.
  — <https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md>
- Vérifiez la prise en charge des outils propre à chaque fournisseur dans le client exact avant de vous y fier ; un ticket ouvert signale que la recherche web intégrée de style Anthropic n'était pas prise en charge malgré la compatibilité avec l'API Messages.
  — <https://github.com/MiniMax-AI/MiniMax-M3/issues/23>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-01 — la recommandation selon laquelle un modèle de la série M2 est le modèle M par défaut le plus récent est remplacée pour les nouveaux travaux ciblant M3 à long contexte, multimodaux, de programmation et agentiques. La documentation actuelle maintient les modèles M2 disponibles plutôt que de les déclarer retirés.

## Toujours inconnu {#still-unknown}

- Aucune note de version de première partie ni aucun commit en amont n'identifie un modèle, des poids ou une modification de l'API MiniMax M3 distincts le 2026-06-13 ; nous considérons cette date comme une étape d'accès aux liens, et non comme une date de lancement.
- Les commits du README des 2026-07-01 et 2026-07-11 ont des messages génériques ; leurs changements visibles par l'utilisateur ne peuvent donc pas être énoncés de manière fiable.
- MiniMax n'a pas publié de tableau unique et actuel de dimensionnement matériel de première partie pour le point de contrôle officiel M3 en BF16, selon les différentes longueurs de contexte cibles.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://www.minimax.io/blog/minimax-m3 | MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3 | MiniMax-AI/MiniMax-M3 | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/commits/main | Historique des commits MiniMax-M3 | 2026-09-05 |
| https://huggingface.co/MiniMaxAI/MiniMax-M3 | Fiche du modèle MiniMaxAI/MiniMax-M3 | 2026-09-05 |
| https://platform.minimax.io/docs/guides/text-generation | Model Invocation — MiniMax API Docs | 2026-09-05 |
| https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md | MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/issues/23 | M3 Bug: Anthropic-compatible endpoint does not support the web_search tool | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:minimax-m3`, fil `minimax-m3`, 1 événement daté du 2026-06-13 au 2026-06-13.
- **Remarque pratique :** Au 2026-06-13, les praticiens doivent évaluer MiniMax M3 à partir de son dépôt lié, de sa page de modèle Hugging Face et de sa documentation de génération de texte avant de décider de l'adopter.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
