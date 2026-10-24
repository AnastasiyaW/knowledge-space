---
title: "Cursor Router"
category: projects
date: 2026-07-25
tags: [cursor, project, router]
aliases: ["Cursor Router"]
level: 2
source_sha256: 89adf4b8478602b37f2839c8c43f69453a86335b0b1210c8b868a5e6b1496358
translation: machine
translated_at: '2026-10-24'
---
# Cursor Router {#cursor-router}

**Ligne de développement :** `project:router` · fil `router`  
**Dernier événement :** 2026-07-25 · 1 événement daté depuis le 2026-07-25 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Cursor Router achemine chaque requête de l'Agent vers le pool de modèles changeant de Cursor, au lieu de demander au développeur de choisir un modèle pour chaque requête. Il propose les modes Cost, Balance et Intelligence pour les offres Teams et Enterprise. Balance et Intelligence consomment les limites d'utilisation plus vite que Cost ; il faut donc choisir explicitement un mode plutôt que de considérer Auto comme un modèle fixe. Le router convient au contrôle des coûts et de la qualité à l'échelle d'une équipe, mais pas aux charges de travail qui exigent un modèle sous-jacent figé.

## Ligne de développement {#development-line}

- **2026-07-25 — Cursor a publié une mise à jour publique associée à Router.** Le 2026-07-25, Cursor a publié un article de blog public associé à Router. Cette publication marque une étape publique pour la ligne de développement de Cursor Router, mais Cursor n'a pas détaillé ses fonctionnalités, l'état de son déploiement ni son impact pour les utilisateurs.

## Ce qui a changé {#what-changed}

- 2026-07-25 — Cursor Router a remplacé le routage fixe d'Auto par une classification par requête et introduit les contrôles Cost, Balance et Intelligence pour les offres Teams et Enterprise.
- 2026-08-06 — Cursor a documenté l'approche de routage en deux étapes fondée sur l'apprentissage et a signalé des améliorations après le lancement, grâce à davantage de trafic en production.
- 2026-08-12 — Cursor a publié des recommandations de déploiement : l'activer d'abord pour une équipe très sollicitée, surveiller le coût par commit, puis n'élargir l'usage que si le résultat mesuré se confirme.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-25, consultez l'annonce de Cursor concernant Router avant de vous y fier ou de le configurer.

1. Dans le sélecteur de modèles de Cursor, sélectionnez Auto, puis choisissez Cost pour maîtriser les dépenses, Balance pour le compromis par défaut, ou Intelligence pour les tâches complexes en plusieurs étapes.
  — <https://prod.cursor.com/docs/cursor-router>
2. Pour une équipe Enterprise, activez Router dans le tableau de bord de l'équipe ; configurez les modes autorisés, l'accès aux modèles, la visibilité du modèle routé et, facultativement, l'application souple ou stricte d'Auto.
  — <https://prod.cursor.com/docs/cursor-router>
3. Dans le SDK Agent pour TypeScript ou Python, utilisez l'identifiant de modèle `auto-smart` et `optimize_for` défini sur `cost`, `balanced` ou `intelligence` ; appelez `Cursor.models.list()` avant de vous y fier pour une équipe.
  — <https://prod.cursor.com/docs/cursor-router>

## Bonnes pratiques {#best-practices}

- Testez Router avec une seule équipe active et mesurez le coût par commit pendant une semaine avant d'étendre le déploiement.
  — <https://cursor.com/guides/model-routing>
- Gardez activée une option de routage économique ; la documentation Enterprise de Cursor indique que bloquer trop de modèles peut réduire la qualité ou désactiver Router, et cite Cursor Grok 4.5 comme requis pour que Router fonctionne.
  — <https://prod.cursor.com/docs/cursor-router>
- Ne devinez pas quel modèle a répondu à partir du seul résultat : le modèle routé est masqué par défaut, et le pool peut changer à mesure que de nouveaux modèles sont publiés.
  — <https://prod.cursor.com/docs/cursor-router>

## Remplacé par ceci {#superseded-by-this}

- 2026-07-22 — considérer Auto comme un choix de modèle unique, stable et prévisible manuellement n'est plus valable pour les requêtes routées en Balance et Intelligence ; Cursor choisit désormais le modèle sous-jacent pour chaque requête.
- 2026-07-22 — selon la documentation actuelle, le comportement antérieur d'Auto ne subsiste que dans le mode Cost.

## Points encore inconnus {#still-unknown}

- Cursor ne publie pas de correspondance stable et exhaustive entre les types de requêtes et les noms de modèles sous-jacents ; le pool de modèles évolue dans le temps.
- Les chiffres publiés sur les économies et la satisfaction sont des mesures internes à Cursor, et non un benchmark reproductible et indépendant.
- Les changements de flux de travail spécifiques restent non vérifiés tant que l'article d'annonce n'a pas été analysé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://cursor.com/blog/router | Introducing Cursor Router | 2026-09-05 |
| https://cursor.com/changelog/router | Cursor Router changelog | 2026-09-05 |
| https://prod.cursor.com/blog/how-cursor-router-works | How Cursor Router chooses the right model for the task | 2026-09-05 |
| https://cursor.com/guides/model-routing | Model routing: right model, right job, right price | 2026-09-05 |
| https://prod.cursor.com/docs/cursor-router | Cursor Router documentation | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:router`, fil `router`, 1 événement daté du 2026-07-25 → 2026-07-25.
- **Note pratique :** À partir du 2026-07-25, consultez l'annonce de Cursor concernant Router avant de vous y fier ou de le configurer.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
