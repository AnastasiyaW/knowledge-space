---
title: "Function Calling und Tool Use (September 2026)"
category: techniques
tags: [llm-agents, function-calling, tool-use, schemas, validation]
level: 3
source_sha256: 7d465263558d2aca1d81f099c204b716d7c94c89935b831942cfe48f49f9849b
translation: machine
translated_at: '2026-10-24'
---
# Function Calling und Tool Use (September 2026) {#function-calling-and-tool-use-september-2026}

Geprüft am 2026-09-03. Function Calling ist ein Vertrag: Ein Modell gibt eine strukturierte Anfrage aus, die Anwendung validiert und führt sie aus, und das Ergebnis geht zurück an das Modell oder den Workflow. Allein dadurch, dass ein Modell eine Funktion benennt, erhält es keine Befugnis, eine Aktion auszuführen.

## Der Vertrag {#the-contract}

```text
user request
    -> model selects a declared tool
    -> application validates name, schema, policy, and approval
    -> application executes or rejects the call
    -> structured result becomes the next model/workflow input
```

| Feld | Anforderung |
|---|---|
| Tool-Name | Stabil, eindeutig und auf einer Allowlist geführt |
| Argumente | Typisiertes Schema mit Einschränkungen und Beispielen, wo Mehrdeutigkeit eine Rolle spielt |
| Aufrufer | Run-ID, Agent-Version und Identität der Tool-Policy |
| Deadline | Begrenzte Ausführungszeit und Verhalten bei Abbruch |
| Ergebnis | Strukturierte Erfolgs- oder Fehlerhülle |
| Seiteneffekt | Explizite Freigabe und Idempotency-Key, sofern wesentlich |

Dieselbe, von der Anwendung kontrollierte Schleife findet sich bei allen Provider-APIs. Claude dokumentiert clientseitige Tool-Aufrufe als Modellanfrage, gefolgt von der Ausführung durch die Anwendung und einem Tool-Ergebnis; Gemini beschreibt dieselbe Verantwortung für die Ausführung von Funktionen. [Claude tool-use contract](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Ein minimaler sicherer Dispatcher {#a-minimal-safe-dispatcher}

Dieses Python-3.11+-Beispiel hält Validierung und Befugnisprüfung außerhalb der Modellantwort.

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

In der Produktion ersetzt man das Beispielergebnis durch einen begrenzten Service-Aufruf und ergänzt Authentifizierung, Audit-Logging, Idempotenz und domänenspezifische Schemavalidierung.

## Regeln für Tool-Definitionen {#tool-definition-rules}

| Regel | Begründung |
|---|---|
| Beschreiben, wann ein Tool zu verwenden ist und wann nicht | Verhindert, dass überlappende Beschreibungen zu willkürlicher Auswahl führen |
| Schemas eng halten | Macht Validierung, Policy und Review praktikabel |
| Maschinenlesbare Fehler zurückgeben | Ermöglicht dem Modell die Wiederherstellung ohne Prosa-Parsing |
| Lese- und Schreib-Tools trennen | Erlaubt unterschiedliche Autorisierungsrichtlinien |
| Tool-Zugriff an eine Phase oder Aufgabe binden | Vermeidet die Freigabe ungenutzter Fähigkeiten |
| Breaking-Changes am Schema versionieren | Bestehende Prompts und Clients können auf die alte Form angewiesen sein |

Structured Output verwendet man für eine finale Antwort, die einem Schema entsprechen muss. Function Calling verwendet man, wenn das Modell eine Zwischeninteraktion mit einer von der Anwendung kontrollierten Fähigkeit benötigt. Beide lösen unterschiedliche Stufen eines Workflows.

## Ausführungsrichtlinie {#execution-policy}

```json
{
  "tool_policy_id": "research-readonly-v2",
  "allowed_tools": ["search_sources", "read_document"],
  "requires_approval": ["publish_article", "send_email"],
  "timeout_ms": 15000,
  "idempotency_scope": "run_id:tool_call_id"
}
```

Diese Richtlinie darf nicht allein im System-Prompt ausgedrückt werden. Sie muss im Dispatcher oder Gateway durchgesetzt werden, das die Aktion ausführt.

## Parallele Aufrufe und Wiederholungen {#parallel-calls-and-retries}

Parallele Aufrufe sind nur dann sicher, wenn die Operationen unabhängig voneinander sind und die Reihenfolge der Ergebnisse definiert ist. Ein Retry eines externen Schreibvorgangs muss den Idempotency-Key wiederverwenden und einen unklaren ersten Versuch abgleichen, bevor eine weitere Anfrage gesendet wird.

## Stolperfallen {#gotchas}

- **Problem: Aufruf eines vom Modell gelieferten Tool-Namens ohne Allowlist.** Eine Modellantwort ist nicht vertrauenswürdige Eingabe. **Lösung:** Namen über eine serverseitige Registry auflösen und unbekannte Tools ablehnen.
- **Problem: Schemavalidierung als Autorisierung behandeln.** Gültige Argumente können trotzdem eine unzulässige Aktion anfordern. **Lösung:** Identität, Policy, Freigabe und Budget getrennt von der Argumentform prüfen.
- **Problem: Freitext-Fehlermeldungen zurückgeben.** Der nächste Modellzug kann einen Wiederherstellungspfad erfinden. **Lösung:** Stabile Fehlercodes, Wiederholbarkeit und eine sichere nächste Aktion zurückgeben.
- **Problem: Schreibvorgänge nach einem Timeout wiederholen.** Der ursprüngliche Aufruf könnte erfolgreich gewesen sein. **Lösung:** Einen Idempotency-Key persistieren und zuerst den externen Beleg abfragen.

## Siehe auch {#see-also}

- [[tool-use-patterns]]
- [[agent-orchestration]]
- [[agent-security]]
- [[llm-api-integration]]

## Quellen {#sources}

- [Claude: How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Claude: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Gemini API: Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [OpenAI Agents SDK: Tools](https://openai.github.io/openai-agents-js/guides/tools/)
