---
title: "MOSS-Video-Preview"
category: projects
date: 2026-06-10
tags: [moss-video-preview, project]
aliases: ["MOSS-Video-Preview"]
level: 2
source_sha256: 75c81ecd7122de156bbd6f2838ad262a02defb6a608cab82850f016b9b137af5
translation: machine
translated_at: '2026-10-24'
---
# MOSS-Video-Preview {#moss-video-preview}

**Ligne de développement :** `project:moss-video-preview` · fil `moss-video-preview`  
**Dernier événement :** 2026-06-10 · 1 événement daté depuis 2026-06-10 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

MOSS-Video-Preview est une famille de modèles vidéo-langage sous licence Apache-2.0, à code personnalisé, reposant sur une attention croisée image-vidéo à portes (gated cross-attention). Elle comprend Base pour le préentraînement, SFT pour le suivi d'instructions hors ligne, et Real-Time-SFT pour l'inférence en direct, image par image. Le point de contrôle Base publié fait 11B en BF16 ; le projet rapporte une mesure sur un seul H200 de 1,9537 s de TTFT moyen sur un test de 256 images. Verdict : n'utiliser Real-Time-SFT que lorsque le comportement en flux continu est requis ; il s'agit d'une version de recherche exploratoire, et non d'un service d'inférence hébergé.

## Ligne de développement {#development-line}

- **2026-06-10 — Ressources publiques du projet MOSS-Video-Preview référencées.** Le 2026-06-10, la ligne de développement MOSS-Video-Preview a été associée à un dépôt GitHub public et à une collection Hugging Face. Les liens datés établissent un point de référence public pour le projet, mais ils n'établissent pas à eux seuls une version précise, une capacité du modèle ou un changement de version.

## Ce qui a changé {#what-changed}

2026-06-10 — Le paquet du projet relié était accessible publiquement ; les documents de première main présentent la famille comme un modèle vidéo à attention croisée à portes d'environ 10,7B/11B, avec des points de contrôle distincts Base, SFT hors ligne et Real-Time-SFT. 2026-06-01 — OpenMOSS a publié le rapport technique et diffusé Realtime-QA-100K, un sous-ensemble d'entraînement de 100 000 échantillons pour le questionnement-réponse vidéo en temps réel. 2026-04-08 — OpenMOSS a publié MOSS-VL-Base-0408 et MOSS-VL-Instruct-0408, après avoir lancé la ligne MOSS-VL. 2026-03-04 — Le code source et les détails d'architecture de MOSS-Video-Preview ont été publiés. 2025-10-18 — Le projet a enregistré un bilan post-mortem et a démarré MOSS-VL. 2025-10-08 — Une démonstration interne a été présentée. 2025-09 — Le point de contrôle Real-Time-SFT était prêt. 2025-08 — Le point de contrôle SFT hors ligne était prêt.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-10, les praticiens doivent utiliser le dépôt GitHub et la collection Hugging Face reliés comme points de référence publics initiaux pour MOSS-Video-Preview, tout en vérifiant les détails de version revendiqués à partir des documents primaires du projet.

1. Cloner le dépôt, créer l'environnement Python 3.12.4 documenté et installer le paquet ; la pile testée est PyTorch 2.4.0 avec CUDA 12.1 et DeepSpeed 0.16.1.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
2. Utiliser `moss-video-preview-sft` avec `inference.offline_infer` pour une vidéo préenregistrée et une instruction ; utiliser le point de contrôle Base pour la complétion ou comme point de départ d'un SFT.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
3. Utiliser `moss-video-preview-realtime-sft` avec `inference.realtime_streaming_infer` pour les images entrantes ; Base et le SFT standard ne sont pas compatibles avec le chemin de streaming.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
4. Charger Realtime-QA-100K avec la bibliothèque `datasets` de Hugging Face lors de la reproduction ou de l'adaptation des données de SFT en temps réel ; il fournit des annotations, des identifiants YouTube et des horodatages, et non des fichiers vidéo.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Bonnes pratiques {#best-practices}

- Choisir le point de contrôle selon la tâche : Base nécessite un SFT en aval pour le suivi d'instructions, le SFT hors ligne sert aux clips complets, et Real-Time-SFT est le point de contrôle requis pour le streaming.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-base>
- Utiliser `trust_remote_code=True` seulement après avoir examiné le code du dépôt, car cette famille de modèles nécessite des correspondances personnalisées de Transformers ; utiliser FlashAttention 2 sur CUDA lorsque la faible latence est importante.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft>
- Traiter la comparaison de vitesse publiée comme un montage sur un seul H200, et non comme un benchmark général ; son test a utilisé 256 images extraites d'une vidéo 1080p de 97,56 secondes.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
- Pour Realtime-QA-100K, prévoir soi-même la disponibilité et les droits des vidéos : la diffusion ne contient aucune vidéo, et le matériel YouTube d'origine peut disparaître ou être restreint géographiquement.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Remplacé par cette entrée {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Points encore inconnus {#still-unknown}

- Le point d'accès de la collection Hugging Face fourni n'a renvoyé aucun contenu lisible lors de cette vérification ; sa date de création et l'état exact de la collection au 2026-06-10 ne sont donc pas vérifiés.
- Aucune source de première main examinée ne déclare MOSS-Video-Preview formellement déprécié ni n'indique que MOSS-VL le remplace ; MOSS-VL est donc consigné comme une ligne de développement successeur apparentée, et non comme un remplacement formel.
- Le README actuel du projet décrit encore une montée en échelle, un entraînement distribué et des publications plus larges de code et de données comme travaux futurs ; la maturité de production, la cadence de publication maintenue et la prise en charge de services par des tiers ne sont pas vérifiées.
- event_findings:[2026-06-10] La documentation du projet identifie la version reliée comme une famille de modèles d'environ 10,7B (commercialisée comme 11B) comportant 40 couches décodeur, dont 8 couches d'attention croisée à portes ; elle distingue Base, SFT hors ligne et Real-Time-SFT plutôt que de livrer un point de contrôle unique interchangeable. Date de la source : entrée d'actualité du projet du 2026-06-01 ; URL de la source : https://github.com/OpenMOSS/MOSS-Video-Preview.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/OpenMOSS/MOSS-Video-Preview | Dépôt OpenMOSS/MOSS-Video-Preview et README | 2026-09-05 |
| https://huggingface.co/collections/OpenMOSS-Team/moss-video-preview | Collection OpenMOSS-Team MOSS-Video-Preview | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-base | Fiche modèle OpenMOSS-Team/moss-video-preview-base | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-sft | Fiche modèle OpenMOSS-Team/moss-video-preview-sft | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft | Fiche modèle OpenMOSS-Team/moss-video-preview-realtime-sft | 2026-09-05 |
| https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K | Fiche de jeu de données OpenMOSS-Team/Realtime-QA-100K | 2026-09-05 |
| https://github.com/OpenMOSS/MOSS-VL | Dépôt OpenMOSS/MOSS-VL | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:moss-video-preview`, fil `moss-video-preview`, 1 événement daté du 2026-06-10 au 2026-06-10.
- **Note pratique :** Au 2026-06-10, les praticiens doivent utiliser le dépôt GitHub et la collection Hugging Face reliés comme points de référence publics initiaux pour MOSS-Video-Preview, tout en vérifiant les détails de version revendiqués à partir des documents primaires du projet.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
