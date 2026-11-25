---
title: "Inline Studio"
category: projects
date: 2026-08-16
tags: [inline-studio, inline-studio-development, inlineresearch/inline-studio, project]
aliases: ["Inline Studio"]
level: 3
source_sha256: 08c66da8fd26412d9bb0402095ad90f6ebfd9e179fa1069c8fa1f01387034ff2
translation: machine
translated_at: '2026-10-24'
---
# Inline Studio {#inline-studio}

**Ligne de développement :** `project:inline-studio` · fil `inline-studio-development`  
**Dernier événement :** 2026-08-16 · 1 événement daté depuis le 2026-08-16 · **Recherche :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Inline Studio est un espace de travail open source pour la génération d'images et de vidéos centrée sur les personnages. Il combine un canevas de nœuds, des fichiers `.char` portables, l'entraînement local de LoRA, des nœuds de modèles et un historique des prises.

- Génération de personnages cohérents à travers les nœuds de modèles.
- Génération sur GPU local et via des nœuds API.
- Entraînement de LoRA sur matériel local.
- Workflows réutilisables sur un canevas de nœuds.
- Historique des prises avec versions des rendus.

L'entraînement local documenté atteint de 8,6 Go à 13,4 Go de VRAM pour plusieurs chemins de modèles en 512 px ; LTX-2.5 nécessite 48 Go.

Utilisez-le lorsque la continuité du personnage et un workflow local par graphe comptent davantage qu'un générateur d'images ponctuel.

## Ligne de développement {#development-line}

- **2026-08-16 — Inline Studio a publié la version v1.2.71.** Le 2026-08-16, Inline Studio a publié la version GitHub v1.2.71. La version renvoyait vers la page des personnages comme point de contrôle de version, sans détailler le contenu précis de la publication.

## Changements {#what-changed}

2026-08-16 — La version v1.2.71 permet aux nœuds de génération FLUX.2 de sélectionner des fichiers `.char` portables sans entraînement de LoRA ni adaptateur.

2026-08-21 — La version v1.3.0 a fusionné l'entraînement avec la génération et refondu le graphe de nœuds. Un seul fichier `.char` contient désormais les charges de modèles pour FLUX.2 et Krea 2.

2026-08-25 — La version v1.3.11 a ajouté la prise en charge de `.char` aux nœuds MiniMax H3 de texte vers vidéo, d'image vers vidéo et de référence vers vidéo.

2026-08-30 — La version v1.3.13 a ajouté des références de corps et de vêtements aux personnages, et protégé l'historique des prises contre les écritures obsolètes du navigateur.

2026-09-03 — La version v1.3.15 a étendu la prise en charge des personnages aux nœuds API, dont MiniMax, Seedance et Nano Banana.

## Mode d'emploi {#how-to-use-this}

Considérez Inline Studio v1.2.71 comme un point de contrôle de version daté du 2026-08-16. Consultez la page des personnages pour les fonctionnalités liées aux personnages, car les liens ne donnent aucune indication de migration.

1. Installez Python 3.11+ et clonez le dépôt. Exécutez `webui.bat --install --extra all` sous Windows ou `./webui.sh --install --extra all` sous macOS/Linux, puis lancez l'interface locale.
  — <https://github.com/inlineresearch/Inline-Studio/blob/main/README.md>
2. Créez un personnage à partir d'une photo ou d'une prise existante dans le panneau Personnages. Inline Studio enregistre un fichier `.char` portable dans `models/characters`.
  — <https://inlinestudio.art/characters>
3. Sélectionnez ce personnage dans un nœud de génération compatible. Exécutez le graphe et inspectez le score de continuité enregistré pour chaque prise.
  — <https://inlinestudio.art/characters>

## Bonnes pratiques {#best-practices}

- Utilisez des angles de référence variés plutôt que de nombreuses images de face. Les références sont appariées indépendamment, et chacune ajoute des jetons d'inférence.
  — <https://inlinestudio.art/characters>
- Réservez les workflows de personnages aux plans centrés sur une seule personne. Dans les scènes à plusieurs personnes, l'identité peut se propager à d'autres visages alors que le score indique tout de même une correspondance.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>
- Considérez le score de continuité comme un outil de diagnostic, et non comme une preuve de scène de foule correcte. Le score correspond à 0,8 de similarité faciale plus 0,2 de similarité du sujet. Il bascule sur la seule similarité du sujet lorsqu'aucun visage n'est visible.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>

## Remplacé par cette version {#superseded-by-this}

- 2026-08-21 — La version v1.3.0 a remplacé le format réservé à FLUX.2 de la v1.2.71 par un format `.char` unifié pour FLUX.2 et Krea 2.
- 2026-08-25 — La version v1.3.11 a remplacé le workflow de personnages limité aux modèles d'images, pour les nœuds MiniMax H3.
- 2026-09-03 — La version v1.3.15 a remplacé la prise en charge des personnages limitée aux nœuds de modèles locaux, en l'étendant aux nœuds API pris en charge.

## Points encore inconnus {#still-unknown}

- GitHub date la version v1.2.71 du 2026-08-15, alors que notre date d'événement est le 2026-08-16. Nous conservons le 2026-08-16 comme date d'événement et notons le 2026-08-15 à titre de contexte.
- La page des personnages couvre FLUX.2 et Krea 2, tandis que les notes de version ajoutent MiniMax H3 et certains nœuds API. La parité avec les autres modèles n'est pas vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71 | Version v1.2.71 - Personnages cohérents, sans entraîner de LoRA (Flux uniquement) | 2026-09-05 |
| https://inlinestudio.art/characters | Personnages portables : un seul fichier pour FLUX.2 et Krea 2 | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/releases | Versions d'Inline Studio | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/blob/main/README.md | README d'Inline Studio | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:inline-studio`, fil `inline-studio-development`, 1 événement daté du 2026-08-16 au 2026-08-16.
- **Note pratique :** Considérez Inline Studio v1.2.71 comme un point de contrôle de version daté du 2026-08-16. Consultez la page des personnages pour les fonctionnalités liées aux personnages ; les liens ne donnent aucune indication de migration.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
