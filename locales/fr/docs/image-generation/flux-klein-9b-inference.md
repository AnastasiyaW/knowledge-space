---
title: "Inférence FLUX.2 [klein] 9B"
description: "L'inférence FLUX.2 [klein] 9B doit suivre la variante de modèle, le checkpoint, le scheduler et la licence publiés ; évaluez le workflow exact de texte ou d'édition au lieu de reprendre des règles génériques de sampler, de VRAM ou de poids LoRA."
category: models
tags: [flux, flux2, klein, 9b, inference, editing, lora, reproducibility, licensing]
aliases: ["Klein 9B", "FLUX Klein 9B", "Klein Distilled"]
level: 3
source_sha256: 40feef373f1be8858fd4eb15f218296398c86c5f23f44735b2956251fc5e3f73
translation: machine
translated_at: '2026-10-24'
---
# Inférence FLUX.2 [klein] 9B {#flux2-klein-9b-inference}

FLUX.2 [klein] est une famille de modèles. FLUX.2 [klein] 9B est une version distillée nommée,
mais elle ne constitue toujours pas une configuration d'inférence complète sans sa révision de
checkpoint et ses ressources d'exécution. Le [dépôt officiel de FLUX.2](https://github.com/black-forest-labs/flux2)
distingue les variantes 9B, 9B KV et 9B Base ; ses recommandations placent les variantes distillées
pour les workflows interactifs, et les variantes de base pour le fine-tuning et une flexibilité
maximale. Considérez le checkpoint nommé et ses ressources d'exécution publiées comme un seul contrat.

## Identifier le contrat exact {#identify-the-exact-contract}

Consignez avant toute exécution d'inférence ou d'édition :

- le modèle et la révision du checkpoint, y compris la variante distillée/base ou KV ;
- le pipeline, le scheduler, l'encodeur de texte, le décodeur/VAE, le chargeur d'adaptateurs et le runtime ;
- la référence de prompt ou d'image, la seed, les dimensions et le format de sortie ;
- tous les adaptateurs et leur compatibilité avec le modèle source/de base ; et
- les conditions applicables aux poids, à l'API et à l'usage des dérivés.

Le projet officiel indique que FLUX.2 [klein] 9B est publié sous une licence non commerciale.
Cela n'autorise pas à lui seul un workflow de produit : vérifiez les conditions actuelles pour les
poids choisis et vérifiez séparément les conditions de tout service hébergé ou de tout composant tiers.

## La génération texte-image et l'édition sont des tests distincts {#text-to-image-and-editing-are-separate-tests}

Pour la génération texte-image, utilisez une suite de prompts courte et versionnée, incluant des
fixtures de composition, de matériaux, de typographie et de prompt négatif. Pour l'édition d'image,
conservez l'image source et déclarez les modifications demandées ainsi que les propriétés à protéger
avant la génération.

La [documentation d'édition d'images de FLUX.2](https://docs.bfl.ai/flux_2/flux2_image_editing)
décrit l'édition pilotée par texte, avec une ou plusieurs références. Cela ne signifie pas que chaque
wrapper local, checkpoint ou adaptateur préserve tous les détails. Vérifiez le parcours exact à l'aide
de comparaisons source/édité, et non à partir d'une affirmation générale sur les capacités du modèle.

## Ajuster par la mesure, non par la tradition {#tune-by-measurement-not-folklore}

Ne reprenez pas un nombre d'étapes universel, une valeur de guidance, un sampler, une force de
denoise, un chiffre de VRAM ou une plage de poids LoRA issus d'un autre workflow. Procédez plutôt ainsi :

1. exécutez la baseline publiée pour le checkpoint choisi ;
2. faites varier un seul paramètre pris en charge à la fois, sur les mêmes fixtures ;
3. mesurez la latence à froid et à chaud, le pic de mémoire, la reproductibilité et l'acceptation visuelle ;
4. évaluez séparément la préservation de la source pour un workflow d'édition ; et
5. publiez le tuple de versions retenu et les limites connues avec le job.

La quantification, la compilation et le déchargement mémoire sont des compromis d'exécution. Consultez
[[diffusion-inference-acceleration]] pour le justificatif requis avant de les combiner avec un workflow d'image.

## Compatibilité des adaptateurs {#adapter-compatibility}

Un adaptateur doit nommer le checkpoint de base exact et le chargeur pour lesquels il a été entraîné.
Des nombres de paramètres similaires ou un libellé commun « FLUX » ne constituent pas une preuve de
compatibilité. Testez un adaptateur seul avant de tester une combinaison, conservez son échelle et
son ordre de chargement dans le justificatif d'exécution, et rejetez une sortie si son contenu protégé
dérive.

Pour entraîner un nouvel adaptateur, appuyez-vous sur les recommandations actuelles propres au modèle,
comme la [documentation d'entraînement de FLUX.2 [klein]](https://docs.bfl.ai/flux_2/flux2_klein_training),
puis validez l'artefact obtenu dans le même pipeline d'inférence que celui qui le servira.

## Registre de publication {#release-record}

Conservez le manifeste du modèle, la référence de prompt ou d'image, le hash de sortie, la revue
d'acceptation, la décision de licence et toute métadonnée de marquage des sorties avec chaque exécution
approuvée. Cela rend observable une future mise à niveau du runtime ou du modèle, au lieu de modifier
silencieusement le comportement des images.

## Pages connexes {#related-pages}

- [[flux-klein-9b-architecture]]
- [[flux-klein-style-lora-system]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
