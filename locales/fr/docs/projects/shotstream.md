---
title: "ShotStream"
category: projects
date: 2026-03-31
tags: [project, shotstream]
aliases: ["ShotStream"]
level: 2
source_sha256: 863fb2e57be4307e03617dd1702ed6451417364908e1122c454bbb50c2474979
translation: machine
translated_at: '2026-10-24'
---
# ShotStream {#shotstream}

**Ligne de développement :** `project:shotstream` · fil `shotstream`  
**Dernier événement :** 2026-03-31 · 1 événement daté depuis le 2026-03-31 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

ShotStream est une implémentation de recherche en CUDA destinée aux créateurs et aux développeurs de modèles vidéo qui souhaitent piloter un récit vidéo multi-plans à partir de texte pendant sa génération.

- Génération du plan suivant à partir des plans historiques et de prompts en flux continu.
- Exécution sur Wan2.1-T2V-1.3B avec des checkpoints locaux.
- Caches global et local distincts pour la continuité inter-plans et intra-plan.

Les auteurs rapportent 15,95 FPS en 832×480 sur un NVIDIA H200. Les démonstrations montrent 5 à 6 plans et près de 500 images. Il s'agit d'une voie de reproduction de recherche en local, et non d'un service vidéo hébergé. Les démonstrations publiques ne garantissent pas la parité avec la configuration d'entraînement interne.

## Ligne de développement {#development-line}

- **2026-03-31 — La page projet publique, le code et les pages de modèle de ShotStream ont été publiés en ligne.** Le 2026-03-31, une publication datée renvoyait vers la page projet publique, le dépôt GitHub et la page Hugging Face. Les éléments disponibles fournissent un point de référence public pour la ligne de développement. Ils n'établissent ni numéro de version, ni capacités, ni auteurs, ni le texte exact du message d'origine.

## Ce qui a changé {#what-changed}

- 2026-03-25 — L'historique Hugging Face de ShotStream enregistre une configuration et trois envois de checkpoints.
- 2026-03-26 — La version v1 de ShotStream sur arXiv a été soumise.
- 2026-03-27 — ShotStream a publié sa page projet, la version arXiv, le code d'entraînement et d'inférence, ainsi que les checkpoints.
- 2026-03-31 — La fiche du modèle de ShotStream a reçu une étiquette text-to-video ainsi qu'une documentation, des instructions d'utilisation et des éléments de citation enrichis.
- 2026-06-18 — Le dépôt de ShotStream a signalé l'acceptation à ECCV 2026.

## Comment l'utiliser {#how-to-use-this}

1. Cloner le dépôt et créer l'environnement documenté : Python 3.10, CUDA, PyTorch, dépendances et FlashAttention.
  — <https://github.com/KlingAIResearch/ShotStream>
2. Télécharger le modèle de base Wan2.1-T2V-1.3B et les checkpoints de ShotStream avec Git LFS dans les répertoires documentés.
  — <https://github.com/KlingAIResearch/ShotStream>
3. Préparer un JSON de prompts contenant un global_caption et des descriptions shot1 à shotN pour la séquence.
  — <https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json>
4. Lancer le script d'inférence multi-plans autoregressive en quatre étapes documenté.
  — <https://github.com/KlingAIResearch/ShotStream>

## Remplacé par {#superseded-by-this}

- 2026-03-27 — La publication du code d'entraînement, du code d'inférence et des checkpoints remplace l'état de l'article antérieur à la publication.
- 2026-03-31 — Documentation de la fiche de modèle et métadonnées du pipeline mises à jour ; cette date n'a apporté ni nouveaux poids ni nouveau code.
- 2026-06-18 — L'acceptation à ECCV 2026 remplace le statut de publication antérieur à l'acceptation, sans annoncer de nouvel artefact d'exécution.

## Points encore inconnus {#still-unknown}

- Les liens seuls ne permettent pas de savoir si l'événement du 2026-03-31 renvoyait spécifiquement à la mise à jour de la fiche de modèle du même jour.
- Les sources primaires ne mentionnent aucun point d'accès hébergé pris en charge, ni de minimum de GPU grand public, ni d'exigence en VRAM, ni de benchmark de reproduction indépendant. Le débit indiqué est une mesure des auteurs sur H200.
- Les sources primaires ne contiennent aucune consigne d'utilisation en chinois simplifié émanant des auteurs, ni de discussion indépendante de praticiens. Les résumés secondaires n'ont pas été retenus comme preuves.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://luo0207.github.io/ShotStream/ | Page projet ShotStream | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream | Dépôt KlingAIResearch/ShotStream et README | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream | Fiche du modèle KlingTeam/ShotStream | 2026-09-07 |
| https://arxiv.org/abs/2603.25746 | ShotStream: Streaming Multi-Shot Video Generation for Interactive Storytelling | 2026-09-07 |
| https://arxiv.org/html/2603.25746 | Version HTML de l'article ShotStream | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/commits/main | Historique des commits de KlingTeam/ShotStream | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/discussions/1 | Improve model card and add pipeline tag | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json | JSON de prompts de démonstration de ShotStream | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:shotstream`, fil `shotstream`, 1 événement daté du 2026-03-31 au 2026-03-31.
- **Note pratique :** voir les sections d'usage et de pratique sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
