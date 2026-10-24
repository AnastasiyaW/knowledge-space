---
title: "3DreamBooth"
category: projects
date: 2026-03-21
tags: [3dreambooth, 3dreambooth-development, project]
aliases: ["3DreamBooth"]
level: 3
source_sha256: 7fccec91638e54a5674ee80aa7ab3b37da3ff5443d88dc75d23d7c3ffb0dc52a
translation: machine
translated_at: '2026-10-24'
---
# 3DreamBooth {#3dreambooth}

**Ligne de développement :** `project:3dreambooth` · fil `3dreambooth-development`  
**Dernier événement :** 2026-03-21 · 1 événement daté depuis 2026-03-21 · **Consulté le :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

3DreamBooth est une base de code de recherche permettant d'adapter HunyuanVideo-1.5 à un sujet capturé sous plusieurs points de vue.

- 3DreamBooth : optimisation LoRA par sujet, sur une seule image, pour l'identité spatiale.
- 3Dapter : un adaptateur de conditionnement par image de référence, optimisé conjointement avec la LoRA du sujet.

L'article rapporte des sorties en 720p, 81 images, 50 étapes ; le dépôt public indique toujours que le code d'évaluation n'est pas disponible. Utilisez-le pour une reproduction contrôlée ou une inférence à partir de points de contrôle fournis, et non comme un paquet clé en main pour la production.

## Ligne de développement {#development-line}

- **2026-03-21 — Les ressources du projet 3DreamBooth ont été publiquement liées.** Le 2026-03-21, une entrée a relié le site web du projet 3DreamBooth et son dépôt source GitHub. Nous considérons cela comme un point de référence public pour l'historique du projet. Nous n'inférons aucune version, fonctionnalité ou autre modification non attestée.

## Changements {#what-changed}

- 2026-03-19 — La v1 sur arXiv a présenté 3DreamBooth, 3Dapter et 3D-CustomBench.
- 2026-03-20 — Le dépôt enregistre son commit initial, retire le badge Code Coming Soon et publie les fichiers sources.
- 2026-03-21 — La page du projet et le dépôt ont été liés pour l'événement daté. Nous n'avons pas de vérification indépendante d'une date de lancement officielle.
- 2026-07-22 — Hugging Face a indiqué que le jeu de données 3D-CustomBench avait été mis à jour.
- 2026-07-28 — Hugging Face a indiqué que la collection de points de contrôle 3DreamBooth-CustomBench avait été mise à jour.

## Mode d'emploi {#how-to-use-this}

1. Clonez le dépôt, créez son environnement Python 3.10 et installez les dépendances déclarées.
  — <https://github.com/Ko-Lani/3DreamBooth>
2. Téléchargez HunyuanVideo-1.5, ses dépendances de texte et de vision, ainsi que le 3Dapter pré-entraîné. Obtenez l'accès à FLUX.1-Redux-dev, dont l'accès est restreint, avant de lancer une tâche.
  — <https://github.com/Ko-Lani/3DreamBooth>
3. Pour un essai prêt à l'emploi, téléchargez l'une des 30 paires de points de contrôle conjoints CustomBench et utilisez la phrase de déclenchement exacte, composée de l'identifiant et de la classe.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
4. Pour un sujet personnalisé, préparez des captures multi-vues ordonnées dans `images/` ainsi qu'un ensemble plus réduit de références carrées, sans arrière-plan et normalisées en blanc, dans `references/`.
  — <https://github.com/Ko-Lani/3DreamBooth>
5. Exécutez la configuration YAML fournie avec `--dry-run` en premier, puis utilisez le mode `3dreambooth` de référence ou le mode conjoint, selon le cas.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
6. Gardez une longueur de vidéo générée de la forme 4n + 1, par exemple 49, 81 ou 129 images. Ne considérez pas une exécution visuelle comme une reproduction officielle des métriques tant que le code d'évaluation est absent.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Bonnes pratiques {#best-practices}

- Commencez par un point de contrôle CustomBench fourni avant d'entreprendre un entraînement personnalisé. Cela sépare les erreurs d'environnement et de prompt des erreurs d'entraînement du sujet.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Utilisez des vues et des références variées et ordonnées, couvrant les 360 degrés complets de l'objet. Retirez les arrière-plans des références avant le conditionnement.
  — <https://arxiv.org/html/2603.18524>
- Conservez à l'identique la phrase entre crochets, composée de l'identifiant et de la classe, pendant l'entraînement et la validation. La phrase littérale est l'empan de LoRA qui active l'identité.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Validez la résolution du YAML avec `--dry-run` avant de charger de gros points de contrôle ou de lancer un entraînement distribué.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
- Vérifiez les conditions d'accès à FLUX et les termes de licence dérivés de Hunyuan avant de vous engager dans un flux de travail ou un usage commercial.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-20 — L'état initial Code Coming Soon est obsolète : l'historique du dépôt enregistre sa suppression et la publication des fichiers sources.

## Points inconnus {#still-unknown}

- Nous n'avons trouvé ni tag immuable ni GitHub Release correspondant à l'état exact du code au 2026-03-21 ; nous ne pouvons donc pas figer cette révision à partir des pages publiques consultées.
- Les étiquettes Hugging Face de juillet établissent les dates de mise à jour, mais pas les modifications exactes au niveau des fichiers effectuées à ces dates.
- Nous n'avons effectué aucune installation locale, aucune mesure de mémoire GPU, aucun test de débit et aucune reproduction indépendante des métriques ; le code d'évaluation officiel reste indisponible.
- Nous n'avons trouvé aucune documentation de première main en chinois simplifié ni aucun guide communautaire officiel en chinois ; les indications pratiques actuelles reposent sur des sources primaires en anglais.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ko-lani.github.io/3DreamBooth/ | 3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth | Ko-Lani/3DreamBooth | 2026-09-07 |
| https://arxiv.org/abs/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |
| https://arxiv.org/html/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model — HTML | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/commits/main | Commits · Ko-Lani/3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md | Modes d'entraînement et de validation | 2026-09-07 |
| https://huggingface.co/lanikoworld/3DreamBooth-CustomBench | Points de contrôle 3DreamBooth-CustomBench | 2026-09-07 |
| https://huggingface.co/datasets/lanikoworld/3D-CustomBench | 3D-CustomBench | 2026-09-07 |
| https://huggingface.co/papers/2603.18524 | Page de l'article — 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:3dreambooth`, fil `3dreambooth-development`, 1 événement daté, du 2026-03-21 au 2026-03-21.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les mentions de remplacement datées ci-dessus font autorité pour ce qui est obsolète.
