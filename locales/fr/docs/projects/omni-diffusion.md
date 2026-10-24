---
title: "Omni-Diffusion"
category: projects
date: 2026-03-11
tags: [multimodal_models, omni-diffusion, omni-diffusion-development, project]
aliases: ["Omni-Diffusion"]
level: 2
source_sha256: 8ed6b65de65a8ac4873a405610c63cf974cfd09dbacd677b0fef96bb525e1549
translation: machine
translated_at: '2026-10-24'
---
# Omni-Diffusion {#omni-diffusion}

**Ligne de développement :** `project:omni-diffusion` · fil `omni-diffusion-development`  
**Dernier événement :** 2026-03-11 · 1 événement daté depuis le 2026-03-11 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Omni-Diffusion est un modèle multimodal any-to-any reposant sur une diffusion discrète masquée. Il offre aux chercheurs et aux ingénieurs une pile ouverte unique, à la place de modèles autorégressifs distincts.

- Tâches de texte vers image, de parole vers image, de VQA, de VQA orale, d'ASR et de TTS.
- Génération et compréhension conjointes à travers le texte, les images et la parole.

Le point de contrôle publié compte 8 milliards de paramètres en BF16. Les tâches audio nécessitent un tokenizer et un décodeur GLM-4-Voice distincts ; les images nécessitent MagViT-v2. Il s'agit d'une pile de recherche reproductible plutôt que d'une API hébergée, car la fiche du modèle ne mentionne aucun fournisseur d'inférence connecté.

## Ligne de développement {#development-line}

- **2026-03-11 — Publication des ressources publiques du projet Omni-Diffusion.** Le 2026-03-11, une entrée datée a relié le site du projet Omni-Diffusion, le dépôt source et la page du modèle sur Hugging Face. Ensemble, ces ressources constituent un point de référence public pour la documentation, l'implémentation et l'accès au modèle. Les liens datés ne permettent pas à eux seuls d'établir la version publiée, les capacités ou les résultats d'évaluation.

## Évolutions {#what-changed}

- 2026-03-11 — Publication du code, de la page du projet et du point de contrôle ouvert Omni-Diffusion 8B BF16 pour les tâches any-to-any texte/image/parole.
- 2026-07-03 — La version 2 sur arXiv met à jour la version ICML de l'article et précise un point de contrôle de modèle optimisé.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-11, évaluez Omni-Diffusion à partir du site du projet, du dépôt source et de la page du modèle sur Hugging Face auxquels il renvoie, plutôt que de vous fier à une description secondaire non vérifiée.

1. Clonez le dépôt, initialisez les sous-modules, puis installez les dépendances et le paquet dans un environnement issu de l'image Docker officielle.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
2. Téléchargez le point de contrôle principal dans ../models/Omni-Diffusion ; pour les tâches audio, ajoutez le tokenizer et le décodeur GLM-4-Voice, et pour les images, ajoutez MagViT-v2.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
3. Exécutez tools/inference.py en indiquant les chemins vers les poids principaux, le tokenizer d'images, le tokenizer audio, le décodeur audio et le répertoire de sortie.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Bonnes pratiques {#best-practices}

- Utilisez le chemin d'inférence du dépôt officiel pour les tâches multimodales : le chargement via Transformers ne remplace pas les tokenizers d'images et d'audio requis.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
- Épinglez et vérifiez la révision du modèle avant d'activer `trust_remote_code`, car la fiche exige explicitement une architecture personnalisée.
  — <https://huggingface.co/lijiang/Omni-Diffusion>
- Conservez les poids principaux et les trois artefacts auxiliaires dans des chemins et un environnement cohérents, faute de quoi la pile texte/image/parole annoncée ne pourra pas être construite.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Remplacé par {#superseded-by-this}

- 2026-07-03 — La version 2 sur arXiv remplace la version 1 du 2026-03-06 comme version actuelle de l'article ; la version 2 est indiquée comme la version ICML, avec un point de contrôle optimisé.

## Points encore inconnus {#still-unknown}

- Les exigences publiées et principales en matière de VRAM, de latence ou de version CUDA prise en charge pour l'inférence n'ont pas été trouvées.
- Aucune source officielle en chinois ni aucun retour d'expérience indépendant en chinois n'ont été confirmés ; la recherche en chinois n'a donné que des synthèses secondaires.
- L'absence de fournisseur d'inférence sur la fiche Hugging Face confirme l'absence de fournisseur hébergé répertorié, mais n'exclut pas des déploiements auto-hébergés par des tiers.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://omni-diffusion.github.io/ | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |
| https://github.com/VITA-MLLM/Omni-Diffusion | Dépôt VITA-MLLM/Omni-Diffusion | 2026-09-05 |
| https://huggingface.co/lijiang/Omni-Diffusion | Fiche de modèle lijiang/Omni-Diffusion | 2026-09-05 |
| https://arxiv.org/abs/2603.06577 | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:omni-diffusion`, fil `omni-diffusion-development`, 1 événement daté du 2026-03-11 au 2026-03-11.
- **Note pratique :** Au 2026-03-11, les praticiens doivent évaluer Omni-Diffusion à partir du site du projet, du dépôt source et de la page du modèle sur Hugging Face auxquels il renvoie, plutôt que de se fier à une description secondaire non vérifiée.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
