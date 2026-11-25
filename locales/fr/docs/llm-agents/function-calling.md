---
title: "Appel de fonctions et utilisation d'outils (septembre 2026)"
category: techniques
tags: [llm-agents, function-calling, tool-use, schemas, validation]
level: 3
source_sha256: 7d465263558d2aca1d81f099c204b716d7c94c89935b831942cfe48f49f9849b
translation: machine
translated_at: '2026-10-24'
---
# Appel de fonctions et utilisation d'outils (septembre 2026) {#function-calling-and-tool-use-september-2026}

Relu le 2026-09-03. L'appel de fonctions est un contrat : un modèle émet une requête structurée, l'application la valide et l'exécute, puis le résultat est renvoyé au modèle ou au workflow. Le modèle ne reçoit pas le droit d'exécuter une action du seul fait de nommer une fonction.

## Le contrat {#the-contract}

```text
user request
    -> model selects a declared tool
    -> application validates name, schema, policy, and approval
    -> application executes or rejects the call
    -> structured result becomes the next model/workflow input
```

| Champ | Exigence |
|---|---|
| Nom de l'outil | Stable, unique et présent dans une liste d'autorisation |
| Arguments | Schéma typé avec contraintes et exemples lorsque l'ambiguïté l'exige |
| Appelant | Identifiant d'exécution, version de l'agent et identité de la politique d'outils |
| Délai | Durée d'exécution bornée et comportement en cas d'annulation |
| Résultat | Enveloppe structurée de succès ou d'erreur |
| Effet de bord | Approbation explicite et clé d'idempotence lorsque l'effet est significatif |

La même boucle, gérée par l'application, apparaît dans les API des différents fournisseurs. Claude documente les appels d'outils côté client comme une requête du modèle suivie de l'exécution par l'application et d'un résultat d'outil ; Gemini documente la même répartition des responsabilités pour l'exécution des fonctions. [Claude tool-use contract](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Un dispatcher minimal et sûr {#a-minimal-safe-dispatcher}

Cet exemple Python 3.11+ garde la validation et l'autorité en dehors de la réponse du modèle.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    payload: dict[str, Any]


def get_weather(city: str, units: str = "celsius") -> ToolResult:
    if units not in {"celsius", "fahrenheit"}:
        return ToolResult(False, {"error": "unsupported_units"})
    return ToolResult(True, {"city": city, "units": units, "temperature": 20})


TOOLS = {"get_weather": get_weather}


def dispatch(call: dict[str, Any]) -> ToolResult:
    name = call.get("name")
    arguments = call.get("arguments")
    if name not in TOOLS:
        return ToolResult(False, {"error": "tool_not_allowed"})
    if not isinstance(arguments, dict):
        return ToolResult(False, {"error": "invalid_arguments"})
    city = arguments.get("city")
    units = arguments.get("units", "celsius")
    if not isinstance(city, str) or not city:
        return ToolResult(False, {"error": "city_required"})
    if not isinstance(units, str):
        return ToolResult(False, {"error": "invalid_units"})
    return TOOLS[name](city=city, units=units)


if __name__ == "__main__":
    print(dispatch({"name": "get_weather", "arguments": {"city": "Paris"}}))
```

En production, remplacez le résultat d'exemple par un appel de service borné et ajoutez l'authentification, la journalisation d'audit, l'idempotence ainsi qu'une validation de schéma propre au domaine.

## Règles de définition des outils {#tool-definition-rules}

| Règle | Justification |
|---|---|
| Décrire quand utiliser un outil et quand ne pas l'utiliser | Évite que des descriptions qui se chevauchent produisent une sélection arbitraire |
| Garder des schémas étroits | Rend la validation, la politique et la revue réalisables |
| Renvoyer des erreurs lisibles par machine | Permet au modèle de se rétablir sans analyser de la prose |
| Séparer les outils de lecture et d'écriture | Permet d'appliquer des politiques d'autorisation différentes |
| Lier l'accès aux outils à une phase ou à une tâche | Évite d'exposer des capacités inutilisées |
| Versionner toute modification de schéma non rétrocompatible | Les prompts et clients existants peuvent dépendre de l'ancienne forme |

Utilisez la sortie structurée pour une réponse finale qui doit respecter un schéma. Utilisez l'appel de fonctions lorsque le modèle a besoin d'une interaction intermédiaire avec une capacité détenue par l'application. Ces deux mécanismes répondent à des étapes différentes d'un workflow.

## Politique d'exécution {#execution-policy}

```json
{
  "tool_policy_id": "research-readonly-v2",
  "allowed_tools": ["search_sources", "read_document"],
  "requires_approval": ["publish_article", "send_email"],
  "timeout_ms": 15000,
  "idempotency_scope": "run_id:tool_call_id"
}
```

N'exprimez pas cette politique uniquement dans un prompt système. Appliquez-la dans le dispatcher ou la passerelle qui effectue l'action.

## Appels parallèles et tentatives {#parallel-calls-and-retries}

Les appels parallèles ne sont sûrs que si les opérations sont indépendantes et que l'ordre de leurs résultats est défini. Une nouvelle tentative d'écriture externe doit réutiliser la clé d'idempotence et réconcilier toute première tentative incertaine avant d'envoyer une nouvelle requête.

## Pièges {#gotchas}

- **Problème : appeler un nom d'outil fourni par le modèle sans liste d'autorisation.** La réponse d'un modèle est une entrée non fiable. **Correctif :** résoudre les noms via un registre côté serveur et rejeter les outils inconnus.
- **Problème : considérer la validation de schéma comme une autorisation.** Des arguments valides peuvent toujours demander une action non permise. **Correctif :** évaluer séparément l'identité, la politique, l'approbation et le budget, indépendamment de la forme des arguments.
- **Problème : renvoyer des erreurs en texte libre.** Le tour suivant du modèle peut inventer un chemin de récupération. **Correctif :** renvoyer des codes d'erreur stables, l'indication de réessayabilité et une action suivante sûre.
- **Problème : relancer des écritures après un délai d'attente.** L'appel initial a peut-être réussi. **Correctif :** persister une clé d'idempotence et interroger d'abord le reçu externe.

## Voir aussi {#see-also}

- [[tool-use-patterns]]
- [[agent-orchestration]]
- [[agent-security]]
- [[llm-api-integration]]

## Sources {#sources}

- [Claude : How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Claude : Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Gemini API : Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [OpenAI Agents SDK : Tools](https://openai.github.io/openai-agents-js/guides/tools/)
