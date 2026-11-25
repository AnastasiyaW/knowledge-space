---
title: "Correction d'anatomie dans les modèles de diffusion"
description: "La correction d'anatomie est un flux de travail diagnostiquer-masquer-conditionner-inpainter ; utilisez des méthodes de recherche tenant compte de la géométrie et des outils d'édition adaptés au modèle, puis vérifiez visuellement chaque main ou membre modifié par rapport à la source."
category: workflows
tags: [anatomy, hands, inpainting, diffusion, image-editing, quality-control, comfyui]
aliases: ["Hand correction", "Diffusion anatomy repair"]
level: 2
source_sha256: d272fa5fbb6e97668e07de397dc146ae328265204bb6b7367d0f9de9cc5a2159
translation: machine
translated_at: '2026-10-24'
---
# Correction d'anatomie dans les modèles de diffusion {#anatomy-correction-in-diffusion-models}

**Périmètre vérifié : 2026-09-04.** La correction d'anatomie est un flux de travail d'édition d'image locale destiné aux mains, doigts, visages ou membres mal formés. Ce n'est pas un préréglage universel de sampler, et aucun détecteur, LoRA ou modèle d'inpainting ne peut à lui seul certifier qu'une anatomie générée est correcte.

## La boucle de correction {#the-correction-loop}

1. **Inspecter la source à la taille de livraison.** Identifiez précisément ce qui ne va pas : nombre, topologie des articulations, occlusion, pose, silhouette ou artefact de rendu.
2. **Choisir la zone d'édition la plus petite et sûre.** Incluez l'anatomie endommagée et une zone de transition étroite ; préservez les pixels non concernés et conservez le fichier original.
3. **Fournir une structure lorsque c'est possible.** Un maillage de main, une pose, une estimation de profondeur ou une référence soigneusement vérifiée peuvent contraindre la correction plus fiablement qu'un prompt positif générique.
4. **Utiliser un flux d'édition ou d'inpainting adapté au modèle.** Le checkpoint, l'encodeur de texte, le VAE, le format de conditionnement et la version des nœuds doivent être compatibles en tant qu'ensemble.
5. **Relire le résultat manuellement.** Vérifiez le nombre de doigts, les articulations, le contact avec les objets, la perspective, la continuité de la peau et des matériaux, les ombres et le bord de la zone éditée.
6. **Régénérer plutôt que corriger par retouches successives** lorsque l'erreur est globale, que la pose visée est ambiguë, ou que l'édition locale modifie l'identité ou la géométrie en dehors de la zone cible.

## Pistes de recherche tenant compte de la structure {#structure-aware-research-directions}

HandRefiner et HandCraft sont des références utiles pour le principe sous-jacent à une réparation locale robuste : dériver une structure de main, la transformer en conditionnement tel que la profondeur ou des masques, puis utiliser un inpainting par diffusion pour intégrer la région corrigée. Les résultats qu'ils rapportent s'appliquent à leurs configurations de recherche déclarées ; ils n'établissent pas l'existence d'un nœud directement compatible avec chaque modèle de diffusion actuel.

La conséquence pratique est simple : un signal géométrique peut rendre une édition plus contrainte, mais son alignement avec l'image originale doit être vérifié avant de l'utiliser comme conditionnement.

## ComfyUI actuel et limites des modèles {#current-comfyui-and-model-boundary}

ComfyUI documente actuellement des flux de travail FLUX.2 [klein] distincts pour les variantes base et distillée des modèles qu'il prend en charge. Suivez la documentation officielle et les emplacements de modèles pour la variante 4B ou 9B exacte sélectionnée. Ne supposez pas qu'un nœud, un modèle de contrôle, une LoRA, un encodeur de texte ou un VAE conçu pour FLUX.1, SDXL ou une autre version sera compatible avec un flux FLUX.2 [klein].

Les nœuds communautaires et les LoRA d'anatomie tierces peuvent être utiles comme expérimentations, mais chacun nécessite une révision source figée, sa propre revue de licence et un test visuel propre au projet. Cette page ne prescrit délibérément ni poids communautaires non vérifiés, ni réglages numériques universels.

## Grille de contrôle qualité {#quality-gate}

| Contrôle | Ce qui doit être observé |
|---|---|
| Anatomie | nombre, articulations, proportions et pose plausibles |
| Interaction | les doigts, outils, vêtements et autres objets entrent correctement en contact physique |
| Préservation | identité, typographie, logos, bijoux et géométrie hors cible restent inchangés |
| Composition | éclairage, direction des ombres, texture et transition de bord correspondent à la source |
| Reproductibilité | empreinte de la source, masque/conditionnement, révision du modèle, réglages, empreinte de la sortie et décision du relecteur |

Un score de détecteur peut aider à trier un lot, mais ce n'est pas une condition de validation. Tout actif impliquant l'identité d'une personne, des informations produit, une pertinence médicale ou une valeur probante nécessite une relecture humaine avant publication.

## Conditions et données {#terms-and-data}

Le code, les modèles, les adaptateurs, les estimateurs de maillage ou de pose, les images d'entrée et les sorties générées peuvent être régis par des licences et des obligations de consentement différentes. Vérifiez les artefacts exacts et les droits d'édition de l'image avant toute réutilisation ou tout déploiement commercial.

## Références {#references}

- [Article HandRefiner](https://arxiv.org/abs/2311.17957)
- [Article HandCraft](https://arxiv.org/abs/2411.04332)
- [Dépôt HandFixer](https://github.com/Xiangyu-CAS/HandFixer)
- [Documentation ComfyUI FLUX.2 [klein]](https://docs.comfy.org/tutorials/flux/flux-2-klein)
