---
title: "ACE++ : création et édition d'images pilotées par référence"
description: "ACE++ permet de créer et d'éditer des images pilotées par référence grâce à des workflows LoRA spécifiques à chaque tâche et à un modèle FFT généraliste ; utilisez l'association de modèle de base publiée et vérifiez ses conditions d'utilisation."
category: models
tags: [image-editing, alibaba, flux, reference-image, inpainting, lora, comfyui]
aliases: ["ACE Plus", "FuseAnyPart"]
level: 2
source_sha256: 17371554ba213dcd211e0d1d1c5ae9a42dec44badad0fd439e56000e468607e5
translation: machine
translated_at: '2026-10-24'
---
# ACE++ : création et édition d'images pilotées par référence {#ace-reference-driven-image-creation-and-editing}

**Périmètre vérifié : 2026-09-04.** ACE++ est le système de post-entraînement d'Alibaba Tongyi Lab pour la génération et l'édition d'images à partir de références. Il combine des images de référence, des images à éditer ou des masques si nécessaire, et une instruction textuelle. Le dépôt officiel fournit plusieurs routes LoRA spécialisées par tâche ainsi qu'un modèle plus général à réglage fin complet (FFT), et non un point de contrôle unique interchangeable pour tous les workflows.

## Choisir la route de modèle publiée {#select-the-published-model-route}

| Route | Périmètre visé | Remarque opérationnelle |
|---|---|---|
| LoRA portrait | génération ou édition à partir d'une référence d'identité ou de portrait | utiliser le workflow de référence associé |
| LoRA sujet | cohérence d'objet, de logo, de motif et de sujet | utiliser le workflow de référence associé |
| LoRA d'édition locale | modifications locales guidées par masque ou par contrôle | peut nécessiter la chaîne de prétraitement documentée |
| Modèle FFT | tâches plus générales de référence et d'édition | les auteurs signalent des résultats moins stables que les routes LoRA spécialisées |

Le dépôt recommande les workflows LoRA lorsqu'une route spécialisée existe. Un modèle général peut être pratique, mais il ne doit pas être considéré comme la référence de qualité pour une tâche qui dispose d'un adaptateur dédié.

## Modèle de base et périmètre du workflow {#base-model-and-workflow-boundary}

Les exemples LoRA publiés associent ACE++ à `FLUX.1-Fill-dev` ; certains workflows utilisent aussi FLUX.1 Redux ou des composants de prétraitement documentés. La route FFT possède sa propre configuration. Conservez les éléments suivants comme une unité versionnée :

- les poids ACE++ et le workflow sélectionné ;
- la révision du modèle de base et tout modèle associé ;
- le modèle de prétraitement et la convention de masque ou de contrôle ;
- les dimensions de l'image, le réglage de longueur de séquence, les paramètres d'échantillonnage et le prompt ;
- l'artefact de sortie et l'autorisation d'utilisation des références sources.

Ne chargez pas un adaptateur ACE++ dans un point de contrôle FLUX arbitraire au seul motif que les noms de fichiers semblent compatibles. L'option `max_seq_length` du dépôt est un réglage de compromis entre mémoire et détail pour le workflow fourni, et non un paramètre de qualité universel.

## Contrôles pratiques de validation {#practical-acceptance-checks}

Testez la classe d'édition exacte avant de vous y fier :

1. vérifiez que le sujet ou l'objet de référence est conservé là où cela est requis ;
2. inspectez la frontière d'édition, les fuites de masque, les mains, la typographie et les petits logos à la taille de livraison ;
3. vérifiez que les zones non concernées restent inchangées lorsque la préservation est exigée ;
4. conservez l'image d'entrée, le masque, le prompt, la graine, les révisions des modèles et la sortie pour une revue reproductible ;
5. revenez à une voie manuelle contrôlée ou à une composition lorsque le résultat modifie le mauvais objet.

Le projet amont liste des limitations dans le suivi d'instructions pour certaines opérations d'ajout ou de suppression, et signale d'éventuels artefacts. Un résultat visuellement plausible n'est pas une preuve que l'édition locale demandée a été correctement réalisée.

## Licences et distribution {#licensing-and-distribution}

ACE++ repose sur des artefacts de modèles de base externes. Examinez la licence et les conditions d'accès actuelles du modèle de base sélectionné, des poids ACE++ et de chaque point de contrôle associé avant tout usage commercial, toute redistribution ou toute mise à disposition dans un service hébergé. Ne présentez jamais un workflow comme commercialement autorisé au seul motif que son code est visible sur GitHub.

## Références {#references}

- [Dépôt officiel d'ACE++](https://github.com/ali-vilab/ACE_plus)
- [Article ACE++](https://arxiv.org/abs/2501.02487)
- [Collection ACE++ sur Hugging Face](https://huggingface.co/ali-vilab/ACE_Plus)
