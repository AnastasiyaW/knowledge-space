---
title: "Architecture FLUX.2 [klein] : interface liée à la version publiée"
description: "Les affirmations d'architecture sur FLUX.2 [klein] doivent être rattachées à la version officielle nommée et à son artefact ; la famille publique prend en charge la génération texte-vers-image et l'édition à partir de référence, mais les structures internes des blocs, le câblage de l'encodeur, la quantification et la compatibilité des adaptateurs ne peuvent pas être déduits sans risque d'une variante ou d'un environnement d'exécution à l'autre."
category: reference
tags: [flux, klein, architecture, model-contract, adapters, inference, provenance]
aliases: ["Klein Architecture", "FLUX2 Klein Architecture"]
level: 2
source_sha256: dc36186cf6588c455a0d27e7ed5709515066920c70e24caef3adc1837e9d5e4a
translation: machine
translated_at: '2026-10-24'
---
# Architecture FLUX.2 [klein] : interface liée à la version publiée {#flux2-klein-architecture-release-bound-interface}

FLUX.2 [klein] est une famille de modèles, et non un fichier d'architecture
unique et interchangeable. Pour toute affirmation interne, faites référence au
point de contrôle nommé, à la fiche modèle officielle, à la révision du code
source et à l'environnement d'exécution. Les étiquettes de nombre de paramètres,
un nom de famille ou un workflow tiers ne permettent pas d'établir le nombre de
blocs, le câblage de l'encodeur de texte, la disposition des latents, la prise
en charge de la quantification ou la compatibilité des adaptateurs.

## Ce que la déclaration officielle de la famille couvre {#what-the-official-family-declaration-supports}

Le [dépôt officiel FLUX.2](https://github.com/black-forest-labs/flux2)
répertorie les variantes [klein] 4B, 9B, 9B KV, 4B Base et 9B Base, et décrit
la génération texte-vers-image ainsi que l'édition à partir d'une ou de plusieurs
images de référence pour l'ensemble de la famille. Il distingue les variantes
distillées des variantes Base et recommande les modèles Base pour le
fine-tuning et les travaux LoRA.

Cela permet de choisir une version, mais cela ne rend pas vrais un schéma
interne fixe du transformeur, une méthode d'extraction des couches Qwen, un
nombre de canaux du VAE, un décalage RoPE, une limite de longueur de séquence
ou un réglage d'inférence pour tout artefact portant le nom [klein].

## Figer l'interface d'exécution {#bind-the-executable-interface}

Pour un déploiement ou un job d'entraînement donné, conservez :

- l'identifiant officiel du modèle, la révision ou le condensé (digest), la
  mention de licence et tous les composants requis ;
- la source et la version de l'environnement d'exécution, le tokenizer et
  l'encodeur de texte, le VAE ou décodeur, le scheduler et le schéma d'entrée
  des images et des références ;
- la prise en charge du dtype, de la quantification et du matériel (device et
  back-end), telle que documentée pour cette version exacte ;
- le point d'entrée exposé pour la génération ou l'édition, le prétraitement
  requis et les métadonnées de sortie ; et
- un reçu de référence prouvant que le chemin choisi (texte, référence unique
  ou références multiples) s'exécute réellement.

Les images de référence sont des entrées qui ont leurs propres règles de
propriété, de prétraitement, de nombre, d'ordre et de gestion des échecs. Ne
déduisez pas une disposition commune des séquences latentes, ni la réutilisation
d'un état issu d'une autre variante, au motif qu'une interface accepte plusieurs
images.

## Frontière entre Base, distillé et compatibilité {#base-distilled-and-compatibility-boundary}

Les versions Base et distillées n'ont pas les mêmes finalités déclarées. Le
[guide d'entraînement klein](https://docs.bfl.ai/flux_2/flux2_klein_training) de
BFL présente les modèles Base comme des points de départ non distillés pour le
fine-tuning, tandis que l'aperçu public des modèles répertorie les distinctions
d'environnement d'exécution et d'usage au niveau de la famille. Figez l'artefact
choisi plutôt que de présenter ces indications comme une garantie générale de
conversion ou d'inférence.

Un adaptateur n'est compatible qu'après avoir testé ensemble le point de
contrôle de base cible, l'architecture, le chargeur, la configuration de
l'adaptateur et le comportement en sortie. Ne chargez jamais un adaptateur
FLUX.1, 4B, 9B, communautaire ou quantifié en vous fiant uniquement à son nom de
fichier, à son nombre de paramètres ou à une forme interne supposée. Un
adaptateur en échec ou non vérifié doit renvoyer un résultat d'incompatibilité
visible, et non une fusion partielle silencieuse.

## Limites de licence et de sortie {#license-and-output-boundary}

La licence des poids locaux s'applique à l'artefact nommé, et non au mot générique
« FLUX ». Le [tableau officiel des modèles](https://github.com/black-forest-labs/flux2)
indique actuellement Apache-2.0 pour [klein] 4B et 4B Base, et la licence FLUX
Non-Commercial pour les variantes 9B. Vérifiez la licence jointe et la voie
commerciale en vigueur avant tout déploiement ou toute distribution ; un
adaptateur affiné peut constituer une œuvre dérivée soumise à des obligations
supplémentaires.

Les sorties générées ou éditées nécessitent également leur propre traçabilité,
une vérification des droits et une relecture visuelle. Une capacité du modèle ne
prouve pas qu'une modification donnée a préservé les faits, l'identité, la
géométrie des produits, le texte ou les zones protégées.

## Pages associées {#related-pages}

- [[flux-klein-capability-map]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
