---
title: "SpatialEdit-16B : contrat de géométrie et d'évaluation"
description: "SpatialEdit-16B est une version de recherche pour l'édition d'images pilotée par la géométrie ; lier l'artefact exact du code/modèle et ses conditions, l'autorité sur les assets source et cible, le contrat de transformation objet/caméra et de coordonnées, le prétraitement/l'exécution, l'évaluation géométrique et de préservation, et la revue humaine avant utilisation."
category: techniques
tags: [spatialedit, image-editing, geometry, camera-control, provenance, evaluation]
aliases: ["SpatialEdit-16B Geometric Control", "SpatialEdit Geometry Editing"]
level: 2
source_sha256: 5b010a5ade22bcc16253039f2182b7301a2f6f7f0a0b502ff490383a168b7331
translation: machine
translated_at: '2026-10-24'
---
# SpatialEdit-16B : contrat de géométrie et d'évaluation {#spatialedit-16b-geometry-and-evaluation-contract}

L'[article SpatialEdit](https://arxiv.org/abs/2604.04911) présente un benchmark d'édition d'images piloté par la géométrie, une supervision synthétique et un modèle de référence SpatialEdit-16B pour les modifications centrées sur l'objet et sur la caméra. La [version officielle](https://github.com/EasonXiao-888/SpatialEdit) publie le code, les points de contrôle (checkpoints), les assets du benchmark et des prérequis externes distincts. Cela permet d'évaluer la version nommée ; cela ne constitue pas une preuve, à partir d'une image plausible, que la géométrie demandée a bien été respectée.

## Lier la version et le contrat d'édition {#bind-the-release-and-edit-contract}

Pour chaque édition évaluée ou publiée, conserver :

- la révision du dépôt, l'identifiant et le digest du modèle/checkpoint, les conditions du code et des artefacts, l'enregistrement des dépendances et de l'environnement d'exécution, ainsi que chaque prérequis externe utilisé par la configuration retenue ;
- le digest de l'image source, l'enregistrement de propriété ou d'autorisation d'édition, la définition du sujet/objet, les régions protégées et tout changement sémantique interdit ;
- la classe de tâche : translation d'objet, mise à l'échelle, rotation canonique, ou changement de point de vue/cadrage de la caméra ; les systèmes de coordonnées source et cible ; la boîte cible, la pose, le recadrage, la résolution et la convention d'orientation ;
- le prétraitement des entrées, les chemins du VAE/du modèle, la seed, le scheduler et ses paramètres, le digest de la sortie, et la correspondance entre les pixels de sortie et le repère source ; et
- le résultat fidélité géométrique, le résultat de préservation des zones non cibles, les exemples d'échec, la décision du relecteur et la conclusion sur l'usage autorisé.

La disponibilité du code ou une licence permissive du dépôt ne établit pas les conditions applicables à chaque checkpoint, modèle de base, jeu de données ou image source. Conserver séparément chaque enregistrement d'autorité.

## Évaluer séparément la géométrie et la préservation {#evaluate-geometry-and-preservation-separately}

Utiliser des assets tenus à l'écart, disjoints de la source, couvrant les classes de sujets requises, les occlusions, les reflets, les contours fins, la complexité du fond et les transformations caméra/objet visées. Évaluer la transformation demandée dans le système de coordonnées déclaré, puis inspecter de manière indépendante l'identité de l'objet, la continuité du fond, la cohérence de l'éclairage et des ombres, le texte, les logos et les détails factuels du produit.

Ne pas agréger un score de préférence visuelle avec la correctitude géométrique. Un résultat peut paraître cohérent alors que la localisation, l'échelle, l'orientation ou le changement de point de vue de l'objet sont faux. Comparer à une référence déclarée et conserver aussi bien les cas réussis que les cas échoués, plutôt que de ne retenir que les sorties attrayantes.

## Pièges {#gotchas}

- **Problème :** un prompt peut produire une scène sémantiquement plausible au résultat spatial erroné → **Correctif :** valider la boîte, la pose, le cadrage ou la relation caméra demandés dans le système de coordonnées source déclaré.
- **Problème :** la version officielle contient des chemins de substitution ou internes ainsi que des prérequis externes sous forme de checkpoints → **Correctif :** ne remplacer ces chemins que dans une configuration locale versionnée, et enregistrer chaque artefact résolu avant de considérer une exécution comme reproductible.
- **Problème :** on suppose qu'un résultat général d'édition se transfère à une nouvelle opération objet/caméra → **Correctif :** évaluer cette opération sur un jeu de test tenu à l'écart et propre à l'opération ; ne pas l'inférer depuis la famille du modèle.

## Limite d'échec {#failure-boundary}

Si l'autorité sur la source, la version et ses conditions exactes, la définition des coordonnées, l'enregistrement du prétraitement ou la revue géométrie-et-préservation font défaut, maintenir la sortie en état de revue. Ne pas substituer silencieusement un autre modèle, ne pas réinterpréter une édition purement sémantique comme un contrôle métrique, et ne pas la publier comme vue vérifiée ou reconstruction factuelle.

## Pages liées {#related-pages}

- [[MMDiT]]
- [[flow-matching]]
- [[tile-position-encoding]]
- [[diffusion-inference-acceleration]]
- [[flux-klein-capability-map]]
