---
title: "LoRA de colorisation de manga FLUX.2 Klein 9B — LoRA de colorisation de manga par référence"
category: projects
date: 2026-06-10
tags: [flux-2-klein-9b-manga-colorization-by-reference-lora, flux-lora, manga-colorization-by-reference-lora, project]
aliases: ["FLUX.2 Klein 9B Manga Colorization LoRA"]
level: 2
source_sha256: 1ce3f35c1e27dc6e59c8e9423cbb09842c1ae4ec469f88b3d09c4a9b97350e96
translation: machine
translated_at: '2026-10-24'
---
# LoRA de colorisation de manga FLUX.2 Klein 9B — LoRA de colorisation de manga par référence {#flux2-klein-9b-manga-colorization-lora-manga-colorization-by-reference-lora}

**Ligne de développement :** `project:flux-2-klein-9b-manga-colorization-by-reference-lora` · fil `manga-colorization-by-reference-lora`  
**Dernier événement :** 2026-06-10 · 1 daté depuis le 2026-06-10 · **Recherche :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Le LoRA de colorisation de manga FLUX.2 Klein 9B est un adaptateur LoRA destiné aux artistes et aux utilisateurs de ComfyUI ou de Diffusers qui souhaitent transférer les palettes de personnages depuis une image couleur de référence vers des planches au trait ou en niveaux de gris.

- Correspondance de palette pour les cheveux, les yeux, les vêtements et les teintes de peau.
- Prise en charge de plusieurs personnages à partir d'une seule image de référence.
- Indications de prompt pour les ajustements d'éclairage et d'arrière-plan.

## Ligne de développement {#development-line}

- **2026-06-10 — Référence du modèle Hugging Face enregistrée pour le projet.** Nous avons enregistré le dépôt de modèle Hugging Face du LoRA de colorisation de manga FLUX.2 Klein 9B par référence le 2026-06-10.

## Ce qui a changé {#what-changed}

2026-06-10 — Le dépôt initial de l'adaptateur sous licence Apache-2.0 a été publié pour FLUX.2 Klein 9B Base ; il définit le déclencheur `mngclranm` et précise le modèle de base. 2026-07-05 — Un workflow ComfyUI tiers a montré la colorisation par lots d'un dossier de pages à partir d'une image couleur de référence distincte ; il s'agit d'une intégration communautaire, et non d'une nouvelle version du LoRA.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-10, considérez le LoRA Hugging Face lié comme un workflow de référence. Vérifiez ses capacités, sa compatibilité, sa licence et ses instructions d'utilisation avant de l'adopter.

1. Chargez `black-forest-labs/FLUX.2-klein-base-9B`, puis connectez les poids de l'adaptateur avec `load_lora_weights` ou Load LoRA dans ComfyUI.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
2. Fournissez la planche en noir et blanc comme image cible et une fiche de personnage, une couverture ou une page de titre colorée distincte comme référence.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
3. Ajoutez `mngclranm` au prompt ; ajoutez des notes sur l'éclairage, l'ambiance ou l'arrière-plan si nécessaire.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
4. Commencez avec un poids LoRA de 0,8 à 1,0 ; réduisez-le si le transfert de couleurs devient excessif.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>

## Bonnes pratiques {#best-practices}

- Choisissez une référence propre où les personnages de la planche sont clairement visibles ; une couverture ou une fiche de personnage convient pour plusieurs personnages.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
- Si les couleurs des personnages se mélangent, changez d'abord le seed ; puis nettoyez la référence ou découpez la planche en cases plus petites.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>
- Dans ComfyUI, gardez la page cible plus grande que la référence : une exécution d'environ 1,5 MP face à une référence de 0,5 MP a réduit la contamination de composition entre les images lors de tests communs.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour le moment.

## Points encore inconnus {#still-unknown}

- La fiche du dépôt décrit un workflow à deux images de référence, mais son exemple générique de widget Diffusers ne montre qu'une seule image d'entrée ; l'appel public exact de Diffusers permettant de fournir la seconde image de référence couleur n'y est pas documenté.
- Aucun journal des modifications officiel ni aucune révision ultérieure du modèle n'a été trouvé après le commit initial du 2026-06-10 ; l'élément du 2026-07-05 constitue une preuve issue d'un workflow communautaire, et non une version du LoRA.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | 2026-09-05 |
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA/commit/78d5314569e7fdc7fb14dabde2281fd82db61304 | initial commit · thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA at 78d5314 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training — Black Forest Labs | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/ | [ComfyUI] Manga Colorization with Color Reference | One-Click Batch Processing | Fast & Consistent Results | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:flux-2-klein-9b-manga-colorization-by-reference-lora`, fil `manga-colorization-by-reference-lora`, 1 événement daté du 2026-06-10 au 2026-06-10.
- **Note pratique :** Au 2026-06-10, les praticiens devraient considérer le LoRA Hugging Face lié comme une référence candidate pour les workflows de colorisation de manga, tout en vérifiant de manière indépendante ses capacités, sa compatibilité, sa licence et ses instructions d'utilisation avant de l'adopter.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
