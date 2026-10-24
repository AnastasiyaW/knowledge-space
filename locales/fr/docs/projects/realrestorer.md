---
title: "RealRestorer"
category: projects
date: 2026-03-27
tags: [project, realrestorer]
aliases: ["RealRestorer"]
level: 2
source_sha256: dbcd624d983283fcdc41d329c6c3457ecec4627c6799b6d1b46df6095a83e60e
translation: machine
translated_at: '2026-10-24'
---
# RealRestorer {#realrestorer}

**Ligne de développement :** `project:realrestorer` · fil `realrestorer`  
**Dernier événement :** 2026-03-27 · 1 événement daté depuis le 2026-03-27 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

RealRestorer est un fine-tuning de Step1X-Edit destiné à la restauration d'images plutôt qu'à la génération d'images générale.

- Supprime le flou, le bruit, la brume, la pluie, le moiré, les reflets, les éblouissements et les artefacts de compression.
- Préserve la structure de la scène et le contenu sémantique grâce à un pipeline associant image et instruction.
- Livre le code, les poids, l'outillage de dégradation synthétique et RealIR-Bench.

## Ligne de développement {#development-line}

- **2026-03-27 — Les ressources du projet RealRestorer ont été reliées.** Le 2026-03-27, la ligne de développement de RealRestorer a été consignée avec des liens vers une page de projet, le dépôt source, la page du modèle et la référence source. Cet élément est important pour l'historique du projet, car il établit un point de référence public daté pour le code et les ressources de modèle associés. Les liens fournis ne suffisent pas à établir le statut exact de la publication, ses capacités ou ses versions.

## Ce qui a changé {#what-changed}

2026-03-26 — RealRestorer a publié ses poids de modèle, son pipeline de dégradation synthétique et RealIR-Bench ; l'article décrit neuf catégories de dégradation et un benchmark de 464 images. 2026-03-27 — L'ensemble de références publiques du projet a relié la page du projet, le code, la carte du modèle et l'article ; la fiche de publication officielle corrige la date de lancement sous-jacente au 2026-03-26. 2026-03-29 — Une démo Hugging Face est devenue disponible, ajoutant une voie d'essai accessible depuis un navigateur.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-27, les praticiens doivent considérer RealRestorer comme un projet disposant de ressources de code et de modèle liées, tout en vérifiant les versions exactes, les capacités et les conditions d'utilisation auprès des sources primaires liées avant toute adoption.

1. Clonez le dépôt officiel, installez son checkout diffusers patché fourni avec Python 3.12, puis installez les dépendances du projet et du benchmark.
  — <https://github.com/yfyang007/RealRestorer>
2. Téléchargez les poids RealRestorer/RealRestorer, chargez-les avec RealRestorerPipeline en BF16 ; fournissez une image d'entrée RGB et une instruction de restauration.
  — <https://huggingface.co/RealRestorer/RealRestorer>
3. Exécutez 28 étapes de débruitage, un guidance scale de 3.0, la graine 42 et un niveau de taille 1024 ; enregistrez l'image renvoyée.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Bonnes pratiques {#best-practices}

- Utilisez le checkout local patché de diffusers du dépôt plutôt que de supposer qu'une installation Diffusers standard implémente RealRestorerPipeline.
  — <https://github.com/yfyang007/RealRestorer>
- Commencez avec CUDA, BF16, 28 étapes, un guidance de 3.0, la graine 42 et une entrée d'environ 1024×1024 ; prévoyez environ 34 Go de mémoire GPU au pic avec ce paramétrage.
  — <https://github.com/yfyang007/RealRestorer>
- Considérez le modèle publié et les ressources du benchmark comme des matériaux de recherche académique non commerciaux, même si le code est destiné à une publication sous licence Apache-2.0.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-29 — L'hypothèse d'un accès uniquement par ligne de commande est obsolète : le dépôt officiel consigne la publication d'une démo Hugging Face.

## Points encore inconnus {#still-unknown}

- Les éléments disponibles ne permettent pas d'établir que le 2026-03-27 correspond à une publication technique distincte, plutôt qu'à la documentation de la publication du 2026-03-26.
- Le résultat du benchmark de l'article, présenté comme le meilleur parmi les logiciels open source, n'a pas été reproduit de manière indépendante dans les sources examinées.
- event_findings:[{"event_date":"2026-03-27","finding":"Correction : le dépôt officiel date la publication des poids de RealRestorer, du pipeline de dégradation et de RealIR-Bench au 2026-03-26, soit un jour avant cet enregistrement daté.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-26"},{"event_date":"2026-03-27","finding":"Le modèle exact publié est RealRestorer/RealRestorer : un modèle BF16 de 12B affiné à partir de stepfun-ai/Step1X-Edit ; sa carte de modèle distingue le code destiné à une publication sous Apache-2.0 des modèles et ressources de benchmark réservés à la recherche académique non commerciale.","source_url":"https://huggingface.co/RealRestorer/RealRestorer","source_date":"2026-03-26"}]
- new_events:[{"date":"2026-03-26","finding":"L'article, les poids, le pipeline de dégradation synthétique et le lancement de RealIR-Bench ont été documentés. Le benchmark contient 464 images réelles dégradées couvrant neuf types de dégradation courants.","source_url":"https://arxiv.org/abs/2603.25502","source_date":"2026-03-26"},{"date":"2026-03-29","finding":"Le dépôt officiel a annoncé la publication d'une démo Hugging Face pour RealRestorer.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-29"}]

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://yfyang007.github.io/RealRestorer/ | RealRestorer : vers une restauration d'images généralisable en conditions réelles | 2026-09-05 |
| https://github.com/yfyang007/RealRestorer | yfyang007/RealRestorer | 2026-09-05 |
| https://huggingface.co/RealRestorer/RealRestorer | Carte du modèle RealRestorer/RealRestorer | 2026-09-05 |
| https://arxiv.org/abs/2603.25502 | RealRestorer : vers une restauration d'images généralisable en conditions réelles grâce à des modèles d'édition d'images à grande échelle | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:realrestorer`, fil `realrestorer`, 1 événement daté du 2026-03-27 au 2026-03-27.
- **Note pratique :** À partir du 2026-03-27, les praticiens doivent considérer RealRestorer comme un projet disposant de ressources de code et de modèle liées, tout en vérifiant les versions exactes, les capacités et les conditions d'utilisation auprès des sources primaires liées avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
