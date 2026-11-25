---
title: "LoRA d'édition de visage : corrections locales appariées"
description: "Un LoRA d'édition de visage est une tâche d'entraînement d'édition locale appariée et sensible au consentement ; liez l'adaptateur à son modèle de base exact et validez la correction demandée séparément de la préservation de l'identité."
category: workflows
tags: [lora, image-editing, paired-data, face, consent, evaluation, privacy]
aliases: ["Face Beautify Edit LoRA", "Face Correction LoRA"]
level: 2
source_sha256: b0117e88e78687687f078de6f633bbe0aab2485c1006a0a9c5701c7342b4d8fb
translation: machine
translated_at: '2026-10-24'
---
# LoRA d'édition de visage : corrections locales appariées {#face-edit-lora-paired-local-corrections}

Un adaptateur d'édition de visage doit apprendre une correction demandée et bornée, et non une définition globale de la « beauté ». Définissez l'édition en termes opérationnels (par exemple, rouvrir un œil fermé tout en préservant la pose, l'éclairage et l'identité) et précisez ce que l'adaptateur ne doit pas modifier.

## Contrat de données appariées {#paired-data-contract}

Chaque enregistrement d'entraînement nécessite une image source, une image cible, une instruction d'édition et un enregistrement de provenance, tous auditables. La source et la cible ne doivent différer que par la correction approuvée, dans la mesure du possible. Conservez :

- le consentement ou un droit documenté d'entraîner et de dériver la paire ;
- les empreintes (digests) de la source et de la cible, la provenance de capture ou de génération, et l'historique des éditions ;
- la modification locale prévue ainsi que les régions ou traits à « préserver impérativement » ;
- les motifs d'exclusion des exemples ambigus, sur-édités ou de qualité insuffisante ; et
- la politique de conservation et d'accès aux données pour les contenus sensibles au regard de la biométrie.

Les dégradations synthétiques ne peuvent enrichir un jeu de données que si leur générateur, leurs instructions et leur revue d'acceptation sont consignés. Elles ne remplacent pas des exemples appariés représentatifs et ne doivent introduire aucune modification cachée de l'identité ou du style dans la cible.

## Lier l'adaptateur à un contrat de modèle unique {#bind-the-adapter-to-one-model-contract}

Un adaptateur n'est pas portable du seul fait que deux outils le désignent comme un LoRA. Conservez avec l'artefact le point de contrôle ou la révision exacts du modèle de base, le pipeline, les encodeurs de texte, le VAE, le format de l'adaptateur, les modules cibles, le chemin de résolution et de recadrage, l'optimiseur et la configuration d'entraînement.

[ai-toolkit](https://github.com/ostris/ai-toolkit) fournit des exemples de configuration de fine-tuning maintenus. Partez de l'exemple actuel pour le modèle de base choisi, n'apportez que les modifications minimales documentées, et enregistrez la configuration exacte à côté de l'adaptateur produit. Un exemple de l'outil établit une voie d'exécution ; il ne prouve pas un résultat générique d'édition faciale pour un autre modèle ou un autre jeu de données.

## Découper et valider correctement {#split-and-validate-correctly}

Découpez les données par personne, par source ou par session de capture, avant toute augmentation. Des découpages aléatoires au niveau des images peuvent introduire des portraits quasi identiques dans la validation et faire paraître un adaptateur meilleur qu'il ne l'est.

Évaluez une suite d'édition figée comprenant :

1. des corrections locales demandées selon la pose, l'éclairage, la présentation de l'âge, le maquillage et les conditions de qualité d'image ;
2. des fixtures négatives où la région demandée doit rester inchangée ;
3. des contrôles de préservation de l'identité, de la pose, de l'éclairage et de l'arrière-plan ; et
4. des fixtures d'échec qui doivent être rejetées plutôt que modifiées de façon agressive.

Présentez le score de correction demandée séparément des résultats de préservation et de revue humaine. Une édition esthétiquement réussie ne prouve pas à elle seule la préservation de l'identité ni l'aptitude à un usage en production.

## Barrière de mise en production {#release-gate}

Avant toute utilisation hors expérimentation, publiez une fiche d'adaptateur contenant la liaison au modèle, le périmètre des données et des droits, le vocabulaire d'édition autorisé, les cas d'échec connus, les fixtures de validation et une procédure de retour arrière. Relancez la suite à chaque changement du modèle de base, du runtime, du chargeur d'adaptateur ou du périmètre d'édition demandé.

## Pages associées {#related-pages}

- [[lora-fine-tuning-for-editing-models]]
- [[diffusion-lora-training]]
- [[face-detection-filtering-pipeline]]
- [[anatomy-correction-diffusion]]
