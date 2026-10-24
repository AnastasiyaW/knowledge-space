---
title: "Dashboards zur Beobachtbarkeit von Agenten"
description: "Trace-Verträge, Dashboard-Ansichten und datensparsame Telemetrie für werkzeugnutzende und Multi-Agenten-Systeme; geprüft am 2026-09-03."
level: 3
source_sha256: b79e8a8f26cf69b6498bac22401dc7d84c5ce9435e6c926b8f4ee8d1f1432878
translation: machine
translated_at: '2026-10-24'
---
# Dashboards zur Beobachtbarkeit von Agenten {#agent-observability-dashboards}

Geprüft am 2026-09-03. Ein Observability-Dashboard beantwortet vier operative Fragen: Welche Arbeit wurde ausgeführt, welche Instanz hat gehandelt, welche Werkzeuge oder Modelle waren beteiligt und welche Nachweise machen das Ergebnis vertrauenswürdig. Es sollte nicht von einem bestimmten IDE-Hook oder einem Herstellerereignisnamen abhängen.

## Mit einem Trace-Vertrag beginnen {#start-with-a-trace-contract}

Verwenden Sie einen Trace für einen für Nutzer sichtbaren Workflow oder ein dauerhaftes Arbeitselement. Jeder Modellaufruf, Werkzeugaufruf, Handoff, Validator und jede Freigabe wird zu einem untergeordneten Span oder Ereignis.

```json
{
  "schema_version": "agent-trace/v1",
  "timestamp": "2026-09-03T14:10:31.442Z",
  "trace_id": "tr_01J...",
  "span_id": "sp_01J...",
  "parent_span_id": "sp_01J-parent",
  "run_id": "run_01J...",
  "operation": "tool.fetch_source",
  "actor": { "kind": "agent", "id": "researcher@2026-09-03" },
  "outcome": "ok",
  "duration_ms": 184,
  "input_ref": "source:42",
  "output_ref": "artifact:claim-set-42",
  "tool": { "name": "fetch_source", "policy_id": "research-readonly-v2" },
  "attributes": { "attempt": 1, "environment": "production" }
}
```

Legen Sie keine Geheimnisse, rohen Nutzer-Prompts, Zugriffstoken oder uneingeschränkte Werkzeugausgaben in die Standard-Ereignisnutzlast. Speichern Sie bei Bedarf für die Wiederholbarkeit eine kontrollierte Referenz oder einen Digest.

## Minimale Span-Taxonomie {#minimum-span-taxonomy}

| Operation | Übergeordnet | Pflichtfelder | Nachweis des Erfolgs |
|---|---|---|---|
| Workflow | Keiner | Run-ID, Ziel, Verantwortlicher, Endzustand | Abschlussbeleg |
| Agenten-Turn | Workflow | Agenten-/Konfigurationsversion, Modell, Referenzen für Ein- und Ausgabe | validierte Ausgabe oder Fehler |
| Werkzeugaufruf | Agenten-Turn | Allowlist-Richtlinie, Werkzeugname, Referenz auf Argumente, Frist | Werkzeugbeleg |
| Handoff | Agenten-Turn | Verantwortlicher von/an, Weiterleitungsgrund, Kontextreferenz | akzeptierter Handoff |
| Validator | Workflow | Version der Kriterien, Ergebnis, Referenz auf Befunde | Prüfbericht mit Bestanden/Nicht bestanden |
| Freigabe | Workflow | Identität des Prüfers, Geltungsbereich, Entscheidung | Freigabebeleg |

Das Projekt OpenTelemetry GenAI Semantic Conventions beschreibt Spans, Metriken und Ereignisse für GenAI-Clients und MCP. Verwenden Sie dessen Konventionen, wo sie passen; anwendungsspezifische Felder sollten namensraumgetrennt und dokumentiert sein. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Ein strukturiertes Ereignis ausgeben {#emit-a-structured-event}

Dieses abhängigkeitsfreie Python-3.11+-Beispiel schreibt pro Zeile ein JSON-Ereignis auf die Standardausgabe. Ein produktiver Collector kann dieselbe Hülle an einen OTLP-Endpunkt, eine Warteschlange oder eine Datenbank weiterleiten.

```python
from __future__ import annotations

import json
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4


def emit(operation: str, trace_id: str, started: float, outcome: str) -> None:
    event = {
        "schema_version": "agent-trace/v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "trace_id": trace_id,
        "span_id": f"sp_{uuid4().hex}",
        "operation": operation,
        "outcome": outcome,
        "duration_ms": round((perf_counter() - started) * 1000, 2),
        "attributes": {"environment": "development"},
    }
    print(json.dumps(event, separators=(",", ":"), sort_keys=True))


def main() -> None:
    trace_id = f"tr_{uuid4().hex}"
    started = perf_counter()
    try:
        # Replace with a bounded model or tool invocation.
        result = "validated"
        emit("agent.generate_summary", trace_id, started, "ok")
        print(result)
    except Exception:
        emit("agent.generate_summary", trace_id, started, "error")
        raise


if __name__ == "__main__":
    main()
```

## Dashboard-Ansichten, die Entscheidungen steuern {#dashboard-views-that-drive-decisions}

| Ansicht | Leitfrage | Benötigte Daten |
|---|---|---|
| Run-Liste | Welche Arbeit hängt, ist fehlgeschlagen oder wartet auf Freigabe? | Endzustand, Verantwortlicher, Alter, Anzahl Wiederholungen |
| Trace-Baum | Wo sind Zeit oder Berechtigung gewandert? | übergeordnete/untergeordnete Spans, Dauer, Handoffs |
| Werkzeug-Journal | Welche Fähigkeit hat einen Fehler oder einen Kostensprung verursacht? | Werkzeugrichtlinie, Werkzeugergebnis, Referenz auf Argumente |
| Validator-Warteschlange | Welche Kandidaten sind sicher zu veröffentlichen? | Version der Kriterien, Urteil, Nachweisreferenz |
| Budget-Ansicht | Welcher Workflow überschreitet sein Kontingent? | Modell-/Werkzeugeinheiten, Kostenzuordnung, Parallelität |
| Vorfallsansicht | Kann dieser Lauf wiederholt oder abgeglichen werden? | Idempotenzschlüssel, externer Beleg, Fehlerkategorie |

Vermeiden Sie Schaudiagramme. Ein Token-Diagramm ohne Workflow-Identität kann einem Operator nicht sagen, welche Nutzeraufgabe oder welche Produktionsänderung es darstellt.

## Pipeline-Design {#pipeline-design}

```text
application / workflow controller
        |
        v
structured trace emitter
        |
        v
collector with schema validation and redaction
        |
        +--> durable event store
        |
        +--> OpenTelemetry-compatible backend
        |
        v
operator dashboard and alerts
```

Der Collector ist eine Vertrauensgrenze. Er validiert die Struktur der Ereignisse, vergibt die Erfassungszeit, wendet Sampling und Redaktion an und weist fehlerhafte Nutzlasten zurück. Instrumentieren Sie an Ihren eigenen Workflow- und Werkzeuggrenzen, statt anzunehmen, dass ein Drittanbieter-Client jedes Ereignis erzeugt, das Ihr Betriebsteam benötigt.

Das OpenAI Agents SDK bietet integriertes Tracing mit Spans für Trace, Agent, Turn, Generation, Funktion, Guardrail und Handoff. Ein Adapter kann diese Spans mit Ihren Referenzen auf Arbeitselemente und Nachweise anreichern, statt deren Trace-Hierarchie zu ersetzen. [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-js/guides/tracing/)

## Sampling, Aufbewahrung und Datenschutz {#sampling-retention-and-privacy}

| Datenklasse | Standardrichtlinie | Eskalation |
|---|---|---|
| Kennungen und Zeitangaben | Für das operative Zeitfenster aufbewahren | Nach Ablauf des Fensters aggregieren |
| Prompt-/Ausgabetext | Standardmäßig nicht speichern | Opt-in, redigiert, zugriffsgeschützte Erfassung |
| Werkzeugargumente/-ergebnisse | Referenzen oder allowlist-Felder speichern | Vollständige Erfassung nur für genehmigtes Debugging |
| Fehlernutzlasten | Vor der Speicherung redigieren | Zeitlich begrenzter, gesicherter Vorfallsdatensatz |

Legen Sie die Aufbewahrung nach Zweck fest. Debug-Wiederholung, Produktanalytik, Kostenzuordnung und Audit-Nachweise haben unterschiedliche Zugriffs- und Löschanforderungen. Prüfen Sie das tatsächliche Speicherverhalten des Tracing-Backends, das Sie einsetzen; Aussagen der Dashboard-Oberfläche sind keine Richtlinie zur Datenaufbewahrung.

## Alarmbedingungen {#alert-conditions}

Alarmieren Sie bei Zustandsübergängen, die ein Handeln erfordern, nicht bei reiner Ereignismenge:

- ein Lauf überschreitet seine Frist oder sein Budget;
- ein Werkzeug mit Nebenwirkungen hat ein unbekanntes Ergebnis;
- die Validator-Fehlerrate ändert sich nach einer Freigabe von Agent oder Konfiguration;
- eine Freigabe-Warteschlange überschreitet ihr Altersziel;
- ein Collector weist Ereignisse zurück oder verliert die Bestätigung des dauerhaften Speichers.

Jeder Alarm sollte auf eine Trace-ID, einen Verantwortlichen, eine Nachweisreferenz und eine Runbook-Aktion verweisen.

## Fallstricke {#gotchas}

- **Problem: Rohe Prompts und Werkzeugergebnisse werden standardmäßig protokolliert.** Die Telemetrie wird zu einem zusätzlichen Datenleck und einem teuren Wiederholungsspeicher. **Lösung:** Protokollieren Sie Referenzen, Hashes und allowlist-Metadaten; vollständige Nutzlasten nur unter einer dokumentierten, zugriffsgeschützten Richtlinie erfassen.
- **Problem: Wiederverwendung einer Span-ID über Wiederholungen hinweg.** Das Dashboard kann einen neuen Versuch nicht vom ursprünglichen, unsicheren Aufruf unterscheiden. **Lösung:** Behalten Sie Trace- und Arbeitselement-Identität bei, erzeugen Sie aber für jede Wiederholung einen neuen Span und eine neue Versuchsnummer.
- **Problem: Die Ereignisse eines Client-Bibliothek werden als vollständiger Systemtrace behandelt.** Freigaben, Warteschlangen und externe Belege finden oft außerhalb des SDK statt. **Lösung:** Instrumentieren Sie die Grenzen des Workflow-Controllers und korrelieren Sie Anbieter-Spans mit der dauerhaften Run-ID.
- **Problem: Alarmierung allein anhand der Token-Anzahl.** Hohe Mengen können legitim sein; ein stiller Timeout bei Nebenwirkungen ist dringender. **Lösung:** Alarmieren Sie bei verletzter Richtlinie, verletztem Zustand oder verletzten Service-Level-Zielen.

## Siehe auch {#see-also}

- [[llmops]]
- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]

## Quellen {#sources}

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-js/guides/tracing/)
- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
