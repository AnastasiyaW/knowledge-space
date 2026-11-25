---
title: "Modèles de déploiement d'agents (septembre 2026)"
category: patterns
tags: [llm-agents, deployment, production, reliability, observability, rollout]
level: 3
source_sha256: 81cecd25e0f4e8ba4a45006267a19abc67811b3d487d502d1bc1c493a3c0b8f9
translation: machine
translated_at: '2026-10-24'
---
# Modèles de déploiement d'agents (septembre 2026) {#agent-deployment-patterns-september-2026}

Relu le 2026-09-03. Déployez un agent comme un workflow applicatif versionné, et non comme une invite attachée à un point de terminaison de modèle. Un déploiement doit rendre inspectables, une fois la requête terminée, sa configuration de modèle, ses outils, ses politiques, ses transitions d'état et ses preuves.

## Unité de déploiement {#deployment-unit}

| Élément | Figer et consigner | Pourquoi c'est important |
|---|---|---|
| Application | Image ou révision source immuable | Reproduit le comportement d'orchestration et de validation |
| Modèle | Fournisseur, identifiant exact du modèle/artefact, politique de décodage | Évite une dérive involontaire de capacités ou de coûts |
| Invite/configuration | Gabarit versionné et configuration d'exécution | Permet d'attribuer les changements de sortie |
| Outils | Manifeste, portées, délais d'expiration et politique d'approbation | Limite les effets de bord |
| Données | Révision du corpus de récupération et politique d'accès | Identifie les preuves que l'agent pouvait lire |
| Évaluation | Jeu de tests, grille d'évaluation et seuil de mise en production | Distingue une build nouvelle d'une build vérifiée |

Un digest d'image seul ne suffit pas lorsque des alias de modèles, des invites, des définitions d'outils ou un index peuvent changer indépendamment.

## Choisir la voie d'exécution {#choose-the-execution-lane}

| Voie | À utiliser lorsque | Contrat requis |
|---|---|---|
| Requête synchrone | Une réponse bornée est attendue dans l'interaction utilisateur | Échéance, annulation, schéma de réponse et message de délai d'expiration sûr |
| Tâche durable | Le travail peut dépasser la durée d'une requête HTTP ou comporter plusieurs étapes | Clé d'idempotence, point de contrôle, prédicat de relance et reçu terminal |
| Suspension pour approbation | Un outil peut produire un effet externe matériel | Approbateur nommé, action proposée immuable, expiration et décision auditable |
| Traitement par lots planifié | Les entrées sont connues et le traitement peut être différé | Manifeste, clé de déduplication, état par élément et comptabilisation de l'achèvement |

Ne placez pas un travail de longue durée derrière un gestionnaire de requêtes au seul motif que le premier appel au modèle est rapide. Persistez l'état avant d'invoquer une action pouvant être relancée.

## Un petit élément de travail durable {#a-small-durable-work-item}

```json
{
  "work_id": "news-2026-09-03-0042",
  "input_revision": "sha256:...",
  "agent_release": "2026-09-03.2",
  "state": "AWAITING_APPROVAL",
  "idempotency_key": "publish:news-2026-09-03-0042",
  "tool_manifest_revision": "tools-19",
  "checkpoint": "extract-complete",
  "evidence": ["source-17", "evaluation-run-82"]
}
```

`state` est géré par l'application. Un modèle peut proposer une action suivante, mais il ne doit pas directement définir `SUCCEEDED`, s'approuver lui-même ni effacer l'enregistrement d'audit.

## Politique d'échec et de relance {#failure-and-retry-policy}

Traitez chaque classe d'erreur différemment :

1. **Entrée invalide ou refus de politique :** rejetez définitivement avec un motif compréhensible par l'utilisateur ; ne relancez pas une entrée inchangée.
2. **Erreur transitoire fournisseur ou réseau :** ne relancez qu'une opération idempotente, dans un budget borné, et conservez l'enregistrement de la tentative.
3. **Effet de bord ambigu côté outil :** réconciliez à l'aide de la clé d'idempotence ou du reçu du fournisseur avant toute relance.
4. **Sortie de modèle invalide :** exécutez un chemin de réparation/validation déterministe ou renvoyez un échec typé ; ne la réinterprétez pas silencieusement comme un succès.
5. **Interruption du processus :** reprenez depuis le dernier point de contrôle vérifié, et non depuis une transcription de conversation déduite.

## L'observabilité comme exigence de mise en production {#observability-as-a-release-requirement}

Une seule trace doit permettre à un opérateur de répondre à ces questions : quelle version s'est exécutée, quelle révision d'entrée ou de données elle a vue, quels outils elle a demandés, quelles actions ont été refusées ou approuvées, quelles relances ont eu lieu, et comment le workflow a atteint son état terminal. Enregistrez des identifiants opaques ou des attributs expurgés plutôt que des secrets bruts et des données personnelles.

Les conventions sémantiques GenAI fournissent un vocabulaire commun pour les spans de modèle ; elles complètent les événements métier de tâche et d'approbation, sans les remplacer. [Conventions GenAI d'OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai)

## Contrat de déploiement progressif {#rollout-contract}

```text
candidate release
    -> deterministic and adversarial evaluation set
    -> isolated canary with trace + receipt inspection
    -> bounded rollout with rollback target
    -> production observation against explicit SLOs
```

Revenez en arrière sur l'unité de déploiement complète. Changer uniquement le modèle en conservant une politique d'outils ou une révision d'index modifiée rend l'incident impossible à reconstituer.

## Pièges courants {#gotchas}

- **Problème : qualifier de « sans état » un point de terminaison d'agent asynchrone.** La connexion du navigateur est sans état ; le travail, lui, ne l'est pas. **Correctif :** stockez un élément de travail et un point de contrôle avant toute action pouvant être relancée ou reprise.
- **Problème : relancer un outil à effets de bord après un délai d'expiration.** La requête initiale a peut-être réussi à distance. **Correctif :** exigez un reçu du fournisseur ou une clé d'idempotence avant de relancer.
- **Problème : traiter une trace LLM comme un journal d'audit.** Les traces peuvent omettre les décisions de politique et ne doivent pas stocker aveuglément des charges utiles sensibles. **Correctif :** émettez des événements structurés distincts pour l'autorisation, l'approbation et le résultat terminal.
- **Problème : faire progresser un alias de modèle sans évaluation.** Le déplacement d'un alias peut modifier la forme des sorties et le comportement des outils. **Correctif :** épinglez l'identifiant de version et relancez le corpus de mise en production avant la promotion.

## Voir aussi {#see-also}

- [[production-patterns]]
- [[agent-observability-dashboards]]
- [[tool-use-patterns]]
- [[agent-evaluation]]

## Sources {#sources}

- [Bonnes pratiques de production d'OpenAI](https://developers.openai.com/api/docs/guides/production-best-practices)
- [Persistance dans LangGraph](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Conventions sémantiques GenAI d'OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai)
