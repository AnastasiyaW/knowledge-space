---
title: "Agentenbewertung und Nachweise"
description: "Bewerten Sie das Verhalten von Agenten mit versionierten Task-Fixtures, deterministischen Validatoren, kontrollierten Prüfungen von Nebenwirkungen und reproduzierbaren Nachweisen statt mit einem einzelnen Benchmark-Wert."
tags: [llm-agents, evaluation, testing, benchmarks, evidence, swe-bench]
level: 4
source_sha256: b9bcbe8f4f828d916e5204b2e1cfdfcda95f22c3d63ab7af71d6aecc19e219a7
translation: machine
translated_at: '2026-10-24'
---
# Agentenbewertung und Nachweise {#agent-evaluation-and-evidence}

**Geprüfter Stand: 2026-09-06.** Ein Agentenlauf kombiniert ein Modell mit Anweisungen, Werkzeugen, Zustand, Daten, Berechtigungen und einer Ausführungsumgebung. Ein Benchmark-Ergebnis kann als Nachweis für ein klar definiertes Harness nützlich sein; es beweist jedoch nicht, dass eine Produktionsintegration sicher, aktuell oder für eine andere Aufgabe geeignet ist.

## Das Bewertungsobjekt definieren {#define-the-evaluation-object}

Legen Sie vor dem Vergleich von Ergebnissen genau fest, was bewertet wird:

- Task-Fixture und unveränderliche Eingabe-Revision;
- Agenten-Anweisungen, Modellkonfiguration und Werkzeugversionen;
- verfügbare Berechtigungen, Datenumfang und Umgebung;
- erwartetes Ergebnis und verbotene Nebenwirkungen;
- Reihenfolge der Validatoren und die Freigabeentscheidung, die das Ergebnis stützen darf.

Ein reproduzierbarer Bewertungsdatensatz bindet diese Fakten zusammen.

```json
{
  "run_id": "support-triage-2026-09-04-a",
  "source_revision": "immutable commit or content digest",
  "fixture_revision": "versioned test data",
  "agent_configuration": "policy and tool configuration digest",
  "authority": "local test only",
  "validators": ["schema", "unit", "sandboxed integration"],
  "result": "pass | fail | blocked",
  "evidence": ["test output", "external receipt if applicable"]
}
```

Verwenden Sie eine alte Lauf-Kennung nicht erneut, nachdem Sie Fixture, Quell-Revision, Umgebung oder Konfiguration geändert haben. Andernfalls werden Cache-Wiederverwendung und historische Vergleiche mehrdeutig.

## Mehr als den Abschluss der Aufgabe bewerten {#evaluate-more-than-task-completion}

| Dimension | Frage | Stärkster praktikabler Nachweis |
|---|---|---|
| funktionales Ergebnis | hat die Aufgabe ihre Abnahmekriterien erfüllt? | deterministischer Test oder validiertes Artefakt |
| Qualität | ist die Antwort korrekt, vollständig und für ihre Zielgruppe brauchbar? | Bewertungsraster mit kalibrierter menschlicher Prüfung oder Modell-als-Richter |
| Sicherheit und Nebenwirkungen | hat der Lauf verbotene Zugriffe oder Änderungen vermieden? | Fähigkeitsprotokoll, Sandbox-Aufzeichnung und externe Belege |
| Berechtigungen | ist der Agent innerhalb erlaubter Werkzeuge, Daten und Freigaben geblieben? | wirksame Richtlinie und Audit der Werkzeugaufrufe |
| Betriebsverhalten | lagen Wiederholungen, Zeitüberschreitungen und Ressourcennutzung im deklarierten Budget? | strukturierte Laufzeit-Telemetrie |
| Reproduzierbarkeit | kann ein Prüfer dieselben Bedingungen erneut ausführen oder überprüfen? | versionierte Fixture, Konfiguration und aufbewahrte Nachweise |

Die richtige Metrik folgt dem Aufgabenvertrag. Eine niedrige Anzahl von Werkzeugaufrufen ist nicht automatisch besser, wenn dabei die Validierung übersprungen wird; eine schnelle erfolgreiche Antwort ist keine sichere Produktionsaktion ohne den erforderlichen Beleg.

## Reihenfolge der Validatoren {#validator-order}

Führen Sie die günstigsten und deterministischsten Prüfungen zuerst aus und greifen Sie erst danach auf subjektive Beurteilungen zurück:

1. Schemas, Berechtigungen und statische Vorgaben validieren;
2. Unit- oder Fixture-Tests in einer kontrollierten Umgebung ausführen;
3. autorisierte Integrationsprüfungen gegen isolierte oder umkehrbare Ziele durchführen;
4. externe Zustände prüfen und Belege aufbewahren, wo eine Aktion erlaubt ist;
5. kalibrierte menschliche Prüfung oder Modell-Richter für Eigenschaften einsetzen, die ein deterministischer Test nicht entscheiden kann.

Generierter Code und Werkzeugaufrufe sollten nicht uneingeschränkte lokale oder produktive Berechtigungen erhalten, nur um die Bewertung zu vereinfachen. Verwenden Sie die kleinste Sandbox oder Test-Fixture, mit der sich das relevante Verhalten feststellen lässt. Ein Fehlschlagen bei der Beobachtung eines externen Zustands ist ein blockiertes oder unvollständiges Ergebnis, kein automatisches Bestehen.

## Stochastische Läufe brauchen transparente Berichterstattung {#stochastic-runs-need-transparent-reporting}

Wenn ein Agent nichtdeterministisch arbeitet, bewahren Sie jedes Laufergebnis auf und berichten Sie die für die Entscheidung relevante Verteilung: Erfolgs- und Fehlerzahlen, Streuung bei Kosten oder Latenz, Fehlerkategorien und beobachtete Nebenwirkungen. Verwenden Sie für Vergleiche eine feste Aufgabenmenge, halten Sie für Regressionsprüfungen eine Holdout-Menge zurück und legen Sie Konfigurationsänderungen offen.

Wählen Sie die Anzahl der Wiederholungen und das Budget anhand des Risikos, der erwarteten Streuung und der Kosten einer falschen Entscheidung. Es gibt keine allgemeingültige Stichprobengröße, die ein Agentenergebnis zu einem Beweis macht. Wenn eine Freigabe eine Konfidenzschranke benötigt, definieren Sie diese im Bewertungsplan, bevor das Experiment läuft.

## Benchmarks sind Harnesses, keine Produktionszertifikate {#benchmarks-are-harnesses-not-production-certificates}

[SWE-bench](https://github.com/SWE-bench/SWE-bench) bewertet Aufgaben der Softwareentwicklung über einen bestimmten Datensatz und ein bestimmtes Ausführungs-Harness. Die aktuellen Kommandozeilenwerkzeuge erfassen eine Lauf-Kennung und können Instanzen überspringen, für die bereits ein Bericht für diesen Lauf existiert. Behandeln Sie Lauf-ID, Aufgabenteilmenge, Umgebung und Harness-Version als Bestandteil der Identität des Ergebnisses; sonst kann ein gecachtes Ergebnis für eine frische Bewertung gehalten werden. [SWE-bench CLI-Referenz](https://www.swebench.com/SWE-bench/reference/cli/)

Ein Benchmark kann eine Regression aufdecken oder ein definiertes System mit seiner Vorgängerversion vergleichen. Er kann nicht zeigen, dass die Tests eines Repositorys bestehen, dass die Zugangsdaten einer Organisation geschützt sind oder dass ein externes Deployment korrekt funktioniert. Halten Sie diese Punkte als eigene Nachweisfelder fest.

## Freigabe-Gate {#release-gate}

Eine Freigabeentscheidung sollte die Nachweise benennen, die für ihre Risikostufe erforderlich sind:

| Änderungsklasse | Mindestnachweis |
|---|---|
| Text oder lokale nicht ausführbare Änderung | Link- und Build-Validierung sowie redaktionelle Prüfung |
| Codeänderung ohne externe Wirkung | relevante automatisierte Tests, Diff-Prüfung und Quell-Revision |
| Integration mit umkehrbarem Testziel | kontrollierter Integrationsbeleg und Prüfung des Fehlerpfads |
| externe oder produktive Wirkung | ausdrückliche Berechtigung, Idempotenz- bzw. Rollback-Plan, frischer Zielbeleg und unabhängige Prüfung |

Ein einzelner Gesamtwert ist ein Dashboard-Signal, kein Ersatz für das einzelne Gate, das einen Nutzer, eine Datenbank, eine Zahlung, ein Deployment oder eine veröffentlichte Aussage schützt.

## Die Abschlussaussage an den Nachweis binden {#match-the-completion-claim-to-the-evidence}

Verwenden Sie getrennte Nachweisstufen statt eines undifferenzierten `PASS`. Das Folgende ist eine Konvention für die technische Berichterstattung, keine Statustaxonomie eines SDK.

| Beobachtete Stufe | Was sie belegt | Was unbewiesen bleibt |
|---|---|---|
| Quellprüfung | die geprüfte Revision enthält die beabsichtigte Anweisung oder Implementierung | ob ein aktives System sie lädt |
| fokussierte Fixture | die benannten Eingaben und Assertions haben in der protokollierten Umgebung bestanden | Verhalten außerhalb dieser Fälle oder in einer anderen Laufzeit |
| Installation und Registrierung | erwartete Bytes sind installiert und der aktive Einstiegspunkt wählt sie aus | ob ein realer Aufruf den geänderten Zweig erreicht |
| nutzender Workflow | der angeforderte Nutzerpfad hat das festgelegte Ergebnis in der benannten Umgebung erzeugt | nicht betroffene Pfade, Versionen, Lasten und Qualitätsdimensionen |

Welche Stufe erforderlich ist, folgt aus der Anfrage. Die Prüfung einer Anweisungsdatei kann eine Quellprüfung abschließen. Sie schließt nicht eine Anfrage ab, diese Anweisung zu installieren und ihre Wirkung zu zeigen. Ein Testdouble kann einen lokalen Interaktionsvertrag belegen; es kann nicht feststellen, dass der reale Dienst eine Anfrage angenommen hat. Bewahren Sie Eingabe, Revision, Assertion, tatsächliche Beobachtung und die gestützte Aussage gemeinsam auf.

Auch die Registrierung selbst kann Erreichbarkeitslücken verbergen. Im OpenAI Agents SDK für TypeScript gelten Eingabe-Guardrails für den ersten Agenten, Ausgabe-Guardrails für die finale Ausgabe und Werkzeug-Guardrails für unterstützte Function-Tool-Aufrufe. Eingabeprüfungen können nebenläufig zum Agenten laufen. Dass ein Guardrail in der Konfiguration steht, belegt deshalb nicht, dass er vor jeder Nebenwirkung lief. Prüfen Sie den tatsächlichen Pfad und den Ausführungsmodus. [SDK: Geltungsbereich und Ausführung von Guardrails](https://openai.github.io/openai-agents-js/guides/guardrails/)

## Weiterarbeiten bis zum akzeptierten Ergebnis, nicht bis zum nächsten Bericht {#continue-until-the-accepted-outcome-not-until-the-next-report}

Ein brauchbarer Abschlussvertrag verbindet das angeforderte Ergebnis mit der nächsten ausführbaren Aktion und ihrem Abnahmebeleg. Ein Befund, eine Prüfung, eine Übergabe oder ein fehlgeschlagener Versuch verändert diesen Zustand; er schließt die Aufgabe nicht automatisch ab.

| Aktuelle Beobachtung | Aktion innerhalb der bestehenden Aufgabe und Berechtigung | Endbeleg |
|---|---|---|
| reproduzierbarer lokaler Implementierungsfehler | ursächliche Korrektur vornehmen und die betroffene Prüfung erneut ausführen | korrigiertes Verhalten im fehlschlagenden Fall und in den relevanten Kontrollen |
| Arbeit in einem Branch abgeschlossen, aber nicht installiert | die angeforderte Auslieferung über den etablierten Weg abschließen | Quell-Revision, Installationsergebnis und erforderliche Prüfung des Verbrauchers |
| Prozess beendet, ohne Endergebnis | teilweise Wirkungen abgleichen, bevor eine idempotente Reparatur oder Fortsetzung erfolgt | vollständige Ausgabe oder eine belegte Grenze, die das Fortsetzen verhindert |
| erforderliche Freigabe oder externe Abhängigkeit ist tatsächlich nicht verfügbar | teilweise Arbeit erhalten und die genaue offene Entscheidung oder erneute Prüfung benennen | beobachtete Ablehnung, ausstehende Freigabe oder Antwort der Abhängigkeit |
| alle akzeptierten Kriterien sind hinreichend belegt | Aufgabe schließen | Zuordnung von Kriterien zu Nachweisen, mit angegebenen Grenzen des Beweises |

Dies ist eine Betriebsregel, die aus der Trennung von Aufgabenzustand und Agentenmeldungen folgt. Sie ist kein Auftrag, unbegrenzt erneut zu versuchen oder Berechtigungen zu erweitern. Ein fehlgeschlagener lokaler Test ist für sich genommen kein externes Hindernis. Umgekehrt berechtigt ein Abschlussziel nicht zum Löschen, zu einem neuen Veröffentlichungsziel oder zu einer nicht genehmigten Produktionsänderung.

Das SDK unterstützt sowohl modellgesteuerte Orchestrierung als auch explizite Kontrollflüsse im Code. Ein deterministischer Zustandsübergang passt, wenn die nächste Aktion auf einer bekannten Bedingung beruht; das Urteil eines Sprachmodells bleibt für die Diagnose nützlich. Wenn ein Werkzeug tatsächlich eine Freigabe verlangt, bewahrt der Human-in-the-Loop-Mechanismus den unterbrochenen Lauf für eine ausdrückliche Freigabe oder Ablehnung, statt das Werkzeug als ausgeführt zu behandeln. [Agenten-Orchestrierung](https://openai.github.io/openai-agents-js/guides/multi-agent/), [Freigabe und Fortsetzung](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

Kompensieren Sie einen vorzeitigen Abbruch nicht durch verpflichtende zusätzliche Prüfrunden. Wiederholen Sie Prüfungen, weil ein fehlgeschlagenes Kriterium, eine geänderte Abhängigkeit oder ein neu beobachtetes wesentliches Risiko frühere Nachweise ungültig macht. Behalten Sie noch gültige Ergebnisse für unveränderte Bereiche. Hören Sie mit der Erweiterung auf, sobald der gesamte akzeptierte Umfang erfüllt ist; optionale Verfeinerung ist eine eigene Entscheidung. Binden Sie bei nebenläufiger Arbeit jedes Ergebnis an seinen Verantwortlichen und seine Revision: [[multi-session-coordination]], [[swarm-based-review-and-multisampling-in-agentic-workflows]].

## Fallstricke {#gotchas}

- **Benchmark-Ersatz:** Ein Wert wird als Beweis für einen unverwandten Produktions-Workflow behandelt.
- **Veränderliche Fixtures:** Ergebnisse sind nicht vergleichbar, weil sich die Aufgabendaten stillschweigend geändert haben.
- **Mehrdeutiger Cache:** Eine Lauf-Kennung wird über unterschiedlichen Code oder unterschiedliche Konfigurationen hinweg wiederverwendet.
- **Nur-Richter-Abnahme:** Ein Modell erklärt den Erfolg ohne deterministischen oder externen Beleg.
- **Unsichere Bewertung:** Generierter Code erhält Netzwerk-, Zugangsdaten- oder Produktionszugriff ohne begrenztes Testziel.
- **Nur Durchschnittswerte:** Seltene Fehler und kostspielige Ausreißer verschwinden hinter einer Zusammenfassung.
- **Bericht als Ergebnis:** Ein Befund oder eine erfolgreiche Prüfung wird als Abschluss erfasst, obwohl die angeforderte Installation oder der Nutzer-Workflow noch fehlt.
- **Installation als Ausführung:** Übereinstimmende Installations-Hashes werden als Beleg dafür dargestellt, dass eine Live-Anfrage das geänderte Verhalten ausgeübt hat.
- **Selbstspeisende Prüfung:** Eine bestandene Prüfung löst eine weitere allgemeine Prüfung aus, ohne dass sich das Risiko geändert hat, und die akzeptierte Auslieferung bleibt unvollendet.

## Grenzen {#limitations}

Diese Konventionen ordnen Nachweise; sie beweisen nicht, dass ein Abnahmekriterium hinreichend ist oder dass ein automatisiertes Urteil korrekt ist. Visuelle Qualität, fachliche Gültigkeit und seltene Fehler können andere Messverfahren erfordern. Eine begrenzte Beobachtung kann das universelle Fehlen von Fehlern nicht belegen. Halten Sie ungetestete Bedingungen ausdrücklich fest, statt Unsicherheit oder einen lokalen grünen Check in eine Aussage über das gesamte Produkt zu verwandeln.

## Referenzen {#references}

- [OpenAI Evals-Dokumentation](https://platform.openai.com/docs/guides/evals) — aktuelle Konzepte für Bewertungsdefinitionen, Läufe und Graders.
- [SWE-bench-Repository](https://github.com/SWE-bench/SWE-bench) und [CLI-Referenz](https://www.swebench.com/SWE-bench/reference/cli/) — Verhalten von Benchmark und Lauf-Artefakten.
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — Risikorahmen für die Bewertung generativer KI.
