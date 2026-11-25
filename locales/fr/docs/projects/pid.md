---
title: "PiD — Publication de recherche"
category: projects
date: 2026-05-25
tags: [pid, project, research-release]
aliases: ["PiD"]
level: 2
source_sha256: 8612bd230e9b3a84e5c191ac530299757f5c5382a3d155f4a22af63874042745
translation: machine
translated_at: '2026-10-24'
---
# PiD — Publication de recherche {#pid-research-release}

**Ligne de développement :** `project:pid` · fil `research-release`  
**Dernier événement :** 2026-05-25 · 1 daté depuis le 2026-05-25 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

PiD est un décodeur de diffusion par pixels pour les pipelines de génération d'images, qui remplace les décodeurs VAE et RAE standard.

- Décodage de latents : décode les latents en pixels avec un sur-échantillonnage 4× simultané, ou 8× pour Scale-RAE.
- Prise en charge des latents : fonctionne avec les latents VAE conventionnels et les latents sémantiques, notamment DINOv2 et SigLIP.
- Inférence rapide : les points de contrôle distillés décodent en quatre étapes.

Les poids NSCLv1 sont limités à la recherche non commerciale ou à l'évaluation.
Utilisez PiD lorsque vous avez besoin d'un décodage contrôlé du latent vers 2K/4K sur un backbone pris en charge, plutôt que d'un sur-échantillonneur de pixels distinct après le VAE.

## Ligne de développement {#development-line}

- **2026-05-25 — Les ressources de recherche, de code et de modèle de PiD ont été rendues publiques.** Le 2026-05-25, PiD a été publié avec les liens vers la recherche, le code source et les ressources de modèle Hugging Face. Ces liens établissent des points d'entrée techniques publics pour le projet, bien que les éléments de publication n'établissent pas de version précise ni l'ensemble des capacités.

## Modifications {#what-changed}

- 2026-05-25 — Publication de l'article, du code source et des poids PiD pour FLUX, FLUX.2, Z-Image, Z-Image-Turbo, SD3, DINOv2 et SigLIP.
- 2026-05-27 — Ajout de la prise en charge de PiD dans ComfyUI.
- 2026-06-02 — Publication des points de contrôle pour SDXL, Qwen-Image et Qwen-Image-2512 ; nettoyage de la base de code et activation de la prise en charge de torch.compile.
- 2026-07-09 — Publication du code d'entraînement, des versions distillée et non distillée de PiD v1.5 2K→4K, et des points de contrôle v1.5 pour FLUX, Z-Image, Z-Image-Turbo, FLUX.2 et Qwen-Image.
- 2026-07-14 — Ajout de la prise en charge optionnelle de la génération native Boogu-Image et du décodage PiD de ses latents VAE de type Flux.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-05-25, les praticiens doivent considérer la page de recherche de PiD, le dépôt source et la page de modèle Hugging Face comme ses points d'entrée techniques publics datés.

1. Clonez le dépôt, créez un environnement Python 3.12/CUDA avec `uv sync --frozen` ou installez les dépendances, puis exécutez `PYTHONPATH=. python verify_env.py`.
  — <https://github.com/nv-tlabs/PiD>
2. Téléchargez uniquement l'arborescence des points de contrôle : `hf download nvidia/PiD --local-dir . --include "checkpoints/*"`.
  — <https://github.com/nv-tlabs/PiD>
3. Utilisez `from_ldm` avec `--backbone` pour la génération d'image à partir d'un prompt ; utilisez `from_clean` pour encoder une image existante et la décoder avec PiD.
  — <https://github.com/nv-tlabs/PiD>
4. Sélectionnez `--pid_ckpt_type 2k` pour une sortie 2K ; choisissez `2kto4k_v1pt5` pour les modèles 4K pris en charge, ou `2kto4k` pour SD3 et SDXL.
  — <https://github.com/nv-tlabs/PiD>

## Bonnes pratiques {#best-practices}

- Vérifiez l'environnement avec `verify_env.py` avant d'exécuter l'inférence, et lancez les commandes depuis la racine du dépôt avec `PYTHONPATH=.`.
  — <https://github.com/nv-tlabs/PiD>
- Ne confondez pas les fichiers VAE avec les modèles PiD : les fichiers `PiD_*` sont des points de contrôle de décodeur distillés, tandis que `ae.safetensors`, VAE/RAE et les fichiers similaires sont des encodeurs et décodeurs dépendants.
  — <https://huggingface.co/nvidia/PiD>
- Choisissez v1.5 2K→4K pour FLUX, FLUX.2 et Qwen-Image afin de résoudre les artefacts de couleur et de grille aux coins ; le point de contrôle 2K reste plus net à exactement 2048 px.
  — <https://github.com/nv-tlabs/PiD>
- Vérifiez la licence avant tout déploiement : les poids publiés sont limités à la recherche non commerciale ou à l'évaluation.
  — <https://huggingface.co/nvidia/PiD>

## Remplacé par {#superseded-by-this}

- 2026-07-09 — Les anciens points de contrôle `2kto4k` pour FLUX, FLUX.2 et Qwen-Image sont dépréciés au profit de `2kto4k_v1pt5` ; les anciens poids ont été déplacés vers `checkpoints_deprecated/`.
- 2026-07-09 — Le conseil d'utiliser v1 `2kto4k` pour les nouveaux décodages 4K de FLUX, FLUX.2 et Qwen-Image est obsolète ; v1 `2kto4k` reste actuel pour SD3 et SDXL.

## Points non élucidés {#still-unknown}

- Le README initial indique des dates pour les mises à jour ultérieures, mais GitHub ne publie pas de versions distinctes numérotées ; les SHA de commit exacts et les horodatages ne sont pas établis.
- Les affirmations de vitesse et de qualité proviennent des propres benchmarks des auteurs ; une évaluation indépendante et reproductible sur un flux de travail précis n'a pas été testée ici.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/pid/ | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |
| https://github.com/nv-tlabs/PiD | nv-tlabs/PiD — PiD: Pixel Diffusion Decoder | 2026-09-05 |
| https://huggingface.co/nvidia/PiD | nvidia/PiD model repository | 2026-09-05 |
| https://arxiv.org/abs/2605.23902 | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:pid`, fil `research-release`, 1 événement daté du 2026-05-25 au 2026-05-25.
- **Note pratique :** À partir du 2026-05-25, les praticiens doivent considérer la page de recherche de PiD, le dépôt source et la page de modèle Hugging Face comme ses points d'entrée techniques publics datés.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
