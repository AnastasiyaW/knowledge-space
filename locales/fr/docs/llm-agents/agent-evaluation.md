---
title: "Évaluation des agents et preuves"
description: "Évaluez le comportement des agents à l'aide de fixtures de tâches versionnées, de validateurs déterministes, de contrôles d'effets de bord maîtrisés et de preuves reproductibles, plutôt que d'un score de benchmark unique."
tags: [llm-agents, evaluation, testing, benchmarks, evidence, swe-bench]
level: 4
source_sha256: b9bcbe8f4f828d916e5204b2e1cfdfcda95f22c3d63ab7af71d6aecc19e219a7
translation: machine
translated_at: '2026-10-24'
---
# Évaluation des agents et preuves {#agent-evaluation-and-evidence}

**Périmètre vérifié : 2026-09-06.** Une exécution d'agent combine un modèle avec des instructions, des outils, un état, des données, des permissions et un environnement d'exécution. Un résultat de benchmark peut constituer une preuve utile pour un harnais précisément défini ; il ne démontre pas qu'une intégration en production est sûre, à jour ou adaptée à une autre tâche.

## Définir l'objet de l'évaluation {#define-the-evaluation-object}

Précisez exactement ce qui est évalué avant de comparer les résultats :

- fixture de tâche et révision immuable des entrées ;
- instructions de l'agent, configuration du modèle et versions des outils ;
- autorité disponible, périmètre des données et environnement ;
- résultat attendu et effets de bord interdits ;
- ordre des validateurs et décision de mise en production que le résultat peut justifier.

Un enregistrement d'évaluation reproductible lie ces éléments entre eux.

```json
{
  "run_id": "support-triage-2026-09-04-a",
  "source_revision": "immutable commit or content digest",
  "fixture_revision": "versioned test data",
  "agent_configuration": "policy and tool configuration digest",
  "authority": "local test only",
  "validators": ["schema", "unit", "sandboxed integration"],
  "result": "pass | fail | blocked",
  "evidence": ["test output", "external receipt if applicable"]
}
```

Ne réutilisez pas un ancien identifiant d'exécution après avoir modifié la fixture, la révision des sources, l'environnement ou la configuration. Cela rendrait ambiguë la réutilisation du cache et la comparaison avec l'historique.

## Évaluer plus que l'achèvement de la tâche {#evaluate-more-than-task-completion}

| Dimension | Question | Preuve pratique la plus solide |
|---|---|---|
| résultat fonctionnel | la tâche a-t-elle satisfait ses critères d'acceptation ? | test déterministe ou artefact validé |
| qualité | la réponse est-elle exacte, complète et utilisable par son public ? | grille d'évaluation avec relecture humaine calibrée ou juge par modèle |
| sécurité et effets de bord | l'exécution a-t-elle évité les accès ou modifications interdits ? | journal des capacités, trace du bac à sable et accusés de réception externes |
| autorité | l'agent est-il resté dans les outils, données et approbations autorisés ? | politique effective et audit des appels d'outils |
| comportement opérationnel | les nouvelles tentatives, délais d'attente et ressources utilisées sont-ils restés dans le budget déclaré ? | télémétrie d'exécution structurée |
| reproductibilité | un relecteur peut-il relancer ou inspecter les mêmes conditions ? | fixture, configuration et preuves conservées et versionnées |

La métrique pertinente découle du contrat de la tâche. Un faible nombre d'appels d'outils n'est pas intrinsèquement meilleur s'il évite la validation ; une réponse rapide et réussie n'est pas une action de production sûre sans le justificatif requis.

## Ordre des validateurs {#validator-order}

Exécutez d'abord les contrôles les moins coûteux et les plus déterministes, puis seulement le jugement subjectif :

1. valider les schémas, les permissions et les contraintes statiques ;
2. exécuter les tests unitaires ou de fixture dans un environnement maîtrisé ;
3. lancer les contrôles d'intégration autorisés sur des cibles isolées ou réversibles ;
4. inspecter l'état externe et conserver les accusés de réception lorsqu'une action est permise ;
5. recourir à une relecture humaine calibrée ou à des juges par modèle pour les qualités qu'un test déterministe ne peut pas trancher.

Le code généré et les appels d'outils ne doivent pas recevoir une autorité locale ou de production illimitée pour simplifier l'évaluation. Utilisez le bac à sable ou la fixture de test le plus petit permettant d'établir le comportement pertinent. L'impossibilité d'observer une condition externe constitue un résultat bloqué ou incomplet, et non un succès automatique.

## Les exécutions stochastiques exigent un reporting transparent {#stochastic-runs-need-transparent-reporting}

Lorsqu'un agent échantillonne de manière non déterministe, conservez le résultat de chaque exécution et présentez la distribution pertinente pour la décision : nombre de succès et d'échecs, variance du coût ou de la latence, catégories d'erreurs et effets de bord observés. Utilisez un ensemble de tâches fixe pour les comparaisons, conservez un ensemble de contrôle (holdout) pour les tests de régression et signalez toute modification de configuration.

Choisissez le nombre de répétitions et le budget en fonction du risque, de la variance attendue et du coût d'une mauvaise décision. Il n'existe pas de nombre d'échantillons universel qui transforme un résultat d'agent en preuve. Si une mise en production exige un intervalle de confiance, définissez-le dans le plan d'évaluation avant de lancer l'expérience.

## Les benchmarks sont des harnais, non des certificats de production {#benchmarks-are-harnesses-not-production-certificates}

[SWE-bench](https://github.com/SWE-bench/SWE-bench) évalue des tâches d'ingénierie logicielle à travers un jeu de données et un harnais d'exécution spécifiques. Son outillage en ligne de commande actuel enregistre un identifiant d'exécution et peut ignorer les instances qui disposent déjà d'un rapport pour cette exécution. Considérez l'identifiant d'exécution, le sous-ensemble de tâches, l'environnement et la version du harnais comme faisant partie de l'identité du résultat ; sinon, un résultat mis en cache pourrait être pris pour une évaluation fraîche. [Référence CLI de SWE-bench](https://www.swebench.com/SWE-bench/reference/cli/)

Un benchmark peut révéler une régression ou comparer un système défini à sa version précédente. Il ne peut pas démontrer que les tests d'un dépôt passent, que les identifiants d'une organisation sont protégés, ou qu'un déploiement externe s'est comporté correctement. Conservez ces éléments comme des cellules de preuve distinctes.

## Barrière de mise en production {#release-gate}

Une décision de mise en production doit nommer les preuves requises pour son niveau de risque :

| Classe de changement | Preuves minimales |
|---|---|
| modification de texte ou locale non exécutable | validation des liens et de la compilation, et relecture éditoriale |
| modification de code sans effet externe | tests automatisés pertinents, revue de différences et révision des sources |
| intégration avec une cible de test réversible | accusé de réception d'intégration maîtrisé et vérification du chemin d'échec |
| effet externe ou en production | autorité explicite, plan d'idempotence et de retour arrière, accusé de réception frais de la cible et revue indépendante |

Un score agrégé unique est un signal de tableau de bord, et non un substitut à la barrière individuelle qui protège un utilisateur, une base de données, un paiement, un déploiement ou une affirmation publiée.

## Faire correspondre l'affirmation d'achèvement aux preuves {#match-the-completion-claim-to-the-evidence}

Utilisez des niveaux de preuve distincts plutôt qu'un unique `PASS` indifférencié. Ce qui suit est une convention de reporting d'ingénierie, et non une taxonomie de statuts d'un SDK.

| Niveau observé | Ce qui est établi | Ce qui reste non démontré |
|---|---|---|
| revue des sources | la révision inspectée contient l'instruction ou l'implémentation prévue | si un système actif la charge effectivement |
| fixture ciblée | les entrées et assertions nommées ont réussi dans l'environnement enregistré | le comportement hors de ces cas ou dans un autre runtime |
| installation et enregistrement | les octets attendus sont installés et le point d'entrée actif les sélectionne | si une invocation réelle atteint la branche modifiée |
| workflow consommateur | le parcours utilisateur demandé a produit le résultat spécifié dans l'environnement nommé | les parcours non concernés, versions, charges et dimensions de qualité |

Le niveau requis découle de la demande. La revue d'un fichier d'instructions peut compléter un audit de sources. Elle ne satisfait pas une demande d'installation de ces instructions et de démonstration de leur effet. Un double de test peut prouver un contrat d'interaction local ; il ne peut pas établir que le service réel a accepté une requête. Conservez ensemble l'entrée, la révision, l'assertion, l'observation réelle et l'affirmation justifiée.

L'enregistrement lui-même peut masquer des lacunes d'atteignabilité. Dans le SDK OpenAI Agents pour TypeScript, les garde-fous d'entrée s'appliquent au premier agent, les garde-fous de sortie à la sortie finale, et les garde-fous d'outils aux appels de fonctions-outils pris en charge. Les contrôles d'entrée peuvent s'exécuter en parallèle de l'agent. Par conséquent, voir un garde-fou dans la configuration n'établit pas qu'il s'est exécuté avant chaque effet de bord. Vérifiez le chemin réel et le mode d'exécution. [Portée et exécution des garde-fous du SDK](https://openai.github.io/openai-agents-js/guides/guardrails/)

## Poursuivre jusqu'au résultat accepté, et non jusqu'au rapport suivant {#continue-until-the-accepted-outcome-not-until-the-next-report}

Un contrat d'achèvement utile relie le résultat demandé à la prochaine action exécutable et à ses preuves d'acceptation. Une constatation, une revue, une passation ou une tentative échouée modifie cet état ; elle ne clôt pas automatiquement la tâche.

| Observation actuelle | Action dans le cadre de la tâche et de l'autorité existantes | Preuve terminale |
|---|---|---|
| défaut d'implémentation local reproductible | appliquer une correction causale, puis relancer le contrôle concerné | comportement corrigé sur le cas en échec et les contrôles pertinents |
| travail terminé sur une branche mais non installé | finaliser la livraison demandée par la voie établie | révision des sources, résultat d'installation et contrôle consommateur requis |
| processus terminé sans résultat final | réconcilier les effets partiels avant une réparation idempotente ou une reprise | sortie complète ou limite documentée empêchant la poursuite |
| approbation requise ou dépendance externe réellement indisponible | conserver le travail partiel et identifier la décision en attente exacte ou la vérification à relancer | refus observé, approbation en attente ou réponse de la dépendance |
| tous les critères acceptés disposent de preuves suffisantes | clôturer la tâche | correspondance critères-preuves, avec les limites de preuve énoncées |

Il s'agit d'une politique opérationnelle dérivée de la séparation entre l'état de la tâche et les messages de l'agent. Ce n'est pas un mandat pour réessayer indéfiniment ou étendre l'autorité. Un test local échoué n'est pas, à lui seul, un blocage externe. À l'inverse, un objectif d'achèvement n'autorise ni la suppression, ni une nouvelle destination de publication, ni une modification de production non approuvée.

Le SDK prend en charge à la fois l'orchestration dirigée par le modèle et un flux de contrôle explicite en code. Une transition d'état déterministe convient lorsque l'action suivante découle d'une condition connue ; le jugement d'un modèle de langage reste utile pour le diagnostic. Lorsqu'un outil exige réellement une approbation, le mécanisme human-in-the-loop conserve l'exécution interrompue pour une approbation ou un rejet explicite, au lieu de considérer l'outil comme exécuté. [Orchestration des agents](https://openai.github.io/openai-agents-js/guides/multi-agent/), [approbation et reprise](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

Ne compensez pas un arrêt prématuré par des cycles de revue supplémentaires obligatoires. Relancez les contrôles lorsqu'un critère échoue, qu'une dépendance change ou qu'un risque matériel nouvellement observé invalide leurs preuves antérieures. Conservez les résultats encore valides pour les zones inchangées. Arrêtez d'élargir le périmètre dès que l'ensemble du périmètre accepté est satisfait ; les améliorations facultatives relèvent d'une décision distincte. Pour les travaux concurrents, liez chaque résultat à son responsable et à sa révision : [[multi-session-coordination]], [[swarm-based-review-and-multisampling-in-agentic-workflows]].

## Pièges courants {#gotchas}

- **Substitution par le benchmark :** prendre un score pour une preuve d'un workflow de production sans rapport.
- **Fixtures mutables :** les résultats ne peuvent pas être comparés parce que les données de la tâche ont changé silencieusement.
- **Ambiguïté du cache :** réutiliser un identifiant d'exécution pour des codes ou configurations différents.
- **Acceptation par le seul juge :** un modèle déclare le succès sans preuve déterministe ou externe.
- **Évaluation non sûre :** le code généré reçoit un accès réseau, aux identifiants ou à la production sans cible de test bornée.
- **Reporting par la seule moyenne :** les échecs rares et les cas extrêmes coûteux disparaissent derrière un chiffre de synthèse.
- **Rapport tenu pour résultat :** une constatation ou une revue réussie est enregistrée comme terminale alors que l'installation ou le parcours utilisateur demandé manque encore.
- **Installation tenue pour exécution :** la concordance des empreintes installées est présentée comme la preuve qu'une requête réelle a exercé le comportement modifié.
- **Auto-alimentation des revues :** une revue réussie déclenche une nouvelle revue générique sans changement de risque, laissant la livraison acceptée inachevée.

## Limites {#limitations}

Ces conventions organisent les preuves ; elles ne démontrent ni que le critère d'acceptation est suffisant, ni que le juge automatique a raison. La qualité visuelle, la validité métier et les défaillances peu fréquentes peuvent exiger des mesures différentes. Une observation bornée ne peut pas établir l'absence universelle de défaillances. Explicitez les conditions non testées, plutôt que de transformer l'incertitude ou un contrôle local vert en affirmation sur l'ensemble du produit.

## Références {#references}

- [Documentation OpenAI Evals](https://platform.openai.com/docs/guides/evals) — concepts actuels pour les définitions d'évaluation, les exécutions et les correcteurs (graders).
- [Dépôt SWE-bench](https://github.com/SWE-bench/SWE-bench) et [référence CLI](https://www.swebench.com/SWE-bench/reference/cli/) — comportement du benchmark et des artefacts d'exécution.
- [NIST AI RMF : Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — cadrage des risques pour l'évaluation de l'IA générative.
