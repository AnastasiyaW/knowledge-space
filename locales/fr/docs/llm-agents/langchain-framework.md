---
title: "Framework LangChain"
category: frameworks
tags: [llm-agents, langchain, agents, middleware, langgraph, observability]
description: "Guide tenant compte des versions sur le harnais d'agent actuel de LangChain, les intégrations de fournisseurs, le middleware, l'état et les limites de production."
level: 3
source_sha256: 7febd62e904ce424c976918dfc93cd51ca429f5710660dfd1bd3cbaffdce2479
translation: machine
translated_at: '2026-10-24'
---
# Framework LangChain {#langchain-framework}

**Périmètre vérifié : 2026-09-03.** LangChain s'articule désormais autour de `create_agent` : un harnais d'agent configurable, composé à partir d'un modèle, d'outils, d'un prompt système et de middleware. Il est utile lorsqu'une application a besoin de cette composition et de portabilité entre fournisseurs ; il n'est pas nécessaire pour une intégration de modèle en un seul appel. [Vue d'ensemble de LangChain](https://docs.langchain.com/oss/python/langchain/overview)

## Choisir le bon niveau {#choose-the-right-layer}

| Besoin | Privilégier | Pourquoi |
|---|---|---|
| Un appel de modèle ou un appel d'outil stable | SDK du fournisseur | Surface minimale et modes de défaillance les plus clairs |
| Harnais configurable utilisant des outils | `create_agent` de LangChain | Modèle, outils, prompt et middleware sont composés explicitement |
| Machine à états durable, approbations ou flux mixtes déterministes/agentiques | LangGraph | L'orchestration de bas niveau est conçue pour ces points de contrôle |
| Traces, évaluation et diagnostic en production | LangSmith ou équivalent | L'observabilité est distincte du contrat d'exécution |

Le choix du framework ne remplace ni l'autorisation, ni la validation, ni la logique métier. Conservez les mouvements d'argent, les publications, le contrôle d'accès et les effets irréversibles dans du code applicatif déterministe.

## Contrat minimal d'un agent {#minimal-agent-contract}

Un agent est un modèle qui appelle des outils dans une boucle. Un harnais de production a besoin d'un contrat explicite pour chaque couche :

| Couche | Déclarer | Vérifier |
|---|---|---|
| Modèle | fournisseur, identifiant du modèle, délai d'expiration, politique de relance | capacités du fournisseur et reçu d'erreur |
| Outils | schéma d'entrée, schéma de sortie, classe de permission, niveau d'effet | validation côté serveur et reçu de l'outil |
| État | identité du fil, politique de points de contrôle, rétention | test de restauration et d'annulation |
| Middleware | routage, garde-fous, relances, politique de contexte | test déterministe pour chaque politique |
| Observabilité | identifiant de trace, versions modèle/outil, résultat | trace liée au reçu terminal |

Ne considérez pas une interface indépendante du fournisseur comme une preuve que tous les fournisseurs offrent des fenêtres de contexte, une sémantique d'outils, des garanties de sortie structurée ou une disponibilité régionale identiques.

## Point de départ actuel {#current-starting-point}

```python
# pip install -U langchain "langchain[anthropic]"
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def lookup_project(project_id: str) -> dict:
    """Return a public project record after server-side authorization."""
    return {"project_id": project_id, "status": "published"}


agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[lookup_project],
    system_prompt="Use tools only for public project records.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Show project happyin-space"}]}
)
```

L'exemple volontairement réduit garde l'outil petit. La fonction doit malgré tout authentifier l'appelant, valider le `project_id`, appliquer le périmètre et renvoyer une erreur structurée lorsque l'action est indisponible. Le modèle ne doit pas recevoir d'identifiants de base de données étendus simplement parce que l'outil est pratique.

## Le middleware est une frontière de politique {#middleware-is-a-policy-boundary}

Le middleware peut ajouter du routage, des relances, une politique d'outils, une gestion du contexte et des garde-fous. Traitez chaque ajout comme une politique exécutable, et non comme une simple décoration :

1. énoncer le déclencheur et le résultat attendu ;
2. nommer le responsable de la politique et sa version ;
3. rendre observables les chemins d'autorisation, de refus, de relance et d'escalade ;
4. tester la politique avec des entrées malformées et des dépendances indisponibles ;
5. ne conserver un repli déterministe que s'il préserve les mêmes garanties de sécurité.

Par exemple, un wrapper de relance peut gérer une erreur transitoire du modèle. Il ne doit pas rejouer silencieusement un appel d'outil susceptible de publier, débiter, supprimer ou envoyer un message.

## État et travail durable {#state-and-durable-work}

Les agents LangChain sont construits sur LangGraph, qui fournit l'exécution durable, la persistance et la prise en charge de l'intervention humaine. C'est utile pour les travaux de longue durée, mais la persistance modifie le contrat de données : consignez quel état est conservé, qui peut le restaurer, et comment un effet externe interrompu est réconcilié. [Vue d'ensemble de LangChain](https://docs.langchain.com/oss/python/langchain/overview)

Utilisez un enregistrement de tâche en dehors du contexte du modèle :

```json
{
  "task_id": "research-044",
  "state": "awaiting_review",
  "input_revision": "source-set@2026-09-03",
  "allowed_actions": ["draft_article"],
  "approval_ref": null,
  "terminal_receipt": null
}
```

Le runtime peut résumer cet enregistrement pour le modèle, mais l'application reste l'autorité pour les transitions, l'approbation et le reçu terminal.

## Observabilité et évaluation {#observability-and-evaluation}

Le traçage peut montrer les prompts, les appels d'outils, les transitions d'état, la latence et les erreurs. Il ne prouve pas que le résultat est correct. Associez les traces à :

- un jeu d'évaluation représentatif et versionné ;
- des cas attendus d'appels d'outils et de refus ;
- des mesures de qualité liées à la tâche plutôt qu'au nombre de tokens ;
- des règles de masquage et de rétention pour les prompts, les entrées et sorties d'outils ;
- un circuit de revue pour les défaillances à fort impact.

LangSmith documente le traçage et l'évaluation des agents construits avec LangChain, LangGraph et d'autres frameworks. [Observabilité LangSmith](https://docs.langchain.com/langsmith/observability)

## Pièges {#gotchas}

- **Les anciens exemples utilisent des helpers de chaînes et de mémoire dépréciés.** Ils peuvent encore apparaître dans les résultats de recherche. **Correctif :** partir de la documentation actuelle de `create_agent` et des intégrations de fournisseurs, puis épingler les versions de paquets que vous testez.
- **Une interface de modèle commune n'est pas un contrat de capacités commun.** Les fournisseurs diffèrent sur l'appel d'outils, les limites et le comportement en cas d'erreur. **Correctif :** valider la paire modèle-fournisseur retenue en CI ou lors d'un canari contrôlé.
- **Le middleware peut masquer une relance à effet de bord.** Une relance de modèle n'est pas forcément sûre pour une action externe. **Correctif :** placer l'idempotence et la réconciliation à la frontière de l'exécuteur.
- **Les données de trace peuvent devenir un magasin de données parallèle.** Les journaux de débogage contiennent souvent prompts et sorties d'outils. **Correctif :** classer, masquer, restreindre et faire expirer les données d'observabilité.
- **La persistance de l'état n'est pas un système de permissions.** La restauration d'un point de contrôle ne doit pas restaurer une autorité expirée. **Correctif :** revalider les capacités et les approbations au moment de l'effet.

## Sources {#sources}

- [Vue d'ensemble de LangChain](https://docs.langchain.com/oss/python/langchain/overview)
- [Agents LangChain](https://docs.langchain.com/oss/python/langchain/agents)
- [Intégrations de fournisseurs LangChain](https://docs.langchain.com/oss/python/integrations/providers/overview)
- [Observabilité LangSmith](https://docs.langchain.com/langsmith/observability)

## Voir aussi {#see-also}

- [[langgraph]]
- [[agent-orchestration]]
- [[tool-use-patterns]]
- [[agent-safety-alignment]]
- [[llmops]]
