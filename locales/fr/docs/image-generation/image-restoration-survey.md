---
title: "Restauration d'image : guide des tâches et de la fidélité"
description: "La restauration d'image doit déclarer la dégradation et la cible de fidélité ; choisir une méthode déterministe ou par diffusion compatible avec la tâche, puis valider séparément la récupération mesurée et les détails plausibles mais inventés."
category: techniques
tags: [image-restoration, denoising, deblurring, super-resolution, jpeg-artifacts, diffusion, fidelity, evaluation]
aliases: ["Image Restoration Survey", "Image Enhancement", "Denoising Survey"]
level: 3
source_sha256: 65f1bf83a00073b2f9eb0d334b0bb5d2d8dee8ed5dd5d781ac967be050fa4c94
translation: machine
translated_at: '2026-10-24'
---
# Restauration d'image : guide des tâches et de la fidélité {#image-restoration-task-and-fidelity-guide}

La restauration d'image nécessite une dégradation déclarée et une cible de
fidélité déclarée. « Ça paraît mieux » ne suffit pas pour des contenus de
produit, documentaires, scientifiques ou judiciaires : une méthode générative
peut produire des détails plausibles qui ne sont pas étayés par l'image
observée.

## Commencer par le contrat de restauration {#start-with-the-restoration-contract}

Définir :

- le type de dégradation et l'historique d'acquisition connu, comme le bruit,
  le flou, la compression, une zone manquante, un faible éclairage ou une
  résolution limitée ;
- le comportement attendu en sortie : récupération fidèle aux mesures,
  nettoyage perceptuel ou reconstruction créative clairement étiquetée ;
- la cible de référence disponible ou une méthode de validation propre à la
  source ;
- les contenus protégés, comme le texte, les visages, la géométrie des
  produits, les couleurs et les marquages ; et
- les limites d'utilisation autorisées pour le modèle, les données et la
  licence.

Ne pas regrouper plusieurs classes de dégradation sous une seule action
générique « améliorer », sauf si le modèle a été entraîné et validé pour ce
contrat combiné.

## Familles de méthodes {#method-families}

### Modèles déterministes spécifiques à une tâche {#task-specific-deterministic-models}

Les approches CNN et transformeur spécifiques à une tâche restent appropriées
lorsque la dégradation est connue et que la récupération fidèle au pixel
importe. Parmi les exemples figurent
[SwinIR](https://github.com/JingyunLiang/SwinIR),
[NAFNet](https://github.com/megvii-research/NAFNet) et
[Restormer](https://arxiv.org/abs/2111.09881). Leurs résultats publiés
s'appliquent à des tâches, des jeux de données et des points de contrôle
particuliers ; il faut choisir une version compatible plutôt que de les
considérer comme un modèle de restauration universel.

### Diffusion conditionnelle pour la restauration {#conditional-diffusion-restoration}

[Palette](https://research.google/pubs/palette-image-to-image-diffusion-models/)
illustre la diffusion conditionnelle sur des tâches image-à-image, notamment
la colorisation, l'inpainting, le recadrage vers l'extérieur (uncropping) et
la restauration JPEG. Les méthodes par diffusion peuvent modéliser une
distribution de sorties plus large, mais cette flexibilité fait des détails
non étayés un risque central pour l'acceptation.

[IR-SDE](https://arxiv.org/abs/2301.11699) est une autre formulation de
recherche qui utilise une équation différentielle stochastique à retour à la
moyenne pour la restauration. Elle n'établit ni un calendrier par défaut ni
une configuration de production pour un autre point de contrôle.

### Workflows d'édition et modèles de fondation {#editing-and-foundation-model-workflows}

Les systèmes généralistes d'édition d'image peuvent être utiles pour une
réparation bornée, contrôlée par masque et instruction. Ils nécessitent une
évaluation de la préservation de la source et doivent rester distincts des
méthodes de débruitage ou de super-résolution orientées métriques. Voir
[[RealRestorer]] pour un workflow propre à une version donnée, plutôt qu'un
classement de l'ensemble des outils de restauration.

## Évaluation permettant de détecter les inventions {#evaluation-that-catches-invention}

Utiliser un jeu de validation avec des cibles connues lorsque c'est possible,
et présenter la métrique dans son contexte de tâche. Ajouter une revue visuelle
pour :

- le texte, la géométrie, les textures ou les petits détails hallucinés ;
- la dérive de couleur et de tonalité, en particulier après compression ou
  correction en faible lumière ;
- les coutures et discontinuités au niveau des masques, recadrages ou tuiles ;
- la préservation des éléments de produit, de document ou de preuve médicale
  ou scientifique ; et
- le comportement sur des entrées dégradées situées hors de la distribution
  d'entraînement.

Distinguer un résultat métrique d'une décision de publication. Une métrique de
reconstruction élevée ne prouve pas automatiquement la préservation factuelle,
et une sortie de diffusion visuellement attrayante peut être inacceptable
lorsque les pixels constituent une preuve.

## Dossier de publication {#release-record}

Conserver l'empreinte de l'entrée, le diagnostic de dégradation, le modèle et
son point de contrôle, les paramètres, la cible de référence ou l'élément de
validation, la sortie, le résultat d'acceptation, ainsi qu'une étiquette
explicite pour toute reconstruction créative. Relancer la validation après
tout changement de modèle, d'environnement d'exécution ou de domaine d'entrée.

## Pages connexes {#related-pages}

- [[RealRestorer]]
- [[color-checker-and-white-balance]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
