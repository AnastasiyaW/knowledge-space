---
title: "Kimi Code CLI — Référence publique du projet"
category: projects
date: 2026-06-09
tags: [kimi-code-cli, kimi_code, project, public-project-reference]
aliases: ["Kimi Code CLI"]
level: 3
source_sha256: 90ca202bdd556789947dbafc6f2c4abc65ad16d65a12e2503b3dd5c0e0b6d0ba
translation: machine
translated_at: '2026-10-24'
---
# Kimi Code CLI — Référence publique du projet {#kimi-code-cli-public-project-reference}

**Ligne de développement :** `project:kimi-code-cli` · fil `public-project-reference`  
**Dernier événement :** 2026-06-09 · 1 événement daté depuis le 2026-06-09 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

Kimi Code CLI est un agent de codage en terminal destiné aux développeurs, et non un modèle autonome.

- Lit et modifie du code, exécute des commandes shell, recherche des fichiers et récupère des pages web.
- Utilise l'authentification OAuth de Kimi Code, une clé API de Kimi Platform ou des fournisseurs compatibles configurés ; prend en charge l'intégration ACP avec les éditeurs.
- Version publiée documentée actuelle : v0.41.0 le 2026-09-04 ; l'installation via npm nécessite Node.js 22.19+, et Windows nécessite Git for Windows.

Les modes de permission et les vérifications de version relèvent du pilotage opérationnel, et non de la simple configuration initiale.

## Ligne de développement {#development-line}

- **2026-06-09 — La documentation et le dépôt source de Kimi Code CLI ont été rendus publics.** Le 2026-06-09, une publication datée concernant Kimi Code CLI a fait le lien vers la documentation anglaise du projet et vers son dépôt GitHub. Cela établit un point de référence public pour la documentation et le code source de la CLI. Les éléments disponibles n'identifient ni version, ni mécanisme de publication, ni ensemble de fonctionnalités.

## Modifications {#what-changed}

2026-06-09 — Kimi Code CLI v0.12.0 a ajouté `/swarm` avec suivi de progression en direct et nouvelles tentatives tenant compte des limites de débit. Les objectifs, les questions en arrière-plan et la découverte des sous-compétences ne sont plus soumis à des indicateurs expérimentaux. La version a ajouté la prise en charge des proxys et de Homebrew, et activé la micro-compaction par défaut. À la même date, la v0.12.1 a corrigé la compatibilité avec l'ancienne configuration expérimentale et la transmission de l'effort `xhigh` pour les Chat Completions compatibles OpenAI.

## Mode d'emploi {#how-to-use-this}

1. Installez avec le script officiel, ou installez `@moonshot-ai/kimi-code` via npm ; sous Windows, installez Git for Windows avant le premier lancement.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
2. Accédez au répertoire du dépôt, exécutez `kimi`, puis utilisez `/login` pour l'OAuth de Kimi Code ou une clé API de Kimi Platform.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
3. Commencez par une demande d'orientation en lecture seule, par exemple demander à Kimi d'expliquer les répertoires du projet ; utilisez `kimi -p` pour une instruction ponctuelle.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
4. Vérifiez les approbations avant d'effectuer des modifications, et utilisez `/plan` avant tout travail complexe ou à haut risque.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
5. Pour un travail en plusieurs tours, utilisez `/goal` avec une condition d'achèvement et des éléments de preuve démontrant que l'objectif est atteint.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
6. Configurez les fournisseurs autres que Kimi et les alias de modèles dans `~/.kimi-code/config.toml` ; les variables d'environnement de clés API du shell ne sont pas automatiquement utilisées comme identifiants de fournisseur.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>

## Bonnes pratiques {#best-practices}

- Conservez le mode Always Ask ou Plan pour les modifications complexes ou risquées ; Never Ask s'exécute entièrement sans supervision, y compris pour les accès sensibles et les sorties du mode plan.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
- Rédigez les objectifs `/goal` avec une ligne d'arrivée et des éléments de vérification ; évitez les objectifs ouverts comme « trouver tous les bogues ».
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
- Utilisez des règles durables d'autorisation, de refus et de demande de confirmation avec des motifs exacts de commandes d'outils ; gardez activé le garde-fou des commandes dangereuses, sauf si un autre contrôle filtre les commandes.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>
- Vérifiez la version installée avant d'automatiser un flux de travail : les versions récentes ont modifié le comportement des permissions et des commandes.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html>

## Remplacé par ce qui suit {#superseded-by-this}

- :{
- claim
- La consigne de Kimi Code CLI visant à désactiver la micro-compaction expérimentale via `/experiments` est obsolète : la v0.23.0 a supprimé la fonctionnalité et son interrupteur.
- obsolete_since
- 2026-07-06
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html
- claim
- L'arborescence de commandes `kimi server` est dépréciée ; utilisez `kimi web` au premier plan et arrêtez-la avec Ctrl+C.
- obsolete_since
- 2026-07-20
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html

## Points restant inconnus {#still-unknown}

- Le libellé d'origine de l'événement du 2026-06-09 n'est pas disponible ; nous ne pouvons donc pas déterminer s'il concernait la v0.12.0, la v0.12.1 ou les deux. Le journal officiel des modifications mentionne les deux versions à cette date.
- Le guide d'interaction utilise les libellés Always Ask, Ask When Needed et Never Ask, tandis que les exemples de configuration conservent `manual`, `yolo` et `auto` ; nous n'avons pas testé indépendamment la compatibilité de ces alias de libellés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://moonshotai.github.io/kimi-code/en/ | Documentation de Kimi Code CLI | 2026-09-07 |
| https://github.com/MoonshotAI/kimi-code | GitHub - MoonshotAI/kimi-code : Kimi Code CLI — Le point de départ des agents de nouvelle génération | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html | Journal des modifications \| Documentation Kimi Code | 2026-09-07 |
| https://www.kimi.com/code/docs/kimi-code-cli/release-notes/changelog.html | Journal des modifications (version chinoise) \| Documentation Kimi Code | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html | Prise en main \| Documentation Kimi Code | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html | Interaction et saisie \| Documentation Kimi Code | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html | Objectifs \| Documentation Kimi Code | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html | Fichiers de configuration \| Documentation Kimi Code | 2026-09-07 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:kimi-code-cli`, fil `public-project-reference`, 1 événement daté du 2026-06-09 au 2026-06-09.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les obsolescences datées ci-dessus font foi pour ce qui est obsolète.
