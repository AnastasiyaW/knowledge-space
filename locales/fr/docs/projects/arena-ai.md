---
title: "Arena.ai — Agent Mode"
category: projects
date: 2026-06-04
tags: [agent-mode, arena-ai, arena_ai, project]
aliases: ["Arena.ai"]
level: 3
source_sha256: 2be68514e30a62d82567888e1529a44a3351d43125f96a6f78927e8a2f3f413f
translation: machine
translated_at: '2026-10-24'
---
# Arena.ai — Agent Mode {#arenaai-agent-mode}

**Ligne de développement :** `project:arena-ai` · fil `agent-mode`  
**Dernier événement :** 2026-06-04 · 1 daté depuis le 2026-06-04 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Arena.ai Agent Mode est un espace de travail dans le navigateur destiné aux tâches en plusieurs étapes, plutôt qu'aux réponses isolées d'un chat.

- Planifie les tâches et les exécute à l'aide de la recherche web, de la génération d'images, des envois de fichiers, d'une aide au code et d'un Bash en bac à sable.
- Connecte un dépôt GitHub à cloner dans un bac à sable, afficher les diff et créer des pull requests.
- Achemine chaque session vers un modèle orchestrateur non divulgué, choisi au hasard.

Une session liée à un dépôt ne crée qu'une seule pull request et ne peut plus pousser de travail supplémentaire une fois la pull request fusionnée ou fermée.
À utiliser pour des livrables bornés que nous pouvons inspecter ; le classement reflète l'environnement d'Arena et non une garantie universelle.

## Ligne de développement {#development-line}

- **2026-06-04 — Arena.ai a publié une mise à jour de développement d'Agent Mode.** Arena.ai a lancé Agent Mode avec des workflows multi-étapes utilisant des outils, ainsi qu'un classement Agent Arena construit à partir de traces de sessions réelles.

## Ce qui a changé {#what-changed}

- 2026-06-04 : Arena.ai a lancé Agent Mode avec un workflow multi-étapes utilisant des outils, ainsi que le classement Agent Arena dérivé de traces de sessions réelles.
- 2026-06-29 : Arena a annoncé plus de 5 M de tours Agent Mode par mois et une croissance de 10 % d'une semaine sur l'autre.
- 2026-08-14 : Agent Arena a ajouté les filtres Code, Chat et Work, ainsi que des vues coût par tâche et Pareto.
- 2026-08-24 : Agent Mode a ajouté le codage connecté à GitHub, avec clones en bac à sable, diff en direct, commits, pushes et pull requests.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-04, les praticiens qui évaluent Arena.ai doivent examiner son workflow Agent Mode et sa surface produit d'agent dans le cadre de leur évaluation d'outil, tout en vérifiant les capacités directement, car cette ligne ne contient aucune preuve de fonctionnalité issue de recherches.

1. Ouvrir Agent Mode directement.
  — <https://arena.ai/agent>
2. Décrire le résultat multi-étapes souhaité, joindre les fichiers pertinents et lancer le workflow depuis la barre de chat.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
3. Utiliser Workspace pour récupérer les résultats : télécharger un ZIP sans dépôt, ou inspecter le Diff et la pull request lorsqu'un dépôt est connecté.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
4. Pour le travail sur dépôt, connecter GitHub, sélectionner les organisations et dépôts auxquels Arena peut accéder, puis activer GitHub dans Agent Mode.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
5. Examiner le diff et les Checks automatisés avant la fusion ; rester dans la limite actuelle d'une pull request par chat.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>

## Bonnes pratiques {#best-practices}

- Utiliser Agent Mode pour la recherche, le codage, l'analyse ou l'itération connectés ; utiliser Battle, Side-by-Side ou Direct pour une requête simple en une étape.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
- Choisir un modèle d'agent dans la vue Code, Chat ou Work pertinente et comparer le coût des tâches, plutôt que de traiter un classement global unique comme universel.
  — <https://arena.ai/blog/agent-categories-and-cost>
- Pour le travail sur GitHub, limiter une session à une seule pull request relisible et inspecter à la fois le Diff et les Checks avant la fusion.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
- Pousser ou télécharger le travail avant de fusionner ou fermer une pull request, car la session ne peut pas livrer de fichiers ultérieurs dans ce workflow clos.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>

## Remplacé par ceci {#superseded-by-this}

- Depuis le 2026-08-14, choisir un modèle Agent Arena à partir du seul classement global est incomplet ; utiliser les vues par catégorie et par coût.
- Depuis le 2026-08-24, décrire Agent Mode comme un bac à sable sans workflow de livraison sur dépôt est obsolète ; il peut connecter des dépôts GitHub et créer des pull requests.

## Toujours inconnu {#still-unknown}

- Arena ne divulgue pas le modèle orchestrateur après retour d'information ; une session terminée ne peut donc pas être rattachée à un modèle nommé à partir de l'interface publique décrite ici.
- Les sources consultées ne établissent pas la tarification, les limites de débit, la conservation des données ou un engagement de niveau de service pour Agent Mode.
- Les permissions des dépôts et le comportement de livraison en direct n'ont pas été testés directement dans une session connectée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| http://arena.ai/blog/agent-mode/ | Empowering Users to Get More Done With Agent Mode | 2026-09-05 |
| https://arena.ai/agent | Agent Mode \| Agents autonomes d'IA pour les tâches du monde réel | 2026-09-05 |
| https://arena.ai/blog/agent-arena-methodology | Agent Arena : évaluation causale des agents dans le monde réel | 2026-09-05 |
| https://help.arena.ai/articles/5432423882-how-to-use-agent-mode | Comment utiliser Agent Mode sur Arena | 2026-09-05 |
| https://arena.ai/blog/arena-100m-revenue | Arena atteint 100 M$ en 8 mois | 2026-09-05 |
| https://arena.ai/blog/agent-categories-and-cost | Agent Leaderboard Improvements : Categories & Task Cost | 2026-09-05 |
| https://arena.ai/blog/coding-in-agent-mode | Coding in Agent Mode : From Idea to Shipping with GitHub | 2026-09-05 |
| https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode | Comment utiliser le codage dans Agent Mode | 2026-09-05 |

## Brief d'agent {#agent-brief}

- **Sujet :** `project:arena-ai`, fil `agent-mode`, 1 événement daté du 2026-06-04 au 2026-06-04.
- **Note pratique :** À partir du 2026-06-04, les praticiens qui évaluent Arena.ai doivent examiner son workflow Agent Mode et sa surface produit d'agent dans le cadre de leur évaluation d'outil, tout en vérifiant les capacités directement, car cette ligne ne contient aucune preuve de fonctionnalité issue de recherches.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
