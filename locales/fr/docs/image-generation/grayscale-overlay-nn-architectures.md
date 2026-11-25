---
title: "Prédiction de superposition en niveaux de gris : contrat de retouche appariée"
description: "La prédiction de superposition en niveaux de gris est une tâche de retouche appariée et alignée au pixel ; préserver le contrat de mélange et la référence sans opération, associer chaque paire source/cible et chaque masque, et évaluer l'image composite ainsi que la carte avant de publier un ajustement automatisé."
category: reference
tags: [image-restoration, retouching, regression, paired-data, evaluation, provenance]
level: 3
source_sha256: 11f9c34050b3dfc4d2fb32bc63decf012b8b11eb3c7dc0cb9a90fe9c12c8ed37
translation: machine
translated_at: '2026-10-24'
---
# Prédiction de superposition en niveaux de gris : contrat de retouche appariée {#grayscale-overlay-prediction-paired-retouching-contract}

La prédiction de superposition en niveaux de gris estime une carte d'ajustement à canal unique pour une opération de composition déclarée. C'est une tâche de retouche appariée et alignée au pixel, et non un benchmark générique de restauration d'image. La carte n'a de sens que conjointement avec l'implémentation exacte du mélange, la gestion des couleurs, l'image d'entrée et le périmètre d'édition approuvé.

## Définir d'abord le contrat de mélange {#define-the-blend-contract-first}

Avant de choisir un réseau, rendre la cible reproductible :

- espace colorimétrique d'entrée, profondeur de bits, orientation et gestion de l'alpha ;
- plage de superposition et sa valeur neutre sans opération ;
- fonction de mélange et version de l'implémentation, y compris la gestion linéaire/gamma ;
- opacité, masques, zones protégées et comportement de saturation (clipping) ; et
- image source, carte cible, cible composite approuvée et dossier de droits/consentement.

Modifier l'un de ces éléments peut changer la carte attendue, même si la retouche visible semble similaire. Une carte cible privée de son contrat de composition n'est pas une donnée d'entraînement réutilisable.

## Les modèles candidats sont des hypothèses {#model-candidates-are-hypotheses}

[NAFNet](https://github.com/megvii-research/NAFNet) et
[Restormer](https://github.com/swz30/Restormer) sont des implémentations publiées de restauration d'image. Elles peuvent servir de candidates pour une référence de régression appariée, mais leurs architectures publiées ne permettent pas d'établir que l'une est la meilleure pour une carte de retouche à canal unique, qu'une modification particulière de la tête de sortie est compatible, ni qu'une recette fixe de fonction de perte ou de découpage en tuiles est sûre pour toute superposition.

Commencer par le plus petit modèle versionné capable de produire la disposition de canaux requise. Lier le code d'entraînement et d'inférence à :

1. une révision du point de contrôle ou du dépôt ;
2. la plage de sortie et la politique d'initialisation sans opération ;
3. le comportement en pleine résolution et par tuiles utilisé à la publication ; et
4. une référence qui émet la carte neutre.

Traiter les réécritures non prises en charge de la tête, les hooks personnalisés et le comportement de la normalisation par lots comme des expériences disposant de leurs propres preuves, et non comme des caractéristiques implicites de l'architecture.

## Construire des paires qui signifient la même chose {#build-pairs-that-mean-the-same-thing}

Chaque exemple doit associer la même géométrie de scène à l'ajustement cible :

- aucun recadrage, changement de perspective, alignement de visage ou opération de retouche ne doit dériver entre l'entrée et la cible ;
- les masques doivent distinguer les pixels éditables des pixels protégés ou inconnus ;
- séparer les ressources sources par photographe, sujet, séance et chaîne de dérivation avant le découpage entraînement/validation/test ; et
- conserver ensemble l'original, la carte, la cible composite, la justification de l'édition et la décision du relecteur.

Les augmentations ne sont valides que si elles préservent la relation image-carte et le contrat de mélange. Une transformation qui modifie l'éclairage, la composition ou la géométrie peut créer une paire d'apparence alignée mais dotée d'une cible invalide.

## Évaluer la carte et le résultat visible {#evaluate-the-map-and-the-visible-result}

Utiliser l'erreur de carte appariée seulement après avoir défini son échelle et sa région valide. Elle ne peut pas indiquer si l'ajustement paraît correct après composition. Examiner les deux surfaces :

| Surface | Vérification |
|---|---|
| Carte prédite | les régions neutres restent neutres, les gradients sont stables, les masques sont respectés et les contours ne fuient pas |
| Image composite | la correction voulue apparaît, les caractéristiques protégées restent inchangées, et aucun effet de bandes, de coutures, de saturation ou de dérive colorimétrique n'est introduit |
| Sources retenues | les performances tiennent sur de nouveaux sujets, éclairages, matériaux et recadrages |
| Exécution | la résolution, la mémoire, le comportement par tuiles et le chemin de repli/d'échec correspondent à l'environnement de publication |

Pour les visages ou les produits, un résultat visuellement lisse exige tout de même une vérification des éléments pertinents pour l'identité, des étiquettes, de la texture et des détails factuels. Le réseau propose un ajustement ; il n'autorise pas une retouche finale.

## Barrière de publication {#release-gate}

Publier une superposition automatisée seulement lorsqu'un relecteur peut reproduire l'entrée, le modèle, la carte, le contrat de mélange, la sortie composite et l'approbation. Si le modèle émet un changement non neutre en dehors du masque autorisé, ou si l'évaluation ne permet pas de distinguer une carte plausible d'un ajustement approuvé, le retenir pour correction manuelle.

## Sources et pages associées {#sources-and-related-pages}

- [Dépôt officiel de NAFNet](https://github.com/megvii-research/NAFNet)
- [Dépôt officiel de Restormer](https://github.com/swz30/Restormer)
- [[paired-training-for-restoration]]
- [[image-restoration-survey]]
- [[low-vram-inference-strategies]]
