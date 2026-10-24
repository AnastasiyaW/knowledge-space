---
title: "FASTER"
category: projects
date: 2026-03-20
tags: [faster, project]
aliases: ["FASTER"]
level: 2
source_sha256: 08c77261c2f7dc624dc5a41ccdb7f452fa291e6ddb44fcffb37cdb67e37156ac
translation: machine
translated_at: '2026-10-24'
---
# FASTER {#faster}

**Ligne de développement :** `project:faster` · fil `faster`  
**Dernier événement :** 2026-03-20 · 1 événement daté depuis le 2026-03-20 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

FASTER est une méthode open source d'échantillonnage à action rapide et de déploiement en streaming, destinée aux équipes qui affinent des politiques Vision-Language-Action à flux (flow VLA), et non une politique robotique autonome.

- Le Horizon-Aware Schedule (HAS) privilégie les actions à court terme.
- Le chemin de streaming client-serveur envoie les actions précoces pendant que les actions ultérieures sont affinées.
- Le code actuel s'appuie sur JAX openpi et documente les workflows π0.5 et AgileX Piper.

## Ligne de développement {#development-line}

- **2026-03-20 — Le site web public et le dépôt de FASTER ont été reliés.** Le dépôt public a enregistré deux mises à jour du README pour documenter l'état du projet et de l'article.

## Ce qui a changé {#what-changed}

2026-03-19 : l'article FASTER est entré sur arXiv en version v1. 2026-03-20 : le dépôt public a enregistré deux mises à jour du README pour documenter l'état du projet et de l'article. 2026-04-29 : la version arXiv v2 est apparue sans journal de modifications techniques. 2026-04-30 : FASTER v1.0 a publié en open source l'implémentation officielle. 2026-05-16 : la version arXiv v3 est devenue la version actuelle de l'article, sans note de révision.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-03-20, utilisez le site web public de FASTER et le dépôt GitHub pour la documentation du projet et l'accès aux sources ; nous n'avons vérifié aucune autre affirmation d'usage ou de publication.

1. Partez d'un workflow de politique à flux JAX openpi et d'une plateforme robotique déjà cartographiée ; utilisez `pi05_faster_agilex` comme référence maintenue plutôt que de traiter FASTER comme une politique autonome pré-entraînée.
  — <https://github.com/innovator-zero/FASTER>
2. Clonez le dépôt avec ses sous-modules, puis créez l'environnement uv documenté avec `GIT_LFS_SKIP_SMUDGE=1 uv sync` et `GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .`.
  — <https://github.com/innovator-zero/FASTER>
3. Préparez un jeu de données LeRobot v2.1 et la correspondance des entrées/sorties de la plateforme, puis calculez les statistiques de normalisation pour la configuration FASTER.
  — <https://github.com/innovator-zero/FASTER>
4. Affinez π0.5 avec `pi05_faster_agilex` et pointez le serveur de politique vers le checkpoint obtenu.
  — <https://github.com/innovator-zero/FASTER>
5. Lancez le serveur de politique et le client contrôleur du robot via WebSocket ; sélectionnez l'inférence HAS asynchrone ou l'inférence en streaming selon l'exigence de temps de réaction de la tâche.
  — <https://github.com/innovator-zero/FASTER>

## Bonnes pratiques {#best-practices}

- Maîtrisez le workflow openpi d'origine avant d'adapter FASTER.
  — <https://github.com/innovator-zero/FASTER>
- Conservez les paramètres d'inférence HAS `alpha` et `u0` identiques à ceux utilisés pendant l'entraînement.
  — <https://github.com/innovator-zero/FASTER>
- Réglez le délai du contrôleur à un pas au-dessus du délai d'inférence mesuré pour couvrir les variations d'exécution et du réseau, et gardez l'horizon d'exécution au moins égal au délai.
  — <https://github.com/innovator-zero/FASTER>
- Utilisez un réseau local filaire pour l'inférence à distance afin de réduire la latence et la perte de paquets.
  — <https://github.com/innovator-zero/FASTER>
- Réservez le streaming avec un petit horizon d'exécution aux tâches très dynamiques ; sur des tâches ordinaires de type pick-and-place ou pliage, il peut introduire des tremblements de mouvement.
  — <https://github.com/innovator-zero/FASTER>
- Respectez les limites de mémoire documentées et la frontière actuelle : le fine-tuning complet de π0.5 a été testé sous Ubuntu 22.04, et l'entraînement multi-nœuds n'est pas pris en charge.
  — <https://github.com/innovator-zero/FASTER>

## Ce qui est remplacé {#superseded-by-this}

- 2026-04-30 : la publication open source v1.0 a remplacé l'état antérieur où FASTER n'avait aucune implémentation publique.
- 2026-05-16 : la version arXiv v3 a remplacé la version arXiv v1 comme texte actuel de l'article.

## Points restant inconnus {#still-unknown}

- Les documents officiels ne fournissent ni téléchargement de checkpoint ni procédure complète de reproduction pour la configuration de tennis de table en robotique réelle rapportée ; la documentation suppose des checkpoints entraînés localement.
- arXiv horodate les versions v2 et v3 sans journal de modifications techniques, de sorte que leurs écarts exacts par rapport à la v1 restent inconnus.
- Nous n'avons trouvé aucune documentation technique en chinois simplifié de première main ; les explications en chinois disponibles sont secondaires.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://innovator-zero.github.io/FASTER/ | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://arxiv.org/abs/2603.19199 | [2603.19199] FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/commits/main | Commits · innovator-zero/FASTER | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/releases/tag/v1.0 | Release FASTER Open-source · innovator-zero/FASTER | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:faster`, fil `faster`, 1 événement daté du 2026-03-20 au 2026-03-20.
- **Note pratique :** Depuis le 2026-03-20, utilisez le site web public de FASTER et le dépôt GitHub comme points de départ pour la documentation du projet et l'accès aux sources ; nous n'avons vérifié aucune autre affirmation d'usage ou de publication.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
