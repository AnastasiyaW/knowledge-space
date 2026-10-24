---
title: "Agent-Architekturen"
description: "Eine begrenzte Kontrollflussarchitektur für LLM-Agenten wählen: Zustand, Werkzeuge, Übergaben, Protokolle und Nachweise"
level: 3
source_sha256: 10a2ee8095fa5c4cc714b2472281890d36f6998a671e438d5b38f11c367ba0c7
translation: machine
translated_at: '2026-10-24'
---
# Agent-Architekturen (September 2026) {#agent-architectures-september-2026}

Versionskontext: geprüft anhand der MCP-Spezifikation `latest`, der A2A-Spezifikation und der Dokumentation des OpenAI Agents SDK. Protokollrevisionen und SDK-Releases sind Abhängigkeiten; die genaue Revision, die in einem produktiven System verwendet wird, ist zu dokumentieren.

Eine Agent-Architektur ist die deterministische Kontrollebene um probabilistische Modellaufrufe. Die Architektur verantwortet Berechtigungen, Zustandsübergänge, Wiederholungsgrenzen, dauerhafte Arbeitsvorgänge und Nachweise. Das Modell schlägt vor; die Kontrollebene entscheidet, was als Nächstes geschehen darf.

## Die kleinste ausreichende Form wählen {#choose-the-smallest-sufficient-shape}

| Form | Einsatz, wenn | Erforderliche Kontrollen |
|---|---|---|
| Einzelne begrenzte Aktion | Eine Anfrage, keine Seiteneffekte oder eine reversible Werkzeugaktion | Eingabevalidierung, Timeout, Ausgabevalidierung |
| Expliziter Zustandsautomat | Eine Aufgabe hat Phasen, Wiederholungen, Freigaben oder Wiederherstellung | Übergangstabelle, Budget, Idempotenz, Endzustände |
| DAG | Unabhängige Aufgaben können parallel laufen und haben explizite Zusammenführungen | Abhängigkeitsgraph, Join-Semantik, Nachweise pro Knoten |
| Spezialisierte Übergabe | Eine andere Autorität oder Domäne ist für eine Aufgabe zuständig | Typisierter Übergabevertrag, Autorisierung, Filter für den Verlauf |
| Grenze zu einem Remote-Agenten | Ein unabhängiger Dienst verantwortet die Ausführung | Protokoll, Authentifizierung, Aufgabenlebenszyklus, Artefaktvertrag |

Mit einem Multi-Agenten-Graphen sollte man nicht beginnen. Struktur ist nur dann hinzuzufügen, wenn ein einfacherer begrenzter Ablauf den geforderten Zuverlässigkeits-, Berechtigungs- oder Latenzvertrag nicht erfüllen kann.

## Vertrag für Arbeitsvorgänge {#work-item-contract}

Ein dauerhafter Arbeitsvorgang macht Wiederholungen und Wiederherstellung nachvollziehbar.

```json
{
  "task_id": "task_01J...",
  "state": "planned",
  "attempt": 0,
  "attempt_limit": 3,
  "idempotency_key": "sha256:...",
  "input_ref": "artifact://request/...",
  "policy_revision": "agent-policy-v4",
  "trace_ref": "trace_...",
  "terminal_receipt": null
}
```

Jeder Übergang hat genau einen Verantwortlichen und einen Grund. Unbekannte Zustände führen zu einem Fehlerabbruch im sicheren Zustand (fail closed).

## Minimaler Zustandsautomat {#minimal-state-machine}

```python
from dataclasses import dataclass, replace
from typing import Literal

State = Literal["planned", "running", "verified", "failed", "cancelled"]
ALLOWED: dict[State, set[State]] = {
    "planned": {"running", "cancelled"},
    "running": {"verified", "failed", "cancelled"},
    "verified": set(),
    "failed": set(),
    "cancelled": set(),
}


@dataclass(frozen=True)
class WorkItem:
    task_id: str
    state: State
    attempt: int
    attempt_limit: int


def transition(item: WorkItem, target: State) -> WorkItem:
    if target not in ALLOWED[item.state]:
        raise ValueError(f"invalid transition: {item.state} -> {target}")
    if target == "running" and item.attempt >= item.attempt_limit:
        raise RuntimeError("attempt budget exhausted")
    return replace(
        item,
        state=target,
        attempt=item.attempt + (target == "running"),
    )
```

Werkzeugaufrufe finden nur im Zustand `running` statt, nachdem Autorisierung und Schemavalidierung erfolgt sind. `verified` erfordert einen unabhängig prüfbaren Nachweis und nicht die Aussage des Modells, dass die Arbeit abgeschlossen wurde.

## Speicher und Kontext {#memory-and-context}

Vier Dinge sind getrennt zu behandeln:

- **Laufzustand:** der dauerhafte Arbeitsvorgang und die Übergangsnachweise.
- **Gesprächskontext:** die minimale Eingabe, die für den nächsten Modellzug nötig ist.
- **Langzeitspeicher:** abgegrenzte, versionierte Einträge mit Verantwortlichkeit und Aufbewahrungsregeln.
- **Wissenskorpus:** Quelldokumente, die mit Herkunftsnachweis abgerufen werden.

Eine Zusammenfassung im Prompt kann einen dauerhaften Zustandseintrag nicht ersetzen. Umgekehrt sollte das Modell nicht standardmäßig alle dauerhaften Einträge erhalten; stattdessen ist eine Projektion mit minimalen Rechten abzurufen.

## Werkzeuggrenze {#tool-boundary}

Jedes Werkzeug benötigt ein typisiertes Eingabeschema, einen Akteur- und Mandantenbezug, eine Autorisierungsrichtlinie, ein Timeout, eine Idempotenzregel, eine Klassifizierung der Seiteneffekte und einen Ausgabenachweis.

```text
model proposal -> schema validation -> policy decision -> tool execution
               -> receipt persistence -> verified state transition
```

Reine Lesewerkzeuge und reversible Aktionen können unterschiedlichen Richtlinienpfaden folgen. Destruktive, finanzielle, extern wirksame oder Rechte ändernde Aktionen erfordern eine explizite Freigabegrenze.

## Grenzen der Interoperabilität {#interoperability-boundaries}

MCP und A2A lösen unterschiedliche Probleme:

| Protokoll | Grenze | Kerneinheit | Nicht voraussetzen |
|---|---|---|---|
| MCP | Host-Anwendung zu einem fokussierten Server | Ressourcen, Prompts, Werkzeuge; ausgehandelte Fähigkeiten | Dass ein Werkzeug autorisiert ist, nur weil es angekündigt wird |
| A2A | Unabhängige Agenten-Dienste | Agent Card, Aufgabe, Nachricht, Artefakt | Dass ein Remote-Agent seinen internen Speicher oder seine Werkzeuge offenlegt |

Die Host-Client-Server-Architektur von MCP hält den Geltungsbereich jedes Servers isoliert. Die aktuelle `latest`-Protokollversion ist zustandslos: Jede Anfrage trägt die deklarierte Protokollversion und die Fähigkeiten, und ein Client kann vor weiteren Aufrufen `server/discover` zur Serverermittlung verwenden. A2A stellt einen Aufgabenlebenszyklus für undurchsichtige Remote-Agenten bereit und verwendet eine Agent Card für Erkennung und Anforderungen an die Interaktion.

Ein Protokoll ist nur dort zu verwenden, wo seine Grenze tatsächlich existiert. Ein In-Process-Funktionsaufruf wird nicht dadurch sicherer, dass man ihn in ein Remote-Agenten-Protokoll verpackt.

## Übergaben und Spezialisten {#handoffs-and-specialists}

Eine spezialisierte Übergabe muss enthalten:

1. Identität des Ziels und zulässige Fähigkeit;
2. typisierten Grund und Aufgabenreferenz;
3. eine autorisierte Kontextprojektion statt standardmäßig des vollständigen Verlaufs;
4. Verantwortung für Seiteneffekte und die finale Antwort;
5. Verknüpfung der Traces und einen Endnachweis.

Das OpenAI Agents SDK ist eine aktuelle Implementierung als Beispiel: Es unterstützt Werkzeuge, Guardrails, Übergaben, strukturierte Ausgaben und Tracing. Diese SDK-Funktionen ersetzen weder die anwendungsseitige Autorisierung noch den dauerhaften Workflow-Zustand.

## Observability und Evaluation {#observability-and-evaluation}

Modellaufrufe, Werkzeugaufrufe, Übergaben, Richtlinienentscheidungen, Übergangsnachweise, Fehler sowie geschwärzte Metadaten zu Ein- und Ausgaben sind zu erfassen. Sie sind mit Aufgaben-ID, Trace-ID, Richtlinienrevision und Deployment-Revision zu korrelieren.

Die Architektur ist mit wiederholbaren Szenarien zu evaluieren:

- erlaubter und verweigerter Werkzeugaufruf;
- Wiederholung nach einem transienten Fehler;
- doppelte Anfrage mit demselben Idempotenzschlüssel;
- fehlerhaftes Werkzeugergebnis;
- Übergabe mit überdimensioniertem Verlauf;
- Timeout, Abbruch und Wiederherstellung in einen Endzustand.

## Fallstricke {#gotchas}

- **Eine Schleife ohne Budget ist keine Architektur.** Sie kann eine erfolglose Aktion unbegrenzt wiederholen. **Abhilfe:** Iterations-, Zeit-, Kosten- und Wiederholungsgrenzen im deterministischen Zustand durchsetzen.
- **Eine Übergabe ist eine Autorisierungsgrenze.** Die Weitergabe des vollständigen Gesprächsverlaufs kann Daten offenlegen oder unbeabsichtigte Fähigkeiten gewähren. **Abhilfe:** eine typisierte Projektion mit minimalen Rechten übergeben und den empfangenden Spezialisten autorisieren.
- **Protokoll-Erkennung ist kein Vertrauen.** Ein angekündigtes MCP-Werkzeug oder eine A2A Agent Card erteilt keine Berechtigung zur Nutzung. **Abhilfe:** Erkennung an Identität, explizite Richtlinie und Autorisierung pro Aktion binden.
- **Tracing kann sensible Inhalte enthalten.** Generation- und Werkzeug-Spans können Ein- und Ausgaben aufzeichnen. **Abhilfe:** Schwärzungs- und Aufbewahrungsrichtlinie festlegen, bevor Telemetrie aktiviert wird, und mit repräsentativen Daten testen.

## Quellen {#sources}

- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol latest server primitives](https://modelcontextprotocol.io/specification/latest/server)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI Agents SDK: agents](https://openai.github.io/openai-agents-python/agents/)
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

## Siehe auch {#see-also}

- [[agent-design-patterns]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
