---
title: "CutLER"
category: projects
date: 2024-03-11
tags: [cutler, cutler-development, project]
aliases: ["CutLER", "VideoCutLER"]
level: 3
source_sha256: e5f70c51bdd22ee22e0391fc4b1ed27f06bdd3d3f8a01a6e5e74f8325232b7d6
translation: machine
translated_at: '2026-10-24'
---
# CutLER {#cutler}

**Ligne de développement :** `project:cutler` · fil `cutler-development`  
**Dernier événement :** 2024-03-11 · 2 événements datés depuis 2023-03-01 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

CutLER est un pipeline de conversion de pseudo-masques en détecteur pour la détection d'objets non supervisée et la segmentation d'instances.

- MaskCut génère des pseudo-masques à instances multiples.
- CutLER entraîne des détecteurs et des segmenteurs d'images à partir de ces masques.
- VideoCutLER transforme des paires d'images en trajectoires vidéo synthétiques, puis entraîne la segmentation d'instances vidéo sans annotations humaines, sans vidéo naturelle et sans flux optique.

La configuration cible Linux/macOS, Python 3.8+, PyTorch 1.8+, Detectron2 et OpenCV 4.6+ ; le dépôt ne comporte aucune version étiquetée.

Nous pouvons l'utiliser comme code de recherche ou comme référence reproductible. Testez la pile de dépendances historique avant de vous engager dans l'entraînement.

## Ligne de développement {#development-line}

- **2023-03-01 — Les ressources du projet CutLER sont devenues disponibles.** MaskCut produit des pseudo-masques, puis CutLER apprend la détection d'objets et la segmentation d'instances à partir d'ImageNet-1K, sans annotations humaines.
- **2024-03-11 — La documentation de VideoCutLER a étendu la ligne du projet CutLER.** MaskCut → ImageCut2Video → entraînement de modèles vidéo, étendant le projet au suivi de multiples instances à travers les images.

## Ce qui a changé {#what-changed}

2023-03-01 — CutLER a établi le flux de travail sur images : MaskCut produit des pseudo-masques, puis CutLER apprend la détection d'objets et la segmentation d'instances à partir d'ImageNet-1K, sans annotations humaines.

2023-08-27–29 — L'historique Git officiel place l'ajout du code VideoCutLER avant l'événement documentaire ultérieur, dans des commits intitulés « Add videocutler. ».

2024-03-02 — L'historique officiel recense deux autres commits VideoCutLER, mais leurs messages succincts n'établissent aucune modification fonctionnelle précise.

2024-03-11 — VideoCutLER est documenté comme un flux de travail vidéo distinct : MaskCut → ImageCut2Video → entraînement de modèles vidéo, étendant le projet au suivi de multiples instances à travers les images.

2025-06-03–04 — En amont, les liens vers les points de contrôle de VideoCutLER et son README ont été mis à jour. Aucune version étiquetée n'est disponible.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-03-01, les praticiens pouvaient utiliser le dépôt CutLER, l'espace MaskCut et les ressources Colab pour évaluer le projet. À partir du 2024-03-11, consultez la documentation de VideoCutLER lorsque le cas d'usage concerne la vidéo.

1. Installez la pile locale documentée : Linux ou macOS, PyTorch/torchvision compatibles et Detectron2. Clonez CutLER récursivement et installez ses dépendances.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
2. Pour les images fixes, commencez par MaskCut en local ou par la démo CutLER préentraînée. Sélectionnez la configuration et le point de contrôle correspondants dans le model zoo, puis enregistrez les sorties localement.
  — <https://github.com/facebookresearch/CutLER>
3. Pour l'inférence vidéo, téléchargez le point de contrôle officiel de VideoCutLER. Exécutez `videocutler/demo_video/demo.py` sur des images de vidéo séquentielles, avec la configuration Mask2Former fournie, un répertoire de sortie et les poids du modèle.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
4. Pour le réentraînement, préparez ImageNet-1K, puis générez ou téléchargez les pseudo-masques MaskCut. Placez le préentraînement de CutLER dans `videocutler/pretrain`, puis exécutez `train_net_video.py`.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>

## Bonnes pratiques {#best-practices}

- Maintenez PyTorch, torchvision et Detectron2 dans des versions mutuellement compatibles. L'exemple en amont utilise PyTorch 1.8.1 ; traitez un environnement récent comme une cible de validation distincte.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
- Utilisez le flux de travail local plutôt que la démo web MaskCut : l'espace Hugging Face officiel signale actuellement une erreur de build.
  — <https://huggingface.co/spaces/facebook/MaskCut>
- Pour VideoCutLER, commencez par le seuil de confiance documenté de 0,8. Abaissez-le uniquement lorsque le rappel élevé est prioritaire, et conservez des images ou des masques pour inspection.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
- Pour les grandes campagnes d'annotation MaskCut, répartissez les dossiers avec `--num-folder-per-job` et `--job-index`. Fusionnez les fichiers JSON en utilisant des paramètres `fixed_size`, `tau` et `N` identiques.
  — <https://github.com/facebookresearch/CutLER>
- Figez le commit exact du dépôt et le point de contrôle utilisés pour une exécution, car l'amont ne fournit aucune version étiquetée.
  — <https://github.com/facebookresearch/CutLER/tags>

## Remplacé par ce qui suit {#superseded-by-this}

- 2023-03-01 : la voie de la démo web MaskCut est obsolète pour un usage actuel. Son espace Hugging Face officiel signale désormais une erreur de build ; utilisez donc le code local.
- 2023-03-01 : les indications CutLER limitées aux images sont incomplètes pour les travaux vidéo multi-instances. Utilisez le flux d'inférence et d'entraînement dédié de VideoCutLER, tout en conservant CutLER pour les images fixes.
- 2024-03-11 : la documentation obsolète des points de contrôle VideoCutLER doit céder le pas à la révision du README en amont enregistrée le 2025-06-03–04. La disponibilité des points de contrôle n'a pas été vérifiée par un téléchargement indépendant.

## Points encore inconnus {#still-unknown}

- Nous n'avons ni installé ni exécuté le dépôt ; la compatibilité avec les versions actuelles de CUDA, PyTorch et Detectron2 reste non vérifiée.
- La page de projet Berkeley d'origine et le notebook Colab de 2023 n'ont pas pu être récupérés ni exécutés de façon indépendante lors de cette session ; ils ne permettent donc pas d'étayer une affirmation d'usage actuel.
- L'historique officiel identifie la mise à jour de VideoCutLER de mars 2024, mais pas sa modification de comportement exacte.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/facebookresearch/CutLER | Cut and Learn for Unsupervised Image & Video Object Detection and Instance Segmentation — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md | Instructions d'installation de CutLER — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md | VideoCutLER: Unsupervised Video Instance Segmentation — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/commits/main | Historique des commits de CutLER — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/tags | Versions et étiquettes de CutLER — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/facebook/MaskCut | MaskCut — Espace Hugging Face de facebook | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:cutler`, fil `cutler-development`, 2 événements datés du 2023-03-01 au 2024-03-11.
- **Note pratique :** À partir du 2023-03-01, les praticiens pouvaient utiliser le dépôt CutLER, l'espace MaskCut et les ressources Colab pour évaluer le projet ; à partir du 2024-03-11, ils doivent aussi consulter la documentation de VideoCutLER lorsque leur cas d'usage concerne la vidéo.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font référence pour ce qui est devenu obsolète.
