---
title: "FP8 E4M3 : contrat de quantification mesuré"
description: "La quantification FP8 E4M3 constitue un contrat numérique propre à chaque version et à chaque backend ; il faut documenter le format de tenseur, la recette de mise à l'échelle, les opérations et le matériel pris en charge, les preuves de calibration ou d'amax, le chemin de sérialisation et d'exécution, ainsi que les mesures de qualité, de latence et de mémoire, et ne jamais substituer silencieusement un écrêtage ou un autre format."
category: optimization
tags: [fp8, e4m3, quantization, transformer-engine, inference, measurement]
aliases: ["FP8 Quantization Optimization for E4M3", "E4M3 Quantization"]
level: 3
source_sha256: b92587c3b44bf0a3a4b6319c99d06eaafa36e6052ff08ffe583d478183a5f0f9
translation: machine
translated_at: '2026-10-24'
---
# FP8 E4M3 : contrat de quantification mesuré {#fp8-e4m3-measured-quantization-contract}

FP8 n'est pas un interrupteur d'optimisation interchangeable. La
[documentation de Transformer Engine sur le current scaling](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/fp8_current_scaling/fp8_current_scaling.html)
décrit E4M3 comme un format FP8 comportant un bit de signe, quatre bits d'exposant,
trois bits de mantisse, des valeurs finies allant jusqu'à plus ou moins 448, ainsi que NaN.
Il l'oppose à E5M2, dont le compromis entre plage et précision diffère. Ces formats,
leurs noyaux et leurs recettes de mise à l'échelle ne doivent pas être substitués silencieusement.

## Sélectionner un chemin numérique documenté {#select-a-documented-numerical-path}

La version de Transformer Engine citée décrit le current scaling comme une échelle FP32
par tenseur : calcul de la valeur absolue maximale, mise à l'échelle vers la plage FP8 choisie,
puis conversion. Elle précise que cela nécessite deux lectures du tenseur. Cela explique un
compromis pour cette recette nommée ; cela ne justifie pas une échelle statique universelle, un chemin
d'écrêtage dur, un nombre de couches, une affirmation de latence ou une garantie matérielle pour un
autre framework ou un autre modèle.

Consigner la version exacte du framework ou du moteur, le GPU et le pilote, le modèle ou le checkpoint,
les paramètres de précision, les opérations prises en charge, la disposition des tenseurs ainsi que le
comportement en cas de repli ou d'erreur. Vérifier la matrice des périphériques et des opérations prises
en charge pour la version utilisée, plutôt que d'étendre un résultat documenté à un autre accélérateur
ou à un autre runtime.

## Conserver les preuves de calibration et de mesure {#keep-calibration-and-measurement-evidence}

Pour chaque chemin d'exécution prévu, conserver :

- le format de tenseur et la recette de mise à l'échelle par opération, en précisant si une stratégie
  documentée d'amax, de delayed, de block ou une autre est utilisée ;
- les entrées de calibration ou les preuves d'amax en temps réel, la politique de mise à jour de l'échelle,
  ainsi que les observations sur les valeurs aberrantes et la saturation ;
- le chargement des checkpoints, la sérialisation, la compilation et le chemin de service, y compris
  les endroits où les conversions ont lieu ;
- des exécutions de référence et FP8 comparables, avec la latence à chaud et en régime permanent, le pic
  de mémoire, le débit, la reproductibilité, les échecs numériques et les résultats de qualité sur la tâche ; et
- les seuils d'acceptation définis pour la tâche réelle, ainsi que l'environnement de mesure et
  l'ensemble d'évaluation disjoint des données de calibration.

La distribution d'activations, la passe de calibration ou le comportement du compilateur d'un modèle
ne certifient pas un autre modèle, une autre distribution de prompts, une autre résolution, une autre
forme de batch ou une autre phase d'entraînement.

## Frontière des échecs {#failure-boundary}

Si une opération ou un périphérique requis ne prend pas en charge le chemin déclaré, si les preuves d'amax
ou de qualité sont absentes, si une frontière de sérialisation modifie le format, ou si les mesures
dépassent le seuil de la tâche, signaler un état d'échec ou de revue visible. Ne pas remplacer E4M3 par E5M2,
désactiver la mise à l'échelle, écrêter des valeurs ni revenir à une autre précision tout en décrivant le
résultat comme une même exécution FP8.

## Pages liées {#related-pages}

- [[low-vram-inference-strategies]]
- [[diffusion-inference-acceleration]]
- [[diffusion-lora-training]]
- [[tiled-inference]]
