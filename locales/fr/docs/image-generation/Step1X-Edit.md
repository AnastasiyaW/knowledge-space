---
title: "Step1X-Edit : édition d'images spécifique à chaque version"
description: "Step1X-Edit est une famille multimodale d'édition d'images de StepFun, avec des pipelines propres à chaque version ; associez chaque point de contrôle à la branche Diffusers documentée correspondante et vérifiez indépendamment les conditions d'utilisation du modèle et des artefacts."
category: models
tags: [image-editing, step1x, stepfun, multimodal, diffusion, lora, gedit-bench]
aliases: ["Step1X-Edit"]
level: 3
source_sha256: 7f65df47c40baaae86eb2bd4337af8f539abfefe2dd5f204e1f372ce4d221037
translation: machine
translated_at: '2026-10-24'
---
# Step1X-Edit : édition d'images spécifique à chaque version {#step1x-edit-release-specific-image-editing}

**Périmètre vérifié : 2026-09-04.** Step1X-Edit est la famille de recherche et de modèles open source de StepFun dédiée à l'édition d'images. L'approche publiée utilise un modèle de langage multimodal pour traiter une image de référence et une instruction d'édition, puis couple la représentation latente obtenue à un décodeur d'images par diffusion. Il s'agit d'une pile d'édition d'images, et non d'une couche de compatibilité générique pour tous les modèles d'image.

## Traiter chaque version comme une cible d'intégration distincte {#treat-each-release-as-its-own-integration-target}

Le dépôt amont actuel documente le modèle d'origine ainsi que les versions plus récentes `v1p1` et `v1p2`. Le runtime local dépend explicitement de la version : l'amont désigne des classes de pipeline et des branches Diffusers différentes selon les points de contrôle. Sélectionnez la fiche du modèle, la révision du dépôt, la branche de dépendances et l'exemple d'une version donnée comme une unité de compatibilité unique.

Ne déduisez pas qu'un modèle d'édition d'images d'un autre éditeur est une variante de Step1X-Edit au seul motif que les deux utilisent un conditionnement multimodal ou la diffusion. En particulier, les versions d'édition d'images Qwen sont des artefacts distincts, avec leurs propres pipelines et conditions.

## Ce que fournit le projet officiel {#what-the-official-project-provides}

Le dépôt officiel fournit :

- des exemples d'inférence locale pour les versions documentées ;
- les artefacts de modèles et une ressource d'évaluation GEdit-Bench ;
- des scripts de fine-tuning et un exemple de chemin LoRA pour le modèle d'origine ;
- des intégrations optionnelles de performance et des intégrations communautaires, chacune avec sa propre limite de compatibilité.

Le projet distingue également une version plus récente orientée raisonnement des variantes antérieures. Une recette d'inférence sans gestion de version n'est donc pas sûre : un pipeline qui s'importe ou s'exécute pour un point de contrôle ne prouve pas qu'il est correct pour un autre.

## Contrat d'intégration sécurisé {#safe-integration-contract}

1. Choisissez un point de contrôle Step1X-Edit précis et lisez sa fiche de modèle actuelle ainsi que l'exemple amont correspondant.
2. Construisez l'environnement à partir de la branche de dépendances documentée correspondante ; consignez le commit du dépôt et les versions des paquets.
3. Commencez par une image de petite taille, dont les droits sont purgés, et une instruction d'édition explicite. Conservez l'entrée non modifiée.
4. Conservez l'empreinte du point de contrôle, la classe du pipeline, le prompt, la graine lorsqu'elle est disponible, les empreintes d'entrée et de sortie, ainsi que tout module optionnel activé.
5. Testez un jeu de données de validation réservé, couvrant à la fois la modification demandée et les éléments qui doivent rester inchangés.

Lors d'un fine-tuning ou du chargement d'une LoRA, rattachez-la strictement à la version de base exacte, aux modules cibles et au chemin de chargement utilisés pour la produire. Un chargement réussi du fichier ne prouve ni la compatibilité sémantique ni la qualité de préservation.

## Évaluer l'édition, et non une affirmation de démonstration {#evaluate-editing-not-a-demo-claim}

Utilisez des critères d'acceptation distincts :

| Question | Preuve |
|---|---|
| L'édition demandée a-t-elle eu lieu ? | revue visuelle spécifique à la tâche, par rapport à l'instruction |
| Le contenu protégé est-il resté intact ? | comparaison côte à côte des visages, du texte, des logos, de la géométrie et des détails produit |
| Le résultat est-il reproductible ? | environnement figé, révision du modèle, prompt, graine et reçu d'entrée/sortie |
| Un benchmark s'applique-t-il ? | le protocole GEdit-Bench déclaré, et non un score reporté sur une autre tâche |

Pour les travaux qui exigent une fidélité à la source, comme l'identité produit, les documents, les preuves ou les mesures, une image éditée est un artefact dérivé. Conservez l'original comme référence faisant autorité.

## Conditions et limite de déploiement {#terms-and-deployment-boundary}

La licence du dépôt, la licence du point de contrôle, les conditions du service hébergé, les dépendances de base, les données d'entraînement et les droits sur les images d'entrée peuvent différer. Confirmez les conditions en vigueur pour chaque artefact effectivement utilisé avant tout déploiement commercial ou hébergé ; aucune étiquette au niveau de la famille ne remplace cette vérification.

## Références {#references}

- [Dépôt officiel de Step1X-Edit](https://github.com/stepfun-ai/Step1X-Edit)
- [Rapport technique de Step1X-Edit](https://arxiv.org/abs/2504.17761)
- [Collection de modèles Step1X-Edit](https://huggingface.co/stepfun-ai/Step1X-Edit)
