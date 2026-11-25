---
title: "OpenMAIC"
category: projects
date: 2026-03-16
tags: [openmaic, openmaic-development, project]
aliases: ["OpenMAIC"]
level: 2
source_sha256: edbb7f1400bb32e90646085c9d869842f0a52fea0779f44eec33abc390395d5b
translation: machine
translated_at: '2026-10-24'
---
# OpenMAIC {#openmaic}

**Ligne de développement :** `project:openmaic` · fil `openmaic-development`  
**Dernier événement :** 2026-03-16 · 1 événement daté depuis le 2026-03-16 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

OpenMAIC est un générateur de salles de classe open source destiné aux enseignants et aux apprenants : diapositives, quiz, scènes HTML interactives, apprentissage par projet, discussions avec un enseignant ou des pairs IA, tableau blanc, synthèse vocale (TTS) et exports. L'auto-hébergement exige actuellement Node.js 22.19+ et pnpm 10+. Verdict : à utiliser lorsqu'une leçon générée doit prendre la forme d'une salle de classe interactive plutôt que d'une simple réponse de chatbot.

## Ligne de développement {#development-line}

- **2026-03-16 — Ressources du projet OpenMAIC citées.** Le 2026-03-16, un message daté concernant OpenMAIC mentionnait le dépôt GitHub du projet ainsi que son site web public. Les éléments fournis n'établissent ni publication, ni fonctionnalité, ni lancement, ni autre jalon technique : cet événement ne consigne donc que la disponibilité de ces ressources.

## Ce qui a changé {#what-changed}

2026-03-16 — OpenMAIC a été fondé et publié en open source comme projet de salle de classe interactive multi-agents ; la première version étiquetée est sortie le 2026-03-26.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-16, les praticiens peuvent utiliser le dépôt GitHub et le site du projet mentionnés comme ressources OpenMAIC identifiées ; les éléments fournis n'établissent aucune capacité, publication ni recommandation d'usage spécifique.

1. Clonez le dépôt et installez les dépendances avec pnpm.
  — <https://github.com/THU-MAIC/OpenMAIC>
2. Copiez .env.example vers .env.local et configurez au moins un fournisseur de LLM.
  — <https://github.com/THU-MAIC/OpenMAIC>
3. Exécutez pnpm dev, puis ouvrez http://localhost:3000 ; utilisez pnpm build && pnpm start pour une construction de production.
  — <https://github.com/THU-MAIC/OpenMAIC>
4. Pour un déploiement partagé, définissez ACCESS_CODE afin que l'interface et les routes de l'API exigent le mot de passe du site.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Bonnes pratiques {#best-practices}

- Considérez les widgets interactifs antérieurs à la version 0.3 comme des candidats à la compatibilité : la version v0.3.0 a supprimé l'accès de même origine depuis le bac à sable (sandbox) de l'iframe.
  — <https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md>
- Ne transmettez pas d'identifiants dans les arguments de build Docker : les métadonnées de l'image ou la provenance du build peuvent les conserver.
  — <https://github.com/THU-MAIC/OpenMAIC>
- Utilisez ACCESS_CODE pour une instance partagée plutôt que de laisser ouverts ses salles de classe générées et ses routes de l'API.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Remplacé par ce document {#superseded-by-this}

- 2026-06-28 — Les recommandations relatives à la concession de licence commerciale sous AGPL-3.0 sont obsolètes : la version v0.3.0 a changé la licence d'OpenMAIC en MIT.
- 2026-06-28 — Les recommandations supposant que les widgets interactifs peuvent utiliser un accès de même origine depuis une iframe sont obsolètes ; cette autorisation du bac à sable a été supprimée.

## Points toujours inconnus {#still-unknown}

- L'ensemble exact des fonctionnalités et le commit présents au lancement du 2026-03-16 ne peuvent pas être reconstitués à partir d'une source étiquetée au lancement : la première version étiquetée est la v0.1.0, datée du 2026-03-26.
- Le service hébergé n'a pas été retenu comme source, car sa page n'affichait pas de contenu lisible lors de l'examen.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/THU-MAIC/OpenMAIC | Dépôt THU-MAIC/OpenMAIC et guide d'installation actuel | 2026-09-05 |
| https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md | Journal des modifications d'OpenMAIC | 2026-09-05 |
| https://shangqingtu.github.io/ | Shangqing Tu — Actualités | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:openmaic`, fil `openmaic-development`, 1 événement daté du 2026-03-16 au 2026-03-16.
- **Note pratique :** Au 2026-03-16, les praticiens peuvent utiliser le dépôt GitHub et le site du projet mentionnés comme ressources OpenMAIC identifiées ; les éléments fournis n'établissent aucune capacité, publication ni recommandation d'usage spécifique.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
