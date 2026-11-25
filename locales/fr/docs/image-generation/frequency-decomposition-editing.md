---
title: "Édition par décomposition fréquentielle : contrat de transformation et de fidélité"
description: "La décomposition fréquentielle est une transformation déclarée, et non une carte d'édition sémantique ; consignez l'espace colorimétrique, la transformation ou le filtre, la politique de bord et de reconstruction, les masques d'édition et la revue de sortie, et distinguez le signal reconstruit mathématiquement des détails générés ou visuellement plausibles."
category: techniques
tags: [frequency, wavelets, laplacian, filtering, reconstruction, retouching, fidelity]
aliases: ["Frequency Separation", "Low and High Frequency Editing"]
level: 2
source_sha256: aab36b6efbc9e636fea850a26a2c89d4e9e3fd211fb0cb90a7349b3cfe425abf
translation: machine
translated_at: '2026-10-24'
---
# Édition par décomposition fréquentielle : contrat de transformation et de fidélité {#frequency-decomposition-editing-transform-and-fidelity-contract}

Les étiquettes de basses et de hautes fréquences décrivent la réponse d'une
transformée ou d'un filtre choisi. Elles n'identifient pas automatiquement
une région sémantique comme « peau », « détail », « éclairage » ou toute autre
zone. Un flux de travail fréquentiel n'est fiable que si son espace colorimétrique,
sa transformation, son comportement aux bords, ses modifications, sa reconstruction
et sa revue sont tous déclarés.

## Déclarer le contrat du signal {#declare-the-signal-contract}

Pour chaque tâche, consignez :

- l'empreinte de la source, les dimensions, l'orientation, la politique alpha/masque,
  l'encodage colorimétrique, et si les opérations sont effectuées sur des valeurs
  linéaires ou référencées à l'affichage ;
- la famille de transformation ou de filtre, son implémentation et sa version,
  l'échelle, le niveau ou le rayon, les canaux, le dtype et la normalisation ;
- le mode de remplissage ou d'extension des bords, la politique de recadrage et
  d'alignement, et la routine de reconstruction ;
- les régions éditables et protégées, ainsi que toute composante générée ; et
- la transformation de sortie, le comportement d'écrêtage ou de gamut, la vérification
  numérique de la reconstruction et le justificatif de revue visuelle.

Modifier un rayon de flou, une ondelette, un mode de remplissage, un encodage
colorimétrique ou un recadrage change les bandes. Ne réutilisez pas un rayon
numérique ou une étiquette de bande de fréquence issu d'une autre résolution, d'un
autre objectif, d'un autre domaine d'image ou d'une autre transformation, comme s'il
désignait le même contenu.

## Choisir une transformation selon la propriété visée {#choose-a-transform-for-the-stated-property}

Les pyramides gaussiennes et laplaciennes, les ondelettes décimées, les ondelettes
stationnaires, les filtres guidés et les modules fréquentiels appris présentent des
comportements différents en matière de redondance, d'alignement, de bords et de
reconstruction. Sélectionnez une méthode parce que sa propriété documentée
soutient la tâche, puis validez-la sur des images représentatives.

La [documentation PyWavelets sur la transformée en ondelettes stationnaire](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html)
décrit la SWT comme une modification invariante par translation et non décimée de la
DWT ; elle précise également la redondance et les contraintes de taille du signal. La
[documentation sur les modes d'extension du signal](https://pywavelets.readthedocs.io/en/latest/ref/signal-extension-modes.html)
montre pourquoi le mode de bord doit figurer dans le contrat. Ni l'une ni l'autre
n'établit qu'une famille d'ondelettes donnée est exempte d'artefacts, ou préférable
pour toutes les tâches de retouche.

## Conserver les preuves de reconstruction {#preserve-reconstruction-evidence}

Pour une transformation linéaire couplée à son inverse exacte et à des coefficients
inchangés, calculez et conservez un résidu numérique d'aller-retour sous le dtype et
la politique de bord déclarés. Dès que les coefficients sont modifiés, écrêtés,
masqués, mélangés à une autre image ou traités par un modèle non linéaire ou génératif,
le résultat est une image dérivée et nécessite une revue de fidélité distincte.

Inspectez les coutures, les halos, les anneaux, l'intensité des textures, les
gradients, les décalages colorimétriques, le texte, la géométrie des produits, les
visages et les régions protégées à la résolution de livraison. Si des hautes fréquences
sont synthétisées après une modification basse fréquence, étiquetez-les comme détails
générés ; ne les présentez pas comme une texture source récupérée.

## Frontière d'édition et de publication {#editing-and-release-boundary}

Utilisez des masques et une intention de modification explicite, plutôt que de traiter
une bande de fréquence comme une autorisation de modifier chaque pixel de cette bande.
Un résultat visuellement lisse peut néanmoins supprimer des marques factuelles ou altérer
le détail d'un matériau, de la peau ou d'un produit. Comparez au source et à une
référence de tâche approuvée, et conservez le justificatif de transformation avec la sortie.

Si la transformation ne peut pas reconstruire dans la tolérance déclarée, si la politique
de bord est ambiguë, ou si la revue visuelle révèle une modification de détail protégé,
renvoyez un état d'échec ou de revue explicite et visible. Ne réinjectez pas silencieusement
une autre bande, n'appliquez pas un nouveau modèle de renforcement de netteté, et ne
prétendez pas à une reconstruction exacte.

## Pages connexes {#related-pages}

- [[color-space-and-gamma-reference]]
- [[tiled-inference]]
- [[paired-training-for-restoration]]
- [[skin-retouch-pipeline]]
