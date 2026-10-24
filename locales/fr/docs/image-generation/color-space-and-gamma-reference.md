---
title: "Gestion des couleurs : contrat de transformation versionné"
description: "La gestion des couleurs est une chaîne versionnée d'interprétation de l'entrée, d'espace de travail, de transformations créatives, de transformation d'affichage ou de vue, et d'encodage de sortie ; les étiquettes de caméra ou de conteneur et les règles de gamma génériques sont insuffisantes sans le profil exact, la version de la transformation, la politique de métadonnées et l'écran de validation."
category: reference
tags: [color-management, color-space, transfer-function, icc, ocio, aces, output-transform]
aliases: ["Color Space and Gamma Reference", "Color Pipeline Reference"]
level: 3
source_sha256: 005fb80d074aee094050bf680f6c5bc52fe6578e65105af181b97fecb9456e90
translation: machine
translated_at: '2026-10-24'
---
# Gestion des couleurs : contrat de transformation versionné {#color-management-versioned-transform-contract}

La gestion des couleurs rend interprétables les valeurs numériques des images entre la capture, le traitement et l'affichage. Un nom de fichier, un conteneur, une marque de caméra ou une étiquette informelle comme « log » ne permet pas d'identifier une transformation d'entrée complète. Traitez chaque chaîne de transformation comme un contrat versionné, puis validez l'image livrée sur le parcours de visualisation prévu.

## Déclarer la chaîne de transformation {#declare-the-transform-chain}

Enregistrez chaque étape, dans l'ordre :

```text
source file or raw data
  -> input interpretation and decode
  -> working or reference space
  -> approved creative operations
  -> display or view transform
  -> output encoding, profile, and delivery metadata
```

Pour chaque tâche, associez le condensat (digest) de la source, les métadonnées embarquées, l'assignation d'entrée retenue, la révision de la transformation ou de la configuration, la politique d'espace de travail, le nom de l'affichage ou de la vue, l'encodage de sortie et l'écran de validation. Un décodage RAW, une transformation d'entrée caméra, une LUT et une transformation d'affichage sont des opérations distinctes, même lorsqu'une application les présente dans une même interface.

## Ne pas deviner l'interprétation de l'entrée {#do-not-guess-input-interpretation}

Les métadonnées peuvent être absentes, obsolètes ou incohérentes avec l'image capturée. Le type de conteneur et la famille de caméra ne suffisent pas à sélectionner une transformation. Si l'assignation d'entrée ne peut pas être vérifiée à partir de métadonnées faisant autorité, d'enregistrements de capture ou d'une référence approuvée, arrêtez-vous pour une revue ou marquez la sortie comme une interprétation explicite. Ne choisissez jamais silencieusement un profil de caméra « le plus proche », une fonction de transfert ou un espace à gamut étendu.

La même règle s'applique aux courbes de transfert. Le gamma, les encodages logarithmiques et les fonctions de transfert HDR sont définis par un encodage nommé et un contexte de diffusion ; une seule règle de gamma générique ne peut pas décoder en toute sécurité toutes les sources ni afficher toutes les sorties.

## Utiliser des configurations gérées et inspectables {#use-managed-inspectable-configurations}

L'[International Color Consortium](https://www.color.org/getting-started/) définit un Profile Connection Space (PCS) qui relie des profils d'entrée et de sortie créés indépendamment. [OpenColorIO](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html) utilise une configuration explicite pour les espaces colorimétriques, les affichages, les vues, les looks et les transformations. Les [transformations de sortie ACES](https://docs.acescentral.com/system-components/output-transforms/) sont elles aussi sélectionnées selon des combinaisons nommées de gamut cible, de luminance, de point blanc et d'encodage d'affichage.

Ces systèmes ne rendent pas à eux seuls une transformation générique correcte. Figez le profil ou la configuration ainsi que la version de la transformation, conservez-les avec la tâche, et validez leurs hypothèses d'entrée et de sortie après chaque mise à jour.

## Valider les images source, de travail et livrées {#validate-source-working-and-delivery-images}

Utilisez des images de test autorisées ou des mires calibrées couvrant les zones neutres, les couleurs proches de la limite du gamut, les dégradés, les hautes et basses lumières, le texte et les détails à préserver. Évaluez :

- le décodage de l'entrée et la gestion des métadonnées ;
- le comportement des couleurs, des tons et du gamut sur l'ensemble de la chaîne de transformation ;
- la cohérence entre l'affichage ou la vue de validation choisis et le fichier livré ;
- l'écrêtage, le banding, les mappings de gamut inattendus et les intégrations irréversibles (bake-in) ; et
- la reproductibilité après redémarrage, réinitialisation du cache ou mise à jour de la configuration.

Enregistrez le fichier et le profil de sortie ainsi qu'un accusé de revue. L'égalité numérique des pixels n'a de sens que si le même encodage et le même parcours de transformation sont nommés.

## Politique en cas d'échec {#failure-policy}

Une entrée non reconnue, un profil manquant, une cible d'affichage non prise en charge ou une validation de configuration échouée constituent un échec de capacité visible. Ce n'est pas une autorisation pour supprimer les métadonnées, intégrer une supposition ou modifier le parcours de sortie sans consigner ce choix. Gardez les modifications de gestion des couleurs et les modifications créatives d'étalonnage séparément auditables, afin qu'un rendu visuel ne soit jamais présenté à tort comme une correction.

## Pages associées {#related-pages}

- [[color-correction-by-numbers]]
- [[color-checker-and-white-balance]]
- [[color-theory-for-ml]]
- [[diffusion-lora-training]]
