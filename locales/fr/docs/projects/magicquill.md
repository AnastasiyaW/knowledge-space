---
title: "MagicQuill"
category: projects
date: 2024-11-18
tags: [magicquill, magicquill-development, magicquill_pinokio, project]
aliases: ["MagicQuill"]
level: 3
source_sha256: 83bffc3f42b96e1320c0be817b465e6ba4602b3177089269d5918bac76a7519f
translation: machine
translated_at: '2026-10-24'
---
# MagicQuill {#magicquill}

**Ligne de développement :** `project:magicquill` · fil `magicquill-development`  
**Dernier événement :** 2024-11-18 · 1 événement daté depuis le 2024-11-18 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

MagicQuill est un éditeur d'images de recherche destiné aux artistes qui ont besoin d'un contrôle local dépassant l'inpainting guidé par prompt seul.

- La V2 contrôle le contenu, le placement, la structure et la couleur à l'aide de calques visuels, en ajoutant un pinceau d'édition locale, des accessoires de premier plan et une segmentation SAM.
- La V1 contrôle les ajouts, les suppressions et les modifications de couleur au pinceau, Draw&Guess suggérant des prompts à partir de croquis.

## Ligne de développement {#development-line}

- **2024-11-18 — La démo publique de MagicQuill, le dépôt source et le Space hébergé ont été rendus accessibles.** La page du projet, le code source et la démo Hugging Face constituaient les points d'entrée publics pour les praticiens.

## Évolutions {#what-changed}

- 2024-11-14 — MagicQuill V1 : la prépublication arXiv a défini l'éditeur à trois pinceaux et l'assistant de prompts Draw&Guess.
- 2024-11-18 — MagicQuill V1 : la page du projet, le code source et la démo Hugging Face constituaient les points d'entrée publics pour les praticiens.
- 2024-11-21 — MagicQuill V1 : la gestion des chemins Windows, le comportement de sauvegarde et les scripts d'installation `.bat`/`.sh` ont été mis à jour.
- 2024-11-25 — MagicQuill V1 : le glisser-déposer d'images et un bouton de téléchargement ont été ajoutés.
- 2024-12-06 — MagicQuill V1 : la sauvegarde automatique et les contrôles de résolution ont été ajoutés.
- 2024-12-07 — MagicQuill V1 : un nœud personnalisé ComfyUI a été publié.
- 2024-12-16 — MagicQuill V1 : un déploiement ModelScope a été ajouté.
- 2025-01-02 — MagicQuill V1 : une voie de déploiement par conteneur Docker a été ajoutée.
- 2025-02-24 — MagicQuill : une route de lancement Pinokio a été référencée ; son état historique du paquet ne peut pas être reconstitué à partir du point d'accès fourni.
- 2025-02-27 — MagicQuill V1 : l'article a été accepté à CVPR 2025.
- 2025-12-02 — MagicQuill V2 : l'article sur les indices visuels en calques a été soumis à arXiv.
- 2025-12-03 — MagicQuill V2 : le système publié est passé de l'interaction au seul pinceau de la V1 à des calques de contenu, spatiaux, structurels et de couleur, sur Flux Kontext.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-11-18, les praticiens pouvaient évaluer MagicQuill via sa démo publique et son Space hébergé, tout en utilisant le dépôt lié pour examiner l'implémentation avant adoption.

1. Utilisez le Space Hugging Face V2 en fonctionnement lorsqu'aucun GPU local disposant d'environ 40 Go de VRAM n'est disponible.
  — <https://huggingface.co/spaces/AI4Editing/MagicQuillV2>
2. Pour la V2 en local, utilisez le dépôt actif `zliucz/MagicQuillV2`, créez un environnement Python 3.10 et installez ses dépendances.
  — <https://github.com/zliucz/MagicQuillV2>
3. Téléchargez `LiuZichen/MagicQuillV2-models` dans `models/`, puis lancez l'interface avec `python app.py`.
  — <https://huggingface.co/LiuZichen/MagicQuillV2-models>
4. Dans la V2, isolez un accessoire de premier plan avec SAM, placez-le via le Visual Cue Manager, puis utilisez les contrôles d'édition locale, de contours, de couleur ou de suppression pour le calque concerné.
  — <https://magicquill.art/v2/>
5. Pour un GPU de 8 Go, utilisez la V1 : clonez récursivement afin que le sous-module LLaVA soit présent, récupérez les points de contrôle, puis exécutez `python gradio_run.py`.
  — <https://github.com/magic-quill/magicquill>

## Bonnes pratiques {#best-practices}

- Considérez Draw&Guess comme une suggestion et remplacez son prompt lorsque un croquis est ambigu.
  — <https://arxiv.org/abs/2411.09703>
- Pour la V1, abaissez Edge Strength lorsqu'un tracé grossier entre en conflit avec le prompt ; réduisez l'opacité/l'intensité de la couleur lorsque la colorisation supprime trop de détails.
  — <https://arxiv.org/abs/2411.09703>
- Choisissez la V1 plutôt que de forcer la V2 sur du matériel à mémoire limitée : la configuration requise annoncée pour la V2 est d'environ 40 Go de VRAM, tandis que la V1 est l'option documentée à moindres ressources.
  — <https://github.com/zliucz/MagicQuillV2>
- Clonez la V1 avec `--recursive` ; sans cela, son sous-module LLaVA requis est absent.
  — <https://github.com/magic-quill/magicquill>
- Considérez l'installateur Pinokio comme du code tiers et examinez-le avant utilisation : son script actuel clone `6Morpheus6/MagicQuill`, et non le dépôt canonique.
  — <https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js>
- Vérifiez que la licence CC BY-NC 4.0 convient à l'usage prévu avant d'utiliser l'une ou l'autre implémentation dans un cadre commercial.
  — <https://github.com/zliucz/MagicQuillV2>

## Remplacé par {#superseded-by-this}

- 2025-12-03 — MagicQuill V2 remplace la V1 comme ligne de capacités active, mais la V1 reste la voie documentée à faible VRAM et n'est pas universellement obsolète.
- 2026-09-04 — L'ancienne cible de clonage du README V2 est périmée : la route `magic-quill/MagicQuillV2` observée renvoie une erreur 404 ; utilisez le dépôt actif `zliucz/MagicQuillV2`.
- 2026-09-04 — Pinokio ne doit pas être considéré comme une référence officielle pour les modèles MagicQuill ; son installateur actuel est un wrapper tiers autour d'un fork non canonique.

## Points non élucidés {#still-unknown}

- Le contenu de la page Pinokio du 2025-02-24 n'est pas récupérable à partir de l'URL fournie : elle redirige vers le site général de Pinokio, ce qui laisse non confirmées la révision de l'installateur et son comportement à cette date.
- La route `/demo/` de la V1 n'a renvoyé aucun contenu de page exploitable, et son Space Hugging Face affiche « Running on Zero » ; la complétion d'une édition en direct n'a pas été testée de manière indépendante.
- Pinokio est une voie de lancement et non un second modèle MagicQuill ; son lien précis avec l'événement du 2025-02-24 reste non confirmé.
- Les pages GitHub des V1 et V2 ne présentent aucune version logicielle immuable ; les dates du journal de mise à jour des README constituent donc les seuls indices de publication disponibles.
- Les configurations matérielles annoncées pour la V1 et la V2 sont des exigences déclarées par les auteurs, et non des benchmarks indépendants.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://magicquill.art/demo/ | Démo MagicQuill | 2026-09-04 |
| https://github.com/magic-quill/magicquill | Dépôt MagicQuill V1 | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuill | Space Hugging Face MagicQuill V1 | 2026-09-04 |
| https://pinokio.computer/ | Pinokio | 2026-09-04 |
| https://arxiv.org/abs/2411.09703 | MagicQuill: An Intelligent Interactive Image Editing System | 2026-09-04 |
| https://github.com/pinokiofactory/MagicQuill | Dépôt Pinokio MagicQuill | 2026-09-04 |
| https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js | Script d'installation Pinokio MagicQuill | 2026-09-04 |
| https://github.com/magic-quill/MagicQuillV2 | Ancienne route de clonage GitHub MagicQuillV2 | 2026-09-04 |
| https://github.com/zliucz/MagicQuillV2 | Dépôt MagicQuill V2 | 2026-09-04 |
| https://arxiv.org/abs/2512.03046 | MagicQuillV2: Precise and Interactive Image Editing with Layered Visual Cues | 2026-09-04 |
| https://magicquill.art/v2/ | Page du projet MagicQuill V2 | 2026-09-04 |
| https://huggingface.co/LiuZichen/MagicQuillV2-models | Fiche modèle MagicQuill V2 | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuillV2 | Space Hugging Face MagicQuill V2 | 2026-09-04 |

## Résumé pour l'agent {#agent-brief}

- **Sujet :** `project:magicquill`, fil `magicquill-development`, 1 événement daté du 2024-11-18 au 2024-11-18.
- **Note pratique :** À partir du 2024-11-18, les praticiens pouvaient évaluer MagicQuill via sa démo publique et son Space hébergé, tout en utilisant le dépôt lié pour examiner l'implémentation avant adoption.
- **Confiance :** moyenne. Les remplacements datés font foi pour déterminer ce qui est obsolète.
