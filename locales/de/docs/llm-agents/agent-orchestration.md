---
title: "Agent-Orchestrierung"
description: "Modellaufrufe, Tools, Übergaben, Freigaben, Wiederholungen und Nachweise über explizit modellierten Aufgabenzustand koordinieren, statt sich auf eine framework-spezifische Agent-Schleife zu verlassen."
tags: [llm-agents, orchestration, workflows, multi-agent, state-machine, approvals, observability]
level: 3
source_sha256: b4b4897397c6c55fa24fe0f9c734fba9795a491cbbc65117b8b93f0fa99ddb66
translation: machine
translated_at: '2026-10-24'
---
# Agent-Orchestrierung (September 2026) {#agent-orchestration-september-2026}

Versionskontext: Orchestrierungs-Frameworks, SDKs, Protokollversionen, Speicher-Backends und die Semantik von Modell-Tools ändern sich schnell. Entwerfen Sie zuerst den Aufgabenzustand, die Autorisierungsgrenze und die terminalen Nachweise; wählen Sie ein Framework erst aus, wenn diese Verträge geklärt sind.

Agent-Orchestrierung ist die kontrollierte Ausführung einer Aufgabe über Modellaufrufe, deterministischen Code, Tools, Agents, Menschen und dauerhaften Zustand. Sie ist kein Synonym für „mehrere Agents unterhalten sich miteinander“. Der Orchestrator verantwortet den Lebenszyklus der Aufgabe und belegt, ob eine angeforderte Wirkung eingetreten ist.

## Den dauerhaften Aufgabenvertrag definieren {#define-the-durable-task-contract}

```json
{
  "task_id": "publish-research-044",
  "schema_version": "agent-task/v1",
  "objective": "prepare a cited draft for review",
  "input_refs": ["artifact:source-manifest-44"],
  "owner": "editorial-platform",
  "state": "PENDING",
  "tool_policy_revision": "tools@9",
  "approval_policy_revision": "review@4",
  "idempotency_key": "publish-research-044:v1",
  "attempt": 0
}
```

Der Aufgabendatensatz gehört der Anwendung. Er enthält nur Referenzen auf kontrollierte Daten und bleibt über Neustarts von Workern, Verbindungsabbrüche im Browser und Übergaben zwischen Agents hinweg erhalten.

## Zustände und Belege getrennt modellieren {#model-states-and-receipts-separately}

Verwenden Sie nicht-terminale Zustände für laufende Arbeit und sich gegenseitig ausschließende terminale Zustände für das Ergebnis der Aufgabe. Die zulässigen Übergänge müssen eine Freigabeentscheidung, Ablauf und Abbruch umfassen:

```text
PENDING -> RUNNING -> COMPLETED | FAILED
RUNNING -> NEEDS_APPROVAL
NEEDS_APPROVAL + bound approved receipt -> RUNNING
NEEDS_APPROVAL + denied or expired receipt -> CANCELLED
any non-terminal state -> CANCELLED

verification status: PENDING | VERIFIED | REJECTED
```

Jeder Übergang erzeugt einen Beleg. Ein terminaler Beleg enthält die Referenz auf die Ausgabe, das Ergebnis des Validators, gegebenenfalls den Beleg über die externe Wirkung, die Einstufung der Wiederholbarkeit und die Konfigurationsrevisionen. Die Aufgabe wird aus `NEEDS_APPROVAL` nur fortgesetzt, wenn der Freigabebeleg an genau die Aufgabe, die Wirkung, den Digest der Argumente, den Akteur, den Geltungsbereich, das Ablaufdatum und den Idempotency-Key gebunden ist. Der Verifikationsstatus ist eine Prüfung unveränderlicher terminaler Nachweise: `REJECTED` tut nicht so, als wäre eine bereits abgeschlossene externe Wirkung nie eingetreten, und `VERIFIED` autorisiert keine neue Wirkung.

## Deterministische Steuerung von modellbasiertem Urteil trennen {#separate-deterministic-control-from-model-judgment}

Verwenden Sie deterministischen Code für:

- Autorisierung, Mandantengeltungsbereich, Budgets, Ratenbegrenzungen und Datenklassifizierung;
- Schema-Parsing, Geschäftsinvarianten, Idempotenz und Wiederholungen;
- Zustandsübergänge, Timer, Abbruch und Abgleich externer Wirkungen;
- Freigabe-Routing und Audit-Protokolle.

Setzen Sie ein Modell dort ein, wo tatsächlich Interpretation, Planung alternativer Vorgehensweisen, Zusammenfassung oder begrenzte Auswahl nötig ist. Frameworks wie LangGraph unterstützen Workflows, die deterministische und modellgesteuerte Schritte, dauerhafte Ausführung und Prüfpunkte mit menschlicher Beteiligung kombinieren. [LangGraph-Überblick](https://docs.langchain.com/oss/python/langgraph/overview)

## Rollen sind keine Berechtigungen {#roles-are-not-permissions}

Ein Router darf eine geprüfte Konfiguration auswählen. Ein Researcher darf eine Menge von Behauptungen erstellen. Ein Executor darf ein Tool anfordern. Ein Reviewer darf ein Urteil abgeben. Keine dieser Bezeichnungen gewährt Zugriff auf Daten oder externe Wirkungen.

Definieren Sie für jede Rolle:

| Rolle | Darf | Darf nicht allein entscheiden | Erforderlicher Beleg |
|---|---|---|---|
| Router | einen freigegebenen Pfad wählen | Zugriff über den Aufgabenumfang hinaus | Route und Konfigurationsrevision |
| Worker | begrenzte Modell- und Tool-Arbeit ausführen | standardmäßig veröffentlichen oder ausrollen | Ausgabe-, Tool- und terminale Belege |
| Reviewer | explizite Kriterien bewerten | Kandidatenevidenz verändern | Urteil und Verweis auf Befunde |
| Approver | eine definierte Wirkung autorisieren | die Aufgabe stillschweigend umschreiben | Identität, Geltungsbereich und Entscheidung |

So wird verhindert, dass aus einer Übergabe eine Rechteausweitung wird.

## Tools, Übergaben und Protokollgrenzen {#tools-handoffs-and-protocol-boundaries}

Ein Tool-Aufruf eines Modells ruft eine Fähigkeit auf, die dem aktuellen Agent zur Verfügung steht. Eine Übergabe delegiert eine begrenzte Aufgabe an einen anderen Worker oder Spezialisten. Beide benötigen ein Schema, eine Identität, eine Frist und einen dauerhaften Ergebnisbeleg.

MCP beschreibt ein Host-Client-Server-Protokoll für den Austausch von Kontext zwischen Agent und Tool, während A2A die Zusammenarbeit zwischen unabhängigen Agents abdeckt. Keines der beiden Protokolle ersetzt die Autorisierung auf Anwendungsebene oder Aufgabenbelege. [MCP-Architektur](https://modelcontextprotocol.io/specification/latest/architecture) und [A2A Protocol](https://a2a-protocol.org/latest/)

Das OpenAI Agents SDK ist ein aktuelles Beispiel für eine Agent-Laufzeit mit Tools, Übergaben, Guardrails, menschlicher Beteiligung und Tracing. Seine Primitive können einen Entwurf inspirieren, sollten aber nicht zum anbieterneutralen Aufgabenschema werden. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

## Wiederholung, Abbruch und Nebenwirkungen {#retry-cancellation-and-side-effects}

Wiederholen Sie nur eine Aktion, deren Wiederholung nachweislich sicher ist. Erzeugen Sie einen Idempotency-Key, bevor ein wirksamer Tool-Aufruf erfolgt, und erhalten Sie ihn über Warteschlangen-, Agent- und Tool-Grenzen hinweg.

```text
timeout or lost response
  -> reconcile external receipt
  -> retry only if absence of effect is established
  -> otherwise mark for review
```

Ein Abbruch ist ein Zustandsübergang mit einem Abgleichschritt und nicht bloß eine Anforderung, die Textgenerierung zu stoppen. Eine abgebrochene Aufgabe muss angeben, ob ein Tool-Aufruf nicht gestartet, gestoppt oder vor Eintreffen des Abbruchs abgeschlossen wurde.

## Laufzeit anhand des Vertrags auswählen {#select-a-runtime-by-contract}

| Anforderung | Zu forderende Fähigkeit |
|---|---|
| Langlaufende Arbeit | dauerhafter Zustand, Fortsetzung, Timeout und Abgleich |
| Sensible Aktion | Freigabe-Prüfpunkt, Durchsetzung von Richtlinien, Idempotenz |
| Mehrere Spezialisten | typisierte Übergabe, Ergebnisschema, Verantwortlichkeit und Frist |
| Parallele Worker | Queue-Lease, Deduplizierung, Backpressure, Dead-Letter-Pfad |
| Nachvollziehbarkeit | Trace, Belege für Zustandsübergänge, Schwärzung, Version des Evaluators |
| Portabilität | interner Aufgabenvertrag, getrennt von SDK-Objekten des Frameworks |

Eine kleine, von der Anwendung verwaltete Zustandsmaschine reicht oft aus. Ergänzen Sie eine Graph-Laufzeit, ein Agent-SDK oder ein Multi-Agent-Protokoll nur dann, wenn deren Fähigkeit eine gemessene Anforderung erfüllt.

## Stolperfallen {#gotchas}

- **Ein Gesprächsverlauf ist kein Orchestrierungszustand.** Der Chat-Verlauf belegt weder, wem eine Aufgabe gehört, noch ob eine Wirkung abgeschlossen wurde. **Abhilfe:** Aufgabendatensatz und terminale Belege persistieren.
- **Übergaben können Berechtigungen vervielfachen.** Eine delegierte Anweisung kann Tools oder Daten freigeben, die der Sender nicht kontrolliert hat. **Abhilfe:** Der Empfänger und jede Tool-Grenze autorisieren jeweils eigenständig.
- **Wiederholungen können reale Aktionen duplizieren.** Ein Timeout beweist nicht, dass ein API-Aufruf fehlgeschlagen ist. **Abhilfe:** Vor einer Wiederholung anhand des Idempotency-Keys abgleichen.
- **Menschliche Prüfung nach einer Wirkung kommt zu spät.** Ein Reviewer kann eine bereits veröffentlichte oder bezahlte Aktion nicht rückgängig machen. **Abhilfe:** Die Freigabe vor die nicht umkehrbare Grenze legen.
- **Framework-Zustand ist nicht automatisch portabel.** Objektlayouts und Persistenzsemantik von SDKs ändern sich. **Abhilfe:** einen kleinen, von der Anwendung verwalteten Vertrag außerhalb des Frameworks speichern.
- **Durchsatz ist kein Abschluss.** Eine ausgelastete Queue kann fehlgeschlagene Aufgaben ohne terminale Nachweise verbergen. **Abhilfe:** bei fehlenden oder veralteten terminalen Belegen alarmieren.

## Quellen {#sources}

- [LangGraph-Überblick](https://docs.langchain.com/oss/python/langgraph/overview)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Model Context Protocol – Architektur](https://modelcontextprotocol.io/specification/latest/architecture)
- [A2A Protocol](https://a2a-protocol.org/latest/)

## Siehe auch {#see-also}

- [[multi-agent-messaging]]
- [[multi-session-coordination]]
- [[agent-design-patterns]]
- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[agent-security]]
