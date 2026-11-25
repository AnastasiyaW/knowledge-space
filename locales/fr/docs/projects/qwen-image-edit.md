---
title: "MCNL v1 pour Qwen-Image-Edit-2511"
category: projects
date: 2026-09-03
tags: [qwen-image-edit, mcnl-v1, lora, community-adapter]
aliases: ["MCNL v1", "ScottzillaSystems Qwen Image Edit adapter"]
level: 2
source_sha256: 83cf6eba7bcc6ccc9d17a6f857c7e781ec8bc530ec32de2ae0fa6b94fe7dd2ad
translation: machine
translated_at: '2026-10-24'
---
# MCNL v1 pour Qwen-Image-Edit-2511 {#mcnl-v1-for-qwen-image-edit-2511}

**Ligne de développement :** `project:qwen-image-edit` · fil `qwen-image-edit-development`  
**Dernier événement :** 2026-09-03 · 1 événement daté · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

MCNL v1 est un LoRA communautaire pour `Qwen-Image-Edit-2511`, issu du dépôt ScottzillaSystems. La fiche le présente comme un doublon de `aiunivers/qwen-image-edit-plus-nsfw-lora`. [Fiche modèle du distributeur](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true)

La fiche indique un adaptateur safetensors d'environ 563 Mo, et non une installation complète de modèle. [Fiche modèle du distributeur](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true)

## Mise en œuvre pratique {#practical-handling}

1. Considérer le téléchargement comme une dépendance d'adaptateur de `Qwen-Image-Edit-2511`, et non comme une installation autonome de 563 Mo.
   — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true>

2. Conserver l'identité exacte du checkpoint de base et de l'adaptateur dans le journal du workflow.
   — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true>

## Limites et questions ouvertes {#limits-and-open-questions}

Aucun test de fonctionnement contrôlé ni de configuration matérielle minimale n'a été établi pour cet adaptateur.

Aucune source qualifiée en chinois simplifié ni aucun retour d'expérience indépendant portant sur cet adaptateur précis n'a été trouvé.

Une page alternative liée à la fiche a renvoyé une erreur HTTP 401 lors de la vérification. Aucune disponibilité de successeur ni aucune affirmation de migration n'en découle.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true | Fiche modèle du distributeur de MCNL v1 | 2026-09-05 |

## Note pour agent {#agent-brief}

- **Sujet :** `project:qwen-image-edit`, fil `qwen-image-edit-development`, un événement daté du 2026-09-03.
- **Artefact exact :** `ScottzillaSystems/qwen-image-edit-plus-nsfw-lora`, MCNL v1 ; identité de base : `Qwen-Image-Edit-2511` ; fichier d'adaptateur : environ 563 Mo.
- **Règle d'usage :** Considérer le téléchargement comme une dépendance d'adaptateur, et non comme une installation autonome. Conserver l'identité exacte du checkpoint de base et de l'adaptateur dans le journal du workflow.
- **Limites :** Aucun test de fonctionnement contrôlé ni configuration matérielle minimale n'a été établi ; aucune source qualifiée en chinois simplifié n'a été trouvée ; aucune disponibilité de successeur ni aucune affirmation de migration ne découle de la page alternative.
