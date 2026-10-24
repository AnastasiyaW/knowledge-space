---
title: "Données de détection synthétiques : pipeline de preuves et de revue"
description: "Les données de détection synthétiques constituent un corpus de candidats étiquetés, et non une vérité terrain automatique ; conservez la provenance du générateur et des sources, relisez les annotations, empêchez les fuites entre partitions et validez sur des données réelles mises de côté."
category: pipelines
tags: [synthetic-data, object-detection, annotations, provenance, review, dataset-quality, validation]
aliases: ["Synthetic Dataset Pipeline for Object Detection", "Synthetic Detection Dataset"]
level: 2
source_sha256: 008f3f7fa10d92702831ff8795c800a8298a2135b5add37481b132e8372ceab1
translation: machine
translated_at: '2026-10-24'
---
# Données de détection synthétiques : pipeline de preuves et de revue {#synthetic-detection-data-evidence-and-review-pipeline}

Les images synthétiques et les annotations générées par modèle peuvent accélérer la création de jeux de données, mais ce sont des preuves candidates, et non une vérité terrain automatique. Un détecteur entraîné uniquement sur les motifs d'un générateur peut sembler performant sur un jeu de validation synthétique, puis échouer sur les images réelles auxquelles il est destiné.

## Manifeste des sources et du générateur {#source-and-generator-manifest}

Pour chaque image source ou générée, conservez :

- le condensé (digest) de l'entrée/référence et la décision de droits/licence ;
- le générateur, le modèle de base, le point de contrôle (checkpoint), les entrées de prompt/contrôle, la graine (seed) et le condensé de la sortie ;
- les classes d'objets visées et la révision de la taxonomie ;
- le producteur/la révision du modèle d'annotation ainsi que la sortie brute des candidats ; et
- une étiquette de provenance distinguant les contenus capturés, rendus, transformés et générés.

Ne prétendez pas qu'une image représente un objet réel, un défaut réel ou un fait produit simplement parce qu'un générateur ou un outil d'étiquetage automatique l'a désignée ainsi.

## Création des candidats et annotation {#candidate-creation-and-annotation}

Utilisez des détecteurs, segmenteurs, outils de légendage ou métadonnées de rendu automatiques pour proposer des boîtes, des masques et des classes. Conservez la proposition brute et présentez-la dans un outil de revue permettant la correction, le rejet, l'ajout d'objets manquants et l'escalade des étiquettes ambiguës.

L'enregistrement d'annotation final doit comporter le réviseur ou la version de la politique, le condensé de la source, la version de la taxonomie, la géométrie, la confiance ou l'incertitude, ainsi que la raison de la décision. N'utilisez pas de seuil universel de confiance, de similarité ou de qualité d'image ; calibrez chaque règle à partir d'exemples relus localement.

## Découpage sans fuite {#split-without-leakage}

Découpez par scène source, produit, sujet, gabarit, recette de génération ou session de capture, et non simplement par fichier. Les variantes synthétiques quasi identiques, les arrière-plans partagés ou les descendants générés doivent rester du même côté d'une frontière entre entraînement et jeu de test. Conservez la logique de découpage et ses exceptions dans le manifeste du jeu de données.

Conservez un jeu de test réel et disjoint par source chaque fois que le déploiement visé traite des images réelles. Un score uniquement synthétique est une mesure d'alignement avec le générateur, et non une preuve de performance en conditions réelles.

## Entraînement et validation {#train-and-validate}

Liez la version du jeu de données à l'architecture du détecteur, à la configuration d'entraînement, à la correspondance des classes et aux jeux d'évaluation. Examinez :

- la couverture des annotations et les faux positifs sur un échantillon audité représentatif ;
- les conditions de petits objets, d'occlusion, d'éclairage, de matériau et d'arrière-plan ;
- les performances sur des données réelles mises de côté et sur des groupes de sources absents de l'entraînement ;
- la calibration de la confiance par rapport à l'erreur réelle ; et
- les cas d'échec qui nécessitent une collecte de données plutôt qu'une extension synthétique.

Publiez les métriques avec le manifeste exact du jeu de données et la partition de test. Ne généralisez pas un résultat d'une taxonomie d'objets à une autre.

## Porte de publication {#release-gate}

Ne publiez un jeu de données que lorsque les droits, la provenance, la revue des annotations, l'intégrité des partitions, la validation sur données réelles et les obligations de retour arrière ou de retrait sont documentés. Si le générateur ou le modèle d'annotation change, créez une nouvelle version du jeu de données et refaites la validation.

## Pages associées {#related-pages}

- [[face-detection-filtering-pipeline]]
- [[rights-first-text-to-mask-training]]
- [[flux-klein-jewelry-photography]]
- [[diffusion-lora-training]]
