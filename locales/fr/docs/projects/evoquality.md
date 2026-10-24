---
title: "EvoQuality"
category: projects
date: 2026-06-11
tags: [bytedance-evoquality, bytedance-evoquality-development, evoquality, project]
aliases: ["EvoQuality"]
level: 2
source_sha256: a03c212de492ca7201b786313fc5927969d561b7fc3a86035f448fcdeb31c145
translation: machine
translated_at: '2026-10-24'
---
# EvoQuality {#evoquality}

**Ligne de développement :** `project:evoquality` · fil `bytedance-evoquality-development`  
**Dernier événement :** 2026-06-11 · 1 événement daté depuis le 2026-06-11 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

EvoQuality est un VLM d'évaluation de la qualité d'image sans référence, destiné aux chercheurs et aux équipes de pipelines d'images.
- Notation : attribue une note à une image selon sa qualité perceptuelle.
- Comparaison : compare deux images côte à côte.
- Classement : produit un signal de classement fondé sur le vote, utilisable pour le filtrage ou le nettoyage de données.

Le checkpoint BF16 publié comporte 8 milliards de paramètres et correspond à un seul cycle d'auto-évolution. Utilisez-le comme proxy perceptuel, avec des vérifications ponctuelles, et non comme décideur objectif ou pour des décisions à forts enjeux.

## Ligne de développement {#development-line}

- **2026-06-11 — ByteDance a publié une ressource EvoQuality sur Hugging Face.** ByteDance a publié un lien public vers EvoQuality sur Hugging Face le 2026-06-11. Ce lien marque le point de publication officielle du projet. La publication ne précise ni le type d'artefact, ni les détails de version, ni les capacités, ni les notes d'annonce.

## Changements {#what-changed}

2026-06-11 — Les poids d'EvoQuality sont devenus disponibles sur ByteDance/EvoQuality. La version publiée expose un checkpoint BF16 de 8B, entraîné à partir de Qwen2.5-VL-7B par vote par paires auto-supervisé et GRPO.

2025-09-30 — L'article est paru sur arXiv. Il décrit la méthode de vote et de classement sans étiquettes, et rapporte une amélioration de 31,8 % du PLCC par rapport à son VLM de base, dans une évaluation IQA en zero-shot.

## Mode d'emploi {#how-to-use-this}

Utilisez la ressource Hugging Face ByteDance/EvoQuality du 2026-06-11 comme point de référence daté. Confirmez le type d'artefact et les modalités d'usage avant toute adoption.

1. Chargez `ByteDance/EvoQuality` avec Transformers en tant que modèle image-texte-vers-texte, soumettez une image accompagnée du prompt de notation de la fiche modèle, puis analysez la note numérique finale placée dans la boîte (boxed).
  — <https://huggingface.co/ByteDance/EvoQuality>
2. Pour un lot de classement en local, exécutez le script d'inférence par vote par paires du dépôt avec votre checkpoint, votre répertoire d'images, votre CSV de paires et un nombre de votes explicite.
  — <https://github.com/bytedance/EvoQuality>
3. Pour le déploiement, lancez le modèle avec vLLM ou SGLang et envoyez des requêtes de chat-completions combinant image et texte.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Bonnes pratiques {#best-practices}

- Utilisez-le pour le classement, le filtrage, le nettoyage de données et l'évaluation de pré-production. Combinez la note avec des indicateurs métier et des vérifications manuelles ponctuelles.
  — <https://huggingface.co/ByteDance/EvoQuality>
- Pour l'inférence par paires, randomisez l'ordre des images afin de réduire le biais de position. Gardez les prompts, le nombre d'échantillons et les paramètres de décodage fixes lorsque vous comparez des exécutions.
  — <https://huggingface.co/ByteDance/EvoQuality>
- N'utilisez pas le résultat comme critère unique de modération, d'imagerie médicale, de preuve juridique ou de toute autre décision à forts enjeux. Le décalage de domaine et le biais des pseudo-étiquettes restent des limites déclarées.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Remplacé par {#superseded-by-this}

- Aucun élément marqué comme obsolète à ce jour.

## Points inconnus {#still-unknown}

- La fiche Hugging Face documente le checkpoint et les modes d'utilisation, mais ne propose pas d'historique de notes de version numérotées. Nous n'avons trouvé aucun checkpoint EvoQuality officiel plus récent dans les sources examinées.
- L'extrait d'installation du dépôt utilise une URL de clonage fictive (`your-organization/evoquality`). Utilisez l'URL publique du dépôt indiquée ci-dessus pour le clonage.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/ByteDance/EvoQuality | Fiche modèle ByteDance/EvoQuality | 2026-09-05 |
| https://github.com/bytedance/EvoQuality | Dépôt bytedance/EvoQuality | 2026-09-05 |
| https://arxiv.org/abs/2509.25787 | Self-Evolving Vision-Language Models for Image Quality Assessment via Voting and Ranking | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:evoquality`, fil `bytedance-evoquality-development`, 1 événement daté, du 2026-06-11 au 2026-06-11.
- **Note pratique :** à partir du 2026-06-11, les praticiens doivent utiliser la ressource Hugging Face ByteDance/EvoQuality comme point de référence public daté pour évaluer les artefacts du projet, tout en confirmant indépendamment le type exact d'artefact et les modalités d'usage avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
