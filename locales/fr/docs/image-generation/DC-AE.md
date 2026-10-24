---
title: "DC-AE : autoencodeur à compression profonde"
description: "Utilisez DC-AE uniquement avec un modèle de diffusion et le contrat de latent pour lequel il a été entraîné ; une forte compression réduit le travail sur les tokens latents mais ne en fait pas un remplacement direct d'un VAE."
category: architectures
tags: [vae, autoencoder, compression, latent-space, dc-ae, sana, efficientvit]
aliases: ["DC-AE", "Deep Compression Autoencoder", "AE-F32C32"]
level: 2
source_sha256: b966161657cefcc5341d2e19c636d7781e6ec8ffc30041405df58acfb686f1d1
translation: machine
translated_at: '2026-10-24'
---
# DC-AE : Deep Compression Autoencoder {#dc-ae-deep-compression-autoencoder}

**Périmètre vérifié : 2026-09-04.** DC-AE est une famille d'autoencodeurs à forte compression spatiale issus du MIT Han Lab. Il encode une image dans une grille latente plus petite avant qu'un modèle de diffusion ne la traite. Cette réduction peut diminuer sensiblement le travail sur les tokens latents à haute résolution, mais elle modifie la forme du latent, le nombre de canaux, la mise à l'échelle et les hypothèses sur le décodeur. C'est donc un composant d'un pipeline de modèles compatible, et non un remplacement générique de tous les VAE.

## Ce que fournit la famille publiée {#what-the-published-family-provides}

L'implémentation de référence décrit DC-AE comme une famille plutôt que comme un point de contrôle universel. Ses variantes publiées comprennent des modèles entraînés sur ImageNet et sur des données mixtes, à plusieurs taux de compression spatiale. La paire SANA est l'appariement pertinent pour [[SANA]] :

| Artefact | Forme du latent pour une entrée H × W | Rôle publié |
|---|---|---|
| `dc-ae-f32c32-sana-1.0` | `32 × H/32 × W/32` | point de contrôle compatible SANA |
| `dc-ae-f32c32-sana-1.1` | `32 × H/32 × W/32` | version ultérieure du décodeur compatible SANA |

L'article sur DC-AE attribue la reconstruction à forte compression à l'autoencodage résiduel et à l'adaptation haute résolution découplée. Ce sont des méthodes d'entraînement ; elles ne garantissent pas qu'un point de contrôle conservera le comportement d'un autre modèle de diffusion.

## La compatibilité est la contrainte principale {#compatibility-is-the-main-constraint}

Avant d'introduire DC-AE, rattachez ces éléments à la révision exacte du modèle :

1. **Contrat du latent :** facteur spatial, nombre de canaux latents, valeurs de mise à l'échelle et de décalage, normalisation et disposition attendue des tenseurs.
2. **Contrat du débruiteur :** un modèle entraîné pour un latent F32/C32 ne peut pas accepter le latent à quatre canaux et F8 utilisé par de nombreux pipelines de diffusion plus anciens.
3. **Prétraitement et post-traitement :** contraintes de taille d'entrée, comportement de remplissage et de recadrage, type de données et plage d'images doivent correspondre au pipeline de référence.
4. **Provenance des artefacts :** conservez la révision de la fiche modèle ou du dépôt source, pour l'autoencodeur comme pour le débruiteur.

Ne décodez pas un latent produit par un autoencodeur avec un autre décodeur, ne réutilisez pas un ancien cache de latents après avoir changé d'autoencodeur, et ne déduisez pas la compatibilité du seul nom `VAE`.

## Utilisation pratique {#practical-use}

[Diffusers](https://huggingface.co/docs/diffusers/main/en/api/models/autoencoder_dc) expose l'architecture sous le nom `AutoencoderDC`, tandis que le dépôt du MIT Han Lab publie les points de contrôle correspondants et des exemples de chargement. Partez d'une paire compatible publiée, comme SANA avec son point de contrôle DC-AE documenté ; ce n'est qu'ensuite que vous ferez des modifications de mémoire, de tuilage ou de précision.

Pour un pipeline d'images en production, conservez un jeu de fixtures A/B à travers le changement :

- résolutions, recadrages, zones transparentes ou quasi uniformes, et texte représentatifs ;
- vérifications de reconstruction encodage/décodage avant la génération ;
- générations contrôlées par prompt et graine à partir de la même révision du débruiteur ;
- observations de mémoire, de latence et de corruption d'artefacts sur le matériel cible ;
- un chemin de retour arrière vers la paire encodeur/débruiteur complète précédente.

Une forte compression réduit une source de calcul. Elle ne supprime ni le coût du débruiteur, ni les limites de mémoire, ni les échecs liés au contenu, ni la nécessité d'inspecter les sorties à la résolution visée.

## Périmètre de maintenance actuel {#current-maintenance-boundary}

Le dépôt `efficientvit` d'origine reste la référence pour les artefacts DC-AE publiés. Ses mainteneurs indiquent que les mises à jour et annonces futures ont été déplacées vers [DC-Gen](https://github.com/dc-ai-projects/DC-Gen). Traitez une nouvelle génération de DC-AE comme un nouveau projet de compatibilité, et non comme une mise à niveau sur place.

## Références {#references}

- [Implémentation DC-AE du MIT Han Lab et liste des artefacts](https://github.com/mit-han-lab/efficientvit/tree/master/applications/dc_ae)
- [Article sur DC-AE](https://arxiv.org/abs/2410.10733)
- [Implémentation de référence de SANA](https://github.com/NVlabs/Sana)
- [Documentation Diffusers de AutoencoderDC](https://huggingface.co/docs/diffusers/main/en/api/models/autoencoder_dc)
