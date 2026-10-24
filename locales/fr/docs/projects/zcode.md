---
title: "ZCode 3.0 — ZCode IDE"
category: projects
date: 2026-06-15
tags: [project, zcode, zcode-ide, zcode_ide]
aliases: ["ZCode 3.0"]
level: 2
source_sha256: 68cb5ebe098b17cf0ad7c9fe0239f87dbcb8a984be97af6a96d32257698b0bba
translation: machine
translated_at: '2026-10-24'
---
# ZCode 3.0 — ZCode IDE {#zcode-30-zcode-ide}

**Ligne de développement :** `project:zcode` · fil `zcode-ide`  
**Dernier événement :** 2026-06-15 · 1 événement daté depuis le 2026-06-15 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ZCode 3.0 est l'ADE de bureau de Z.ai. Il fonctionne comme un harnais graphique pour un agent, et non comme un agent de codage uniquement en terminal. L'environnement combine ZCode Agent, des références aux fichiers et à l'espace de travail, des commandes de terminal, des permissions d'exécution, l'état Git, Review et le contrôle à distance. Les téléchargements actuels fournissent la version v3.11.2. La documentation officielle centre le produit sur GLM-5.3 et sa fenêtre de contexte annoncée de 1M de tokens. Nous l'utilisons pour son flux de travail intégré sur le bureau, et non comme un remplacement direct qui charge récursivement les règles CLAUDE.md existantes.

## Ligne de développement {#development-line}

- **2026-06-15 — Apparition de la documentation d'installation de ZCode.** Le 2026-06-15, Z.ai a publié la documentation d'installation de ZCode en anglais. L'URL d'installation officielle marque une étape d'intégration pour la ligne ZCode 3.0. Les éléments disponibles n'établissent ni les détails de publication du produit, ni les plateformes prises en charge, ni le fait que le guide lui-même soit apparu pour la première fois ce jour-là.

## Ce qui a changé {#what-changed}

- **2026-06-15** — Le lien d'installation de ZCode 3.0 pointait vers le client de bureau. La version associée du 2026-06-13 a basculé vers ZCode Agent, développé en interne et optimisé pour GLM-5.2. Elle a ajouté des espaces de travail de tâches regroupées, la connaissance de projet Zread, un graphe de branches Git, la surveillance et la saisie de pièces jointes.
- **2026-08-14** — ZCode v3.7.7 a rendu GLM-5.3 disponible.
- **2026-08-20** — ZCode v3.8.1 a ajouté des contrôles globaux et par espace de travail des capacités de l'agent, ainsi que des Hooks au niveau de l'espace de travail.
- **2026-08-26** — ZCode v3.9.2 a ajouté GLM-5.3 Flash et des demandes explicites de permission de contrôle de l'ordinateur.
- **2026-09-04** — ZCode v3.11.2 a ajouté les aperçus PDF et médias dans les conversations ainsi que l'installation de plugins propre à un espace de travail.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-15, utilisez le guide d'installation officiel en anglais pour la configuration. Les sources disponibles ne confirment ni les environnements pris en charge, ni les capacités de la version.

1. Téléchargez la version actuelle pour macOS, Windows ou Linux, puis installez-la.
  — <https://zcode.z.ai/en/docs/install>
2. Au premier lancement, choisissez le répertoire du projet comme espace de travail et envoyez une courte instruction pour vérifier que l'Agent répond.
  — <https://zcode.z.ai/en/docs/install>
3. Connectez un compte Z.ai ou BigModel, ou configurez un fournisseur tiers compatible ou une clé API.
  — <https://zcode.z.ai/en/docs/configuration>
4. Placez les règles d'équipe durables, les commandes de validation et les consignes relatives aux fichiers à haut risque dans AGENTS.md à la racine de l'espace de travail.
  — <https://zcode.z.ai/en/docs/agents>
5. Énoncez un objectif concret, joignez les fichiers pertinents avec @, puis sélectionnez un mode d'exécution adapté au risque de la tâche.
  — <https://zcode.z.ai/en/docs/agents>

## Bonnes pratiques {#best-practices}

- Utilisez le mode Plan ou Ask avant toute modification pour les fichiers critiques, les commandes shell et les changements étendus. Réservez l'accès complet aux travaux clairs et à faible risque.
  — <https://zcode.z.ai/en/docs/agents>
- Conservez les règles importantes du projet dans le AGENTS.md de l'espace de travail courant. ZCode ne fusionne pas les fichiers imbriqués et n'étend pas les imports.
  — <https://zcode.z.ai/en/docs/agents>
- Pour une clé API Coding Plan, utilisez son point de terminaison dédié au code plutôt que le point de terminaison API général.
  — <https://zcode.z.ai/en/docs/configuration>
- Utilisez les commandes pour une invite simple et réutilisable. Utilisez les Skills lorsque le flux de travail nécessite aussi des scripts, des modèles ou des exemples.
  — <https://zcode.z.ai/en/docs/commands>
- Configurez un proxy requis directement dans ZCode. Un champ de proxy vide établit une connexion directe et n'hérite pas de HTTP_PROXY.
  — <https://zcode.z.ai/en/docs/install>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-14 — La sélection du modèle par défaut ne repose plus sur GLM-5.2 issu de la version 3.0 de ZCode. La version v3.7.7 a rendu GLM-5.3 disponible, et la documentation actuelle de ZCode Agent centre la présentation sur la famille GLM-5.3.
- 2026-09-04 — Le téléchargement de ZCode 3.0 est obsolète pour les nouvelles installations. Le téléchargement officiel actuel est la version v3.11.2.

## Points non élucidés {#still-unknown}

- Nous n'avons trouvé aucune note de version ZCode 3.0 datée de source première, ni d'empreinte immuable de l'installateur v3.0, dans l'historique officiel indexé. Un rapport secondaire daté confirme le détail de la version du 2026-06-13, à défaut d'une note de version primaire archivée.
- Nous n'avons pas évalué de manière indépendante l'avantage de quota intégré de 150 % annoncé, ni les affirmations d'une meilleure réussite des tâches par rapport aux agents tiers. Nous ne les recommandons pas.
- Les quotas des forfaits actuels, la disponibilité des fournisseurs et les versions de bureau sont susceptibles de changer. Nous ne donnons aucune recommandation de prix ou de quota.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://zcode.z.ai/en/docs/install | Install | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/agents | ZCode Agent | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/configuration | Connect Models | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/commands | Command | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/changelog | ZCode Releases & Updates | GLM-5.3 Coding Agent | 2026-09-05 |
| https://zcode.z.ai/cn/docs/install | 安装 | ZCode Docs | 2026-09-05 |
| https://www.ithome.com/0/963/985.htm | 智谱 AI 编程工具 ZCode 3.0 版本发布：切换自研 ZCode Agent 内核，深度适配 GLM-5.2 | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:zcode`, fil `zcode-ide`, 1 événement daté du 2026-06-15 au 2026-06-15.
- **Note pratique :** À partir du 2026-06-15, les praticiens qui évaluent ZCode doivent utiliser le guide d'installation officiel en anglais comme point d'entrée pour la configuration. Les sources disponibles ne confirment ni les environnements pris en charge, ni les capacités de la version.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
