---
title: "RealRestorer : restauration d'images réelles généralisable"
description: "RealRestorer est un flux de restauration reposant sur un grand modèle d'édition d'images, pour neuf types de dégradation documentés ; utilisez le runtime local corrigé du dépôt et évaluez la fidélité séparément des scores de benchmark."
category: models
tags: [image-restoration, deblur, denoise, dehaze, derain, compression-artifacts, low-light, moire, flare, reflection]
aliases: ["RealRestorer", "RealIR-Bench"]
level: 2
source_sha256: 6490d45ffa0b5fbf0d429f33258786396337969b1e43e72501f3f0fd3c1d7fe4
translation: machine
translated_at: '2026-10-24'
---
# RealRestorer : restauration d'images réelles généralisable {#realrestorer-generalizable-real-world-image-restoration}

**Périmètre vérifié : 2026-09-04.** RealRestorer est un flux de restauration d'images publié, construit autour d'un grand modèle d'édition d'images. Le projet combine un modèle, un pipeline de dégradation synthétique et du matériel d'évaluation RealIR-Bench afin de traiter neuf catégories de dégradation réelles documentées. Il s'agit d'une pile de recherche et d'ingénierie, et non d'une API de restauration générique installable avec `pip install`.

## Classes de tâches prises en charge {#supported-task-classes}

Le dépôt actuel documente des flux guidés par prompt pour le flou, les artefacts de compression, les reflets de lentille (lens flare), le moiré, la brume, les images en faible luminosité, le bruit, la pluie et les reflets. Sélectionnez délibérément une seule catégorie de tâche et conservez le prompt de tâche avec l'exécution ; des instructions vagues peuvent inciter un modèle d'édition d'images à modifier le contenu au-delà de la dégradation.

Pour chaque sortie, distinguez :

- la suppression de la dégradation demandée ;
- la préservation de l'identité, de la géométrie, du texte et des petits détails de produit ;
- les détails inventés, le lissage ou les changements sémantiques indésirables ;
- la vraisemblance visuelle par rapport à la restauration fidèle à la source.

Pour les documents, les éléments de preuve, l'identité des produits ou les mesures, considérez l'image originale comme référence. Une restauration générée doit être signalée comme sortie dérivée et vérifiée par rapport à l'original.

## Limites du runtime publié {#published-runtime-boundary}

Le démarrage rapide officiel exige actuellement le dossier local corrigé `diffusers/` inclus dans le dépôt RealRestorer. Il installe ce dossier en mode éditable et vérifie que `RealRestorerPipeline` peut être importé avant l'inférence. Une installation générique de la bibliothèque Diffusers ne fournit pas nécessairement le même pipeline.

Partez du dépôt actuel et conservez :

1. le commit du dépôt, la révision locale corrigée de Diffusers, l'environnement Python et les empreintes (digests) de tous les artefacts de modèle ;
2. l'image d'entrée, la catégorie de dégradation sélectionnée, le prompt, la graine (seed), la précision et les paramètres d'inférence ;
3. l'image de sortie et une comparaison explicite avec la source ;
4. les journaux d'erreurs et un retour à l'image source non modifiée.

Le dépôt fournit également un pipeline de dégradation synthétique et le code d'évaluation des benchmarks. Gardez les données de test synthétiques séparées des images de production réelles, afin qu'un jeu de données de benchmark ne soit jamais pris pour une preuve en conditions réelles.

## Les benchmarks sont des éléments de preuve, pas un certificat de publication {#benchmarks-are-evidence-not-a-release-certificate}

RealIR-Bench combine une mesure de distance perceptuelle et un score fondé sur un VLM dans le score qu'il rapporte. Cela peut étayer une comparaison reproductible dans le cadre de benchmark déclaré, mais cela ne permet pas de prouver la fidélité à la source pour une autre image, la conformité des licences ou l'exactitude d'une retouche publiée.

Associez à tout résultat de benchmark un jeu de revue spécifique à la tâche, assorti de contrôles stricts de préservation. Si un critère d'acceptation est « ne pas altérer un logo, un visage, une pierre, un texte de document ou une mesure », intégrez-le comme fixture explicite et inspectez-le à la résolution de livraison.

## Licences et déploiement {#licensing-and-deployment}

Le code, les dépendances corrigées, les poids des modèles, les données de benchmark, les démonstrations hébergées et les artefacts des modèles de base peuvent être soumis à des conditions actuelles distinctes. Vérifiez la licence exacte du dépôt et de la fiche du modèle, les restrictions d'accès, les conditions de redistribution et les droits sur les images d'entrée avant tout déploiement commercial ou hébergé. Ne déduisez pas une décision d'usage commercial d'une seule étiquette de métadonnées.

## Références {#references}

- [Dépôt officiel de RealRestorer](https://github.com/yfyang007/RealRestorer)
- [Article RealRestorer](https://arxiv.org/abs/2603.25502)
- [Collection de modèles RealRestorer](https://huggingface.co/RealRestorer/RealRestorer)
- [Jeu de données RealIR-Bench](https://huggingface.co/datasets/RealRestorer/RealIR-Bench)
