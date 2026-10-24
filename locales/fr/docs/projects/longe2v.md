---
title: "LongE2V"
category: projects

tags: [longe2v, longe2v-development, project]
aliases: ["LongE2V"]
level: 2
source_sha256: e2f7bf63445dff3e8febad526d3f9ff84c79d4b08709e61fb25af969314f7d1f
translation: machine
translated_at: '2026-10-24'
---
# LongE2V {#longe2v}

**Ligne de développement :** `project:longe2v` · fil `longe2v-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

LongE2V est une pile de recherche open source pour la vision événementielle, affinée sous forme de LoRA sur THUDM/CogVideoX-5B-I2V.

- Reconstruction vidéo à partir de flux d'événements épars.
- Prédiction à long horizon à partir de flux d'événements épars.
- Interpolation d'images à partir de flux d'événements épars.

Une exécution standard nécessite Linux, NVIDIA/CUDA 12.8, Python 3.10 et des voxels d'événements ; aucun fournisseur d'inférence hébergé n'existe. La pile convient à la reproduction et à l'évaluation de tâches de caméras événementielles, et non à la génération vidéo standard à partir de photos.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-12 — LongE2V est apparu comme projet SIGGRAPH 2026, avec du code pour une approche unifiée par diffusion de la reconstruction, de la prédiction et de l'interpolation d'images basées sur les événements. 2026-07-14 — Le modèle et le jeu de données LongE2V associés sur Hugging Face ont été marqués comme mis à jour ; le chemin public comprend désormais des poids LoRA prêts à l'emploi et des données prétraitées pour une reproduction locale.

## Comment l'utiliser {#how-to-use-this}

1. Clonez le dépôt, créez un environnement Python 3.10 et installez PyTorch 2.8.0 pour CUDA 12.8 ainsi que les dépendances du projet.
  — <https://github.com/cdfan0627/LongE2V>
2. Téléchargez le fichier LoRA publié dans weights/ et récupérez les données prétraitées, ou préparez manuellement les voxels d'événements.
  — <https://github.com/cdfan0627/LongE2V>
3. Choisissez la reconstruction, la prédiction ou l'interpolation, puis exécutez le script infer_*.sh correspondant avec la valeur DATASET définie.
  — <https://github.com/cdfan0627/LongE2V>
4. Traitez les images de sortie avant de comparer les métriques : redimensionnez-les, appliquez une correction de luminosité pour la reconstruction et la prédiction, puis exécutez le script de métriques correspondant.
  — <https://github.com/cdfan0627/LongE2V>

## Bonnes pratiques {#best-practices}

- LongE2V : ne remplacez pas les flux d'événements par des images d'entrée standard ; les méthodes sont conditionnées par des voxels d'événements et résolvent des tâches de caméras événementielles.
  — <https://arxiv.org/abs/2607.08770>
- LongE2V : utilisez la structure de données publiée pour obtenir des résultats reproductibles ; des fichiers de voxels manquants ou en trop modifient les segments d'événements, et les voxels inversés ne sont nécessaires que pour l'interpolation.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V : exécutez sur un seul GPU et préservez la compatibilité avec CUDA 12.8 et les paquets épinglés ; le multi-GPU reste non testé, et une valeur ATTENTION_SCORE_CHUNK_SIZE plus petite économise de la mémoire au prix de la vitesse.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V : ne comparez pas les images brutes aux métriques publiées ; les métriques de reconstruction et de prédiction nécessitent un environnement EVREAL séparé, car pyiqa entre en conflit avec les dépendances principales.
  — <https://github.com/cdfan0627/LongE2V>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- LongE2V — aucun journal des modifications public, tag ou GitHub Release n'existe ; les dates exactes de publication initiale du code et des poids, ainsi que les changements sémantiques ultérieurs, ne peuvent pas être retrouvées de manière fiable.
- LongE2V — la disponibilité et la compatibilité avec des données d'événements personnalisées arbitraires et avec des GPU quelconques n'ont pas été confirmées par une exécution réelle ; la documentation ne confirme que le chemin de recherche publié.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://cdfan0627.github.io/LongE2V-page/ | LongE2V — page du projet | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V | cdfan0627/LongE2V — implémentation officielle et README | 2026-09-06 |
| https://arxiv.org/abs/2607.08770 | LongE2V: Long-Horizon Event-based Video Reconstruction, Prediction, and Frame Interpolation with Video Diffusion Models | 2026-09-06 |
| https://huggingface.co/fansam39/LongE2V | fansam39/LongE2V — fiche modèle LoRA | 2026-09-06 |
| https://huggingface.co/datasets/fansam39/LongE2V-data | fansam39/LongE2V-data — jeu de données prétraité | 2026-09-06 |
| https://huggingface.co/papers/2607.08770 | Page Hugging Face du papier arXiv:2607.08770 | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V/releases | Versions GitHub de LongE2V | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:longe2v`, fil `longe2v-development`, 0 événement daté - → -.
- **Remarque pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
