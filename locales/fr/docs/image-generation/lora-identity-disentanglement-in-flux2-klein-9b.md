---
title: "LoRA d'identité FLUX.2 [klein] 9B : contrat de désentrelacement"
description: "Un LoRA d'identité FLUX.2 [klein] 9B est une expérimentation d'adaptateur liée à une version, à des données et à des droits ; il faut associer la version de base officielle et ses conditions, le format de l'adaptateur et du runtime, les références d'identité autorisées, la politique d'étiquetage/légendes et de préservation, l'évaluation sur identités et cibles non-cibles disjointes des sources, ainsi qu'une revue avant toute utilisation."
category: techniques
tags: [flux2-klein, lora, identity, disentanglement, provenance, evaluation]
aliases: ["LoRA Identity Disentanglement in FLUX.2 Klein 9B", "FLUX.2 Klein Identity LoRA"]
level: 2
source_sha256: ae1410d6e60e28c1f20df38252c724bacbbc83e05f4697d255873dd8959892d4
translation: machine
translated_at: '2026-10-24'
---
# LoRA d'identité FLUX.2 [klein] 9B : contrat de désentrelacement {#flux2-klein-9b-identity-lora-disentanglement-contract}

Un LoRA d'identité apprend un adaptateur pour une version particulière du
modèle de base ; il n'isole pas par défaut une personne de tous les attributs
qui l'entourent. Le « désentrelacement » est une affirmation de préservation
qui doit être étayée par des preuves pour les données, l'adaptateur, le
runtime et le flux de travail de prompt/édition nommés.

La [documentation officielle d'entraînement FLUX.2 [klein]](https://docs.bfl.ai/flux_2/flux2_klein_training)
décrit le fine-tuning LoRA pour la famille, y compris les cas d'usage de
cohérence de personnage. Elle distingue également le modèle de base 9B et ses
conditions des autres variantes. Cela justifie une expérimentation sur la
version compatible exacte, et non l'affirmation que les choix de blocs, la
réduction de rang, l'arithmétique d'adaptateurs ou la recette d'une autre
famille se transposent sans modification.

## Associer l'adaptateur et son autorité {#bind-the-adapter-and-its-authority}

Pour chaque exécution, conserver :

- l'identifiant officiel du modèle de base/point de contrôle, le condensat
  (digest) de l'artefact, la licence et les conditions d'accès, le runtime du
  modèle, et le chemin de sérialisation/chargement de l'adaptateur ;
- les ressources de référence autorisées, le consentement ou tout autre
  fondement d'usage, la finalité, les règles de conservation et de suppression,
  les légendes, le vocabulaire de déclenchement, ainsi que tout attribut ou
  région exclu ;
- la répartition entraînement, le regroupement source/dérivé, le prétraitement,
  le recadrage/l'orientation, la politique de légendes, la politique
  d'augmentation, la révision du code/de la configuration, et les graines
  (seeds) ;
- le fichier d'adaptateur proposé, les contrôles de fusion/intensité, le
  condensat de sortie, et le flux de travail exact utilisé pour l'évaluation ;
  et
- la décision du relecteur, avec les preuves de correspondance d'identité, les
  preuves de préservation des éléments non-cibles, les exemples d'échec et une
  conclusion sur l'usage permis.

Un adaptateur 9B doit être associé à la version du modèle et au runtime pour
lesquels il a été entraîné. Ne pas déduire la compatibilité d'une variante
FLUX similaire, d'une extension de fichier ou d'un libellé d'interface
communautaire.

## Mesurer la séparation plutôt que la présumer {#measure-separation-rather-than-assume-it}

Définir quelles propriétés d'identité demandées peuvent être transférées et
quelles propriétés non-cibles doivent rester contrôlables : pose, expression,
présentation de l'âge, vêtements, arrière-plan, éclairage, style, morphologie
et attributs protégés. Évaluer le transfert demandé séparément de la
préservation, sur des prompts et des références mis de côté et disjoints des
sources. Conserver les corrections des relecteurs autorisés et les cas
négatifs, en particulier lorsqu'un adaptateur reproduit un arrière-plan,
modifie une région protégée ou crée une ressemblance non voulue.

Le ciblage par blocs, la sélection de rang, les pertes d'orthogonalité, la
soustraction, la fusion et la troncature SVD sont des expérimentations propres
au modèle et à l'implémentation. Elles requièrent une hypothèse déclarée, une
implémentation figée, une référence de comparaison et la même revue
d'identité/de préservation ; aucune n'est une étape de nettoyage universelle.

## Limite d'échec {#failure-boundary}

Si la version de base ou ses conditions sont inconnues, si l'autorité sur les
références est incomplète, si le format de l'adaptateur/du runtime diffère,
si des groupes de sources fuient dans l'évaluation, ou si un relecteur ne peut
pas distinguer le transfert demandé d'une modification non-cible, retirer
l'adaptateur de l'usage. Ne pas le charger silencieusement sur une autre
variante, ne pas supprimer de preuves, et ne pas qualifier une ressemblance
générée d'identité vérifiée.

## Pages connexes {#related-pages}

- [[flux-klein-character-lora]]
- [[diffusion-lora-training]]
- [[lora-auxiliary-losses]]
- [[face-beautify-edit-lora]]
