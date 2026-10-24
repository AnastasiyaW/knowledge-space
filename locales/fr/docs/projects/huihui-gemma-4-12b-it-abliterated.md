---
title: "Huihui-gemma-4-12B-it-abliterated — Publication du modèle"
category: projects
date: 2026-06-07
tags: [gemma, huihui-gemma-4-12b-it-abliterated, model-release, project]
aliases: ["Huihui-gemma-4-12B-it-abliterated"]
level: 2
source_sha256: 3703837ba61a043893ef50c980946abde70c07b9ef76ffe8d1d4e71cecf05b2b
translation: machine
translated_at: '2026-10-24'
---
# Huihui-gemma-4-12B-it-abliterated — Publication du modèle {#huihui-gemma-4-12b-it-abliterated-model-release}

**Ligne de développement :** `project:huihui-gemma-4-12b-it-abliterated` · fil `model-release`  
**Dernier événement :** 2026-06-07 · 1 événement daté depuis le 2026-06-07 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Huihui-gemma-4-12B-it-abliterated est un dérivé abliterated du modèle d'instructions Gemma 4 12B de Google, destiné aux utilisateurs locaux ayant besoin d'entrées texte, image et audio sans le comportement de refus habituel du modèle parent. Il conserve l'architecture multimodale unifiée ; son dépôt BF16 de 24 Go et le filtrage de sécurité réduit le rendent inadapté à une utilisation publique non supervisée. Verdict : ne l'utiliser que derrière des contrôles de politique au niveau applicatif et une revue des sorties.

## Ligne de développement {#development-line}

- **2026-06-07 — Référence au dépôt Huihui-gemma-4-12B-it-abliterated.** Le 2026-06-07, l'enregistrement a consigné un lien vers le dépôt Huihui-gemma-4-12B-it-abliterated sur Hugging Face. D'après les seuls éléments disponibles, cela justifie de considérer cette référence de dépôt comme un événement public significatif, sans établir de détails de publication ni de capacités du modèle.

## Ce qui a changé {#what-changed}

2026-06-07 — Huihui AI a publié Huihui-gemma-4-12B-it-abliterated. La fiche du modèle l'identifie comme une version abliterated de google/gemma-4-12B-it, avec les modes de réflexion et de non-réflexion traités et les couches 23 à 28 modifiées ; l'historique du dépôt à la même date consigne la publication. Constat sur l'événement : l'éditeur a ultérieurement averti que les tout premiers poids amont de Gemma 4 12B-it étaient défectueux, a relancé l'ablation du modèle et a invité les utilisateurs ayant déjà téléchargé le modèle à le télécharger à nouveau. Contexte nouveau : Google a introduit le Gemma 4 12B amont le 2026-06-03, comme modèle multimodal unifié de 12 B sans encodeur, conçu pour fonctionner localement avec 16 Go de VRAM ou de mémoire unifiée ; cette version amont est antérieure à ce dérivé et ne le remplace pas.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-07, les praticiens doivent considérer le dépôt Hugging Face lié comme point de départ pour évaluer ce modèle, et vérifier de manière indépendante sa fiche, sa licence, sa provenance et son usage prévu avant toute adoption.

1. Installez une version récente d'Ollama, puis exécutez `ollama run huihui_ai/gemma-4-abliterated:12b`.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
2. Pour Transformers, chargez le modèle avec `AutoProcessor` et `AutoModelForMultimodalLM`, en utilisant `device_map="auto"` ; testez séparément les chemins texte, image et audio avant tout déploiement.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
3. Si un artefact local plus petit est nécessaire, utilisez le dérivé GGUF QAT Q4_0 ultérieur avec llama.cpp ou Ollama, plutôt que de considérer le dépôt BF16 de 24 Go comme un téléchargement léger.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF>

## Bonnes pratiques {#best-practices}

- Téléchargez à nouveau le modèle plutôt que de conserver une copie locale ancienne : l'éditeur indique que les premiers poids amont présentaient des problèmes et que le dérivé a été à nouveau ablaté.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
- Conservez une revue humaine et des garde-fous côté application pour les contextes sensibles, publics, impliquant des mineurs ou à haute sécurité ; le filtrage réduit est une limitation explicite du modèle.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
- Utilisez la dernière version d'Ollama pour le nom de modèle Ollama fourni.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-07 — toute copie locale en cache issue des tout premiers poids amont de Gemma 4 12B-it est obsolète pour ce dérivé ; remplacez-la par la version republiée après ablation.

## Points restant inconnus {#still-unknown}

- La fiche du modèle ne fournit pas de résultats reproductibles avant/après sur le refus, les capacités ou la sécurité, de sorte que le coût pratique en qualité de l'abliteration n'est pas vérifié.
- La date exacte de la republication des poids après ablation n'est pas exposée par l'historique accessible du dépôt ; elle est donc rattachée à l'étape de publication du 2026-06-07 plutôt que traitée comme un événement daté distinct.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated | huihui-ai/Huihui-gemma-4-12B-it-abliterated | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated/commits/main | Commits · huihui-ai/Huihui-gemma-4-12B-it-abliterated | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/ | Présentation de Gemma 4 12B | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF | huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:huihui-gemma-4-12b-it-abliterated`, fil `model-release`, 1 événement daté du 2026-06-07 au 2026-06-07.
- **Remarque pratique :** Au 2026-06-07, les praticiens doivent considérer le dépôt Hugging Face lié comme point de départ pour évaluer ce modèle, et vérifier de manière indépendante sa fiche, sa licence, sa provenance et son usage prévu avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
