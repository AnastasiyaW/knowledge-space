---
title: "SHELLS"
category: projects

tags: [google-shells, project, shells]
aliases: ["SHELLS"]
level: 2
source_sha256: 9e608c92aa11aa41c79e197f190834063a46c456657d6a20d06833549b26b2e9
translation: machine
translated_at: '2026-10-24'
---
# SHELLS {#shells}

**Ligne de développement :** `project:google-shells` · fil `shells`  
**Dernier événement :** - · 0 daté depuis - · **Recherché :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

SHELLS est une méthode de recherche destinée aux équipes de capture 3D : à partir d'images calibrées provenant de plusieurs caméras, elle construit une tête à topologie fixe et à correspondance sémantique dense. — DINOv2 avec LoRA extrait les caractéristiques ; — une grille grossière guide les couches d'échantillonnage le long des normales ; — un transformeur commun prédit le maillage final. Mesure : 18k sommets en 0,08 s et environ 2,4 GB de mémoire d'inférence déclarée, contre 20 GB pour les méthodes volumétriques de référence. Conclusion : il s'agit d'une spécification pour reproduire et évaluer la capture, et non d'un SDK public prêt à l'emploi.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-21 — SHELLS a formalisé le passage d'une retouche volumétrique locale des sommets à un échantillonnage de surface en deux étapes guidé par une grille grossière : d'abord la grille grossière, puis des couches de points autour d'elle, pour une reconstruction unique et cohérente à 18k sommets.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-21, ne modifiez aucune pratique sur la seule base de cette ligne : conservez les liens vers SHELLS et Google GNM comme pistes à vérifier ultérieurement, avant de vous appuyer sur l'un ou l'autre projet, ou sur leur relation.

1. Commencez uniquement par une capture multi-caméras calibrée : la méthode a besoin des images et des paramètres de caméra pour l'échantillonnage projectif des caractéristiques.
  — <https://arxiv.org/html/2605.31283v1>
2. Pour une reproduction autonome, implémentez l'ordre décrit : DINOv2 avec LoRA, graphe global épars, grille grossière, puis couches de points à ±4 mm le long des normales, et transformeur commun.
  — <https://arxiv.org/html/2605.31283v1>
3. Évaluez séparément la correspondance sémantique V2V et la proximité géométrique au scan P2S : ces métriques peuvent diverger.
  — <https://arxiv.org/html/2605.31283v1>
4. Ne prévoyez pas de lancer le projet depuis le dépôt GitHub officiel de SHELLS : il contient le code du site du projet, et non l'implémentation du modèle ni les points de contrôle.
  — <https://github.com/syntec-research/SHELLS>

## Bonnes pratiques {#best-practices}

- Vérifiez la calibration, y compris les paramètres intrinsèques, extrinsèques et les distorsions de l'objectif ; la méthode utilise les paramètres de caméra connus et ne résout pas la géométrie à partir d'une seule image.
  — <https://arxiv.org/html/2605.31283v1>
- N'utilisez pas une image unique comme entrée standard : les auteurs qualifient la reconstruction à partir d'une seule vue de problème mal posé ; la robustesse n'est démontrée qu'à partir de deux vues.
  — <https://arxiv.org/html/2605.31283v1>
- Ne présentez pas le maillage comme un actif finaux photoréaliste : les rides fines et les pores sont absents, et ils nécessitent une couche distincte de displacement maps et de textures.
  — <https://arxiv.org/html/2605.31283v1>
- Testez séparément les articulations extrêmes de la langue et la géométrie externe des cheveux ou de la barbe : d'après les limitations publiées, ces cas ne sont pas couverts de manière fiable.
  — <https://arxiv.org/html/2605.31283v1>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Le code public, les poids, la licence du modèle et le script d'inférence reproductible de SHELLS n'ont pas été trouvés : le dépôt officiel de SHELLS est explicitement décrit comme le dépôt du site.
- Les deux URL sources renvoient à des ressources différentes : SHELLS renvoie à l'article et au site de reconstruction, GNM au modèle paramétrique de tête. Le texte de l'article ne mentionne pas GNM ; leur lien technique, au-delà des auteurs communs et de Google, n'est donc pas confirmé.
- Le protocole de préparation des données réelles en dehors de la capture à 13 caméras décrite par les auteurs n'est pas publié ; le transfert vers une prise de vue par téléphone ou non calibrée n'est donc pas confirmé.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://arxiv.org/html/2605.31283v1 | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://syntec-research.github.io/SHELLS/ | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/syntec-research/SHELLS | GitHub - syntec-research/SHELLS: Website repository for the project SHELLS | 2026-09-05 |
| https://arxiv.org/abs/2605.31283v1 | arXiv:2605.31283v1 — Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/google/GNM/tree/main | GitHub - google/GNM: An open ecosystem of parametric human models and perception stacks, starting with GNM Head | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:google-shells`, fil `shells`, 0 événement daté - → -.
- **Note pratique :** Au 2026-07-21, ne modifiez aucune pratique sur la seule base de cette ligne : conservez les liens vers SHELLS et Google GNM comme pistes à vérifier ultérieurement, avant de vous appuyer sur l'un ou l'autre projet, ou sur leur relation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
