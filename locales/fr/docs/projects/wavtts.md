---
title: "WavTTS"
category: projects
date: 2026-06-08
tags: [project, wavtts, wavtts-development]
aliases: ["WavTTS"]
level: 2
source_sha256: 4bc106e987d74ed84836b4d87c53d11987a8839d1fd016fb4870fe658f0a56eb
translation: machine
translated_at: '2026-10-24'
---
# WavTTS {#wavtts}

**Ligne de développement :** `project:wavtts` · fil `wavtts-development`  
**Dernier événement :** 2026-06-08 · 1 événement daté depuis le 2026-06-08 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

WavTTS est un système de synthèse vocale zero-shot open source qui se conditionne sur un court enregistrement de référence et sa transcription. Capacités : génération directe à partir de la forme d'onde brute ; inférence par CLI et par script ; point de contrôle officiel à 16 kHz ; code d'entraînement et d'évaluation. Limite : les poids publiés sont sous licence CC BY-NC 4.0, et le modèle n'est pas proposé par un fournisseur d'inférence Hugging Face. Verdict : à utiliser pour une synthèse vocale conditionnée par la voix, locale et non commerciale, et non comme API de production hébergée et interchangeable.

## Ligne de développement {#development-line}

- **2026-06-08 — Les ressources publiques du projet WavTTS ont été consignées.** Le 2026-06-08, la ligne de développement de WavTTS a été consignée avec des liens vers son site du projet, son dépôt source, sa page de modèle, sa démo et une intégration ComfyUI. Cela fournit un point de référence public daté pour localiser le projet et les outils associés. Les éléments disponibles ne permettent pas d'établir quelle publication ou quelle modification de code, le cas échéant, accompagnait ces liens.

## Changements {#what-changed}

2026-06-08 — WavTTS a été présenté avec sa page de projet, son code officiel et son point de contrôle à 16 kHz, une démo web, ainsi qu'une intégration ComfyUI communautaire postérieure ; la publication officielle elle-même est datée du 2026-06-03.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-08, les praticiens doivent utiliser les liens datés vers le projet, le code source, le modèle, la démo et l'intégration ComfyUI de WavTTS comme point de départ pour évaluer ou intégrer le projet ; cette seule ligne n'établit aucun comportement particulier d'une version.

1. Clonez le dépôt officiel, créez un environnement Conda Python 3.10, installez PyTorch compatible CUDA, puis installez WavTTS en mode éditable.
  — <https://github.com/cwx-worst-one/WavTTS>
2. Exécutez `wavtts_infer-cli` avec `--model WavTTS`, un fichier WAV de référence, la transcription de cet enregistrement et le texte à synthétiser ; la configuration par défaut télécharge automatiquement le point de contrôle officiel.
  — <https://huggingface.co/worstchan/WavTTS>
3. Pour ComfyUI, installez le nœud communautaire via ComfyUI Manager ou dans `custom_nodes`, redémarrez ComfyUI, puis connectez une entrée audio de référence, la transcription de référence obligatoire, le chargeur de modèle et le nœud de génération.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Bonnes pratiques {#best-practices}

- Utilisez la configuration Conda/Python 3.10 fournie et une version de PyTorch prise en charge par CUDA ; le dépôt amont recommande Conda pour la gestion des dépendances.
  — <https://github.com/cwx-worst-one/WavTTS>
- Fournissez une transcription exacte avec l'enregistrement de référence. L'intégration ComfyUI traite `reference_text` comme obligatoire et recommande une invite vocale propre de 5 à 12 secondes.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>
- Pour l'intégration ComfyUI communautaire, privilégiez FP32 pour la fiabilité ou son préréglage BF16 mixte pour une consommation de VRAM plus faible ; évitez les préréglages FP16, que son mainteneur signale comme pouvant produire des échantillons non finis.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- L'espace Hugging Face lié le 2026-06-08 a renvoyé une erreur interne lors de la relecture ; sa disponibilité actuelle et son interface exacte ne sont donc pas vérifiées.
- L'intégration ComfyUI est un dépôt communautaire distinct, et non une publication officielle de WavTTS.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://wavtts.github.io/ | Page du projet WavTTS | 2026-09-05 |
| https://github.com/cwx-worst-one/WavTTS | Dépôt GitHub officiel de WavTTS | 2026-09-05 |
| https://huggingface.co/worstchan/WavTTS | Fiche de modèle officielle worstchan/WavTTS | 2026-09-05 |
| https://github.com/Saganaki22/WavTTS-ComfyUI | Intégration communautaire WavTTS-ComfyUI | 2026-09-05 |
| https://arxiv.org/abs/2606.03455 | WavTTS : vers une synthèse vocale zero-shot de haute qualité par modélisation directe de la forme d'onde brute | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:wavtts`, fil `wavtts-development`, 1 événement daté du 2026-06-08 au 2026-06-08.
- **Note pratique :** Au 2026-06-08, les praticiens doivent utiliser les liens datés vers le projet, le code source, le modèle, la démo et l'intégration ComfyUI de WavTTS comme point de départ pour évaluer ou intégrer le projet ; cette seule ligne n'établit aucun comportement particulier d'une version.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
