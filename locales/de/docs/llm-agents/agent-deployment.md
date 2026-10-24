---
title: "Deployment-Muster für Agenten (September 2026)"
category: patterns
tags: [llm-agents, deployment, production, reliability, observability, rollout]
level: 3
source_sha256: 81cecd25e0f4e8ba4a45006267a19abc67811b3d487d502d1bc1c493a3c0b8f9
translation: machine
translated_at: '2026-10-24'
---
# Deployment-Muster für Agenten (September 2026) {#agent-deployment-patterns-september-2026}

Geprüft am 2026-09-03. Deployen Sie einen Agenten als versionierten Anwendungs-Workflow und nicht als einen an einen Modell-Endpunkt angehängten Prompt. Ein Deployment muss seine Modellkonfiguration, Tools, Richtlinien, Zustandsübergänge und Nachweise auch nach Abschluss einer Anfrage nachvollziehbar machen.

## Deployment-Einheit {#deployment-unit}

| Bestandteil | Fixieren und protokollieren | Warum es wichtig ist |
|---|---|---|
| Anwendung | Image oder unveränderlicher Quellstand | Reproduziert das Verhalten von Orchestrierung und Validierung |
| Modell | Anbieter, exakter Modell-/Artefakt-Bezeichner, Decoding-Richtlinie | Verhindert unbeabsichtigte Veränderungen bei Fähigkeiten oder Kosten |
| Prompt/Konfiguration | Versionierte Vorlage und Laufzeitkonfiguration | Macht Ausgabeänderungen nachvollziehbar |
| Tools | Manifest, Berechtigungsbereiche, Timeouts und Genehmigungsrichtlinie | Begrenzt Seiteneffekte |
| Daten | Revision des Retrieval-Korpus und Zugriffsrichtlinie | Legt fest, welche Belege der Agent lesen konnte |
| Evaluation | Testset, Bewertungsraster und Freigabeschwelle | Unterscheidet einen neuen Build von einem verifizierten Build |

Ein Image-Digest allein reicht nicht aus, wenn sich Modell-Aliase, Prompts, Tool-Definitionen oder ein Index unabhängig voneinander ändern können.

## Ausführungspfad wählen {#choose-the-execution-lane}

| Pfad | Verwenden, wenn | Erforderlicher Vertrag |
|---|---|---|
| Synchrone Anfrage | Eine begrenzte Antwort innerhalb der Benutzerinteraktion erwartet wird | Deadline, Abbruch, Antwortschema und sichere Timeout-Meldung |
| Dauerhafter Job | Die Arbeit kann die HTTP-Anfrage überdauern oder mehrere Schritte umfassen | Idempotenzschlüssel, Checkpoint, Wiederholungsbedingung und terminaler Beleg |
| Genehmigungsstopp | Ein Tool kann eine wesentliche externe Nebenwirkung auslösen | Benannter Genehmiger, unveränderliche vorgeschlagene Aktion, Ablauf und nachvollziehbare Entscheidung |
| Geplanter Batch | Eingaben sind bekannt und die Verarbeitung darf verzögert werden | Manifest, Deduplizierungsschlüssel, Zustand pro Element und Abschlussbuchhaltung |

Legen Sie langlaufende Arbeit nicht allein deshalb hinter einen Request-Handler, weil der erste Modellaufruf schnell ist. Persistieren Sie den Zustand, bevor Sie eine wiederholbare Aktion auslösen.

## Ein kleines dauerhaftes Arbeitselement {#a-small-durable-work-item}

```json
{
  "work_id": "news-2026-09-03-0042",
  "input_revision": "sha256:...",
  "agent_release": "2026-09-03.2",
  "state": "AWAITING_APPROVAL",
  "idempotency_key": "publish:news-2026-09-03-0042",
  "tool_manifest_revision": "tools-19",
  "checkpoint": "extract-complete",
  "evidence": ["source-17", "evaluation-run-82"]
}
```

`state` wird von der Anwendung verwaltet. Ein Modell darf einen nächsten Schritt vorschlagen, aber es darf nicht direkt `SUCCEEDED` setzen, sich selbst genehmigen oder den Prüfprotokolleintrag löschen.

## Fehler- und Wiederholungsrichtlinie {#failure-and-retry-policy}

Behandeln Sie jede Fehlerklasse unterschiedlich:

1. **Ungültige Eingabe oder Richtlinienablehnung:** Terminal mit einem für Benutzer verständlichen Grund ablehnen; unveränderte Eingabe nicht erneut senden.
2. **Vorübergehender Fehler bei Anbieter oder Netzwerk:** Nur eine idempotente Operation innerhalb eines begrenzten Budgets wiederholen und den Versuchsprotokolleintrag aufbewahren.
3. **Mehrdeutiger Seiteneffekt im Tool:** Vor jeder Wiederholung mit dem Idempotenzschlüssel oder dem Beleg des Anbieters abgleichen.
4. **Ungültige Modellausgabe:** Einen deterministischen Reparatur- bzw. Validierungspfad ausführen oder einen typisierten Fehler zurückgeben; sie nicht stillschweigend als Erfolg uminterpretieren.
5. **Prozessunterbrechung:** Vom letzten verifizierten Checkpoint aus fortsetzen, nicht aus einem abgeleiteten Gesprächsverlauf.

## Observability als Freigabeanforderung {#observability-as-a-release-requirement}

Ein einziger Trace sollte einem Operator ermöglichen zu beantworten: welches Release lief, welche Eingabe- bzw. Datenrevision es sah, welche Tools es angefordert hat, welche Aktionen abgelehnt oder genehmigt wurden, welche Wiederholungen auftraten und wie der Workflow seinen terminalen Zustand erreicht hat. Erfassen Sie undurchsichtige Kennungen oder geschwärzte Attribute statt Rohdaten mit Geheimnissen und personenbezogenen Daten.

Die semantischen Konventionen für GenAI bieten ein gemeinsames Vokabular für Modell-Spans; sie ergänzen, ersetzen aber nicht die geschäftlichen Ereignisse zu Arbeitselementen und Genehmigungen. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Rollout-Vertrag {#rollout-contract}

```text
candidate release
    -> deterministic and adversarial evaluation set
    -> isolated canary with trace + receipt inspection
    -> bounded rollout with rollback target
    -> production observation against explicit SLOs
```

Rollen Sie die vollständige Deployment-Einheit zurück. Wird nur ein Modell zurückgesetzt, während eine geänderte Tool-Richtlinie oder Index-Revision bestehen bleibt, lässt sich der Vorfall nicht mehr rekonstruieren.

## Stolpersteine {#gotchas}

- **Problem: Einen asynchronen Agenten-Endpunkt als „zustandslos“ bezeichnen.** Die Browserverbindung ist zustandslos; die Arbeit ist es nicht. **Lösung:** Speichern Sie ein Arbeitselement und einen Checkpoint, bevor eine Aktion ausgeführt wird, die wiederholt oder fortgesetzt werden kann.
- **Problem: Ein Tool mit Seiteneffekten nach einem Timeout erneut ausführen.** Die ursprüngliche Anfrage kann auf dem Remote-System erfolgreich gewesen sein. **Lösung:** Vor einer Wiederholung einen Beleg des Anbieters oder einen Idempotenzschlüssel verlangen.
- **Problem: Einen LLM-Trace als Audit-Log behandeln.** Traces können Richtlinienentscheidungen auslassen und dürfen sensible Nutzdaten nicht ungeprüft speichern. **Lösung:** Separate strukturierte Ereignisse für Autorisierung, Genehmigung und terminales Ergebnis ausgeben.
- **Problem: Einen Modell-Alias ohne Evaluation vorrücken lassen.** Eine Verschiebung des Alias kann Ausgabeform und Tool-Verhalten verändern. **Lösung:** Den Release-Bezeichner festschreiben und den Release-Korpus vor der Freigabe erneut ausführen.

## Siehe auch {#see-also}

- [[production-patterns]]
- [[agent-observability-dashboards]]
- [[tool-use-patterns]]
- [[agent-evaluation]]

## Quellen {#sources}

- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
