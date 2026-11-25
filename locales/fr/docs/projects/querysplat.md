---
title: "QuerySplat"
category: projects
date: 2026-08-04
tags: [project, querysplat, querysplat-development]
aliases: ["QuerySplat"]
level: 2
source_sha256: 598e952ebb319537d3e7984a5c17062f64ed7a4e6284946d19de325b8cfbf901
translation: machine
translated_at: '2026-10-24'
---
# QuerySplat {#querysplat}

**Ligne de développement :** `project:querysplat` · fil `querysplat-development`  
**Dernier événement :** 2026-08-04 · 1 événement daté depuis le 2026-08-04 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

QuerySplat est un framework feed-forward de Gaussian Splatting 3D destiné à celles et ceux qui ont besoin d'une scène rendable et de vues inédites à partir d'images multi-vues, sans poses de caméra fournies au préalable.

- Un décodeur de requêtes à double branche sépare la géométrie de l'apparence.
- VGGT-Omega fournit la prédiction de la caméra et de la profondeur ; l'optimisation au moment du test est facultative.

## Ligne de développement {#development-line}

- **2026-08-04 — Le 2026-08-04, QuerySplat a été relié à son site de projet, à son dépôt GitHub et à sa page Hugging Face..** Le 2026-08-04, l'enregistrement daté a relié QuerySplat à un site web public de projet, à un dépôt GitHub et à une page Hugging Face. Il s'agit d'une étape publique importante du développement, car elle établit des ressources de projet liées entre elles, mais les éléments disponibles ne permettent pas d'affirmer quoi que ce soit sur une version publiée, sur des fonctionnalités ou sur des résultats.

## Ce qui a changé {#what-changed}

2026-08-02 — InSpatio a qualifié QuerySplat de open source. 2026-08-04 — Aucune version distincte et numérotée de QuerySplat n'est attestée ; son article public et son statut open source renvoient tous deux à la publication du 2 août.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-04, les praticiens doivent consulter le site de projet, le dépôt de sources et la page Hugging Face liés à QuerySplat, qui constituent son ensemble de ressources publiques, et vérifier directement dans ces ressources les capacités et le statut de publication avant de l'adopter.

1. Préparez la pile testée : Linux, un GPU NVIDIA compatible CUDA, Python 3.12, PyTorch 2.11.0 et CUDA 12.8 ; clonez ensuite le dépôt officiel d'inférence et installez ses dépendances.
  — <https://github.com/inspatio/querysplat>
2. Téléchargez le point de contrôle QuerySplat et la configuration fournie dans le dossier `checkpoints`, téléchargez-y `vggt_omega_1b_512.pt`, puis exécutez `sha256sum -c SHA256SUMS` avant l'inférence.
  — <https://github.com/inspatio/querysplat>
3. Connectez-vous et acceptez les conditions d'accès à VGGT-Omega avant de télécharger son point de contrôle ; son accès fait l'objet d'une restriction distincte.
  — <https://huggingface.co/facebook/VGGT-Omega>
4. Placez les images d'une même scène dans le dossier d'entrée et exécutez `python -m scripts.infer` avec la configuration fournie, le point de contrôle QuerySplat, le dossier d'entrée et le répertoire de sortie.
  — <https://github.com/inspatio/querysplat>
5. Ajoutez `--use_tto` pour l'optimisation au moment du test ; omettez-le pour une inférence purement feed-forward.
  — <https://github.com/inspatio/querysplat>

## Bonnes pratiques {#best-practices}

- Ne placez que les images d'une seule scène dans chaque dossier d'entrée. Le nombre d'images accepté correspond à l'interface d'entrée en amont, et non à une garantie de passage à l'échelle publiée.
  — <https://github.com/inspatio/querysplat>
- Utilisez la combinaison PyTorch/CUDA testée et faites correspondre les extensions gsplat et fused-ssim à celle-ci ; LPIPS peut télécharger les poids VGG16 lors de la première utilisation.
  — <https://github.com/inspatio/querysplat>
- Vérifiez les deux points de contrôle téléchargés avec le manifeste SHA-256 du projet avant de lancer une exécution.
  — <https://github.com/inspatio/querysplat>
- Considérez à titre de précaution la zone de 30 vues et plus comme une capacité non vérifiée : un utilisateur a signalé, le 6 août, un échec par manque de mémoire, sans indication de matériel, de résolution, de détails de reproduction ni de réponse des mainteneurs. Commencez avec un nombre plus réduit de vues et mesurez la VRAM ; il s'agit d'un constat anecdotique, et non d'une limite officielle.
  — <https://github.com/inspatio/querysplat/issues/2>
- Examinez les licences composant par composant : le code écrit par les auteurs de QuerySplat est sous Apache-2.0, tandis que le code source VGGT-Omega/DINOv3 inclus est soumis à la FAIR Noncommercial Research License.
  — <https://github.com/inspatio/querysplat>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues à ce jour {#still-unknown}

- Aucune version distincte et numérotée de QuerySplat datée du 2026-08-04 n'a été trouvée ; l'article public et le statut open source sont datés indépendamment du 2026-08-02.
- Le dépôt officiel consulté ne décrit que l'inférence. Aucune publication officielle du code d'entraînement n'a pu être vérifiée lors de ce passage de recherche ; une question du 7 août à ce sujet reste sans réponse des mainteneurs.
- Aucune reproduction indépendante du résultat sur DL3DV n'a été trouvée lors de ce passage de recherche ; les gains rapportés de 2,30 dB sans pose et de 1,04 dB avec pose requise sont des résultats annoncés par les auteurs dans l'article.
- La dépendance VGGT-Omega requise a publié, le 18 août, un avertissement sur une éventuelle contamination des benchmarks dans un point de contrôle ancêtre. Il indique que les usages en aval peuvent se poursuivre, mais cela n'établit pas d'erreur directe dans le résultat DL3DV de QuerySplat.
- Une description en chinois simplifié émanant du projet a été trouvée, mais aucun retour d'exploitation indépendant en chinois simplifié n'a été utilisé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://inspatio.github.io/querysplat/ | Page de projet QuerySplat | 2026-09-05 |
| https://github.com/inspatio/querysplat | Dépôt officiel d'inférence QuerySplat | 2026-09-05 |
| https://huggingface.co/inspatio/querysplat | Fiche de modèle et point de contrôle QuerySplat | 2026-09-05 |
| https://arxiv.org/abs/2608.01186 | QuerySplat: Decoupling Geometry and Appearance Representations in 3DGS Prediction | 2026-09-05 |
| https://www.inspatio.com/models/querysplat | Page du modèle QuerySplat d'InSpatio | 2026-09-05 |
| https://huggingface.co/facebook/VGGT-Omega | Fiche de modèle VGGT-Omega et conditions d'accès | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/2 | large scene reconstruction, QuerySplat issue 2 | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/3 | Will the training code be open-sourced?, QuerySplat issue 3 | 2026-09-05 |
| https://www.inspatio.com/zh/models | Modèles ouverts d'InSpatio, chinois simplifié | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:querysplat`, fil `querysplat-development`, 1 événement daté du 2026-08-04 au 2026-08-04.
- **Note pratique :** Au 2026-08-04, les praticiens doivent consulter le site de projet, le dépôt de sources et la page Hugging Face liés à QuerySplat, qui constituent son ensemble de ressources publiques, et vérifier directement dans ces ressources les capacités et le statut de publication avant de l'adopter.
- **Confiance :** moyenne. Les remplacements datés font foi pour ce qui est obsolète.
