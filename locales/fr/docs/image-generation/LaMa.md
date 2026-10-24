---
title: "LaMa : inpainting à grand masque robuste à la résolution"
description: "LaMa est un modèle d'inpainting à convolutions de Fourier pour les grands masques et la généralisation en résolution ; utilisez-le avec un checkpoint compatible et testez séparément la continuité des textures par rapport à la restauration sémantique d'objets."
category: models
tags: [inpainting, ffc, fourier, large-mask, samsung, feed-forward, resolution-robust]
aliases: ["Large Mask Inpainting", "Big-LaMa"]
level: 2
source_sha256: 98c7d5e462b0d8a64dda4074ead11d0088491fa16af4c75ec1284e2f77c411e3
translation: machine
translated_at: '2026-10-24'
---
# LaMa : inpainting à grand masque robuste à la résolution {#lama-resolution-robust-large-mask-inpainting}

**Périmètre vérifié : 2026-09-04.** LaMa est une méthode d'inpainting en mode feed-forward, conçue pour de grandes zones manquantes et des images haute résolution. Le travail d'origine combine des Fast Fourier Convolutions (FFC), une perte perceptuelle à champ réceptif élevé et de grands masques d'entraînement. Son comportement solide de complétion de textures et de structures en fait une référence utile, mais ce n'est pas un système de reconstruction déterministe d'objets.

## Pourquoi les convolutions de Fourier comptent {#why-fourier-convolutions-matter}

Une couche FFC répartit le traitement des caractéristiques entre un chemin local et un chemin global. Le chemin global utilise un traitement dans le domaine de Fourier, afin qu'une couche puisse intégrer des informations à travers toute l'image plutôt que seulement dans un petit voisinage spatial. Dans l'article de LaMa, ce champ réceptif plus large est associé à de grands masques et à un objectif perceptuel afin d'améliorer la complétion de lacunes difficiles et de structures périodiques.

Le dépôt source indique que le modèle peut se généraliser à des résolutions nettement supérieures à sa résolution d'entraînement. Considérez cela comme une capacité à tester sur les tailles d'image visées, et non comme une garantie que des entrées de plusieurs mégapixels préserveront la typographie fine, les facettes de bijoux, les visages ou l'identité des objets.

## Utiliser LaMa pour la bonne classe de restauration {#use-it-for-the-right-restoration-class}

LaMa est un bon candidat lorsque le critère d'acceptation est une continuité cohérente de l'arrière-plan, de la texture ou d'une structure simple :

- supprimer un objet indésirable masqué sur un arrière-plan texturé ou répétitif ;
- combler un grand vide visuel lorsque le contexte source est suffisant ;
- produire une base rapide et conservatrice avant une modification générative plus coûteuse.

Utilisez une voie distincte d'édition sémantique ou de composition manuelle lorsque la tâche exige un logo exact, un texte lisible, l'identité d'une personne précise ou un objet critique pour la sécurité. Un remplissage d'apparence propre n'est pas une preuve que le contenu supprimé ou reconstruit est correct.

## Enregistrement reproductible d'une exécution {#reproducible-run-record}

Le dépôt amont publie plusieurs configurations de modèles et renvoie vers des checkpoints ; certains anciens liens de téléchargement ont changé. Pour chaque exécution, conservez :

1. la révision du dépôt ainsi que l'origine exacte et l'empreinte (digest) du checkpoint ;
2. le prétraitement des images, la méthode de création du masque et la résolution d'entrée ;
3. la règle de composition des sorties, en particulier si les pixels non masqués proviennent de l'original ;
4. les images avant/après, le masque et un résultat d'acceptation humaine ;
5. un retour à l'image source non modifiée lorsque le remplissage franchit une limite critique.

Les applications tierces, portages et nœuds ComfyUI listés par le projet sont des intégrations distinctes. Vérifiez leur source de modèle, leur comportement en matière de confidentialité et leur licence avant de les considérer comme équivalents à l'implémentation amont.

## Périmètre de la licence {#license-boundary}

Le dépôt source `advimman/lama` vérifié contient une licence Apache-2.0. Les checkpoints téléchargés, les conditions des plateformes d'hébergement de modèles et les portages tiers peuvent ajouter leurs propres conditions ; vérifiez donc l'artefact exact avant toute distribution ou déploiement commercial.

## Références {#references}

- [Dépôt officiel de LaMa](https://github.com/advimman/lama)
- [Article de LaMa](https://arxiv.org/abs/2109.07161)
- [Page projet de LaMa](https://advimman.github.io/lama-project/)
