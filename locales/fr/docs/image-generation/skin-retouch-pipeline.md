---
title: "Retouche cutanée : workflow de correction respectueux du consentement"
description: "La retouche cutanée est un workflow de correction respectueux du consentement et à portée limitée ; préserver l'identité, la texture et les traits protégés, garder chaque masque et chaque modification traçables, et exiger la revue de toute zone de peau modifiée."
category: workflows
tags: [skin-retouch, inpainting, consent, privacy, masks, texture-preservation, quality-control]
aliases: ["Skin Retouch Pipeline", "Blemish Correction Workflow"]
level: 2
source_sha256: ae13db7c36f0197bf792c23ae5ba3ce1da370f29dc84db88b55997355f52cb04
translation: machine
translated_at: '2026-10-24'
---
# Retouche cutanée : workflow de correction respectueux du consentement {#skin-retouching-consent-aware-correction-workflow}

La retouche cutanée doit corriger un défaut visuel précisément approuvé, sans
modifier silencieusement l'identité, la présentation de l'âge, le teint, les
caractéristiques corporelles ni l'apparence liée à la santé. Il ne s'agit pas
d'une opération générale d'« embellissement », et elle ne doit jamais servir à
inférer ou classer des traits médicaux ou personnels sensibles.

## Admission et consentement {#intake-and-consent}

Pour chaque image source, conserver l'empreinte (digest) de l'image, l'autorisation
de modifier, la finalité approuvée, le périmètre de correction demandé, la
politique d'accès et de conservation, ainsi que toute modification interdite.
Traiter les portraits comme des données sensibles, même lorsque la modification
envisagée est purement cosmétique.

Décrire les demandes en termes visuels bornés, par exemple un artefact visible
et temporaire dans une zone nommée. Si une demande est ambiguë, potentiellement
médicale, ou modifie une apparence protégée, la confier à une revue humaine
plutôt qu'à une retouche automatisée.

## Workflow centré sur le masque {#mask-first-workflow}

1. Créer ou revoir un masque pour le défaut approuvé.
2. Marquer les zones protégées, notamment les yeux, les lèvres, la ligne de
   cheveux, les contours du visage, les tatouages, les bijoux et tout contenu
   que la demande indique de préserver.
3. Choisir la correction la moins générative capable de satisfaire le masque.
4. Conserver ensemble l'original, le masque, les paramètres de l'opération et
   le résultat modifié.
5. Revoir chaque zone modifiée à la résolution de livraison et à côté de la
   source.

La détection ou la segmentation automatique peut proposer des masques, mais ne
peut pas décider quelle caractéristique de la peau doit être modifiée. Ne jamais
laisser un score de confiance du détecteur remplacer le consentement, l'intention
ou une décision d'acceptation humaine.

## Préservation de la texture et de l'identité {#texture-and-identity-preservation}

Utiliser un jeu de validation représentatif pour vérifier la continuité des
pores et de la texture, les transitions de bord, l'éclairage, la couleur et la
géométrie du visage. Une zone floue ou trop lissée constitue un échec, même si
l'artefact demandé a disparu. Lorsqu'un modèle d'inpainting est utilisé,
distinguer la zone générée des détails observés dans la source, et rejeter les
résultats qui modifient l'identité, les traits protégés ou les objets
adjacents.

Pour une modification plus importante ou un modèle d'édition, valider la
correction demandée séparément de la préservation ; voir
[[face-beautify-edit-lora]]. Pour le nettoyage de l'arrière-plan ou d'objets
autour d'une personne, utiliser le contrat de masque contraint décrit dans
[[object-removal-inpainting]].

## Fiche de livraison {#release-record}

Une retouche approuvée requiert les empreintes de la source et de la sortie, la
version du masque, la révision du modèle ou de l'outil, l'instruction, le
relecteur, la décision de périmètre et un chemin de livraison réversible. Ne pas
remplacer l'original par une image modifiée sans conserver les deux.

## Pages associées {#related-pages}

- [[face-beautify-edit-lora]]
- [[object-removal-inpainting]]
- [[face-detection-filtering-pipeline]]
- [[retouch-patch-harmonization]]
