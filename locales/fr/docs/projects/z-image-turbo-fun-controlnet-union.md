---
title: "Z-Image-Turbo-Fun-Controlnet-Union"
category: projects
date: 2025-12-12
tags: [project, z-image-turbo-fun-controlnet-union, z-image-turbo-fun-controlnet-union-development, z_image]
aliases: ["Z-Image-Turbo-Fun-Controlnet-Union", "Z-Image-Turbo-Fun-Controlnet-Union-2.0"]
level: 2
source_sha256: 1087c343347ac56a0adacd640b707f9f92139bd0a459d59ac4acd6299fac351b
translation: machine
translated_at: '2026-10-24'
---
# Z-Image-Turbo-Fun-Controlnet-Union {#z-image-turbo-fun-controlnet-union}

**Ligne de développement :** `project:z-image-turbo-fun-controlnet-union` · fil `z-image-turbo-fun-controlnet-union-development`  
**Dernier événement :** 2025-12-12 · 2 événements datés depuis 2025-12-02 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Z-Image-Turbo-Fun-Controlnet-Union est une famille de poids ControlNet pour Z-Image-Turbo dans VideoX-Fun. Fonctionnalités : guider la génération par contours, profondeur, pose, lignes, Scribble et Gray ; utiliser l'inpaint ; appliquer un point de contrôle Tile distinct pour la super-résolution. La version Union 2.1-2602-8steps actuelle prend en charge sept types de contrôle et est conçue pour 8 étapes. Verdict : il s'agit d'un workflow local, et non d'un fournisseur d'inférence hébergé ; la branche 2.1 actuelle a remplacé les versions 1.0 et 2.0 pour un usage pratique.

## Ligne de développement {#development-line}

- **2025-12-02 — Jalon initial du dépôt Z-Image-Turbo-Fun-Controlnet-Union.** ControlNet sur six blocs avec Canny, HED, Depth, Pose et MLSD.
- **2025-12-12 — Jalon du dépôt Z-Image-Turbo-Fun-Controlnet-Union 2.0.** Davantage de blocs contrôlables, un entraînement plus long et un mode inpaint.

## Modifications {#what-changed}

2025-12-02 — publication de la version initiale Z-Image-Turbo-Fun-Controlnet-Union : ControlNet sur six blocs avec Canny, HED, Depth, Pose et MLSD. 2025-12-12 — publication de Z-Image-Turbo-Fun-Controlnet-Union-2.0 : davantage de blocs contrôlables, un entraînement plus long et un mode inpaint. 2025-12-17 — la version 2.1 a corrigé un défaut de la 2.0 qui faisait exécuter deux passes forward aux blocs et ralentissait l'inférence. 2025-12-22 — sortie de la distillation 8 étapes de la 2.1 et du modèle Tile pour la super-résolution. 2026-01-12 — la version 2601 a ajouté Scribble, des variantes lite et un réentraînement contre la fuite de masque et les artefacts. 2026-02-26 — la version 2602 a ajouté Gray Control.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-12-02, les praticiens doivent utiliser le dépôt Z-Image-Turbo-Fun-Controlnet-Union lié comme point de départ daté de cette ligne ; à partir du 2025-12-12, ils doivent évaluer séparément le dépôt 2.0 lié, sans supposer qu'il est identique au dépôt initial.

1. Cloner VideoX-Fun et créer les répertoires de modèles `models/Diffusion_Transformer` et `models/Personalized_Model`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
2. Télécharger les poids de base Z-Image-Turbo et la version actuelle `Z-Image-Turbo-Fun-Controlnet-Union-2.1-2602-8steps.safetensors` ; placer le ControlNet dans `models/Personalized_Model`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
3. Fournir l'image de contrôle préparée du type voulu et lancer le workflow 2.1 depuis VideoX-Fun ; pour l'inpaint, utiliser l'exemple correspondant `predict_i2i_inpaint_2.1.py`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
4. Pour Union 2602, utiliser 8 étapes de diffusion et choisir un contrôle parmi Canny, Depth, Pose, MLSD, HED, Scribble ou Gray.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Bonnes pratiques {#best-practices}

- Pour une nouvelle installation, choisir 2.1-2602-8steps : elle inclut les corrections de la 2.0, la distillation 8 étapes et Gray Control.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Conserver un prompt textuel détaillé ; pour les versions 2.1 et 2.0, régler `control_context_scale` dans la plage 0.65–1.00, et l'augmenter en cas d'inpaint pour assurer la continuité de l'image.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Pour un matériel modeste ou un résultat plus naturel avec un control scale élevé, utiliser les variantes lite 2601/2602 ; cela affaiblit le contrôle, car celui-ci s'applique à un plus petit nombre de couches.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Remplacé par {#superseded-by-this}

- 2025-12-17 — Z-Image-Turbo-Fun-Controlnet-Union-2.0 est obsolète pour les nouvelles exécutions : la 2.1 corrige son défaut de double passe forward et rétablit la vitesse d'inférence en une étape.
- 2025-12-22 — la version 2.1 non distillée cède la place à 2.1-8steps pour la génération courante : la fiche du modèle recommande 8 étapes.
- 2026-02-26 — 2.1-2601-8steps ne couvre pas Gray Control ; il faut 2.1-2602-8steps pour cela.

## Points non élucidés {#still-unknown}

- L'URL `Z-Image-Turbo-Fun-Controlnet-Union-2.0` redirige actuellement vers la 2.1 ; une fiche modèle 2.0 distincte et immuable n'est pas accessible à cette adresse. Les caractéristiques historiques de la 2.0 sont confirmées par la section conservée « Models Before 2601 » de la fiche primaire actuelle.
- Il est impossible de déterminer à partir des pages primaires accessibles quel texte accompagnait exactement les messages source ; les conclusions sont rattachées aux dates de publication et de mise à jour des poids dans le dépôt primaire.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union | alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union — fiche modèle Hugging Face | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union/commits/main | Historique des commits — Z-Image-Turbo-Fun-Controlnet-Union | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0 | URL Z-Image-Turbo-Fun-Controlnet-Union-2.0, redirigée vers la fiche modèle 2.1 maintenue | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1/commits/main | Historique des commits — Z-Image-Turbo-Fun-Controlnet-Union-2.1 | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:z-image-turbo-fun-controlnet-union`, fil `z-image-turbo-fun-controlnet-union-development`, 2 événements datés du 2025-12-02 au 2025-12-12.
- **Note pratique :** à partir du 2025-12-02, les praticiens doivent utiliser le dépôt Z-Image-Turbo-Fun-Controlnet-Union lié comme point de départ daté de cette ligne ; à partir du 2025-12-12, ils doivent évaluer séparément le dépôt 2.0 lié, sans supposer qu'il est identique au dépôt initial.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
