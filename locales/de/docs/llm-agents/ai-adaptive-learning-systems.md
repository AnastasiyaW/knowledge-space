---
title: "KI-gestützte adaptive Lernsysteme"
description: "Eine versionsbewusste Architektur für Lernnachweise, deterministische Terminplanung, eingeschränktes LLM-Tutoring, Evaluation und Schutzmaßnahmen für Lernerdaten."
tags: [education, adaptive-learning, knowledge-tracing, spaced-repetition, llm-agents, privacy]
level: 3
source_sha256: 753325bd14b886c9d820ecbba34f5e0ab61917fd87834dffd469f500c40dcf78
translation: machine
translated_at: '2026-10-24'
---
# KI-gestützte adaptive Lernsysteme {#ai-powered-adaptive-learning-systems}

**Stand geprüft: 2026-09-03.** Ein adaptives Lernsystem ist ein Entscheidungssystem auf Basis von Lernnachweisen und kein Chatbot, der das Niveau einer lernenden Person errät. Messung, Terminplanung, Inhaltserzeugung und Governance sollten getrennt werden, damit jede Komponente unabhängig evaluiert und korrigiert werden kann.

## Vier getrennte Verantwortlichkeiten {#four-distinct-responsibilities}

| Schicht | Verantwortet | Darf nicht allein entscheiden |
|---|---|---|
| Domänenmodell | Konzepte, Voraussetzungen, Inhaltsanforderungen | Identität der lernenden Person oder Zugriffsrechte |
| Lernnachweise | Antworten, Versuche, Konfidenz, Herkunft | unumkehrbare Fähigkeitsbewertungen |
| Entscheidungsengine | nächste Aktivität, Wiederholungsplan, Eskalationsregel | freie Inhalte und Ausnahmen von Richtlinien |
| Tutor-Oberfläche | Erklärung, Darstellung von Übungen, Feedback | Autorität über Beherrschung oder Speicherung privater Daten |

Ein LLM kann Erklärungen und Übungen adaptiv gestalten. Es sollte jedoch weder zur maßgeblichen Datenbank des Lernzustands noch zum Scheduler oder zur letzten Instanz für die Feststellung von Beherrschung in folgenreichen Situationen werden.

## Lernzustand ausgehend von Nachweisen {#evidence-first-learner-state}

Beobachtbare Nachweise und abgeleitete Schätzungen werden getrennt gespeichert:

```json
{
  "learner_ref": "student:opaque-id",
  "concept_ref": "algebra:linear-equations",
  "evidence": {
    "activity_ref": "exercise-044",
    "response_class": "correct_after_hint",
    "observed_at": "2026-09-03T16:20:00Z"
  },
  "estimate": {
    "mastery": 0.63,
    "confidence": "low",
    "model_revision": "kt-model@2026-09-03"
  },
  "next_review_at": "2026-09-06T09:00:00Z",
  "consent_revision": "learner-data-policy@3"
}
```

Der numerische Schätzwert ist ein Modellergebnis und keine Tatsache über die lernende Person. Er muss anhand späterer Ergebnisse kalibriert, revidierbar und im Umfang erklärbar sein, den der Lernkontext erfordert.

## Knowledge Tracing ist eine gemessene Modellwahl {#knowledge-tracing-is-a-measured-model-choice}

Knowledge Tracing sagt den Lernzustand auf Basis von Interaktionssequenzen voraus. Dafür können einfache probabilistische Modelle, rekurrente oder aufmerksamkeitsbasierte Modelle oder andere Ansätze eingesetzt werden. Keine Modellfamilie ist universell überlegen: Datenmenge, Granularität der Konzepte, Kaltstart, fehlende Werte und Qualität der Prüfungen beeinflussen das Ergebnis.

Das pyKT-Toolkit bietet standardisierte Vorverarbeitung, mehrere Datensätze und Szenarien sowie mehr als zehn Deep-Knowledge-Tracing-Ansätze für vergleichende Experimente. Damit lässt sich eine Baseline etablieren; anschließend sollte auf dem tatsächlichen Curriculum und mit der tatsächlichen Lernendenpopulation evaluiert werden. [pyKT toolkit](https://github.com/pykt-team/pykt-toolkit)

Mindestanforderungen an die Evaluation:

1. Daten nach Lernenden und Zeit aufteilen, um die Verwendung zukünftiger Antworten (Leakage) zu verhindern;
2. mit einer einfachen Baseline vergleichen;
3. Kalibrierung ebenso messen wie Rangfolge oder Treffergenauigkeit;
4. Fehler nach Konzept, Sprache, Barrierefreiheitsbedarf und Lernendenkohorte untersuchen;
5. einen menschlichen Prüfpfad vorsehen, wenn die Schätzung eine folgenreiche Chance beeinflusst.

## Deterministische Planung von Wiederholungen {#deterministic-review-scheduling}

Die Planung von Wiederholungen wird in einem deterministischen Dienst mit versioniertem Algorithmus, Eingabehistorie, gewählten Parametern und reproduzierbarer Ausgabe geführt. Das LLM kann erklären, warum eine Wiederholung sinnvoll ist, oder Übungsmaterial erstellen; es sollte die fällige Aktivität jedoch als Tatsache erhalten und das Fälligkeitsdatum nicht selbst erfinden.

FSRS ist eine offene Familie von Spaced-Repetition-Verfahren, die auf Gedächtniszustandsvariablen und Parameteroptimierung beruht. Implementierungen und Algorithmusversionen entwickeln sich weiter, daher sollten sowohl die genaue Bibliothek mit Version als auch die für eine lernende Person oder ein Kartendeck verwendeten Parameter protokolliert werden. [Open Spaced Repetition](https://github.com/open-spaced-repetition) [SRS benchmark](https://github.com/open-spaced-repetition/srs-benchmark)

```text
assessment event -> learner evidence store -> scheduler / decision rule
                                           -> due activity
                                           -> constrained tutor prompt
                                           -> learner response -> new evidence
```

## LLMs in einer eingeschränkten Rolle einsetzen {#use-llms-in-a-constrained-role}

Ein LLM eignet sich gut dazu,

- mehrere Übungsentwürfe aus einer freigegebenen Konzeptvorlage zu erzeugen;
- einen bekannten Fehler unter Verweis auf eine pädagogische Regel zu erklären;
- Sprache, Darstellungsform oder Beispiele innerhalb eines freigegebenen Schwierigkeitsbands anzupassen;
- einen Fortschrittsbericht zusammenzufassen, den eine berechtigte prüfende Person einsehen darf;
- eine Rückfrage zu stellen, wenn die Nachweise nicht ausreichen.

Es sollte nicht stillschweigend

- geschützte Merkmale ableiten oder einen festen „Lernstil“ zuschreiben;
- eine lernende Person allein auf Grundlage generierten Feedbacks höherstufen;
- Voraussetzungen, Terminplan, Altersregeln oder Richtlinien für Nachteilsausgleich verändern;
- rohe Lernhistorie außerhalb des deklarierten Datenspeichers aufbewahren;
- eine generierte Antwort als richtig markieren, ohne dass eine deterministische oder menschliche Prüfung stattgefunden hat.

## Prompt-Vertrag für Tutoring {#prompt-contract-for-tutoring}

Es wird nur der für diese Aktivität erforderliche Nachweis übergeben:

```text
Role: explain one approved concept.
Known concept: linear equations.
Evidence: correct after one hint; confidence low.
Allowed action: generate one practice item and an explanation.
Forbidden action: change mastery, scheduling, or learner record.
Output: structured draft with answer key and cited concept reference.
```

Die Anwendung validiert das resultierende Schema, prüft den Antwortschlüssel und protokolliert die Revision des generierten Inhalts, bevor er einer lernenden Person angezeigt wird.

## Evaluation betrifft Lernergebnisse {#evaluation-is-about-learning-outcomes}

Es sollte mehr bewertet werden als die sprachliche Flüssigkeit der Antworten:

| Frage | Nachweis |
|---|---|
| Hat die lernende Person das Konzept gelernt und behalten? | verzögerte Prüfung oder Abrufleistung |
| Ist das Lernendenmodell kalibriert? | vorhergesagte im Vergleich zu beobachteten Ergebnissen |
| Ist die Intervention gerecht? | Kohorten- und Barrierefreiheitsanalyse |
| Ist das Feedback pädagogisch fundiert? | unabhängige Prüfung und Bewertungsraster |
| Ist die Datennutzung rechtmäßig? | Einwilligung, Aufbewahrung, Zugriff und Löschnachweise |
| Führt das LLM Fehler ein? | stichprobenartige Inhaltsprüfung und automatisierte Checks |

Vor dem Einsatz für Noten, Einstufung, Zertifikate oder Berechtigungen sollte ein Pilotbetrieb mit eingeschränktem Curriculum und in einem umkehrbaren Setting erfolgen.

## Rechte und Daten der Lernenden {#learner-rights-and-data}

Adaptive Systeme können sensible Bildungs- und Verhaltensdaten verarbeiten. Die UNESCO-Leitlinien fordern einen menschenzentrierten Ansatz, Datenschutz sowie die Prüfung der pädagogischen und ethischen Eignung. [UNESCO guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)

Festzulegen sind:

- die Mindestdaten, die für den genannten Lernzweck nötig sind;
- Wege für Einwilligung, Zugriff, Korrektur, Export und Löschung;
- altersgerechte Interaktion und menschliche Eskalation;
- Aufbewahrungsfristen für rohe Interaktionsprotokolle im Vergleich zu abgeleitetem Zustand;
- Evaluation von Barrierefreiheit, Sprache und Verzerrung (Bias);
- ein Weg über Lehrkräfte oder berechtigte prüfende Personen für folgenreiche Entscheidungen.

## Stolperfallen {#gotchas}

- **Ein Beherrschungswert kann sicherer wirken, als er ist.** Spärliche oder verzerrte Interaktionsdaten führen zu instabilen Schätzungen. **Abhilfe:** Konfidenz erhalten, mit Baseline-Prüfungen vergleichen und Korrekturen ermöglichen.
- **Ein personalisierter Prompt kann Lernerdaten preisgeben.** Mehr Kontext bedeutet nicht automatisch besseres Tutoring. **Abhilfe:** nur das minimal freigegebene Material übergeben und Protokolle schwärzen.
- **Planung und Generierung lösen unterschiedliche Probleme.** Eine flüssige Erklärung berechnet keine Behaltensleistung. **Abhilfe:** Terminplanung deterministisch und versioniert halten.
- **Benchmark-Genauigkeit belegt keinen Nutzen im Unterricht.** Erfolg auf einem Datensatz muss sich nicht auf ein anderes Curriculum oder eine andere Kohorte übertragen. **Abhilfe:** zeitbewusste, lokale Evaluationen und berechtigte Prüfung durchführen.
- **Generiertes Feedback kann überzeugend, aber falsch sein.** Es kann eine Fehlvorstellung verstärken. **Abhilfe:** Antwortschlüssel validieren, Ausgaben stichprobenartig prüfen und einen Korrekturprozess vorhalten.

## Quellen {#sources}

- [pyKT toolkit](https://github.com/pykt-team/pykt-toolkit)
- [Open Spaced Repetition](https://github.com/open-spaced-repetition)
- [SRS benchmark](https://github.com/open-spaced-repetition/srs-benchmark)
- [UNESCO guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)

## Siehe auch {#see-also}

- [[adaptive-learning-systems]]
- [[rag-pipeline]]
- [[agent-memory]]
- [[token-optimization]]
- [[agent-evaluation]]
