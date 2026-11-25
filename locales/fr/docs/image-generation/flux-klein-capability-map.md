---
title: "Carte des capacités FLUX.2 [klein] : contrat d'opération attesté"
description: "Une capacité FLUX.2 [klein] n'est utilisable que lorsque la variante exacte, le checkpoint, la licence, le runtime ou le point de terminaison du fournisseur, le contrat d'entrée et la revue des sorties sont attestés au moment de l'exécution ; la prise en charge de la génération et de l'édition au niveau de la famille n'autorise ni chaque adaptateur, ni chaque service, ni chaque usage commercial, ni chaque résultat d'édition."
category: reference
tags: [flux, klein, capabilities, operations, licensing, adapters, provenance]
aliases: ["Klein Operations Map", "Klein Capability Map"]
level: 2
source_sha256: b9205c899ceefbe88b49888d4e1dace0c52c1b3fb7d4fe2b782d04dacda3f962
translation: machine
translated_at: '2026-10-24'
---
# Carte des capacités FLUX.2 [klein] : contrat d'opération attesté {#flux2-klein-capability-map-attested-operation-contract}

Les cartes de capacités vieillissent vite. Une annonce de famille, un adaptateur communautaire ou un ancien point de terminaison de fournisseur ne peuvent pas prouver ce qui est disponible, licencié, compatible ou sûr dans un travail en cours. Considérez une opération comme utilisable seulement après avoir attesté la version exacte et le chemin d'exécution.

## La prise en charge au niveau de la famille n'est pas un reçu d'opération {#family-support-is-not-an-operation-receipt}

Le [dépôt officiel de FLUX.2](https://github.com/black-forest-labs/flux2) indique que la famille [klein] prend en charge la génération de texte vers image, l'édition d'image à partir d'une seule référence et l'édition d'image à partir de références multiples. Il nomme également les versions 4B, 9B, 9B KV et Base, avec des finalités et des licences annoncées différentes.

Ce sont des capacités au niveau de la famille. Elles n'établissent pas que :

- un LoRA, un nœud, une conversion de checkpoint, une quantification ou un workflow communautaire particulier se charge sur la variante choisie ;
- un fournisseur hébergé expose toujours le même point de terminaison, le même schéma d'entrée, le même prix, la même politique de conservation ou le même droit commercial ;
- une image de référence peut être soumise à ce fournisseur ; ou
- une modification générée a correctement supprimé, préservé, déplacé, rééclairé ou identifié un sujet réel.

## Attester l'opération au moment de l'exécution {#attest-the-operation-at-execution-time}

Pour chaque tâche, conservez :

| Domaine du contrat | Reçu requis |
|---|---|
| Modèle | variante exacte, empreinte du checkpoint, composants, source et mention de licence |
| Runtime | révision du code/nœud local ou du point de terminaison du fournisseur, schéma d'entrée/sortie et comportement en cas d'erreur |
| Adaptateur | poids de l'adaptateur ainsi que sa configuration, base cible déclarée, test de chargement, auteur/source et licence |
| Entrées | autorité sur les ressources, consentement pour l'image de référence, prétraitement, masques/régions et divulgation des tiers |
| Politique | finalité autorisée, statut commercial/de distribution, provenance des sorties et autorité du relecteur |
| Preuves | empreinte de la requête/configuration, empreinte de la sortie, reçu modèle/runtime et revue propre à la tâche |

La [présentation du modèle](https://bfl.ai/models/flux-2-klein) de BFL publie des informations actuelles propres à chaque variante, notamment la finalité décrite d'une version. La fiche du modèle ou la documentation du fournisseur en vigueur au moment de l'exécution reste la source de référence ; ne figez pas dans une promesse opérationnelle des tableaux volatils de VRAM, de vitesse, d'échelle, de point de terminaison ou de tarification.

## Frontière des adaptateurs et des fournisseurs {#adapter-and-provider-boundary}

Les adaptateurs ne sont pas des capacités natives. Avant utilisation, vérifiez la compatibilité exacte avec la base, le format et la configuration de l'adaptateur, les modules cibles, la licence, ainsi que le comportement au chargement et en sortie. Les étiquettes communautaires telles que « remove », « relight », « consistency » ou « character » décrivent un effet visé, et non une autorisation approuvée de modifier un contenu protégé.

Pour un service distant, consignez le point de terminaison exact, les conditions de région et de conservation, le schéma de requête, le schéma de réponse, les conditions commerciales et les entrées visibles par le fournisseur. Si l'un de ces éléments ne peut pas être attesté, laissez l'opération indisponible plutôt que de basculer silencieusement vers un autre modèle, un autre point de terminaison ou un autre nœud local.

## Relire la sortie, pas l'étiquette {#review-the-output-not-the-label}

La génération de texte vers image, l'édition à partir de références et les adaptateurs peuvent produire des contenus plausibles. Ils ne restituent pas des faits absents et ne prouvent pas une identité inchangée. Vérifiez les régions protégées déclarées, le texte, la géométrie, les indices de matière et de couleur, ainsi que les droits avant toute publication. Traitez les sorties incertaines comme des propositions dotées d'une provenance visible, et non comme des résultats fidèles à la source.

## Pages associées {#related-pages}

- [[flux-klein-9b-architecture]]
- [[flux-klein-9b-inference]]
- [[flux-klein-character-lora]]
- [[style-reference-ux]]
