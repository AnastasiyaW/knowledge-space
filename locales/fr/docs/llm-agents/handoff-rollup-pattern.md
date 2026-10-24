---
title: "Synthèses de passation de session"
description: "Comment créer une synthèse bornée et auditable du travail d'agent de longue durée, sans prétendre qu'un résumé est sans perte."
tags: [handoff, continuity, context-management, agent-operations, documentation]
level: 3
source_sha256: 07890b896ab508e075fe1b8d8d6f7ce0837027ca93ee8fa1418e6f0ad0859ffa
translation: machine
translated_at: '2026-10-24'
---
# Synthèses de passation de session {#session-handoff-rollups}

**Périmètre vérifié : 2026-09-03.** Une synthèse est un instantané daté qui aide l'opérateur suivant à reprendre un projet. Ce n'est pas un substitut à l'historique source, une garantie de compression sans perte, ni une raison d'effacer les justificatifs qui ont étayé les décisions antérieures.

Le jeu de reprise sûr est constitué d'une synthèse vérifiée et de la queue bornée des entrées enregistrées après son point de coupure.

## Pourquoi une synthèse existe {#why-a-rollup-exists}

Les travaux de longue durée accumulent de petites passations : actions terminées, contraintes actives, tentatives échouées et approbations en attente. Ne lire que la passation la plus récente peut faire perdre une décision toujours valide. Lire toutes les notes historiques est lent et risque de faire remonter un contexte périmé.

Une synthèse répond à quatre questions :

1. Quels enregistrements source exacts couvre-t-elle ?
2. Qu'est-ce qui est vérifié, rapporté, bloqué ou inconnu au point de coupure ?
3. Quels artefacts, révisions et justificatifs restent faisant autorité ?
4. Quelles entrées une nouvelle session doit-elle lire après le point de coupure ?

## Le contrat de l'instantané {#the-snapshot-contract}

Utilisez un frontmatter explicite et des références source stables :

```yaml
---
project: example-project
status: ACTIVE
as_of: 2026-09-03T20:15:00Z
covered_sources:
  - handoff-2026-08-30-a
  - handoff-2026-09-01-b
source_index_ref: handoffs/INDEX.md
verification_ref: receipts/rollup-2026-09-03.json
---
```

`as_of` correspond au dernier événement source inclus, et non au moment où quelqu'un a rédigé le résumé. Un lecteur charge :

```text
current rollup
  + source index
  + every entry after as_of
  + artifacts named by the current task
```

La queue doit rester bornée. Créez une nouvelle synthèse à une frontière de phase, ou lorsque l'index montre qu'une reprise normale nécessite de nouveau trop d'enregistrements source.

## Préserver l'attribution et le niveau de confiance {#preserve-attribution-and-confidence}

Chaque affirmation importante doit être traçable :

| Champ | Signification |
|---|---|
| claim | énoncé concis de l'état actuel |
| confidence | `VERIFIED`, `REPORTED`, `UNKNOWN` ou `BLOCKED` |
| evidence reference | sortie de test, commit, ticket, justificatif d'exécution ou rapport utilisateur |
| owner | qui peut agir sur l'étape suivante |
| recheck | événement ou commande susceptible de modifier l'affirmation |

Cela empêche un résumé de transformer un diagnostic provisoire en fait établi. Lorsqu'une source manque ou qu'une affirmation ne peut pas être reproduite, marquez-la `UNKNOWN` ; ne comblez pas le vide à partir de la mémoire conversationnelle.

## Procédure de synthèse sûre {#safe-rollup-procedure}

1. inventorier les identifiants de passation, commits, justificatifs et branches actives à couvrir ;
2. choisir un point de coupure immuable et l'enregistrer ;
3. extraire uniquement les décisions, contraintes, résultats vérifiés, échecs et autorités encore ouvertes ;
4. attacher une référence source à chaque conclusion importante ;
5. comparer la synthèse avec l'index source et tester le chemin de reprise énoncé ;
6. publier la synthèse comme nouvel artefact en ajout seul ;
7. laisser les passations ultérieures dans la queue pour la synthèse suivante.

N'écrasez pas les passations d'origine pour rendre la synthèse plus propre. Si un index a besoin d'une relation, ajoutez une ligne d'index ou une référence inverse, après avoir vérifié que des écrivains concurrents ne peuvent pas la perdre.

## Le travail parallèle exige une frontière de coupure {#parallel-work-requires-a-cut-boundary}

Ne synthétisez pas un projet vivant et ramifié comme s'il était séquentiel. Au point de coupure :

- enregistrez chaque branche active et chaque worktree ;
- identifiez les baux de ressources et leurs propriétaires ;
- traitez les modifications non fusionnées comme `RUNNING`, et non comme terminées ;
- enregistrez les messages ou justificatifs encore en transit ;
- conservez dans la queue les nouvelles écritures postérieures à la coupure.

Si l'instantané ne peut pas nommer ses écrivains et ses artefacts, reportez-le plutôt que de fabriquer une image complète.

## Structure d'une synthèse {#rollup-structure}

```text
purpose and scope
covered source IDs and cut point
verified current state
active work and owners
decisions and rejected paths
known failures and evidence
release or publication gates
next safe action and recheck
tail-reading rule
```

La prochaine action sûre est une aide à la continuation, et non une commande permettant de contourner une approbation, de rejouer un effet irréversible ou de modifier un projet sans rapport.

## Valider avant réutilisation {#validate-before-reuse}

Avant qu'une nouvelle session n'agisse sur une synthèse :

1. confirmez que la révision de dépôt citée ou l'état d'exécution existe toujours ;
2. vérifiez si l'événement de recheck s'est produit ;
3. lisez toutes les entrées de la queue postérieures à `as_of` ;
4. vérifiez tout bail de ressource de manière externe avant d'en prendre la propriété ;
5. créez un nouvel instantané lorsque l'actuel est périmé.

Cela rend la passation utile même lorsqu'une session précédente s'est terminée de façon inattendue.

## Pièges courants {#gotchas}

- **Une synthèse n'a pas de point de coupure explicite.** Les lecteurs ne peuvent pas savoir ce qu'il faut ajouter. **Correctif :** enregistrez `as_of` et les identifiants des sources couvertes.
- **Un résumé présente tout l'état comme terminé.** Il masque les vérifications échouées et les autorités en attente. **Correctif :** utilisez les niveaux de confiance et les libellés d'état terminal, accompagnés de justificatifs.
- **Des agents concurrents modifient le même index.** Le dernier écrivain peut supprimer une autre relation. **Correctif :** privilégiez des enregistrements en ajout seul ou sérialisez la mise à jour de l'index mutable.
- **La queue devient aussi volumineuse que l'historique d'origine.** La synthèse n'améliore plus la récupération. **Correctif :** créez un nouvel instantané daté après la prochaine frontière de phase vérifiée.
- **Une ancienne synthèse est traitée comme une politique en vigueur.** Elle peut réintroduire des décisions périmées. **Correctif :** vérifiez son `as_of`, ses justificatifs et ses règles de recheck avant d'agir.

## Voir aussi {#see-also}

- [[multi-session-coordination]]
- [[session-persistence]]
- [[agent-memory]]
- [[claude-code-harness-patterns]]
