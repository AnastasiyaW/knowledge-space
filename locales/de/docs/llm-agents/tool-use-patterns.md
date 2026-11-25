---
title: "Muster für Tool-Nutzung (September 2026)"
category: patterns
tags: [llm-agents, tool-use, function-calling, mcp, authorization, observability]
level: 3
source_sha256: 87d66ca1145e644bd2212216442356d8530c2684669b660a950be98fc38879d7
translation: machine
translated_at: '2026-10-24'
---
# Muster für Tool-Nutzung (September 2026) {#tool-use-patterns-september-2026}

Geprüft am 2026-09-03. Ein Tool ist eine Anwendungsfähigkeit, die einem Modell über ein Schema zugänglich gemacht wird. Es sollte als API mit Autorisierung, Validierung, Timeouts, Audit-Einträgen und expliziter Fehlersemantik entworfen werden – nicht als zusätzlicher Absatz in einem Prompt.

## Tool-Manifest {#tool-manifest}

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

Jedes Feld oben ist Teil der Anwendungsrichtlinie. Ein Modell kann die deklarierte Fähigkeit anfordern, aber das Gateway entscheidet, ob der Aufruf zulässig ist.

## Entwurfsmuster {#design-patterns}

| Muster | Einsatz, wenn | Erforderliche Schutzmaßnahme |
|---|---|---|
| Schreibgeschützte Suche/Abruf | Das Modell benötigt aktuelle oder proprietäre Informationen | Quellen-Allowlist und Ausgabe von Zitaten/Referenzen |
| Eingeschränkter Schreibzugriff | Das Modell schlägt einen genehmigten Entwurf oder eine Datensatzaktualisierung vor | Genehmigungsstatus, Idempotenz und Audit-Beleg |
| Phasenspezifisches Toolset | Workflow-Stufen benötigen unterschiedliche Fähigkeiten | Der Controller wählt die Phase; das Modell kann sie nicht erweitern |
| Tool-Suche | Ein großer Katalog würde den Kontext belegen | Discovery-Richtlinie und explizite Prüfung der ausgewählten Tools |
| MCP-Integration | Tools werden von einem separaten Server bereitgestellt | Vom Host verwaltete Berechtigungen und Prüfung des Server-Vertrauens |

MCP verwendet eine Host-Client-Server-Architektur, bei der der Host den Lebenszyklus und die Berechtigungen der Clients steuert. [MCP Architecture](https://modelcontextprotocol.io/specification)

## Ergebnis-Envelope {#result-envelope}

Gib einen Envelope zurück, mit dem der nächste Schritt ein Ergebnis von einem Fehler unterscheiden kann, ohne Fließtext parsen zu müssen.

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

Für Tools mit Seiteneffekten sollten zusätzlich zu diesem Envelope eine Caller-/Run-Identität und eine dauerhafte externe Beleg-Referenz enthalten sein.

## Tool-Auswahl {#tool-selection}

Beschreibungen sollten Folgendes angeben:

- das Nutzerergebnis, das das Tool ermöglicht;
- das Eingabeformat und gültige Wertebereiche;
- was zurückgegeben wird;
- wann das Tool nicht verwendet werden sollte;
- ob es liest, schreibt oder eine externe Aktion auslöst.

Anthropic dokumentiert, dass Tool-Definitionen und angesammelte Tool-Ergebnisse Kontext verbrauchen, und empfiehlt, eine Kontextverwaltungsmethode zu wählen, die zur Quelle des Drucks passt. [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)

## Fehler und Wiederherstellung {#failure-and-recovery}

| Fehler | Sicheres Verhalten |
|---|---|
| Unbekanntes Tool | Ohne Ausführung ablehnen |
| Schema-Abweichung | Einen stabilen Validierungsfehler zurückgeben |
| Berechtigung verweigert | Verweigerung zurückgeben; keinen Umgehungsweg vorschlagen |
| Timeout bei Lesezugriff | Als wiederholbar markieren und Wiederholungsbudget begrenzen |
| Timeout bei Schreibzugriff | Ergebnis als unbekannt markieren; Beleg abgleichen, bevor erneut versucht wird |
| Teilweises externes Ergebnis | Beleg/Referenz erhalten und zur Abstimmung zurückhalten |

## Fallstricke {#gotchas}

- **Problem: Jedem Agenten werden alle Tools gegeben.** Mehr Tools erzeugen Unklarheit, Kosten und Angriffsfläche. **Lösung:** Die kleinste aufgabenspezifische Allowlist bereitstellen.
- **Problem: Ein einziges generisches Such- oder Ausführungs-Tool wird verwendet.** Modell und Betreiber können nicht erkennen, welche Richtlinie gilt. **Lösung:** Zweck, Befugnis, Eingaben und Ausgaben explizit machen.
- **Problem: Nach einem Fehler stillschweigend auf eine Alternative ausweichen.** Ein anderes Tool oder ein anderer Anbieter kann die Datenverarbeitung oder Seiteneffekte verändern. **Lösung:** Jede Ausweichlösung mit Auslöser, gleichwertiger Garantie und sichtbarem Signal registrieren.
- **Problem: Einen MCP-Server als grundsätzlich vertrauenswürdig behandeln.** Protokoll-Interoperabilität validiert nicht das Verhalten eines Servers. **Lösung:** Server-Identität, Berechtigungen, Datenfluss und Tool-Schema vor der Bereitstellung prüfen.

## Siehe auch {#see-also}

- [[function-calling]]
- [[agent-security]]
- [[agent-orchestration]]
- [[agent-observability-dashboards]]

## Quellen {#sources}

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification)
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Claude: Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)
- [OpenAI Agents SDK: Tools](https://openai.github.io/openai-agents-js/guides/tools/)
