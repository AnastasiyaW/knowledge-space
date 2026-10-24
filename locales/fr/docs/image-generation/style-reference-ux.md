---
title: "Style Reference UX : autorité, intensité et provenance"
description: "L'UX des références de style doit séparer l'influence temporaire de l'entraînement enregistré, le style du contenu et de la structure, et les données locales du traitement par des tiers, tout en rendant l'intensité et la provenance visibles pour l'utilisateur."
category: systems
tags: [style-reference, ux, provenance, privacy, lora, content-reference, strength-control]
aliases: ["Style Reference UX", "Style Reference Workflow"]
level: 2
source_sha256: c6f9b17c7801c58b9e2ea2f57a9db8ea7ada3c31dc9ae5f1fbbe705a01fa415d
translation: machine
translated_at: '2026-10-24'
---
# Style Reference UX : autorité, intensité et provenance {#style-reference-ux-authority-strength-and-provenance}

Un contrôle de référence de style modifie le rendu visuel, mais les utilisateurs
doivent comprendre ce qu'il peut emprunter, ce qu'il préservera, où leur
référence est envoyée, et si le choix est temporaire ou crée un actif
entraîné réutilisable. Ces éléments relèvent des exigences produit, et non
d'une aide facultative.

## Séparer les intentions de l'utilisateur {#separate-the-users-intents}

Exposer des contrôles distincts pour :

- **style :** palette, texture, ambiance, médium et langage visuel ;
- **contenu :** sujet, identité de l'objet, géométrie du produit et faits de la scène ;
- **structure :** pose, mise en page, cadrage ou contraintes spatiales ; et
- **préservation :** caractéristiques de la référence qu'une modification doit laisser intactes.

Ne pas présenter ces éléments comme un unique curseur vague « intensité de
référence ». Si un flux de travail ne peut techniquement pas les séparer, le
signaler et montrer le conflit attendu, plutôt que de suggérer que toutes les
propriétés de la référence seront préservées.

## Choix temporaires et choix durables {#temporary-versus-durable-choices}

Proposer deux parcours clairement étiquetés :

1. **Référence de session :** appliquée uniquement au travail en cours et
   supprimable avec l'enregistrement de ce travail.
2. **Style enregistré ou adaptateur entraîné :** un actif durable avec un nom,
   un propriétaire, une source/provenance, une liaison au modèle, une politique
   de conservation et un chemin de suppression.

Un style enregistré ne doit jamais être créé implicitement à partir d'un
téléversement. L'entraînement, le partage ou la réutilisation exigent une
action explicite distincte et un énoncé visible des données qui seront
conservées.

## Contrôles d'intensité qui communiquent le risque {#strength-controls-that-communicate-risk}

Utiliser un contrôle d'intensité réversible, avec des effets décrits en langage
clair et un aperçu comparé à la référence de base sans référence. L'interface
doit indiquer quand l'augmentation de l'influence du style affaiblit également
la préservation du contenu ou de la structure. Éviter de laisser croire que les
pondérations numériques sont comparables entre différents modèles, adaptateurs
ou images de référence.

Pour les requêtes complexes, fournir un résumé explicite des conflits avant la
génération : quelle source contrôle la couleur, laquelle contrôle la
composition, laquelle contrôle les faits de l'objet, et laquelle prime lorsqu'elles
divergent.

## Frontière des données et des fournisseurs {#data-and-provider-boundary}

Avant d'accepter une référence, indiquer si elle reste locale ou si elle est
envoyée à un fournisseur de légendage, d'embeddings, de génération ou
d'entraînement. Consigner dans le reçu du travail le fournisseur, le
modèle/la révision, les conditions de conservation et d'accès, ainsi que
l'autorité de l'utilisateur. Les portraits sensibles, les produits couverts
par un accord de confidentialité (NDA) et les œuvres de tiers exigent une
décision explicite sur les usages autorisés.

## Acceptation et réutilisation {#acceptance-and-reuse}

Afficher un panneau source avec miniatures/empreintes numériques, liaison au
modèle et à l'adaptateur, portée de la référence, prompt, sortie et retours.
Les évaluations des utilisateurs sont des signaux de préférence utiles, mais
elles ne prouvent ni les droits, ni l'exactitude factuelle du produit, ni la
préservation de l'identité. Un adaptateur réutilisable doit suivre le contrat
de publication décrit dans [[flux-klein-style-lora-system]].

## Pages connexes {#related-pages}

- [[flux-klein-style-lora-system]]
- [[megastyle-flux-style-transfer]]
- [[flux-klein-jewelry-photography]]
- [[face-beautify-edit-lora]]
