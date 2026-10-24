---
title: "Évolution autonome d'agents"
description: "Exécuter des expériences d'agents en parallèle de façon sûre grâce à des worktrees isolés, des preuves en ajout seul, des verrous sur les ressources et une évaluation indépendante"
level: 3
source_sha256: fd7adfe8af09f6d68cbe6f4efb6b7d7a7df59243206c8ba7fc75b844620ba0f4
translation: machine
translated_at: '2026-10-24'
---
# Évolution autonome d'agents (septembre 2026) {#autonomous-agent-evolution-september-2026}

Contexte de version : cette page décrit une architecture d'expérimentation contrôlée, et non l'affirmation que des agents autonomes devraient modifier des systèmes de production. Épinglez la révision du dépôt, l'évaluateur, le manifeste des tâches, l'image d'environnement et la politique de ressources pour chaque exécution.

Des agents en parallèle peuvent explorer des modifications candidates indépendantes, mais seulement lorsque le travail dispose d'un objectif mesurable, d'un espace de mutation isolé et d'une voie de promotion qui rejette les résultats non étayés.

## Critères d'admission {#admission-gate}

Ne lancez pas une exécution d'évolution en parallèle tant que toutes les conditions suivantes ne sont pas réunies :

1. Un manifeste de tâches énumère chaque unité de travail candidate.
2. Un évaluateur déterministe ou pouvant faire l'objet d'une revue indépendante existe.
3. Chaque worker dispose d'une branche/d'un worktree ou d'un bac à sable isolé.
4. Les ressources mutables partagées disposent de verrous explicites et d'une vérification externe.
5. Les artefacts de sortie ont des identifiants stables, des empreintes (digests) et une politique de rétention.
6. Un coordinateur est responsable de la promotion, du retour arrière et de la comptabilité finale.

Sans ces conditions, les agents parallèles produisent des modifications concurrentes et des récits non vérifiés plutôt que des preuves.

## Modèle d'isolation {#isolation-model}

Les worktrees Git permettent plusieurs branches extraites d'un même dépôt. Ils isolent les modifications de fichiers par branche, mais n'isolent pas les processus, l'accès réseau, les identifiants, les lecteurs montés ni les ressources cloud.

```text
coordinator
  ├── worker-a: worktree + branch + task shard
  ├── worker-b: worktree + branch + task shard
  └── evaluator: fresh context, read-only evidence review
shared: append-only receipts + explicit resource locks
```

Utilisez des contrôles au niveau de l'environnement lorsque les workers ne doivent pas partager de secrets, de capacité GPU, de ports, de bases de données ou d'identifiants de services externes.

## Travail adossé à un manifeste {#manifest-backed-work}

```json
{
  "run_id": "evolution-2026-09-03",
  "baseline_commit": "abc123",
  "evaluator_revision": "git:eval456",
  "objective": "accepted_task_rate",
  "guard_metrics": {"policy_violations_max": 0},
  "shards": [
    {"id": "A", "state": "pending", "owner": null},
    {"id": "B", "state": "pending", "owner": null}
  ],
  "promotion_state": "hold"
}
```

Un lot (shard) n'est terminé qu'après avoir obtenu un reçu d'évaluation terminal. Un processus worker, une branche ou un message de progression ne prouve pas l'achèvement.

## Protocole du worker {#worker-protocol}

Pour chaque lot assigné :

1. Vérifiez que le lot est toujours `pending` sous le verrou du manifeste.
2. Créez ou réservez un worktree/une branche isolé(e) à partir de la base enregistrée.
3. Appliquez une seule modification candidate bornée.
4. Exécutez l'évaluateur nommé et conservez le résultat brut, l'empreinte, l'environnement et l'identifiant de commit.
5. Marquez le lot `passed`, `rejected` ou `blocked_external` avec une raison.
6. N'envoyez au coordinateur que des références de preuves ; ne promouvez jamais directement vers la base.

Un worker ne doit pas reprendre une tâche déjà tentée sans avoir réconcilié le reçu précédent et la clé d'idempotence.

## Connaissance partagée sans conditions de course {#shared-knowledge-without-races}

Conservez les informations partagées dans deux catégories :

| État | Représentation sûre | Règle |
|---|---|---|
| Preuves, observations, reçus | Fichiers en ajout seul par exécution | Ne jamais réécrire l'enregistrement d'un autre worker |
| Verrous, réservations, gagnant courant | Un fichier par ressource | Revendiquer de manière atomique ; vérifier l'état externe avant toute récupération |

Exemple de reçu :

```json
{
  "shard_id": "A",
  "candidate_commit": "def456",
  "parent_commit": "abc123",
  "evaluator_digest": "sha256:...",
  "primary_metric": 0.0,
  "guards": {"policy_violations": 0},
  "verdict": "rejected",
  "recorded_at": "2026-09-03T18:00:00Z"
}
```

Les observations sont utiles mais ne constituent pas des instructions partagées. Traitez les notes rédigées par les agents comme des hypothèses non fiables tant que l'évaluateur ou la source de référence ne les a pas confirmées.

## Sélection et promotion {#selection-and-promotion}

Le coordinateur ne compare que les reçus produits par la même révision de l'évaluateur et dans un environnement comparable. Un candidat ne l'emporte que s'il améliore l'objectif principal et réussit toutes les garde-fous.

```text
candidate receipt -> independent evaluator -> selection record
                  -> integration test -> staged/canary evidence -> promotion
```

Utilisez un contexte d'évaluateur neuf pour l'acceptation finale. Le worker ayant effectué une modification ne peut pas certifier lui-même la justesse sémantique de celle-ci.

## Verrous sur les ressources {#resource-locks}

Git n'est pas un gestionnaire de verrous pour les GPU, les ports, les bases de données, les files d'attente distantes ni les URL externes. Pour chaque ressource mutable, enregistrez le propriétaire, le battement de cœur (heartbeat), l'identifiant de processus ou de réservation, le budget de tentatives et la procédure de récupération.

Avant de récupérer un verrou périmé, vérifiez de l'extérieur que le processus propriétaire ou l'opération distante n'est plus active. Ne déduisez pas qu'une ressource est libre à partir d'un simple horodatage ancien.

## Stagnation et conditions d'arrêt {#stagnation-and-stop-conditions}

Arrêtez ou réorientez une exécution lorsque :

- chaque lot dispose d'un reçu terminal ;
- l'évaluateur est invalide ou indisponible ;
- des candidats répétés régressent selon la même mesure ;
- un garde-fou de ressources ou de sécurité est déclenché ;
- le budget configuré de tentatives, de coût ou de temps est atteint.

Changer la métrique après un plateau constitue une nouvelle expérience, et non une poursuite de la précédente. Conservez les preuves des candidats rejetés afin que les futurs workers ne répètent pas le même candidat échoué.

## Pièges {#gotchas}

- **Les worktrees ne constituent pas une isolation complète.** Ils partagent les processus, les identifiants et les ressources montées de l'hôte. **Correctif :** ajoutez une isolation au niveau de l'environnement et des verrous par ressource lorsque nécessaire.
- **Les messages de progression parallèles peuvent masquer des travaux en double.** Deux workers peuvent évaluer le même candidat. **Correctif :** réservez les lots dans un manifeste avec une clé d'idempotence et une vérification du reçu.
- **Les notes partagées peuvent propager une hypothèse erronée.** Le résumé d'un agent peut être faux ou périmé. **Correctif :** reliez chaque observation réutilisable à un reçu d'évaluateur ou à une source primaire.
- **Un score plus élevé peut être une comparaison invalide.** Un environnement, une graine, des données ou une révision d'évaluateur différents modifient l'expérience. **Correctif :** ne comparez que des reçus compatibles et consignez toutes les entrées significatives.
- **La promotion automatique est une escalade d'autorité.** Un test de worker réussi n'autorise pas la modification de la production. **Correctif :** exigez une évaluation indépendante, des preuves d'intégration et un responsable de mise en production défini.

## Sources {#sources}

- [Documentation de git worktree](https://git-scm.com/docs/git-worktree)
- [OpenAI API : travailler avec les evals](https://developers.openai.com/api/docs/guides/evals)
- [SDK Agents d'OpenAI : orchestration d'agents](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [SDK Agents d'OpenAI : traçage](https://openai.github.io/openai-agents-python/tracing/)

## Voir aussi {#see-also}

- [[agent-self-improvement]]
- [[agent-evaluation]]
- [[multi-agent-systems]]
- [[agent-architectures]]
- [[production-patterns]]
