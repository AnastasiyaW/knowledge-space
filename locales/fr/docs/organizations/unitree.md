---
title: "Unitree"
category: organizations

tags: [organization, unitree, unitree-development]
aliases: ["Unitree"]
level: 2
source_sha256: 272495f16804600e2afe61cedda5e51d4bde926bac4f2ebf11df2a9c4765a82e
translation: machine
translated_at: '2026-10-24'
---
# Unitree {#unitree}

**Ligne de développement :** `organization:unitree` · fil `unitree-development`  
**Dernier événement :** - · 0 événement daté depuis - · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Unitree conçoit du matériel et des logiciels pour le travail pratique avec le humanoïde G1, des robots quadrupèdes et des bras robotiques.

- Robots physiques : plateformes humanoïdes et quadrupèdes pour les tests en conditions réelles.
- SDK2 et DDS : communication programmatique et contrôle du robot.
- ROS et MuJoCo : environnements de simulation pour les contrôleurs.
- Téléopération et kits de politiques : outils de collecte de données et d'entraînement de politiques.

Le G1 EDU offre 23 à 43 degrés de liberté, environ 2 heures d'autonomie et un développement secondaire ; le G1 de base dispose de 23 degrés de liberté.
Il s'agit d'une plateforme pour l'intégration et les tests d'ingénierie sur du matériel réel, et non d'un travailleur autonome à usage général prêt à l'emploi.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-04-12 — Une vidéo publiée par Unitree n'a pas pu être attribuée de manière fiable à un modèle, une version ou une publication spécifique. La consultation disponible n'a renvoyé aucune métadonnée, nous ne pouvons donc pas développer ce fait.
- 2026-06-01 — Unitree a annoncé le H2 Plus comme robot humanoïde de référence pour la recherche académique avec NVIDIA Isaac GR00T. Il s'agit d'un événement distinct et postérieur, et non d'une clarification de la vidéo d'avril.
- 2026-09-05 — La page actuelle du G1 indique un prix de départ de 13 500 $. L'article d'actualité historique de 2024 indiquait un prix à partir de 16 000 $.

## Comment l'utiliser {#how-to-use-this}

Au 2026-04-12, n'apportez aucune modification de pratique sur la base de cette ligne tant que la vidéo liée n'a pas été recherchée et que ses faits d'événement n'ont pas été vérifiés.

1. Choisissez le modèle et le pack spécifiques. Le développement sur G1 requiert la variante EDU, car le G1 de base ne prend pas en charge le développement secondaire.
  — <https://www.unitree.com/g1/>
2. Connectez le robot au réseau en suivant les instructions officielles. Installez l'interface Python SDK2 et les dépendances Cyclone DDS, puis commencez par les exemples de statut et de contrôle.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
3. Testez le contrôleur dans le simulateur Unitree MuJoCo avant de le déployer sur le matériel. Utilisez les messages unitree_hg pour le G1, et non unitree_go.
  — <https://github.com/unitreerobotics/unitree_mujoco>
4. Utilisez la pile d'apprentissage par imitation publiée par Unitree pour entraîner et déployer des politiques. Elle couvre la collecte de données, le développement d'algorithmes, l'entraînement et la vérification sur G1.
  — <https://www.unitree.com/mobile/opensource/>

## Bonnes pratiques {#best-practices}

- Commencez par les exemples officiels de SDK2 et vérifiez le nom de l'interface réseau avant d'envoyer des commandes au robot.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
- Exécutez d'abord les boucles de contrôle dans MuJoCo. Sélectionnez explicitement les messages unitree_hg pour le G1.
  — <https://github.com/unitreerobotics/unitree_mujoco>
- Ne mélangez pas les modes de contrôle bas niveau et haut niveau sans vérifier l'état. Des rapports ouverts du SDK confirment des erreurs RPC et des conflits après l'exécution d'exemples bas niveau.
  — <https://github.com/unitreerobotics/unitree_sdk2_python/issues/39>

## Remplacé par ceci {#superseded-by-this}

- 2024-07-05 — Le chiffre historique de Unitree pour le G1, à partir de 16 000 $, n'est plus une référence de prix valable. La page actuelle du G1 indique des tarifs à partir de 13 500 $.

## Toujours inconnu {#still-unknown}

- La vidéo du 2026-04-12 n'a renvoyé aucun titre, auteur, date de publication ni description vérifiables depuis YouTube. Le modèle précis et la nature de l'événement restent inconnus.
- Unitree gère plusieurs lignes de produits. Sans métadonnées, nous ne pouvons pas attribuer la vidéo d'avril au G1, au H2, au H1, au R1 ou à un robot quadrupède.
- Le prix actuel à partir de 13 500 $ correspond à la page du G1. Il ne confirme pas le prix d'une configuration, d'une région, de l'expédition ou des taxes en particulier.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.youtube.com/watch?v=zoMDadPQLKA | Vidéo YouTube zoMDadPQLKA | 2026-09-05 |
| https://www.unitree.com/g1/ | Unitree G1 | 2026-09-05 |
| https://www.unitree.com/news/ | Centre d'actualités Unitree | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python | unitree_sdk2_python | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_mujoco | unitree_mujoco | 2026-09-05 |
| https://www.unitree.com/mobile/opensource/ | Open Source officiel | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python/issues/39 | Can't run g1 high_level example after running low_level examples | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `organization:unitree`, fil `unitree-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-04-12, n'apportez aucune modification de pratique sur la base de cette ligne tant que la vidéo liée n'a pas été recherchée et que ses faits d'événement n'ont pas été vérifiés.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
