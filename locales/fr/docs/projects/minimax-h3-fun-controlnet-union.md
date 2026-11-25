---
title: "MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union"
category: projects
date: 2026-08-24
tags: [minimax-h3-fun-controlnet-union, minimax_h3_fun_controlnet_union, project]
aliases: ["MiniMax-H3-Fun-Controlnet-Union"]
level: 2
source_sha256: bc6807995cdf199098a2bd4934e92e1c4e63c1ab23b428291635c1d6c9c7cabd
translation: machine
translated_at: '2026-10-24'
---
# MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union {#minimax-h3-fun-controlnet-union-minimax-h3-fun-controlnet-union}

**Ligne de développement :** `project:minimax-h3-fun-controlnet-union` · fil `minimax-h3-fun-controlnet-union`  
**Dernier événement :** 2026-08-24 · 1 événement daté depuis le 2026-08-24 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

MiniMax-H3-Fun-Controlnet-Union est un adaptateur de contrôle pour le générateur vidéo de base MiniMax-H3, conçu pour les utilisateurs de VideoX-Fun.

- Point de contrôle unifié permettant d'exploiter les conditionnements Canny, Depth, HED, MLSD et Pose.
- Pipeline vidéo-vers-vidéo pour diriger la génération à partir d'une vidéo de contrôle.
- Pipeline d'inpainting vidéo pour éditer les zones masquées.

Les poids de contrôle ne fonctionnent pas de manière autonome : le transformeur de base et Qwen3-VL réunis dépassent 80 Go de VRAM. Choisissez-le lorsque la structure du mouvement importe davantage que la génération texte-vers-vidéo seule et que le déchargement (offload) est disponible.

## Ligne de développement {#development-line}

- **2026-08-24 — MiniMax H3 Fun ControlNet Union relié à un exemple VideoX-Fun.** Le 2026-08-24, une mise à jour du projet a relié le dépôt Hugging Face MiniMax-H3-Fun-Controlnet-Union à un répertoire d'exemple VideoX-Fun pour MiniMax H3 Fun. Ce lien associe les poids du modèle à un exemple d'implémentation. Les détails de configuration et les capacités de la version n'ont pas été vérifiés de manière indépendante.

## Ce qui a changé {#what-changed}

2026-08-24 — VideoX-Fun a ajouté le répertoire `examples/minimax_h3_fun`, et ControlNet-Union pour MiniMax-H3 est devenu disponible en tant que modèle de contrôle séparé. 2026-08-27 — ComfyUI a préparé le chargement des points de contrôle, le conditionnement vidéo et inpainting, et l'application du flux de contrôle, mais la PR #15860 reste ouverte.

## Comment l'utiliser {#how-to-use-this}

Évaluez l'exemple MiniMax H3 Fun de VideoX-Fun conjointement avec MiniMax-H3-Fun-Controlnet-Union à partir du 2026-08-24 ; la configuration exacte et les capacités restent non vérifiées.

1. Clonez VideoX-Fun et créez `models/Diffusion_Transformer`. Placez le modèle de base MiniMax-H3 et `MiniMax-H3-Fun-Controlnet-Union.safetensors` dans des répertoires distincts, comme indiqué sur la fiche du modèle.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
2. Dans `examples/minimax_h3_fun/predict_v2v_control.py`, renseignez le modèle de base, `minimax_h3_control.yaml`, le chemin des poids de contrôle, la vidéo de contrôle et le prompt, puis exécutez le script.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
3. Pour l'édition par masque, exécutez `predict_v2v_control_inpaint.py` au lieu du script standard de contrôle par vidéo.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
4. Sur un seul GPU de 80 Go, activez `model_group_offload` ou `model_cpu_offload_and_qfloat8` ; ne vous attendez pas à ce que le transformeur de base et Qwen3-VL tiennent ensemble en mémoire.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Bonnes pratiques {#best-practices}

- Gardez `guidance_scale = 1.0`. Le point de contrôle est distillé pour le guidage ; des valeurs plus élevées réappliquent le guidage et dégradent la sortie.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Conservez une disposition fixe du réseau de contrôle. La configuration doit préserver `control_blocks_places: [0, 10, 20, 30, 40]`, `control_in_dim: 49` et un contrôle audio désactivé, sinon les poids ne se chargent pas.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Commencez avec `control_context_scale = 1.0`. Réduisez-le uniquement pour affaiblir le suivi de la vidéo de contrôle ; `0.0` désactive complètement le conditionnement de contrôle.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Vérifiez la licence communautaire MiniMax H3 avant toute distribution ou utilisation hébergée. Elle exclut l'UE, le Royaume-Uni, la République de Corée et les États-Unis du Territoire applicable, et prévoit des conditions particulières pour les revenus annuels supérieurs à 20 millions de dollars US.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- `event_findings` et `new_events` ont été ajoutés comme extensions d'objet car la tâche les exige alors que le schéma JSON du système les omet.
- La publication du dépôt Hugging Face avant le 2026-08-24 reste non confirmée ; la page de commit affiche une durée relative au lieu d'un horodatage ISO.
- La PR #15860 de ComfyUI reste ouverte ; confirmer la prise en charge de la version nécessite une fusion en amont ou un justificatif de publication.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/aigc-apps/VideoX-Fun/tree/main/examples/minimax_h3_fun | VideoX-Fun — examples/minimax_h3_fun | 2026-09-05 |
| https://github.com/aigc-apps/VideoX-Fun/commits/main/examples/minimax_h3_fun | VideoX-Fun — history for examples/minimax_h3_fun | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union | alibaba-pai/MiniMax-H3-Fun-Controlnet-Union model card | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0 | Update Weights — MiniMax-H3-Fun-Controlnet-Union | 2026-09-05 |
| https://github.com/Comfy-Org/ComfyUI/pull/15860 | ComfyUI PR #15860 — Support MiniMax-H3 fun controlnet | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:minimax-h3-fun-controlnet-union`, fil `minimax-h3-fun-controlnet-union`, 1 événement daté du 2026-08-24 au 2026-08-24.
- **Note pratique :** Évaluez l'exemple MiniMax H3 Fun de VideoX-Fun avec l'artefact MiniMax-H3-Fun-Controlnet-Union à partir du 2026-08-24 ; la configuration exacte et les capacités restent non vérifiées.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
