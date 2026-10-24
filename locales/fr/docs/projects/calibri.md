---
title: "Calibri"
category: projects
date: 2026-03-29
tags: [calibri, project]
aliases: ["Calibri"]
level: 2
source_sha256: 664d9e97c3eec161fca71f0df3c7f6339b0f5608ff6e6fd97e1db6ccd72addef
translation: machine
translated_at: '2026-10-24'
---
# Calibri {#calibri}

**Ligne de développement :** `project:calibri` · fil `calibri`  
**Dernier événement :** 2026-03-29 · 1 événement daté depuis le 2026-03-29 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Calibri : méthode open source de calibration de Diffusion Transformer destinée aux développeurs de pipelines text-to-image. — ajoute des coefficients sur les sorties des blocs DiT ; — ajuste ces coefficients par CMA-ES à partir d'un modèle de récompense ; — prend en charge FLUX.1-dev, Stable Diffusion 3.5 et Qwen-Image. Limite : les poids prêts à l'emploi ne sont publiés que pour FLUX.1-dev et Qwen-Image ; il n'existe pas d'inférence hébergée officielle. Conclusion : c'est un outil pour accélérer et configurer un modèle DiT existant, et non un nouveau modèle de base.

## Ligne de développement {#development-line}

- **2026-03-29 — Les ressources du projet Calibri sont devenues publiquement accessibles.** 12B `v-gen-ai/flux-calibri-gates` et 20B `v-gen-ai/qwen-calibri` ; l'article avait été soumis pour la première fois sur arXiv le 2026-03-25.

## Modifications {#what-changed}

2026-03-29 — Deux modèles Calibri BF16 prêts à l'emploi sont apparus : 12B `v-gen-ai/flux-calibri-gates` et 20B `v-gen-ai/qwen-calibri` ; l'article avait été soumis pour la première fois sur arXiv le 2026-03-25. 2026-04-13 — Publication des poids de calibration ouverts pour FLUX.1-dev et Qwen-Image. 2026-07-29 — L'article a été mis à jour vers arXiv v2 ; le dépôt ne décrit pas de version runtime distincte pour cette révision.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-29, les praticiens doivent utiliser la page du projet, le dépôt et la collection Hugging Face liés comme points de départ pour évaluer Calibri ; la version exacte et les consignes d'utilisation restent non vérifiées.

1. Pour une génération prête à l'emploi avec FLUX, chargez `v-gen-ai/flux-calibri-gates` via Diffusers en BF16 sur CUDA, puis utilisez 15 étapes, un guidance scale de 3.5 et une résolution de base de 512×512.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
2. Pour une génération prête à l'emploi avec Qwen, utilisez `v-gen-ai/qwen-calibri` avec le custom pipeline indiqué dans la model card ; les paramètres de départ sont 15 étapes, `true_cfg_scale=4.0` et 512×512.
  — <https://huggingface.co/v-gen-ai/qwen-calibri>
3. Pour votre propre calibration, clonez le dépôt, créez l'environnement avec `uv sync`, lancez le reward server adéquat, puis démarrez CMA-ES via Accelerate avec la configuration de `configs/calibri.py`.
  — <https://github.com/v-gen-ai/Calibri>

## Bonnes pratiques {#best-practices}

- Commencez par les poids publiés et leurs paramètres standard plutôt que par l'entraînement : pour FLUX, la model card indique 15 étapes, un guidance scale de 3.5 et 512×512.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
- Pour l'entraînement, lancez d'abord le reward server HPSv3 ou Q-Align ; le script d'entraînement principal, sans service de récompense sélectionné, ne constitue pas un lancement reproductible.
  — <https://github.com/v-gen-ai/Calibri>
- Choisissez la granularité de recherche selon la tâche : block scaling d'environ 57 paramètres, layer scaling d'environ 76, gate scaling d'environ 114.
  — <https://github.com/v-gen-ai/Calibri>
- Vérifiez la calibration sur votre propre validation dataset : une inférence lancée sans `--prompt` génère des images de validation et calcule les métriques de récompense.
  — <https://github.com/v-gen-ai/Calibri>

## Éléments désormais obsolètes {#superseded-by-this}

- 2026-04-13 — Pour FLUX.1-dev et Qwen-Image, l'hypothèse selon laquelle Calibri ne pouvait être obtenu que par une calibration CMA-ES autonome n'est plus valable : des calibration weights prêts à l'emploi ont été publiés.
- 2026-07-29 — arXiv v1 du 2026-03-25 a été remplacé par la révision v2 ; le contenu des modifications entre les deux versions n'est pas détaillé dans les sources consultées.

## Points restant inconnus {#still-unknown}

- `event_findings` : 2026-03-29 — La collection Hugging Face, mise à jour le 2026-03-27, précise que la publication comprenait `v-gen-ai/flux-calibri-gates` (12B) et `v-gen-ai/qwen-calibri` (20B) ; arXiv v1 est daté du 2026-03-25. Sources : https://huggingface.co/collections/v-gen-ai/calibri-models ; https://arxiv.org/abs/2603.24800.
- `new_events` : 2026-04-13 — Les calibration weights pour FLUX.1-dev et Qwen-Image ont été ouverts. Source : https://github.com/v-gen-ai/Calibri.
- `new_events` : 2026-07-29 — arXiv v2 a mis à jour l'article ; l'entrée consultée ne fournit pas de liste des différences substantielles avec v1. Source : https://arxiv.org/abs/2603.24800.
- Le fragment Diffusers généré automatiquement dans la model card Qwen diffère de la section séparée Guide to run : cette dernière indique `makriot/qwen-calibri`, `custom_pipeline` et `trust_remote_code=True`. Il est impossible de confirmer, à partir des sources consultées, lequel de ces deux chemins est actuellement canonique.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://v-gen-ai.github.io/Calibri-page/ | Calibri: Parameter-Efficient Calibration of Diffusion Transformers | 2026-09-05 |
| https://github.com/v-gen-ai/Calibri | v-gen-ai/Calibri — implémentation officielle et README | 2026-09-05 |
| https://huggingface.co/collections/v-gen-ai/calibri-models | Modèles Calibri — collection v-gen-ai | 2026-09-05 |
| https://huggingface.co/v-gen-ai/flux-calibri-gates | Model card de v-gen-ai/flux-calibri-gates | 2026-09-05 |
| https://huggingface.co/v-gen-ai/qwen-calibri | Model card de v-gen-ai/qwen-calibri | 2026-09-05 |
| https://arxiv.org/abs/2603.24800 | Calibri: Enhancing Diffusion Transformers via Parameter-Efficient Calibration | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:calibri`, fil `calibri`, 1 événement daté, du 2026-03-29 au 2026-03-29.
- **Note pratique :** À partir du 2026-03-29, les praticiens doivent utiliser la page du projet, le dépôt et la collection Hugging Face liés comme points de départ pour évaluer Calibri ; la version exacte et les consignes d'utilisation restent non vérifiées.
- **Confiance :** élevée. Les mentions datées de remplacement ci-dessus font foi pour ce qui est obsolète.
