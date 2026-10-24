---
title: "Flow Matching : entraînement de champ vectoriel conditionnel"
description: "Le flow matching entraîne un champ vectoriel continu le long d'un chemin de probabilité choisi ; les réglages du scheduler, du chemin et de l'inférence sont propres à chaque checkpoint et ne constituent pas des valeurs par défaut universelles de la diffusion."
category: architectures
tags: [flow-matching, conditional-flow-matching, scheduler, sampling, continuous-normalizing-flow, ode]
aliases: ["Flow Matching", "Rectified Flow", "Flow Matching Scheduler"]
level: 2
source_sha256: 13ab6140027142ed2d477d46684c7d5b47e39321fe353def17779be40b2a93fb
translation: machine
translated_at: '2026-10-24'
---
# Flow Matching : entraînement de champ vectoriel conditionnel {#flow-matching-conditional-vector-field-training}

[Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)
définit une manière sans simulation d'entraîner des flux normalisants continus (CNF).
Plutôt que d'exiger la simulation du flux appris pendant l'entraînement, le modèle
effectue une régression d'un champ vectoriel sur une famille choisie de chemins de probabilité conditionnels.

Le chemin compte. La formulation originale peut couvrir les chemins de diffusion
et les chemins de type transport optimal ; il ne s'agit pas d'une interpolation linéaire unique
ni d'une équation fixe pour tous les checkpoints.

## Ce que l'inférence intègre {#what-inference-integrates}

À l'inférence, un pipeline compatible part de sa distribution source configurée et
intègre numériquement le champ vectoriel appris jusqu'à obtenir un échantillon. Le solveur, le calendrier temporel, le conditionnement, le guidage et le nombre d'évaluations de fonction font partie du contrat du pipeline et du modèle.

Ne pas en déduire que chaque checkpoint de flow matching :

- accepte la même classe de scheduler ou le même décalage de schedule ;
- s'améliore à un nombre de pas particulier ;
- supporte une correspondance particulière de la force img2img ; ou
- peut affiner son propre résultat par passes répétées en toute sécurité.

Ces affirmations nécessitent des preuves de la part de l'éditeur du checkpoint et un résultat sur la tâche visée.

## Compatibilité des schedulers {#scheduler-compatibility}

Diffusers fournit
[FlowMatchEulerDiscreteScheduler](https://huggingface.co/docs/diffusers/api/schedulers/flow_match_euler_discrete)
comme une implémentation. Sa configuration exposée comprend les pas de temps d'entraînement, le comportement du décalage (shift), le décalage dynamique, les paramètres de longueur de séquence et des schedules de sigma alternatifs. Ces options décrivent une interface d'implémentation ; elles ne constituent pas des valeurs par défaut universelles à copier dans un autre modèle de flow.

Charger le scheduler et la configuration publiés avec le checkpoint chaque fois que possible. Si une expérience modifie le scheduler, le décalage, le solveur ou le schedule de pas, la traiter comme un nouveau contrat d'échantillonnage et conserver un résultat reproductible avant de l'utiliser en production.

## Protocole d'évaluation {#evaluation-protocol}

Pour chaque couple modèle/pipeline pris en charge :

1. consigner le checkpoint, les révisions du pipeline et du scheduler, la fixture d'entrée, la graine, les dimensions, le guidage, le nombre de pas et l'appareil/runtime ;
2. établir une petite grille supportée de nombres de pas ou de réglages de schedule ;
3. comparer le déterminisme des sorties, la fidélité pertinente pour la tâche, les artefacts et la latence ;
4. examiner la préservation en img2img ou en édition séparément de la qualité en text-to-image ; et
5. publier la configuration retenue avec sa fixture de validation et ses limites connues.

Ceci est particulièrement important pour la restauration et l'édition : une image peut paraître plus soignée tout en s'éloignant de la source, en modifiant du texte ou en altérant une propriété matérielle qui doit être préservée.

## Pages associées {#related-pages}

- [[diffusion-inference-acceleration]]
- [[SANA]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
