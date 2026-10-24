---
title: "OmniRoute"
category: projects
date: 2026-07-25
tags: [omniroute, project]
aliases: ["OmniRoute"]
level: 2
source_sha256: c70e84768644811a4ba3bedb90c2ca9f1152fd621096324f32e80f3adcda6489
translation: machine
translated_at: '2026-10-24'
---
# OmniRoute {#omniroute}

**Ligne de développement :** `project:omniroute` · fil `omniroute`  
**Dernier événement :** 2026-07-25 · 1 daté depuis le 2026-07-25 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

OmniRoute est une passerelle sous licence MIT qui connecte Claude Code, Codex, Cursor, Cline et d'autres clients à des fournisseurs de modèles via un point d'accès unique.

- Fournisseurs et modèles : acheminer le trafic vers des cibles en amont.
- Routage de secours et combinaisons : gérer le basculement entre plusieurs points d'accès.
- Quotas : suivre les limites d'utilisation.
- MCP/A2A : connecter des protocoles d'outils et d'agents.
- Application de bureau/PWA : exécuter des interfaces locales et web.

Le README recense 352 fournisseurs et 1 312 identifiants de modèles de chat pour la ligne v3.8.50. Cela convient à un déploiement auto-hébergé et à la gestion de plusieurs sources d'API. Vérifiez les données de quota gratuit avant de dimensionner le trafic.

## Ligne de développement {#development-line}

- **2026-07-25 — Référence du dépôt GitHub d'OmniRoute.** La prise en charge de Gemini 3.6 flash-high, flash-medium et flash-low a été ajoutée via le fournisseur Antigravity CLI, mais elle attendait la version v3.8.49. Le mainteneur l'a confirmé le 2026-07-26.

## Ce qui a changé {#what-changed}

2026-07-25 — la version v3.8.48 publiée était en retard sur le développement : la prise en charge de Gemini 3.6 flash-high, flash-medium et flash-low a été ajoutée via le fournisseur Antigravity CLI, mais elle attendait la version v3.8.49 ; le mainteneur l'a confirmé le 2026-07-26. 2026-08-06 — la feuille de route a acté la transition de la ligne v3.8.x vers la v3.9.0 LTS et la v4 modulaire : la v3 reste la ligne stable, tandis que les nouvelles fonctionnalités passent en v4.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-25, les praticiens doivent utiliser le dépôt GitHub d'OmniRoute lié comme point de départ pour l'inspection du code source, sans déduire un ensemble de fonctionnalités prises en charge ni un statut de version tant que le dépôt n'a pas été analysé.

1. Pour développer à partir du code source, clonez le dépôt, exécutez `npm install`, `npm run build` puis `npm start` ; lancez le serveur de développement avec `npm run dev` sur le port 20128.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
2. Connectez un client compatible au point d'accès OmniRoute et configurez les fournisseurs, les modèles et les règles de secours dans le tableau de bord ou la configuration du projet.
  — <https://github.com/diegosouzapw/OmniRoute>

## Bonnes pratiques {#best-practices}

- Ne confondez pas un modèle en cours de développement avec une disponibilité dans une version publiée : Gemini 3.6 au 25 juillet nécessitait la branche release/v3.8.49 ou une compilation depuis les sources.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
- En production, choisissez la ligne stable v3/LTS ; n'utilisez les builds nightly et de publication que pour tester de nouvelles fonctionnalités.
  — <https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md>

## Remplacé par ceci {#superseded-by-this}

- 2026-07-25 : supposer que la version publiée v3.8.48 incluait Gemini 3.6 est obsolète ; la prise en charge n'existait que dans la future version release/v3.8.49.
- 2026-08-06 : ajouter toutes les nouvelles fonctionnalités à la v3 est remplacé par la séparation entre la v3/LTS stable et la v4 modulaire.

## Points encore inconnus {#still-unknown}

- Le schéma fourni ne contient pas les champs event_findings et new_events. Le détail de l'événement du 2026-07-25 et l'événement ultérieur du 2026-08-06 sont enregistrés dans what_changed ; la source primaire de la première addition est datée du 2026-07-26.
- La version stable actuellement publiée n'est pas confirmée par ces sources : le dépôt affiche release/v3.8.51, mais cela ne prouve pas qu'une version soit publiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/diegosouzapw/OmniRoute | Dépôt OmniRoute et README | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/discussions/8556 | New Release? — réponse du mainteneur sur Gemini 3.6 et release/v3.8.49 | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md | Feuille de route d'OmniRoute | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:omniroute`, fil `omniroute`, 1 événement daté du 2026-07-25 au 2026-07-25.
- **Note pratique :** À partir du 2026-07-25, les praticiens doivent utiliser le dépôt GitHub d'OmniRoute lié comme point de départ pour l'inspection du code source, sans déduire un ensemble de fonctionnalités prises en charge ni un statut de version tant que le dépôt n'a pas été analysé.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
