---
title: "MACRO : données d'images multi-références structurées"
description: "MACRO est un jeu de données structuré multi-références, un benchmark et un ensemble de ressources de fine-tuning spécifiques à des modèles ; validez le modèle de base compatible et les conditions d'utilisation des artefacts avant tout déploiement."
category: models
tags: [multi-reference, dataset, benchmark, fine-tuning, bagel, omnigen2, qwen-image-edit]
aliases: ["MACRO-400K", "MacroData", "MacroBench"]
level: 2
source_sha256: 365e6eba5a7196a54c3f78e12a0b5b90f785e06c664b113509069d2be325e862
translation: machine
translated_at: '2026-10-24'
---
# MACRO : données d'images multi-références structurées {#macro-structured-multi-reference-image-data}

**Périmètre vérifié : 2026-09-04.** MACRO est une publication de recherche sur la génération d'images à partir de multiples références, et non une nouvelle architecture d'inférence universelle. Les auteurs publient des données structurées, un benchmark, des supports d'entraînement et des points de contrôle pour certains modèles ouverts sélectionnés, afin qu'un système apprenne à exploiter plus d'une image de référence sans reposer uniquement sur des exemples d'entraînement à contexte court.

## Ce qui est publié {#what-is-released}

Le projet décrit une publication de données de `400K` échantillons, comportant jusqu'à dix images de référence par échantillon. Les exemples sont organisés selon quatre familles de tâches complémentaires :

| Famille de tâches | Ce que les références sont censées fournir |
|---|---|
| Personnalisation | sujets, identité, objets ou attributs visuels |
| Illustration | contexte multimodal pour une composition demandée |
| Spatial | point de vue, géométrie ou relations de scène |
| Temporel | état visuel à travers le temps |

`MacroBench` évalue ces scénarios, et le dépôt fournit des chemins spécifiques à chaque modèle pour Bagel, OmniGen2 et Qwen-Image-Edit. Les données et le benchmark constituent un substrat d'évaluation utile ; ils n'établissent pas qu'un modèle arbitraire accepte dix images ni qu'il conservera fidèlement chaque référence.

## Choisir une voie compatible {#choose-a-compatible-route}

Utilisez exactement la voie maintenue par le projet :

1. choisissez un modèle de base pris en charge et sa révision documentée ;
2. suivez le prétraitement, le budget de résolution, la syntaxe des prompts et le chargement de points de contrôle propres à ce modèle ;
3. utilisez le point de contrôle MACRO ou la configuration d'entraînement correspondante, sans mélanger les formats d'adaptateurs ;
4. conservez une exécution de référence avec le modèle de base non modifié pour le même jeu de tâches.

Le nombre de références modifie le budget de tokens d'image. L'implémentation de MACRO réduit dynamiquement la résolution des images d'entrée à mesure que davantage de références sont fournies. N'appliquez pas un budget de pixels fixe issu d'un ancien tutoriel à un autre modèle de base ; inspectez la configuration actuelle et mesurez si les détails critiques survivent au redimensionnement.

## Évaluer la tâche réelle {#evaluate-the-real-task}

La génération à partir de multiples références présente plusieurs modes de défaillance indépendants : mélange de sujets, perte de petits détails, relations incorrectes, copie sélective et sortie plausible mais infidèle. Construisez une fixture d'acceptation qui précise quelle référence contrôle quel attribut du résultat, puis inspectez la sortie au regard de cette correspondance.

MacroBench s'appuie sur un flux de notation fondé sur un LLM. Il peut constituer un signal de recherche reproductible, mais il ne remplace ni une revue humaine, ni les vérifications de droits, ni les validateurs propres à la tâche dans un flux de production. Conservez les prompts, l'ordre des entrées, la révision du modèle, la graine aléatoire le cas échéant, ainsi que les artefacts générés, pour chaque comparaison.

## Données, droits et conditions de publication {#data-rights-and-release-terms}

Le projet documente un pipeline de construction des données et fournit des artefacts publiés, mais la provenance et les conditions de chaque entrée, de chaque modèle de base, de chaque point de contrôle et de chaque sortie en aval restent des questions distinctes. En particulier :

- lisez la licence et la fiche modèle du modèle de base choisi ainsi que de l'artefact MACRO ;
- vérifiez si le déploiement envisagé et la redistribution sont autorisés ;
- n'utilisez que des images de référence que l'opérateur est autorisé à traiter ;
- ne déduisez pas une autorisation commerciale pour chaque composant de la simple disponibilité du dépôt.

## Références {#references}

- [Dépôt officiel de MACRO](https://github.com/HKU-MMLab/Macro)
- [Article MACRO](https://arxiv.org/abs/2603.25319)
- [Page projet MACRO](https://macro400k.github.io/)
