---
title: "CARLA-Air"
category: projects
date: 2026-04-03
tags: [carla-air, carla-air-release, carla_air_release, project]
aliases: ["CARLA-Air"]
level: 2
source_sha256: 2b54d89e3d6f89205047e89b7a6cc6d89988e49c682f938899430b295454882d
translation: machine
translated_at: '2026-10-24'
---
# CARLA-Air {#carla-air}

**Ligne de développement :** `project:carla-air` · fil `carla-air-release`  
**Dernier événement :** 2026-04-03 · 1 événement daté depuis le 2026-04-03 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

CARLA-Air est un environnement de simulation air-sol ouvert, destiné aux chercheurs en IA incarnée, en navigation, en perception et en apprentissage par renforcement.

- Monde unifié : combine acteurs aériens et terrestres dans une même simulation.
- Capteurs synchrones : capture simultanément les flux des deux plateformes.
- Deux API Python : CARLA pour les véhicules et AirSim pour les multirotors.

La version publique actuelle est la v0.1.7. Town10HD nécessite environ 8 Go de VRAM, et la calibration des coordonnées dépend de la carte. Cette approche est plus efficace que l'exécution de CARLA et d'AirSim en processus séparés lorsqu'un drone et une voiture doivent partager un même monde.

## Ligne de développement {#development-line}

- **2026-04-03 — Dépôt GitHub de CARLA-Air relié.** Le 2026-04-03, la ligne de développement de CARLA-Air a relié le dépôt GitHub du projet, louis zeng CN/CarlaAir. Cela fournit une référence publique datée pour le projet. Les éléments disponibles ne montrent ni version publiée, ni numéro de version, ni ensemble de modifications, ni contenu du dépôt.

## Modifications {#what-changed}

- 2026-03-19 — Version publique v0.1.6 : CARLA 0.9.16 et AirSim dans un processus unique, trafic automatique, bascule des collisions et plaquage au sol.
- 2026-03-24 — La version v0.1.7 corrige la stabilité de VSync et du trafic, et ajoute une installation en un clic, l'enregistrement des vols et la documentation des coordonnées ; la compatibilité avec les scripts et configurations de la v0.1.6 est préservée.
- 2026-04-03 — Lien du projet enregistré ; la source primaire ne contient aucune entrée de journal des modifications pour cette date, nous ne pouvons donc pas la considérer comme une nouvelle version.
- 2026-04-10 — Publication d'une branche de code source pour Windows.
- 2026-04-16 — Le paquet binaire précompilé v0.1.7 est disponible pour Windows 11 x86_64.
- 2026-04-17 — Publication du site web du projet.
- 2026-04-20 — Ajout d'exemples minimaux ROS 2 Humble pour les capteurs de voiture et de drone, avec RViz 2.

## Mode d'emploi {#how-to-use-this}

Au 2026-04-03, utilisez le dépôt GitHub relié comme source candidate pour CARLA-Air, en vérifiant son contenu et sa pertinence avant de vous y fier.

1. Téléchargez et décompressez le paquet précompilé Linux ou Windows ; pour une première exécution sous Linux, utilisez Ubuntu 20.04/22.04 pris en charge.
  — <https://github.com/louiszengCN/CarlaAir>
2. Dans le répertoire v0.1.7, exécutez `bash env_setup/setup_env.sh`, puis `bash env_setup/test_env.sh`, et activez l'environnement conda `carlaAir`.
  — <https://github.com/louiszengCN/CarlaAir/releases>
3. Exécutez `./CarlaAir.sh Town10HD` ; attendez que CARLA soit prêt sur localhost:2000 et AirSim sur localhost:41451.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>
4. Testez les deux API avec des clients distincts `carla.Client` et `airsim.MultirotorClient`, puis lancez `examples/quick_start_showcase.py`.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Bonnes pratiques {#best-practices}

- Conservez le mode asynchrone pour le contrôle interactif ; pour les jeux de données, la relecture et l'enregistrement, utilisez le mode synchrone à pas fixe et un Traffic Manager synchronisé.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Rétablissez toujours le monde en mode asynchrone dans `finally`, afin que le serveur ne reste pas bloqué sur `world.tick()` après la fin du script.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Recalibrez les décalages CARLA-AirSim lorsque vous changez de carte ; la formule de la version est calibrée pour Town10HD.
  — <https://github.com/louiszengCN/CarlaAir/releases>
- Commencez par une carte plus petite et une qualité ou un nombre d'acteurs réduits si la VRAM manque ou si les fréquences d'images chutent.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Remplacé par {#superseded-by-this}

- 2026-03-24 : la v0.1.7 remplace la v0.1.6 comme version courante ; effectuez la mise à jour dans un répertoire propre en relançant l'installation, plutôt que par-dessus une ancienne installation.
- 2026-04-16 : Windows dispose désormais d'un paquet précompilé ; un binaire Windows 11 x86_64 est disponible pour la v0.1.7.
- 2026-04-20 : la visualisation ROS 2 de base ne nécessite plus de compiler carla-ros-bridge à partir des sources ; les exemples du projet utilisent directement les API Python et rclpy. Le pont complet reste nécessaire uniquement pour ses actions, services et contrôle Ackermann supplémentaires.

## Points encore inconnus {#still-unknown}

- Le texte du message pour le 2026-04-03 n'est pas disponible ; le lien vers le dépôt ne prouve à lui seul ni une version publiée, ni une modification précise à cette date.
- Les sources primaires consultées ne fournissent aucun fait daté qui se rattache directement à l'événement du 2026-04-03.

## Sources {#sources}

| source | titre | consultée |
|---|---|---|
| https://github.com/louiszengCN/CarlaAir | CARLA-Air : faire voler des drones dans un monde CARLA | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/releases | Versions de CARLA-Air | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md | Guide de démarrage rapide de CARLA-Air | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md | FAQ de CARLA-Air | 2026-09-05 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:carla-air`, fil `carla-air-release`, 1 événement daté du 2026-04-03 au 2026-04-03.
- **Note pratique :** Au 2026-04-03, les praticiens peuvent utiliser le dépôt GitHub relié comme source candidate pour CARLA-Air, en vérifiant son contenu et sa pertinence avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
