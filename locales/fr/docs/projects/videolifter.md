---
title: "VideoLifter"
category: projects
date: 2025-01-22
tags: [project, videolifter]
aliases: ["VideoLifter"]
level: 2
source_sha256: 93d4713af674cbf8a7d8c97c8afb1e9b1ab58a828e5aa9e21309febe36bc1d5a
translation: machine
translated_at: '2026-10-24'
---
# VideoLifter {#videolifter}

**Ligne de développement :** `project:videolifter` · fil `videolifter`  
**Dernier événement :** 2025-01-22 · 2 événements datés depuis 2025-01-09 · **Consulté :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

VideoLifter est un framework sans SfM destiné aux chercheurs en reconstruction 3D : il prend des images non calibrées issues d'une vidéo, utilise DUSt3R et MASt3R pour la géométrie initiale, puis optimise une 3D Gaussian representation et aligne les fragments dans une scène commune. Fonctionnalités : estimation des poses et de la structure, reconstruction de vidéos longues par fenêtres locales, novel-view synthesis. Mesure : les auteurs annoncent une réduction du temps d'entraînement de plus de 82 %. Verdict : à utiliser dans un environnement CUDA, avec Tanks and Temples ou CO3D préparés, en s'attendant à un pipeline de recherche avec entraînement et évaluation.

## Ligne de développement {#development-line}

- **2025-01-09 — Site du projet VideoLifter référencé.** L'alignement stéréo hiérarchique remplace les caméras précalculées et le SfM traditionnel dans le passage de la vidéo à la 3D.
- **2025-01-22 — Dépôt GitHub de VideoLifter référencé.** Le 2025-01-22, un enregistrement daté a relié le dépôt GitHub VITA-Group/VideoLifter et un lien connexe antérieur. Cela établit une référence publique au dépôt source dans l'historique du projet, mais n'établit ni la version, ni la release, ni le commit, ni l'état des fonctionnalités du dépôt à cette date.

## Ce qui a changé {#what-changed}

2025-01-09 — publication de la description de la méthode : l'alignement stéréo hiérarchique remplace les caméras précalculées et le SfM traditionnel dans le passage de la vidéo à la 3D. 2025-01-22 — apparition du dépôt officiel de reproduction, avec les dépendances, le checkpoint MASt3R préentraîné et des scripts distincts pour Tanks and Temples et CO3D.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-01-22, les praticiens qui recherchent du matériel d'implémentation de VideoLifter doivent commencer par le dépôt VITA-Group/VideoLifter référencé, en prenant le site du 2025-01-09 comme point d'entrée public du projet, et vérifier séparément la version, la licence et les modalités d'utilisation.

1. Clonez le dépôt avec ses submodules et téléchargez le checkpoint MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth dans submodules/mast3r/checkpoints.
  — <https://github.com/VITA-Group/VideoLifter>
2. Créez un environnement conda avec Python 3.10, PyTorch 2.1.0 et CUDA 11.8 ; installez ensuite les requirements et les deux paquets CUDA locaux.
  — <https://github.com/VITA-Group/VideoLifter>
3. Préparez les données : Tanks and Temples dans data/Tanks, ou le prétraitement CO3D des auteurs dans data/co3d.
  — <https://github.com/VITA-Group/VideoLifter>
4. Lancez scripts/train_tt.sh pour Tanks and Temples ou scripts/train_co3d.sh pour CO3D ; les résultats sont destinés à l'entraînement et à l'évaluation de la reconstruction 3D.
  — <https://github.com/VITA-Group/VideoLifter>

## Bonnes pratiques {#best-practices}

- Clonez avec --recursive : DUSt3R et MASt3R sont intégrés comme submodules, sans eux le pipeline ne se reproduit pas.
  — <https://github.com/VITA-Group/VideoLifter>
- Utilisez les versions de Python, PyTorch et CUDA fixées par les auteurs, et non un environnement moderne quelconque.
  — <https://github.com/VITA-Group/VideoLifter>
- Compilez les kernels CUDA pour RoPE issus de CroCo : les auteurs indiquent qu'il s'agit d'une accélération facultative, mais fortement recommandée.
  — <https://github.com/VITA-Group/VideoLifter>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points restant inconnus {#still-unknown}

- Aucune release, aucun paquet ni aucun modèle VideoLifter datés n'ont été trouvés après le dépôt source ; la documentation actuelle décrit une reproduction de recherche, mais ne confirme pas la prise en charge de vidéos utilisateur arbitraires comme produit finalisé.
- Pour l'événement du 2025-01-22, le README GitHub est disponible, mais sa page n'indique pas la date propre de la modification concernée ; les détails d'environnement doivent donc être lus comme l'état actuel du dépôt officiel, et non comme la preuve que chacun a été ajouté précisément le 22 janvier.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://videolifter.github.io/ | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://github.com/VITA-Group/VideoLifter | VITA-Group/VideoLifter — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2501.01949 | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://ece.utexas.edu/news/wenyan-cong-receives-best-paper-award-cvpr-workshop | Wenyan Cong Receives Best Paper Award at CVPR Workshop | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:videolifter`, fil `videolifter`, 2 événements datés du 2025-01-09 au 2025-01-22.
- **Note pratique :** À partir du 2025-01-22, les praticiens qui recherchent du matériel d'implémentation de VideoLifter doivent commencer par le dépôt VITA-Group/VideoLifter référencé, en prenant le site du 2025-01-09 comme point d'entrée public du projet, et vérifier séparément la version, la licence et les modalités d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
