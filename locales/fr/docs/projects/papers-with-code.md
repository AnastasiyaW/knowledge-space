---
title: "Papers with Code"
category: projects

tags: [papers-with-code, papers-with-code-development, project]
aliases: ["Papers with Code"]
level: 2
source_sha256: 6d2d5beaf4244b95a151a1b750ea90ecab45916dbbc0f6cf4deb66c5d2b3a6a0
translation: machine
translated_at: '2026-10-24'
---
# Papers with Code {#papers-with-code}

**Ligne de développement :** `project:papers-with-code` · fil `papers-with-code-development`  
**Dernier événement :** - · 0 depuis une date - · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Papers with Code est une relance, hébergée par Hugging Face, de l'ancien index de recherche destiné aux praticiens qui doivent trouver des articles, des implémentations, des tâches, des jeux de données et des résultats d'évaluation.

- Découverte d'articles pour trouver des publications et les implémentations associées.
- Pages de tâches et de benchmarks pour naviguer parmi les jeux de données et les métriques.
- Classements multi-métriques pour comparer les performances des modèles.
- Liens vers le code pour examiner les implémentations de référence.
- Soumissions de résultats pour ajouter des articles et du code à l'index.

Le catalogue s'enrichit en continu, avec un enrichissement automatisé pour certaines parties de l'index. Un rang dans un classement réduit l'ensemble des candidats, mais ne prouve pas qu'un résultat sera reproductible dans un environnement cible.

## Ligne de développement {#development-line}

- L'entrée datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-05-19 : Papers with Code est devenu disponible sur le nouveau domaine paperswithcode.co peu après sa relance. Une mise à jour du mainteneur datée du 24 mai situe le lancement une semaine plus tôt. Le lien daté seul ne préserve pas l'affirmation d'origine, mais les éléments disponibles indiquent le service relancé plutôt qu'une mise à jour de l'ancien domaine .com.
- 2026-05-24 : Ajout de tableaux de benchmarks multi-métriques, de soumission d'articles externes, de généalogie des articles, de pages de méthodes, d'export d'images de classements et d'environ 3 000 évaluations.
- 2026-06-22 : Ajout de badges SOTA pour les trois meilleurs scores de benchmarks, de résultats d'évaluations tierces, ainsi que de tâches et de benchmarks supplémentaires. Le score de tendance prend désormais aussi en compte l'activité sur les artefacts Hugging Face liés.

## Mode d'emploi {#how-to-use-this}

Au 2026-05-19, aucune modification de pratique ne peut être établie à partir du seul lien daté vers la page d'accueil de Papers with Code.

1. Ouvrez la page d'accueil, recherchez ou parcourez par tâche de recherche, puis ouvrez les pages des articles candidats et leurs implémentations associées.
  — <https://paperswithcode.co/>
2. Comparez les modèles sur la tâche ou le benchmark pertinent ; lisez chaque métrique plutôt que de vous fier à un rang unique.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
3. Soumettez un article arXiv, un dépôt, un billet de blog ou un autre article externe pris en charge via la page de soumission lorsque vous ajoutez des travaux à l'index.
  — <https://paperswithcode.co/submit>
4. Utilisez le catalogue des tâches pour découvrir des benchmarks et vérifier si le résultat rapporté par un article est issu de ses auteurs ou d'une évaluation externe.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Bonnes pratiques {#best-practices}

- Comparez la précision avec la métrique d'efficacité qui l'accompagne lorsque le benchmark expose plusieurs métriques ; par exemple, WER avec RTFx, ou mAP avec FPS.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
- Considérez le flux des tendances comme un outil de découverte, et non comme un classement de qualité : son score intègre la vitesse d'obtention d'étoiles GitHub et l'activité sur les artefacts Hugging Face liés.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>
- Séparez les résultats produits par les auteurs de l'article des évaluations tierces avant d'utiliser un chiffre de classement pour une décision technique.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Remplacé par ce qui suit {#superseded-by-this}

- Avant le 2026-05-24 : les consignes qui considèrent le catalogue historique de Papers with Code comme seule interface actuelle sont obsolètes ; le service actif est paperswithcode.co et accepte des soumissions au-delà d'arXiv.
- Avant le 2026-06-22 : les consignes qui n'attendent que des évaluations introduites par les articles sont incomplètes, car le service relancé affiche aussi des évaluations externes.

## Points encore inconnus {#still-unknown}

- Le contenu de l'entrée du 2026-05-19 n'est pas disponible ; il est impossible de reconstituer l'affirmation exacte formulée à cette date à partir de son seul URL.
- Le site maintenu confirme que la relance a eu lieu environ une semaine avant le 2026-05-24, tandis qu'un billet de lancement à la première personne est daté du 2026-05-18 ; la mise à jour disponible émanant des auteurs n'établit pas un horodatage unique et précis du lancement.
- Aucune source primaire examinée ici ne précise une politique formelle de vérification ni une garantie de couverture pour chaque enregistrement enrichi automatiquement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://paperswithcode.co/ | Papers with Code — Trending research and open source | 2026-09-05 |
| https://huggingface.co/blog/nielsr/paperswithcode-launch | Relaunching PapersWithCode with new features | 2026-09-05 |
| https://huggingface.co/blog/nielsr/updates-to-pwc | New updates to Papers with Code | 2026-09-05 |
| https://paperswithcode.co/submit | Papers with Code submission page | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:papers-with-code`, fil `papers-with-code-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-05-19, aucune modification de pratique ne peut être établie à partir du seul lien daté vers la page d'accueil de Papers with Code.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
