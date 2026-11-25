---
title: "Grundlagen von Agenten"
description: "Zentrale Verträge für LLM-Agenten: Modellentscheidungen, Tools, Zustand, Richtlinien, Nachweise und kontrollierte Autonomie"
level: 2
source_sha256: a207fedf0efb8cbba88c3a3b8899577449322ac47be91c09fb4db308ec721e67
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen von Agenten (September 2026) {#agent-fundamentals-september-2026}

Versionskontext: Ein Agent ist ein System, keine Modellfähigkeit. Erfassen Sie bei jeder bereitgestellten Agentenversion die Modellrevision, die Prompt- und Tool-Richtlinie, das Zustandsschema und die Evaluierungssuite.

Ein LLM-Agent kombiniert Modellinferenz mit einer Steuerungsebene, die Eingaben beobachtet, zulässige Aktionen auswählt, Zustand persistiert und Nachweise zurückgibt. Ein Chatbot wird erst dann zum Agenten, wenn er über steuerbare Fähigkeiten eine Umgebung beeinflussen oder abfragen kann.

## Kernkomponenten {#core-components}

| Komponente | Verantwortung | Muss deterministisch sein? |
|---|---|---|
| Modell | Sprache, strukturierte Ausgabe oder nächste Aktion vorschlagen | Nein |
| Anweisungen | Rolle, Einschränkungen und Ausgabevertrag definieren | Versioniert |
| Tools | Über typisierte Schnittstellen lesen oder handeln | Ja, an der Grenze |
| Richtlinienschicht | Aktionen autorisieren und Budgets durchsetzen | Ja |
| Zustandsspeicher | Arbeitseinheiten, Belege und Wiederherstellungsdaten persistieren | Ja |
| Evaluator | Entscheiden, ob das Endergebnis die Abnahmekriterien erfüllt | Ja / unabhängig geprüft |
| Observability | Modellaufrufe, Tools, Entscheidungen und Fehler korrelieren | Ja |

Das Modell ist keine Quelle der Wahrheit für Berechtigungen, Fakten, Aufgabenabschluss oder den Status von Nebenwirkungen.

## Lebenszyklus eines Agenten {#agent-lifecycle}

```text
request -> validate identity and input -> create durable work item
        -> choose a permitted next action -> execute or refuse
        -> persist receipt -> verify terminal result -> respond
```

Eine Arbeitseinheit sollte eine eindeutige ID, einen Akteur- bzw. Mandantenbezug, einen Idempotenzschlüssel, ein Versuchsbudget, eine Richtlinienrevision, eine Trace-Referenz und einen abschließenden Beleg besitzen. Die erneute Ausführung derselben Anfrage muss sicher sein oder ausdrücklich abgelehnt werden.

## Tools {#tools}

Ein Tool ist eine typisierte Fähigkeit mit einem Verantwortlichen, nicht bloß eine Beschreibung in natürlicher Sprache.

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

Validieren Sie die vom Modell vorgeschlagenen Parameter serverseitig. Ein gültiges Schema beweist nicht, dass ein Aufruf autorisiert ist; die Autorisierung muss Akteur, Mandant, Ressource, Aktion und die aktuelle Richtlinie einbeziehen.

## Zustand und Gedächtnis {#state-and-memory}

Trennen Sie diese Objekte:

- **Gesprächskontext:** die minimal nötigen Informationen für den nächsten Modellzug.
- **Laufzustand:** aktueller Workflow-Zustand, Versuchszähler und Tool-Belege.
- **Langzeitgedächtnis:** abgegrenzte Einträge mit Eigentümerschaft, Ablaufzeit und Schreibrichtlinie.
- **Wissenskorpus:** Quellmaterial, das mit Herkunftsnachweis abgerufen wird.

Ein Kontextfenster ist keine Datenbank. Speichern Sie keine undurchsichtigen Fakten im Prompt und bezeichnen Sie das nicht als dauerhaftes Gedächtnis.

## Agent versus Workflow {#agent-versus-workflow}

| Frage | Workflow bevorzugen | Agent in Betracht ziehen |
|---|---|---|
| Ist die Schrittfolge bereits bekannt? | Ja | Nur, wenn eine unbekannte Entscheidung verbleibt |
| Sind Aktionen mit hohen Auswirkungen oder nicht umkehrbar? | Ja, mit Freigaben | Nur innerhalb einer eng gefassten Richtliniengrenze |
| Ändert neue Evidenz den nächsten Schritt? | Meist nicht nötig | Ja, mit expliziten Stopp- bzw. Neuplanungsbedingungen |
| Lässt sich der Erfolg maschinell prüfen? | Ja | Vor produktiver Autonomie erforderlich |
| Sind Latenz und Kosten eng begrenzt? | In der Regel | Erst, nachdem die Evaluierung den Nutzen belegt hat |

Beginnen Sie mit einem Workflow und führen Sie eine Modellentscheidung an der kleinsten Stelle ein, an der sie einen messbaren Nutzen bringt.

## Einfaches Aktions-Gateway {#basic-action-gateway}

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

Produktivcode ergänzt die tatsächliche Identitätsprüfung, einen Repository-Aufruf, die Persistierung des Audit-Protokolls, die Weitergabe von Fristen und die Richtlinienabfrage. Die wichtige Invariante lautet: Das Modell umgeht dieses Gateway niemals.

## Autonomiestufen {#autonomy-levels}

Wählen Sie pro Aktion eine explizite Stufe:

1. nur vorschlagen — Mensch oder Anwendung führt sie aus;
2. nur lesend ausführen — das System liefert Nachweise;
3. umkehrbare Aktion ausführen — begrenzte Wiederholung und Beleg;
4. externe bzw. nicht umkehrbare Aktion ausführen — explizite Freigabe;
5. autonomer dauerhafter Workflow — erst nach durchgängiger Evaluierung und Vorfallkontrollen.

Ein Agent kann für verschiedene Tools auf unterschiedlichen Stufen arbeiten. Gewähren Sie nie global die höchste Stufe, nur weil es eine risikoarme Aufgabe gibt.

## Interoperabilität {#interoperability}

MCP standardisiert eine Host-/Client-/Server-Grenze für Ressourcen, Prompts und Tools. A2A standardisiert die Kommunikation mit einem unabhängigen Agentendienst über Agenten-Discovery, Tasks, Nachrichten und Artefakte. Keines der beiden Protokolle ersetzt Identität, Autorisierung, Datenverwaltung auf Anwendungsebene oder aufgabenbezogene Nachweise.

Verwenden Sie Protokolle, um eine reale Grenze zu definieren, nicht um einer In-Process-Funktion unnötigen Aufwand hinzuzufügen.

## Observability und Evaluierung {#observability-and-evaluation}

Erfassen Sie Aktionsvorschläge, Richtlinienentscheidungen, Ein- und Ausgaben von Tool-Aufrufen mit angemessener Schwärzung, Wiederholungsgründe, Zeitverhalten, Kosten und das abschließende Urteil. Evaluierungen sollten normale Anfragen, fehlerhafte Eingaben, abgelehnte Aktionen, Injection-Versuche, Tool-Ausfälle, doppelte Einreichungen und Wiederherstellung abdecken.

## Fallstricke {#gotchas}

- **Mehr Tools bedeuten nicht automatisch mehr Fähigkeit.** Sie erhöhen Mehrdeutigkeit und Angriffsfläche. **Abhilfe:** Stellen Sie nur die aufgabenbezogene Allowlist bereit.
- **Eine erfolgreiche API-Antwort ist kein Aufgabenabschluss.** Sie kann unvollständige, veraltete oder nicht autorisierte Daten enthalten. **Abhilfe:** Definieren Sie eine eigene Abnahmeprüfung, die am Nutzerergebnis ausgerichtet ist.
- **Wachsender Kontext verdeckt Zustandsverlust.** Lange Verlaufstranskripte werden teuer und können kritische Fakten auslassen. **Abhilfe:** Persistieren Sie strukturierten Zustand und rufen Sie eine minimale, autorisierte Projektion ab.
- **Ein Protokoll ist für sich genommen keine Sicherheitsgrenze.** MCP-/A2A-Metadaten kündigen Fähigkeiten an, können aber keine Berechtigung gewähren. **Abhilfe:** Erzwingen Sie Autorisierung an jedem lokalen oder entfernten Aktions-Gateway.

## Quellen {#sources}

- [OpenAI Agents SDK: agents](https://openai.github.io/openai-agents-python/agents/)
- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI API: function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Siehe auch {#see-also}

- [[agent-design-patterns]]
- [[agent-architectures]]
- [[agent-memory]]
- [[function-calling]]
- [[agent-security]]
