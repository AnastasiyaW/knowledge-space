---
title: "Architekturen für Multi-Agent-Systeme (September 2026)"
description: "Produktionsmuster für Routing, Fan-out, Evaluation und dauerhafte Wiederherstellung in Multi-Agent-Systemen; geprüft am 2026-09-03."
level: 3
source_sha256: b7005cf447c53216b8c991e861c08394b23f0d92f90ca874cb8aebd67f41c583
translation: machine
translated_at: '2026-10-24'
---
# Architekturen für Multi-Agent-Systeme (September 2026) {#multi-agent-systems-architectures-september-2026}

Geprüft am 2026-09-03. Ein Multi-Agent-System ist ein Workflow mit mehr als einem modellgesteuerten Worker. Seine Architektur wird durch Autorität, Zustand, Datenfluss und Validierung bestimmt – nicht durch anthropomorphe Berufsbezeichnungen.

## Muster nach Kontrollfluss wählen {#choose-a-pattern-by-control-flow}

| Muster | Controller | Geeignet für | Hauptrisiko |
|---|---|---|---|
| Manager mit Spezialisten als Tools | Manager | Eine finale Antwort, zusammengesetzt aus begrenzten Teilergebnissen | Manager-Prompt wird zu einer nicht testbaren Policy-Engine |
| Explizite Übergabe (Handoff) | Router, danach ausgewählter Spezialist | Ein Spezialist muss die aktive Nutzerinteraktion übernehmen | Unklare Zuständigkeit nach dem Routing |
| Fan-out / Fan-in | Deterministischer Scheduler | Unabhängige Partitionen, Suche oder Prüfdimensionen | Doppelte Arbeit und nicht deterministisches Zusammenführen |
| Generator / Evaluator | Workflow-Controller | Teure Ausgaben mit expliziten Akzeptanzkriterien | Selbstprüfung im selben Kontext |
| Dauerhafter Workflow | State-Machine-Controller | Jobs, die einen Prozess überdauern oder externe Systeme aufrufen | Wiederholung eines Seiteneffekts ohne Abgleich |

Im OpenAI Agents SDK behält der Manager die Kontrolle, wenn ein Agent als Tool verwendet wird; ein Handoff überträgt die aktive Konversation an den ausgewählten Spezialisten. Der Unterschied ist architektonisch, auch wenn beide Varianten Modellaufrufe nutzen. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## Gemeinsamer Arbeitsvertrag {#shared-work-contract}

Jeder Worker erhält ein begrenztes Arbeitspaket und liefert genau einen Ergebnis-Envelope. Vermeiden Sie ein gemeinsam genutztes, veränderbares Freitext-Transkript als System of Record.

```json
{
  "work_item_id": "research:chunk-07",
  "run_id": "run_01J...",
  "parent_run_id": "run_01J-parent",
  "objective": "extract claims from this source set",
  "input_refs": ["source:42", "source:43"],
  "allowed_tools": ["fetch_source", "quote_locator"],
  "deadline_at": "2026-09-03T16:00:00Z",
  "output_schema": "claim-set/v1",
  "idempotency_key": "research:chunk-07:v1"
}
```

Das Ergebnis muss einen terminalen Status, Quell- und Evidenzverweise sowie eine Fehlerkategorie enthalten. Ein Synthesizer sollte standardmäßig validierte Ergebnis-Envelopes erhalten, nicht rohe Worker-Traces.

## Deterministisches Fan-out / Fan-in {#deterministic-fan-out-fan-in}

Verwenden Sie Fan-out nur, wenn jede Partition unabhängig ist und die Zusammenführungsregel deterministisch ist. Dieses Python-3.11+-Beispiel ist providerunabhängig; ersetzen Sie den Worker-Körper durch einen Modellaufruf, der das deklarierte Ergebnisschema zurückgibt.

```python
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(frozen=True)
class Result:
    item_id: str
    status: str
    value: str


async def run_partition(item_id: str) -> Result:
    # Replace with a bounded model/tool invocation.
    await asyncio.sleep(0)
    return Result(item_id=item_id, status="passed", value=item_id.upper())


async def run_all(
    item_ids: list[str],
    worker: Callable[[str], Awaitable[Result]],
    concurrency: int = 4,
) -> list[Result]:
    semaphore = asyncio.Semaphore(concurrency)

    async def guarded(item_id: str) -> Result:
        async with semaphore:
            return await worker(item_id)

    results = await asyncio.gather(*(guarded(item_id) for item_id in item_ids))
    failures = [result for result in results if result.status != "passed"]
    if failures:
        raise RuntimeError(f"partition failures: {[item.item_id for item in failures]}")
    return sorted(results, key=lambda result: result.item_id)


async def main() -> None:
    results = await run_all(["a", "b", "c"], run_partition, concurrency=2)
    print([result.value for result in results])


if __name__ == "__main__":
    asyncio.run(main())
```

Der Reducer muss, bevor die Arbeit beginnt, festlegen, wie er doppelte Aussagen, widersprüchliche Antworten, fehlende Partitionen und Ausfälle des Evaluators behandelt.

## Unabhängige Evaluation {#independent-evaluation}

Verwenden Sie die Aufteilung in Generator und Evaluator, wenn eine Ausgabe eine Qualitäts- oder Sicherheitsentscheidung erfordert, die der Generator nicht selbst bestätigen kann.

| Schritt | Eingabe | Ausgabe | Autorität |
|---|---|---|---|
| Generieren | Arbeitsvertrag und Quellen | Kandidaten-Artefakt | Generator |
| Validieren | Kandidat plus eingefrorene Kriterien | Bestanden/Nicht bestanden-Befunde | Deterministischer Validator |
| Evaluieren | Kandidat, Quellen, Kriterien | Prüfurteil | Unabhängig abgegrenzter Evaluator |
| Entscheiden | Belege von Validator/Evaluator | Veröffentlichen, wiederholen oder zurückhalten | Workflow-Controller |

Der Evaluator sollte die privaten Überlegungen des Generators nicht als Evidenz übernehmen. Geben Sie ihm das Artefakt, die akzeptierten Kriterien und die relevanten Primärquellen. Das verringert korrelierte Fehler, garantiert aber keine Korrektheit.

## Grenze des dauerhaften Workflows {#durable-workflow-boundary}

Persistieren Sie den Zustand vor einem externen Aufruf und gleichen Sie ihn nach einem Timeout ab.

```text
PENDING -> RUNNING -> VALIDATING -> PASSED
                    |               |
                    v               v
                 RETRYABLE        PUBLISHED
                    |
                    v
                 FAILED
```

Regeln für die State Machine:

- Ein Controller, nicht ein Worker, besitzt die terminalen Übergänge.
- Jeder externe Aufruf trägt einen stabilen Idempotency-Key.
- Ein Timeout ist unbekannt, nicht fehlgeschlagen. Fragen Sie den externen Beleg ab, bevor Sie wiederholen.
- Die Veröffentlichung erfordert einen eigenen Freigabezustand, wenn redaktionelle oder rechtliche Prüfung nötig ist.
- Ein Neustart setzt vom letzten persistierten Zustand fort und wiederholt keine abgeschlossenen Seiteneffekte.

## Dienstübergreifende Agenten {#cross-service-agents}

Verwenden Sie ein dienstübergreifendes Protokoll nur, wenn Agenten unabhängig deployed oder unabhängig verantwortet werden. A2A bietet eine Interoperabilitätsgrenze für die Kommunikation zwischen Agenten; MCP bietet eine vom Host verwaltete Grenze für Tools und Kontext. [A2A Protocol](https://a2a-protocol.org/latest/) [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

Für Agenten innerhalb einer Anwendung ist eine typisierte interne API meist einfacher. Führen Sie ein öffentliches Protokoll erst ein, nachdem Regeln für Kompatibilität, Authentifizierung, Discovery, Timeouts und Versionierung definiert sind.

## Rollen sind Dokumentation, keine Architektur {#roles-are-documentation-not-architecture}

Bezeichnungen wie Researcher, Reviewer oder Coordinator sind nur dann nützlich, wenn sie einem unterschiedlichen Vertrag entsprechen:

- **Researcher:** Nur-Lese-Zugriff auf Quellen und zitierfähige Ausgabe.
- **Reviewer:** Keine Schreibbefugnis und ein Bestanden/Nicht-bestanden-Raster.
- **Coordinator:** Besitzt Scheduling, Budgets und Zustandsübergänge.
- **Publisher:** Darf öffentliche Ausgaben nur nach einem Freigabebeleg schreiben.

Wenn zwei Rollen dieselben Tools, Daten, Budgets und denselben Validator haben, führen Sie sie zusammen, bis eine konkrete Trennung nötig wird.

## Fallstricke {#gotchas}

- **Problem: Parallele Worker bearbeiten denselben Datensatz.** Last-Writer-Wins-Korruption kann wie eine erfolgreiche Zusammenführung aussehen. **Lösung:** Unveränderliche Eingaben partitionieren und genau einem Reducer die exklusive Verantwortung für veränderbare Ausgaben geben.
- **Problem: Der Evaluator ist nur der Generator, der sich selbst loben oder kritisieren soll.** Er übernimmt dieselben blinden Flecken und kann auf die eigene Formulierung hin optimieren. **Lösung:** Separaten Kontext, eingefrorene Kriterien und quellenbasierte Prüfungen verwenden.
- **Problem: Eine Übergabe verliert die Zuständigkeit für die finale Antwort.** Der Nutzer sieht eine Antwort, aber das System hat keinen verantwortlichen Eigentümer. **Lösung:** Aktuellen Eigentümer, Routing-Grund und Abschlussregel nach der Übergabe festhalten.
- **Problem: Ein Timeout wird als sauberer Fehler wiederholt.** Die erste Anfrage hat unter Umständen bereits gewirkt. **Lösung:** Vor einem weiteren Aufruf über Idempotency-Key oder Provider-Beleg abgleichen.

## Einschränkungen {#limitations}

Multi-Agent-Systeme erhöhen Kosten, Latenz und operative Angriffsfläche. Parallelität verbessert den Durchsatz nur bei wirklich unabhängiger Arbeit. Ein zusätzlicher Agent kann fehlende Quellenautorität, ein unklares Akzeptanzkriterium oder einen Seiteneffekt ohne Idempotency-Vertrag nicht ausgleichen.

## Siehe auch {#see-also}

- [[agent-architectures]]
- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-messaging]]
- [[multi-session-coordination]]

## Quellen {#sources}

- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
