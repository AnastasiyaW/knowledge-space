---
title: "Unabhängige Prüfung und Multisampling für Agent-Workflows"
description: "Unabhängige Kandidaten erzeugen, Evidenz validieren und Agent-Ergebnisse anhand expliziter Akzeptanzkriterien auswählen – statt anhand fester Stimmenzahlen oder Modell-Confidence."
tags: [llm-agents, multisampling, review, evaluation, evidence]
level: 4
source_sha256: 9c7fa4ad382325c6caa9181850efb5fcf20bbf2e77923bed7cca8dce834d3cbc
translation: machine
translated_at: '2026-10-24'
---
# Unabhängige Prüfung und Multisampling für Agent-Workflows {#independent-review-and-multisampling-for-agent-workflows}

**Stand der Prüfung: 2026-09-04.** Mehrere Agent-Ergebnisse können unterschiedliche Fehlermuster offenlegen, aber weder ein Mehrheitsentscheid noch die Confidence eines Agenten ist ein Nachweis dafür, dass ein Ergebnis korrekt ist. Multisampling sollte als begrenzte Methode verstanden werden, konkurrierende Kandidaten zu erzeugen; Review ist eine eigenständige Verifikationsaktivität mit einem benannten Akzeptanzvertrag.

## Mit einem Task-Vertrag beginnen {#start-with-a-task-contract}

Bevor Alternativen erzeugt werden, sollte festgehalten werden, was für diese Aufgabe „fertig“ bedeutet. Ein brauchbarer Vertrag macht Kandidaten vergleichbar und verhindert, dass ein Review-Schwarm die Anfrage stillschweigend verändert.

```yaml
task_id: payment-retry-001
source_revision: immutable repository revision
deliverable: patch and test receipt
acceptance:
  - named test command passes
  - retry is idempotent
  - no production mutation during evaluation
authority:
  - repository read and local test only
escalation:
  - missing credential, production target, or unclear owner
```

Der Vertrag sollte eine gewünschte Antwort von dem Nachweis unterscheiden, der sie belegen kann. Bei einer quellengestützten Antwort können das aktuelle Primärquellen sein. Bei einer Code-Änderung kann es ein Diff, deterministische Tests und ein unabhängiges Review sein. Bei einer externen Aktion muss die Freigabe sowie der daraus resultierende Beleg (Receipt) enthalten sein.

## Kandidaten und Verifikation trennen {#separate-candidates-from-verification}

| Rolle | Erlaubte Arbeit | Ausgabe | Allein nicht beweisbar |
|---|---|---|---|
| Kandidatengenerator | einen Antwort- oder Patch-Vorschlag innerhalb des Vertrags erstellen | Kandidat mit belegten Annahmen | dass der Vorschlag funktioniert |
| Evidenzsammler | Quellen finden, erlaubte Prüfungen ausführen, Belege sichern | Evidenzbündel | dass die Evidenz jedes Akzeptanzkriterium erfüllt |
| Verifikator | Kandidat und Evidenz gegen den Vertrag prüfen | bestanden, nicht bestanden oder begrenzte Unsicherheit | Berechtigung, das Ziel zu verändern |
| Selektor | wählt einen bewiesenen Kandidaten oder gibt keine Entscheidung zurück | Begründung der Auswahl | Korrektheit ohne Verifikations-Evidenz |

Unabhängigkeit sollte über unterschiedliche Evidenzpfade gestaltet werden, nicht über theatralisch benannte Rollen. Beispielsweise kann ein Kandidat einen Datenfluss-Übergang nachverfolgen, während ein anderer den angegebenen Akzeptanztest durchführt. Wenn jeder Agent denselben Entwurf, dieselben Werkzeuge und dieselben unausgesprochenen Annahmen erhält, entstehen korrelierte Fehler – selbst wenn sich die Prompts unterscheiden.

## Eine Aggregationsregel wählen, die zur Aussage passt {#choose-an-aggregation-rule-that-fits-the-claim}

| Aussagetyp | Bevorzugte Regel | Warum eine Abstimmung nicht genügt |
|---|---|---|
| deterministische Berechnung oder Code-Verhalten | den benannten Validator ausführen | das Testergebnis ist stärker als Konsens |
| faktische, zeitkritische Aussage | aktuelle Primärquellen-Zitate verlangen | viele Agenten können eine veraltete Quelle wiederholen |
| Designentscheidung | Abwägungen gegen explizite Randbedingungen vergleichen | es kann mehr als eine akzeptable Antwort geben |
| Sicherheitsbedenken | die Vereinigungsmenge als Triage behalten und jeden Befund bestätigen | seltene Befunde können wertvoll sein, unbestätigte Befunde sind aber keine Schwachstellen |
| irreversible Aktion | die deklarierte Freigabe und einen Side-Effect-Beleg verlangen | Übereinstimmung erteilt keine Berechtigung |

Ein Selektor darf auch „kein Kandidat nachgewiesen“ zurückgeben. Das ist ein gesundes Ergebnis, wenn Evidenz fehlt, der Vertrag mehrdeutig ist oder die erlaubten Werkzeuge die relevante Grenze nicht prüfen können.

## Begrenzte Multisampling-Schleife {#bounded-multisampling-loop}

1. Task-Vertrag, Eingabe-Revision, Werkzeugrichtlinie und Abbruchbedingung festschreiben.
2. Unabhängige Kandidaten erzeugen, die eine Evidenzperspektive oder einen Implementierungsansatz variieren.
3. Deterministische Validierung ausführen, bevor ein Modell Fließtext über die Validierung bewertet.
4. Nur Kandidat und das für den Verifikator notwendige Evidenzbündel an einen blinden Verifikator übergeben, der den Vertrag anwendet.
5. Einen Kandidaten nur auswählen, wenn seine erforderliche Evidenz vorliegt; andernfalls die Lücke festhalten und eskalieren oder abbrechen.

Ein Budget in Größen festlegen, die Betreibende beobachten können: erlaubte Kandidaten, Zeit, Werkzeugaufrufe oder Kosten. Früh stoppen, wenn alle Kriterien belegt sind, und an der Budgetgrenze stoppen, wenn nicht. Die Stichprobenzahl nicht stillschweigend erhöhen, bis eine bevorzugte Antwort gewinnt.

## Evidenzprotokoll {#evidence-record}

Genug Information festhalten, damit ein späterer Prüfer die Entscheidung reproduzieren kann:

- Aufgaben- und Kandidaten-Kennungen;
- Quell-Revision, Konfigurationsversion und Eingabe-Fixture;
- exakte Validierungsbefehle und Exit-Ergebnisse;
- Quell-URLs oder Artefakt-Digests;
- verweigerte Werkzeuge, Freigaben und Belege externer Nebenwirkungen;
- Begründung der Auswahl und offen gebliebene Unsicherheiten.

Dieses Protokoll macht ein Agent-Ensemble zu einem auditierbaren Workflow. Außerdem macht es Regressionsbewertungen möglich: Ein künftiger Lauf kann denselben Vertrag verwenden und offenlegen, welche Eingabe, welches Werkzeug oder welche Quelle sich geändert hat.

## Sicherheits-Reviews brauchen Bestätigung {#security-reviews-need-confirmation}

Sicherheitsorientierte Agenten dürfen ein weites Netz auswerfen, ihre Ausgabe ist aber ein Hinweis, keine Freigabeentscheidung. Befund, betroffene Revision, vermuteter Auslösepfad und die zur Reproduktion nötige Evidenz festhalten. Vor der Bezeichnung als Schwachstelle oder einer Änderung am Produktivsystem über die sicherste verfügbare Methode bestätigen – Code-Inspektion, ein kontrolliertes Test-Fixture oder eine autorisierte Umgebung. Einem Review-Agenten keine zusätzlichen Netzwerk-, Zugangsdaten- oder Deployment-Berechtigungen geben, nur damit sein Ergebnis überzeugender wirkt.

## Häufige Fehlermuster {#common-failure-modes}

- **Mehrheit als Beweis:** Übereinstimmung kann eine gemeinsame falsche Prämisse verstärken.
- **Gemeinsames veränderliches Scratchpad:** Spätere Kandidaten kopieren den ersten, statt ihn zu prüfen.
- **Unbegrenzte Debatte:** Mehr Nachrichten ersetzen einen fehlenden Akzeptanztest.
- **Blindes Vertrauen in Confidence-Werte:** Confidence ist keine kalibrierte Korrektheitsgarantie.
- **Sicherheits-„Vereinigung“ als Fakt ausgeliefert:** Triage-Befunde erfordern Bestätigung und Prüfung durch den Verantwortlichen.
- **Verlorene Herkunftsnachweise:** Ohne Revision, Fixture und Beleg kann ein künftiges Ergebnis nicht ehrlich verglichen werden.

## Referenzen {#references}

- [OpenAI Evals documentation](https://platform.openai.com/docs/guides/evals) — Definitionen, Läufe und Grader für Evaluationen.
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — ein Risikomanagement-Rahmen für generative KI-Systeme.
- [Claude Code subagents](https://code.claude.com/docs/en/subagents) — aktuelle Dokumentation zu eng gefassten Subagent-Definitionen und delegierter Arbeit.
