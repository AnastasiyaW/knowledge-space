---
title: "Qwen-Image-Edit-Rapid-AIO"
category: projects
date: 2025-12-29
tags: [project, qwen-image-edit-rapid-aio, qwen_image_edit_rapid_aio]
aliases: ["Qwen-Image-Edit-Rapid-AIO"]
level: 3
source_sha256: b71545247048c73c4a3ede919ac1027699acc89425fab3eddbd76029fe13ddf3
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Image-Edit-Rapid-AIO {#qwen-image-edit-rapid-aio}

**Ligne de développement :** `project:qwen-image-edit-rapid-aio` · fil `qwen-image-edit-rapid-aio`  
**Dernier événement :** 2025-12-29 · 2 événements datés depuis 2025-10-07 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Qwen-Image-Edit-Rapid-AIO fusionne en un seul checkpoint les accélérateurs de vitesse, le VAE et le CLIP de Qwen-Image-Edit, à l'intention des utilisateurs de ComfyUI.

- Génération d'image à partir de texte sans image d'entrée
- Édition d'image guidée par texte avec plusieurs images d'entrée
- Variantes SFW et NSFW

Le workflow s'exécute en 4 étapes avec un CFG de 1 ; la v18 pèse 28,4 Go par variante.

Il convient à l'édition locale rapide et à la génération d'image à partir de texte, mais il ne s'agit pas d'une version officielle de Qwen, et l'auteur ne publiera pas de nouvelles versions.

## Ligne de développement {#development-line}

- **2025-10-07 — Référence du dépôt public pour Qwen-Image-Edit-Rapid-AIO.** La v1 d'origine combinait Qwen-Image-Edit-2509 et Lightning v2.0 à 4 étapes.
- **2025-12-29 — Ressources v18 et références de workflow pour Qwen-Image-Edit-Rapid-AIO.** Le 2025-12-29, le dépôt a enregistré des liens vers son répertoire v18, un workflow JSON Qwen-Rapid-AIO et une distribution GGUF associée. Ces liens datés confirment une distribution et une référence de workflow ultérieures, mais ils ne prouvent ni les modifications exactes, ni la compatibilité, ni les performances de la v18.

## Modifications {#what-changed}

- 2025-10-07 : apparition du premier checkpoint Rapid-AIO ; la v1 d'origine combinait Qwen-Image-Edit-2509 et Lightning v2.0 à 4 étapes.
- 2025-12-29 : la v18 a été scindée en variantes SFW et NSFW distinctes ; le miroir GGUF a ajouté les quantifications SFW Q4_K et Q5_K.
- 2026-01-08 : sortie de la v19.
- 2026-01-24 : sortie de la v23. L'auteur a indiqué par la suite que la v19 offre une meilleure cohérence d'édition et que la v23 suit mieux les prompts complexes, puis a cessé les mises à jour.

## Mode d'emploi {#how-to-use-this}

Au 2025-12-29, commencez l'évaluation à partir des ressources du dépôt v18 et du workflow JSON, et vérifiez les sources avant de vous fier aux affirmations sur la disponibilité, la compatibilité ou la qualité des GGUF.

1. Téléchargez le checkpoint Rapid-AIO choisi et placez-le dans le dossier checkpoints de ComfyUI.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>
2. Importez le workflow JSON fourni ; il utilise CheckpointLoaderSimple, TextEncodeQwenImageEditPlus, KSampler et VAE Decode.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
3. Connectez une ou deux images source aux entrées d'image facultatives, ou laissez-les vides pour une génération à partir de texte ; définissez le prompt dans TextEncodeQwenImageEditPlus.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
4. Exécutez avec 4 étapes, CFG 1, le sampler sa_solver et le scheduler beta, tels que définis dans le workflow.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
5. Pour un téléchargement plus léger, utilisez la variante GGUF correspondante et un chargeur GGUF compatible au lieu du chargeur de checkpoint standard.
  — <https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main>

## Bonnes pratiques {#best-practices}

- Commencez par le workflow fourni et ses réglages de 4 étapes/CFG 1 ; ne reprenez pas aveuglément les paramètres standard de Qwen-Image-Edit.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- Pour les éditions, décrivez la modification précise et transmettez la source à l'entrée d'image ; pour la génération à partir de texte, laissez l'entrée d'image vide.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- Si des problèmes apparaissent, réduisez d'abord les entrées volumineuses : le workflow officiel de Qwen-Image-Edit ramène l'entrée à environ un million de pixels afin d'éviter une perte de qualité sur les images surdimensionnées.
  — <https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit>
- Préférez la v19 à la v23 pour des éditions cohérentes ; la v23 est utile lorsque le respect d'instructions complexes prime.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>

## Remplacé par {#superseded-by-this}

- 2025-12-29 : les quantifications GGUF Q4_K/Q5_K SFW de la v18 ont étendu les quantifications NSFW antérieures de la v18.
- 2026-01-24 : la v23 est la dernière version publiée, mais elle ne remplace pas la v19 lorsque la cohérence de l'édition est plus importante.

## Points inconnus {#still-unknown}

- Rapid-AIO est un checkpoint communautaire, et non une version officielle de Qwen-Image-Edit ; les capacités du modèle de base ne peuvent pas être présumées pour chaque fusion Rapid-AIO.
- Le journal du dépôt pour l'événement du 2025-10-07 ne conserve pas la date du commit d'origine de la première version v1 ; la fiche du modèle confirme la description de la v1, mais sa date historique reste la date de l'événement.
- L'URL Hugging Face pour GGUF redirige de Arunk25 vers Novice25 ; cela ressemble à un renommage ou à un transfert de compte, mais la raison n'est pas confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO | Fiche du modèle Phr00t/Qwen-Image-Edit-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/commits/main | Historique des commits de Phr00t/Qwen-Image-Edit-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/tree/main/v18 | Fichiers v18 de Phr00t/Qwen-Image-Edit-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json | Workflow ComfyUI Qwen-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main | Fichiers de Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/commits/main/v18 | Historique des commits v18 de Novice25 Qwen-Image-Edit-Rapid-AIO-GGUF | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit | Exemple de workflow natif ComfyUI pour Qwen-Image-Edit | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:qwen-image-edit-rapid-aio`, fil `qwen-image-edit-rapid-aio`, 2 événements datés du 2025-10-07 au 2025-12-29.
- **Note pratique :** Au 2025-12-29, évaluez d'abord les ressources du dépôt v18 et le workflow JSON, et vérifiez les sources avant de vous fier aux affirmations sur la disponibilité, la compatibilité ou la qualité des GGUF.
- **Confiance :** élevée. Les remplacements datés ci-dessus déterminent ce qui est obsolète.
