---
title: "ComfyUI Sol-Attn — implémentations Blackwell et Triton"
category: projects
date: 2026-08-07
tags: [blackwell-and-triton-implementations, comfyui-sol-attn, project]
aliases: ["ComfyUI Sol-Attn"]
level: 2
source_sha256: d828905bfe197d0eef8806ead92d5e95ed41d4bf65021e31877193f042a1ad5b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Sol-Attn — implémentations Blackwell et Triton {#comfyui-sol-attn-blackwell-and-triton-implementations}

**Fil de développement :** `project:comfyui-sol-attn` · thread `blackwell-and-triton-implementations`  
**Dernier événement :** 2026-08-07 · 1 événement daté depuis 2026-08-07 · **Recherche :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

ComfyUI Sol-Attn désigne de façon générique deux extensions communautaires pour ComfyUI, qui remplacent l'attention de MiniMax H3 par une variante clairsemée de Sol-Attn. — Kijai : variante Triton expérimentale, annoncée comme testée avec MiniMax H3 sur RTX 4090 et RTX 5090. — KingGore : variante pour RTX 5090 (SM120), utilisant PyTorch flex_attention. Limite : la mesure de KingGore donne 1,46× sur 4K et 9,00× sur 32K tokens par rapport à SDPA après échauffement, uniquement pour sa configuration MiniMax H3 / RTX 5090. Verdict : c'est un outil pour la comparaison A/B de rendus H3 longs, et non un accélérateur ComfyUI universel.

## Fil de développement {#development-line}

- **2026-08-07 — Les implémentations ComfyUI Sol-Attn pour Blackwell et Triton ont été référencées.** Variante Triton de Kijai et variante Blackwell de KingGore.

## Ce qui a changé {#what-changed}

2026-07-27 — publication de la première version du travail Sol-Attn : attention clairsemée sans entraînement, avec correction des blocs omis. 2026-07-28 — NVIDIA a publié les noyaux Sol-Attn en amont pour SM89/SM90/SM100/SM120 ainsi que les intégrations HunyuanVideo-13B et Wan2.1-T2V-14B. 2026-08-04 — KingGore a ajouté une v2 avec attention exacte pour le préfixe de conditionnement et étapes finales denses ; Kijai a accepté une correction d'import pour les GPU antérieurs à SM90. 2026-08-06 — Sol-Engine en amont a ajouté MiniMax H3 sur GB10 et RTX 5090 ; ce n'est pas une publication de nœud ComfyUI. 2026-08-07 — la branche ComfyUI a référencé deux implémentations indépendantes : la variante Triton de Kijai et la variante Blackwell de KingGore. 2026-08-17 — Sol-Engine en amont a ajouté un noyau SM89 optimisé pour RTX 4090 ; la compatibilité du nœud Kijai reste une question propre à ce nœud.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-07, les praticiens qui évaluent ComfyUI Sol-Attn doivent distinguer l'implémentation ciblant Blackwell de celle ciblant Triton, et vérifier la compatibilité de leur environnement avant d'adopter l'une ou l'autre.

1. Pour MiniMax H3 sur RTX 5090, installez la variante Blackwell dans ComfyUI/custom_nodes et redémarrez ComfyUI ; elle nécessite PyTorch 2.6+ et CUDA 12.x ou 13.x.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
2. Insérez Sol-Attn MiniMax H3 Patcher entre Load Diffusion Model et KSampler.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
3. Commencez avec tau=1.0 ; pour la variante Blackwell, la plage documentée est 0.8–1.5. En cas d'artefacts, activez dense_steps ou step_off pour une fin dense, et exact_kv pour le préfixe de conditionnement exact.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
4. Pour la variante Triton de Kijai, limitez le premier test MiniMax H3 à RTX 4090 ou RTX 5090, puis ajustez start_percent, end_percent et tau avec un seed identique.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>

## Bonnes pratiques {#best-practices}

- Ne mesurez pas la première exécution : la compilation Triton a lieu au premier usage et la rend plus lente.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>
- Comparez la vitesse et l'image sur le même modèle, seed, résolution, nombre d'étapes et GPU : même les mesures en amont fixent toutes ces conditions.
  — <https://github.com/NVlabs/Sana/tree/sol-engine>
- Sur MiniMax H3, gardez les dernières étapes de débruitage denses si l'attention clairsemée introduit une erreur notable ; exact_kv fournit une attention exacte pour le préfixe de conditionnement pour environ 3 % de coût supplémentaire.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-04 — pour KingGore, le mode initial uniquement clairsemé est obsolète : la v2 a ajouté dense_steps/step_off et exact_kv/exact_kv_and_rows pour préserver la qualité de MiniMax H3.
- 2026-08-04 — pour Kijai, il n'est plus nécessaire de subir l'erreur ModuleNotFoundError TensorDescriptor sur les builds Triton antérieurs à SM90 : la correction est acceptée, mais sa confirmation se limite à RTX 3060 et ne garantit pas RTX 20/10.

## Toujours inconnu {#still-unknown}

- ComfyUI Sol-Attn n'est pas un projet unique : Kijai et KingGore sont deux dépôts distincts, avec des backends, une prise en charge GPU et des paramètres différents. Leur compatibilité mutuelle n'est pas documentée.
- Le texte de l'événement du 2026-08-07 n'a pas de contenu disponible ; event_findings reste donc volontairement vide : aucune autre affirmation datée ne peut être honnêtement rattachée à ce jour précis.
- Kijai qualifie le projet de work in progress et ne documente des tests que sur RTX 4090 et RTX 5090 ; la fusion pour RTX 3060 ne prouve pas la prise en charge de tous les GPU antérieurs à SM90.
- Aucune des sources upstream de NVIDIA utilisées ne annonce de nœud ComfyUI officiel ; Sol-Engine et les nœuds communautaires doivent être considérés comme des voies d'intégration distinctes.
- La recherche en chinois n'a pas donné de source primaire en chinois concernant précisément ces deux dépôts.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/kijai/ComfyUI-SolAttn_triton | kijai/ComfyUI-SolAttn_triton | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md | ComfyUI-SolAttn README | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/pull/1 | Kijai pull request #1: pre-SM90 TensorDescriptor import fix | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell | KingGore/ComfyUI_sol-attn_Blackwell | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md | KingGore Blackwell README | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/commits/main | KingGore Blackwell commit history | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Attn/ | NVIDIA Sol-Attn project page | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana sol-engine branch | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:comfyui-sol-attn`, thread `blackwell-and-triton-implementations`, 1 événement daté du 2026-08-07 au 2026-08-07.
- **Note pratique :** Au 2026-08-07, les praticiens qui évaluent ComfyUI Sol-Attn doivent distinguer l'implémentation ciblant Blackwell de celle ciblant Triton, et vérifier la compatibilité de leur environnement avant d'adopter l'une ou l'autre.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
