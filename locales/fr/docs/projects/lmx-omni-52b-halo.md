---
title: "LMX-Omni-52B-Halo"
category: projects
date: 2026-06-12
tags: [lmx-omni-52b-halo, project]
aliases: ["LMX-Omni-52B-Halo"]
level: 2
source_sha256: 6eb3737b10406bb03330fd56b51fcb9ce8f013ff23bfd6e3a0b8caf4a92d980c
translation: machine
translated_at: '2026-10-24'
---
# LMX-Omni-52B-Halo {#lmx-omni-52b-halo}

**Ligne de développement :** `project:lmx-omni-52b-halo` · fil `lmx-omni-52b-halo`  
**Dernier événement :** 2026-06-12 · 1 daté depuis le 2026-06-12 · **Recherché :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

LMX-Omni-52B-Halo est un ensemble composé de Qwen3.6-35B-A3B-MTP, Flux-2-Klein-9B, Whisper-Large-v3-Turbo et kokoro-v1, destiné aux applications multimodales locales. Fonctionnalités : chat et analyse d'images ; génération et édition d'images ; transcription ; synthèse vocale. Limite : le chargement des composants occupe environ 44,8 Go, et la classe Halo vise les appareils de niveau Strix Halo. Verdict : à choisir pour un prototype ou une application any-to-any locale, si le volume de téléchargement et la latence de la boucle interne de tool-calling sont acceptables.

## Ligne de développement {#development-line}

- **2026-06-12 — LMX-Omni-52B-Halo a été lié à son dépôt de modèle Hugging Face.** Le 2026-06-12, la fiche a enregistré un lien vers le dépôt Hugging Face de LMX-Omni-52B-Halo. Cela établit que le dépôt est un artefact du projet à cette date, mais n'établit ni son statut de publication, ni ses capacités, ni sa licence, ni son usage prévu.

## Modifications {#what-changed}

2026-06-12 — la fiche du modèle décrivait LMX-Omni-52B-Halo comme un ensemble omni unique compatible OpenAI ; le dépôt principal a été créé le 2026-06-03, et le 2026-06-04 son manifeste est passé au format unifié et l'ancien `collection.json` a été supprimé. 2026-06-23 — un system prompt configurable pour la collection a été ajouté au manifeste publié. 2026-08-08 — un rapport ouvert et non résolu : la collection ne transmet pas le reasoning_content du planificateur dans le flux Open WebUI ; pour une interface qui requiert un raisonnement visible, cela reste une limitation.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-12, les praticiens doivent utiliser le dépôt Hugging Face lié comme point de départ pour vérifier les artefacts et la documentation de LMX-Omni-52B-Halo avant de s'appuyer sur le projet.

1. Installez Lemonade, puis téléchargez tous les composants avec la commande `lemonade pull LMX-Omni-52B-Halo` et lancez le modèle avec `lemonade run LMX-Omni-52B-Halo`.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
2. Dans un client compatible OpenAI, choisissez le nom du modèle pour les requêtes vers `/chat/completions` ; le serveur appelle lui-même les composants et renvoie les images et l'audio dans le message de réponse.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
3. Dans un client MCP, transmettez `model: "LMX-Omni-52B-Halo"` à `lemonade_omni` si vous voulez un seul tour multimodal avec images et audio.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>

## Bonnes pratiques {#best-practices}

- Indiquez Halo explicitement uniquement sur le matériel approprié ; par défaut, MCP utilise LMX-Omni-5.5B-Lite, plus petit et plus rapide.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Pour les artefacts MCP, définissez `output_dir` : cela donne des noms de fichiers uniques et convient aux clients qui n'affichent pas les audio content blocks.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Ne comptez pas sur l'affichage en flux du raisonnement dans Open WebUI : le problème signalé pour les collections Omni reste ouvert.
  — <https://github.com/lemonade-sdk/lemonade/issues/2990>

## Éléments remplacés {#superseded-by-this}

- 2026-05-21 — l'ancien guide sur les « collections » est obsolète : la version Lemonade v10.6.0 les a remplacées par les modèles LMX-Omni-52B-Halo et LMX-Omni-5.5B-Lite.
- 2026-06-04 — l'ancien format de manifeste `collection.json` pour ce modèle a été remplacé par le fichier unifié `LMX-Omni-52B-Halo.json`.

## Points non élucidés {#still-unknown}

- La source primaire ne date pas précisément du 2026-06-12 une publication ou une modification ; elle confirme l'état de la page, mais ne fournit pas d'entrée distincte pour un événement ce jour-là.
- Le schéma de réponse ne contient pas les champs demandés event_findings et new_events ; leurs compléments effectifs figurent dans what_changed et unknowns.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo | Fiche du modèle LMX-Omni-52B-Halo | 2026-09-05 |
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo/commits/main | Historique des commits de LMX-Omni-52B-Halo | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/dev/lemonade-omni.md | Documentation des modèles Lemonade Omni | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md | Documentation de l'API MCP de Lemonade | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/releases/tag/v10.6.0 | Version Lemonade v10.6.0 | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/issues/2990 | Les collections Omni ne diffusent pas le reasoning_content du planificateur | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:lmx-omni-52b-halo`, fil `lmx-omni-52b-halo`, 1 événement daté, 2026-06-12 → 2026-06-12.
- **Remarque pratique :** Au 2026-06-12, les praticiens doivent utiliser le dépôt Hugging Face lié comme point de départ pour vérifier les artefacts et la documentation de LMX-Omni-52B-Halo avant de s'appuyer sur le projet.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
