---
title: "DDColor"
category: projects
date: 2024-01-15
tags: [ddcolor, ddcolor-development, project]
aliases: ["DDColor"]
level: 3
source_sha256: ced4ea966cacc4b53f8d393c47057eaf4a8f7fc032baadb50f563500edfe5db2
translation: machine
translated_at: '2026-10-24'
---
# DDColor {#ddcolor}

**Ligne de développement :** `project:ddcolor` · fil `ddcolor-development`  
**Dernier événement :** 2024-01-15 · 1 événement daté depuis le 2024-01-15 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

DDColor est un modèle PyTorch issu de ICCV 2023 pour la colorisation automatique de photos.

- Photos monochromes : les colorise automatiquement.
- Canaux en niveaux de gris : recolore des images couleur existantes à partir de ces canaux.
- Déploiement : s'exécute via des scripts locaux, Hugging Face, ModelScope, Gradio ou un export ONNX.

## Ligne de développement {#development-line}

- **2024-01-15 — Le dépôt source de DDColor et le workflow Colab ont été reliés.** Camenduru a publié des notebooks Colab et Gradio-Colab pointant vers le code canonique de DDColor. Il s'agissait d'un wrapper communautaire, et non d'une publication du modèle principal.

## Ce qui a changé {#what-changed}

Les deux voies de janvier 2024 étaient des wrappers autour du même modèle, suivies d'options d'inférence officielles.

- 2024-01-15 : Camenduru a publié des notebooks Colab et Gradio-Colab pointant vers le code canonique de DDColor, en tant que wrapper communautaire et non comme publication du modèle principal.
- 2024-01-22 : le Space Old Photo Restoration de ModelScope utilisait `iic/cv_ddcolor_image-colorization` derrière une interface d'envoi et de curseur, ce qui confirme une intégration de DDColor plutôt qu'un modèle de restauration distinct.
- Les mises à jour officielles ont ajouté l'intégration Hugging Face le 2024-01-26, un correctif le 2024-01-29, la prise en charge de l'export ONNX le 2024-10-25, une refonte de l'inférence locale ne reposant pas sur BasicSR le 2024-12-31, et un chargement et une inférence simplifiés le 2026-01-17.

## Comment l'utiliser {#how-to-use-this}

Nous pouvons travailler avec DDColor à partir du dépôt source et de son workflow Colab depuis le 2024-01-15. Vérifiez le workflow pris en charge dans ces ressources avant de l'exécuter.

1. Créez l'environnement Python 3.9 documenté, puis installez PyTorch 2.2.0 avec CUDA 11.8 ainsi que `requirements.txt`. La voie d'inférence locale ne nécessite pas BasicSR.
  — <https://github.com/piddnad/DDColor>
2. Commencez par `ddcolor_modelscope` pour les images ordinaires hors ImageNet. Utilisez `ddcolor_paper` uniquement pour reproduire les résultats de l'article, `ddcolor_artistic` pour un résultat alternatif, ou `ddcolor_paper_tiny` lorsque l'empreinte mémoire est critique.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
3. Exécutez `python scripts/infer.py --model_name ddcolor_modelscope --input ./assets/test_images`. Sinon, téléchargez le checkpoint ModelScope et transmettez son `pytorch_model.pt` via `--model_path`.
  — <https://github.com/piddnad/DDColor>
4. Pour une intégration Python, créez un pipeline ModelScope `Tasks.image_colorization` avec `iic/cv_ddcolor_image-colorization`, transmettez une image, puis enregistrez `OutputKeys.OUTPUT_IMG`.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
5. Lancez `python demo/gradio_app.py` en local lorsqu'une interface d'envoi est nécessaire.
  — <https://github.com/piddnad/DDColor>

## Bonnes pratiques {#best-practices}

- Utilisez `ddcolor_modelscope` par défaut pour les images hors ImageNet. Réservez le modèle de l'article à la reproduction plutôt qu'à un usage général.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Comparez avec `ddcolor_artistic` lorsque les artefacts de couleur posent problème, car son entraînement a omis la perte de colorfulness. Utilisez `ddcolor_paper_tiny` lorsque l'empreinte mémoire est critique.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Examinez avec soin les bandes dessinées, les entrées basse résolution et les images bruitées, car le modèle a été entraîné sur des photos naturelles.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
- N'utilisez pas le Space Old Photo Restoration hébergé comme point d'entrée actuel. Il renvoie une erreur d'exécution causée par un téléchargement incomplet de la configuration du modèle.
  — <https://huggingface.co/spaces/modelscope/old_photo_restoration>

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-01-15 — Consignes de configuration réservées à Colab : les voies officielles de scripts locaux, Hugging Face, ModelScope, Gradio et ONNX les remplacent.
- 2024-01-22 — Démo hébergée du Space Old Photo Restoration : obsolète, car elle renvoie une erreur d'exécution.
- 2024-12-31 — Inférence locale dépendant de BasicSR : la voie actuelle des scripts locaux ne nécessite pas BasicSR.

## Points encore inconnus {#still-unknown}

- Le texte du lien enregistré était inaccessible ; son affirmation éditoriale et la comparaison visée n'ont donc pas pu être vérifiées.
- Les sources ne précisent pas si l'identifiant historique ModelScope `iic/cv_ddcolor_image-colorization` et l'identifiant actuel du dépôt `damo/cv_ddcolor_image-colorization` sont des alias ou une migration. Ne supposez pas qu'ils sont interchangeables.
- Aucune exécution d'inférence locale actuelle, mesure matérielle ni benchmark face à un colorisateur plus récent n'a été vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/piddnad/DDColor | DDColor — implémentation PyTorch officielle | 2026-09-04 |
| https://github.com/piddnad/DDColor/commits/master/ | Historique des commits de DDColor | 2026-09-04 |
| https://github.com/camenduru/DDColor-colab | camenduru/DDColor-colab | 2026-09-04 |
| https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md | DDColor Model Zoo | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration | Old Photo Restoration — un Space Hugging Face de modelscope | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration/blob/main/app.py | Old Photo Restoration app.py | 2026-09-04 |
| https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary | DDColor pour la colorisation d'images | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:ddcolor`, fil `ddcolor-development`, 1 événement daté du 2024-01-15 au 2024-01-15.
- **Note pratique :** Nous pouvons commencer le travail sur DDColor à partir du dépôt source et du workflow Colab liés, depuis le 2024-01-15. Vérifiez le workflow exact pris en charge dans ces ressources avant utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
