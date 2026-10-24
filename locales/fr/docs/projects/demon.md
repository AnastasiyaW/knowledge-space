---
title: "DEMON"
category: projects
date: 2026-06-03
tags: [demon, project]
aliases: ["DEMON"]
level: 3
source_sha256: 4e07a151f080c0b7c7fc47ee1ebd16d9f2d2d24dd02cad902b60f4b1099362a6
translation: machine
translated_at: '2026-10-24'
---
# DEMON {#demon}

**Ligne de développement :** `project:demon` · fil `demon`  
**Dernier événement :** 2026-06-03 · 1 daté depuis 2026-06-03 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

DEMON transforme ACE-Step v1.5 en générateur et transformateur musical en temps réel sur GPU. C'est l'équivalent audio de StreamDiffusion, destiné aux interprètes, aux développeurs d'outils créatifs et aux chercheurs.

- La diffusion par tampon circulaire (ring-buffer) diffuse de l'audio finalisé tandis que l'audio source, les prompts, les LoRA et les courbes évoluent pendant la lecture.
- L'interface web expose le mélange de prompts, les références de timbre et de structure, l'automatisation, le mappage MIDI, l'enregistrement et une API de session.

## Ligne de développement {#development-line}

- **2026-06-03 — Ensemble des ressources publiques de DEMON documenté.** Le projet principal n'avait aucun enregistrement GitHub Releases. Le client TouchDesigner demonTD, versionné séparément, a publié les versions v0.2.11 et v0.2.12 pour des corrections liées aux sessions hébergées et au protocole socket.

## Ce qui a changé {#what-changed}

- 2026-04-22 : DreamVAE a été publié comme ressource autonome de décodeur pour ACE-Step.
- 2026-05-27 : l'article sur DEMON a publié le runtime à tampon circulaire et TensorRT, avec des mesures sur RTX 5090.
- 2026-06-02 : DreamVAE a été présenté comme faisant partie de la recherche sur DEMON, tout en restant une ressource limitée au décodeur.
- 2026-06-03 : le projet principal n'avait aucun enregistrement GitHub Releases ; le client TouchDesigner demonTD, versionné séparément, a publié les versions v0.2.11 et v0.2.12 pour des corrections liées aux sessions hébergées et au protocole socket.
- 2026-06-04 : demonTD v0.2.13 a ajouté un sélecteur de périphérique de sortie audio.
- 2026-06-09 : demonTD v0.2.15 a ajouté la gestion automatique des déclencheurs de LoRA et le câblage du prompt B. demonTD v0.2.16 a déplacé le travail de cadencement hors du thread de l'interface pour corriger les coupures audio.
- 2026-06-11 : demonTD v0.2.17 a regroupé les corrections de connexion et de fuite audio, et documenté l'installation du bundle.

## Mode d'emploi {#how-to-use-this}

1. Pour un essai sans installation, ouvrez l'instance hébergée sur music.daydream.live ; c'est la voie indiquée pour les utilisateurs sans GPU local.
  — <https://huggingface.co/daydreamlive/DEMON>
2. Pour un flux de travail web en local, utilisez un GPU NVIDIA, uv et environ 40 Go d'espace disque libre. Clonez daydreamlive/DEMON, exécutez `uv sync`, puis `uv run demon-setup` pour obtenir les ressources ACE-Step v1.5 prises en charge et construire des moteurs TensorRT minimaux.
  — <https://github.com/daydreamlive/DEMON>
3. Lancez `uv run python -u -m demos.realtime_motion_graph_web.run` et ouvrez http://localhost:6660. Si l'installation a ignoré les moteurs, utilisez `-- --accel compile` plutôt que le lancement par défaut en TensorRT intégral.
  — <https://github.com/daydreamlive/DEMON>
4. Chargez l'audio source, les prompts et les références facultatives dans l'interface web. Utilisez le mélange de prompts, l'intensité, les LoRA, les courbes, le MIDI ou l'enregistrement selon l'objectif de performance.
  — <https://huggingface.co/daydreamlive/DEMON>
5. Ajoutez les LoRA facultatives compatibles sous forme de fichiers .safetensors dans $ACESTEP_MODELS_DIR/loras/ (par défaut ~/.daydream-scope/models/demon/loras/) et ajustez leur intensité pendant la session en direct.
  — <https://huggingface.co/daydreamlive/DEMON>

## Bonnes pratiques {#best-practices}

- Conservez ensemble les points de contrôle ACE-Step v1.5 fournis et l'installation de DEMON ; ne remplacez pas les points de contrôle ou les chemins par des fichiers arbitraires pour une configuration TensorRT qui attend la structure de modèles figée.
  — <https://github.com/daydreamlive/DEMON>
- Commencez par le décodeur VAE fenêtré TensorRT associé à un décodeur compilé afin d'éviter la construction d'un moteur complet ; c'est la voie documentée et peu coûteuse vers le décodage en flux.
  — <https://huggingface.co/daydreamlive/DEMON>
- Reconstruisez les plans TensorRT après tout changement de GPU, de CUDA, de pilote ou de version de TensorRT, car les plans dépendent du matériel et de la version.
  — <https://github.com/daydreamlive/DEMON>
- Traitez les changements de prompt, de source et de débruitage scalaire comme des commandes à tampon circulaire : effectuez-les délibérément et jugez l'audio après leur propagation, plutôt que d'attendre que chaque commande soit audible dans le même cycle.
  — <https://daydreamlive.github.io/DEMON/>
- Si vous utilisez DreamVAE séparément, associez son décodeur à l'encodeur ACE-Step standard ; seul le décodeur est distillé.
  — <https://huggingface.co/daydreamlive/DreamVAE>
- Pour l'intégration TouchDesigner, installez le ZIP de la version avec demonTD.tox à côté de son répertoire vendor ; le fichier .tox seul ne convient qu'à une installation disposant déjà des dépendances correspondantes.
  — <https://github.com/daydreamlive/demonTD>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-06-04 : pour demonTD, les instructions utilisant Edit -> Preferences -> Audio -> Audio Device -> None sont obsolètes. demonTD v0.2.13 indique que ce réglage n'existe pas et fournit un sélecteur de périphérique de sortie audio. Source : https://github.com/daydreamlive/demonTD/releases
- 2026-06-09 : pour demonTD, considérer qu'une LoRA sélectionnée est automatiquement effective sans son mot-clé de déclenchement est obsolète. demonTD v0.2.15 ajoute en tête les déclencheurs principaux enregistrés et renvoie le prompt lorsque la LoRA change. Source : https://github.com/daydreamlive/demonTD/releases

## Points encore inconnus {#still-unknown}

- Aucune version officielle GitHub Release du moteur principal n'identifie le 2026-06-03 comme une version numérotée de DEMON. Il ne faut pas considérer cette date comme la date de sortie du modèle ou du runtime principal.
- L'URL Civitai https://civitai.com/models/2416425/acestep-loras n'a fourni aucune fiche de modèle vérifiable pendant la recherche. Les fichiers exacts, versions, dates, déclencheurs et compatibilité avec DEMON restent non vérifiés ; traitez ces LoRA comme des ressources externes facultatives et non comme une dépendance par défaut.
- La licence publiée du code principal est AGPL-3.0-or-later, tandis que la fiche Hugging Face de DEMON et la page du projet indiquent MIT. Les sources ne réconcilient pas cette différence ; confirmez la licence de distribution applicable avant toute modification, déploiement réseau ou redistribution.
- La page du projet Daydream décrit la base XL Turbo comme étant de 5B, alors que le dépôt ACE-Step en amont décrit son DiT XL comme étant de 4B. Les sources n'expliquent pas l'écart de nombre de paramètres.
- Les chiffres de performance sont des mesures RTX 5090 rapportées par les auteurs, dans les conditions indiquées de 60 secondes, TensorRT, profondeur et nombre d'étapes. Aucun benchmark indépendant multi-matériel ni plancher universel de latence ou de VRAM n'a été trouvé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://daydreamlive.github.io/DEMON/ | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://music.daydream.live/ | Daydream Demo | 2026-09-06 |
| https://github.com/daydreamlive/DEMON | daydreamlive/DEMON | 2026-09-06 |
| https://github.com/daydreamlive/DEMON/releases | Releases · daydreamlive/DEMON | 2026-09-06 |
| https://huggingface.co/daydreamlive/DEMON | daydreamlive/DEMON model card | 2026-09-06 |
| https://arxiv.org/abs/2605.28657 | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE | daydreamlive/DreamVAE model card | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/53e74f7ed07cd053680fc2aa2b072124c63528d0 | DreamVAE initial release | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/abb4c6d9913df0aedd685fed2e2f5aef3d742707 | DreamVAE: add links to paper, project page, and code repository | 2026-09-06 |
| https://github.com/daydreamlive/demonTD | daydreamlive/demonTD | 2026-09-06 |
| https://github.com/daydreamlive/demonTD/releases | Releases · daydreamlive/demonTD | 2026-09-06 |
| https://huggingface.co/ACE-Step/Ace-Step1.5 | ACE-Step/Ace-Step1.5 model card | 2026-09-06 |
| https://github.com/ACE-Step/ACE-Step-1.5 | ACE-Step/ACE-Step-1.5 | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:demon`, fil `demon`, 1 événement daté du 2026-06-03 au 2026-06-03.
- **Remarque pratique :** voir les sections sourcées d'usage et de bonnes pratiques ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
