---
title: "Bernini — Disponibilité des modèles et intégration ComfyUI"
category: projects
date: 2026-06-02
tags: [bernini, model-availability-and-comfyui-integration, project]
aliases: ["Bernini"]
level: 3
source_sha256: 1ed0848b9c92977960fb95673a0608abbbd7d260b2dcc4c611f44a7025245401
translation: machine
translated_at: '2026-10-24'
---
# Bernini — Disponibilité des modèles et intégration ComfyUI {#bernini-model-availability-and-comfyui-integration}

**Ligne de développement :** `project:bernini` · fil `model-availability-and-comfyui-integration`  
**Dernier événement :** 2026-06-02 · 1 événement daté depuis le 2026-06-02 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

Bernini est un cadre de génération et d'édition vidéo de ByteDance, destiné aux praticiens qui ont besoin d'une alternative locale à un workflow Wan limité au moteur de rendu.

- Bernini complet / v2 : planification sémantique avec Qwen2.5-VL 7B, plus un moteur de rendu Wan2.2-T2V-A14B pour t2i, i2i, t2v, v2v, rv2v et r2v.
- Bernini-R : la ligne Wan limitée au moteur de rendu, pour une inférence plus simple et les modèles ComfyUI maintenus.

L'environnement de référence officiel est H100, CUDA 12.6 et Python 3.11.2. Les scripts vidéo utilisent par défaut huit processus, une résolution 480p, 16 ips et 81 images. Utilisez la v2 complète pour les modifications complexes en plusieurs étapes ; n'utilisez Bernini-R que si son périmètre de rendu plus restreint ou le chemin ComfyUI est l'objectif.

## Ligne de développement {#development-line}

- **2026-06-02 — Ressources du modèle Bernini et du workflow ComfyUI référencées.** Le 2026-06-02, une entrée datée sur Bernini a référencé le site du projet et le dépôt de modèle ByteDance/Bernini sur Hugging Face. Elle a également référencé un fichier JSON de workflow de test Bernini et un répertoire Bernini dans le dépôt WanVideo Comfy FP8 scaled de Kijai. Ensemble, ces ressources marquent une étape vers l'accès au modèle et l'utilisation dans ComfyUI.

## Changements {#what-changed}

- 2026-05-22 — L'article de Bernini a présenté l'architecture planificateur sémantique plus moteur de rendu DiT.
- 2026-06-01 — Le code et les poids de Bernini-R ont été publiés comme ligne limitée au moteur de rendu.
- 2026-06-02 — Des consignes de chargement au format Diffusers, basées uniquement sur la configuration, ont été publiées pour la version initiale du moteur de rendu.
- 2026-06-09 — Bernini-R a reçu une variante 1.3B basée sur Wan2.1 pour des modifications plus simples.
- 2026-06-11 — Le code d'inférence et les poids complets de Bernini ont ajouté le planificateur Qwen au moteur de rendu Wan.
- 2026-06-12 — R2V a reçu l'interpolation SA3D RoPE pour plus de cinq images de référence.
- 2026-06-13 — Le premier répertoire de conversion ComfyUI de Kijai a été supprimé.
- 2026-07-13 — Le code d'entraînement de Bernini-R a été publié.
- 2026-08-13 — Bernini-Diffusers-v2 est apparu, avec un connecteur de planificateur réentraîné et des résultats d'édition par référence révisés, communiqués par le fournisseur.

## Mode d'emploi {#how-to-use-this}

1. Choisissez d'abord l'artefact. Utilisez `Bernini-Diffusers-v2` complet pour la planification sémantique et les modifications complexes ; utilisez `Bernini-R-Diffusers` uniquement pour les tâches limitées au moteur de rendu.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
2. Clonez le dépôt officiel et installez ses dépendances épinglées. Installez le paquet VeOmni requis sans dépendances, afin qu'il ne remplace pas la version de PyTorch épinglée.
  — <https://github.com/bytedance/Bernini>
3. Téléchargez `ByteDance/Bernini-Diffusers-v2`, transmettez ce répertoire via `--config`, et commencez par un cas d'image fourni avant de passer aux cas vidéo ou guidés par référence.
  — <https://huggingface.co/ByteDance/Bernini-Diffusers-v2>
4. Utilisez les scripts de tâche maintenus et les fichiers JSON de cas pour t2i, i2i, t2v, v2v, rv2v ou r2v. Les scripts du pipeline complet contiennent les valeurs d'échantillonnage par défaut propres à chaque tâche.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
5. Pour ComfyUI, utilisez le workflow vidéo Bernini-R maintenu et le repack Comfy-Org Bernini-R. Il s'agit d'un chemin limité au moteur de rendu, qui ne prouve pas la prise en charge de la v2 complète.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json>

## Bonnes pratiques {#best-practices}

- Privilégiez le répertoire Diffusers autonome avec `--config`. N'utilisez les indicateurs séparés de points de contrôle à bruit élevé et faible que si vous utilisez volontairement l'ancienne structure.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md>
- Conservez intact l'environnement PyTorch/CUDA épinglé du dépôt lorsque vous ajoutez VeOmni, en l'installant avec `--no-deps`.
  — <https://github.com/bytedance/Bernini>
- Partez des scripts et fichiers de cas fournis plutôt que d'inventer des paramètres d'échantillonnage. Leur valeur vidéo par défaut est 480p, 16 ips et 81 images.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
- Dans le modèle ComfyUI, n'utilisez Turbo que pour itérer sur les prompts, désactivez-le pour la sortie finale, et indiquez à la fois la modification visée et les éléments qui doivent rester inchangés.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json>

## Remplacé par la suite {#superseded-by-this}

- 2026-06-11 — Considérer l'ensemble de Bernini comme la version de juin limitée au moteur de rendu est obsolète. Bernini complet a ajouté un planificateur sémantique MLLM.
- 2026-06-13 — Le chemin de téléchargement Kijai `WanVideo_comfy_fp8_scaled/tree/main/Bernini` est obsolète. Son historique enregistre la suppression de ce répertoire.
- 2026-08-13 — Le point de contrôle complet d'origine `Bernini-Diffusers` n'est plus l'unique recommandation actuelle du pipeline complet pour les travaux guidés par référence. La v2 décrit une recette d'entraînement du connecteur modifiée, sans garantie de compatibilité.

## Points non résolus {#still-unknown}

- Nous n'avons pas pu récupérer l'adresse d'origine `https://huggingface.co/ByteDance/Bernini`, si bien que son lien avec les dépôts Bernini-R actuels n'est pas établi.
- Nous n'avons pas pu récupérer la pièce jointe de workflow GitHub fournie. Son graphe de nœuds, les fichiers de modèle exacts et le résultat d'exécution restent non vérifiés.
- Le dossier Bernini direct de Kijai renvoie désormais une erreur 404. Son historique prouve la conversion FP8 initiale haut/bas bruit puis la suppression, mais pas la compatibilité actuelle ni les sommes de contrôle.
- Nous n'avons trouvé aucune annonce de lancement de la v2 datée et émanant du premier éditeur. Une mise à jour du dépôt le même jour et un rapport secondaire daté corroborent la date du 2026-08-13 ; la fiche officielle du modèle confirme le contenu de la v2 mais n'annonce pas cette date.
- Le matériel ComfyUI examiné comporte des modèles Bernini-R maintenus, alors que la prise en charge de la v2 complète faisait encore l'objet d'une demande ouverte. Cela n'exclut pas des workflows v2 communautaires non examinés.
- Nous n'avons trouvé aucune exécution indépendante et récente de performances dans l'environnement exact de la v2. Les chiffres de benchmark du fournisseur ne garantissent pas le comportement en déploiement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://bernini-ai.github.io/ | Bernini: Latent Semantic Planning for Video Diffusion | 2026-09-07 |
| https://github.com/bytedance/Bernini | GitHub - bytedance/Bernini | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini.md | Bernini — pipeline complet | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md | Bernini-R — moteur de rendu uniquement | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r_train.md | Guide d'entraînement Bernini-R | 2026-09-07 |
| https://github.com/bytedance/Bernini/commits/main | Commits · bytedance/Bernini | 2026-09-07 |
| https://huggingface.co/ByteDance/Bernini-Diffusers-v2 | ByteDance/Bernini-Diffusers-v2 · Hugging Face | 2026-09-07 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/commits/main/Bernini | Commits · Kijai/WanVideo_comfy_fp8_scaled — Bernini | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Bernini-R | Comfy-Org/Bernini-R · Hugging Face | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json | Modèle de workflow Comfy-Org Bernini-R pour l'édition vidéo | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json | Modèle de workflow Comfy-Org Bernini-R pour l'édition d'image | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/issues/15702 | Consider support for ByteDance Bernini-Diffusers-v2 · Issue #15702 | 2026-09-07 |
| https://www.orcarouter.ai/blog/bernini-diffusers-v2-shipped-quietly | Bernini-Diffusers-v2: ByteDance's Quiet Checkpoint Drop | 2026-09-07 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:bernini`, fil `model-availability-and-comfyui-integration`, 1 événement daté du 2026-06-02 au 2026-06-02.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
