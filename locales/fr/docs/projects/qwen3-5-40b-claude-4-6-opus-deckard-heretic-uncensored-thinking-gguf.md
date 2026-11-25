---
title: "Distribution GGUF de Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF"
category: projects
date: 2026-03-25
tags: [gguf-distribution, project, qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf, qwen3_5_40b_claude_4_6_opus_deckard_heretic_uncensored_thinking_gguf]
aliases: ["Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF"]
level: 2
source_sha256: b571ae47d2533c74f3dfc4f434367508b1bd9957486ee309ee173d9ed16eb543
translation: machine
translated_at: '2026-10-24'
---
# Distribution GGUF de Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF {#qwen35-40b-claude-46-opus-deckard-heretic-uncensored-thinking-gguf-gguf-distribution}

**Ligne de développement :** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf` · fil `gguf-distribution`  
**Dernier événement :** 2026-03-25 · 1 événement daté depuis le 2026-03-25 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF est un ensemble de quantifications GGUF statiques d'un modèle multimodal de 39B affiné, destiné à llama.cpp, Ollama et aux serveurs locaux compatibles OpenAI.

- Traitement de texte et d'images lorsqu'il est associé à un fichier mmproj.
- Exécution locale en CLI et en serveur local.
- Choix de la quantification en fonction de la mémoire disponible et de la qualité recherchée.

Q4_K_M occupe 24,0 Go, Q8_0 occupe 41,6 Go, et les fichiers mmproj autonomes occupent 0,7 à 1,0 Go.

Il s'agit d'une version locale utilisable en pratique, mais les affirmations sur l'absence de censure et la qualité de l'affinage doivent être vérifiées séparément, au regard de vos propres tâches et risques.

## Ligne de développement {#development-line}

- **2026-03-25 — Référence Hugging Face enregistrée pour la lignée de modèles GGUF.** Les fichiers vont de Q2_K (14,5 Go) à Q8_0 (41,6 Go), auxquels s'ajoutent deux fichiers de projecteur multimodal ; la fiche du modèle renvoie directement au dépôt amont de DavidAU et à une variante i1/imatrix distincte.

## Ce qui a changé {#what-changed}

2026-03-25 — Les quantifications GGUF statiques du modèle de base de 39B sont disponibles : de Q2_K (14,5 Go) à Q8_0 (41,6 Go), auxquels s'ajoutent deux fichiers de projecteur multimodal ; la fiche renvoie directement au dépôt amont de DavidAU et à une variante i1/imatrix distincte.

2026-03-25 — L'index des quantifications répertorie aussi une version i1-GGUF distincte de mradermacher ; il s'agit d'une construction imatrix pondérée parallèle du même point de contrôle, et non d'une mise à jour de la lignée GGUF statique.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-25, les praticiens peuvent utiliser la page Hugging Face liée comme piste pour cette lignée de modèles GGUF, tout en vérifiant de manière indépendante ses fichiers, sa provenance, sa licence et sa compatibilité d'exécution avant utilisation.

1. Choisissez une quantification en fonction de la mémoire disponible ; la fiche suggère Q4_K_M pour une première exécution locale, et présente Q4_K_S comme une option rapide recommandée.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
2. Exécutez le modèle avec llama.cpp : `llama serve -hf mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M` ; le serveur fournit un point de terminaison local compatible OpenAI.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
3. Pour Ollama, exécutez `ollama run hf.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M` ; téléchargez un mmproj compatible depuis le dépôt statique pour traiter des images.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>

## Bonnes pratiques {#best-practices}

- Ne choisissez pas une quantification uniquement sur la taille du fichier : l'auteur indique que la liste est triée par taille, et que les quantifications IQ surpassent souvent les variantes non IQ de taille similaire.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
- Récupérez le mmproj depuis le dépôt GGUF statique pour les tâches de vision ; le dépôt i1/imatrix indique que son mmproj s'y trouve.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF>
- Testez le modèle sur vos propres tâches et exigences de sécurité avant déploiement : la fiche décrit la provenance et les caractéristiques revendiquées, mais ne fournit ni benchmark indépendant ni garantie de comportement.
  — <https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking>

## Remplacé par ceci {#superseded-by-this}

- Rien d'obsolète signalé pour l'instant.

## Toujours inconnu {#still-unknown}

- Les champs event_findings et new_events demandés sont absents du schéma de réponse ; les faits relatifs au 2026-03-25 figurent dans what_changed.
- La date exacte de publication du modèle amont de DavidAU et les métriques de qualité indépendantes ne sont pas confirmées par les sources citées.
- La fiche du modèle qualifie le modèle de vision et fournit un mmproj, mais la compatibilité d'exécution avec les images dépend de la version et de la configuration du runtime.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | 2026-09-05 |
| https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | 2026-09-05 |
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf`, fil `gguf-distribution`, 1 événement daté, du 2026-03-25 au 2026-03-25.
- **Note pratique :** Au 2026-03-25, les praticiens peuvent utiliser la page Hugging Face liée comme piste pour cette lignée de modèles GGUF, tout en vérifiant de manière indépendante ses fichiers, sa provenance, sa licence et sa compatibilité d'exécution avant utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
