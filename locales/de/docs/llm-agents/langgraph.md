---
title: "LangGraph (September 2026)"
category: frameworks
tags: [llm-agents, langgraph, state-machine, workflow, orchestration]
level: 3
source_sha256: cb854075391a363826e3a34df2c6fc548b0ad20cebc876a5832e61f463fb9b76
translation: machine
translated_at: '2026-10-24'
---
# LangGraph (September 2026) {#langgraph-september-2026}

Geprüft am 2026-09-03. LangGraph ist ein Low-Level-Framework und eine Laufzeitumgebung für langlebige, zustandsbehaftete Agenten-Workflows. Es kann LangChain-Komponenten verwenden, ein LangGraph-Workflow kann aber auch andere Modell- und Tool-Integrationen nutzen. [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)

## Was der Graph verantwortet {#what-the-graph-owns}

| Belang des Graphen | Explizit halten |
|---|---|
| State | Typisierte Felder und Merge-Semantik |
| Nodes | Eine begrenzte Operation pro Node |
| Edges | Deterministische oder nachvollziehbare Routing-Regeln |
| Persistenz | Checkpoint-Identität und Resume-Vertrag |
| Interrupts | Menschliche Freigabe oder externe Wartegrenze |
| Terminaler Zustand | Pass, HOLD, wiederholbarer Fehler oder Fehler |

Verwende einen Graphen, wenn der Workflow sichtbaren Zustand, Verzweigungen, Wiederanlauffähigkeit oder eine menschliche Grenze benötigt. Für eine einzelne, begrenzte Aufgabe mit einer von der Anwendung gesteuerten Agenten-Schleife ist eine einfachere Lösung ausreichend.

## Minimales StateGraph {#minimal-stategraph}

Dieses Python-3.11+-Beispiel enthält keinen Modellaufruf. Ersetze die deterministischen Nodes erst durch Provider-Aufrufe, wenn State und Kriterien für den terminalen Zustand klar sind.

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

## Gestaltungsregeln {#design-rules}

| Regel | Begründung |
|---|---|
| State serialisierbar halten | Checkpoints und Debugging benötigen eine dauerhafte Darstellung |
| Node-Ausgaben eng halten | Verringert versehentliche Mutationen und mehrdeutige Merges |
| Policy-Routen im Code festlegen | Budgets, Berechtigungen und Veröffentlichungsfreigaben sind keine Modellpräferenzen |
| Modell-Routing nur für offene Klassifikation nutzen | Es lässt sich als eigene Aufgabe evaluieren |
| Externe Belege als Referenzen im State speichern | Eine Textantwort ist kein Nachweis einer externen Nebenwirkung |

## Interrupt und Resume {#interrupt-and-resume}

Ein Interrupt ist ein Zustandsübergang und keine UI-Komfortfunktion. Bevor der Workflow für eine Freigabe oder externe Eingabe pausiert, sind folgende Angaben zu persistieren:

- Workflow-/Run-ID;
- Checkpoint oder State-Referenz;
- angeforderte Aktion und Nachweise;
- erforderliche Freigabeperson bzw. -rolle;
- Ablaufzeitpunkt und Resume-Regel.

Beim Fortsetzen sind zeitkritische Eingaben und Berechtigungen erneut zu prüfen. Eine Nebenwirkung wird nicht allein deshalb erneut ausgeführt, weil der Prozess neu gestartet wurde.

## LangGraph oder Anwendungscode {#langgraph-vs-application-code}

| LangGraph verwenden, wenn | Einfachen Anwendungscode verwenden, wenn |
|---|---|
| Der Workflow dauerhaften Zustand, Verzweigungen und Wiederherstellung benötigt | Die Aufgabe aus einer einzelnen, begrenzten Modell-/Tool-Schleife besteht |
| Betreiber einen sichtbaren Ausführungspfad benötigen | Eine einfache typisierte Funktionspipeline ausreicht |
| Eine menschliche Freigabe einen Neustart überstehen muss | Die Freigabe synchron und lokal erfolgt |
| Mehrere unabhängig getestete Nodes einen State-Vertrag teilen | Eine Aufteilung nur zusätzlichen Aufwand erzeugen würde |

## Fallstricke {#gotchas}

- **Problem: Ein Node-Name wird als Berechtigungsgrenze behandelt.** Ein Node kann weiterhin jedes Tool aufrufen, das seiner Laufzeitumgebung zur Verfügung steht. **Lösung:** Eine eigenständige Tool-Policy am Anwendungs- bzw. Tool-Gateway durchsetzen.
- **Problem: Verschachtelter State wird direkt verändert.** Parallele oder fortgesetzte Pfade können ungewollte Änderungen sehen. **Lösung:** Enge Updates zurückgeben und das Merge-Verhalten explizit definieren.
- **Problem: Schleife über Modell-Feedback ohne Obergrenze.** Eine Selbstkorrektur-Schleife kann das Budget unbegrenzt verbrauchen. **Lösung:** Versuchsanzahl, Validator-Ergebnis und einen terminalen HOLD-Zustand persistieren.
- **Problem: Fortsetzen eines externen Schreibvorgangs ohne Abgleich.** Der vorherige Versuch könnte erfolgreich gewesen sein. **Lösung:** Einen Idempotency-Key und eine Referenz auf den externen Beleg im State speichern.

## Siehe auch {#see-also}

- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-agent-messaging]]
- [[agent-evaluation]]
- [[production-patterns]]

## Quellen {#sources}

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph documentation index](https://docs.langchain.com/llms.txt)
