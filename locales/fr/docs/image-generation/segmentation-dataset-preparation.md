---
title: "Préparation des jeux de données de segmentation : contrat de provenance et de supervision"
description: "La préparation d'un jeu de données de segmentation est un contrat de provenance et de supervision : lier source et droits, politique d'annotation et sémantique des masques, découpages disjoints par groupe, comportement des augmentations et de l'interpolation, couverture des classes et métriques de publication, et échouer en mode sécurisé en cas de fuite, d'étiquettes non revues ou de cibles incompatibles."
category: techniques
tags: [segmentation, dataset, annotations, masks, augmentation, splits, provenance, evaluation]
aliases: ["Binary Small-Object Segmentation Dataset", "Segmentation Data Preparation"]
level: 2
source_sha256: a2baa617d2e7f0fb9e993eb5f06c7a160d7b3df6705ba50171ac8a923d3499df
translation: machine
translated_at: '2026-10-24'
---
# Préparation des jeux de données de segmentation : contrat de provenance et de supervision {#segmentation-dataset-preparation-lineage-and-supervision-contract}

Un jeu de données de segmentation ne se résume pas à des images et des masques. C'est un système de supervision versionné : les assets sources, les droits, la politique d'annotation, la sémantique des masques, les règles d'échantillonnage, les unités de découpage, les transformations et l'évaluation doivent être cohérents entre eux. Un modèle peut produire des superpositions séduisantes tout en s'entraînant sur des fuites de données, des masques mal alignés ou des étiquettes qui ne représentent pas la tâche visée.

## Définir le contrat d'échantillon et d'annotation {#define-the-sample-and-annotation-contract}

Pour chaque asset source et chaque recadrage dérivé, conserver un identifiant stable de source/groupe, le digest de l'asset, les droits et la finalité autorisée, la provenance d'acquisition et de prétraitement, la version de l'annotation et le statut de relecture, la taxonomie des classes, la géométrie, l'encodage du masque, la sémantique des pixels ignorés ou inconnus, ainsi que tout score de confiance ou motif d'exclusion. Préciser si un masque est binaire, multiclasse, sensible aux instances, souple ou partiellement étiqueté. Ne jamais déduire le sens d'une classe à partir de la seule valeur d'un canal 8 bits.

Inspecter ensemble l'image source, le masque, la superposition, les métadonnées et les effectifs par classe. Mettre en quarantaine les étiquettes illisibles, dupliquées, ambiguës ou non revues, plutôt que de les convertir silencieusement en arrière-plan.

## Découper selon la véritable unité de fuite {#split-by-the-real-leakage-unit}

Tous les recadrages, augmentations, images d'une séquence, quasi-doublons et vues répétées qui partagent une même source causale doivent rester dans un même groupe de découpage. Le groupe approprié peut être une image source, un sujet, un produit, une scène, une session, une fenêtre temporelle ou un dispositif de capture ; documenter pourquoi ce groupe correspond à la frontière attendue en déploiement.

[GroupKFold de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) garantit des groupes non chevauchants, mais il ne peut pas choisir la bonne définition de groupe ni prouver que deux assets ne sont pas des doublons. Après chaque découpage, conserver les manifestes et vérifier qu'aucun groupe, digest d'asset ou lignée de dérivés ne traverse les ensembles d'entraînement, de validation ou de test. Examiner la couverture par classe après le regroupement ; ne jamais corriger un découpage de classe rare en laissant fuir des recadrages apparentés.

## Garder images et supervision synchronisées {#keep-images-and-supervision-synchronized}

Toute transformation spatiale doit mettre à jour chaque cible pertinente avec la même géométrie échantillonnée. Toute transformation ne portant que sur les pixels doit être vérifiée au regard de la sémantique des cibles. La [documentation d'Albumentations sur les cibles](https://albumentations.ai/docs/2-core-concepts/targets/) distingue les cibles de type image et les cibles de type masque, et explique pourquoi les masques catégoriels nécessitent normalement une interpolation compatible avec les masques. La version exacte de la bibliothèque et la configuration du pipeline doivent néanmoins figurer dans la publication du jeu de données.

Enregistrer l'interpolation de recadrage, de remplissage et de redimensionnement, la rotation, la gestion des valeurs de masque, les pixels ignorés, les transformations activées par découpage, ainsi que le routage de toute cible annexe comme les boîtes, les instances, la profondeur ou les métadonnées. Une transformation non prise en charge pour la cible déclarée doit échouer, plutôt que de générer une supervision plausible mais désalignée.

## Évaluer le jeu de données publié, et non un recadrage commode {#evaluate-the-released-dataset-not-a-convenient-crop}

Figer un jeu de test disjoint par source avant d'ajuster les seuils ou les fonctions de perte. Rapporter des métriques par classe et sensibles aux groupes, les effectifs d'échantillons, l'incertitude et la couverture, ainsi que des superpositions qualitatives à la résolution livrée. Choisir le modèle, la résolution, la fonction de perte, la pondération des classes, le seuil et l'augmentation à partir de cette expérience versionnée ; il n'existe pas de configuration de sortie binaire ni de poids de perte universels pour les objets rares.

Pour les cibles petites ou critiques pour la sécurité, inspecter par groupe de source les faux négatifs, les faux positifs, les frontières et les cas de masque vide. Maintenir une taxonomie des erreurs afin que les futures annotations et collectes de données puissent être améliorées sans réécrire les étiquettes historiques.

## Limite d'échec et de publication {#failure-and-release-boundary}

Bloquer la publication d'un jeu de données lorsque les droits sur la source ou la politique d'étiquetage sont absents, qu'un chevauchement de groupes est détecté, que des transformations sont incompatibles, que la sémantique des classes ou des masques est ambiguë, que des exemples de test ont servi à l'ajustement, ou que des annotations ne possèdent pas la relecture requise. Ne jamais supprimer silencieusement des enregistrements, réétiqueter des pixels inconnus, substituer un découpage ou fusionner des instances dans l'arrière-plan pour améliorer artificiellement une métrique.

## Pages liées {#related-pages}

- [[in-context-segmentation]]
- [[rights-first-text-to-mask-training]]
- [[defect-detection-small-objects]]
- [[paired-training-for-restoration]]
