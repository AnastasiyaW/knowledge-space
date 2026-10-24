---
title: "Détection de défauts et de petits objets : contrat de preuve"
description: "La détection de défauts et de petits objets produit des candidats examinables, et non une vérité automatique sur la qualité ; liez le modèle, le protocole de capture, la politique d'annotation ou de référence normale, la correspondance de découpage ou de fusion, les seuils et l'évaluation disjointe par source avant toute décision d'inspection ou de flux de travail."
category: reference
tags: [defect-detection, anomaly-detection, small-objects, inspection, provenance, evaluation, tiling]
aliases: ["Anomaly Detection", "Defect Detection Models", "Small Object Detection"]
level: 3
source_sha256: ce70ab843b008e778197e00f6385e7eb855943a70269c0d37780326c0e7d05d2
translation: machine
translated_at: '2026-10-24'
---
# Détection de défauts et de petits objets : contrat de preuve {#defect-and-small-object-detection-evidence-contract}

Les systèmes de détection et d'anomalies identifient des candidats à inspecter. Une boîte, un masque, une carte de chaleur ou un score ne constitue pas une preuve qu'un produit est défectueux, qu'une modification visuelle a été introduite, ni qu'une image peut être publiée en toute sécurité. Liez les conditions de capture, la définition de la tâche, le modèle et la politique de revue avant d'utiliser un résultat dans une décision opérationnelle.

## Choisir explicitement la tâche {#choose-the-task-explicitly}

| Tâche | Supervision ou référence requise | Signification du résultat |
|---|---|---|
| Détection ou segmentation supervisée | taxonomie de classes approuvée et annotations liées aux sources | classe/région candidate |
| Détection d'anomalies | une politique de référence normale définie et des exclusions connues | écart par rapport à cette distribution de référence |
| Comparaison avant/après | captures appariées alignées et autorisées, politique de changement | différence candidate |

[EfficientAD](https://anomalib.readthedocs.io/en/v2.0.0/markdown/guides/reference/models/image/efficient_ad.html)
est documenté dans Anomalib comme une méthode d'anomalie de type student-teacher. Son article évalue une famille de modèles particulière sur des jeux de données nommés. Aucune de ces sources ne fait d'une carte d'anomalie un label de défaut universel, ne fixe un seuil sûr pour tous les matériaux, ni ne garantit un budget fixe de latence ou de mémoire sur un autre runtime.

## Lier les preuves de capture et d'entraînement {#bind-capture-and-training-evidence}

Pour chaque échantillon ou référence normale, conservez :

- l'identité de l'actif ou de la capture d'origine, les droits, et le périmètre produit ou scène ;
- la caméra, l'objectif, la distance, la mise au point, l'éclairage, le fond et les conditions de traitement qui affectent la texture visible ;
- la taxonomie de la tâche, les exemples d'inclusion et d'exclusion, la révision des annotations et la provenance des relecteurs ;
- le modèle ou point de contrôle, le prétraitement, la résolution d'entrée, le runtime et la politique de seuil ; et
- l'incertitude, les candidats rejetés et les facteurs confondants connus.

Les reflets spéculaires, la compression, la poussière sur le chemin de capture, les changements de mise au point, les reflets de fond et les modifications de géométrie peuvent paraître anormaux. Séparez les observations réelles des défauts synthétiques et n'utilisez pas une augmentation comme preuve qu'un détecteur de défauts réels est validé.

## Traiter le découpage comme un contrat de coordonnées {#treat-slicing-as-a-coordinate-contract}

[SAHI](https://obss.github.io/sahi/guides/sliced-inference/) documente les tranches qui se chevauchent, la détection par tranche et la fusion vers les coordonnées de l'image complète. Si une inspection haute résolution utilise des tuiles, consignez avec la prédiction la géométrie des tuiles, le chevauchement, la transformation d'entrée, la correspondance des coordonnées, la règle de fusion ou de suppression, et le traitement des bords. La fusion des tuiles d'un détecteur ne valide pas une carte de chaleur d'anomalie ni une jointure de retouche pixel.

Évaluez les candidats sur l'image d'origine. Un aperçu sous-échantillonné peut masquer précisément le très petit objet ou l'artefact de surface que le système prétend signaler.

## Valider pour l'environnement cible {#validate-for-the-target-environment}

Séparez les données d'entraînement, de réglage et de test selon l'actif d'origine, le produit ou le sujet, la session de capture et la chaîne de dérivation. Les jeux de validation doivent inclure les variations de matériau, d'échelle, d'éclairage et de capture attendues à la mise en production. Présentez une analyse d'erreurs propre à la tâche, incluant la charge de faux candidats et les cas critiques manqués, au lieu de transférer des valeurs d'AUROC, de mAP, de VRAM ou de latence issues d'un benchmark ou d'un autre appareil.

Revoyez les régions prédites par rapport à l'image source et à la définition de tâche approuvée. Gardez les modifications de seuil versionnées, et revalidez lorsque la caméra, l'éclairage, le prétraitement, le plan de tuilage, le modèle ou le runtime changent.

## Porte de publication {#release-gate}

Ne publiez que des candidats examinables, accompagnés de la provenance du modèle et de la configuration, ainsi que d'un état d'incertitude ou d'échec visible. Ne rejetez pas automatiquement l'inventaire, n'effacez pas les détails de retouche, et ne rendez pas de verdict de sécurité ou de qualité uniquement à partir du score d'un détecteur. Si la politique exige une action automatique, définissez son autorité bornée, le contrôle de contre-vérification, le reçu d'audit et la procédure de retour arrière avant l'activation.

## Pages associées {#related-pages}

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[skin-retouch-pipeline]]
- [[synthetic-dataset-pipeline]]
