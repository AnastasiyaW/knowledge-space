---
title: "Alibaba — Recherche sur les modèles génératifs"
category: organizations
tags: [alibaba, alibaba:mofusion, alibaba_latent_to_pixel, generative-model-research, humanomniv2, organization]
aliases: ["Alibaba"]
level: 3
source_sha256: 28bbaa01ab471f806049beba20d436f43945fadea07eb788e4ea2212558d189f
translation: machine
translated_at: '2026-10-24'
---
# Alibaba — Recherche sur les modèles génératifs {#alibaba-generative-model-research}

**Ligne de développement :** `organization:alibaba` · fil `generative-model-research`  
**Événements :** 3 datés, 2022-12-11 → 2026-08-23 · **Recherche effectuée le :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

Alibaba n'est pas un outil d'IA unique, mais un ensemble de résultats de recherche destinés aux équipes R&D : — MoFusion — modèle de diffusion pour text-to-motion, motion completion et mélange de signaux de contrôle. — HumanOmniV2 — modèle open-weight de raisonnement sur images, vidéos et audio, prenant en compte le contexte complet. — Latent-to-pixel — recette d'entraînement d'un modèle text-to-image : d'abord dans l'espace latent, puis dans l'espace pixel. Limite : parmi ces trois travaux, seul HumanOmniV2 publie son code, ses poids et son workflow d'évaluation ; la fiche indique 9B BF16 et l'absence de fournisseur d'inférence hébergée. Verdict : HumanOmniV2 peut être utilisé pour une exécution de recherche en local ; les deux autres travaux servent de bases de recherche, et non de remplacement prêt pour la production.

## Ligne de développement {#development-line}

- **2022-12-11 — La ligne de développement Alibaba a enregistré le projet MoFusion.** Le 2022-12-11, la ligne de développement Alibaba a enregistré un lien vers le projet MoFusion. Ce point est considéré comme une étape de recherche-développement importante, car les preuves archivées identifient un artefact de projet nommé. Les éléments fournis n'établissent pas la formulation, l'auteur ni le statut de déploiement de la publication d'origine.
- **2025-07-09 — La ligne de développement Alibaba a enregistré les ressources de recherche HumanOmniV2.** Le 2025-07-09, la ligne de développement Alibaba a enregistré des liens vers les ressources de recherche HumanOmniV2, notamment une page d'article et un dépôt source. Ce point est considéré comme une étape importante, car les liens datés identifient un artefact de recherche nommé associé à du code. Les preuves archivées n'établissent pas la formulation, l'auteur, les affirmations techniques ni le statut de publication de la publication d'origine.
- **2026-08-23 — La ligne de développement Alibaba a enregistré un article sur Latent-to-Pixel.** Le 2026-08-23, la ligne de développement Alibaba a enregistré un lien vers un article sur Latent-to-Pixel. Ce point est considéré comme une étape de recherche importante dans la ligne des modèles génératifs, et non comme une annonce de mise en production. Les éléments fournis n'établissent pas la formulation, l'auteur, les affirmations techniques ni la disponibilité de la publication d'origine.

## Ce qui a changé {#what-changed}

Les lignes d'Alibaba évoluent en parallèle, et non comme des versions successives d'un même produit. — 2022-12-11 : MoFusion a proposé un Transformer de diffusion unique et pré-entraîné pour la synthèse de mouvements humains, avec cross-attention pour différents contrôles et un adaptateur de squelette. — 2025-07-09 : HumanOmniV2 a ajouté un raisonnement omni-modal centré sur le contexte : récompenses contextuelles et logiques, IntentBench et une pile de recherche ouverte pour les tâches vidéo, audio et image. — 2026-08-23 : un travail sur la diffusion dans l'espace pixel a montré qu'un pré-entraînement direct à grande échelle dans l'espace pixel converge plus lentement ; il propose une transition latent-to-pixel pendant le post-entraînement, avec une accélération annoncée de l'inférence de bout en bout de 3,18 à 4,75 fois. — Constaté aujourd'hui, 2026-09-03 : le dépôt MoFusion est archivé et en lecture seule ; HumanOmniV2 publie ses poids, son code et ses données ; pour l'article 2608.16887, aucun modèle, jeu de données ou Space n'était lié au moment de la vérification.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-23, les praticiens qui suivent Alibaba doivent considérer les artefacts datés MoFusion, HumanOmniV2 et Latent-to-Pixel comme une lignée de recherche, et vérifier chaque article ou dépôt directement avant de l'utiliser comme guide d'implémentation ou de déploiement.

1. Si vous avez besoin d'un artefact fonctionnel de cette lignée, commencez par HumanOmniV2 : clonez le dépôt des auteurs et récupérez les poids via les liens Hugging Face ou ModelScope indiqués.
  — <https://github.com/HumanMLLM/HumanOmniV2>
2. Pour une évaluation reproductible, téléchargez IntentBench, Daily-Omni et WorldSense, indiquez les chemins vers les vidéos et lancez l'évaluation distribuée fournie ; l'exemple utilise 8 processus.
  — <https://github.com/HumanMLLM/HumanOmniV2>
3. Pour l'entraînement, téléchargez les données long-CoT et les jeux de données indiqués, définissez les chemins JSON et vidéo dans les configurations YAML, puis exécutez SFT, RL de l'étape 1 et RL de l'étape 2 dans l'ordre documenté.
  — <https://github.com/HumanMLLM/HumanOmniV2>
4. Pour une nouvelle R&D en text-to-image, utilisez un pré-entraînement dans l'espace latent, puis adaptez séparément le modèle à l'espace pixel ; il s'agit d'une recette d'entraînement, et non d'un point d'inférence prêt à l'emploi publié.
  — <https://arxiv.org/pdf/2608.16887>

## Bonnes pratiques {#best-practices}

- Pour le raisonnement vidéo/audio, constituez d'abord le contexte multimodal complet, puis répondez : ce travail vise spécifiquement les signaux visuels et audio qui sont habituellement omis.
  — <https://arxiv.org/pdf/2506.21277>
- N'évaluez pas HumanOmniV2 sur un seul exemple commode : utilisez IntentBench avec Daily-Omni et WorldSense, après avoir vérifié les chemins vers les vidéos.
  — <https://github.com/HumanMLLM/HumanOmniV2>
- Distinguez les droits sur le code, les poids et les vidéos : le code et le modèle sont annoncés sous Apache-2.0, tandis que les vidéos autocollectées sont sous CC BY-NC-SA 4.0.
  — <https://huggingface.co/PhilipC/HumanOmniV2>
- Considérez IntentBench comme un jeu de données distinct, non commercial et sans dérivés, et vérifiez son autorisation d'usage avant l'entraînement ou toute application commerciale.
  — <https://huggingface.co/datasets/PhilipC/IntentBench>
- Pour le latent-to-pixel, ne traitez pas le noise scale comme une constante théorique : les auteurs ont obtenu le meilleur résultat avec gamma=2 dans leur configuration et exigent explicitement un calibrage empirique.
  — <https://arxiv.org/pdf/2608.16887>

## Remplacé par ce qui suit {#superseded-by-this}

- 2023-02-28 — L'hypothèse selon laquelle MoFusion serait une voie d'implémentation officielle activement maintenue est obsolète : le dépôt est archivé et en lecture seule.
- 2025-07-01 — L'état de HumanOmniV2 « seulement l'article et une partie du code » est remplacé par la publication du code d'entraînement et d'évaluation, des poids, d'IntentBench et des données d'entraînement.
- Il n'est pas établi que MoFusion, HumanOmniV2 et le travail latent-to-pixel se remplacent mutuellement : ce sont des tâches et des modalités différentes, et la migration de l'un à l'autre n'est donc pas une voie de mise à niveau.

## Points encore inconnus {#still-unknown}

- MoFusion, HumanOmniV2 et le travail sur l'espace pixel sont liés par une affiliation commune à Alibaba, mais les sources primaires ne montrent ni modèle, ni API, ni feuille de route produit commune.
- Pour l'article 2608.16887, aucun code officiel, poids, jeu de données ni point de service n'a été trouvé ; la reproductibilité pratique exige une implémentation indépendante.
- HumanOmniV2 publie des workflows d'entraînement et d'évaluation, mais pas de guide de démarrage rapide d'inférence destiné à l'utilisateur final ; l'extrait Transformers générique sur Hugging Face n'a pas été exécuté de manière indépendante.
- La compatibilité actuelle de l'archive MoFusion avec les dépendances récentes et son aptitude à la production ne sont pas confirmées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ofa-sys.github.io/MoFusion/ | MoFusion: Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://github.com/OFA-Sys/MoFusion | OFA-Sys/MoFusion | 2026-09-03 |
| https://arxiv.org/pdf/2212.02837 | Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://huggingface.co/papers/2506.21277 | Page de l'article — HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://arxiv.org/pdf/2506.21277 | HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://github.com/HumanMLLM/HumanOmniV2 | HumanMLLM/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/PhilipC/HumanOmniV2 | PhilipC/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/datasets/PhilipC/IntentBench | PhilipC/IntentBench | 2026-09-03 |
| https://huggingface.co/papers/2608.16887 | Page de l'article — An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |
| https://arxiv.org/pdf/2608.16887 | An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `organization:alibaba`, fil `generative-model-research`, 3 événements datés du 2022-12-11 au 2026-08-23.
- **Note pratique :** Au 2026-08-23, les praticiens qui suivent Alibaba doivent considérer les artefacts datés MoFusion, HumanOmniV2 et Latent-to-Pixel comme une lignée de recherche, et vérifier chaque article ou dépôt directement avant de l'utiliser comme guide d'implémentation ou de déploiement.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
