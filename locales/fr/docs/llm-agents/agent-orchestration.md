---
title: "Orchestration d'agents"
description: "Coordonner les appels de modèles, les outils, les transferts, les approbations, les nouvelles tentatives et les preuves via un état de tâche explicite plutôt qu'une boucle d'agent propre à un framework."
tags: [llm-agents, orchestration, workflows, multi-agent, state-machine, approvals, observability]
level: 3
source_sha256: b4b4897397c6c55fa24fe0f9c734fba9795a491cbbc65117b8b93f0fa99ddb66
translation: machine
translated_at: '2026-10-24'
---
# Orchestration d'agents (septembre 2026) {#agent-orchestration-september-2026}

Contexte de version : les frameworks d'orchestration, les SDK, les versions de protocoles, les backends de stockage et la sémantique des outils des modèles évoluent rapidement. Concevez d'abord l'état de la tâche, la frontière d'autorisation et les preuves terminales ; ne sélectionnez un framework qu'une fois ces contrats clairs.

L'orchestration d'agents est l'exécution contrôlée d'une tâche à travers des appels de modèles, du code déterministe, des outils, des agents, des personnes et un état durable. Ce n'est pas un synonyme de « laisser plusieurs agents discuter entre eux ». L'orchestrateur gère le cycle de vie de la tâche et prouve si un effet demandé s'est produit.

## Définir le contrat durable de la tâche {#define-the-durable-task-contract}

```json
{
  "task_id": "publish-research-044",
  "schema_version": "agent-task/v1",
  "objective": "prepare a cited draft for review",
  "input_refs": ["artifact:source-manifest-44"],
  "owner": "editorial-platform",
  "state": "PENDING",
  "tool_policy_revision": "tools@9",
  "approval_policy_revision": "review@4",
  "idempotency_key": "publish-research-044:v1",
  "attempt": 0
}
```

L'enregistrement de la tâche appartient à l'application. Il ne contient que des références vers des données contrôlées et persiste à travers les redémarrages de workers, les déconnexions du navigateur et les transferts entre agents.

## Modéliser séparément les états et les reçus {#model-states-and-receipts-separately}

Utilisez des états non terminaux pour décrire le travail en cours, et des états terminaux mutuellement exclusifs pour le résultat de la tâche. Les transitions légales doivent inclure une décision d'approbation, une expiration et une annulation :

```text
PENDING -> RUNNING -> COMPLETED | FAILED
RUNNING -> NEEDS_APPROVAL
NEEDS_APPROVAL + bound approved receipt -> RUNNING
NEEDS_APPROVAL + denied or expired receipt -> CANCELLED
any non-terminal state -> CANCELLED

verification status: PENDING | VERIFIED | REJECTED
```

Chaque transition est accompagnée d'un reçu. Un reçu terminal contient la référence de sortie, le résultat du validateur, le reçu de l'effet externe le cas échéant, la classification de la nouvelle tentative et les révisions de configuration. La tâche ne reprend depuis `NEEDS_APPROVAL` que si le reçu d'approbation est lié à la tâche exacte, à l'effet, au condensat (digest) des arguments, à l'acteur, au périmètre, à l'expiration et à la clé d'idempotence. Le statut de vérification est une revue de preuves terminales immuables : `REJECTED` ne prétend pas qu'un effet externe déjà réalisé ne s'est jamais produit, et `VERIFIED` n'autorise pas un nouvel effet.

## Séparer le contrôle déterministe du jugement du modèle {#separate-deterministic-control-from-model-judgment}

Utilisez du code déterministe pour :

- l'autorisation, le périmètre du tenant, les budgets, les limites de débit et la classification des données ;
- l'analyse des schémas, les invariants métier, l'idempotence et les nouvelles tentatives ;
- les transitions d'état, les minuteurs, l'annulation et la réconciliation des effets externes ;
- le routage des approbations et les journaux d'audit.

Utilisez un modèle lorsque l'interprétation, la planification d'alternatives, la synthèse ou une sélection bornée sont réellement nécessaires. Des frameworks comme LangGraph prennent en charge des workflows combinant étapes déterministes et étapes pilotées par le modèle, l'exécution durable et des points de validation humaine. [Présentation de LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)

## Les rôles ne sont pas des permissions {#roles-are-not-permissions}

Un routeur peut choisir une configuration validée. Un chercheur peut produire un ensemble d'affirmations. Un exécutant peut demander l'usage d'un outil. Un relecteur peut émettre un verdict. Aucune de ces étiquettes n'accorde l'accès à des données ou à des effets externes.

Pour chaque rôle, définissez :

| Rôle | Peut faire | Ne doit pas décider seul | Reçu requis |
|---|---|---|---|
| Routeur | choisir un chemin approuvé | accéder au-delà du périmètre de la tâche | route et révision de configuration |
| Worker | effectuer un travail borné avec le modèle ou des outils | publier ou déployer par défaut | reçus de sortie, d'outil et terminaux |
| Relecteur | évaluer des critères explicites | modifier les preuves du candidat | verdict et référence des constats |
| Approbateur | autoriser un effet défini | réécrire la tâche implicitement | identité, périmètre et décision |

Cela empêche un transfert de devenir une escalade d'autorité.

## Outils, transferts et frontières de protocole {#tools-handoffs-and-protocol-boundaries}

Un appel d'outil de modèle invoque une capacité exposée à l'agent courant. Un transfert délègue une tâche bornée à un autre worker ou spécialiste. Les deux nécessitent un schéma, une identité, une échéance et un enregistrement durable du résultat.

MCP décrit un protocole hôte-client-serveur pour l'échange de contexte entre agent et outil, tandis que A2A couvre la collaboration entre agents indépendants. N'utilisez aucun de ces protocoles en remplacement de l'autorisation applicative ou des reçus de tâche. [Architecture MCP](https://modelcontextprotocol.io/specification/latest/architecture) et [Protocole A2A](https://a2a-protocol.org/latest/)

Le SDK OpenAI Agents est un exemple actuel de runtime d'agents proposant outils, transferts, garde-fous, validation humaine et traçage. Ses primitives peuvent inspirer une conception, mais ne doivent pas devenir un schéma de tâche indépendant du fournisseur. [SDK OpenAI Agents](https://openai.github.io/openai-agents-python/)

## Nouvelles tentatives, annulation et effets de bord {#retry-cancellation-and-side-effects}

Ne relancez que les actions prouvées sûres à rejouer. Créez une clé d'idempotence avant tout appel d'outil à effet et conservez-la à travers les frontières de file, d'agent et d'outil.

```text
timeout or lost response
  -> reconcile external receipt
  -> retry only if absence of effect is established
  -> otherwise mark for review
```

L'annulation est une transition d'état accompagnée d'une étape de réconciliation, et non une simple demande d'arrêt de la génération de texte. Une tâche annulée doit indiquer si un appel d'outil n'a pas été démarré, a été interrompu, ou s'est terminé avant l'arrivée de l'annulation.

## Choisir un runtime selon le contrat {#select-a-runtime-by-contract}

| Exigence | Capacité à exiger |
|---|---|
| Travail de longue durée | état durable, reprise, délai d'expiration et réconciliation |
| Action sensible | point de contrôle d'approbation, application de politiques, idempotence |
| Plusieurs spécialistes | transfert typé, schéma de résultat, responsabilité et échéance |
| Workers concurrents | bail de file, déduplication, contre-pression, file de lettres mortes |
| Auditabilité | trace, reçus de transition d'état, caviardage, version de l'évaluateur |
| Portabilité | contrat de tâche interne isolé des objets du SDK du framework |

Une machine d'états légère gérée par l'application suffit souvent. N'ajoutez un runtime de graphe, un SDK d'agents ou un protocole multi-agents que lorsque sa capacité couvre une exigence mesurée.

## Pièges {#gotchas}

- **Une conversation n'est pas un état d'orchestration.** L'historique de discussion ne prouve ni qui possède une tâche, ni si un effet s'est accompli. **Correction :** persistez un enregistrement de tâche et des reçus terminaux.
- **Les transferts peuvent multiplier l'autorité.** Une instruction déléguée peut exposer des outils ou des données que l'émetteur ne contrôlait pas. **Correction :** autorisez indépendamment chez le récepteur et à chaque frontière d'outil.
- **Les nouvelles tentatives peuvent dupliquer des actions réelles.** Un délai d'attente ne prouve pas qu'un appel d'API a échoué. **Correction :** réconciliez par clé d'idempotence avant de relancer.
- **Une revue humaine après l'effet arrive trop tard.** Un relecteur ne peut pas annuler une action déjà publiée ou payée. **Correction :** placez l'approbation avant la frontière irréversible.
- **L'état d'un framework n'est pas automatiquement portable.** La disposition des objets du SDK et la sémantique de persistance évoluent. **Correction :** stockez un petit contrat géré par l'application, en dehors du framework.
- **Le débit n'est pas l'achèvement.** Une file occupée peut masquer des tâches échouées sans preuve terminale. **Correction :** alertez sur les reçus terminaux manquants ou périmés.

## Sources {#sources}

- [Présentation de LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [SDK OpenAI Agents](https://openai.github.io/openai-agents-python/)
- [Architecture du Model Context Protocol](https://modelcontextprotocol.io/specification/latest/architecture)
- [Protocole A2A](https://a2a-protocol.org/latest/)

## Voir aussi {#see-also}

- [[multi-agent-messaging]]
- [[multi-session-coordination]]
- [[agent-design-patterns]]
- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[agent-security]]
