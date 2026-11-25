---
title: "Correspondance de distributions en temps continu : contrat de distillation de recherche"
description: "La Correspondance de distributions en temps continu (CDM) est une méthode de recherche pour la distillation de diffusion en peu d'étapes, et non un simple interrupteur de vitesse à intégrer tel quel. Avant toute utilisation, associez l'article, le code et le checkpoint à leur licence, définissez la paramétrisation et le calendrier du professeur et de l'élève, le runtime d'entraînement et distribué, une évaluation qualité, diversité et préservation sur un jeu source-disjoint, ainsi que des preuves de service permettant un retour arrière."
category: optimization
tags: [cdm, diffusion-distillation, flow-matching, evaluation, serving, reproducibility]
aliases: ["CDM Diffusion Distillation", "Continuous-Time Distribution Matching Distillation"]
level: 2
source_sha256: 0fbde824bce9af395fb604845fb2b5070644a823afa67a41558afa63c5b0d5a6
translation: machine
translated_at: '2026-10-24'
---
# Correspondance de distributions en temps continu : contrat de distillation de recherche {#continuous-time-distribution-matching-research-distillation-contract}

[Correspondance de distributions en temps continu](https://arxiv.org/abs/2605.06376)
est une méthode de recherche pour la distillation de diffusion en peu d'étapes. L'article décrit la correspondance de distributions en temps continu
pour les architectures expérimentales nommées et renvoie vers le code. Il s'agit d'une base pour reproduire ou étendre
cette version publiée dans ses conditions, et non d'une promesse clé en main concernant un nombre d'étapes précis, un gain de vitesse, un niveau de qualité, une topologie de GPU ou une compatibilité avec un autre professeur.

## Lier professeur, élève et trajectoire {#bind-teacher-student-and-trajectory}

Pour chaque expérience, conservez :

- la version de l'article, le commit du code, les identifiants et empreintes (digests) des checkpoints et artefacts, les conditions de licence et d'accès, les révisions du framework et des dépendances, ainsi que le relevé du runtime distribué et du matériel ;
- la paramétrisation du professeur et de l'élève, le chemin de conditionnement, la cible de prédiction, le calendrier de bruit et de trajectoire, les branches et pondérations de la perte, le pipeline de données, les graines aléatoires et la politique de checkpoint et de reprise ;
- un jeu d'évaluation source-disjoint, avec les mesures de qualité de la tâche, de diversité, de préservation des éléments non ciblés, de sécurité et droits, de reproductibilité et d'échecs ;
- des exécutions de référence comparables, utilisant la même distribution de prompts ou d'entrées, la même résolution de sortie, le même environnement d'inférence, la latence à chaud et en régime établi, le débit, la mémoire et la politique d'erreurs ; et
- la version et l'artefact de service, la cible de retour arrière, la provenance des sorties, la supervision et la décision de mise en production.

Modifier le professeur, l'architecture de base, le planificateur (scheduler), le contrat de conditionnement ou l'implémentation distribuée change le problème de distillation. N'héritez pas d'une interface d'adaptateur, d'un calendrier, d'une branche de perte ou d'un résultat publié provenant d'une autre famille de modèles sans implémentation explicite et validation mesurée.

## Évaluer l'accélération séparément de la fiabilité des sorties {#evaluate-acceleration-separately-from-output-trust}

Les sorties en peu d'étapes doivent être comparées au professeur et à la référence déclarés pour la tâche demandée. Présentez la vitesse et le coût séparément de la fidélité, de la diversité, de la préservation du texte et de la géométrie, et du taux d'artefacts. Un échantillon visuellement attrayant ne prouve pas qu'un élève préserve les faits de la source, se comporte de manière cohérente sur une nouvelle distribution de prompts, ni qu'il peut être mis en service en toute sécurité.

Conservez les checkpoints et la traçabilité des sorties en quantité suffisante pour rejouer une évaluation en échec ou revenir à un élève déployé. Un entraînement interrompu prématurément, dont la provenance est perdue ou dont l'évaluation ne peut pas être reproduite, reste incomplet.

## Limite en cas d'échec {#failure-boundary}

Si le contrat professeur/élève, le code ou les artefacts, la licence, l'évaluation source-disjoint ou le chemin de retour arrière font défaut, maintenez la CDM à l'état de recherche. Ne remplacez pas la méthode par une autre méthode de distillation, ne publiez pas un checkpoint non mesuré et ne présentez pas un échantillonneur plus rapide comme un résultat CDM équivalent.

## Pages associées {#related-pages}

- [[flow-matching]]
- [[diffusion-inference-acceleration]]
- [[MMDiT]]
- [[diffusion-lora-training]]
