---
title: "Cells2Pixels"
category: projects

tags: [cells2pixels, cells2pixels-development, project]
aliases: ["Cells2Pixels"]
level: 2
source_sha256: feaebfd250a4132359d5cfe06dbfadee738fce14323d5c2ab9f88a51885acbe3
translation: machine
translated_at: '2026-10-24'
---
# Cells2Pixels {#cells2pixels}

**Ligne de développement :** `project:cells2pixels` · fil `cells2pixels-development`  
**Dernier événement :** - · 0 événement daté depuis - · **Recherché :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Cells2Pixels est le code et la démo interactive de Neural Cellular Automata: From Cells to Pixels, destiné aux chercheurs en infographie générative.

- Le NCA et le Local Pattern Producing Network (LPPN) sont entraînés conjointement.
- Les modes principaux couvrent la morphogenèse 2D, les textures PBR, les textures sur maillages et les textures 3D.
- Les modes expérimentaux couvrent les textures dynamiques, le champ de radiance et la croissance de voxels.

Le dépôt est conçu pour l'entraînement, sans version packagée ni Colab prêt à l'emploi. Le README mentionne encore Colab et les tests comme des éléments à faire (TODO). Il convient à des expériences NCA reproductibles, et non à la génération d'images en production.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-11 — Cells2Pixels est paru comme implémentation de SIGGRAPH 2026. Une grille cellulaire grossière évolue par mises à jour locales. Le LPPN décode les états interpolés des cellules et les coordonnées locales en images ou en propriétés de surface, à une résolution arbitraire.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2026-07-11, considérez Cells2Pixels comme un projet qui nécessite une revue des sources via son site et son dépôt ; les liens datés seuls ne justifient aucune modification du flux de travail des praticiens.

1. Installez les dépendances avec `pip install -r requirements.txt`. Kaolin est optionnel pour les exécutions sans maillages.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
2. Téléchargez les jeux de données et les structures de répertoires d'entrée avec `python scripts/download_data.py`.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
3. Lancez l'entraînement avec `python train.py --config <path>`. Commencez par `configs/nca2d/growing.yaml` pour la croissance 2D, `configs/nca2d/pbr_texture.yaml` pour le PBR, `configs/meshnca/texture.yaml` pour les maillages, ou `configs/nca3d/3d_texture.yaml` pour la 3D.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
4. Ajoutez `--test` après l'entraînement pour charger le point de contrôle et enregistrer les images et les vidéos de déroulement dans le répertoire de sortie configuré.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
5. Testez le comportement du modèle dans le canevas interactif en choisissant un mode, en ajustant l'échelle du LPPN, puis en cliquant ou en touchant le NCA.
  — <https://cells2pixels.github.io/>

## Bonnes pratiques {#best-practices}

- Faites correspondre les versions de PyTorch et de Kaolin à celles de requirements. Kaolin n'est nécessaire que pour le rendu et la rastérisation de maillages.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Ne présentez pas la texture dynamique, la croissance par champ de radiance ou la croissance de voxels comme des résultats de l'article. Le README distingue ces modes expérimentaux des quatre modes d'entraînement de l'article.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Évaluez les modèles à partir d'un point de contrôle sauvegardé et d'un déroulement de test explicite, plutôt que de vous fier au seul run d'entraînement.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- La page du projet et le README ne fournissent aucun journal des modifications daté du dépôt ; les dates de publication du code, des démos et de configurations spécifiques ne peuvent donc pas être vérifiées.
- Aucune version packagée confirmée, aucun catalogue de points de contrôle et aucun flux de travail de production pris en charge n'existent à ce jour.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://cells2pixels.github.io/ | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |
| https://github.com/TheDevilWillBeBee/Cells2Pixels | TheDevilWillBeBee/Cells2Pixels — implémentation officielle | 2026-09-05 |
| https://arxiv.org/abs/2506.22899 | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:cells2pixels`, fil `cells2pixels-development`, 0 événement daté - → -.
- **Note pratique :** Depuis le 2026-07-11, considérez Cells2Pixels comme un projet qui nécessite une revue des sources via son site et son dépôt ; les liens datés seuls ne justifient aucune modification du flux de travail des praticiens.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
