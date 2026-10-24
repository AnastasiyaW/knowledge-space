---
title: "z-image-turbo-sda — Publication de modèle sur Hugging Face"
category: projects
date: 2026-03-26
tags: [hugging-face-model-release, project, z-image-turbo-sda, z_image_turbo_sda]
aliases: ["z-image-turbo-sda"]
level: 2
source_sha256: 7c3f5d73dbe3714f5f4d9ed191408311d588f1bbfd8a153fe1a950467cb62efa
translation: machine
translated_at: '2026-10-24'
---
# z-image-turbo-sda — Publication de modèle sur Hugging Face {#z-image-turbo-sda-hugging-face-model-release}

**Ligne de développement :** `project:z-image-turbo-sda` · fil `hugging-face-model-release`  
**Dernier événement :** 2026-03-26 · 1 événement daté depuis le 2026-03-26 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Description {#what-it-is}

Z-Image-Turbo-SDA est un adaptateur LoKr/LyCORIS tiers destiné aux utilisateurs de Tongyi-MAI/Z-Image-Turbo, et non un point de contrôle Z-Image autonome.

- Se charge dans le pipeline Turbo pour faire varier la pose, l'angle de caméra et la mise en page d'un seed à l'autre.
- Conserve un flux de travail en 8 étapes, avec un compromis signalé entre diversité et anatomie.

## Ligne de développement {#development-line}

- **2026-03-26 — z-image-turbo-sda a été relié à un dépôt de modèle Hugging Face.** Z-Image-Turbo-SDA était référencé comme un adaptateur déjà publié. Aucun commit du dépôt n'est enregistré à cette date.

## Modifications {#what-changed}

- 2026-03-11 : le dépôt a téléversé `zit_sda_v1.safetensors` et documenté un adaptateur LoKr pour Tongyi-MAI/Z-Image-Turbo.
- 2026-03-26 : Z-Image-Turbo-SDA était référencé comme un adaptateur déjà publié ; aucun commit n'est enregistré à cette date.
- 2026-04-09 : deux commits intitulés `Update README.md` ont modifié la documentation, et non l'artefact de poids public.
- 2026-05-12 : le mainteneur a reconnu des problèmes de compatibilité avec certains modèles ZIT dérivés et a indiqué une alternative distincte, ne contenant que le code.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-26, nous considérons le dépôt Hugging Face F16/z-image-turbo-sda comme la référence de distribution de z-image-turbo-sda. Vérifiez sa fiche de modèle, ses fichiers, sa licence et sa compatibilité avant utilisation.

1. Commencez par la base exacte `Tongyi-MAI/Z-Image-Turbo`. SDA est un adaptateur, et non un checkpoint qui se charge seul.
  — <https://huggingface.co/F16/z-image-turbo-sda>
2. Dans une configuration Diffusers sur CUDA, chargez la base en float16, puis chargez `F16/z-image-turbo-sda` avec `pipeline.load_lora_weights(..., adapter_name="sda_diversity")`. La fiche recommande une version récente de `diffusers` ainsi que `peft`.
  — <https://huggingface.co/F16/z-image-turbo-sda>
3. Reproduisez d'abord l'exécution de référence fournie : 8 étapes d'inférence, CFG 1.0 et une grille fixe de seeds. Évaluez la variation sur l'ensemble de la grille plutôt que sur une seule sortie.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Bonnes pratiques {#best-practices}

- Validez SDA seul avant de cumuler d'autres LoRA Z-Image-Turbo. Si un cumul est nécessaire, le mainteneur suggère de réduire le poids de SDA à 0,5–0,7 et d'accepter une diversité moindre.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Effectuez un test A/B multi-seeds avec des prompts simples et des prompts à contraintes spatiales, puis inspectez les poses complexes à la recherche d'erreurs anatomiques. La fiche précise que les prompts contraints laissent moins de marge aux changements de composition.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Conservez le préréglage de la fiche de l'adaptateur (8 étapes, CFG 1.0) séparé de la recette officielle de la base. La recette officielle spécifie ZImagePipeline, bf16, 9 étapes de scheduler pour 8 passes DiT et CFG 0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- Considérez les gains LPIPS et les pourcentages de récupération de diversité annoncés comme des résultats du mainteneur, et non comme des benchmarks reproduits de manière indépendante.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Aucun code d'entraînement public, aucune provenance de jeu de données, aucun condensat immuable du checkpoint d'entraînement, aucune version minimale de `diffusers`/`peft` ni aucun flux de travail ComfyUI pris en charge n'ont été trouvés.
- Les valeurs LPIPS de la fiche et les taux revendiqués de récupération de diversité, 70,2 % et 58 %, sont rapportés par le mainteneur et n'ont pas été validés de manière indépendante.
- Aucune activité publique du dépôt n'établit une nouvelle version de SDA exactement le 2026-03-26. Cette date identifie un artefact existant, et non une mise à jour démontrée des poids.
- Aucun élément ne montre que Tongyi-MAI a créé, approuvé ou maintient cet adaptateur.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/F16/z-image-turbo-sda | Fiche de modèle F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/commits/main | Historique des commits · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/2557329bb6c6b23fdf846f3f21ab42d4f8df523e/README.md | README.md · F16/z-image-turbo-sda à la révision 2557329 | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/main/zit_sda_v1.safetensors | zit_sda_v1.safetensors · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/discussions/5 | Pourquoi l'application de ce LoRA à certains modèles ZIT casse-t-elle l'image ? | 2026-09-06 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Fiche de modèle Tongyi-MAI/Z-Image-Turbo | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:z-image-turbo-sda`, fil `hugging-face-model-release`, 1 événement daté du 2026-03-26 au 2026-03-26.
- **Note pratique :** À partir du 2026-03-26, nous considérons le dépôt Hugging Face F16/z-image-turbo-sda comme la référence de distribution de z-image-turbo-sda. Vérifiez sa fiche de modèle, ses fichiers, sa licence et sa compatibilité avant utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
