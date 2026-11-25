---
title: "Architectures d'agents"
description: "Choisir une architecture de flux de contrôle bornée pour les agents LLM : état, outils, transferts, protocoles et preuves"
level: 3
source_sha256: 10a2ee8095fa5c4cc714b2472281890d36f6998a671e438d5b38f11c367ba0c7
translation: machine
translated_at: '2026-10-24'
---
# Architectures d'agents (septembre 2026) {#agent-architectures-september-2026}

Contexte de version : revue effectuée par rapport à la spécification MCP `latest`, à A2A et à la documentation du OpenAI Agents SDK. Les révisions de protocole et les versions de SDK sont des dépendances ; consignez la révision exacte utilisée par un système déployé.

Une architecture d'agent est le plan de contrôle déterministe qui entoure les appels probabilistes au modèle. L'architecture gère les permissions, les transitions d'état, les limites de nouvelles tentatives, le travail durable et les preuves. Le modèle propose ; le plan de contrôle décide de ce qui peut se produire ensuite.

## Choisir la forme suffisante la plus simple {#choose-the-smallest-sufficient-shape}

| Forme | À utiliser quand | Contrôles requis |
|---|---|---|
| Action unique bornée | Une seule requête, sans effet de bord ou avec une seule action d'outil réversible | Validation des entrées, timeout, validation des sorties |
| Machine à états explicite | Une tâche comporte des étapes, des nouvelles tentatives, des approbations ou une reprise | Table de transitions, budget, idempotence, états terminaux |
| DAG | Des tâches indépendantes peuvent s'exécuter en parallèle et ont des jointures explicites | Graphe de dépendances, sémantique de jointure, reçus par nœud |
| Transfert vers un spécialiste | Une autre autorité ou un autre domaine possède la tâche | Contrat de transfert typé, autorisation, filtrage de l'historique |
| Frontière d'agent distant | Un service indépendant possède l'exécution | Protocole, authentification, cycle de vie de la tâche, contrat d'artefacts |

Ne commencez pas par un graphe multi-agents. N'ajoutez de structure que lorsqu'un flux borné plus simple ne peut pas satisfaire le contrat requis de fiabilité, de permissions ou de latence.

## Contrat d'élément de travail {#work-item-contract}

Un élément de travail durable rend les nouvelles tentatives et la reprise inspectables.

```json
{
  "task_id": "task_01J...",
  "state": "planned",
  "attempt": 0,
  "attempt_limit": 3,
  "idempotency_key": "sha256:...",
  "input_ref": "artifact://request/...",
  "policy_revision": "agent-policy-v4",
  "trace_ref": "trace_...",
  "terminal_receipt": null
}
```

Chaque transition a un seul responsable et un motif. Les états inconnus échouent en mode sécurisé (fail closed).

## Machine à états minimale {#minimal-state-machine}

```python
from dataclasses import dataclass, replace
from typing import Literal

State = Literal["planned", "running", "verified", "failed", "cancelled"]
ALLOWED: dict[State, set[State]] = {
    "planned": {"running", "cancelled"},
    "running": {"verified", "failed", "cancelled"},
    "verified": set(),
    "failed": set(),
    "cancelled": set(),
}


@dataclass(frozen=True)
class WorkItem:
    task_id: str
    state: State
    attempt: int
    attempt_limit: int


def transition(item: WorkItem, target: State) -> WorkItem:
    if target not in ALLOWED[item.state]:
        raise ValueError(f"invalid transition: {item.state} -> {target}")
    if target == "running" and item.attempt >= item.attempt_limit:
        raise RuntimeError("attempt budget exhausted")
    return replace(
        item,
        state=target,
        attempt=item.attempt + (target == "running"),
    )
```

Les appels d'outils n'ont lieu que dans l'état `running`, après autorisation et validation du schéma. `verified` exige un reçu vérifiable indépendamment, et non une déclaration du modèle selon laquelle le travail est terminé.

## Mémoire et contexte {#memory-and-context}

Séparez quatre éléments :

- **État d'exécution :** l'élément de travail durable et les reçus de transition.
- **Contexte de conversation :** l'entrée minimale nécessaire au prochain tour du modèle.
- **Mémoire à long terme :** des enregistrements versionnés, bornés à un périmètre, avec propriétaire et politique de conservation.
- **Corpus de connaissances :** des documents sources récupérés avec leur provenance.

Un résumé dans le prompt ne peut pas remplacer un enregistrement d'état durable. Inversement, le modèle ne doit pas recevoir par défaut tous les enregistrements durables ; récupérez une projection à moindre privilège.

## Frontière des outils {#tool-boundary}

Chaque outil a besoin d'un schéma d'entrée typé, d'un périmètre acteur/locataire, d'une politique d'autorisation, d'un timeout, d'une règle d'idempotence, d'une classification des effets de bord et d'un reçu de sortie.

```text
model proposal -> schema validation -> policy decision -> tool execution
               -> receipt persistence -> verified state transition
```

Les outils en lecture seule et les actions réversibles peuvent suivre des chemins de politique différents. Les actions destructrices, financières, les messages externes ou les modifications de privilèges exigent une frontière d'approbation explicite.

## Frontières d'interopérabilité {#interoperability-boundaries}

MCP et A2A résolvent des problèmes différents :

| Protocole | Frontière | Unité centrale | Ne pas supposer |
|---|---|---|---|
| MCP | De l'application hôte vers un serveur ciblé | Ressources, prompts, outils ; capacités négociées | Qu'un outil est autorisé simplement parce qu'il est annoncé |
| A2A | Services d'agents indépendants | Agent Card, tâche, message, artefact | Qu'un agent distant expose sa mémoire ou ses outils internes |

L'architecture hôte-client-serveur de MCP isole le périmètre de chaque serveur. Sa spécification `latest` actuelle est sans état : chaque requête transporte la version de protocole et les capacités déclarées, et un client peut utiliser `server/discover` avant les autres appels pour découvrir le serveur. A2A fournit un cycle de vie de tâche pour des agents distants opaques et utilise une Agent Card pour la découverte et les exigences d'interaction.

N'utilisez un protocole que lorsque sa frontière existe. Un appel de fonction in-process ne devient pas plus sûr en étant encapsulé dans un protocole d'agent distant.

## Transferts et spécialistes {#handoffs-and-specialists}

Un transfert vers un spécialiste doit inclure :

1. l'identité de la destination et la capacité permise ;
2. le motif typé et la référence de la tâche ;
3. une projection de contexte autorisée, et non l'historique complet par défaut ;
4. la responsabilité des effets de bord et de la réponse finale ;
5. le lien de trace et le reçu terminal.

Le OpenAI Agents SDK est un exemple d'implémentation actuel : il prend en charge les outils, les garde-fous, les transferts, les sorties structurées et le traçage. Ces fonctionnalités du SDK ne remplacent ni l'autorisation applicative ni l'état durable du workflow.

## Observabilité et évaluation {#observability-and-evaluation}

Capturez les appels de modèle, les appels d'outils, les transferts, les décisions de politique, les enregistrements de transition, les erreurs et les métadonnées d'entrée/sortie expurgées. Corrélez-les avec l'identifiant de tâche, l'identifiant de trace, la révision de politique et la révision de déploiement.

Évaluez l'architecture à l'aide de scénarios rejouables :

- invocation d'outil autorisée et refusée ;
- nouvelle tentative après une défaillance transitoire ;
- requête en double avec la même clé d'idempotence ;
- résultat d'outil malformé ;
- transfert avec historique surdimensionné en portée ;
- expiration, annulation et reprise terminale.

## Pièges courants {#gotchas}

- **Une boucle sans budget n'est pas une architecture.** Elle peut répéter indéfiniment une action infructueuse. **Correctif :** imposez des limites d'itérations, de temps, de coût et de nouvelles tentatives dans un état déterministe.
- **Un transfert est une frontière d'autorisation.** Transmettre l'historique complet de la conversation peut divulguer des données ou accorder une capacité non prévue. **Correctif :** transmettez une projection typée à moindre privilège et autorisez le spécialiste destinataire.
- **La découverte d'un protocole n'est pas une confiance.** Un outil MCP annoncé ou une Agent Card A2A n'accorde pas la permission de l'utiliser. **Correctif :** liez la découverte à l'identité, à une politique explicite et à une autorisation par action.
- **Le traçage peut contenir des contenus sensibles.** Les spans de génération et d'outils peuvent enregistrer les entrées et sorties. **Correctif :** définissez la politique d'expurgation et de conservation avant d'activer la télémétrie, puis testez-la avec des données représentatives.

## Sources {#sources}

- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol latest server primitives](https://modelcontextprotocol.io/specification/latest/server)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI Agents SDK: agents](https://openai.github.io/openai-agents-python/agents/)
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

## Voir aussi {#see-also}

- [[agent-design-patterns]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
