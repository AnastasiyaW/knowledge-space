---
title: "Canon UltraReal"
category: projects
date: 2026-07-19
tags: [canon-ultrareal, canon-ultrareal-public-model-listing, project]
aliases: ["Canon UltraReal"]
level: 2
source_sha256: 5cd58ca0f6f7196ab1666dc6da2a1bc1dd4369e5b617b13fcc298d7ec6dc3190
translation: machine
translated_at: '2026-10-24'
---
# Canon UltraReal {#canon-ultrareal}

**Ligne de développement :** `project:canon-ultrareal` · fil `canon-ultrareal-public-model-listing`  
**Dernier événement :** 2026-07-19 · 1 événement daté depuis le 2026-07-19 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Canon UltraReal est un LoRA sous licence Apache-2.0 destiné aux workflows text-to-image avec Krea-2-Raw, entraîné sur des photographies prises avec un Canon 1Ds. D'une taille de 114 Mo, il ajuste le rendu des couleurs, la séparation des sujets et le bokeh pour les focales de 28 mm, 50 mm, 100 mm et 500 mm. Il fonctionne comme un adaptateur de rendu photographique ciblé, et non comme un checkpoint autonome ni comme un modèle de réalisme général.

## Ligne de développement {#development-line}

- **2026-07-19 — Canon UltraReal a été publiquement référencé sur Civitai et Hugging Face.** Civitai et Hugging Face ont ajouté des pages publiques pour le modèle le 2026-07-19. Il s'agit d'une étape de diffusion publique pour le projet, même si la source ne mentionne ni version, ni modification des poids, ni notes de version, ni texte original du message.

## Modifications {#what-changed}

2026-07-19 — Canon UltraReal est devenu disponible en tant que LoRA pour Krea-2-Raw ; la fiche modèle principale définit le dépôt, le modèle de base, la source d'entraînement (Canon 1Ds) et l'intensité recommandée de 0,8.

Aucune version ultérieure datée séparément n'a été vérifiée. Le seul fichier de poids hébergé est canon_krea2.safetensors (114 Mo ; SHA-256 3295dec59ab1195631fe9b3dd3493ba9c1546056da86179cc3119c4b029420ce).

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-19, utilisez les pages Civitai et Hugging Face liées pour découvrir Canon UltraReal, et vérifiez la version ainsi que les détails d'utilisation directement sur ces ressources.

1. Installez ou mettez à jour Diffusers, Transformers et Accelerate, puis chargez Danrisi/Canon_UltraReal avec DiffusionPipeline sur CUDA ; utilisez bfloat16 si celui-ci est pris en charge.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
2. Définissez Krea-2-Raw comme modèle de base et réglez l'intensité du LoRA à 0,8.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
3. Commencez vos prompts par c2n0n, décrivez la scène et ajoutez des indications de focale comme 28mm ou 50mm.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Bonnes pratiques {#best-practices}

- Commencez avec une intensité LoRA de 0,8 et ajustez-la seulement après avoir comparé les résultats au sujet et à la composition visés.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Choisissez les focales de façon délibérée : les images d'entraînement couvrent 28 mm, 50 mm, 100 mm et 500 mm, si bien que le rendu change selon les indications d'objectif et le cadrage.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Restez sur Krea-2-Raw ; la fiche modèle n'établit pas la compatibilité avec d'autres modèles de base.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Versions remplacées par celle-ci {#superseded-by-this}

- Aucune version marquée comme obsolète pour le moment.

## Inconnues {#still-unknown}

- L'URL du miroir Civitai pour l'événement du 2026-07-19 n'a pas pu être chargée ; les métadonnées de version, l'horodatage de publication et les indications de workflow ne sont donc pas vérifiés.
- Aucune source de première main ne correspond directement à l'horodatage de publication du 2026-07-19. La fiche modèle principale confirme le périmètre technique et le modèle de base, mais pas l'enregistrement exact du jour de sortie.
- Le schéma de sortie ne comporte pas les champs event_findings et new_events ; les éléments relatifs aux événements figurent donc dans les sections what_changed et unknowns.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/Danrisi/Canon_UltraReal | Danrisi/Canon_UltraReal · Hugging Face | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/blob/main/canon_krea2.safetensors | canon_krea2.safetensors · Danrisi/Canon_UltraReal | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/commit/847c2a1cc7e191f5b3d4451deec984044f4ceabc | Mise à jour du modèle via HuggingFace Uploader · Danrisi/Canon_UltraReal | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:canon-ultrareal`, fil `canon-ultrareal-public-model-listing`, 1 événement daté du 2026-07-19 au 2026-07-19.
- **Note pratique :** À partir du 2026-07-19, les praticiens doivent utiliser les pages Civitai et Hugging Face liées comme points de découverte publics enregistrés pour Canon UltraReal, tout en vérifiant la version exacte et les détails d'utilisation directement sur ces ressources.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
