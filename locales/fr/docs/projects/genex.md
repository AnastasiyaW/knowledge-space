---
title: "GeneX"
category: projects
date: 2024-12-16
tags: [genex, genex-development, project]
aliases: ["GenEx", "GeneX"]
level: 2
source_sha256: c00987acc5928b0371ac57519eb7fa5f5e5e4c139a0ecc7085235f669af22712
translation: machine
translated_at: '2026-10-24'
---
# GeneX {#genex}

**Ligne de développement :** `project:genex` · fil `genex-development`  
**Dernier événement :** 2024-12-16 · 2 événements datés depuis 2024-11-20 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

GeneX est un pipeline de recherche pour le prototypage d'IA incarnée et de modèles du monde. Il crée un panorama à 360° à partir d'une seule image, génère une vidéo panoramique prospective, fait pivoter la vue et exporte des clips d'exploration. La paire publiée comprend un initialiseur BF16 de 12 B et un explorateur FP16 de 2 B ; la démonstration interactive publique est suspendue. À utiliser pour des expériences en monde simulé, et non pour un déploiement de navigation dans le monde réel.

## Ligne de développement {#development-line}

- **2024-11-20 — GeneX a partagé une démonstration interactive.** Le 2024-11-20, GeneX a publié un lien vers une démonstration interactive du projet, comme première étape publique permettant une prise en main.
- **2024-12-16 — GeneX a publié le site web du projet.** Le 2024-12-16, GeneX a publié le lien vers le site web du projet et a renvoyé au message de projet précédent, établissant un point d'entrée public après la démonstration interactive.

## Ce qui a changé {#what-changed}

2024-11-20 — Generative World Explorer a présenté une exploration interactive d'un environnement généré en vidéo, conditionné par un panorama.  
2024-12-16 — GenEx a ajouté l'étape d'initialisation du monde qui manquait : une image RGB unique et une description facultative deviennent un panorama à 360° avant l'exploration vidéo panoramique conditionnée par les actions.  
Constat à la date de recherche — l'implémentation officielle actuelle est un workflow local à deux modèles, dont les fiches de modèle ont été mises à jour le 2025-05-06.

## Comment l'utiliser {#how-to-use-this}

À partir du 2024-11-20, les praticiens pouvaient utiliser GeneX via la démonstration interactive liée ; à partir du 2024-12-16, ils pouvaient également utiliser le site web du projet comme point d'entrée public.

1. Créez un environnement Python CUDA et installez les dépendances d'inférence indiquées par le projet, notamment Diffusers, Transformers, PyTorch, Pillow et les paquets d'export vidéo.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
2. Chargez World Initializer avec une image en perspective ; il produit un panorama équirectangulaire de 2048×1024, avec une invite textuelle facultative pour l'initialisation.
  — <https://huggingface.co/genex-world/World-Initializer-image-to-panorama>
3. Chargez World Explorer, définissez le panorama généré comme image courante et générez un segment vidéo prospectif avec le pipeline Explorer.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
4. Répétez les déplacements vers l'avant et les rotations du panorama pour explorer un parcours, puis exportez le résultat en MP4 ou en GIF. Utilisez des GPU locaux, car la démonstration interactive hébergée est actuellement suspendue.
  — <https://github.com/GenEx-world/genex>

## Bonnes pratiques {#best-practices}

- Suivez les deux étapes dans l'ordre : Explorer attend un panorama à 360°, il faut donc l'initialiser d'abord plutôt que de fournir à Explorer une image en perspective ordinaire.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
- Partez de la configuration de référence documentée pour Explorer — 1024×512, 25 images, 30 étapes d'inférence et augmentation de bruit de 0,02 — avant de modifier les réglages.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
- Limitez les déplacements proches d'obstacles : l'article indique que les commandes qui rapprochent excessivement d'un mur peuvent dégrader les images générées ensuite.
  — <https://arxiv.org/html/2412.09624v4>
- Pour tout workflow d'IA incarnée dans le monde réel, traitez les vues générées comme des a priori simulés et conservez une vérification par capteurs ; le transfert simulation-réel, l'intégration des capteurs, les conditions dynamiques et les garde-fous restent des défis ouverts.
  — <https://arxiv.org/html/2412.09624v4>

## Remplacé par ceci {#superseded-by-this}

- 2024-11-20 — les recommandations d'implémentation qui partent d'un panorama déjà disponible sont incomplètes pour le système GeneX ultérieur ; l'extension de décembre ajoute l'initialisation du monde à partir d'une image en panorama avant l'exploration.

## Inconnues {#still-unknown}

- Les travaux de novembre et de décembre sont liés : l'article de décembre se présente explicitement comme une extension des travaux de novembre. Cependant, aucune note de migration de l'éditeur ne fait correspondre l'instantané de la démonstration interactive de 2024 à une étiquette de code ou à un point de contrôle actuel.
- Aucune exécution locale n'a été réalisée. La mémoire GPU requise, la reproductibilité de la démonstration complète et la compatibilité avec les versions actuelles de CUDA et de Diffusers restent non vérifiées.
- Aucune documentation utilisateur officielle en chinois simplifié n'a été trouvée dans les sources consultées ; les retours d'expérience pratiques en chinois n'ont pas été utilisés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://generative-world-explorer.github.io/#interactive_demo | Generative World Explorer | 2026-09-04 |
| https://www.genex.world/ | Generative World Explorer | 2026-09-04 |
| https://arxiv.org/abs/2411.11844 | Generative World Explorer | 2026-09-04 |
| https://arxiv.org/abs/2412.09624 | GenEx: Generating an Explorable World | 2026-09-04 |
| https://arxiv.org/html/2412.09624v4 | GenEx: Generating an Explorable World | 2026-09-04 |
| https://github.com/GenEx-world/genex | GenEx-world/genex | 2026-09-04 |
| https://github.com/GenEx-world/genex/tree/main/code/inference | GenEx inference documentation | 2026-09-04 |
| https://huggingface.co/genex-world/World-Initializer-image-to-panorama | genex-world/World-Initializer-image-to-panorama | 2026-09-04 |
| https://huggingface.co/genex-world/GenEx-World-Explorer | genex-world/GenEx-World-Explorer | 2026-09-04 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:genex`, fil `genex-development`, 2 événements datés du 2024-11-20 au 2024-12-16.
- **Note pratique :** À partir du 2024-11-20, les praticiens pouvaient utiliser GeneX via la démonstration interactive liée ; à partir du 2024-12-16, ils pouvaient également utiliser le site web du projet comme point d'entrée public.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
