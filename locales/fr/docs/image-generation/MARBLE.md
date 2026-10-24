---
title: "MARBLE : recomposition et mélange de matériaux"
description: "MARBLE réalise le transfert de matériaux, le mélange et des modifications paramétriques de matériaux via des contrôles dans l'espace CLIP sur un générateur d'images pré-entraîné ; valider la géométrie de l'objet, l'éclairage et les licences des artefacts pour chaque flux de travail."
category: models
tags: [material-editing, clip-space, stability-ai, sdxl, ip-adapter, roughness, metallic, transparency, pbr]
aliases: ["Material Recomposition and Blending"]
level: 2
source_sha256: 9179341c0916291d9b98aa02639cc0df4ea2fbd27c7db7cd068f1ef724d22d17
translation: machine
translated_at: '2026-10-24'
---
# MARBLE : recomposition et mélange de matériaux {#marble-material-recomposition-and-blending}

**Périmètre vérifié : 2026-09-04.** MARBLE est la méthode d'édition de matériaux publiée par Stability AI. Elle dérive des représentations de matériaux dans l'espace CLIP et les utilise pour guider un système pré-entraîné de génération d'images à partir de texte, pour trois opérations apparentées : transfert de matériau à partir d'un exemple, mélange entre plusieurs références de matériaux, et ajustement paramétrique d'attributs de matériau choisis.

## Ce que la méthode permet d'exprimer {#what-it-can-express}

L'article démontre un contrôle sur des propriétés telles que la rugosité, l'aspect métallique, la transparence et la luminescence. L'implémentation publique fournit :

- un notebook de mélange de matériaux ;
- un notebook de contrôle paramétrique ;
- une démo Gradio ;
- une extension ComfyUI et un exemple de workflow.

L'objectif de la méthode est l'édition visuelle de matériaux, et non un solveur PBR calibré physiquement. Un résultat qui paraît plus métallique ou plus transparent peut malgré tout présenter des reflets incohérents, une géométrie altérée ou un éclairage invraisemblable. Considérer la sortie comme un résultat de génération d'images qui nécessite une revue spécifique à la tâche.

## Architecture et frontière des dépendances {#architecture-and-dependency-boundary}

MARBLE construit ses blocs de matériaux à partir de la base de code InstantStyle et utilise un générateur d'images pré-entraîné ainsi que les artefacts de conditionnement par image associés. Conserver la chaîne complète de façon explicite :

1. révision du dépôt MARBLE et son verrouillage des dépendances ;
2. révisions du générateur de base, de l'encodeur d'images, de l'adaptateur et du point de contrôle retenus ;
3. image de l'objet source et référence(s) de matériau, avec l'autorisation de les traiter ;
4. type d'opération — transfert, mélange ou contrôle paramétrique — et chaque valeur de contrôle ;
5. sortie et reçu d'acceptation.

Ne pas supposer qu'un contrôle réglé pour un modèle de base, une catégorie d'objet ou un dispositif d'éclairage donné se transposera à un autre. La version de Python testée en amont et les paramètres des notebooks sont des éléments de compatibilité pour cette version, et non un contrat d'API stable.

## Critères d'acceptation pour les images de produits {#acceptance-checks-for-product-images}

Pour un usage produit ou bijouterie, vérifier séparément :

| Exigence | Contrôle |
|---|---|
| identité et silhouette de l'objet | superposition ou comparaison côte à côte avec l'original |
| aspect du matériau | inspecter les reflets, la rugosité, la transparence et le comportement des bords dans le recadrage prévu |
| couleur et exposition | comparer aux cibles source calibrées lorsqu'elles existent |
| périmètre de l'édition | confirmer que l'arrière-plan, le marquage et les zones non concernées n'ont pas changé |
| droits de publication | conserver l'autorisation pour la photo de l'objet et l'exemple de matériau |

Utiliser des workflows de rendu physiquement fondé ou de gestion de couleur mesurée lorsqu'un attribut de matériau doit être numériquement exact plutôt que visuellement plausible.

## Licences {#licensing}

MARBLE, InstantStyle, le générateur de base retenu, les adaptateurs et les éventuels assets d'exemple peuvent avoir des licences et des conditions d'accès différentes. Lire les conditions actuelles de chaque artefact avant toute utilisation hébergée, commerciale ou redistribuée ; la présence d'un dépôt public n'accorde pas de droit général sur l'ensemble du workflow assemblé.

## Références {#references}

- [Dépôt officiel de MARBLE](https://github.com/Stability-AI/marble)
- [Article MARBLE](https://arxiv.org/abs/2506.05313)
- [Page projet MARBLE](https://marblecontrol.github.io/)
