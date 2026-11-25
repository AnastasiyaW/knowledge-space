---
title: "Détection et filtrage de visages : pipeline de revue des candidats"
description: "Le filtrage de visages est un pipeline de sélection de candidats préservant la provenance ; les boîtes et points de repère du détecteur facilitent la revue, mais n'établissent ni l'identité, ni le consentement, ni le réalisme de l'image, ni son aptitude à l'entraînement."
category: workflows
tags: [face-detection, dataset-curation, provenance, quality-control, privacy, review]
aliases: ["Face Detection & Filtering Pipeline", "Face Dataset Review"]
level: 2
source_sha256: 8703837c0cf152ad9e399e0f68979602911ba1ff110e339913b9e037f2a9a5bb
translation: machine
translated_at: '2026-10-24'
---
# Détection et filtrage de visages : pipeline de revue des candidats {#face-detection-and-filtering-candidate-review-pipeline}

La détection de visages doit produire des candidats à la revue et des éléments de preuve structurés, et non une affirmation automatique selon laquelle une image représente une personne réelle, dispose d'un consentement utilisable ou convient à l'entraînement. Gardez la décision de filtrage traçable jusqu'à une entrée et jusqu'à une politique déclarée.

## Inventaire avant inférence {#inventory-before-inference}

Créez un manifeste d'entrée immuable comportant un condensé (digest), l'emplacement de la source, les preuves de licence ou de consentement, l'heure d'ingestion et la classe d'accès pour chaque ressource. Ne remplacez pas ce manifeste par un score du détecteur. Il reste la référence pour les droits, la conservation et l'audit en aval.

## Étape de détection des candidats {#candidate-detection-stage}

Exécutez un détecteur versionné et enregistrez le condensé d'entrée, la révision du modèle, la boîte, la confiance, les coordonnées de recadrage et l'état d'erreur. Le [MediaPipe Face Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector/python) accepte des entrées image et vidéo et renvoie les positions des visages accompagnées de six points-clés : les yeux, le bout du nez, la bouche et les points du tragus des oreilles. Ces sorties peuvent faciliter la revue du recadrage et de l'orientation.

Elles n'établissent ni l'identité d'une personne, ni son consentement, ni son âge, ni son émotion, ni le fait que le visage représenté soit photographique plutôt que synthétique. Traitez la confiance du modèle comme un signal de classement dont le seuil est calibré localement, et non comme un critère d'acceptation universel.

## Filtres de qualité et de pertinence {#quality-and-relevance-gates}

Définissez d'abord l'usage cible, puis ne mesurez que les propriétés pertinentes :

1. **Cadrage :** surface visible suffisante et recadrage compatible avec la tâche d'entraînement ou de retouche visée.
2. **Qualité d'image :** netteté, dégradations de compression, écrêtage, occultation et résolution, revus à partir d'exemples étiquetés localement.
3. **Éditabilité :** uniquement lorsque la tâche déclarée l'exige ; conservez la justification du relecteur plutôt que de l'inférer à partir d'un score générique de visage.
4. **Droits et vie privée :** preuves de consentement ou de licence, classe de conservation et approbation pour l'usage dérivé prévu.

Les scores automatisés peuvent trier la file d'attente, mais les cas incertains doivent rester en revue, sans être silencieusement acceptés ou écartés.

## Similarité, doublons et découpages {#similarity-duplicates-and-splits}

Utilisez une similarité perceptuelle ou par embeddings pour proposer des groupes de doublons et de quasi-doublons. Conservez chaque enregistrement source, consignez le modèle de regroupement et le seuil, et demandez à un relecteur ou à une règle de politique explicite de décider quelle représentation peut être utilisée. N'utilisez jamais un score de similarité comme preuve que deux images montrent la même personne.

Pour l'évaluation des modèles, découpez par source, par session de capture ou par groupe de sujets connu lorsque ces informations sont disponibles. Cela évite que des images quasi identiques ne fuient entre les partitions d'entraînement et de validation. Consignez la règle de découpage et ses exceptions.

## Schéma de sortie et décision de publication {#output-schema-and-release-decision}

Chaque résultat doit comporter :

- le condensé d'entrée et un pointeur vers la provenance ;
- les révisions du détecteur et du modèle de qualité, ainsi que leurs sorties brutes ;
- la décision (accepter, réviser ou rejeter) assortie d'un code de motif ;
- la version du relecteur ou de la politique ; et
- les restrictions en aval, y compris les obligations de suppression et de conservation.

Seul un enregistrement « accepter », accompagné de preuves de droits et d'une portée d'usage déclarée, peut entrer dans un jeu d'entraînement de retouche de visages. Le reste demeure traçable en vue d'une correction ou d'un audit.

## Pages connexes {#related-pages}

- [[face-beautify-edit-lora]]
- [[rights-first-text-to-mask-training]]
- [[diffusion-lora-training]]
