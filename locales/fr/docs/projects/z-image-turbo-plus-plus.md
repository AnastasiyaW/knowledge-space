---
title: "Z-Image Turbo++ — Référence de recherche"
category: projects
date: 2026-06-17
tags: [project, research-reference, z-image-turbo-plus-plus, z_image]
aliases: ["Z-Image Turbo++"]
level: 2
source_sha256: a52e80d26ecd8e6ade666154458d7f6b4c87968280490eb18aa5a25b4c6c355d
translation: machine
translated_at: '2026-10-24'
---
# Z-Image Turbo++ — Référence de recherche {#z-image-turbo-research-reference}

**Ligne de développement :** `project:z-image-turbo-plus-plus` · fil `research-reference`  
**Dernier événement :** 2026-06-17 · 1 événement daté depuis le 2026-06-17 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Z-Image Turbo++ est un modèle de recherche text-to-image destiné aux équipes qui évaluent une génération en deux étapes au lieu de la génération en huit étapes de Z-Image Turbo. — Distribution-Aligned Adversarial Learning : utilise les images du modèle enseignant comme cible GAN. — Step-Decoupled Parameterization : sépare les paramètres des deux étapes de débruitage. — End-to-End Training with Iterative Regularization : transmet l'évaluation finale de la qualité à la première étape. 2 étapes au lieu de 8 pour le modèle enseignant ; un checkpoint distinct et prêt à l'emploi n'est pas confirmé dans les sources primaires consultées. Verdict : c'est une référence pour reproduire la recherche, alors que pour un déploiement opérationnel, seul Z-Image-Turbo est confirmé à ce jour.

## Ligne de développement {#development-line}

- **2026-06-17 — Référence à l'article Z-Image Turbo++ ajoutée.** Le 2026-06-17, une page Hugging Face Papers, identifiée comme l'article 2606.12575, a été ajoutée à la ligne de développement de Z-Image Turbo++. Ce lien daté établit une référence de recherche pour le projet, mais n'établit ni le titre de l'article, ni ses affirmations techniques, ni son statut de publication. Cet événement historique enregistre la référence elle-même et non des capacités non vérifiées.

## Changements {#what-changed}

2026-06-17 — Z-Image Turbo++ est décrit comme une distillation en deux étapes à partir de Z-Image Turbo, qui en comporte huit ; la différence porte sur le nombre d'étapes, et non sur une publication distincte et confirmée des poids.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-17, les praticiens doivent traiter la fiche Hugging Face Papers liée comme une référence de recherche à examiner, et non comme une preuve d'affirmations techniques non vérifiées ou d'une sortie de produit.

1. Pour une reproduction de recherche, implémenter deux étapes de débruitage indépendantes, en les entraînant sur les images du modèle enseignant à huit étapes et en conservant la perte auxiliaire de la première étape.
  — <https://arxiv.org/abs/2606.12575>
2. Pour la génération en pratique, ne pas étiqueter l'exécution comme Turbo++ : utiliser le modèle Tongyi-MAI/Z-Image-Turbo publié séparément, à huit étapes.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
3. Pour Z-Image-Turbo, charger ZImagePipeline en bfloat16 sur CUDA, définir num_inference_steps=9, ce qui donne 8 passes DiT, et guidance_scale=0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Bonnes pratiques {#best-practices}

- Séparer les résultats de Turbo++ et de Z-Image-Turbo dans les expériences : l'article définit Turbo++ comme 2-step, tandis que la fiche officielle de Turbo l'indique comme 8-step.
  — <https://arxiv.org/abs/2606.12575>
- Pour le modèle Turbo publié, ne pas augmenter guidance_scale : la fiche du modèle fixe la valeur à 0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- Utiliser bfloat16 sur un GPU pris en charge ; n'activer le déchargement CPU (CPU offload) qu'en cas de manque de mémoire, en acceptant une exécution plus lente.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Remplacé par ce document {#superseded-by-this}

- 2026-06-10 — la contrainte de recherche de la lignée Z-Image, limitée à la plage de 4 à 8 étapes, est remplacée : ce travail démontre une distillation en deux étapes.

## Points encore inconnus {#still-unknown}

- Les poids officiels distincts, le code, la fiche de modèle ou un runtime compatible pour Turbo++ ne sont pas confirmés parmi les sources primaires consultées ; leur absence sur les pages vérifiées ne prouve pas qu'ils n'existent pas.
- L'abstract de Turbo++ ne contient ni tableau numérique de qualité ni mesure de vitesse ; pour décider d'un déploiement, il faut un benchmark reproductible avec les mêmes prompts et le même matériel.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://huggingface.co/papers/2606.12575 | Paper page - High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2606.12575 | High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2511.22699 | Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion Transformer | 2026-09-05 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Tongyi-MAI/Z-Image-Turbo | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:z-image-turbo-plus-plus`, fil `research-reference`, 1 événement daté du 2026-06-17 au 2026-06-17.
- **Remarque pratique :** À partir du 2026-06-17, les praticiens doivent traiter la fiche Hugging Face Papers liée comme une référence de recherche à examiner, et non comme une preuve d'affirmations techniques non vérifiées ou d'une sortie de produit.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
