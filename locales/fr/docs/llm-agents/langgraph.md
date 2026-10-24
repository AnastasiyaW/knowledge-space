---
title: "LangGraph (septembre 2026)"
category: frameworks
tags: [llm-agents, langgraph, state-machine, workflow, orchestration]
level: 3
source_sha256: cb854075391a363826e3a34df2c6fc548b0ad20cebc876a5832e61f463fb9b76
translation: machine
translated_at: '2026-10-24'
---
# LangGraph (septembre 2026) {#langgraph-september-2026}

Relu le 2026-09-03. LangGraph est un framework d'orchestration bas niveau et un runtime pour des workflows d'agents à état et de longue durée. Il peut utiliser des composants LangChain, mais un workflow LangGraph peut aussi utiliser d'autres intégrations de modèles et d'outils. [Vue d'ensemble de LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)

## Ce que le graphe gère {#what-the-graph-owns}

| Préoccupation du graphe | À rendre explicite |
|---|---|
| État | Champs typés et sémantique de fusion |
| Nœuds | Une opération bornée par nœud |
| Arêtes | Règles de routage déterministes ou auditables |
| Persistance | Identité du checkpoint et contrat de reprise |
| Interruptions | Approbation humaine ou frontière d'attente externe |
| État terminal | Succès, mise en attente, échec réessayable ou échec |

Utilisez un graphe lorsque le workflow nécessite un état visible, des branchements, la possibilité de redémarrer ou une frontière humaine. Une boucle d'agent unique contrôlée par l'application est plus simple pour une tâche bornée.

## StateGraph minimal {#minimal-stategraph}

Cet exemple Python 3.11+ ne contient aucun appel de modèle. Remplacez les nœuds déterministes par des appels à un fournisseur uniquement une fois l'état et les critères terminaux clairement définis.

```python
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    text: str
    verdict: str


def classify(state: ReviewState) -> dict[str, str]:
    verdict = "review" if "citation" in state["text"].lower() else "pass"
    return {"verdict": verdict}


def route(state: ReviewState) -> str:
    return "human_review" if state["verdict"] == "review" else "done"


def human_review(state: ReviewState) -> dict[str, str]:
    return {"verdict": "held_for_review"}


builder = StateGraph(ReviewState)
builder.add_node("classify", classify)
builder.add_node("human_review", human_review)
builder.add_node("done", lambda state: {})
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("human_review", END)
builder.add_edge("done", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"text": "add a citation", "verdict": ""}))
```

## Règles de conception {#design-rules}

| Règle | Raison |
|---|---|
| Garder l'état sérialisable | Les checkpoints et le débogage nécessitent une représentation durable |
| Rendre les sorties des nœuds étroites | Réduit les mutations accidentelles et les fusions ambiguës |
| Placer les routes de politique dans le code | Budgets, permissions et portes de publication ne sont pas des préférences du modèle |
| Utiliser le routage par modèle uniquement pour la classification ouverte | Il peut être évalué comme une tâche séparée |
| Stocker les reçus externes sous forme de références dans l'état | Une réponse textuelle n'est pas la preuve d'un effet de bord externe |

## Interruption et reprise {#interrupt-and-resume}

Une interruption est une transition d'état, pas un confort d'interface. Avant de suspendre l'exécution pour une approbation ou une entrée externe, persistez :

- l'identifiant du workflow/de l'exécution ;
- le checkpoint ou la référence d'état ;
- l'action demandée et les éléments de preuve ;
- l'identité ou le rôle de l'approbateur requis ;
- la date d'expiration et la règle de reprise.

À la reprise, revalidez les entrées sensibles au temps et les permissions. Ne rejouez pas un effet de bord simplement parce que le processus a redémarré.

## LangGraph ou code applicatif {#langgraph-vs-application-code}

| Utilisez LangGraph lorsque | Utilisez du code applicatif simple lorsque |
|---|---|
| Le workflow comporte un état durable, des branchements et une reprise sur incident | La tâche est une boucle modèle/outil bornée |
| Les opérateurs ont besoin d'un chemin d'exécution visible | Un simple pipeline de fonctions typées suffit |
| Une approbation humaine doit survivre à un redémarrage | L'approbation est synchrone et locale |
| Plusieurs nœuds testés indépendamment partagent un contrat d'état | La séparation n'ajouterait que de la lourdeur |

## Pièges courants {#gotchas}

- **Problème : considérer le nom d'un nœud comme une frontière d'autorisation.** Un nœud peut toujours appeler n'importe quel outil exposé à son runtime. **Correction :** appliquer une politique d'outils distincte au niveau de la passerelle applicative/outils.
- **Problème : modifier un état imbriqué sur place.** Des chemins concurrents ou repris peuvent voir des changements non voulus. **Correction :** renvoyer des mises à jour étroites et définir explicitement le comportement de fusion.
- **Problème : boucler sur le retour du modèle sans limite.** Une boucle d'auto-correction peut consommer le budget indéfiniment. **Correction :** persister le nombre de tentatives, le résultat du validateur et un état terminal HOLD.
- **Problème : reprendre une écriture externe sans réconciliation.** La tentative précédente a peut-être réussi. **Correction :** stocker une clé d'idempotence et une référence de reçu externe dans l'état.

## Voir aussi {#see-also}

- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-agent-messaging]]
- [[agent-evaluation]]
- [[production-patterns]]

## Sources {#sources}

- [Vue d'ensemble de LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [Index de la documentation LangGraph](https://docs.langchain.com/llms.txt)
