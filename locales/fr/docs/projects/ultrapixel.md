---
title: "UltraPixel"
category: projects
date: 2024-09-20
tags: [project, ultrapixel, ultrapixel-development]
aliases: ["UltraPixel"]
level: 2
source_sha256: 6ddf3572fa026772845d82be11a3203189ae6daa51563debe3626bdf22ddfe82
translation: machine
translated_at: '2026-10-24'
---
# UltraPixel {#ultrapixel}

**Ligne de développement :** `project:ultrapixel` · fil `ultrapixel-development`  
**Dernier événement :** 2024-09-20 · 2 entrées datées depuis 2024-07-09 · **Consulté :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

UltraPixel — une implémentation de recherche présentée à NeurIPS 2024, fondée sur Stable Cascade, pour la génération d'images à partir de texte à plusieurs résolutions élevées.

- génère des images à travers les étapes de Stable Cascade, avec un guidage sémantique à basse résolution ;
- prend en charge le text-to-image, un exemple de chat personnalisé fourni, et ControlNet Canny ;
- dispose d'un wrapper ComfyUI communautaire avec des workflows fournis.

Les chiffres publiés pour une RTX 4090 de 24 Go situent une génération en 4096×4096 à travers les étapes C, B et A (tuilée) à environ 311 secondes au total. Verdict : utilisable pour des expérimentations locales en haute résolution, mais sa démo officielle tourne actuellement sur Zero et aucun fournisseur d'inférence managé n'est référencé.

## Ligne de développement {#development-line}

- **2024-07-09 — La page du projet UltraPixel a été partagée.** Le 2024-07-09, une publication datée sur UltraPixel renvoyait vers le site du projet. Il s'agit de la plus ancienne référence publique visible pour le projet dans la ligne de développement clôturée. Le texte d'annonce d'origine et les affirmations techniques n'ont pas été fournis.
- **2024-09-20 — Le dépôt UltraPixel et la démo hébergée ont été partagés.** Le 2024-09-20, une publication datée sur UltraPixel renvoyait vers un dépôt GitHub et un Space Hugging Face, accompagnée d'un lien vers le précédent « The recorded link ». Cela enregistre les points d'entrée publics vers la source et la démo du projet dans la ligne clôturée. Les éléments disponibles n'établissent pas l'état exact de la publication, les modifications de code ni la formulation de l'annonce.

## Ce qui a changé {#what-changed}

2024-07-09 — UltraPixel a été présenté comme une méthode de diffusion en cascade pour la génération d'images à partir de texte de 1K à 6K, utilisant un guidage à basse résolution, des représentations neuronales implicites et une normalisation sensible à l'échelle. 2024-09-20 — l'implémentation exécutable et la démo hébergée sont devenues disponibles ; la version fournit l'inférence locale via Gradio et par script, le téléchargement des modèles, ainsi que les chemins ControlNet et de personnalisation.

## Mode d'emploi {#how-to-use-this}

Depuis le 2024-09-20, les praticiens doivent utiliser le dépôt GitHub et le Space Hugging Face liés comme points d'entrée enregistrés de la source et de la démo d'UltraPixel. Les affirmations techniques et l'état exact de la publication doivent être considérés comme non vérifiés tant que les ressources liées n'ont pas été examinées.

1. Installez les dépendances du dépôt, téléchargez les poids Stable Cascade requis ainsi que les paramètres d'UltraPixel, puis placez-les dans le répertoire des modèles du dépôt.
  — <https://github.com/catcathh/UltraPixel>
2. Lancez l'interface Gradio avec CUDA_VISIBLE_DEVICES=0 python app.py, ou utilisez inference/test_t2i.py pour une génération text-to-image scriptée.
  — <https://github.com/catcathh/UltraPixel>
3. Pour ComfyUI, clonez le nœud communautaire dans custom_nodes, installez ses dépendances, chargez workflow_default.json ou workflow_controlnet.json, puis mettez le prompt en file d'attente ; au premier lancement, les modèles sont téléchargés dans ComfyUI/models/ultrapixel.
  — <https://github.com/2kpr/ComfyUI-UltraPixel>

## Bonnes pratiques {#best-practices}

- Utilisez stage_a_tiled pour le décodage de l'étape A lorsque la VRAM est limitée ; cela évite le dépassement de mémoire documenté en 4096×4096 sur une RTX 4090 de 24 Go, au prix d'un temps de calcul nettement plus long.
  — <https://github.com/catcathh/UltraPixel>
- Utilisez un prompt qui précise le sujet, l'arrière-plan, la couleur, l'éclairage et l'ambiance ; considérez les modificateurs de qualité comme des essais facultatifs et non comme une garantie.
  — <https://github.com/catcathh/UltraPixel>
- Restez dans le plafond 4K documenté pour ControlNet, sauf si vous affinez les poids de contrôle ; la configuration publiée cite 3840×2160 et 2048×2048.
  — <https://github.com/catcathh/UltraPixel>

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-09-19 — le chiffre antérieur du dépôt, d'environ trois minutes sur RTX 4090 pour une génération en 2560×5120, a été remplacé par une valeur d'environ 60 secondes après la mise à jour de son environnement PyTorch et Torchvision.
- 2024-09-26 — le statut d'UltraPixel est passé d'implémentation de preprint à article accepté à NeurIPS 2024.

## Points toujours inconnus {#still-unknown}

- Le dépôt GitHub officiel déclare une licence AGPL-3.0, tandis que la fiche du modèle sur Hugging Face déclare Apache-2.0 ; les sources examinées n'expliquent pas quelle licence s'applique à un déploiement combiné. Vérifiez ce point avant toute utilisation commerciale.
- La page de démo publique indique qu'elle tourne sur Zero ; cela n'établit pas que le Space est durablement indisponible, seulement qu'aucune session hébergée active n'était disponible au moment de la vérification.
- Aucune intégration ComfyUI actuelle, maintenue par les auteurs, n'a été trouvée. Le nœud ComfyUI disponible se présente comme un travail en cours et se décrit comme un wrapper modifié.
- Aucune source de fonctionnement en chinois, qu'elle soit officielle ou communautaire, n'a été vérifiée pour cet élément.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://jingjingrenabc.github.io/ultrapixel/ | UltraPixel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2407.02158 | UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks | 2026-09-05 |
| https://github.com/catcathh/UltraPixel | catcathh/UltraPixel | 2026-09-05 |
| https://huggingface.co/roubaofeipi/UltraPixel | roubaofeipi/UltraPixel model card | 2026-09-05 |
| https://huggingface.co/spaces/roubaofeipi/UltraPixel-demo | roubaofeipi/UltraPixel-demo | 2026-09-05 |
| https://github.com/2kpr/ComfyUI-UltraPixel | 2kpr/ComfyUI-UltraPixel | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ultrapixel`, fil `ultrapixel-development`, 2 événements datés du 2024-07-09 au 2024-09-20.
- **Note pratique :** Depuis le 2024-09-20, les praticiens doivent utiliser le dépôt GitHub et le Space Hugging Face liés comme points d'entrée enregistrés de la source et de la démo d'UltraPixel. Les affirmations techniques et l'état exact de la publication doivent être considérés comme non vérifiés tant que les ressources liées n'ont pas été examinées.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
