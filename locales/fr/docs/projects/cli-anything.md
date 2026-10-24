---
title: "CLI-Anything"
category: projects
date: 2026-03-11
tags: [agent_tools, cli-anything, cli-anything-development, project]
aliases: ["CLI-Anything"]
level: 3
source_sha256: b69f20aa5b45a099a4555be0c84671e95c53cafd07e2677916a5b6011060fc3a
translation: machine
translated_at: '2026-10-24'
---
# CLI-Anything {#cli-anything}

**Ligne de développement :** `project:cli-anything` · fil `cli-anything-development`  
**Dernier événement :** 2026-03-11 · 1 événement daté depuis le 2026-03-11 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

CLI-Anything est un projet HKUDS qui remplit deux tâches : installer une CLI existante via CLI-Hub, ou générer un harnais Python/Click pour un logiciel open source.

- Sortie JSON pour un traitement par machine
- REPL pour les sessions interactives
- Annulation et rétablissement pour le retour arrière d'état
- Tests pour la validation des harnais
- SKILL.md pour l'intégration avec les agents

CLI-Hub nécessite Python 3.10+.

Utilisez CLI-Hub pour un outil existant. Lancez le générateur lorsque le harnais est absent et que l'application cible peut être testée localement.

## Ligne de développement {#development-line}

- **2026-03-11 — Le dépôt GitHub CLI-Anything apparaît dans le fil agent_tools.** Le 2026-03-11, le dépôt GitHub HKUDS/CLI-Anything a été relayé dans le fil agent_tools. Ce lien fournit une référence datée dans la source examinée. Les éléments disponibles ne montrent ni publication, ni version, ni modification de fonctionnalité, ni jalon.

## Ce qui a changé {#what-changed}

- **2026-03-11** — Harnais Zoom ajouté comme 11e application prise en charge. Une publication distincte de ce même jour faisait état de plus de 4,4k étoiles GitHub, 9 applications et 1 436 tests ; ne considérez pas ces premiers chiffres comme un catalogue définitif ni comme une métrique actuelle.
- **2026-03-12** — Intégration Codex ajoutée.
- **2026-03-16** — Phase 6.5 ajoutée pour générer automatiquement un SKILL.md pour chaque harnais.
- **2026-03-17** — Lancement de CLI-Hub pour rechercher, installer et exécuter des CLI prêtes à l'emploi.
- **2026-03-30** — La v0.2.0 a retravaillé HARNESS.md autour de la divulgation progressive.
- **2026-04-18** — Fichiers SKILL.md regroupés dans le répertoire racine skills/.
- **2026-04-24** — La v0.3.0 a ajouté de nouveaux outils de harnais, notamment CloudCompare, IntelWatch, VideoCaptioner et Slay the Spire II.
- **2026-06-02** — Publication de l'article *CLI-Anything: Towards Agent-Native Computer Use*, qui définit le passage de l'automatisation GUI par écran aux CLI structurées.
- **2026-06-25** — La v0.4.0 a ajouté CLI-Matrix, 30 nouvelles CLI, 17 corrections et quatre renforcements de sécurité.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-11, les praticiens doivent traiter CLI-Anything comme un projet nécessitant une évaluation au niveau du code source avant adoption ; le lien daté seul ne fournit aucune affirmation vérifiée de capacité, de version ou de compatibilité.

1. Pour un outil existant, installez CLI-Hub avec pip install cli-anything-hub. Recherchez-le avec cli-hub search <requête>, inspectez-le avec cli-hub info <nom>, installez-le avec cli-hub install <nom>, et exécutez cli-hub launch <nom> --help.
  — <https://clianything.cc/docs.html>
2. Pour un logiciel absent du catalogue, préparez Python 3.10+, le code source ou un dépôt accessible, et un agent de codage pris en charge. Dans Claude Code, connectez la marketplace et exécutez /cli-anything <chemin-ou-dépôt>.
  — <https://github.com/HKUDS/CLI-Anything>
3. Après la génération, installez le harnais depuis son répertoire agent-harness avec pip install -e .. Vérifiez les commandes avec --help et utilisez --json pour un traitement par machine.
  — <https://github.com/HKUDS/CLI-Anything>

## Bonnes pratiques {#best-practices}

- Recherchez d'abord une CLI existante dans CLI-Hub ; ne recourez au générateur que si le catalogue ne contient pas le harnais nécessaire.
  — <https://github.com/HKUDS/CLI-Anything>
- Ne considérez pas une CLI générée comme complète après une seule exécution : lancez refine pour les lacunes identifiées, puis validez et testez avant toute utilisation en production.
  — <https://github.com/HKUDS/CLI-Anything>
- Installez et testez l'application cible : un harnais peut nécessiter GIMP, Blender, LibreOffice ou d'autres logiciels en amont.
  — <https://github.com/HKUDS/CLI-Anything>
- En automatisation, utilisez --json et les codes de sortie plutôt que l'analyse de la sortie texte.
  — <https://clianything.cc/docs.html>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-03-11 : la première description du projet comme 9 applications et 1 436 tests est obsolète. L'historique officiel du projet à cette date indique Zoom comme 11e harnais, et la v0.4.0 a ensuite ajouté 30 CLI supplémentaires.
- 2026-03-11 : générer une CLI pour chaque demande est obsolète. Nous vérifions désormais d'abord CLI-Hub pour trouver et installer un outil existant du catalogue.
- 2026-03-11 : l'absence de flux de travail Codex est devenue obsolète le 2026-03-12 avec l'intégration intégrée.

## Toujours inconnu {#still-unknown}

- Le journal officiel du projet confirme l'événement du 2026-03-11, mais ne fournit pas d'instantané immuable du dépôt au moment de la publication. Les premiers chiffres issus de la source secondaire ne servent que de contexte à l'événement.
- Le schéma de sortie ne prend pas en charge les champs event_findings et new_events ; what_changed en stocke le contenu.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/HKUDS/CLI-Anything | Dépôt HKUDS/CLI-Anything et README actuel | 2026-09-05 |
| https://clianything.cc/docs.html | Documentation de CLI-Anything Hub | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases/tag/v0.4.0 | Publication CLI-Anything v0.4.0 | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases | Publications CLI-Anything | 2026-09-05 |
| https://arxiv.org/abs/2606.03854 | CLI-Anything: Towards Agent-Native Computer Use | 2026-09-05 |
| https://linux.do/t/topic/1737269?tl=en | Discussion CLI-Anything GitHub Trending | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:cli-anything`, fil `cli-anything-development`, 1 événement daté du 2026-03-11 au 2026-03-11.
- **Note pratique :** Au 2026-03-11, les praticiens doivent traiter CLI-Anything comme un projet nécessitant une évaluation au niveau du code source avant adoption ; le lien daté seul ne fournit aucune affirmation vérifiée de capacité, de version ou de compatibilité.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
