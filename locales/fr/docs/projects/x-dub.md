---
title: "X-Dub — Développement du projet"
category: projects
date: 2026-03-28
tags: [project, project-development, x-dub]
aliases: ["X-Dub"]
level: 2
source_sha256: be448c0db046accdf5235432e68e73671ae54d790f4d54d18664c4b5168389d6
translation: machine
translated_at: '2026-10-24'
---
# X-Dub — Développement du projet {#x-dub-project-development}

**Ligne de développement :** `project:x-dub` · fil `project-development`  
**Dernier événement :** 2026-03-28 · 1 événement daté depuis le 2026-03-28 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

X-Dub est une publication sous licence Apache-2.0 comprenant le code et les poids du modèle de synchronisation labiale de la vidéo vers l'audio. Le modèle public, X-Dub (Wan-5B), repose sur Wan2.2-TI2V-5B et non sur le X-Dub interne (internal-1B) décrit dans l'article.

- Édition des mouvements de la bouche : synchronise les mouvements de la bouche de la vidéo sur l'audio fourni.
- Prise en charge des personnages : gère les visages humains et non humains.
- Recadrage du visage : recadre automatiquement la zone de la tête.

L'inférence typique nécessite environ 21 Go de VRAM et ne prend actuellement en charge qu'une personne par vidéo. Ce modèle convient au doublage local de sujets uniques lorsque la mémoire GPU est suffisante et que les scintillements occasionnels ou la dérive d'identité sont acceptables.

## Ligne de développement {#development-line}

- **2026-03-28 — Les ressources publiques du projet X-Dub ont été liées.** Le 2026-03-28, une entrée datée de X-Dub a relié le site du projet, le dépôt GitHub et la page Hugging Face. Ces liens confirment la disponibilité publique du code et des poids sans introduire de nouvelle version, de nouvelle version technique ni de modification technique.

## Changements {#what-changed}

- 2025-12-31 — L'article et la page du projet ont présenté ContextDubBench ainsi que la méthode de doublage visuel auto-amorcée et sans masque.
- 2026-03-19 — Le code d'inférence et les poids pré-entraînés de la version publique de X-Dub, basée sur Wan, ont été publiés.
- 2026-03-28 — X-Dub est devenu disponible via la page du projet, le dépôt GitHub et les poids sur Hugging Face.
- 2026-05-15 — Le projet a annoncé son acceptation à ICML 2026.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-03-28, consultez le site du projet X-Dub, le dépôt GitHub et la page Hugging Face lorsque vous évaluez les ressources publiques. L'entrée liée fournit le code et les poids, et non une procédure d'installation distincte.

1. Clonez le dépôt officiel, créez un environnement Conda Python 3.10 et installez les dépendances Python, OpenMMLab et du projet en mode éditable indiquées.
  — <https://github.com/KlingAIResearch/X-Dub>
2. Téléchargez `KlingTeam/X-Dub` dans `checkpoints/`, puis déplacez les modèles DWPose fournis vers `dwpose_tools/models/`.
  — <https://github.com/KlingAIResearch/X-Dub>
3. Exécutez `infer_lip_sync_pipeline.py` avec une vidéo, l'audio de remplacement, `X-Dub_model.safetensors`, le répertoire de sortie et les réglages initiaux `ref_cfg_scale=2.5`, `audio_cfg_scale=10.0` et 30 étapes d'inférence.
  — <https://github.com/KlingAIResearch/X-Dub>
4. Vérifiez la sortie pour détecter les saccades de recadrage, les scintillements, la dérive des couleurs et les images bruitées avant de publier le média modifié.
  — <https://github.com/KlingAIResearch/X-Dub>

## Bonnes pratiques {#best-practices}

- Utilisez des séquences d'une seule personne dont le visage reste suivable. DWPose en ligne perd les têtes qui bougent rapidement et échoue dans les scènes à plusieurs personnes.
  — <https://github.com/KlingAIResearch/X-Dub>
- Commencez avec 25 à 50 étapes d'inférence. Un nombre d'étapes plus élevé augmente le temps d'exécution et n'a pas fait l'objet d'une évaluation exhaustive.
  — <https://github.com/KlingAIResearch/X-Dub>
- Ajustez `ref_cfg_scale` et `audio_cfg_scale` pour chaque clip afin d'arbitrer entre la fidélité à l'apparence de référence et le mouvement de la bouche piloté par l'audio.
  — <https://github.com/KlingAIResearch/X-Dub>
- Signalez clairement les médias générés ou modifiés. N'utilisez pas le système pour l'usurpation d'identité trompeuse.
  — <https://github.com/KlingAIResearch/X-Dub>

## Remplacé par cette entrée {#superseded-by-this}

- 2026-03-19 — Le X-Dub interne (internal-1B) de l'article n'est pas l'implémentation téléchargeable. La version publique est X-Dub (Wan-5B), qui remplace le backbone et utilise un SFT multi-étapes au lieu d'un ajustement LoRA.
- 2026-03-19 — Ne supposez pas la parité avec le modèle de l'article en production. La version publique fonctionne environ 2 fois plus lentement, peut scintiller ou dériver, et signale des images très bruitées dans environ 2 % des cas.

## Points non élucidés {#still-unknown}

- Aucune source primaire n'attribue de changement de produit distinct spécifiquement au 2026-03-28. Le dépôt officiel date la version publique du 2026-03-19. Nous considérons le 2026-03-28 comme la confirmation de la disponibilité, et non comme une version distincte du modèle.
- Le dépôt public indique que des comparaisons quantitatives avec le modèle interne de l'article seront publiées dans une mise à jour ultérieure ; aucune comparaison de ce type n'a été vérifiée ici.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://hjrphoebus.github.io/X-Dub/ | X-Dub: From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |
| https://github.com/KlingAIResearch/X-Dub | KlingAIResearch/X-Dub — dépôt officiel | 2026-09-05 |
| https://huggingface.co/KlingTeam/X-Dub | KlingTeam/X-Dub — fiche du modèle et poids | 2026-09-05 |
| https://arxiv.org/abs/2512.25066 | From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |

## Résumé pour agents {#agent-brief}

- **Sujet :** `project:x-dub`, fil `project-development`, 1 événement daté du 2026-03-28 au 2026-03-28.
- **Remarque pratique :** Depuis le 2026-03-28, les praticiens doivent consulter le site du projet X-Dub, le dépôt GitHub et la page Hugging Face pour évaluer le projet ou trouver ses ressources publiques ; ces éléments ne permettent pas d'établir une procédure d'installation ou d'utilisation spécifique.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
