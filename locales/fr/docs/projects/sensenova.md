---
title: "SenseNova — Modèle U1 MoT et artefacts infographiques"
category: projects
date: 2026-08-01
tags: [project, sensenova, u1-mot-model-and-infographic]
aliases: ["SenseNova"]
level: 3
source_sha256: 34844dcc2b5bc41e4640f26d59e514aee4f4e3bcb41f3917925c275d8be06844
translation: machine
translated_at: '2026-10-24'
---
# SenseNova — Modèle U1 MoT et artefacts infographiques {#sensenova-u1-mot-model-and-infographic-artifacts}

**Ligne de développement :** `project:sensenova` · fil `u1-mot-model-and-infographic`  
**Dernier événement :** 2026-08-01 · 1 événement daté depuis le 2026-08-01 · **Recherche effectuée :** 2026-09-06 · confiance : élevée

## Présentation {#what-it-is}

SenseNova U1 est une famille de modèles OpenSenseNova sous licence Apache-2.0, destinée aux praticiens qui exécutent la création visuelle en local.

Capacités :
- Génération d'images à partir de texte.
- Édition d'images.
- Génération entrelacée d'images et de texte.
- Compréhension visuelle.

La fiche actuelle de U1.5-8B-MoT indique 18B de paramètres en BF16 et aucun Hugging Face Inference Provider. Utilisez U1.5 pour la création et l'édition générales, et Infographic-V3 uniquement pour les travaux spécifiques aux infographies.

## Ligne de développement {#development-line}

- **2026-08-01 — SenseNova a relié les artefacts U1 MoT en préversion et infographiques sur Hugging Face.** Le 2026-08-01, SenseNova a ajouté des liens vers les pages Hugging Face et les Spaces de SenseNova-U1.5-8B-MoT-Preview et de SenseNova-U1-8B-MoT-Infographic-V3. Ces liens marquent une étape pour le modèle et la démonstration. Ils n'établissent ni le statut de publication, ni les modifications techniques, ni les capacités des artefacts.

## Modifications {#what-changed}

- 2026-07-16 — SenseNova-U1-8B-MoT-Infographic-V3 a ajouté la génération et l'édition intégrées d'infographies : contenu textuel local et modifications globales de style et de mise en page.
- 2026-08-01 — SenseNova-U1.5-8B-MoT-Preview était une préversion du 31 juillet destinée à une génération et une édition plus larges ; elle a été associée à la fiche V3 antérieure, et non publiée en même temps que celle-ci.
- 2026-08-04 — Un GGUF Q8 de 19,9 Go, maintenu par la communauté, a facilité l'exécution de la préversion sans modifier les poids officiels.
- 2026-08-20 — SenseNova-U1.5-8B-MoT est devenu la version officielle actuelle ; son LoRA 8 étapes correspondant a ouvert une voie plus rapide.
- 2026-09-01 — Un GGUF Q8 communautaire de 21,2 Go est apparu pour le point de contrôle final de U1.5.

## Mode d'emploi {#how-to-use-this}

1. Pour une évaluation sans installation, ouvrez le playground SenseNova-Studio lié à la fiche U1.5 actuelle ; considérez-le comme un test de flux de travail et non comme une preuve de performance en production.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
2. Pour une utilisation locale, clonez OpenSenseNova/SenseNova-U1, exécutez uv sync dans son environnement, et utilisez le chemin de modèle U1.5-8B-MoT avec le point d'entrée de génération texte-image ou d'édition d'images.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
3. Choisissez un palier de résolution sur lequel le modèle a été entraîné, et configurez device_map ou le mode VRAM du projet avant d'augmenter la résolution ou la taille de lot.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
4. Pour la génération ou l'édition d'infographies, sélectionnez SenseNova-U1-8B-MoT-Infographic-V3 plutôt que de supposer que le point de contrôle U1.5 général possède la même spécialisation ; le Space sensenova est une voie interactive V3.
  — <https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3>

## Bonnes pratiques {#best-practices}

- Utilisez une invite directe pour une tâche claire avec peu de contraintes. Utilisez Image PE pour une composition complexe, du texte, des nombres, une mise en page ou une planification de références, et variez les graines lorsque la diversité compte.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- Pour une édition complexe, énoncez la modification demandée ainsi que tout ce qui doit rester inchangé. Ordonnez délibérément plusieurs images de référence et décrivez le rôle de chaque image.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- Privilégiez les paliers de résolution documentés d'environ 2K. Des combinaisons arbitraires de largeur et hauteur peuvent réduire la qualité.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
- Vérifiez manuellement les textes denses, le nombre exact d'éléments et la mise en page, l'anatomie, ainsi que les éditions larges à références multiples. Abaissez cfg_scale lorsque le détail ou la couleur sont trop accentués.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-20 — Considérer SenseNova-U1.5-8B-MoT-Preview comme le point de contrôle U1.5 généraliste actuel est obsolète.

## Points encore inconnus {#still-unknown}

- SenseNova est une marque plus large de SenseTime ; le matériel vérifié identifie la famille OpenSenseNova U1 mais n'établit pas que U1.5 soit le même produit que SenseNova 6.x commercial ou U1 Pro.
- La démonstration de la préversion appartient à hugging-apps et non à sensenova ; sa page accessible ne prouve pas quel point de contrôle elle exécute actuellement, sa disponibilité, ni un engagement de service en production.
- Les sources revendiquent un rendu natif en 4K, mais les exemples vérifiés documentent des paliers d'entraînement d'environ 2K et aucun résultat de qualité indépendant en 3840x2160 pour une charge de production précise.
- Aucune tarification actuelle de l'API hébergée, aucun SLA ni aucun Hugging Face Inference Provider n'ont été vérifiés pour le point de contrôle U1.5 final.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-Preview | sensenova/SenseNova-U1.5-8B-MoT-Preview | 2026-09-06 |
| https://huggingface.co/spaces/hugging-apps/sensenova-sensenova-u1-5-8b-mot-preview | SenseNova-U1.5-8B-MoT (Preview) - a Hugging Face Space by hugging-apps | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | 2026-09-06 |
| https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3 | SenseNova U1 Infographic V3 - a Hugging Face Space by sensenova | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1 | OpenSenseNova/SenseNova-U1: SenseNova-U series with NEO-unify | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT | sensenova/SenseNova-U1.5-8B-MoT | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md | SenseNova-U1.5 Cookbook | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md | SenseNova-U1 reference inference examples | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:sensenova`, fil `u1-mot-model-and-infographic`, 1 événement daté du 2026-08-01 au 2026-08-01.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
