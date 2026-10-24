---
title: "Décomposition intrinsèque : contrat d'hypothèses et de revue"
description: "La décomposition intrinsèque est une estimation bornée par l'ambiguïté de la réflectance et de l'éclairage, et non une vérité terrain. Fixez les hypothèses de formation de l'image, le modèle et sa version, le domaine colorimétrique, la politique relative aux résidus, les preuves sources et la revue propre à la tâche avant d'utiliser ses sorties d'albédo ou d'ombrage pour l'édition ou le relighting."
category: techniques
tags: [intrinsic-decomposition, albedo, illumination, reflectance, shading, relighting, evidence]
aliases: ["Albedo and Illumination Separation", "Intrinsic Image Decomposition"]
level: 3
source_sha256: a00166d35927c5b5a9cc80ad23ba033b91be26894bfa867c4c5eb8a7a62bc255
translation: machine
translated_at: '2026-10-24'
---
# Décomposition intrinsèque : contrat d'hypothèses et de revue {#intrinsic-decomposition-assumption-and-review-contract}

La décomposition intrinsèque estime des composantes telles que la réflectance (souvent appelée albédo) et l'ombrage à partir d'une image. Il ne s'agit pas d'une mesure du matériau ou de l'éclairage d'une scène photographiée. Dans un modèle diffus simplifié, une image observée peut s'exprimer par `I ≈ R ⊙ S + E`, où `R` est la réflectance, `S` l'ombrage dépendant de l'éclairage, et `E` absorbe les effets que le modèle ne représente pas. Les images réelles comportent des spécularités, de la transparence, de la diffusion sous-surfacique, des traitements du capteur, des écrêtages et un éclairage mixte. Une image RVB unique ne détermine généralement pas ces composantes de façon unique.

## Déclarer le contrat de décomposition {#declare-the-decomposition-contract}

Pour chaque sortie, conservez :

- l'empreinte du fichier source, le recadrage et l'orientation, l'encodage colorimétrique, la politique de canal alpha, ainsi que l'indication selon laquelle le modèle reçoit des valeurs linéaires, référencées à la scène ou référencées à l'affichage ;
- la version exacte du modèle, les poids, l'environnement d'exécution, les entrées de prompt ou de référence, et les hypothèses de formation de l'image que la méthode documente ;
- les sorties nommées, leurs unités et normalisation, la gestion des résidus ou de la confiance, et les pixels qui n'ont pas d'estimation fiable ;
- l'usage prévu, par exemple un aperçu en éclairage seul ou une recoloration contrainte, ainsi que le contenu protégé ;
- la source de comparaison, la vérification numérique ou de reconstruction lorsqu'elle est pertinente, et la revue visuelle à la résolution de livraison.

La sortie de type albédo d'une méthode ne peut pas remplacer l'albédo, la normale, le matériau ou l'entrée de relighting d'une autre méthode sans un test de compatibilité propre à l'implémentation.

## Considérer les estimations comme dépendantes du modèle {#treat-estimates-as-model-scoped}

La tâche couvre des observations et des hypothèses différentes. Par exemple, [Décomposition intrinsèque de scène à partir d'images RGB-D](https://openaccess.thecvf.com/content_iccv_2015/html/Hachama_Intrinsic_Scene_Decomposition_ICCV_2015_paper.html) utilise la profondeur et un modèle d'éclairage explicite, tandis que [Transformation d'images intrinsèques par décomposition de l'espace d'échelle](https://openaccess.thecvf.com/content_cvpr_2018/html/Cheng_Intrinsic_Image_Transformation_CVPR_2018_paper.html) présente les sorties à partir d'une seule image comme des estimations apprises d'image à image. Ces articles n'établissent pas qu'une sortie nommée est physiquement correcte pour des photographies RVB arbitraires, la peau, des produits, des objets transparents ou une version ultérieure du modèle.

Ne sélectionnez une méthode qu'après avoir testé la version exacte sur des images représentatives et sur l'opération en aval. Consignez les cas d'échec, tels que les ombres dures, les reflets spéculaires, les sources lumineuses écrêtées, les couleurs saturées, l'éclairage mixte, les structures fines et les artefacts de traitement de la caméra.

## Utiliser un flux d'édition contraint {#use-a-constrained-edit-workflow}

1. Vérifiez que la source, les droits, le recadrage, le domaine colorimétrique et les zones protégées relèvent du périmètre du travail.
2. Produisez l'estimation annoncée et conservez l'association entre la source et la sortie.
3. Inspectez le résidu et les zones sujettes à l'ambiguïté avant de considérer une valeur comme réflectance ou ombrage.
4. N'appliquez que la modification approuvée, sur des masques explicites. Une couche basse fréquence ou de type albédo n'autorise pas la modification de chaque pixel de matériau ou de visage.
5. Ne recomposez qu'avec la routine déclarée par le modèle. Si une image générée, un écrêtage, un mélange ou une étape non linéaire intervient, étiquetez le résultat comme dérivé et non comme reconstruction exacte.
6. Comparez la source et le résultat à la résolution de livraison afin de détecter la dérive colorimétrique, les halos, les échanges d'ombre ou de matériau, la perte de détail, les modifications de géométrie et les altérations du contenu protégé.

Le transfert de couleur dans le domaine de l'albédo peut être une expérience utile lorsque l'éclairage perturbe une modification de couleur. Il exige néanmoins une comparaison tenant compte de la source et ne prouve pas que la couleur cible est physiquement correcte. Conservez un résidu uniquement lorsque la méthode choisie le définit et que le contrat de sortie précise comment il est combiné.

## Limites d'échec et frontière de livraison {#failure-and-release-boundary}

Ne remplacez pas silencieusement une estimation incertaine par un autre modèle, n'ajoutez pas de texture générée et ne présentez pas un résultat relit comme des données sources récupérées. Renvoyez un état de revue ou d'échec visible lorsque les hypothèses sont inconnues, lorsque l'environnement d'exécution ne peut pas reproduire la sortie déclarée, lorsque le résidu n'est pas expliqué ou lorsque la revue révèle une modification du contenu protégé.

## Pages connexes {#related-pages}

- [[color-space-and-gamma-reference]]
- [[color-checker-and-white-balance]]
- [[frequency-decomposition-editing]]
- [[tiled-inference]]
