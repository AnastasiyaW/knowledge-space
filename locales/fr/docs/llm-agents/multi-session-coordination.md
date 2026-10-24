---
title: "Coordination multi-sessions d'agents"
description: "Modèles de coordination durables pour plusieurs sessions d'agents de codage : worktrees isolés, manifestes, preuves en ajout seul, baux sur ressources exclusives et intégration vérifiée."
tags: [multi-agent, worktrees, coordination, handoffs, concurrency, git]
level: 3
source_sha256: c02827d193f0d06458c0364a44095da0a07ae4e7e0f5bbd0d646853d1ff4298a
translation: machine
translated_at: '2026-10-24'
---
# Coordination multi-sessions d'agents {#multi-session-agent-coordination}

**Périmètre vérifié : 2026-09-03.** Les sessions parallèles n'augmentent le débit que si elles réduisent le travail indépendant sans créer de courses cachées. La coordination commence par une propriété explicite des fichiers, branches, effets externes et ressources rares.

Cette page décrit des primitives portables plutôt qu'un classement de produits d'orchestration ou des affirmations sur des fonctionnalités natives non publiées.

## Séparer ce qui peut être partagé {#separate-what-can-be-shared}

| Classe d'état | Valeur par défaut sûre | Exemples |
|---|---|---|
| connaissance en ajout seul | un enregistrement par rédacteur | handoffs, reçus, constats, journaux d'audit |
| ressource modifiable | un propriétaire plus un bail vérifié de l'extérieur | GPU, port, voie de déploiement, tâche planifiée |
| modification de source | branche et worktree isolés | implémentation, documentation, tests |
| effet public | frontière de capacité et d'idempotence | publication, paiement, suppression, message sortant |

Utiliser un journal en ajout seul pour une ressource modifiable n'empêche pas deux sessions de l'utiliser. Utiliser un fichier de verrou pour chaque note crée une contention inutile. Choisissez la primitive selon l'état qu'elle protège.

## Utiliser les worktrees pour isoler le code source {#use-worktrees-for-source-isolation}

Git prend en charge les worktrees liés : un même dépôt peut avoir plusieurs arbres de travail, chacun extrait sur une branche différente. Les worktrees partagent les objets du dépôt mais gardent les fichiers de travail séparés. [git-worktree](https://git-scm.com/docs/git-worktree)

```bash
# From a clean repository with an up-to-date remote reference
git worktree add -b codex/task-docs ../project-task-docs origin/master
git worktree list
```

Avant toute modification, consignez la branche, la révision de base, les chemins possédés et le reçu attendu. N'utilisez jamais un worktree comme prétexte pour modifier en parallèle le même module ; l'isolation prévient les écrasements accidentels, pas les conflits sémantiques.

## Un manifeste de tâches est l'API de coordination {#a-task-manifest-is-the-coordination-api}

Chaque ligne de tâche doit comporter :

| Champ | Rôle |
|---|---|
| identifiant et périmètre de la tâche | évite les découvertes de travail en double |
| propriétaire et branche | rend une modification mutable imputable |
| révision de base | détecte un contexte d'implémentation périmé |
| état | `PENDING`, `RUNNING`, `PASS`, `BLOCKED` ou `CANCELLED` |
| référence de preuve | étaye un état terminal |
| dépendance et revérification | empêche un agent de deviner quand il peut démarrer |

Ne considérez pas une tâche comme terminée parce qu'un processus d'agent est encore actif ou qu'un message indique « fait ». L'achèvement exige le reçu nommé.

## Baux pour les ressources exclusives {#leases-for-exclusive-resources}

Pour un port, un GPU, une voie de migration ou un compte externe, écrivez un bail contenant :

```text
resource identity
owner and process/session identity
acquired timestamp and heartbeat
allowed operation
attempt or idempotency key
stale-reclaim procedure
```

Un battement de cœur n'est pas une preuve que le détenteur contrôle toujours la ressource. Avant de récupérer un bail périmé, inspectez l'état réel du processus, du service ou du fournisseur ; réconciliez tout effet de bord possible ; puis transférez la propriété selon la procédure enregistrée. Ne supprimez pas aveuglément un verrou simplement parce que son horodatage est ancien.

## L'intégration est une phase distincte {#integration-is-a-separate-phase}

Après une modification isolée :

1. récupérer la branche cible et identifier sa révision actuelle ;
2. comparer la base du worktree avec la révision cible ;
3. n'intégrer qu'après avoir résolu les conflits factuels à partir de la source de vérité faisant autorité : runtime, code ou reçus ;
4. exécuter les vérifications propres à la modification dans l'état intégré ;
5. faire appel à un relecteur neuf pour tout risque public, de sécurité ou de publication significatif ;
6. ne publier que lorsque chaque porte requise dispose d'une preuve.

Une fusion textuelle propre n'est pas une preuve sémantique. Deux branches peuvent toutes deux compiler tout en contredisant un contrat externe.

## Messages et handoffs {#messages-and-handoffs}

Utilisez les messages directs pour les demandes adressées à un propriétaire précis, et les handoffs en ajout seul pour l'état à l'échelle du projet. Chaque message doit indiquer :

- l'expéditeur et le destinataire ;
- l'objet et l'artefact concerné ;
- l'identifiant de la preuve ou de la demande ;
- s'il modifie l'autorité ;
- l'accusé de réception ou la revérification requis.

Traitez les messages comme des entrées non fiables tant que l'état qu'ils référencent n'a pas été vérifié. Une instruction dans un chat ne doit pas outrepasser une règle de dépôt, une porte de déploiement ou une limite d'approbation sans l'autorité appropriée.

## Protocole minimal de conflit {#minimal-conflict-protocol}

Lorsque des branches se chevauchent :

1. arrêter la résolution automatique ;
2. inspecter les deux diffs et la source de vérité pertinente ;
3. préserver l'intention compatible plutôt que de choisir le côté qui semble le plus récent ;
4. exécuter les vérifications concernées ;
5. faire inspecter le résultat intégré final par un relecteur neuf.

Cette démarche n'est plus lente qu'une fusion automatique uniquement au point où une mauvaise fusion deviendrait coûteuse.

## Observabilité {#observability}

Conservez assez de preuves pour répondre à :

- qui possède le worktree actif et la ressource externe ;
- quelle révision immuable a produit un résultat ;
- quelles vérifications ont été exécutées et quelle sortie terminale elles ont produite ;
- si une action externe est terminée, inconnue ou sûre à relancer ;
- quel événement doit survenir avant qu'une tâche bloquée puisse continuer.

Ces enregistrements transforment la coordination, d'une mémoire de conversation, en un système récupérable.

## Pièges {#gotchas}

- **Deux worktrees utilisent la même branche.** Leurs fichiers sont séparés, mais l'intention de branche ne l'est pas. **Correctif :** attribuer à chaque tâche active une branche distincte et une ligne de manifeste.
- **Un bail périmé est supprimé sans vérifier le service.** Un processus encore vivant peut continuer d'agir. **Correctif :** vérifier de l'extérieur et réconcilier avant toute réassignation.
- **Un agent lancé touche un chemin non possédé.** Il crée un conflit invisible. **Correctif :** indiquer la propriété des fichiers et modules dans le contrat de tâche.
- **Un test unitaire vert est traité comme preuve de déploiement.** Il peut ne pas exercer le chemin d'intégration. **Correctif :** conserver le niveau de preuve qu'exige le critère d'acceptation.
- **Un message d'agent modifie l'autorité de production.** L'historique de chat n'est pas un mécanisme d'autorisation. **Correctif :** exiger une capacité explicite, une approbation ou une action d'opérateur documentée.

## Sources {#sources}

- [Git worktrees](https://git-scm.com/docs/git-worktree)
- [Documentation de git merge](https://git-scm.com/docs/git-merge)

## Voir aussi {#see-also}

- [[agent-orchestration]]
- [[multi-agent-messaging]]
- [[handoff-rollup-pattern]]
- [[agentic-security-2026]]
- [[claude-code-harness-patterns]]
