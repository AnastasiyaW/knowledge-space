---
title: "Qwen-Video-Edit"
category: projects
date: 2026-08-18
tags: [project, qwen-video-edit]
aliases: ["Qwen-Video-Edit"]
level: 2
source_sha256: e6f7a89fb52a98ff8bfe993b5cd36ffd59bc477dabee3073f05a801f553406a2
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Video-Edit {#qwen-video-edit}

**Ligne de développement :** `project:qwen-video-edit` · fil `qwen-video-edit`  
**Dernier événement :** 2026-08-18 · 1 événement daté depuis le 2026-08-18 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Qwen-Video-Edit fournit du code et des points de contrôle (checkpoints) pour l'édition de vidéo par instructions, sans transformeur pré-entraîné sur la vidéo. Qwen-Image-Edit modifie la représentation latente du VAE de Wan 2.1, tandis que Wan 2.2 peut améliorer le résultat.

- Cohérence entre les images pour garder les modifications stables sur toute la vidéo.
- Instructions par segment pour attribuer un prompt individuel à chaque portion d'un long clip.
- Workflows CLI et ComfyUI pour les exécutions en local.

Un point de contrôle occupe environ 40 Go, les poids de base et l'amélioration nécessitent environ 55 Go de stockage, et le point de contrôle 720P a moins d'entraînement que les autres.
Pour un premier essai, commencez par 360P/step-30000, et utilisez 480P/global_local_81 pour les segments de 81 images.

## Ligne de développement {#development-line}

- **2026-08-18 — Qwen-Video-Edit a été présenté publiquement avec les liens vers le projet, le code et les modèles.** Le 2026-08-18, les auteurs ont publié la page du projet, le dépôt GitHub et la ressource Hugging Face afin que les utilisateurs puissent évaluer et exécuter les modèles.

## Changements {#what-changed}

- 2026-08-18 — La version initiale a publié le code, le rapport, la page du projet et un point de contrôle 360P ; le README date la version initiale au 2026-08-14.
- 2026-08-20 — Les auteurs ont ajouté des points de contrôle 480P couvrant différents sous-ensembles de données, une variante à 81 images et des poids 720P, ainsi que des nœuds personnalisés pour ComfyUI.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-18, évaluez Qwen-Video-Edit via la page du projet, le dépôt et la ressource Hugging Face, en vérifiant les capacités, l'installation, la licence et les détails des modèles avant toute adoption.

1. Créez un environnement Python 3.10–3.12 avec une version CUDA de PyTorch, installez requirements.txt et définissez DIFFSYNTH_MODEL_BASE_PATH.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
2. Téléchargez le point de contrôle recommandé 360P/step-30000 ainsi que les poids de base, ou laissez le chargeur les récupérer lors du premier lancement.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
3. Exécutez infer.py avec la vidéo d'entrée, prompts.txt, ainsi que le point de contrôle, num_frames et video_max_pixels correspondants, chaque ligne de prompts.txt correspondant à un segment.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
4. Pour ComfyUI, installez le dépôt dans custom_nodes, importez le workflow et définissez les chemins vers le point de contrôle et Wan 2.2.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Bonnes pratiques {#best-practices}

- Lancez les commandes depuis la racine du dépôt afin que les paquets diffsynth et wan fournis soient prioritaires sur les paquets externes.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Faites correspondre num_frames, video_max_pixels, latent_mode et pe_mode au tableau des points de contrôle, car les valeurs incompatibles ne sont pas prises en charge.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Commencez avec 360P/step-30000 comme valeur par défaut la plus sûre et la plus légère ; 720P n'a été entraîné que sur 3 500 étapes, donc revenez à 480P ou 360P si les résultats se dégradent.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Découpez les longues vidéos en segments et attribuez un prompt individuel à chacun ; réservez skip_enhance au débogage.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-20 — Le point de contrôle unique initial 360P ne constitue plus l'inventaire complet des modèles : les versions incluent désormais des variantes 480P, 81 images et 720P, ainsi que l'intégration ComfyUI.

## Inconnues {#still-unknown}

- Le schéma cible omet les champs event_findings et new_events ; la précision datée du 2026-08-18 et l'événement distinct du 2026-08-20 figurent donc dans what_changed et supersedes.
- Des benchmarks indépendants n'ont pas vérifié la qualité visuelle, les besoins en VRAM ni la fiabilité sur des vidéos d'entrée quelconques ; les données actuelles proviennent uniquement des auteurs du projet.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/yunpeng1998/Qwen-Video-Edit | Qwen-Video-Edit — dépôt GitHub et README | 2026-09-05 |
| https://yunpeng1998.github.io/Qwen-Video-Edit-Page/ | Qwen-Image Video-Edit — page du projet | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:qwen-video-edit`, fil `qwen-video-edit`, 1 événement daté du 2026-08-18 au 2026-08-18.
- **Note pratique :** À partir du 2026-08-18, les praticiens doivent utiliser la page du projet, le dépôt et la ressource Hugging Face comme point de départ pour évaluer Qwen-Video-Edit, tout en vérifiant les capacités, l'installation, la licence et les détails des modèles à partir de ces sources avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
