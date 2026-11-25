---
title: "Fondamentaux des agents"
description: "Contrats fondamentaux des agents LLM : décisions du modèle, outils, état, politique, preuves et autonomie contrôlée"
level: 2
source_sha256: a207fedf0efb8cbba88c3a3b8899577449322ac47be91c09fb4db308ec721e67
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux des agents (septembre 2026) {#agent-fundamentals-september-2026}

Contexte de version : un agent est un système, et non une capacité du modèle. Enregistrez la révision du modèle, la politique de prompts et d'outils, le schéma d'état et la suite d'évaluation avec chaque version d'agent déployée.

Un agent LLM combine une inférence de modèle avec un plan de contrôle qui observe les entrées, sélectionne les actions autorisées, persiste l'état et renvoie des preuves. Un chatbot ne devient un agent que lorsqu'il peut agir sur un environnement ou l'inspecter via des capacités gouvernées.

## Composants principaux {#core-components}

| Composant | Responsabilité | Doit être déterministe ? |
|---|---|---|
| Modèle | Proposer du langage, une sortie structurée ou la prochaine action | Non |
| Instructions | Définir le rôle, les contraintes et le contrat de sortie | Versionnées |
| Outils | Lire ou agir via des interfaces typées | Oui à la frontière |
| Couche de politique | Autoriser les actions et appliquer les budgets | Oui |
| Magasin d'état | Persister les éléments de travail, les reçus et les données de reprise | Oui |
| Évaluateur | Décider si le résultat final satisfait les critères d'acceptation | Oui / revu indépendamment |
| Observabilité | Corréler les appels de modèle, les outils, les décisions et les erreurs | Oui |

Le modèle n'est pas la source de vérité pour les permissions, les faits, l'achèvement de la tâche ou l'état des effets de bord.

## Cycle de vie d'un agent {#agent-lifecycle}

```text
request -> validate identity and input -> create durable work item
        -> choose a permitted next action -> execute or refuse
        -> persist receipt -> verify terminal result -> respond
```

Un élément de travail doit disposer d'un identifiant unique, d'un périmètre acteur/locataire, d'une clé d'idempotence, d'un budget de tentatives, d'une révision de politique, d'une référence de trace et d'un reçu terminal. Rejouer la même requête doit être sûr ou explicitement rejeté.

## Outils {#tools}

Un outil est une capacité typée dotée d'un propriétaire, et non simplement une description en langage naturel.

```json
{
  "name": "get_invoice",
  "input_schema": {"invoice_id": "string"},
  "side_effect": "read_only",
  "authorization": "billing.read",
  "timeout_ms": 3000,
  "idempotency": "not_applicable",
  "receipt_schema": "invoice-v2"
}
```

Validez côté serveur les paramètres proposés par le modèle. Un schéma valide ne prouve pas qu'un appel est autorisé : l'autorisation doit lier l'acteur, le locataire, la ressource, l'action et la politique en vigueur.

## État et mémoire {#state-and-memory}

Séparez ces objets :

- **Contexte de conversation :** information minimale pour le prochain tour de modèle.
- **État d'exécution :** état courant du workflow, nombre de tentatives et reçus des outils.
- **Mémoire à long terme :** enregistrements délimités, avec propriétaire, expiration et politique d'écriture.
- **Corpus de connaissances :** matériel source récupéré avec sa provenance.

Une fenêtre de contexte n'est pas une base de données. Ne stockez pas des faits opaques dans un prompt et ne les appelez pas mémoire durable.

## Agent ou workflow {#agent-versus-workflow}

| Question | Privilégier un workflow | Envisager un agent |
|---|---|---|
| L'ordre des étapes est-il déjà connu ? | Oui | Seulement si une décision inconnue subsiste |
| Les actions sont-elles à fort impact ou irréversibles ? | Oui, avec approbations | Seulement dans une frontière de politique étroite |
| De nouvelles preuves modifient-elles l'étape suivante ? | Probablement pas nécessaire | Oui, avec conditions explicites d'arrêt et de replanification |
| Le succès peut-il être vérifié mécaniquement ? | Oui | Requis avant une autonomie en production |
| La latence et le coût sont-ils strictement bornés ? | Généralement | Seulement après une évaluation démontrant la valeur |

Commencez par un workflow, puis introduisez une décision du modèle au plus petit point où elle apporte un bénéfice mesuré.

## Passerelle d'actions de base {#basic-action-gateway}

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestContext:
    actor_id: str
    tenant_id: str
    remaining_steps: int


def execute_read_only(
    context: RequestContext,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    if context.remaining_steps <= 0:
        raise RuntimeError("step budget exhausted")
    if tool_name != "get_invoice":
        raise PermissionError("tool is not available in this stage")
    invoice_id = arguments.get("invoice_id")
    if not isinstance(invoice_id, str) or not invoice_id:
        raise ValueError("invoice_id must be a non-empty string")
    return {"receipt_type": "invoice_lookup", "invoice_id": invoice_id}
```

Le code de production ajoute une vérification d'identité réelle, un appel au dépôt, la persistance d'audit, la propagation des délais et la consultation de la politique. L'invariant essentiel est que le modèle ne contourne jamais cette passerelle.

## Niveaux d'autonomie {#autonomy-levels}

Choisissez un niveau explicite par action :

1. proposer uniquement — un humain ou l'application l'exécute ;
2. exécuter en lecture seule — le système renvoie des preuves ;
3. exécuter une action réversible — nouvelles tentatives bornées et reçu ;
4. exécuter une action externe ou irréversible — approbation explicite ;
5. workflow durable autonome — seulement après évaluation de bout en bout et contrôles d'incident.

Un même agent peut fonctionner à des niveaux différents selon les outils. N'accordez jamais le niveau le plus élevé globalement parce qu'il existe une tâche à faible risque.

## Interopérabilité {#interoperability}

MCP standardise une frontière hôte/client/serveur pour les ressources, les prompts et les outils. A2A standardise la communication avec un service d'agent indépendant via la découverte d'agents, les tâches, les messages et les artefacts. Aucun de ces protocoles ne remplace l'identité applicative, l'autorisation, la gouvernance des données ni les preuves au niveau de la tâche.

Utilisez les protocoles pour définir une frontière réelle, et non pour ajouter du cérémonial à une fonction en processus.

## Observabilité et évaluation {#observability-and-evaluation}

Enregistrez les propositions d'action, les décisions de politique, les entrées/sorties des appels d'outils avec une anonymisation appropriée, la raison de chaque nouvelle tentative, les délais, les coûts et le verdict terminal. Les évaluations doivent couvrir les requêtes normales, les entrées malformées, les actions refusées, les tentatives d'injection, les défaillances d'outils, les soumissions en double et la reprise.

## Pièges courants {#gotchas}

- **Davantage d'outils ne signifie pas automatiquement davantage de capacités.** Ils augmentent l'ambiguïté et la surface d'attaque. **Correctif :** n'exposez que la liste blanche délimitée à la tâche.
- **Une réponse d'API réussie n'est pas l'achèvement de la tâche.** Elle peut contenir des données partielles, obsolètes ou non autorisées. **Correctif :** définissez une vérification d'acceptation distincte, liée au résultat pour l'utilisateur.
- **La croissance du contexte masque la perte d'état.** Un long historique de transcription coûte cher et peut omettre des faits critiques. **Correctif :** persistez un état structuré et récupérez une projection minimale autorisée.
- **Un protocole n'est pas à lui seul une frontière de sécurité.** Les métadonnées MCP/A2A annoncent des capacités mais ne peuvent pas accorder d'autorité. **Correctif :** appliquez l'autorisation à chaque passerelle d'action locale ou distante.

## Sources {#sources}

- [OpenAI Agents SDK : agents](https://openai.github.io/openai-agents-python/agents/)
- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI API : function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Voir aussi {#see-also}

- [[agent-design-patterns]]
- [[agent-architectures]]
- [[agent-memory]]
- [[function-calling]]
- [[agent-security]]
