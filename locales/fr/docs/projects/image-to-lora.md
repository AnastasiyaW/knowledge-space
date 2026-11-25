---
title: "Image-to-LoRA"
category: projects
date: 2026-06-17
tags: [image-to-lora, image-to-lora-v2-release, image_to_lora, project]
aliases: ["Image-to-LoRA"]
level: 2
source_sha256: 59033f2ee5db4d6be07e424fe0ccdd3edfdceaa41acecc78e7642c811a7a9f81
translation: machine
translated_at: '2026-10-24'
---
# Image-to-LoRA {#image-to-lora}

**Ligne de développement :** `project:image-to-lora` · fil `image-to-lora-v2-release`  
**Dernier événement :** 2026-06-17 · 1 événement daté depuis le 2026-06-17 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Image-to-LoRA est la méthode i2L de DiffSynth-Studio qui produit des poids LoRA de style explicites à partir d’une ou plusieurs images de référence, au lieu d’optimiser un nouveau LoRA pour chaque style.

- Transfert de style : génère des poids LoRA de style explicites à partir d’images de référence.
- Fusion multi-références : combine les caractéristiques de style de plusieurs images de référence.
- Composition contrôlée : associe le style cible à des contrôles de génération.

La famille V2 publiée cible trois modèles spécifiques à leur backbone, et chaque modèle i2L ne fonctionne qu’avec son architecture de base correspondante. Utilisez-la pour une instanciation rapide de styles au sein de DiffSynth-Studio, et non comme générateur de LoRA universel pour des interfaces ou des backbones arbitraires.

## Ligne de développement {#development-line}

- **2026-06-17 — La collection publique Image-to-LoRA V2 est devenue une étape publique du projet.** Le 2026-06-17, Image-to-LoRA a publié sur ModelScope une collection publique dédiée à Image-to-LoRA V2. Cette collection sert de point de distribution public du projet à cette date. Les sources disponibles ne précisent pas de modifications techniques, d’auteurs ni de statut de publication au-delà de cette collection liée.

## Évolutions {#what-changed}

- 2025-12-09 — Qwen-Image-i2L a introduit le modèle image-to-LoRA antérieur, avec les notes des mainteneurs sur ses limites de généralisation et de préservation des détails.
- 2026-06-11 — le rapport technique i2L a décrit la prédiction de poids LoRA explicites à partir d’une ou plusieurs références en une seule passe avant.
- 2026-06-15 — Image-to-LoRA V2 a été publié en open source pour Z-Image, FLUX.2-klein-base-4B et HiDream-O1-Image.
- 2026-06-17 — Image-to-LoRA V2 a été rassemblé comme famille de modèles publiée, composée de trois modèles spécifiques à leur backbone, et non d’un LoRA universel unique.

## Mode d’emploi {#how-to-use-this}

À partir du 2026-06-17, utilisez la collection ModelScope liée comme point de référence daté pour localiser et évaluer Image-to-LoRA V2, puis vérifiez séparément sa documentation et son comportement technique.

1. Installez DiffSynth-Studio depuis les sources, puis sélectionnez au besoin le point d’accès ModelScope international ou la source de téléchargement Hugging Face.
  — <https://github.com/modelscope/DiffSynth-Studio>
2. Choisissez le checkpoint V2 correspondant au backbone de génération ; pour Z-Image, chargez `DiffSynth-Studio/ZImage-i2L-v2` avec le pipeline Z-Image et activez le chargement à chaud des LoRA.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
3. Fournissez la liste des images de référence, un prompt de génération et les entrées de modèle négatif correspondantes ; exécutez le modèle dans le pipeline de base pour générer l’image stylisée.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
4. Pour FLUX.2-klein-base-4B, utilisez l’exemple distinct `KleinBase4B-i2L-v2` et son pipeline FLUX.2 correspondant, plutôt que le checkpoint Z-Image.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py>

## Bonnes pratiques {#best-practices}

- Associez exactement le checkpoint i2L et l’architecture de base ; la V2 fournit des checkpoints distincts pour Z-Image, FLUX.2-klein-base-4B et HiDream-O1-Image.
  — <https://github.com/modelscope/DiffSynth-Studio>
- Utilisez une ou plusieurs images de référence qui expriment de manière cohérente le style visé, puis servez-vous du prompt textuel pour la nouvelle scène ou la nouvelle composition ; i2L sépare l’apparence du contenu de référence.
  — <https://arxiv.org/abs/2606.13809>
- Partez de l’exemple d’inférence maintenu, y compris sa configuration de chargement à chaud des LoRA et d’entrée de modèle négatif, avant de modifier le prompt, le nombre de références ou les paramètres d’échantillonnage.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>

## Remplacé par cette version {#superseded-by-this}

- 2025-12-09 — l’état antérieur Qwen-Image-i2L est remplacé, pour les backbones pris en charge par la V2, par la famille V2 ; ne considérez pas ses limites de généralisation et de préservation des détails comme une référence pour la V2.
- 2026-06-15 — la recommandation qui traite Image-to-LoRA comme un modèle unique réservé à Qwen est obsolète : la V2 est une publication de trois checkpoints spécifiques à leur backbone.

## Points non élucidés {#still-unknown}

- La collection ModelScope était accessible, mais n’exposait aucune métadonnée lisible ; sa date de publication et les conditions de licence par checkpoint restent non vérifiées.
- Aucune preuve de première main n’établit un workflow ComfyUI pris en charge, ni ne garantit que les poids peuvent être exportés et utilisés en dehors de DiffSynth-Studio.
- Pour le 2026-06-17, les mises à jour du dépôt datées du 2026-06-15 précisent le périmètre exact de la V2 : `ZImage-i2L-v2`, `KleinBase4B-i2L-v2` et `HidreamO1-i2L-v2` ; le rapport technique a été soumis le 2026-06-11. Événements antérieurs : 2025-12-09, sortie de Qwen-Image-i2L avec les limites annoncées ; 2026-06-11, soumission du rapport technique i2L ; 2026-06-15, passage en open source de la V2. Tous proviennent des sources listées ci-dessus.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://modelscope.ai/collections/DiffSynth-Studio/Image-to-LoRA-V2 | ModelScope — collection DiffSynth-Studio/Image-to-LoRA-V2 | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio | DiffSynth-Studio — dépôt et historique des mises à jour | 2026-09-05 |
| https://arxiv.org/abs/2606.13809 | Compressing Image Style Training into a Single Model Forward | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py | Exemple d’inférence ZImage-i2L-v2 | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py | Exemple d’inférence KleinBase4B-i2L-v2 | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:image-to-lora`, fil `image-to-lora-v2-release`, 1 événement daté du 2026-06-17 au 2026-06-17.
- **Note pratique :** À partir du 2026-06-17, utilisez la collection ModelScope liée comme point de référence daté pour localiser et évaluer Image-to-LoRA V2, tout en vérifiant séparément sa documentation et son comportement technique.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
