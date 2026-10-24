---
title: "Karpathy Output Style : karpathy-output-style-visual-explanations — Karpathy Output Style, explications visuelles"
category: "projects"
date: 2026-10-22
tags: ["karpathy-output-style", "karpathy-output-style-visual-explanations", "project"]
aliases: ["Karpathy Output Style: karpathy-output-style-visual-explanations"]
level: 2
source_sha256: 238eb7e56d23e73ae50b9b56007a64e45b04c4ca174e6c003d9c31d3bc22b713
translation: machine
translated_at: '2026-10-24'
---
# karpathy-output-style : explications visuelles {#karpathy-output-style-visual-explanations}

**Fil d'évolution :** project:karpathy-output-style · thread karpathy-output-style-visual-explanations  
**Dernier événement :** 2026-10-22 · 2 événements datés depuis le 2026-10-22 · **Recherche effectuée le :** 2026-10-23 · confiance : élevée

## Présentation {#what-it-is}

karpathy-output-style est un outil open source et une compétence de prompt destinés aux développeurs qui utilisent des assistants de programmation par IA tels que Claude Code et Codex. Il rend le raisonnement du modèle plus facile à inspecter en présentant chaque réponse selon l'un de quatre formats :

- Anglais technique simplifié, dérivé de la norme ASD-STE100.
- Diagrammes Excalidraw modifiables pour l'architecture système.
- Pages HTML interactives autonomes en un seul fichier, avec curseurs de paramètres.
- Animations explicatives programmatiques avec narration vocale.

Les pages HTML interactives et les vidéos nécessitent un environnement d'exécution de rendu externe ou un navigateur. L'outil ne remplace pas le raisonnement propre du modèle. Il offre un moyen pratique d'inspecter une sortie complexe sans avoir à lire de longs textes.

## Fil d'évolution {#development-line}

- **2026-10-22 — karpathy-output-style permet aux utilisateurs de demander des explications visuelles produites par un LLM.** La chaîne d'IA R77 a signalé qu'un développeur avait découvert le projet open source. Il permet de demander à un LLM des diagrammes, des pages HTML interactives ou de courtes vidéos. L'outil suit l'approche de format de sortie récemment proposée par Andrej Karpathy.
- **2026-10-22 — Des diagrammes et des vidéos à la place de longues réponses textuelles.** Un second article publié le même jour décrivait le projet de la même manière : un LLM renvoie des diagrammes, des pages HTML interactives ou des vidéos au lieu de longs textes. Le projet était présenté comme suivant l'approche de format de sortie récemment proposée par Karpathy.
- **2026-10-22 — autres informations publiées à cette date.**
  - Le dépôt open source d'Ashrya Aggarwal regroupe l'échelle de sorties de Karpathy en compétences modulaires pour agents d'IA, destinées aux assistants de programmation comme Claude Code et Codex. Il définit une progression en 4 niveaux : anglais technique ASD-STE100, diagrammes Excalidraw, bacs à sable HTML interactifs et clips vidéo narrés. (2026-10-22) — <https://github.com/ashryaagr/karpathy-output-style>
  - L'outil suit un flux de travail structuré : comprendre, choisir le format le plus simple, vérifier, produire. Il utilise Excalidraw pour les diagrammes, du HTML/Canvas autonome pour les curseurs, et des services de synthèse vocale comme ElevenLabs pour la narration des vidéos. (2026-10-22) — <https://github.com/ashryaagr/karpathy-output-style>

## Ce qui a changé {#what-changed}

Le dépôt a transformé la proposition de Andrej Karpathy, une échelle d'explication à plusieurs niveaux, en compétences d'agent reproductibles. Il définit quatre niveaux croissants : prose technique contrôlée, diagrammes Excalidraw, bacs à sable HTML autonomes et vidéo narrée. L'intégration avec les environnements en ligne de commande des agents a été documentée plus tard, afin que les modèles puissent choisir un format visuel en fonction de la complexité de la requête.

## Comment l'utiliser {#how-to-use-this}

1. Clonez le dépôt karpathy-output-style, ou copiez le fichier de définition de la compétence dans le répertoire de configuration de l'agent.
  — <https://github.com/ashryaagr/karpathy-output-style>
2. Configurez l'environnement d'exécution de l'agent \(tel que Claude Code ou Codex\) pour qu'il charge les règles de la compétence pendant l'exécution de la requête.
  — <https://github.com/ashryaagr/karpathy-output-style>
3. Donnez à l'agent un concept ou un morceau de code à expliquer. La compétence choisit entre un texte technique simplifié, des diagrammes Excalidraw, du HTML interactif ou une vidéo explicative.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Bonnes pratiques {#best-practices}

- Respectez l'échelle à quatre niveaux : commencez par le format le plus simple avant de demander du HTML interactif ou une vidéo, plus lourds à produire.
  — <https://github.com/ashryaagr/karpathy-output-style>
- Conservez le HTML interactif dans un seul fichier autonome, avec styles et scripts intégrés, afin qu'il s'ouvre immédiatement dans un navigateur local.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Remplacé par {#superseded-by-this}

- Du texte brut non structuré, en plusieurs paragraphes, comme réponse par défaut pour les explications d'architecture technique et d'algorithmes.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Points inconnus {#still-unknown}

- Le résumé du dépôt ne donne ni étiquettes de version ni numéros de version pour le commit initial.
- Les URL de discussions Reddit et Hacker News ont été renvoyées via des redirections. Elles ont été omises afin que chaque lien cité s'ouvre directement.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/ashryaagr/karpathy-output-style | ashryaagr/karpathy-output-style: AI agent skills for visual and structured LLM outputs | 2026-10-23 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** project:karpathy-output-style, thread karpathy-output-style-visual-explanations, 2 événements datés du 2026-10-22 au 2026-10-22.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés font autorité pour déterminer ce qui est obsolète.
