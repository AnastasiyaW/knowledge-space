---
title: "Correction des couleurs : contrat d'étalonnage lié aux mesures"
description: "La correction des couleurs n'est valide que par rapport à une cible de mesure, un illuminant, une caméra ou un profil, un espace de travail et une transformation de visualisation déclarés ; les échantillons neutres et les patchs de mire font foi lorsque leur provenance est connue, alors que les moyennes de scène et les ratios de couleur de peau ne constituent pas une vérité terrain universelle."
category: techniques
tags: [color-correction, white-balance, color-checker, calibration, profiles, evaluation]
aliases: ["Color Correction by Numbers", "White Balance Measurement"]
level: 3
source_sha256: ac7f1845139c6ec71538b30a498b2ff9ec167250b9d4caeedea97a7af1a773e4
translation: machine
translated_at: '2026-10-24'
---
# Correction des couleurs : contrat d'étalonnage lié aux mesures {#color-correction-measurement-bound-calibration-contract}

La correction numérique est défendable lorsque les valeurs sont rattachées à une cible de mesure déclarée et à un chemin de gestion des couleurs défini. Les moyennes de pixels, un ratio RGB global de la scène ou une règle supposée sur la couleur de peau n'établissent ni un illuminant, ni une réflectance, ni une réponse de caméra, ni un étalonnage créatif voulu.

## Commencer par une cible de correction {#start-with-a-correction-target}

Choisissez l'un de ces objectifs explicites avant de modifier les pixels :

| Objectif | Preuves requises |
|---|---|
| Étalonnage de capture | une cible connue, les conditions de capture, la transformation d'entrée et les valeurs de référence mesurées pour cette cible |
| Appariement inter-caméras | des prises de référence approuvées, les deux transformations caméra, les conditions de visualisation et l'acceptation par le relecteur |
| Étalonnage éditorial | une cible/un rendu défini par l'auteur et une politique d'approbation, et non une prétention à la neutralité physique |
| Proposition automatisée | une estimation bornée avec un indice de confiance et une relecture, et non une étiquette de vérité automatique |

La [cible ColorChecker White Balance de Calibrite](https://calibrite.com/us/product/colorchecker-white-balance/?noredirect=en-US)
est conçue comme une référence spectralement neutre pour la balance des blancs
personnalisée. Cela soutient un flux de travail fondé sur la mesure lorsque la cible
réelle est visible et traçable ; cela ne fait pas d'un mur quelconque, d'une
haute lumière écrêtée ou d'une moyenne d'image une référence neutre universelle.

## Lier la mesure {#bind-the-measurement}

Pour chaque correction, conservez :

- le type de cible, sa révision, son propriétaire, sa position dans la scène et le masque de la zone de cible ;
- l'illuminant et les conditions de capture, les réglages de la caméra, le décodeur raw ou le profil d'entrée, ainsi que tout traitement effectué dans l'appareil ;
- l'encodage source, la politique de linéarisation, l'espace de travail, les versions des transformations et la transformation de sortie/de visualisation ;
- les valeurs mesurées des patchs ou des zones neutres, avec leur méthode d'échantillonnage ; et
- la transformation proposée, le comportement de écrêtage et de gamut, la décision du relecteur et l'empreinte numérique de la sortie.

Les valeurs connues d'une mire dépendent de la mire, de l'illuminant, de la géométrie de mesure et de l'encodage. Ne figez pas un tableau unique de valeurs RGB pour des images en raw, en linéaire de scène, en référée à l'affichage ou ayant des profils différents.

## Utiliser un chemin de transformation géré {#use-a-managed-transform-path}

La [documentation des profils ICC](https://www.color.org/getting-started/) explique que les profils de périphériques se connectent via un Profile Connection Space défini. Un triplet RGB désigne des canaux de périphérique tant que son encodage et son profil ne sont pas connus.
[OpenColorIO](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html)
traite de même les espaces colorimétriques et les vues d'affichage comme des objets de configuration explicites. Appliquez une correction dans un chemin déclaré et validez ce chemin, plutôt que de supposer qu'un mode de fusion ou une courbe de canal isole la luminance dans tous les encodages.

Une implémentation peut estimer des gains, une matrice ou une autre transformation, mais elle doit exposer ses hypothèses. Si les métadonnées, la visibilité de la cible ou l'interprétation de l'entrée manquent, renvoyez une estimation relisible ou un état explicite d'impossibilité d'étalonnage, plutôt que d'inventer une référence numérique.

## Évaluer la couleur et le contenu ensemble {#evaluate-color-and-content-together}

Utilisez des captures de validation réalisées dans les conditions de capture et de diffusion prévues. Comparez les patchs de la cible ou les zones de référence approuvées après la même transformation de sortie que celle utilisée pour la diffusion, puis inspectez :

- l'erreur sur les zones neutres ou de cible selon la méthode de mesure déclarée ;
- l'écrêtage des hautes lumières et des ombres, la correspondance de gamut et la continuité des dégradés ;
- l'identité des produits et des matériaux, le texte, les masques et les zones protégées ; et
- l'apparence dans la configuration de visualisation validée.

Choisissez des métriques et des seuils adaptés à la tâche lors de la validation : un écart RGB unique, une hiérarchie de canaux ou un ratio de teinte de peau ne constituent pas un critère de mise en production pour tous les sujets, tous les illuminants ou tous les intentions de rendu.

## Frontière humaine et sécurité {#human-and-safety-boundary}

N'inférez pas l'origine ethnique, l'état de santé, l'attractivité ou une apparence humaine canonique à partir de valeurs de couleur. La peau humaine n'est pas une mire d'étalonnage. Lorsqu'une personne est concernée, utilisez un consentement, une référence visuelle approuvée et des critères de relecture qui ne transforment pas des mesures de couleur en étiquettes de traits sensibles.

## Pages connexes {#related-pages}

- [[color-checker-and-white-balance]]
- [[color-space-and-gamma-reference]]
- [[color-theory-for-ml]]
- [[intrinsic-decomposition]]
