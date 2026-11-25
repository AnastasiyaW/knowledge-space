---
title: "dots.mocr"
category: projects
date: 2026-03-22
tags: [dots-mocr, project]
aliases: ["dots.mocr"]
level: 2
source_sha256: d87df4ce720a836981dbbd41e3ab80bd27a1f7feae200bad41412c8e081a2c70
translation: machine
translated_at: '2026-10-24'
---
# dots.mocr {#dotsmocr}

**Ligne de développement :** `project:dots-mocr` · fil `dots-mocr`  
**Dernier événement :** 2026-03-22 · 1 événement daté depuis le 2026-03-22 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

dots.mocr est un VLM de 3B destiné aux équipes qui doivent extraire de PDF et d'images non seulement le texte, mais aussi la mise en page, les tableaux, les formules et les graphiques ; il concurrence PaddleOCR-VL et DeepSeek-OCR. Fonctionnalités : OCR et bbox, sortie en Markdown, HTML et LaTeX, analyse de pages web et de scènes, conversion d'image en SVG via le modèle séparé dots.mocr-svg. Limite : les tableaux complexes, les formules et les SVG peuvent encore produire des résultats instables. Conclusion : pour un traitement de documents auto-hébergé, il est raisonnable de commencer avec vLLM et de valider les pages complexes sur vos propres données.

## Ligne de développement {#development-line}

- **2026-03-22 — les ressources du projet dots.mocr ont été référencées.** Le 2026-03-22, un message daté a renvoyé vers le dépôt GitHub de dots.mocr, deux ressources Hugging Face et un site de projet. Cela constitue un point de référence public dans la ligne de développement du projet, y compris une ressource liée concernant le SVG. Le contenu de la publication d'origine et la nature d'une éventuelle sortie ou mise à jour n'ont pas été fournis ; cet enregistrement n'affirme donc ni des capacités, ni des versions, ni des performances.

## Ce qui a changé {#what-changed}

2026-03-22 — le modèle principal dots.mocr de 3B et le modèle séparé dots.mocr-svg de 3B sont devenus disponibles ; l'annonce initiale du projet est datée du 2026-03-19, et non du 22 mars. Pour cette étape : GitHub indique une version principale publiée le 2026-03-19, mentionne un modèle de 3 milliards de paramètres et la variante dots.mocr-svg pour la conversion d'image en SVG ; Hugging Face indique le format BF16 et une taille de 3B pour les deux modèles. Nouveaux événements : le 2026-03-13, l'article MOCR a été soumis pour la première fois sur arXiv ; le 2026-03-19, l'article a été mis à jour en v2, et le code ainsi que les deux modèles ont été publiés ; le 2026-03-20, deux commits ultérieurs portant les messages « fix ignore » et « update » ont été ajoutés au dépôt.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-03-22, les praticiens doivent évaluer dots.mocr à partir du dépôt GitHub lié, du site du projet et des ressources Hugging Face distinctes, y compris la ressource liée au SVG, avant de l'retenir pour un flux de travail OCR ; les liens datés seuls ne permettent pas d'étayer des affirmations sur les capacités ou les benchmarks.

1. Déployez l'analyseur de documents principal via vLLM : `vllm serve rednote-hilab/dots.mocr --trust-remote-code` ; pour le SVG, choisissez `rednote-hilab/dots.mocr-svg`.
  — <https://github.com/rednote-hilab/dots.mocr>
2. Transmettez une image ou un PDF à `dots_mocr/parser.py` ; le résultat comprend un JSON avec les éléments de mise en page, un Markdown et une image avec les bbox.
  — <https://github.com/rednote-hilab/dots.mocr>
3. Si vous avez besoin d'un endpoint compatible OpenAI, lancez le modèle via vLLM et envoyez des messages combinant image et texte vers `/v1/chat/completions`.
  — <https://huggingface.co/rednote-hilab/dots.mocr>

## Bonnes pratiques {#best-practices}

- Pour l'inférence en production, utilisez vLLM : les auteurs le recommandent, et Transformers est signalé comme une voie plus lente.
  — <https://github.com/rednote-hilab/dots.mocr>
- Choisissez `dots.mocr-svg` pour la conversion d'image en SVG ; le modèle principal est limité par sa capacité de 3B et n'est pas aussi performant sur toutes les tâches SVG.
  — <https://github.com/rednote-hilab/dots.mocr>
- N'utilisez pas de points dans le nom du dossier local des poids : la documentation indique `DotsMOCR` comme solution de contournement temporaire.
  — <https://github.com/rednote-hilab/dots.mocr>
- Vérifiez les tableaux complexes, les formules et les graphiques sur votre jeu de données cible : ce sont des limites du modèle explicitement mentionnées.
  — <https://github.com/rednote-hilab/dots.mocr>

## Remplace {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Le champ event_findings est absent du schéma de sortie fourni ; son contenu est inclus dans ce qui a changé. GitHub ne propose aucune version publiée (releases) avec numéro, si bien que la build actuelle ne peut pas être rattachée à un tag formel ni à un asset de release.
- Le dépôt et les model cards redirigent de rednote-hilab vers studio-dots ; les sources n'indiquent pas s'il s'agit uniquement d'un renommage ou d'un transfert de l'organisation, ou d'un changement de propriétaire.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/rednote-hilab/dots.mocr | studio-dots-ai/dots.mocr — Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr | dots-studio/dots.mocr — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr-svg | dots-studio/dots.mocr-svg — Hugging Face model card | 2026-09-05 |
| https://arxiv.org/abs/2603.13032 | Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/commits/main | studio-dots-ai/dots.mocr commit history | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/releases | studio-dots-ai/dots.mocr releases | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:dots-mocr`, fil `dots-mocr`, 1 événement daté du 2026-03-22 au 2026-03-22.
- **Note pratique :** Depuis le 2026-03-22, les praticiens doivent évaluer dots.mocr à partir du dépôt GitHub lié, du site du projet et des ressources Hugging Face distinctes, y compris la ressource liée au SVG, avant de le retenir pour un flux de travail OCR ; les liens datés seuls ne permettent pas d'étayer des affirmations sur les capacités ou les benchmarks.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
