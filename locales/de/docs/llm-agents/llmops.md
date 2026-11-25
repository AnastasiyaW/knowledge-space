---
title: "LLMOps"
description: "Sprachmodellsysteme mit versionierten Evaluationen, Release-Gates, nachvollziehbaren Belegen und datensparsamer Telemetrie betreiben."
tags: [llm-agents, llmops, evaluation, observability, governance, cost-optimization]
level: 3
source_sha256: d8b7a97d0456a03381a10b688ed3721496c3b928ecca4c0df6437a791ef247f2
translation: machine
translated_at: '2026-10-24'
---
# LLMOps (September 2026) {#llmops-september-2026}

Versionskontext: Modell-Aliasse, API-Verhalten, Preise, Cache-Regeln, Aufbewahrungskontrollen und Tool-Semantik ändern sich unabhängig voneinander. Behandeln Sie jedes aufgelöste Modell, jeden Prompt, jede Retrieval-Konfiguration, jede Tool-Richtlinie und jeden Evaluationssatz als geprüfte Release-Eingabe und nicht als dauerhafte Dokumentation.

LLMOps ist die betriebliche Disziplin für einen LLM-gestützten Workflow. Ihr Zweck ist nicht, jede Anfrage in einem Dashboard zu sammeln. Ihr Zweck ist es, zu entscheiden, ob eine Änderung eine reale Aufgabe verbessert hat, diese Änderung sicher auszuliefern und ein Ergebnis bei einem Fehler nachvollziehbar zu rekonstruieren oder zurückzurollen.

## Die Änderungseinheit definieren {#define-the-unit-of-change}

Eine Prompt-Änderung kann Sicherheit, Qualität, Latenz und Kosten ebenso stark verändern wie eine Code-Änderung. Legen Sie den vollständigen Kandidaten in ein kleines Release-Manifest:

```json
{
  "release_id": "support-triage-2026-09-03.1",
  "task_contract": "support-triage/v3",
  "model_key": "approved-triage-model",
  "resolved_model_revision": "recorded-at-deploy",
  "prompt_revision": "sha256:...",
  "retrieval_revision": "catalog@17",
  "tool_policy_revision": "tools@9",
  "eval_suite_revision": "triage-evals@12",
  "data_policy_revision": "retention@5",
  "owner": "support-platform"
}
```

Das Manifest beschreibt ein Verhalten, ohne Geheimnisse, vollständige Kundeninhalte oder ein SDK-Objekt des Providers in die Versionskontrolle zu kopieren. Speichern Sie eine geschützte Referenz oder einen Digest, wenn für ein Replay Eingabematerial benötigt wird.

## Release-Lebenszyklus {#release-lifecycle}

| Phase | Frage | Erforderliche Belege | Endergebnis |
|---|---|---|---|
| Aufgabenvertrag | Was muss der Workflow leisten und was niemals tun? | Ein- und Ausgabeschema, Berechtigungsgrenze, Abnahmekriterien | genehmigter oder abgelehnter Umfang |
| Baseline | Was erreicht das aktuelle Release? | eingefrorener, repräsentativer Evaluationssatz und Baseline-Beleg | vergleichbare Referenz |
| Kandidat | Was hat sich geändert? | ein geprüfter Manifest-Diff und Migrationshinweise | auswertbarer Kandidat |
| Offline-Evaluation | Hat es sich verbessert, ohne bekannte Fälle zu brechen? | deterministische Prüfungen, gelabelte Fälle und geprüfte Fehlerstichprobe | bestanden, zurückgehalten oder abgelehnt |
| Staging oder Shadow-Lauf | Arbeitet es unter realistischen Bedingungen sicher? | Trace, Richtlinienprüfungen, Latenz- und Fehlerbelege | bereit oder blockiert |
| Canary | Hält eine begrenzte reale Route den Vertrag ein? | explizite Kohorte, Rollback-Punkt, Endbelege | übernehmen oder zurückrollen |
| Archiv | Kann ein Operator das Ergebnis später erklären? | unveränderliche Release-, Evaluations- und Entscheidungsreferenzen | reproduzierbarer Nachweis |

Befördern Sie einen scheinbar besseren Prompt nicht allein deshalb, weil eine Demo gut aussieht. Eine Release-Entscheidung braucht einen Vergleich mit demselben Aufgabenvertrag und ein Protokoll der Fälle, die weiterhin fehlschlagen.

## Einen Evaluationsvertrag aufbauen {#build-an-evaluation-contract}

Verwenden Sie mehrere Arten von Belegen, weil sie unterschiedliche Fehler erkennen:

| Belegtyp | Geeignet für | Einschränkung |
|---|---|---|
| Deterministische Assertion | Schemata, exakte Labels, Berechtigungen, verbotene Felder | kann nicht jede semantische Antwort beurteilen |
| Gelabelter Referenzsatz | bekannte Aufgabenergebnisse und Regressionen | Abdeckung beschränkt sich auf die ausgewählten Daten |
| Menschliche Prüfung | Nuancen, Nützlichkeit, Interpretation von Richtlinien | erfordert kalibrierte Bewertungsrubrik und Stichprobenziehung |
| Modellbasierter Bewerter | skalierbare Vorauswahl gut definierter Kriterien | ist ein Signal zur Prüfung, keine unbegrenzte Autorität |
| Produktionsbeleg | tatsächlicher Endzustand und für Nutzer sichtbare Fehler | muss datenschutzbewusst und sicher stichprobenartig erhoben sein |

Die Evaluationsleitlinien von OpenAI veranschaulichen Testkriterien wie einen exakten Zeichenkettenvergleich mit einem Referenzlabel. Dieses Muster ist nützlich, wenn die Aufgabe eine objektive Antwort hat; es ersetzt jedoch keine menschliche Prüfung mehrdeutiger oder folgenreicher Ergebnisse. [Working with evals](https://developers.openai.com/api/docs/guides/evals)

Frieren Sie die Testeingaben, die Version des Bewerters und die Abnahmeschwellen ein, bevor Sie Kandidaten vergleichen. Wenn sich ein modellbasierter Bewerter ändert, behandeln Sie das als eigene Kandidatenänderung und kalibrieren Sie ihn an geprüften Beispielen.

## Arbeit verfolgen, ohne ein Datenleck zu erzeugen {#trace-work-without-creating-a-data-leak}

Ein für Nutzer sichtbarer Workflow oder eine dauerhafte Aufgabe sollte genau eine Trace-ID besitzen. Modellaufrufe, Retrieval, Tool-Aufrufe, Freigaben, Validierungen, Wiederholungen und Übergaben werden zu untergeordneten Ereignissen. Geben Sie standardmäßig Referenzen und strukturierte Felder aus, nicht unbeschränkte Prompts oder Tool-Ausgaben.

```json
{
  "schema_version": "llmops-event/v1",
  "trace_id": "tr_01...",
  "release_id": "support-triage-2026-09-03.1",
  "operation": "model.complete",
  "outcome": "completed",
  "duration_ms": 842,
  "usage": {"input": 0, "output": 0},
  "input_ref": "protected:request/...",
  "output_ref": "protected:result/...",
  "tool_policy_revision": "tools@9",
  "attempt": 1
}
```

Ein nützliches Ereignis beantwortet, welches Release lief, welche Berechtigung verwendet wurde, wie es endete und wo die kontrollierten Belege liegen. Das Projekt OpenTelemetry GenAI Semantic Conventions ist eine hilfreiche Referenz für Interoperabilität; anwendungsspezifische Felder sollten weiterhin dokumentiert und mit einem Namensraum versehen bleiben. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Sicherheits- und Berechtigungsprüfungen als Release-Gates einsetzen {#make-safety-and-authorization-release-gates}

Ein Modell oder sein Prompt ist keine Berechtigungsgrenze. Halten Sie Autorisierung, Mandantentrennung, Freigabe von Seiteneffekten und fachliche Invarianten in deterministischem Anwendungscode.

Testen Sie für jeden Kandidaten mindestens:

1. fehlerhafte, fehlende und adversariale Eingaben;
2. Tool-Argumente, die gültiges JSON, aber nicht autorisiert sind;
3. widersprüchliche Anweisungen in abgerufenem oder vom Nutzer kontrolliertem Text;
4. doppelte Zustellung und Timeout-Pfade bei wirksamen Operationen;
5. Schwärzung und Aufbewahrung in Traces und Bewerter-Eingaben;
6. einen bekannt sicheren Rollback auf das vorherige Release-Manifest.

Die aktuellen [OpenAI-Best-Practices für Sicherheit](https://developers.openai.com/api/docs/guides/safety-best-practices) sind ein anbieterspezifischer Ausgangspunkt, kein Ersatz für ein Bedrohungsmodell des eigenen Produkts.

## Kosten als Messgrößen betreiben, nicht als Folklore {#operate-costs-as-measurements-not-folklore}

Erfassen Sie für jedes Release die vom Anbieter gemeldete Nutzung, Cache-Signale, sofern verfügbar, die Modellrevision, Latenz, Anzahl der Wiederholungen, Anzahl der Tool-Aufrufe und das Aufgabenergebnis. Ermitteln Sie den Preis nur aus dem aktuellen Preisplan für genau dieses Modell und diese Verarbeitungsstufe zum Zeitpunkt der Planung oder Abrechnung.

Verwenden Sie ein Budget als Release-Bedingung:

```text
quality and safety SLOs met
    AND measured workload cost is within the approved budget
    AND no unaccounted retry or tool side effect exists
        => candidate may advance
```

Eine niedrigere Token-Anzahl ist nicht automatisch eine Kostenverbesserung, wenn sie mehr Wiederholungen verursacht, Arbeit an ein teures Tool verlagert oder den Aufgabenerfolg senkt.

## Vorfall- und Rollback-Praxis {#incident-and-rollback-practice}

Ein Vorfallsprotokoll sollte Trace, Release-ID, Ein- und Ausgabereferenzen, externe Belege und Befunde des Bewerters verknüpfen. Seine erste Frage ist operativ: Ist eine externe Aktion erfolgt? Seine zweite ist kausal: Welche Release-Eingabe hat das Verhalten verändert?

Rollen Sie zurück, indem Sie ein zuvor geprüftes Manifest wiederherstellen und die aufgelöste Modell- bzw. Konfiguration zur Laufzeit bestätigen. Rollen Sie nicht durch Raten eines historischen Modell-Aliasses, Prompt-Texts oder einer Cache-Konfiguration zurück.

## Stolperfallen {#gotchas}

- **Mittelwerte verbergen schädliche Ausreißer.** Mittlere Latenz oder durchschnittliche Bewertung können eine kleine Klasse katastrophaler Fehler verdecken. **Abhilfe:** Evaluationen und Telemetrie nach Aufgabe, Locale, Tool-Pfad, Mandantenrichtlinie und Endzustand segmentieren.
- **LLM-as-Judge validiert sich nicht selbst.** Ein Bewerter kann driften oder dieselben blinden Flecken wie der Kandidat haben. **Abhilfe:** an von Menschen geprüften Fällen kalibrieren und Abweichungen zur Prüfung aufbewahren.
- **Trace-Nutzdaten können zu einem Schatten-Datenspeicher werden.** Das Protokollieren vollständiger Prompts, abgerufener Dateien oder Tool-Ausgaben schafft Aufbewahrungs- und Zugriffsrisiken. **Abhilfe:** kontrollierte Referenzen ausgeben, früh schwärzen und eine Aufbewahrungsrichtlinie durchsetzen.
- **Ein Canary ohne Rollback-Beleg ist ein Produktionsexperiment.** Eine kleine Kohorte macht einen unbekannten Seiteneffekt nicht umkehrbar. **Abhilfe:** Abbruchbedingung, Idempotenzstrategie und Rollback-Release definieren, bevor Traffic umgeleitet wird.
- **Ein Modell-Alias ist kein Reproduzierbarkeitsnachweis.** Anbieter können Aliasse oder Verfügbarkeit aktualisieren. **Abhilfe:** das aufgelöste Modell bzw. die Konfiguration festhalten, wie sie vom laufenden Release beobachtet wurde.

## Quellen {#sources}

- [OpenAI: Working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI: Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI: Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Siehe auch {#see-also}

- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[llm-api-integration]]
- [[prompt-engineering]]
- [[token-optimization]]
- [[agent-security]]
