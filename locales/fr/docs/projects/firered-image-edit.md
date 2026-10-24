---
title: "FireRed Image Edit — Ressources ComfyUI"
category: projects
date: 2026-03-17
tags: [comfyui-resources, firered, firered-image-edit, project]
aliases: ["FireRed Image Edit"]
level: 3
source_sha256: 5f484c2ba722a5868b668a84372372a36fa4c3e43f6257297d1b59320f84c091
translation: machine
translated_at: '2026-10-24'
---
# FireRed Image Edit — Ressources ComfyUI {#firered-image-edit-comfyui-resources}

**Ligne de développement :** `project:firered-image-edit` · fil `comfyui-resources`  
**Dernier événement :** 2026-03-17 · 1 événement daté depuis le 2026-03-17 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

FireRed Image Edit est un éditeur d'images local piloté par instructions, pour ComfyUI et Diffusers.

- Modification d'une image source à partir de texte.
- Fusion de références avec 1 à 3 images pour les portraits, le style de texte, le maquillage, la restauration et l'essayage virtuel.

Le transformeur BF16 seul nécessite 40,9 Go. La voie optimisée séparée annonce 30 Go et un temps d'exécution d'environ 4,5 secondes.

## Ligne de développement {#development-line}

- **2026-03-17 — Une ressource ComfyUI pour FireRed Image Edit 1.1 a été liée.** Un message du fil FireRed a lié un dépôt Hugging Face de FireRed Image Edit 1.1 pour ComfyUI le 2026-03-17. Le même message incluait 3 URL RunningHub. Nous ne disposons d'aucune preuve concernant le contenu lié, une version, des changements de capacités ou les détails des workflows. Nous consignons uniquement la publication datée de ces liens de ressources.

## Ce qui a changé {#what-changed}

- 2026-02-12 — Le rapport technique v1 a établi le modèle d'édition par instructions.
- 2026-02-14 — Les poids FireRed-Image-Edit-1.0 sont devenus disponibles.
- 2026-02-27 — L'équipe a ajouté une voie Agent et un workflow ComfyUI pour la 1.0.
- 2026-03-01 — Une voie d'inférence locale optimisée a été documentée.
- 2026-03-03 — FireRed-Image-Edit-1.1 a été publié comme successeur de la 1.0, avec une meilleure cohérence des portraits, la fusion multi-éléments, le texte stylisé et le maquillage.
- 2026-03-04 — Le paquet officiel ComfyUI 1.1 est apparu.
- 2026-03-08 — 3 graphes de comparaison indépendants (image unique, double image et multi-images) sont apparus sans modifier le paquet officiel.
- 2026-03-09 — REDEdit-Bench a été publié.
- 2026-03-13 — Un accélérateur 1.0-Lightning v1.1 à 8 étapes a été ajouté au paquet ComfyUI 1.1.
- 2026-03-17 — Le JSON officiel a remplacé son accélérateur optionnel 1.0-Lightning 8steps v1.0 par la v1.1 ; il ne s'agissait pas de la version de base 1.1.
- 2026-03-24 — Le code d'entraînement LoRA a été intégré.
- 2026-03-25 — La prise en charge de l'entraînement LoRA sur ModelScope a été annoncée.
- 2026-03-26 — La collection officielle a marqué LoRA Zoo comme mis à jour.
- 2026-04-03 — La prise en charge du recaptionnement multi-fournisseurs a été fusionnée dans le code canonique.
- 2026-04-10 — Un fichier 1.1-Lightning 8 étapes v1.1 a été ajouté.
- 2026-04-14 — Un fichier 1.1-Lightning 8 étapes v1.2 a été ajouté.

## Comment l'utiliser {#how-to-use-this}

1. Choisissez une voie prise en charge : chargez FireRedTeam/FireRed-Image-Edit-1.1 avec Diffusers, ou partez du paquet officiel ComfyUI 1.1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1>
2. Pour le graphe ComfyUI standard, placez le transformeur 1.1 dans models/diffusion_models, qwen2.5vl-7b-bf16 dans models/text_encoders, qwen_image_vae dans models/vae, puis importez le JSON officiel.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
3. Placez l'image source dans le chargeur principal, ajoutez jusqu'à 2 références optionnelles, et indiquez dans le prompt la modification visée et les numéros des images.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
4. Lancez d'abord un profil standard non modifié : 40 étapes et CFG 4 sans le LoRA d'accélération, ou 8 étapes et CFG 1 avec la voie Lightning incluse.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
5. Pour plus de 3 entrées, utilisez le préprocesseur Agent séparé et vérifiez sa dépendance au traitement ROI de Gemini avant d'envoyer les images.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>

## Bonnes pratiques {#best-practices}

- Épinglez ensemble le JSON du workflow, le transformeur et le LoRA Lightning : le graphe du 17 mars associait volontairement un transformeur 1.1 à l'adaptateur 1.0-Lightning v1.1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019>
- Ne considérez pas le fichier ultérieur 1.1-Lightning v1.2 comme un remplacement documenté et direct du graphe du 17 mars ; testez-le comme une exécution séparée et versionnée.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main>
- Commencez par l'échantillonneur et les réglages fournis plutôt que de recâbler le graphe ; les profils enregistrés sont 40 étapes/CFG 4 ou 8 étapes/CFG 1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
- Ne traduisez pas l'affirmation du projet sur 30 Go et un script optimisé d'environ 4,5 secondes en garantie de capacité ou de vitesse pour ComfyUI.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- Pour les travaux de plus de 3 images, traitez le prétraitement Agent comme une frontière de service externe : la détection ROI utilise toujours Gemini, même si le recaptionnement passe par un autre fournisseur.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- Traitez les graphes de comparaison assemblés indépendamment comme des workflows personnalisés tant que leur checkpoint, leurs réglages et la provenance de leurs nœuds n'ont pas été inspectés.
  — <https://www.runninghub.ai/post/2030612111793065986>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-03 — considérer l'événement du 2026-03-17 comme la sortie de FireRed-Image-Edit-1.1 est obsolète ; la 1.1 avait été annoncée le 2026-03-03.
- 2026-03-08 — considérer le graphe de comparaison multi-images lié comme le paquet ComfyUI officiel FireRedTeam 1.1 est obsolète.
- 2026-04-14 — qualifier FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 de dernier artefact Lightning officiel de la 1.1 est obsolète.

## Toujours inconnu {#still-unknown}

- Aucune source officielle lue n'annonce une version de modèle de base postérieure à la 1.1 ; cela ne prouve pas qu'il n'existe aucune version régionale non indexée.
- Le paquet officiel ne donne ni version minimale explicite de ComfyUI, ni matrice de GPU testés, ni benchmark de performance propre à ComfyUI.
- Le workflow du 17 mars ne documente pas la compatibilité entre son association 1.0-Lightning v1.1 et le fichier ultérieur 1.1-Lightning v1.2.
- Les poids GGUF sont publiés, mais le JSON standard sélectionne les safetensors et ne prouve pas l'existence d'un graphe de chargement GGUF.
- La compatibilité ControlNet et OpenPose n'a pas été confirmée par une source primaire de FireRed.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2602.13344 | Rapport technique de FireRed-Image-Edit-1.0 | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit | README de FireRedTeam/FireRed-Image-Edit | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit/commits/main/ | Commits · FireRedTeam/FireRed-Image-Edit | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1 | FireRedTeam/FireRed-Image-Edit-1.1 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commits/main | Historique des commits · FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019 | Envoi de firered-image-edit-1.1.json · commit 179def9 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true | firered-image-edit-1.1.json | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main | Arborescence des fichiers de FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/collections/FireRedTeam/firered-image-edit | FireRed-Image-Edit · Collection FireRedTeam | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/02dd2dc5586fcf7a60451506e7dee8dd31021455 | Envoi de FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 · commit 02dd2dc | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/8625b60ec52d4fa0d128d8a6ebc8adba296f8592 | Envoi de FireRed-Image-Edit-1.1-Lightning-8steps-v1.2 · commit 8625b60 | 2026-09-06 |
| https://www.runninghub.ai/post/2030611704802971649 | Xiaohongshu FireRed Image edit 1.1 : édition d'image unique vs Qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612012606169089 | Xiaohongshu FireRed Image edit 1.1 : édition double image vs Qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612111793065986 | Xiaohongshu FireRed Image edit 1.1 : édition multi-images vs Qwen | 2026-09-06 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:firered-image-edit`, fil `comfyui-resources`, 1 événement daté du 2026-03-17 au 2026-03-17.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
