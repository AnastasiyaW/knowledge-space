---
title: "Pascal Editor"
category: projects
date: 2026-07-27
tags: [editor, pascal-editor-development, pascal_editor, project]
aliases: ["Pascal Editor"]
level: 3
source_sha256: 3ec53c45d41bdbf4a93551c8169abe954b528cf242d8ac78659bf2bd735f4ad0
translation: machine
translated_at: '2026-10-24'
---
# Pascal Editor {#pascal-editor}

**Ligne de développement :** `project:editor` · fil `pascal-editor-development`  
**Dernier événement :** 2026-07-27 · 1 événement daté depuis le 2026-07-27 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Description {#what-it-is}

Pascal Editor est un éditeur open source de bâtiments en 3D doté d'un graphe de scène sémantique.

- Fonctionne comme éditeur hébergé ou comme runtime CLI local persistant.
- Expose des outils MCP pour l'édition de projets et de scènes, la validation et la sauvegarde.
- Publie des paquets React réutilisables pour l'intégration.

## Ligne de développement {#development-line}

- **2026-07-27 — Dépôt GitHub de Pascal Editor relié.** Le 2026-07-27, nous avons relié le dépôt GitHub du projet. Cela fournit une référence publique au projet, mais ne documente aucune version, fonctionnalité, changement de propriété ni état du dépôt.

## Évolutions {#what-changed}

- 2026-04-09 — Lancement de Pascal v1.0.0 hébergé, avec un graphe de scène sémantique destiné aux personnes et aux agents IA.
- 2026-04-14 — La v1.1.0 hébergée ajoute la génération de disposition par IA et un onglet de rendu photoréaliste.
- 2026-05-05 — La v1.2.0 hébergée ajoute l'édition pilotée par agent et la conversion d'images en 3D SAM3D.
- 2026-06-09 — La v1.3.0 hébergée ajoute des préréglages, des modèles de pièces et une manipulation améliorée.
- 2026-06-10 — La v0.9.1 open source publie les paquets core, viewer et editor en version 0.9.1 ; les paquets v0.9.0 annoncés n'ont jamais été publiés sur npm.
- 2026-06-21 — La v1.4.0 hébergée ajoute les matériaux, les visites à la première personne et les outils MEP.
- 2026-07-08 — La v1.5.0 hébergée ajoute un Studio reconstruit, le premier plugin d'éditeur et la saisie d'unités lingo.
- 2026-07-27 — Aucune version ou entrée de journal des modifications d'origine récupérée n'identifie un changement livré à cette date ; la référence au dépôt est un simple pointeur d'identité, et non une limite de version.
- 2026-07-30 — La v1.6.0 hébergée ajoute des flux de travail pour le terrain et la construction verticale ; les paquets open source associés ont été livrés séparément en tant que v1.0.0-beta.1.
- 2026-08-03 — La v1.7.0 hébergée ajoute l'édition en équipe, les curseurs et caméras partagés, le chat IA partagé et Material Studio.
- 2026-08-11 — La v1.8.0 hébergée ajoute la CLI Pascal et les comptes agents.
- 2026-08-26 — La v1.9.0 hébergée ajoute Bones, la numérisation de maillages Pascal Capture et la modélisation par blocs.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-27, utilisez le dépôt GitHub de Pascal Editor relié comme point de référence du projet, et vérifiez directement ses capacités et son état de publication avant de vous y fier.

1. Choisissez d'abord un espace de stockage de projets : utilisez le MCP hébergé pour les projets de compte ou d'organisation Pascal, ou la CLI locale pour les projets SQLite locaux ; ils ne partagent pas leurs données.
  — <https://editor.pascal.app/docs/developers/mcp>
2. Pour un éditeur local, installez Node.js 22.13+ et exécutez `npx @pascal-app/cli editor`.
  — <https://editor.pascal.app/docs/developers/local-editor>
3. Connectez un agent local avec `pascal mcp setup <codex|claude>` ou `pascal mcp connect` ; ne configurez le point de terminaison hébergé que pour les projets hébergés.
  — <https://editor.pascal.app/docs/developers/mcp>
4. Pour une scène existante, utilisez `list_scenes` puis `load_scene`, effectuez des modifications sémantiques, exécutez `validate_scene` et `verify_scene`, puis `save_scene` et `get_project_status`.
  — <https://editor.pascal.app/docs/developers/mcp>
5. Pour intégrer l'éditeur, installez les paquets publiés et chargez le plugin intégré avant de monter le viewer.
  — <https://github.com/pascalorg/editor>

## Bonnes pratiques {#best-practices}

- N'adoptez pas `v1.0.0-beta.1` par inadvertance : il s'agit d'une préversion publiée sous le tag `beta` de npm, tandis que `latest` reste sur la branche 0.x.
  — <https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1>
- En cas de défaillance du runtime local, exécutez `doctor`, puis `status`, puis consultez les journaux avant de recourir à un arrêt forcé.
  — <https://editor.pascal.app/docs/developers/local-editor>
- Privilégiez les outils de scène sémantiques plutôt que les correctifs bruts, et terminez chaque modification d'agent par une validation, une vérification, une sauvegarde et un contrôle de l'état du projet.
  — <https://editor.pascal.app/docs/developers/mcp>
- Pour les contributions au code source, exécutez `bun check` et `bun run test` ; un simple `bun test` n'exécute pas le script de test de l'espace de travail.
  — <https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- Aucune version ou entrée de journal des modifications d'origine n'a été trouvée pour le 2026-07-27 ; aucune capacité ni version ne peut donc être attribuée sûrement à cette date.
- Le journal des modifications du produit hébergé et les publications des paquets open source utilisent des numéros de version différents ; la version du 30 juillet explique cette distinction, mais aucune matrice complète de compatibilité entre versions postérieures n'a été trouvée.
- Aucune documentation officielle en chinois ni aucun retour d'expérience indépendant et reproductible en chinois n'a été trouvé ; aucune pratique en chinois n'est donc incluse.
- La documentation de la CLI locale décrit toujours la prise en charge de Linux et de Windows comme non vérifiée lors de sa première version ; aucune matrice actuelle de prise en charge des plateformes n'a été trouvée.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/pascalorg/editor | Pascal Editor — dépôt GitHub | 2026-09-06 |
| https://editor.pascal.app/changelog | Journal des modifications \| Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v0.9.1 | Version v0.9.1 — Système de préréglages, pièces et modèles, manipulation de bâtiments | 2026-09-06 |
| https://editor.pascal.app/changelog/2026-07-30-terrain-and-community | Façonner le sol, puis construire dessus \| Journal des modifications \| Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1 | Version Pascal Editor 1.0.0-beta.1 | 2026-09-06 |
| https://editor.pascal.app/docs/developers/local-editor | Exécuter Pascal en local - Pascal | 2026-09-06 |
| https://editor.pascal.app/docs/developers/mcp | Connecter un agent IA - Pascal | 2026-09-06 |
| https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md | Contribuer à Pascal Editor | 2026-09-06 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:editor`, fil `pascal-editor-development`, 1 événement daté du 2026-07-27 au 2026-07-27.
- **Note pratique :** Au 2026-07-27, utilisez le dépôt GitHub de Pascal Editor relié comme point de référence du projet, et vérifiez directement ses capacités et son état de publication avant de vous y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
