---
title: "Claude Managed Agents"
description: "Guide tenant compte de la version sur le harness d'agents gérés d'Anthropic : configuration des agents, environnements, sessions, événements, politiques de permission et frontières de données."
tags: [llm-agents, claude, managed-agents, sandboxes, permissions, orchestration]
level: 3
source_sha256: 1e19b92c130db3a7c893965c363749ff53bf025ad2a092bea883d48da5b32d40
translation: machine
translated_at: '2026-10-24'
---
# Claude Managed Agents {#claude-managed-agents}

**Périmètre vérifié : 2026-09-03.** Claude Managed Agents est le harness géré en bêta d'Anthropic, destiné aux travaux d'agents asynchrones et de longue durée. Il fournit la boucle de l'agent, les environnements, l'exécution des outils, l'historique persisté des événements et le cycle de vie des sessions. L'application reste responsable de son autorisation métier, des décisions d'approbation et des critères de mise en production. [Vue d'ensemble de Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)

## Ce qui est géré {#what-is-managed}

| Concept | Signification actuelle | Responsabilité de l'application |
|---|---|---|
| Agent | modèle, prompt système, outils, serveurs MCP, skills | versionner et relire la configuration |
| Environment | sandbox cloud d'Anthropic ou configuration de sandbox auto-hébergée | choisir la résidence des données et la frontière réseau |
| Session | instance d'agent en cours d'exécution pour une tâche | créer, orienter, interrompre, réconcilier les résultats |
| Events | messages, résultats d'outils, enregistrements de statut et de progression | consommer le flux d'événements faisant foi |

L'infrastructure gérée réduit le travail d'assemblage de l'exécution. Elle ne rend pas un appel d'outil autorisé, un résultat factuellement correct ou une publication sûre à diffuser.

## Contrat de cycle de vie {#lifecycle-contract}

```text
versioned agent + reviewed environment
          -> create session
          -> send user event
          -> stream authoritative events
          -> approval / denial / interrupt as required
          -> reconcile external effects
          -> terminal receipt
```

La plateforme prend en charge l'historique de session persisté et les sorties, le streaming d'événements server-sent, ainsi que l'orientation ou l'interruption en cours d'exécution. Un aperçu dans l'interface n'est pas la référence : utilisez les événements de session persistés et un accusé de réception applicatif pour décider si une tâche est réellement terminée. [Flux d'événements de session](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Configuration minimale {#minimum-configuration}

Partez d'une définition explicite, à moindre privilège :

```yaml
name: Editorial Research Agent
model:
  id: claude-opus-5
system: Draft from approved public sources. Do not publish.
tools:
  - type: agent_toolset_20260401
    default_config:
      permission_policy:
        type: always_ask
```

L'API actuelle est en bêta et nécessite l'en-tête de bêta `managed-agents-2026-04-01` ; les SDK pris en charge l'ajoutent automatiquement. Épinglez la version du SDK et testez sa forme de requête actuelle avant tout déploiement. [Démarrage rapide de Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Une politique de permission n'est pas un contrôle d'accès {#permission-policy-is-not-access-control}

Les politiques de permission déterminent si les outils exécutés côté serveur s'exécutent immédiatement ou attendent une approbation :

| Politique | Résultat |
|---|---|
| `always_allow` | l'outil serveur activé s'exécute sans confirmation |
| `always_ask` | la session se met en pause jusqu'à ce que l'application renvoie allow ou deny |

Le jeu d'outils d'agent prédéfini utilise `always_allow` par défaut ; les jeux d'outils MCP utilisent `always_ask`. Les outils personnalisés s'exécutent dans l'application et nécessitent donc leur propre couche d'autorisation. Les sessions en cours conservent la configuration d'outils avec laquelle elles ont été créées : une modification de politique ne concerne que les sessions ultérieures, sauf si l'application gère explicitement la migration. [Politiques de permission](https://platform.claude.com/docs/en/managed-agents/permission-policies)

Pour un flux de contenu public, adoptez une séparation stricte :

| Étape | Capacité | Par défaut |
|---|---|---|
| Recherche | lire les sources approuvées, créer des notes structurées | autorisée |
| Rédaction | créer une proposition de révision | autorisée |
| Relecture | inspecter les sources et le brouillon | autorisée |
| Publication | créer un effet public | refusée jusqu'à un événement d'approbation concret |
| Reprise | inspecter la tâche et l'accusé de réception | autorisée, sans nouvel effet |

Une interface d'approbation doit identifier l'appel d'outil exact, ses arguments, le compte cible et l'échéance. « L'agent avait été approuvé plus tôt » ne constitue pas une preuve suffisante pour une nouvelle publication.

## Environnement et frontière des données {#environment-and-data-boundary}

Ne choisissez une sandbox cloud qu'après avoir documenté :

- la liste blanche réseau et la politique de sortie ;
- les montages de fichiers, de dépôts et d'artefacts ;
- les identifiants accessibles à la session ;
- la classification et la rétention des données ;
- la nécessité ou non d'une sandbox auto-hébergée pour des raisons de résidence ou de conformité ;
- la manière dont les fichiers envoyés et les données de session seront supprimés.

Les sessions de Managed Agents sont volontairement avec état. Anthropic indique que cette fonctionnalité n'est pas éligible à la Zero Data Retention ni à la couverture BAA HIPAA au stade actuel de la bêta ; évaluez cette frontière avant d'intégrer dans une session un corpus sensible ou des données d'apprenants. [Vue d'ensemble de Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)

## Gestion des événements {#event-handling}

Traitez les événements comme une machine à états, et non comme du texte de conversation :

1. persister l'identifiant de session, l'identifiant de tâche, les entrées attendues et la révision de politique en vigueur ;
2. envoyer la tâche sous la forme d'un événement `user.message` ;
3. diffuser les événements de statut, d'agent et d'outil ;
4. lorsqu'une action `always_ask` met la session en pause, inspecter la demande concrète et envoyer un événement allow ou deny ;
5. en cas d'interruption, attendre la transition vers l'état idle enregistrée ;
6. réconcilier tout effet externe avant d'attribuer un état terminal.

Les deltas d'aperçu de la plateforme servent uniquement à l'affichage ; l'événement persisté et bufferisé constitue la référence. [Flux d'événements de session](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Quand c'est pertinent {#when-it-fits}

Choisissez Managed Agents lorsque la tâche bénéficie d'un environnement géré, de plusieurs appels d'outils sur des minutes ou des heures, de sessions persistées ou d'une exécution planifiée. Utilisez l'API Messages ou un harness local lorsque l'application doit contrôler entièrement la boucle, l'environnement, le chemin des données et chaque exécuteur d'outil.

## Pièges courants {#gotchas}

- **Le jeu d'outils de l'agent est permissif par défaut.** Sa valeur par défaut est `always_allow`. **Correctif :** configurez `always_ask` ou désactivez les outils inutiles avant de créer chaque version d'agent en production.
- **Une approbation MCP n'est pas une autorisation applicative.** Un utilisateur peut approuver un outil tout en n'ayant pas l'autorité pour l'action métier. **Correctif :** validez le tenant, la cible, le périmètre et l'approbation au niveau de l'exécuteur aval.
- **Une session passée à l'état idle n'est pas une preuve de succès.** Elle peut attendre une confirmation, avoir été interrompue, ou être incapable de réconcilier un effet de bord. **Correctif :** exigez un accusé de réception terminal côté domaine.
- **Les sessions avec état conservent plus qu'un prompt.** L'historique, l'état de la sandbox et les sorties font partie de la frontière des données. **Correctif :** classifiez les données, définissez la rétention et vérifiez les opérations de suppression.
- **Les surfaces en bêta évoluent.** Un démarrage rapide copié peut devenir obsolète. **Correctif :** épinglez les dépendances, citez l'en-tête de bêta actuel et lancez un canari contrôlé après chaque modification.

## Sources {#sources}

- [Vue d'ensemble de Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
- [Démarrage rapide de Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Politiques de permission](https://platform.claude.com/docs/en/managed-agents/permission-policies)
- [Flux d'événements de session](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Voir aussi {#see-also}

- [[agent-orchestration]]
- [[agent-safety-alignment]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
