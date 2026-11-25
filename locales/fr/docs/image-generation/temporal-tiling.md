---
title: "Tuilage temporel : périmètre de recherche et plan d'évaluation"
description: "Le tuilage temporel est une expérience de recherche propre à un modèle, portant sur la cohérence inter-tuiles, et non une réutilisation directe de la mémoire vidéo ; lier le plan de tuilage et l'état d'exécution, comparer à une base de référence à recouvrement, et valider les jointures, la composition et le coût sur des images de test."
category: techniques
tags: [tiling, image-generation, research, global-context, evaluation]
aliases: ["Tiles-as-Frames", "Temporal Tile Processing"]
level: 3
source_sha256: 0e154bd08f66a54f7f798a93ca98bd2fdf900d6bed373296e14d4b784fc632c6
translation: machine
translated_at: '2026-10-24'
---
# Tuilage temporel : périmètre de recherche et plan d'évaluation {#temporal-tiling-research-boundary-and-evaluation-plan}

Le tuilage temporel est l'hypothèse selon laquelle une grande image peut être
générée comme une séquence de tuiles spatiales tout en conservant un contexte
utile issu des tuiles précédentes. Le terme *temporel* est une analogie : les
tuiles occupent des emplacements différents dans une même image, et non des
images différentes d'une vidéo. Le considérer comme une expérience de recherche
propre à un modèle tant qu'un modèle entraîné et un runtime ne prennent
explicitement en charge l'état qui est propagé.

## Ce qu'un système par tuiles doit préserver {#what-a-tiled-system-must-preserve}

Le tuilage classique permet de débruiter indépendamment des régions et de
fondre leurs zones de recouvrement. Cela suffit souvent pour maîtriser la
mémoire, mais peut produire des discontinuités dans les gradients, la
géométrie, l'éclairage ou les objets répétés. Une proposition de tuilage
temporel doit corriger ces défauts sans modifier silencieusement le contrat de
l'image.

Consigner ces éléments pour chaque expérience :

- l'image source ou le prompt, le cadre de droits, la graine et la révision du
  checkpoint ;
- la grille de tuiles, le recouvrement, l'ordre, la convention de coordonnées
  et la politique de redimensionnement ;
- le runtime exact, la représentation latente et toute API de cache/état prise
  en charge ;
- les régions protégées et la définition d'une modification acceptable ; et
- une base de référence simple, à recouvrement uniquement, générée à partir des
  mêmes entrées.

Sans cet enregistrement, une sortie plus homogène ne peut pas être attribuée au
contexte des tuiles plutôt qu'à un prompt, un échantillonneur, un recadrage ou
un checkpoint modifié.

## Ne pas assimiler l'état vidéo à l'état d'une tuile d'image {#do-not-equate-video-state-with-image-tile-state}

[SANA-Video](https://github.com/NVlabs/Sana/blob/main/docs/sana_video.md)
utilise des mécanismes autorégressifs par blocs pour un modèle vidéo. Le
[dépôt SANA](https://github.com/NVlabs/Sana) documente l'attention linéaire, les
familles de modèles image/vidéo et leurs propres runtimes. Ces éléments ne font
**pas** de son état interne une interface publique utilisable telle quelle pour
des tuiles d'image quelconques.

En particulier, ne pas :

- injecter des statistiques d'attention non documentées à l'aide de hooks ;
- réutiliser un cache vidéo après avoir modifié les positions des tokens, la
  disposition latente ou la révision du modèle ;
- affirmer qu'un masque causal vidéo prouve une amélioration des jointures
  spatiales ; ni
- recopier une configuration vidéo dans un pipeline image sans implémentation
  et test propres à ce modèle.

La même prudence s'applique à toute cross-attention, tout adaptateur ou tout
transfert d'état caché : il n'est valide que si le checkpoint a été entraîné et
évalué avec ce chemin de conditionnement.

## Approches candidates et limites de leurs preuves {#candidate-approaches-and-their-evidence-boundary}

| Approche | Ce qu'elle permet de tester | Ce qu'elle ne prouve pas |
|---|---|---|
| Recouvrement et fusion | base de référence d'inférence par tuiles sûre en mémoire | cohérence globale des objets |
| Condition globale basse résolution | si un chemin de conditionnement pris en charge aide la structure | que tout modèle de tuiles peut consommer cette condition |
| Module de contexte spatial entraîné | si un checkpoint nommé apprend des dépendances inter-tuiles | le transfert vers un autre modèle, une autre grille ou un autre ratio d'aspect |
| État causal natif vidéo | le comportement sur de longues séquences dans le runtime vidéo compatible | la correction pour un balayage spatial d'image |

Commencer par le chemin pris en charge le plus simple. Si un modèle d'image
expose un mode officiel de condition globale ou d'inférence par tuiles, lier
l'expérience à la documentation propre à ce modèle. Sinon, maintenir la
proposition au stade de la recherche plutôt que de créer un pont d'état caché
non versionné.

## Plan d'évaluation {#evaluation-plan}

Utiliser des images de test disjointes des données source, incluant à la fois
des matériaux homogènes et des scènes à forte composition. Comparer chaque
candidat à la base de référence à recouvrement uniquement, avec la même graine
et le même contrat de modèle.

Évaluer trois questions distinctes :

1. **Continuité aux frontières.** Inspecter les recadrages de recouvrement, les
   gradients, les textures répétées et les décalages de couleur à chaque bord
   de tuile.
2. **Fidélité globale.** Inspecter les objets dupliqués, les nombres modifiés,
   les étiquettes altérées, la géométrie des produits, les visages et les
   régions protégées sur l'image entière.
3. **Coût opérationnel.** Mesurer la mémoire maximale, le temps d'exécution, le
   comportement des nouvelles tentatives et le comportement de réinitialisation
   du cache sur le runtime et le matériel réels.

N'utiliser des métriques que lorsque leur référence et leur calcul sont
définis. Un score de jointure peut comparer une sortie à une cible connue ou à
un recouvrement contrôlé, mais il n'établit pas que le texte généré, l'identité,
les attributs produits ou d'autres faits sont corrects. Conserver la revue
visuelle et la préservation des faits comme contrôles explicites avant
publication.

## Critère de passage en production {#promotion-gate}

Ne qualifier un chemin de tuilage temporel d'implémenté que si tous les
éléments suivants existent :

- une interface modèle/runtime versionnée pour la condition ou l'état propagé ;
- une configuration reproductible et un enregistrement source/sortie ;
- des résultats sur images de test face à la base de référence à recouvrement ;
  et
- une politique de publication approuvée par le responsable, couvrant les
  échecs, les régions protégées et la vérification des détails factuels.

Sinon, le qualifier d'expérience. Une image plausible et sans jointure visible
ne constitue pas une preuve suffisante pour transformer une analogie
architecturale en capacité de production.

## Sources et pages connexes {#sources-and-related-pages}

- [Dépôt SANA](https://github.com/NVlabs/Sana)
- [Documentation SANA-Video](https://github.com/NVlabs/Sana/blob/main/docs/sana_video.md)
- [[tiled-inference]]
- [[block-causal-linear-attention]]
- [[sana-denoiser-architecture]]
