---
title: "PixVerse CLI — Génération en terminal"
category: projects
date: 2026-03-17
tags: [pixverse, pixverse-cli, project, terminal-generation]
aliases: ["PixVerse CLI"]
level: 2
source_sha256: 220e74f8bd162b6af8b18cb8ad78b7c06a714a5f8b38a38ee1dc25ac7228a818
translation: machine
translated_at: '2026-10-24'
---
# PixVerse CLI — Génération en terminal {#pixverse-cli-terminal-generation}

**Ligne de développement :** `project:pixverse-cli` · fil `terminal-generation`  
**Dernier événement :** 2026-03-17 · 1 événement daté depuis le 2026-03-17 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

PixVerse CLI est une interface en ligne de commande destinée aux abonnés PixVerse, permettant de générer des vidéos, des images et des fichiers audio à partir de prompts ou de fichiers de référence.

- Génération de médias à partir de prompts textuels et de fichiers de référence.
- Sortie JSON pour les scripts et les pipelines d'agents.
- Gestion des tâches et des ressources via des commandes CLI dédiées.

Nécessite Node.js 22.12+ ; la génération consomme des crédits de compte. Cet outil convient aux workflows d'automatisation, mais nous devons figer la version de la CLI et vérifier les crédits disponibles ainsi que les emplacements de concurrence libres avant de lancer des traitements par lots.

## Ligne de développement {#development-line}

- **2026-03-17 — PixVerse a introduit une interface de génération orientée terminal.** PixVerse a ouvert l'accès en ligne de commande à sa génération d'images et de vidéos le 2026-03-17. Une entrée ClawHub associée a diffusé cette interface pour les workflows en terminal. Le projet a fait passer la génération de l'accès web vers le terminal.

## Ce qui a changé {#what-changed}

2026-03-17 — PixVerse CLI a été associée à la génération de médias en terminal, mais ce lien ne confirme pas la date de publication.  
2026-03-31 — PixVerse a annoncé la CLI et la bibliothèque Skills pour les workflows des développeurs et des agents.  
2026-07-13 — Le guide pratique officiel a détaillé la vidéo, les images, la voix, la musique, la sortie JSON et les clés d'idempotence pour les pipelines de production.  
2026-09-05 — Le README officiel actuel précise Node.js 22.12+, un flux d'authentification OAuth par code d'appareil, V6 comme modèle vidéo par défaut, ainsi qu'une liste élargie de modèles pris en charge.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-17, nous pouvons utiliser PixVerse depuis le terminal pour la génération d'images et de vidéos, mais nous devons d'abord vérifier la configuration et les limites de production dans la documentation officielle.

1. Installez le paquet avec npm ou exécutez-le directement, puis vérifiez la version de la CLI.
  — <https://github.com/PixVerseAI/cli>
2. Exécutez `pixverse auth login`, terminez l'authentification OAuth dans le navigateur, puis vérifiez l'état avec `pixverse auth status`.
  — <https://github.com/PixVerseAI/cli>
3. Vérifiez les crédits et les emplacements de concurrence disponibles avec `pixverse account info` et `pixverse account slots` avant de mettre des lots en file d'attente.
  — <https://github.com/PixVerseAI/cli>
4. Générez des médias avec `pixverse create video` ou `pixverse create image` ; passez `--json` pour l'automatisation, conservez l'identifiant de tâche, attendez-la avec `pixverse task wait`, puis téléchargez-la avec `pixverse asset download`.
  — <https://github.com/PixVerseAI/cli>

## Bonnes pratiques {#best-practices}

- Définissez explicitement le modèle, la qualité, la durée et le format d'image, car les options prises en charge dépendent du mode et du modèle.
  — <https://github.com/PixVerseAI/cli>
- Passez `--idempotency-key` pour les nouvelles tentatives de traitement par lots, et utilisez `--no-wait` pour envoyer les tâches en parallèle, enregistrer leurs identifiants et les interroger par lots.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>
- Gardez `--json` activé dans les scripts et les exécutions d'agents afin que la sortie standard reste lisible par une machine, tandis que la progression et les erreurs restent séparées.
  — <https://github.com/PixVerseAI/cli>
- Exécutez `pixverse --version` et consultez `pixverse create <mode> --help` avant les exécutions volumineuses, et ne mettez à jour la CLI qu'après avoir vérifié les modifications.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-03-17 : nous ne pouvons pas considérer cette date comme la date de lancement confirmée ; l'annonce initiale de disponibilité date du 2026-03-31.
- 2026-09-05 : l'exigence Node.js 20 figurant dans la fiche Skills publiée est obsolète ; le README officiel actuel exige Node.js 22.12+.
- 2026-09-05 : ne couvrir que la vidéo et les images est incomplet ; la CLI actuelle documente également la voix, la musique, les tâches, les ressources et les espaces de travail.

## Points encore inconnus {#still-unknown}

- La source officielle ne confirme pas que le lien d'origine du 2026-03-17 ait été publié ce jour-là : le guide pratique actuel est daté du 2026-07-13, et l'annonce officielle de disponibilité de la CLI est datée du 2026-03-31.
- La fiche ClawHub indique Node.js 20+, alors que le README officiel actuel précise Node.js 22.12+ ; suivez le README ou l'aide du paquet installé pour l'installation.
- Le schéma de réponse du système ne comporte pas de champs distincts event_findings et new_events ; les précisions utiles figurent dans what_changed, supersedes et unknowns.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal | PixVerse CLI: Generate AI Videos and Images in Terminal | 2026-09-05 |
| https://clawhub.ai/PixVerse-Official/pixverse-ai-image-and-video-generator | PixVerse AI Image and Video Generator | 2026-09-05 |
| https://github.com/PixVerseAI/cli | PixVerseAI/cli — official command-line interface | 2026-09-05 |
| https://pixverse.ai/en/blog/pixverse-evolves-from-creation-tool-to-production-platform | PixVerse Evolves From Creation Tool to Production Platform With New Studio and Developer Releases | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:pixverse-cli`, fil `terminal-generation`, 1 événement daté du 2026-03-17 au 2026-03-17.
- **Note pratique :** Au 2026-03-17, les praticiens devraient envisager un workflow PixVerse en terminal pour la génération d'images et de vidéos, tout en confirmant la configuration, les opérations prises en charge et l'adéquation à la production dans la documentation officielle avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
