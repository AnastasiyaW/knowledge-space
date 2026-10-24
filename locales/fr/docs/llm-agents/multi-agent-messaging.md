---
title: "Messagerie multi-agents et coordination"
description: "Choisir la bonne frontière pour le travail entre agents, l'accès aux outils, les messages durables, les accusés de réception et les modifications concurrentes du dépôt."
tags: [llm-agents, multi-agent, messaging, a2a, mcp, coordination, observability]
level: 3
source_sha256: 42ce38c4b865e34f3fc39a7f4004e9f180002b736b1742d5ab8427f75e3363c6
translation: machine
translated_at: '2026-10-24'
---
# Messagerie multi-agents et coordination (septembre 2026) {#multi-agent-messaging-and-coordination-september-2026}

Contexte de version : les runtimes d'agents, les fonctionnalités des IDE, les révisions de protocoles et les adaptateurs de transport évoluent rapidement. Cette page décrit des contrats de coordination durables plutôt que de affirmer qu'un drapeau de client, un plugin, un broker, un intervalle de polling ou une fonctionnalité expérimentale particulière est universel.

La communication n'est qu'une partie de la coordination. Un système fiable distingue un message, un état de tâche, une décision d'autorité, un artefact partagé et un verrou exclusif. Traiter tous ces éléments comme du texte de conversation rend probables l'exécution en double et une complétion non vérifiable.

## Choisir la bonne frontière {#choose-the-correct-boundary}

| Besoin | Primitive appropriée | Ce qu'elle ne prouve pas |
|---|---|---|
| Un agent a besoin d'un outil, d'une API ou d'une ressource de données | Frontière client/serveur MCP | qu'un autre agent indépendant a accepté une tâche |
| Un agent délègue un objectif à un agent indépendant | A2A ou un protocole de tâches applicatif | qu'un effet de bord s'est terminé en toute sécurité |
| Deux sessions locales partagent une connaissance de projet | artefact versionné, passation ou référence de dépôt | la propriété exclusive d'une ressource modifiable |
| Un seul worker peut modifier une ressource | bail ou verrou avec réconciliation externe | la livraison durable d'un message |
| Un relecteur a besoin de preuves | reçu immuable lié à la tâche | que la description de l'expéditeur était correcte |

La documentation actuelle d'A2A décrit A2A comme une communication agent-à-agent et MCP comme une communication agent-à-outil. Ils sont complémentaires : un agent peut utiliser des outils MCP tout en collaborant avec un autre agent via A2A. [A2A Protocol](https://a2a-protocol.org/latest/)

MCP lui-même repose sur une architecture hôte-client-serveur. L'hôte gère les connexions, la politique, le consentement et l'autorisation de l'utilisateur ; un serveur MCP n'accorde pas automatiquement à un agent distant une autorité sur les ressources d'un utilisateur. [Architecture MCP](https://modelcontextprotocol.io/specification/latest/architecture)

## Une enveloppe de message durable {#a-durable-message-envelope}

Utilisez une enveloppe typée avec une clé d'idempotence, des métadonnées de routage, une expiration et des références à des artefacts contrôlés. Ne placez ni identifiants, ni instructions non restreintes, ni contexte privé brut dans l'enveloppe.

```json
{
  "schema_version": "agent-message/v1",
  "message_id": "msg_01...",
  "trace_id": "tr_01...",
  "idempotency_key": "research:source-set-44:v1",
  "sender": {"agent_id": "researcher@release-12", "role": "research"},
  "recipient": {"queue": "editorial-review", "role": "review"},
  "intent": "review_claim_set",
  "allowed_actions": ["read_artifact", "write_review_receipt"],
  "input_refs": ["artifact:claim-set-44"],
  "expires_at": "2026-09-04T12:00:00Z",
  "sent_at": "2026-09-03T12:00:00Z"
}
```

Le récepteur valide le schéma, l'identité, l'expiration, les actions autorisées et l'accès aux artefacts avant d'accepter le travail. L'expéditeur n'accorde jamais de permissions simplement en les écrivant dans un message.

## Modéliser la tâche séparément de la livraison {#model-the-task-separately-from-delivery}

Un accusé de transport signifie seulement qu'un message a atteint un transport. Ce n'est pas une preuve que le destinataire l'a lu, qu'il en avait l'autorité, qu'il l'a terminé ou qu'il a produit un résultat valide.

Suivez séparément l'état de la tâche et la vérification. Une tâche possède des états terminaux mutuellement exclusifs ; la vérification est une revue du reçu terminal, et non une autre transition de la tâche.

```text
non-terminal task states: PENDING -> ACCEPTED -> RUNNING
terminal task state: COMPLETED | FAILED | CANCELLED
verification receipt: PENDING -> VERIFIED | REJECTED
```

Chaque transition de tâche s'accompagne d'un reçu approprié. Un état terminal exige un reçu terminal :

- **ACCEPTED :** identité du récepteur, périmètre accepté, échéance et révision de la tâche ;
- **COMPLETED :** référence de l'artefact de sortie, résultat de validation et reçu d'absence d'effet de bord ou d'effet de bord constaté ;
- **FAILED :** erreur classifiée, possibilité de nouvelle tentative, preuves conservées et prochaine action sûre ;
- **CANCELLED :** acteur, motif et résultat de réconciliation pour tout effet en cours ;
- **Reçu de vérification :** version des critères indépendants, identité du relecteur et verdict.

L'annulation peut survenir depuis tout état non terminal. Lorsqu'un message pourrait conduire à un paiement, une publication, un déploiement ou un autre effet externe, cet effet a besoin de sa propre autorisation au niveau applicatif et de sa propre clé d'idempotence.

## Choix de transport {#transport-choices}

| Transport | Bon usage | Contrat à ajouter soi-même |
|---|---|---|
| Fichiers en ajout seul | passations locales auditables et recherches asynchrones | écriture atomique, validation de schéma, expiration, reçu de traitement |
| File d'attente ou base de données | nouvelles tentatives, contre-pression, nombreux workers | déduplication, bail, politique de lettres mortes, enregistrement terminal de la tâche |
| Point d'accès A2A | délégation interopérable entre systèmes d'agents indépendants | autorisation applicative, registre local des travaux, contrôles des effets |
| Appel de processus direct | sous-tâche bornée dans le processus | délai d'attente, annulation, validation du résultat, reçu du parent |

Commencez par le plus petit transport qui préserve les preuves nécessaires. Un artefact adossé au dépôt est souvent plus solide qu'un message en temps réel pour la recherche, la planification ou la revue, car il offre à chaque destinataire la même entrée versionnée.

## Traiter le contenu reçu comme une entrée non fiable {#treat-received-content-as-untrusted-input}

Un message d'agent, un fichier récupéré, un résultat d'outil ou un commentaire de ticket peut contenir des instructions en conflit avec la politique du destinataire. Un récepteur doit :

1. analyser l'enveloppe sans exécuter son texte libre ;
2. résoudre les références d'artefacts via un magasin soumis à contrôle d'accès ;
3. appliquer sa propre politique de tâche et d'autorisation ;
4. restreindre les outils à l'ensemble d'actions déclaré et approuvé localement ;
5. valider la sortie par rapport au contrat de la tâche ;
6. écrire un reçu terminal avant de notifier l'expéditeur.

Cela fait de la délégation une interface contrôlée plutôt qu'un tunnel d'injection de prompt.

## Coordonner les travaux concurrents sur le dépôt {#coordinate-concurrent-repository-work}

Pour les modifications de code ou de documentation, assignez un seul rédacteur à un chemin ou à une frontière de fonctionnalité. Utilisez une branche et un worktree dédiés par rédacteur, puis n'échangez que des références de commit, des artefacts de revue et des demandes de modification circonscrites. Les worktrees Git sont conçus pour fournir plusieurs arbres de travail rattachés à un même dépôt. [git-worktree](https://git-scm.com/docs/git-worktree)

Une passation concise doit identifier :

```text
objective + scope + base commit + branch + changed paths
+ verification commands + receipts + known gaps + owner
```

Une transcription de conversation partagée n'est pas un artefact d'intégration. Elle n'a pas de révision de base immuable, pas de sémantique de fusion, et rien ne garantit qu'un lecteur ultérieur voie la bonne entrée.

## Observabilité {#observability}

Attribuez à chaque message, tâche et résultat un identifiant de trace commun. Mesurez l'ancienneté dans la file, le délai d'acceptation, la durée d'exécution, les nouvelles tentatives, les échecs de schéma, les refus d'autorisation et les issues terminales vérifiées. Ne mesurez pas seulement le débit de messages : une file rapide qui perd des reçus n'est pas un système de coordination réussi.

## Pièges {#gotchas}

- **Livraison n'est pas achèvement.** Un accusé du broker ne dit rien du travail du destinataire. **Correctif :** exiger un état accepté et un reçu terminal distinct.
- **Un verrou n'est pas une file de messages.** Il peut exclure les rédacteurs concurrents mais ne peut pas conserver une description de tâche ou un résultat. **Correctif :** garder verrous, messages et enregistrements de tâches comme des primitives séparées.
- **Un expéditeur ne peut pas déléguer une autorité qu'il ne possède pas.** Les permissions déclarées dans un message ne sont qu'une demande. **Correctif :** autoriser de manière indépendante au niveau du récepteur et à chaque frontière d'outil à effet.
- **Les intervalles de polling ne sont pas des garanties de fiabilité.** Un processus peut être endormi, mort ou lire un état périmé. **Correctif :** s'appuyer sur un état durable, des expirations et une réconciliation plutôt que sur des hypothèses de temporisation.
- **Les dumps de contexte complets sont une défaillance de contrôle d'accès.** Ils diffusent du matériel privé et rendent la pertinence plus difficile à auditer. **Correctif :** envoyer des références d'artefacts restreintes, avec provenance et un lecteur soumis à politique.

## Sources {#sources}

- [A2A Protocol](https://a2a-protocol.org/latest/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Voir aussi {#see-also}

- [[multi-session-coordination]]
- [[agent-orchestration]]
- [[agent-design-patterns]]
- [[agent-security]]
- [[agent-observability-dashboards]]
- [[llmops]]
