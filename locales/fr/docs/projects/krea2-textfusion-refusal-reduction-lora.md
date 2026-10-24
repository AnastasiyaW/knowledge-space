---
title: "Krea2 TextFusion Refusal-Reduction LoRA"
category: projects
date: 2026-07-15
tags: [krea2-textfusion-refusal-reduction-lora, krea2_textfusion_refusal_reduction_lora, project]
aliases: ["Krea2 TextFusion Refusal-Reduction LoRA"]
level: 2
source_sha256: 55eb35f5579b272b07abbabde6fd01e5d42d12c808974d03255c0fa47b31e538
translation: machine
translated_at: '2026-10-24'
---
# Krea2 TextFusion Refusal-Reduction LoRA {#krea2-textfusion-refusal-reduction-lora}

**Ligne de développement :** `project:krea2-textfusion-refusal-reduction-lora` · fil `krea2-textfusion-refusal-reduction-lora`  
**Dernier événement :** 2026-07-15 · 1 événement daté depuis le 2026-07-15 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Krea2 TextFusion Refusal-Reduction LoRA — LoRA de rang 64 pour Krea 2, destinée à réduire la suppression des concepts déjà connus du modèle de base. — modifie l'attention et le MLP dans quatre blocs TextFusion ; — n'ajoute pas de styles, de personnages ni de nouveaux concepts visuels ; — ne modifie pas le transformeur d'images, le txtmlp ni le projecteur de tap 1×12. La version actuellement disponible est la v2.0 ; la force recommandée publiquement est de 0.75–1.00.

## Ligne de développement {#development-line}

- **2026-07-15 — Référence Civitai enregistrée pour Krea2 TextFusion Refusal-Reduction LoRA.** LoRA de rang 64 réservée au routage TextFusion pour Krea 2 ; une copie indépendante de la description confirme les quatre blocs cibles et la force 1.00, mais ne donne pas de date de publication propre, il ne s'agit donc pas d'un complément daté à l'événement.

## Ce qui a changé {#what-changed}

2026-07-15 — publication de la branche v1.0 : LoRA de rang 64 réservée au routage TextFusion pour Krea 2 ; une copie indépendante de la description confirme les quatre blocs cibles et la force 1.00, mais ne donne pas de date de publication propre, il ne s'agit donc pas d'un complément daté à l'événement. 2026-08-29 — v2.0 : annonce d'un meilleur respect du prompt et de textures moins lissées ; plage recommandée 0.75–1.00, 1.50 signalée comme fonctionnelle mais non recommandée.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-07-15, les praticiens doivent utiliser la page Civitai liée comme référence de découverte de cette LoRA, et vérifier sur cette page la version actuelle, la licence et les conditions d'utilisation avant adoption ; les éléments disponibles n'étayent aucune recommandation opérationnelle plus forte.

1. Préparez un workflow local Krea 2 Turbo dans ComfyUI, et installez les poids de base, l'encodeur de texte Qwen3VL et le VAE selon le schéma officiel.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
2. Téléchargez le fichier LoRA, placez-le dans `ComfyUI/models/loras/`, sélectionnez ce fichier dans le nœud LoRA de Krea 2 et activez la LoRA.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
3. Pour la v2.0, commencez avec une force de 0.75–1.00 ; comparez le résultat avec le même seed sans LoRA avant de modifier le sampler ou le prompt.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Bonnes pratiques {#best-practices}

- N'utilisez pas cet adaptateur comme LoRA de style ou de concept : il est présenté pour le routage TextFusion, et non pour ajouter des notions visuelles apprises.
  — <https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora>
- Gardez le workflow Krea 2 de base reproductible : utilisez le modèle officiel et activez la LoRA via un interrupteur séparé, afin de pouvoir vérifier sa contribution.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
- Ne passez pas directement la v2.0 à 1.50 : la page de téléchargement signale cette valeur comme non recommandée.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-29 : pour la v2.0, l'ancienne recommandation de la v1.0 « strength 1.00 » est remplacée par la plage de départ actuelle de 0.75–1.00 ; cela concerne le réglage, et non la disparition de la v1.0.

## Inconnues restantes {#still-unknown}

- La fiche Civitai principale ne s'est pas ouverte lors de la vérification ; sa date de publication initiale et la description de l'auteur pour la v1.0 ne sont donc pas confirmées directement.
- Aucun changelog indépendant et daté reliant la v2.0 à la même publication de l'auteur n'a été trouvé ; seuls le nom et l'identifiant de modèle Civitai dans le lien de la page v2.0 concordent.
- Le schéma de réponse ne contient pas de champs distincts event_findings et new_events : les informations datées figurent dans what_changed.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://civitai.com/models/2775340/krea2-textfusion-refusal-reduction-lora | Krea2 TextFusion Refusal-Reduction LoRA | Civitai | 2026-09-05 |
| https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | 2026-09-05 |
| https://tungsten.run/model/GJjkvTwp3m | Krea2 TextFusion Refusal-Reduction v2.0 | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/krea/krea-2 | Krea 2 | ComfyUI Documentation | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:krea2-textfusion-refusal-reduction-lora`, fil `krea2-textfusion-refusal-reduction-lora`, 1 événement daté, du 2026-07-15 au 2026-07-15.
- **Note pratique :** Depuis le 2026-07-15, les praticiens doivent utiliser la page Civitai liée comme référence de découverte de cette LoRA, et vérifier sur cette page la version actuelle, la licence et les conditions d'utilisation avant adoption ; les éléments disponibles n'étayent aucune recommandation opérationnelle plus forte.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
