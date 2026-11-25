---
title: "SAMA"
category: projects
date: 2026-03-20
tags: [project, sama]
aliases: ["SAMA"]
level: 2
source_sha256: b205bd9d1d99e77b86e0868f79a336e5f5acc55e29da2c390f3035d61c637e10
translation: machine
translated_at: '2026-10-24'
---
# SAMA {#sama}

**Ligne de développement :** `project:sama` · fil `sama`  
**Dernier événement :** 2026-03-20 · 1 événement daté depuis le 2026-03-20 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Description {#what-it-is}

Un modèle open source d'édition vidéo guidée par instructions, destiné aux utilisateurs de Wan qui modifient des objets, un style ou du texte dans une vidéo tout en conservant le mouvement.

- L'ancrage sémantique planifie les modifications à travers les images clés.
- L'alignement du mouvement préserve la dynamique temporelle.
- Le checkpoint SAMA-14B et un workflow ComfyUI officiel sont disponibles.

Nécessite Linux, un GPU NVIDIA, Python 3.10, un environnement compatible CUDA 12.1 et Wan2.1-T2V-14B. Il s'agit d'une pile d'inférence locale reposant sur Wan, et non d'un service hébergé.

## Ligne de développement {#development-line}

- **2026-03-20 — Publication du projet public SAMA, de ses sources et de ses ressources de modèle.** Le 2026-03-20, un message daté de SAMA a lié le site web public du projet, le dépôt source et la page Hugging Face de SAMA-14B. Ces liens établissent que les trois ressources publiques étaient associées à SAMA à cette date, sans établir d'autres affirmations sur le modèle ou le projet.

## Évolutions {#what-changed}

- **2026-03-20** — Publication de l'article SAMA ; préimpression soumise le 2026-03-19, 24 pages et 12 figures.
- **2026-03-21** — Publication du checkpoint SAMA-14B ; SAMA-5B toujours indiqué comme « bientôt disponible ».
- **2026-03-24** — Ouverture du workflow officiel SAMA-ComfyUI.
- **2026-06-20** — SAMA accepté à ECCV 2026.
- **2026-06-26** — Publication des métadonnées de l'ensemble SAMA-edit-filtered-1M.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-20, nous utilisons le site web SAMA, le dépôt source et la page du modèle SAMA-14B liés comme points de départ pour l'évaluation. Il convient de vérifier les capacités, la licence et les exigences d'utilisation à partir de ces ressources avant toute adoption.

1. Cloner le dépôt, créer un environnement Python 3.10 et installer les dépendances.
  — <https://github.com/Cynthiazxy123/SAMA>
2. Télécharger SAMA-14B et préparer le répertoire local complet de Wan2.1-T2V-14B.
  — <https://huggingface.co/syxbb/SAMA-14B>
3. Définir MODEL_ROOT, STATE_DICT, SRC_VIDEO, PROMPT et OUTPUT_DIR dans infer_sh/run_sama.sh, puis exécuter le script.
  — <https://github.com/Cynthiazxy123/SAMA>
4. Pour un workflow basé sur des nœuds, utiliser l'intégration ComfyUI officielle avec le modèle de base Wan et SAMA-14B.
  — <https://github.com/Cynthiazxy123/SAMA>

## Bonnes pratiques {#best-practices}

- Vérifier que le répertoire de base Wan2.1-T2V-14B est complet : le script s'arrête volontairement si des fichiers manquent.
  — <https://github.com/Cynthiazxy123/SAMA>
- Utiliser le FPS de la source ; définir explicitement --fps lorsqu'il est absent.
  — <https://github.com/Cynthiazxy123/SAMA>
- Tenir compte du remplissage automatique des images d'entrée pour respecter l'exigence Wan 4k+1.
  — <https://github.com/Cynthiazxy123/SAMA>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-03-20 — état « article uniquement » : SAMA-14B est disponible depuis le 2026-03-21, et le workflow ComfyUI officiel est disponible depuis le 2026-03-24.

## Points non élucidés {#still-unknown}

- Les documents officiels ne fournissent ni mesure de VRAM, ni vitesse d'inférence, ni résolutions prises en charge. La planification matérielle nécessite des tests distincts de la configuration et du workflow.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://cynthiazxy123.github.io/SAMA/ | SAMA : ancrage sémantique factorisé et alignement du mouvement pour l'édition vidéo guidée par instructions | 2026-09-05 |
| https://github.com/Cynthiazxy123/SAMA | Cynthiazxy123/SAMA — code d'inférence officiel | 2026-09-05 |
| https://huggingface.co/syxbb/SAMA-14B | syxbb/SAMA-14B | 2026-09-05 |
| https://arxiv.org/abs/2603.19228 | SAMA : ancrage sémantique factorisé et alignement du mouvement pour l'édition vidéo guidée par instructions | 2026-09-05 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:sama`, fil `sama`, 1 événement daté du 2026-03-20 au 2026-03-20.
- **Note pratique :** Au 2026-03-20, les praticiens peuvent utiliser le site web SAMA, le dépôt source et la page du modèle SAMA-14B comme principaux points de départ pour l'évaluation, tout en vérifiant les capacités, la licence et les exigences d'utilisation à partir de ces ressources avant toute adoption.
- **Confiance :** élevée. Les mentions de remplacement datées ci-dessus font foi pour ce qui est obsolète.
