---
title: "Correction de la mire colorimétrique et de la balance des blancs"
description: "La correction par mire colorimétrique ou balance des blancs exige une mire physique mesurée ou un estimateur validé séparément ; la sortie d'un détecteur et une mire générée ne constituent pas une vérité terrain colorimétrique."
category: techniques
tags: [color-checker, white-balance, color-constancy, calibration, illumination, product-photography]
aliases: ["Color Constancy", "White Balance"]
level: 3
source_sha256: 5a3d13469de01f594e9b21b8c9868e1e970b539fd4ca35ecb8cfba0c8726357e
translation: machine
translated_at: '2026-10-24'
---
# Correction de la mire colorimétrique et de la balance des blancs {#color-checker-and-white-balance-correction}

La balance des blancs et la correction des couleurs résolvent des problèmes liés mais différents. La balance des blancs estime ou neutralise l'illuminant ; une transformation colorimétrique fait correspondre une réponse de capture ou de rendu donnée à une référence définie. Aucune des deux n'est fiable du simple fait qu'un objet ayant la forme d'une mire a été détecté dans une image.

## Définir ce qui fait référence {#decide-what-counts-as-a-reference}

Utilisez l'une de ces voies de preuve et consignez celle qui a été employée :

1. **Mire physique mesurée.** Capturez une mire connue dans le même éclairage et le même chemin optique que le sujet. Relevez ses patchs sur une capture non écrêtée et correctement exposée, puis comparez-les aux valeurs de référence de la mire.
2. **Estimateur validé séparément.** Un estimateur de balance des blancs ou d'illuminant par apprentissage peut être utile en l'absence de mire physique, mais il doit être validé sur la caméra cible, la chaîne de rendu, les matériaux et l'éclairage visés. Sa sortie est une estimation, non une mesure.

Pour la bijouterie et la photographie produit, conservez la capture source, l'identité de la mire, l'illuminant et la configuration, la transformation de rendu et les échantillons de validation. Un résultat agréable à l'œil ne suffit pas à prouver que les couleurs des métaux ou des gemmes sont exactes.

## Procédure avec mire physique {#physical-chart-workflow}

1. Photographiez la mire sous l'éclairage de capture, sans écrêter les hautes lumières et sans modifier l'exposition ni l'éclairage entre les images de référence et celles du produit.
2. Localisez la mire, ordonnez ses patchs et rejetez les images présentant des reflets, du flou, des occultations, une perspective extrême ou une correspondance incertaine des patchs.
3. Dérivez la transformation dans l'espace de travail déclaré et ne l'appliquez qu'aux captures régies par ce contrat d'étalonnage.
4. Validez sur des patchs neutres, de peau, de produit ou de matériau, choisis pour le livrable réel et non utilisés pour le calcul. Inspectez à la fois l'erreur numérique et l'image rendue.
5. Versionnez la transformation avec le profil caméra, la configuration optique et d'éclairage, le convertisseur raw et le justificatif de validation. Réétalonnez après tout changement matériel de configuration ou de chaîne de rendu.

La transformation ne doit pas combiner silencieusement balance des blancs, profil caméra, mappage tonal et étalonnage créatif. Gardez ces opérations explicites afin qu'une revue ultérieure puisse reproduire le résultat.

## La détection ne fait que localiser {#detection-is-only-localization}

[Colour Checker Detection](https://github.com/colour-science/colour-checker-detection) implémente des approches par segmentation, par gabarit et par apprentissage automatique. Son modèle YOLOv8 publié est entraîné pour ColorChecker Classic 24 et n'est pas un détecteur général pour les mires Nano ou SG. Le dépôt documente également des différences de licence pour le chemin d'inférence utilisant l'API Ultralytics.

En conséquence, figez la version du détecteur, le type de mire et la dépendance d'inférence, puis vérifiez l'ordre des patchs et la qualité des recadrages sur le jeu de captures réel. La détection peut trouver une mire candidate ; elle ne valide ni l'état de la mire, ni l'équivalence d'éclairage, ni l'exposition, ni la colorimétrie.

## Estimateurs par apprentissage et génératifs {#learned-and-generative-estimators}

[Deep White Balance](https://github.com/mahmoudnafifi/Deep_White_Balance) est une implémentation de recherche pour la correction de balance des blancs par apprentissage sur des images rendues. Elle peut être évaluée comme estimateur, mais ses données d'entraînement et ses hypothèses de rendu doivent être comparées à la chaîne de capture locale.

La constance des couleurs générative (GCC) est une direction de recherche différente : son [article](https://arxiv.org/abs/2502.17435) fait appel à un inpainting déterministe pour placer une mire virtuelle reflétant un éclairage de scène estimé. C'est utile pour étudier l'estimation d'illuminant, mais pas pour transformer des valeurs de patchs générées en cible mesurée. Une mire générée doit rester étiquetée comme estimation de modèle et ne doit jamais remplacer une référence physique dans un test de recette colorimétrique.

## Enregistrement minimal de recette {#minimal-acceptance-record}

Pour chaque lot étalonné, conservez :

- les identifiants de capture et de mire, l'empreinte de la source et l'espace colorimétrique déclaré ;
- la révision du détecteur ou de l'estimateur et tous les paramètres de transformation ;
- les images rejetées, avec le motif du rejet ;
- les images de validation hors échantillon et le critère de réussite ou d'échec ; et
- le relecteur ou la tâche automatisée qui a approuvé la mise en production.

Cela rend la correction des couleurs auditable lorsqu'une caméra, un dispositif d'éclairage, un modèle ou une chaîne de traitement raw change ultérieurement.

## Pages connexes {#related-pages}

- [[color-correction-by-numbers]]
- [[color-space-and-gamma-reference]]
- [[diffusion-inference-acceleration]]
