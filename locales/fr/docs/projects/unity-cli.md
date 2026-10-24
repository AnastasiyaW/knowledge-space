---
title: "Unity CLI"
category: projects
date: 2026-07-23
tags: [project, unity-cli, unity-cli-introduction, unity_cli]
aliases: ["Unity CLI"]
level: 2
source_sha256: 62d73d94e26b8296c421444daf77d41f98ab65e1aa105de3b0512f2517612026
translation: machine
translated_at: '2026-10-24'
---
# Unity CLI {#unity-cli}

**Ligne de développement :** `project:unity-cli` · fil `unity-cli-introduction`  
**Dernier événement :** 2026-07-23 · 1 événement daté depuis le 2026-07-23 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Unity CLI — binaire autonome `unity` pour Unity 6.0 LTS+ et CI. — installe l'Editor et ses modules ; — ouvre et gère les projets, les licences et l'authentification ; — avec `com.unity.pipeline`, pilote l'Editor local en cours d'exécution ou un Player de développement, lance des commandes et des évaluations C#. Limite : la CLI et Pipeline restent expérimentaux ; Pipeline est un package distinct et fonctionne par défaut en local. Verdict : pour les nouveaux scripts et la CI, c'est un remplacement de Hub CLI, mais la version beta doit être figée et vérifiée d'après les notes de version.

## Ligne de développement {#development-line}

- **2026-07-23 — Unity a publié une annonce concernant Unity CLI.** Le 2026-07-23, Unity a publié une entrée de blog officielle datée portant sur Unity CLI. Le lien officiel spécifique au projet fait de cet événement une étape importante de l'introduction dans l'historique de Unity CLI. Les éléments probants retenus n'établissent ni ses capacités, ni sa disponibilité, ni son comportement technique.

## Évolutions {#what-changed}

2026-04-04 — la première beta publique a livré un binaire unique pour Windows, macOS et Linux, permettant de gérer l'Editor, les projets, l'authentification et une sortie lisible par machine. 2026-04-23 — sont apparues la création de projets, la consultation du changelog et la mise à jour vers une version choisie. 2026-05-06 — Unity Hub 3.18 a commencé à fournir une CLI distincte, indépendante du Hub de bureau. 2026-05-07 — beta.4 a ajouté le diagnostic, la complétion et les commandes principales de gestion de l'Editor et des projets. 2026-05-21 — l'authentification par compte de service et `unity pipeline install` ont rendu la CI sans supervision et le raccordement de Pipeline courants. 2026-06-04 — `unity eval` et `unity status` ont ajouté l'évaluation C# et la supervision de l'Editor connecté. 2026-06-16 — ont été ajoutés la gestion des licences et le clonage de projets depuis GitHub, GitLab et Unity Version Control. 2026-06-25 — est apparu `unity mcp` pour les intégrations agentiques. 2026-06-30 — la branche est passée en 1.0 beta ; des fuites d'identifiants de session OAuth dans les journaux et dans la sortie JSON/NDJSON ont été corrigées. 2026-07-16 — est apparu le `unity shell` interactif à chaud. 2026-07-23 — 1.0.0-beta.3 a ajouté l'historique, la complétion, le contexte de session et le NDJSON encadré dans le shell. 2026-08-12 — beta.4 a ajouté winget et Homebrew et relevé le minimum Linux à glibc 2.34. 2026-08-13 — beta.5 a cessé de transmettre le nom et l'e-mail depuis `unity bug`. 2026-08-21 — beta.6 a modifié les codes de sortie de `unity bug` et `unity test`, qui comptent pour la CI. 2026-09-02 — beta.8 a remplacé la beta.7 retirée, ajouté un workflow VCS conscient d'Unity et corrigé l'incompatibilité avec une version non publiée de Pipeline.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-23, les praticiens doivent suivre Unity CLI comme une ligne de développement officielle d'Unity et n'évaluer son usage pour l'automatisation en ligne de commande qu'après avoir confirmé ses capacités documentées.

1. Installez la CLI selon la notice actuelle d'Unity et vérifiez sa disponibilité avec la commande `unity --version`.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
2. Consultez les commandes avec `unity --help`, installez une version précise de l'Editor avec les modules nécessaires et vérifiez les identifiants de modules disponibles.
  — <https://unity.com/ru/blog/meet-the-unity-cli>
3. Exécutez `unity auth login`, puis `unity auth status` ; pour une CI sans supervision, utilisez l'authentification par compte de service prise en charge.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
4. Ouvrez le projet avec `unity open <path>` ; pour une CI orientée terminal, indiquez une version précise de l'Editor plutôt qu'une sélection interactive.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
5. Si vous devez piloter un Editor en cours d'exécution, installez `com.unity.pipeline` avec `unity pipeline install`, puis appelez `unity command` pour obtenir l'ensemble des commandes disponibles pour le projet.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
6. Pour la CI, demandez du JSON ou du NDJSON, traitez stdout séparément de stderr et vérifiez le code de sortie.
  — <https://unity.com/ru/blog/meet-the-unity-cli>

## Bonnes pratiques {#best-practices}

- Considérez `unity --help` de la version installée comme la source de référence pour les options : la documentation peut ne pas contenir une commande ajoutée récemment.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- En CI, indiquez explicitement la version de l'Editor : sans elle, `unity install` non interactif échoue.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- Ne mettez pas à jour le runner Linux vers beta.4+ sans glibc 2.34 ; pour Ubuntu 20.04 et versions antérieures, Debian 11, RHEL/CentOS 8 et Amazon Linux 2, restez sur beta.3.
  — <https://docs.unity.com/ja-jp/unity-cli/release-notes>
- Laissez Pipeline sur localhost tant que l'authentification et le réseau pour un accès distant ne sont pas conçus.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
- Mettez à jour la beta.7 installée brièvement vers beta.8 : beta.7 a été retirée en raison d'une incompatibilité avec le package Pipeline non encore publié.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>
- Avant `unity close`, enregistrez vos modifications : ni l'appel ordinaire ni `--force` n'enregistrent le travail.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>

## Ce qui est remplacé {#superseded-by-this}

- 2026-05-06 — pour les nouveaux scripts, ne choisissez pas Hub CLI avec `-- --headless` comme voie principale : la CLI Unity distincte est destinée aux nouveaux scénarios d'automatisation et de CI ; Hub CLI est déprécié et maintenu a minima. https://docs.unity.com/hub/cli-overview
- 2026-09-02 — 1.0.0-beta.7 n'est pas une version admissible pour une mise à jour : cette version a été retirée et remplacée par beta.8 en raison d'une incompatibilité avec le package Pipeline requis. https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542

## Points non établis {#still-unknown}

- La documentation officielle indique encore Unity CLI comme expérimental ; la date de disponibilité générale et le support à long terme ne sont pas annoncés.
- La CLI et `com.unity.pipeline` sont deux composants distincts : sans Pipeline, la CLI n'expose pas de surface de pilotage de l'Editor ou du Player en cours d'exécution.
- Le document officiel lié à l'événement est daté du 2026-07-20, alors que l'événement est daté du 2026-07-23 ; beta.3 figure bien dans les notes de version à la date du 2026-07-23.
- La documentation officielle en chinois a été consultée, mais aucun retour d'expérience indépendant en chinois n'a été trouvé pour étayer les recommandations, et il n'a donc pas été utilisé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://unity.com/ru/blog/meet-the-unity-cli | Meet the Unity CLI : piloter Unity depuis le terminal | 2026-09-05 |
| https://unity.com/blog/meet-the-unity-cli | Meet the Unity CLI : manage Unity from your terminal | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli | Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/zh-cn/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference | Unity command-line interface (CLI) reference | 2026-09-05 |
| https://docs.unity.com/ja-jp/unity-cli/release-notes | Unity command-line interface (CLI) release notes | 2026-09-05 |
| https://unity.com/unity-hub/release-notes | Unity Hub Release Notes | 2026-09-05 |
| https://docs.unity.com/hub/cli-overview | Command line interface overview | 2026-09-05 |
| https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe | Introduction to Unity CLI | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-6-is-rolling-out/1734486 | Unity CLI 1.0.0-beta.6 is rolling out | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542 | Unity CLI 1.0.0-beta.8 is rolling out | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:unity-cli`, fil `unity-cli-introduction`, 1 événement daté du 2026-07-23 au 2026-07-23.
- **Note pratique :** Au 2026-07-23, les praticiens doivent suivre Unity CLI comme une ligne de développement officielle d'Unity et n'évaluer son usage pour l'automatisation en ligne de commande qu'après avoir confirmé ses capacités documentées.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
