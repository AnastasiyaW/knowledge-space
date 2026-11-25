---
title: "LoRA d'identité FLUX.2 [klein] : contrat de consentement et d'évaluation"
description: "Un LoRA d'identité est un adaptateur sensible, lié à une version précise, entraîné uniquement à partir d'images autorisées pour une finalité définie ; associez le consentement, le checkpoint de base et le format de l'adaptateur, la politique relative aux données et à la suppression, ainsi qu'une revue de ressemblance et de préservation disjointe par source, et ne considérez jamais une correspondance d'identité générée comme une identité vérifiée."
category: techniques
tags: [lora, identity, consent, provenance, flux, klein, evaluation, privacy]
aliases: ["Klein Character LoRA", "Klein Identity LoRA", "Klein Person LoRA"]
level: 2
source_sha256: b31310c9912250a75883848c8a70b37b972de59e6cfbc6742773995021cf9829
translation: machine
translated_at: '2026-10-24'
---
# LoRA d'identité FLUX.2 [klein] : contrat de consentement et d'évaluation {#flux2-klein-identity-lora-consent-and-evaluation-contract}

Un LoRA d'identité ou de personnage n'est pas un simple preset de style. C'est
un adaptateur sensible, capable de faire apparaître une personne dans de
nouveaux contextes. Ne l'entraînez ou ne l'utilisez que pour une finalité
autorisée, avec une procédure claire de retrait et de suppression, et avec une
revue qui distingue une ressemblance visuelle d'une identité vérifiée.

## Établir l'autorisation avant la préparation des données {#establish-authority-before-data-preparation}

Consignez :

- l'autorisation de la personne représentée, la finalité autorisée, la durée,
  la divulgation et le contact pour la révocation ;
- la propriété des images sources, le contexte d'acquisition et les usages
  dérivés autorisés ;
- la politique de conservation et de suppression des originaux, légendes,
  recadrages, masques, adaptateurs, checkpoints, aperçus et copies chez le
  fournisseur ;
- si une donnée quitte l'environnement approuvé et les conditions applicables
  du fournisseur en matière de données et de conservation ; et
- les usages interdits, notamment l'identification, l'authentification,
  l'usurpation d'identité, l'inférence de caractéristiques sensibles, ou la
  publication sans la revue convenue.

Ne constituez pas un jeu de données d'identité à partir de portraits collectés
sans autorisation, de références non vérifiables, ou d'embeddings d'images qui
ne disposent pas de cette autorisation. Un mot-déclencheur, une légende, un
recadrage de visage ou un exemple généré ne valent pas consentement.

## Fixer la compatibilité du modèle et de l'adaptateur {#pin-model-and-adapter-compatibility}

Associez le checkpoint Base exact, le runtime, les composants texte et image,
la méthode et la configuration de l'adaptateur, les modules cibles, les
versions du trainer et le chargeur d'inférence. Le [guide d'entraînement
klein de BFL](https://docs.bfl.ai/flux_2/flux2_klein_training) décrit les
variantes Base comme des points de départ pour le fine-tuning, mais il ne rend
pas compatible, d'un outil ou d'une version à l'autre, un optimiseur générique,
un nombre d'images, un rang, un placement des légendes ou un adaptateur
« d'identité ».

Conservez à la fois les poids de l'adaptateur et sa configuration. Le
[format de checkpoint PEFT](https://huggingface.co/docs/peft/developer_guides/checkpoint)
illustre pourquoi une configuration est nécessaire à côté des poids. Testez la
paire exacte entraînement/inférence sur une base approuvée et non sensible
avant d'accepter une exécution portant sur des données personnelles.

## Construire un ensemble d'évaluation honnête {#build-an-honest-evaluation-set}

Séparez le matériau d'entraînement, de réglage et de validation finale par
capture d'origine, session, pose/cadrage, tenue/arrière-plan et chaîne de
dérivation. La politique d'évaluation doit nommer ce qui doit rester intact et
ce qui peut changer :

- le contexte, le style ou la modification demandés ;
- la ressemblance, jugée par des relecteurs autorisés dans le cadre de la
  finalité déclarée ;
- les traits faciaux et corporels protégés, les indices d'âge, les marques, le
  texte, les accessoires et les autres zones ; et
- les échecs, tels qu'une ressemblance non voulue, une sexualisation, un
  contexte dégradant, une fausse association ou la perte de détails factuels
  sur le produit ou l'arrière-plan.

N'utilisez pas un score de similarité automatique comme identification, ni
comme unique décision de publication. Ne prétendez pas qu'une image générée
prouve qui est une personne, ce qu'elle a fait, ou son consentement au
résultat.

## Publication et révocation {#release-and-revocation}

Gardez chaque sortie approuvée traçable vers sa base, son adaptateur, sa
politique d'entrée et son justificatif de revue. Indiquez la modification par
IA lorsque la politique ou la loi l'exige. Si l'autorisation expire ou est
retirée, désactivez toute nouvelle inférence, supprimez l'adaptateur et les
données dérivées selon la politique de suppression convenue, et consignez
l'achèvement sans exposer de matériel personnel.

Si le projet ne peut pas satisfaire ces contrôles, n'entraînez pas d'adaptateur
d'identité : utilisez plutôt un flux de travail de personnage ou de style non
identifiant, ou bloquez la demande.

## Pages connexes {#related-pages}

- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
- [[style-reference-ux]]
- [[flux-klein-9b-architecture]]
