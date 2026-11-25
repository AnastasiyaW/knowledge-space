---
title: "MMDiT : Transformeur de diffusion multimodal"
description: "MMDiT est le motif de transformeur multimodal de Stable Diffusion 3 : des représentations spécifiques à chaque modalité participent à une attention conjointe ; les API d'implémentation et les noms de modules ciblés par LoRA varient selon la révision du modèle."
category: architectures
tags: [mmdit, transformer, diffusion, attention, architecture, dit, joint-attention, stable-diffusion-3]
aliases: ["Multi-Modal Diffusion Transformer", "MM-DiT"]
level: 3
source_sha256: 74f1dbff8b0ce1e6f17ae1552857415b3920f7b6addadb5edf085de97baabce8
translation: machine
translated_at: '2026-10-24'
---
# MMDiT : Transformeur de diffusion multimodal {#mmdit-multimodal-diffusion-transformer}

**Périmètre vérifié : 2026-09-04.** MMDiT est l'architecture de transformeur de diffusion multimodal introduite avec Stable Diffusion 3. Elle représente les entrées image et langage à l'aide de paramètres spécifiques à chaque modalité, fusionne leurs séquences de tokens pour l'attention, puis poursuit un traitement propre à chaque modalité. Cette frontière d'attention conjointe permet aux représentations de l'image et du texte de s'influencer mutuellement, sans pour autant considérer toute implémentation comme le même modèle ou la même API.

## Conception de base {#core-design}

L'article de recherche sur Stable Diffusion 3 décrit MMDiT comme deux flux de représentation dotés de poids distincts, dont les séquences de tokens se rejoignent au niveau de l'attention. Cela diffère d'une approche où l'encodeur de texte sert de simple source passive de clés et de valeurs pour un transformeur séparé, ne traitant que l'image :

| Aspect | Frontière MMDiT |
|---|---|
| représentation | l'image et le texte conservent des paramètres propres à chaque modalité |
| attention | les flux peuvent échanger de l'information par attention conjointe |
| débruitage | le transformeur multimodal prédit sur des latents d'image encodés |
| implémentation | la configuration, les encodeurs de texte, le format des latents et les noms de blocs dépendent d'une révision précise du modèle |

Cette architecture concerne Stable Diffusion 3. D'autres transformeurs peuvent partager des idées comme les doubles flux ou l'attention conjointe, mais un schéma similaire ou une appellation commerciale ne prouve en rien la compatibilité des paramètres, des points de contrôle ou des adaptateurs.

## L'intégration dépend du modèle {#integration-is-model-specific}

Pour le pipeline SD3 actuel de Diffusers, le composant MMDiT est exposé sous la forme `SD3Transformer2DModel`, aux côtés du VAE, des encodeurs de texte, du scheduler et de la configuration du pipeline. Ces noms de classes et la sémantique de chargement sont des détails d'implémentation, et non une spécification portable.

Avant d'adapter ou d'exploiter un modèle basé sur MMDiT :

1. épinglez la révision du modèle, du pipeline et de la bibliothèque ;
2. inspectez la configuration publiée ainsi que les noms des state dicts et des modules ;
3. utilisez l'adaptateur ou le chargeur LoRA prévu pour ce transformeur exact ;
4. consignez les encodeurs de texte, le VAE de latents, le scheduler, la précision et les paramètres de prompt comme partie intégrante de l'identité de l'exécution ;
5. validez les sorties et le comportement en cas d'échec sur un petit jeu de test avant de lancer un lot de rendus plus large.

Ne recopiez pas une liste figée de modules cibles `to_q` ou `add_q_proj` provenant d'un modèle apparenté à MMDiT. Les noms de modules, les projections, les couches à double flux et les formats d'adaptateurs pris en charge évoluent d'une version à l'autre.

## Les affirmations sur les performances et l'édition doivent être mesurées {#performance-and-editing-claims-need-measurement}

La mémoire et la latence dépendent du nombre de tokens d'image, de la longueur du texte, de la configuration du transformeur, de l'implémentation de l'attention, de la précision et du matériel. Profilez le pipeline exact plutôt que de réutiliser un chiffre de résolution ou de VRAM issu d'un autre modèle. De même, l'attention conjointe peut aider à modéliser le conditionnement, mais elle ne garantit ni un texte exact, ni la préservation de régions, ni la justesse de la composition, ni une édition sûre.

Pour un flux de travail d'édition contrôlable, conservez des preuves distinctes pour :

- la préservation de l'image source ;
- la modification locale demandée ;
- l'exactitude du prompt et de la typographie ;
- la révision de l'adaptateur ou du modèle ;
- la revue des sorties et l'usage de publication autorisé.

## Références {#references}

- [Article de recherche sur Stable Diffusion 3](https://arxiv.org/abs/2403.03206)
- [Présentation de l'architecture MMDiT par Stability AI](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Documentation du transformeur SD3 de Diffusers](https://huggingface.co/docs/diffusers/main/en/api/models/sd3_transformer2d)
- [Documentation du pipeline Stable Diffusion 3 de Diffusers](https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3)
