---
title: "Pertes auxiliaires LoRA : contrat d'expérimentation et d'évaluation"
description: "Les pertes auxiliaires LoRA sont des objectifs propres à chaque expérimentation, et non une recette portable ; liez le modèle de base, le format d'adaptateur, les droits sur les données, l'implémentation de la perte, la plage de recherche des pondérations, la séparation de validation et l'évaluation de la tâche et de la préservation, et traitez les pertes d'identité ou de masque comme des contrôles sensibles plutôt que comme une preuve de ressemblance."
category: techniques
tags: [lora, training, loss, evaluation, adapters, identity, masks, evidence]
aliases: ["Auxiliary Training Losses", "LoRA Loss Functions"]
level: 3
source_sha256: b2c7f04dcf2cc5acde9e26463b4f3f948777e6339089c0e8aee933fff09c1d9c
translation: machine
translated_at: '2026-10-24'
---
# Pertes auxiliaires LoRA : contrat d'expérimentation et d'évaluation {#lora-auxiliary-losses-experiment-and-evaluation-contract}

Une perte auxiliaire modifie un objectif d'entraînement. Elle ne rend pas un adaptateur portable, ne prouve pas la préservation de l'identité et n'établit pas qu'un résultat visuel est fidèle. Son effet dépend du modèle de base, des modules cibles, des données, de l'optimiseur et du planning, de l'implémentation à l'exécution et de l'évaluation sur données held-out.

## Lier une expérimentation de façon complète {#bind-one-experiment-completely}

Conservez un enregistrement d'expérimentation versionné contenant :

- le manifeste des données autorisées, la finalité prévue, les exclusions, les conditions de consentement et de suppression lorsque des personnes sont représentées, ainsi qu'un découpage train/validation disjoint au niveau des sources ;
- l'empreinte (digest) du checkpoint de base et sa licence, les versions de l'architecture et du runtime, le format de l'adaptateur, les modules cibles, les composants entraînables et les détails de sérialisation ;
- pour chaque terme de perte, son implémentation source, sa réduction, le prétraitement du masque ou des caractéristiques, le domaine numérique, la plage de pondération ou de recherche, et la graine aléatoire ;
- l'objectif de référence et une hypothèse déclarée pour l'ajout du terme ;
- une métrique de tâche held-out et une métrique indépendante de préservation, avec des exemples choisis avant d'observer le résultat ; et
- les artefacts nécessaires pour reproduire ou rejeter l'exécution, y compris les échecs.

La documentation des checkpoints de [PEFT](https://huggingface.co/docs/peft/developer_guides/checkpoint) montre qu'une représentation d'adaptateur nécessite à la fois ses poids et sa configuration. Il s'agit de métadonnées nécessaires, et non d'une garantie qu'un adaptateur de diffusion se charge ou se comporte correctement dans une autre famille de modèles, un autre entraîneur ou un autre service d'inférence.

## Choisir une perte selon la défaillance mesurée {#select-a-loss-by-the-measured-failure}

Les catégories courantes comprennent :

- un objectif de tâche ou de reconstruction pour la tâche de génération ou d'édition déclarée ;
- une pondération par région fondée sur des masques revus, lorsque seule une région autorisée doit influencer l'objectif ;
- un terme de régularisation ou de prior destiné à limiter une forme mesurée de dérive ;
- une comparaison de caractéristiques ou perceptuelle dont l'encodeur, le prétraitement et les modes de défaillance sont déclarés ; et
- une comparaison sensible à l'identité, utilisée uniquement sous une autorité explicite et jamais comme authentification, preuve d'identité ou autorisation d'usurper une identité.

Les encodeurs de masques et de caractéristiques peuvent introduire leurs propres biais. Un masque doit être aligné sur sa source à travers toute transformation spatiale et ne doit pas élargir silencieusement la région d'édition autorisée. Un score de similarité des caractéristiques peut manquer des défaillances de préservation liées à la pose, à l'âge, à l'éclairage, à la démographie ou aux éléments autres que le visage. Inspectez les images sous-jacentes en plus de la valeur scalaire de la perte.

## Ajuster sans copier une recette {#tune-without-copying-a-recipe}

Partez d'une référence reproductible. Modifiez une seule hypothèse de perte à la fois, ne recherchez que dans la plage déclarée, et choisissez le résultat à partir de preuves held-out, et non de la perte d'entraînement ou d'une invite choisie à la main. Si le terme auxiliaire améliore la propriété visée mais dégrade la préservation, les droits, la compatibilité ou la reproductibilité, il n'est pas un candidat à la publication.

La [présentation de l'entraînement de Diffusers](https://huggingface.co/docs/diffusers/training/overview) décrit explicitement ses scripts comme des exemples spécifiques à une tâche qui nécessitent une adaptation. Un rang, un taux d'apprentissage, un poids de perte, un nombre d'images de prior, une liste de blocs ou une force de curseur (slider) provenant d'une autre version constituent donc une entrée à tester, et non une valeur par défaut à publier.

## Frontière de l'identité sensible {#sensitive-identity-boundary}

Pour un adaptateur propre à une personne, consignez l'autorisation, la finalité permise, la gestion de la révocation et de la suppression, la frontière du modèle de base et du fournisseur, ainsi qu'une revue humaine de la ressemblance et de la préservation, disjointe au niveau des sources. N'exportez pas un score d'identité comme une affirmation d'identité. N'utilisez pas un terme auxiliaire d'identité pour déduire des traits sensibles ni pour transformer une personne qui n'a pas consenti.

## Frontière des échecs et de la publication {#failure-and-release-boundary}

Signalez explicitement l'échec lorsqu'un adaptateur ne dispose pas d'une configuration ou de poids compatibles, lorsque les masques ne peuvent pas être rattachés aux images sources, lorsque le découpage held-out présente une fuite, lorsqu'une métrique manque, ou lorsque l'évaluation détecte une modification du contenu protégé. Ne supprimez pas silencieusement une perte, ne remplacez pas le backend, ne fusionnez pas un adaptateur incompatible, et ne présentez pas un échantillon visuellement plausible comme une preuve de préservation.

## Pages associées {#related-pages}

- [[diffusion-lora-training]]
- [[flux-klein-character-lora]]
- [[lora-fine-tuning-for-editing-models]]
- [[paired-training-for-restoration]]
