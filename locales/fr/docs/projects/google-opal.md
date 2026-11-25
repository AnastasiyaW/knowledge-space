---
title: "Google Opal"
category: projects
date: 2025-07-25
tags: [google-opal, opal, project]
aliases: ["Google Opal"]
level: 2
source_sha256: c2b9f1afd4c006f20c7cde4782bea3e7ed4b029485134ad606c6e20e8a10ce5f
translation: machine
translated_at: '2026-10-24'
---
# Google Opal {#google-opal}

**Ligne de développement :** `project:google-opal` · fil `google-opal`  
**Dernier événement :** 2025-07-25 · 1 événement daté depuis le 2025-07-25 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Google Opal est une alternative sans code aux petites applications web sur mesure, conçue pour les personnes qui veulent partager des flux de travail d'IA sans exploiter de serveur.

- Éditeur de flux de travail : construit et modifie des pipelines sous forme de nœuds à partir d'un langage naturel.
- Canevas visuel : enchaîne les entrées, les invites, les appels de modèles, les outils et les sorties.
- Mode Agent : sélectionne les outils, utilise la mémoire, oriente l'exécution et mène des échanges de suivi.

## Ligne de développement {#development-line}

- **2025-07-25 — Google présente Opal.** Le 2025-07-25, Google a publié une présentation d'Opal et partagé son point d'entrée web. Le lancement a confirmé l'existence du projet, sans établir l'ensemble de ses fonctionnalités, sa disponibilité régionale ni les limites des comptes.

## Évolutions {#what-changed}

- **2025-07-25** (annonce initiale datée du 2025-07-24) — Opal a été lancé en version bêta publique réservée aux États-Unis, sous forme de créateur visuel et en langage naturel pour des applications en plusieurs étapes enchaînant invites, appels de modèles et outils.
- **2026-02-25** (annonce officielle datée du 2026-02-24) — L'étape Generate a reçu le Mode Agent, qui permet de choisir outils et modèles en fonction d'un objectif, de conserver la mémoire, d'orienter dynamiquement l'exécution et de poser des questions de suivi.
- **2026-03-24** — La documentation officielle montre que le Mode Agent est activé par défaut et expose Search/Maps, Code Exec, Memory et la génération de médias. Les flux de travail fixes restent disponibles pour une logique rigide ou de haute précision.

## Mode d'emploi {#how-to-use-this}

Nous évaluons Google Opal à partir de sa présentation officielle et de son point d'entrée web du 2025-07-25. La documentation officielle ne fait état d'aucune modification ultérieure du flux de travail ou des capacités.

1. Connectez-vous à Opal, ouvrez une démo de la Galerie et sélectionnez Remix pour créer une copie modifiable. Sélectionnez Create New pour construire une application à partir de zéro.
  — <https://developers.google.com/opal/quickstart>
2. Pour les flux de travail ouverts, ajoutez une étape Generate, activez Agent si nécessaire et définissez le résultat visé.
  — <https://developers.google.com/opal/Agent_Mode>
3. Référencez les capacités nécessaires avec le menu @, par exemple @Search ou @Memory, puis reliez les entrées, les étapes de génération et les sorties dans l'éditeur visuel.
  — <https://developers.google.com/opal/Agent_Mode>
4. Prévisualisez l'application avec des entrées représentatives, inspectez le graphe obtenu, puis affinez les invites ou les nœuds avant de partager.
  — <https://developers.google.com/opal/quickstart>
5. Gardez chaque Opal privé par défaut. Lors du partage, limitez les utilisateurs à la vue de l'application ou accordez un accès complet à l'éditeur et au remix.
  — <https://developers.google.com/opal/faq>

## Bonnes pratiques {#best-practices}

- Faites un remix d'une application existante de la Galerie plutôt que de concevoir le premier flux de travail sur un canevas vide.
  — <https://developers.google.com/opal/quickstart>
- Pour le Mode Agent, précisez l'objectif et le résultat attendu plutôt que de prescrire chaque étape intermédiaire.
  — <https://developers.google.com/opal/Agent_Mode>
- Appelez explicitement les outils avec @ lorsque vous avez besoin d'une capacité particulière, ce que la documentation officielle décrit comme plus précis.
  — <https://developers.google.com/opal/Agent_Mode>
- Testez les invites et le flux de travail complet avant de vous y fier, car Opal peut commettre des erreurs.
  — <https://developers.google.com/opal/faq>
- Considérez le remix et le partage d'éditeur comme une divulgation des invites : le partage expose les invites, le graphe du flux de travail et le fichier Drive sous-jacent.
  — <https://developers.google.com/opal/faq>

## Remplacé par ce qui suit {#superseded-by-this}

- **2025-07-25** — La règle d'accès initiale à la bêta publique réservée aux États-Unis est obsolète : la FAQ actuelle énumère les pays pris en charge au lieu de restreindre l'accès aux États-Unis.
- **Avant le 2026-02-25** — Considérer chaque Opal uniquement comme une chaîne d'invites statique est obsolète pour les tâches ouvertes : le Mode Agent ajoute la sélection d'outils, la mémoire, l'orientation de l'exécution et le dialogue interactif. Les flux de travail fixes restent appropriés pour une logique rigide ou de haute précision.

## Points encore inconnus {#still-unknown}

- Nous n'avons effectué aucun test connecté ; les quotas, la facturation, les plafonds de publication et la disponibilité des fonctionnalités propres à chaque compte n'ont pas été vérifiés.
- Les recherches en chinois n'ont trouvé aucune documentation Opal officielle en chinois simplifié ; les recommandations reposent donc entièrement sur des sources officielles en anglais.
- La disponibilité reste propre à chaque pays ; consultez la FAQ officielle actuelle avant d'adopter Opal pour un flux de travail.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://developers.googleblog.com/en/introducing-opal/ | Introducing Opal: describe, create, and share your AI mini-apps | 2026-09-04 |
| https://opal.google/landing/ | Opal [Experiment] | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/ | Build dynamic agentic workflows in Opal | 2026-09-04 |
| https://developers.google.com/opal/ | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/quickstart | Quickstart | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/Agent_Mode | Agent Mode in Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/faq | Frequently asked questions and best practices | Opal | Google for Developers | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:google-opal`, fil `google-opal`, 1 événement daté, du 2025-07-25 au 2025-07-25.
- **Note pratique :** à partir du 2025-07-25, les praticiens pouvaient évaluer Google Opal à travers la présentation officielle du projet par Google et le point d'entrée web associé ; les éléments disponibles n'établissent aucune modification ultérieure du flux de travail ou des capacités.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
