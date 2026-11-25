---
title: "Adaptive Lernsysteme mit LLMs"
description: "Eine begrenzte Architektur für Lernendenzustand, deterministische Terminplanung, Inhaltserstellung, Bewertung und Datenschutz"
level: 3
source_sha256: 762ce577fe2100b38d73409bfef469b34aeb3d76e9eb86753b083c7a64b024f3
translation: machine
translated_at: '2026-10-24'
---
# Adaptive Lernsysteme mit LLMs (September 2026) {#adaptive-learning-systems-with-llms-september-2026}

Versionskontext: Lernendenmodelle, Curricula und Terminplanungsalgorithmen sind fachliche Richtlinien. Behandeln Sie ihre Versionen, Kalibrierungsdaten und Datenschutzregeln als deploybare Artefakte; betten Sie sie nicht nur in einen LLM-Prompt ein.

Ein LLM kann Erklärungen und Übungsaufgaben erzeugen, sollte aber nicht die Quelle der Wahrheit für Voraussetzungsgraphen, Lernendenakten, Wiederholungsplanung oder hochrelevante Leistungsbewertungen sein.

## Vier begrenzte Schichten {#four-bounded-layers}

```text
Curriculum model  -> concepts, prerequisites, approved objectives
Learner model     -> evidence-backed estimates and review history
Scheduler         -> deterministic next-review and workload policy
Generation layer  -> explanations, examples, feedback, and exercise candidates
```

Durch diese Abgrenzung wird ein System testbar: Curriculum und Terminplanung lassen sich ohne Modellaufruf wiederholen, während die Erzeugung gegen einen bekannten Lernendenzustand evaluiert werden kann.

## Vertrag für Lernereignisse {#learner-event-contract}

Speichern Sie beobachtete Interaktionen, keine unbegründeten Aussagen wie `the learner understands algebra`.

```json
{
  "event_id": "evt_01J...",
  "learner_id": "pseudonymous-id",
  "concept_id": "fractions.addition",
  "activity_revision": "fractions-v5",
  "submitted_at": "2026-09-03T18:00:00Z",
  "result": "incorrect",
  "attempt_count": 2,
  "evidence_ref": "encrypted://assessment/...",
  "consent_policy": "education-data-v2"
}
```

Eine Aktualisierung des Lernendenzustands ist eine versionierte Transformation von Ereignissen. Erfassen Sie deren Modell- bzw. Regelrevision, Konfidenz, Zeitstempel und den Bereich der Quellereignisse.

## Terminplanung außerhalb des LLM {#scheduling-outside-the-llm}

Der Scheduler bestimmt, wann ein Element fällig ist. Anki dokumentiert FSRS als eigenständigen Planungsalgorithmus, der die Abrufwahrscheinlichkeit schätzt und eine Einstellung für die gewünschte Behaltensrate verwendet. Das ist ein gutes Beispiel dafür, warum Terminplanung deterministisch und unabhängig prüfbar sein muss.

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReviewDecision:
    concept_id: str
    due_at: datetime
    scheduler_revision: str
    reason: str


def next_activity(decision: ReviewDecision) -> dict[str, str]:
    return {
        "concept_id": decision.concept_id,
        "scheduler_revision": decision.scheduler_revision,
        "reason": decision.reason,
    }
```

Das LLM darf diese ausgewählte Aktivität zusammen mit dem Kontext des Lernenden mit minimalen Rechten erhalten. Es darf kein anderes Fälligkeitsdatum wählen und den Beherrschungsstatus nicht stillschweigend umschreiben.

## Vertrag für die Inhaltserzeugung {#generation-contract}

Nutzen Sie das Modell, um Inhalte vorzuschlagen, die anschließend gegen Curriculum-Vorgaben validiert werden:

| Eingabe | Validator |
|---|---|
| Konzept und Menge der Voraussetzungen | Curriculum-Dienst |
| Schwierigkeitsband | Kalibrierte Richtlinie |
| Aufgabenformat | Schema-Validator |
| Sachliches Quellmaterial | Validator für Retrieval und Zitierung |
| Für Lernende sichtbares Feedback | Richtlinie für Sicherheit und Tonalität |
| Lösungsschlüssel | Deterministischer Prüfer oder geprüfte Bewertungsmatrix |

Kennzeichnen Sie offenes Feedback als Unterstützung. Stellen Sie erzeugtes Feedback nicht als verifizierte Note dar, sofern eine Bewertungsrichtlinie dies nicht ausdrücklich erlaubt.

## Knowledge Tracing {#knowledge-tracing}

Knowledge Tracing sagt künftige Leistung anhand von Interaktionsabfolgen voraus. Es handelt sich um einen Schätzer, nicht um eine Tatsache über einen Lernenden.

Beginnen Sie mit einer transparenten Baseline und messen Sie die Kalibrierung auf zurückgehaltenen Lernverläufen. Verwenden Sie ein Forschungstoolkit wie pyKT erst, nachdem geprüft wurde, dass seine Datenrepräsentation, Aufteilungsstrategie und Lizenz zum Produkt passen. Die Wahl der Implementierung muss durch eine gemessene Verbesserung gegenüber der Baseline begründet sein.

## Kontext und Datenschutz {#context-and-privacy}

Der Modellkontext sollte nur das enthalten, was für die aktuelle Aktivität benötigt wird:

- aktuelle autorisierte Kennungen von Lernenden und Curriculum;
- ausgewähltes Konzept, Lernziel und Schwierigkeitsrichtlinie;
- zusammenfassendes Feedback aus jüngerer Zeit, soweit es für die Aktivität relevant ist;
- freigegebenes Quellmaterial und Bewertungsvorgaben.

Halten Sie Rohverläufe, personenbezogene Daten und unbezogene Unterhaltungen aus dem Prompt heraus. Legen Sie Aufbewahrungs-, Lösch-, Zugriffsprüfungs- und Exportrichtlinien fest, bevor Sie Lernereignisse erheben.

## Evaluationsschranke {#evaluation-gate}

Evaluieren Sie das gesamte System, nicht nur den erzeugten Text:

1. Die Traversierung des Curriculums beachtet die Voraussetzungen.
2. Der Scheduler liefert für dieselbe Ereignisfolge reproduzierbare Ergebnisse.
3. Schätzungen des Lernendenzustands sind auf zurückgehaltenen Verläufen kalibriert.
4. Erzeugte Übungsaufgaben entsprechen dem Lernziel und dem Antwortschema.
5. Feedback legt keine geschützten Daten offen und enthält keine unbegründeten Aussagen.
6. Arbeitsaufwand und Lernergebnisse werden mit einem genehmigten Studiendesign überwacht.

## Fallstricke {#gotchas}

- **Erzeugter Tutoring-Text ist kein Lernendenmodell.** Eine selbstsicher formulierte Erklärung kann das Kompetenzniveau falsch einschätzen. **Abhilfe:** Leiten Sie den Lernendenzustand aus versionierten Ereignistransformationen ab und machen Sie Konfidenz bzw. Unsicherheit sichtbar.
- **Terminplanung im Prompt ist nicht reproduzierbar.** Derselbe Verlauf kann unterschiedliche Wiederholungsempfehlungen liefern. **Abhilfe:** Führen Sie die Terminplanung als deterministischen Code aus und übergeben Sie die gewählte Aktivität an das Modell.
- **Zukünftige Daten, die in die Evaluation einfließen, machen sie ungültig.** Wird chronologisch geordnete Interaktionsdaten zufällig aufgeteilt, kann spätere Leistung die Antwort verraten. **Abhilfe:** Teilen Sie nach Lernenden und zeitlicher Grenze auf, bevor Sie anpassen oder abstimmen.
- **Bildungsdaten sind sensibel.** Umfangreiche Gesprächsprotokolle können Identität, Behinderung oder Leistungsinformationen enthalten. **Abhilfe:** Minimieren Sie den Prompt-Kontext und setzen Sie explizite Aufbewahrungs- und Zugriffsrichtlinien durch.

## Quellen {#sources}

- [Anki-Handbuch: FSRS](https://docs.ankiweb.net/deck-options.html#fsrs)
- [FSRS-for-Anki-Projekt](https://github.com/open-spaced-repetition/fsrs4anki)
- [pyKT-Toolkit für Knowledge Tracing](https://github.com/pykt-team/pykt-toolkit)

## Siehe auch {#see-also}

- [[agent-memory]]
- [[rag-pipeline]]
- [[embeddings]]
- [[agent-evaluation]]
