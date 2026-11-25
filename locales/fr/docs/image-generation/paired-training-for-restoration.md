---
title: "Entraînement de restauration appariée : preuves et contrat de conditionnement"
description: "L'entraînement de restauration appariée apprend une correspondance déclarée entre une entrée dégradée et une cible approuvée ; il nécessite des paires alignées sur la source et dont les droits ont été vérifiés, un chemin de conditionnement compatible avec le modèle, des holdouts séparés par source, et une évaluation qui distingue la récupération mesurée de l'invention plausible."
category: techniques
tags: [image-to-image, paired-data, restoration, conditioning, provenance, evaluation]
aliases: ["Image-to-Image Conditioning", "Paired Image Training", "Degradation Pipeline"]
level: 3
source_sha256: f3c171e8a93683dfec26052a9103591415540de40b70b4bcbcaaa1a4985d5bc0
translation: machine
translated_at: '2026-10-24'
---
# Entraînement de restauration appariée : preuves et contrat de conditionnement {#paired-restoration-training-evidence-and-conditioning-contract}

L'entraînement de restauration appariée apprend une correspondance déclarée entre
une entrée dégradée et une cible approuvée. Il ne s'agit pas d'un entraînement
text-to-image classique avec des légendes plus propres, et il ne doit jamais
présenter une texture générée plausible comme une preuve source récupérée.

[Palette](https://arxiv.org/abs/2111.05826) est un cadre de diffusion
conditionnelle image-vers-image couvrant des tâches telles que la colorisation,
l'inpainting, le recadrage étendu (uncropping) et la restauration JPEG. Cet
article justifie le besoin général d'une condition image explicite ; il ne
prescrit pas une disposition unique des canaux, une initialisation, une fonction
de perte, un planificateur ni une recette d'entraînement pour tous les modèles
récents.

## Définir la paire {#define-the-pair}

Pour chaque échantillon, conservez :

- l'autorité d'origine de la source et le registre des droits ;
- l'entrée dégradée, la cible et leurs empreintes (hashes) ;
- la politique d'alignement, de recadrage, de redimensionnement et d'espace colorimétrique ;
- la dégradation déclarée ou l'opération de retouche approuvée ;
- les régions éditables et les régions protégées ou inconnues ; et
- la décision du relecteur, ainsi que toute incertitude ou motif d'exclusion.

La source et la cible doivent représenter la même scène approuvée ou une
modification spécifiée délibérément. Si la cible contient une embellissement
manuel, un remplissage génératif ou des modifications historiques inconnues,
signalez ce fait plutôt que de la traiter comme une vérité terrain propre.

## Le conditionnement doit correspondre au modèle {#conditioning-must-match-the-model}

Les systèmes conditionnés par image peuvent utiliser une concaténation de
canaux, une attention croisée, une branche de contrôle dédiée, un encodeur
d'image ou tout autre mécanisme propre à l'architecture. N'utilisez que le
chemin de conditionnement documenté et entraîné pour le checkpoint épinglé.
Modifier le nombre de canaux d'entrée, injecter des latents ou copier un module
de conditionnement issu d'un autre framework crée une nouvelle configuration de
modèle, qui exige sa propre initialisation, son propre entraînement et sa propre
évaluation.

Consignez le contrat de conditionnement complet :

- le modèle de base ou checkpoint, ainsi que les révisions du VAE ou de l'encodeur ;
- le runtime, le planificateur ou l'objectif, et l'implémentation du module de conditionnement ;
- le prétraitement de l'entrée et de la cible, au niveau des latents ou des pixels ; et
- le comportement lorsque la condition est absente, mal formée, masquée ou hors distribution.

Ne supprimez jamais silencieusement une condition image pour renvoyer un résultat
non conditionné comme si la restauration avait réussi.

## Construire des preuves de dégradation honnêtes {#build-honest-degradation-evidence}

La dégradation synthétique peut produire des exemples appariés contrôlés, mais
elle ne modélise que les transformations déclarées. Gardez une distinction nette
entre les dégradations synthétiques et les dégradations réelles observées. Ne
prétendez pas que des paramètres de bruit, de flou, de compression ou de
sous-échantillonnage reproduisent un historique inconnu de prise de vue ou
d'édition sans preuve à l'appui.

Répartissez les données d'entraînement, de réglage et de holdout par ressource
d'origine, session de capture, sujet ou produit, et chaîne de dérivation. Les
recadrages adjacents ou les multiples versions dégradées d'un même original
doivent appartenir au même jeu.

## Évaluer la récupération séparément de la plausibilité {#evaluate-recovery-separately-from-plausibility}

| Type de preuve | Ce qu'elle peut étayer |
|---|---|
| Cible alignée et autorisée | métriques de reconstruction appariée et revue visuelle des erreurs sous une politique couleur/recadrage définie |
| Image dégradée réelle, source disjointe, sans cible | utilité vérifiée et analyse des échecs, sans affirmation de précision au pixel près |
| Détail de cible généré ou incertain | une proposition visuelle dérivée, jamais une vérité terrain factuelle récupérée |

Examinez séparément le texte, les marques, la géométrie des produits, les
visages, les régions protégées et le détail des matériaux, en dehors des
métriques agrégées. Un score de qualité visuelle élevé peut coexister avec une
sortie factuellement altérée.

## Critère de publication {#release-gate}

Ne publiez un modèle de restauration appariée qu'avec des paires reproductibles,
un chemin de conditionnement compatible avec le modèle, des holdouts disjoints
par source, une provenance des sources et des sorties, et une politique pour les
détails factuels incertains ou modifiés. Si le modèle ne peut pas distinguer la
récupération de l'invention pour l'usage visé, ne le diffusez que comme
proposition d'amélioration relue, ou écartez-le de ce flux de travail.

## Pages connexes {#related-pages}

- [[image-restoration-survey]]
- [[synthetic-dataset-pipeline]]
- [[upscaler-evaluation]]
