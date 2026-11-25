---
title: "LangChain-Framework"
category: frameworks
tags: [llm-agents, langchain, agents, middleware, langgraph, observability]
description: "Ein versionsbewusster Leitfaden zum aktuellen Agent-Harness von LangChain, zu Provider-Integrationen, Middleware, Zustandsverwaltung und Grenzen im Produktivbetrieb."
level: 3
source_sha256: 7febd62e904ce424c976918dfc93cd51ca429f5710660dfd1bd3cbaffdce2479
translation: machine
translated_at: '2026-10-24'
---
# LangChain-Framework {#langchain-framework}

**Stand der Prüfung: 2026-09-03.** LangChain ist inzwischen auf `create_agent` ausgerichtet: ein konfigurierbares Agent-Harness, das sich aus einem Modell, Tools, einem System-Prompt und Middleware zusammensetzt. Es ist sinnvoll, wenn eine Anwendung diese Zusammensetzung und die Portabilität zwischen Providern benötigt; für eine einfache Modellintegration mit einem einzelnen Aufruf ist es nicht erforderlich. [LangChain-Überblick](https://docs.langchain.com/oss/python/langchain/overview)

## Die richtige Schicht wählen {#choose-the-right-layer}

| Bedarf | Empfohlen | Begründung |
|---|---|---|
| Ein Modellaufruf oder ein stabiler Tool-Aufruf | Provider-SDK | Kleinste Angriffsfläche und klarste Fehlerbilder |
| Konfigurierbares Tool-nutzendes Harness | LangChain `create_agent` | Modell, Tools, Prompt und Middleware werden explizit zusammengesetzt |
| Dauerhafte Zustandsmaschine, Freigaben oder gemischter deterministischer/agentischer Ablauf | LangGraph | Die Orchestrierung auf niedrigerer Ebene ist für diese Kontrollpunkte ausgelegt |
| Traces, Evaluation und Fehlerdiagnose im Betrieb | LangSmith oder Vergleichbares | Observability ist vom Laufzeitvertrag getrennt |

Die Wahl des Frameworks ersetzt keine Autorisierung, Validierung oder Domänenlogik. Geldbewegungen, Veröffentlichungen, Zugriffskontrolle und nicht umkehrbare Wirkungen gehören in deterministischen Anwendungscode.

## Minimaler Agent-Vertrag {#minimal-agent-contract}

Ein Agent ist ein Modell, das in einer Schleife Tools aufruft. Ein Produktiv-Harness benötigt für jede Schicht einen expliziten Vertrag:

| Schicht | Deklarieren | Verifizieren |
|---|---|---|
| Modell | Provider, Modellkennung, Timeout, Retry-Richtlinie | Provider-Fähigkeit und Fehlerbeleg |
| Tools | Eingabeschema, Ausgabeschema, Berechtigungsklasse, Wirkungsstufe | serverseitige Validierung und Tool-Beleg |
| Zustand | Thread-Identität, Checkpoint-Richtlinie, Aufbewahrung | Wiederherstellungs- und Abbruchtest |
| Middleware | Routing, Schutzmechanismen, Retries, Kontextrichtlinie | deterministischer Test pro Richtlinie |
| Observability | Trace-ID, Modell-/Tool-Versionen, Ergebnis | Trace mit dem terminalen Beleg verknüpft |

Eine providerneutrale Schnittstelle ist kein Nachweis, dass alle Provider identische Kontextfenster, Tool-Semantik, Garantien für strukturierte Ausgaben oder regionale Verfügbarkeit bieten.

## Aktueller Ausgangspunkt {#current-starting-point}

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

Das Beispiel hält das Tool bewusst klein. Die Funktion muss trotzdem den Aufrufer authentifizieren, die `project_id` validieren, den Geltungsbereich durchsetzen und bei nicht verfügbarer Aktion einen strukturierten Fehler zurückgeben. Das Modell sollte keine weitreichenden Datenbank-Zugangsdaten erhalten, nur weil das Tool bequem ist.

## Middleware ist eine Richtliniengrenze {#middleware-is-a-policy-boundary}

Middleware kann Routing, Retries, Tool-Richtlinien, Kontextverwaltung und Guardrails hinzufügen. Jede Ergänzung ist als ausführbare Richtlinie zu behandeln und nicht als Dekoration:

1. Auslöser und erwartetes Ergebnis festhalten;
2. Eigentümer und Version der Richtlinie benennen;
3. Erlaubnis-, Ablehnungs-, Retry- und Eskalationspfade beobachtbar machen;
4. die Richtlinie mit fehlerhaften Eingaben und nicht verfügbaren Abhängigkeiten testen;
5. einen deterministischen Fallback nur dann beibehalten, wenn er dieselben Sicherheitsgarantien erhält.

Ein Retry-Wrapper kann etwa einen vorübergehenden Modellfehler behandeln. Er darf jedoch keinen Tool-Aufruf stillschweigend wiederholen, der etwas veröffentlichen, belasten, löschen oder eine Nachricht senden könnte.

## Zustand und dauerhafte Arbeit {#state-and-durable-work}

LangChain-Agenten basieren auf LangGraph, das dauerhafte Ausführung, Persistenz und Human-in-the-Loop-Unterstützung bereitstellt. Das ist für langlaufende Arbeit nützlich, doch Persistenz verändert den Datenvertrag: Dokumentieren Sie, welcher Zustand gespeichert wird, wer ihn wiederherstellen darf und wie eine unterbrochene externe Wirkung abgeglichen wird. [LangChain-Überblick](https://docs.langchain.com/oss/python/langchain/overview)

Verwenden Sie einen Aufgabendatensatz außerhalb des Modellkontexts:

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

Die Laufzeitumgebung darf diesen Datensatz für das Modell zusammenfassen, doch die Anwendung bleibt die maßgebliche Instanz für Übergänge, Freigaben und den terminalen Beleg.

## Observability und Evaluation {#observability-and-evaluation}

Tracing kann Prompts, Tool-Aufrufe, Zustandsübergänge, Latenzen und Fehler sichtbar machen. Es belegt jedoch nicht, dass die Ausgabe korrekt ist. Ergänzen Sie Traces um:

- einen repräsentativen, versionierten Evaluationsdatensatz;
- erwartete Fälle für Tool-Aufrufe und Ablehnungen;
- Qualitätsmaße, die an die Aufgabe gebunden sind und nicht an die Token-Anzahl;
- Regeln für Schwärzung und Aufbewahrung von Prompts, Tool-Eingaben und Ausgaben;
- einen Prüfpfad für folgenschwere Fehler.

LangSmith dokumentiert Tracing und Evaluation für Agenten, die mit LangChain, LangGraph und anderen Frameworks gebaut wurden. [LangSmith-Observability](https://docs.langchain.com/langsmith/observability)

## Fallstricke {#gotchas}

- **Alte Beispiele verwenden veraltete Chain- und Memory-Helfer.** Sie können weiterhin in Suchergebnissen auftauchen. **Lösung:** Beginnen Sie mit der aktuellen Dokumentation zu `create_agent` und den Provider-Integrationen und fixieren Sie anschließend die Paketversionen, die Sie testen.
- **Eine gemeinsame Modellschnittstelle ist keine gemeinsame Fähigkeitsgarantie.** Provider unterscheiden sich bei Tool-Aufrufen, Grenzwerten und Fehlerverhalten. **Lösung:** Validieren Sie die gewählte Kombination aus Modell und Provider in der CI oder in einem kontrollierten Canary-Betrieb.
- **Middleware kann einen wirksamen Retry verbergen.** Ein Modell-Retry ist für eine externe Aktion nicht zwingend sicher. **Lösung:** Idempotenz und Abgleich an der Executor-Grenze umsetzen.
- **Trace-Daten können zu einem Schattendatenspeicher werden.** Debug-Logs enthalten häufig Prompts und Tool-Ausgaben. **Lösung:** Observability-Daten klassifizieren, schwärzen, einschränken und ablaufen lassen.
- **Zustandspersistenz ist kein Berechtigungssystem.** Das Wiederherstellen eines Checkpoints darf keine abgelaufene Berechtigung wiederherstellen. **Lösung:** Fähigkeiten und Freigaben zum Zeitpunkt der Wirkung erneut prüfen.

## Quellen {#sources}

- [LangChain-Überblick](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain-Agenten](https://docs.langchain.com/oss/python/langchain/agents)
- [LangChain-Provider-Integrationen](https://docs.langchain.com/oss/python/integrations/providers/overview)
- [LangSmith-Observability](https://docs.langchain.com/langsmith/observability)

## Siehe auch {#see-also}

- [[langgraph]]
- [[agent-orchestration]]
- [[tool-use-patterns]]
- [[agent-safety-alignment]]
- [[llmops]]
