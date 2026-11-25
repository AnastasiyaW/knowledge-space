---
title: "Sol-Attn"
category: projects
date: 2026-08-03
tags: [project, sana, sol-attn, sol-attn-development]
aliases: ["Sol-Attn"]
level: 2
source_sha256: 747603d60cfce7b1ebcbca2de0fd076a19d90fb090b9c86a75c3035834607262
translation: machine
translated_at: '2026-10-24'
---
# Sol-Attn {#sol-attn}

**Ligne de développement :** `project:sol-attn` · fil `sol-attn-development`  
**Dernier événement :** 2026-08-03 · 1 daté depuis le 2026-08-03 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Sol-Attn : méthode d'attention par blocs creux de NVIDIA, appliquée à l'inférence, pour les transformeurs de diffusion pré-entraînés.

- achemine les blocs clé/valeur pendant le softmax en ligne, au lieu de construire une carte proxy séparée ;
- calcule exactement les blocs sélectionnés et approxime la contribution des blocs ignorés ;
- s'utilise pour l'auto-attention de la génération visuelle, tandis que l'attention croisée peut rester dense.

Limite : l'implémentation publiée sur B200 ne prend en charge que l'inférence en passe avant et a été évaluée sur la génération visuelle par diffusion bidirectionnelle, et non sur la vidéo autorégressive. Verdict : à utiliser comme option d'accélération propre à un modèle et à un matériel donnés, et non comme garantie directe des accélérations publiées.

## Ligne de développement {#development-line}

- **2026-08-03 — Page projet de Sol-Attn et branche d'implémentation référencées.** Le facteur 3,95× concerne l'ensemble de la pile, tandis que l'ajout de Sol-Attn après la fusion des noyaux a fait passer le résultat cumulé de 1,394× à 1,534×. Le modèle est MiniMax-H3, un générateur omni-modal vidéo et audio de 33B paramètres.

## Ce qui a changé {#what-changed}

2026-07-27 — l'article sur Sol-Attn a été publié, définissant le routage à seuil dépendant de la requête, le calcul creux en une seule passe avec softmax en ligne, et la correction par score proxy. 2026-07-28 — NVIDIA a publié le code de Sol-Attn avec des noyaux SM89, SM90, SM100 et SM120 ; les résultats de bout en bout de Sol-Engine annoncés à l'époque comprenaient environ 5,03× pour HunyuanVideo-13B et 3,48× pour Wan2.1-T2V-14B. 2026-08-03 — la prise en charge de MiniMax-H3 est devenue une recette Sol-Engine mesurée sur huit GPU GB200 : le facteur 3,95× concerne l'ensemble de la pile, tandis que l'ajout de Sol-Attn après la fusion des noyaux a fait passer le résultat cumulé de 1,394× à 1,534×. Le modèle est MiniMax-H3, un générateur omni-modal vidéo et audio de 33B paramètres. 2026-08-06 — les recettes MiniMax-H3 ont été étendues au DGX Spark et à la RTX 5090, avec des résultats annoncés pour la pile complète de 3,92× et 4,52× respectivement. 2026-08-13 — les recettes LTX-2.5 ont intégré Sol-Attn sur B200, RTX 5090 et DGX Spark ; NVIDIA a annoncé jusqu'à 4,68× pour son pipeline multi-étapes et 1,90× pour son pipeline distillé. 2026-08-17 — un noyau Sol-Attn CuTe DSL optimisé pour SM89 a été ajouté pour la RTX 4090 ; NVIDIA a annoncé 4,44× de bout en bout pour la recette MiniMax-H3 complète. 2026-08-22 — « MiniMax-H3 Super Acceleration » a combiné un brouillon H3 en quatre étapes avec trois étapes de raffinement LTX-2.5 ; NVIDIA a annoncé 22,2× pour une vidéo de cinq secondes en 768p et 27,7× pour une vidéo de dix secondes sur un GB200.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-03, les praticiens doivent considérer Sol-Attn comme une ligne de développement distincte de Sana et consulter la page projet et la branche `sol-engine` indiquées avant de l'évaluer ou de l'adopter ; son statut de publication et ses affirmations techniques doivent encore être vérifiés.

1. Vérifiez que l'auto-attention visée est en BF16 avec une dimension de tête de 128 et que l'environnement d'exécution prévu est CUDA ; SGLang documente Sol-Attn comme étant limité à CUDA dans son backend de diffusion.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
2. Installez le paquet amont depuis la branche `sol-engine` du dépôt NVlabs Sana.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
3. Sélectionnez explicitement `sol_attn` et configurez `tau`, le nombre d'étapes et de couches de préchauffage dense, les puits KV de préfixe exacts lorsque les tokens de conditionnement les requièrent, ainsi que `kv_splits=auto` pour les longues séquences.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
4. Exécutez le modèle cible exact, avec la même résolution, la même durée, le même mélange de prompts et le même GPU, face à une référence dense ; comparez la qualité des sorties et la latence de bout en bout avant d'adopter la configuration.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Bonnes pratiques {#best-practices}

- Gardez les premières étapes de débruitage et les premières couches sélectionnées en mode dense ; conservez les tokens de préfixe texte ou audio comme puits KV exacts lorsque le modèle en a besoin.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Augmentez `tau` avec prudence : un seuil plus élevé sélectionne moins de blocs KV exacts et accroît l'approximation.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Ajustez les réglages en fonction du modèle déployé, du matériel, de la résolution, de la durée et de la pile d'accélération ; NVIDIA indique que les réglages ne se transposent pas de façon fiable d'une combinaison à l'autre.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-03 — considérer le résultat annoncé de 3,95× pour MiniMax-H3 comme dû à Sol-Attn seul est obsolète : la décomposition de NVIDIA attribue 1,394× à la fusion des noyaux et à la capture de graphe, 1,534× après l'ajout de Sol-Attn, et 3,95× seulement après la mise en cache inter-étapes.
- 2026-08-03 — supposer qu'une recette d'accélération préserve la qualité du seul fait qu'elle est sans entraînement est obsolète : le préréglage « super-efficient » de NVIDIA active Sol-Attn pour un gain supplémentaire de 1,25×, mais annonce une distance perceptuelle plus élevée que son préréglage préservant la qualité.

## Points encore inconnus {#still-unknown}

- Les deux liens de l'événement source sont des pages courantes non datées ; le contenu visible par les lecteurs le 2026-08-03 ne peut donc pas être reconstitué à partir d'eux seuls. La page MiniMax-H3 datée de NVIDIA fournit la correction et le périmètre propres à cet événement.
- La documentation actuelle de SGLang décrit son intégration `sol_attn` comme limitée à CUDA ; elle n'établit pas la couverture matérielle de chaque intégration directe ou communautaire du paquet amont.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://nvlabs.github.io/Sana/Sol-Attn/ | Sol-Attn | Sparsification de l'attention à la volée | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana — branche sol-engine | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3/ | Déployer MiniMax-H3 avec Sol Engine : accélération de 3,95× en 4,5 heures d'optimisation | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/ | Déployer MiniMax-H3 sur DGX Spark et RTX 5090 avec Sol Engine : accélération de 4,52× | 2026-09-05 |
| https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx | Backends d'attention de diffusion SGLang | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:sol-attn`, fil `sol-attn-development`, 1 événement daté, du 2026-08-03 au 2026-08-03.
- **Note pratique :** À partir du 2026-08-03, les praticiens doivent considérer Sol-Attn comme une ligne de développement distincte de Sana et consulter la page projet et la branche `sol-engine` indiquées avant de l'évaluer ou de l'adopter ; son statut de publication et ses affirmations techniques doivent encore être vérifiés.
- **Confiance :** élevée. Les mises à jour datées ci-dessus font foi pour ce qui est devenu obsolète.
