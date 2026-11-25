---
title: "Schémas d'utilisation d'outils (septembre 2026)"
category: patterns
tags: [llm-agents, tool-use, function-calling, mcp, authorization, observability]
level: 3
source_sha256: 87d66ca1145e644bd2212216442356d8530c2684669b660a950be98fc38879d7
translation: machine
translated_at: '2026-10-24'
---
# Schémas d'utilisation d'outils (septembre 2026) {#tool-use-patterns-september-2026}

Revu le 2026-09-03. Un outil est une capacité applicative exposée à un modèle au moyen d'un schéma. Il doit être conçu comme une API, avec autorisation, validation, délais d'expiration, journaux d'audit et sémantique d'échec explicite, et non comme un paragraphe supplémentaire dans un prompt.

## Manifeste d'outil {#tool-manifest}

```json
{
  "name": "search_sources",
  "version": "v2",
  "purpose": "Read approved public sources for a research run.",
  "input_schema": {"type": "object"},
  "access": "read_only",
  "timeout_ms": 15000,
  "idempotency": "not_required",
  "result_schema": "source-results/v1",
  "owner": "research-platform"
}
```

Chaque champ ci-dessus relève de la politique applicative. Un modèle peut demander la capacité déclarée, mais c'est la passerelle qui décide si l'appel est autorisé.

## Schémas de conception {#design-patterns}

| Schéma | Quand l'utiliser | Garde-fou requis |
|---|---|---|
| Recherche/récupération en lecture seule | Le modèle a besoin d'informations actuelles ou propriétaires | Liste blanche de sources et sortie avec citations/références |
| Écriture limitée | Le modèle propose un brouillon approuvé ou une mise à jour d'enregistrement | État d'approbation, idempotence et accusé de réception d'audit |
| Jeu d'outils par phase | Les étapes d'un workflow nécessitent des capacités différentes | Le contrôleur sélectionne la phase ; le modèle ne peut pas l'élargir |
| Recherche d'outils | Un catalogue volumineux consommerait le contexte | Politique de découverte et revue explicite des outils sélectionnés |
| Intégration MCP | Les outils sont fournis par un serveur distinct | Permissions contrôlées par l'hôte et revue de confiance du serveur |

MCP utilise une architecture hôte-client-serveur dans laquelle l'hôte contrôle le cycle de vie des clients et les permissions. [MCP Architecture](https://modelcontextprotocol.io/specification)

## Enveloppe de résultat {#result-envelope}

Renvoyez une enveloppe qui permet à l'étape suivante de distinguer un résultat d'un échec sans analyser de texte libre.

```python
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ToolEnvelope:
    status: str
    data: dict[str, Any]
    error_code: str | None = None
    retryable: bool = False


def read_document(document_id: str) -> ToolEnvelope:
    if document_id != "allowed-001":
        return ToolEnvelope(
            status="error",
            data={},
            error_code="document_not_allowed",
            retryable=False,
        )
    return ToolEnvelope(status="ok", data={"document_id": document_id, "text": "..."})


if __name__ == "__main__":
    print(asdict(read_document("allowed-001")))
```

Pour les outils à effets de bord, ajoutez à cette enveloppe l'identité de l'appelant ou de l'exécution, ainsi qu'une référence durable vers l'accusé de réception externe.

## Sélection des outils {#tool-selection}

Les descriptions doivent préciser :

- le résultat pour l'utilisateur que l'outil permet d'obtenir ;
- le format des entrées et les plages valides ;
- ce qu'il renvoie ;
- les cas où il ne doit pas être utilisé ;
- s'il lit, écrit ou déclenche une action externe.

Anthropic indique que les définitions d'outils et les résultats d'outils accumulés consomment du contexte, et recommande de choisir une méthode de gestion du contexte adaptée à la source de la pression. [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)

## Échecs et reprise {#failure-and-recovery}

| Échec | Comportement sûr |
|---|---|
| Outil inconnu | Rejeter sans exécution |
| Non-conformité au schéma | Renvoyer une erreur de validation stable |
| Permission refusée | Renvoyer le refus ; ne pas suggérer de contournement |
| Délai dépassé en lecture | Marquer comme réessayable et borner le budget de nouvelles tentatives |
| Délai dépassé en écriture | Marquer l'issue comme inconnue ; réconcilier l'accusé de réception avant toute nouvelle tentative |
| Résultat externe partiel | Conserver la référence ou l'accusé de réception et suspendre pour réconciliation |

## Pièges courants {#gotchas}

- **Problème : donner tous les outils à chaque agent.** Davantage d'outils crée de l'ambiguïté, un coût et une surface d'attaque plus large. **Correction :** exposer la liste blanche la plus restreinte, propre à la tâche.
- **Problème : utiliser un outil générique unique de recherche ou d'exécution.** Le modèle et l'opérateur ne peuvent pas savoir quelle politique s'applique. **Correction :** rendre explicites la finalité, l'autorité, les entrées et les sorties.
- **Problème : basculer silencieusement sur une solution de repli après un échec.** Un autre outil ou fournisseur peut modifier le traitement des données ou les effets de bord. **Correction :** enregistrer chaque repli avec son déclencheur, une garantie équivalente et un signal visible.
- **Problème : considérer un serveur MCP comme intrinsèquement fiable.** L'interopérabilité du protocole ne valide pas le comportement d'un serveur. **Correction :** vérifier l'identité du serveur, ses permissions, ses flux de données et le schéma de ses outils avant de l'exposer.

## Voir aussi {#see-also}

- [[function-calling]]
- [[agent-security]]
- [[agent-orchestration]]
- [[agent-observability-dashboards]]

## Sources {#sources}

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification)
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Claude: Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)
- [OpenAI Agents SDK: Tools](https://openai.github.io/openai-agents-js/guides/tools/)
