---
title: "Context Engineering und dauerhafter Aufgabenzustand"
description: "Behandeln Sie den Modellkontext als begrenzte Arbeitseingabe und bewahren Sie Aufgabenzustand, Evidenz, Autorität und Retrieval-Herkunft in versionierten Artefakten statt in festen Token-Kontingenten."
tags: [llm-agents, context-engineering, state, retrieval, compaction, evidence]
level: 3
source_sha256: 2b915f26b532f8ab9490f0bedd89a2020511772bdaa47c5c268b1648270572da
translation: machine
translated_at: '2026-10-24'
---
# Context Engineering und dauerhafter Aufgabenzustand {#context-engineering-and-durable-task-state}

**Stand der Prüfung: 2026-09-04.** Der Modellkontext ist eine begrenzte Eingabe für einen Turn oder einen Lauf. Er ist weder eine dauerhafte Datenbank, ein Audit-Log noch ein Berechtigungssystem. Context Engineering bezeichnet die Disziplin, die kleinste Informationsmenge auszuwählen, zu validieren und aktuell zu halten, mit der ein Agent eine definierte Aufgabe sicher erledigen kann.

## Informationsebenen trennen {#separate-the-information-planes}

| Ebene | Zweck | Quelle der Wahrheit |
|---|---|---|
| Betriebsrichtlinie | Repository-Regeln, Tool-Grenzen und Eskalation | geprüfte Konfigurations- und Anweisungsdateien |
| Aufgabenzustand | Ziel, Abnahmekriterien, aktueller Schritt und Blockaden | versioniertes Aufgabenartefakt |
| Evidenz | Testausgaben, Quellenangaben, Zielbelege und Reviews | dauerhaftes Artefakt mit Revision oder Zeitstempel |
| Gesprächsverlauf | Dialogkontinuität | Sitzungsprotokoll, nicht der alleinige Aufgabennachweis |
| abgerufenes Material | aufgabenrelevante Dokumente oder Daten | zitierte Quelle plus Retrieval-Metadaten |
| persönliches Gedächtnis | vom Nutzer freigegebene Präferenzen oder Fakten | dokumentierte Einwilligung, Aufbewahrung und Löschpfad |

Verwenden Sie keine Chat-Zusammenfassung als einzige Kopie einer Entscheidung, einer Berechtigungsgrenze oder eines Deployment-Ergebnisses. Die Speicherdokumentation von Claude Code unterscheidet zwischen repositoryweiten Anleitungen und dem flüchtigen Sitzungskontext, der sie verbraucht. [How Claude remembers your project](https://code.claude.com/docs/en/memory)

## Kontext nach Vertrag aufnehmen {#admit-context-by-contract}

Bevor Material in einen Prompt gelangt, beantworten Sie fünf Fragen:

1. **Relevanz:** Ändert es die nächste Entscheidung der aktuellen Aufgabe?
2. **Autorität:** Darf diese Quelle die Aufgabe beeinflussen, oder handelt es sich um nicht vertrauenswürdige Eingabe?
3. **Aktualität:** Kann sich die Aussage geändert haben, und sind Revision oder Abrufzeitpunkt erfasst?
4. **Sensitivität:** Benötigt die Aufgabe diese Daten tatsächlich, und ist das gewählte Tool bzw. der Provider dafür freigegeben?
5. **Evidenz:** Kann ein Reviewer die Originalquelle nachvollziehen, statt der Zusammenfassung zu vertrauen?

Diese Prüfungen sind dauerhafter als eine allgemeingültige prozentuale Aufteilung zwischen Anweisungen, Verlauf, Tools und Ausgabe. Kontextgröße, Preise, Cache-Verhalten und Modellgrenzen ändern sich je nach Provider und Modell; messen Sie sie anhand des aktuellen Zielvertrags.

## Aufgabenzustand außerhalb des Turns persistieren {#persist-task-state-outside-the-turn}

Bei Arbeit, die sich über mehr als einen Turn erstreckt, führen Sie ein kleines Aufgabenverzeichnis oder ein gleichwertiges dauerhaftes Protokoll.

```text
task/
  spec.md          frozen acceptance criteria and authority
  state.json       current phase, owner, attempt, and blocker
  sources.md       primary-source URLs and retrieval dates
  evidence/        test output, receipts, screenshots, or digests
  review.md        independent verdict and required fixes
```

Der Zustandseintrag sollte die Eingaberevision nennen und angeben, ob ein externer Seiteneffekt nur geplant, laufend, abgeschlossen oder blockiert ist. Anhängbare Evidenz ist sicherer als wiederholtes Überschreiben einer gemeinsamen Zusammenfassung; veränderlicher Koordinationszustand braucht einen klaren Eigentümer und eine Konfliktregel.

## Kontext schichtweise aufbauen {#build-context-in-layers}

Eine praktische Reihenfolge für den Kontextaufbau lautet:

1. Betriebsrichtlinie und eingefrorenen Aufgabenvertrag laden;
2. den kleinsten Quell- oder Code-Ausschnitt hinzufügen, der für die nächste Entscheidung nötig ist;
3. zusätzliches Material nur gegen eine benannte Frage abrufen;
4. abgerufenen Text mit Herkunft, Revision/Datum und Vertrauensstufe kennzeichnen;
5. erlaubte Tools ausführen und ihre Belege außerhalb des Prompts speichern;
6. für den nächsten Turn einen kompakten Zustandsverweis oder eine verifizierte Zusammenfassung einfügen.

So wird veränderliche Tool-Ausgabe nicht zu dauerhafter Anweisung. Außerdem lässt sich ein Kontext-Reset wiederherstellen: Der nächste Agent liest die Aufgabenartefakte, statt zu raten, was eine frühere Unterhaltung gemeint hat.

## Verdichtung ist verlustbehaftet {#compaction-is-lossy}

Eine Zusammenfassung kann ein Ergebnis bewahren, sollte aber ausgelassene Details offenlegen und auf die Evidenz verlinken, die sie zusammenfasst. Vor einer Verdichtung persistieren Sie Fakten, deren erneute Ermittlung teuer oder unsicher wäre: Abnahmekriterien, getestete Revisionen, externe Seiteneffekte, ungelöste Konflikte, Freigaben und Quellorte.

Nach der Verdichtung führen Sie wieder nur den aktuellen Aufgabenvertrag und Verweise auf dauerhafte Evidenz ein. Fügen Sie keine stetig wachsende „Master-Zusammenfassung“ erneut ein, denn sie würde zu einer ungeprüften Autoritätsquelle.

## Retrieval ist eine Sicherheitsgrenze {#retrieval-is-a-security-boundary}

Abgerufene Repositories, Tickets, Webseiten und Tool-Ausgaben können Anweisungen enthalten, die für Menschen oder andere Systeme geschrieben wurden. Behandeln Sie sie als Daten. Sie dürfen kein Tool autorisieren, keine Richtlinie ändern, keine Geheimnisse anfordern und keinen Aufgabenvertrag mit höherer Priorität überschreiben.

Für einen Agenten, der Tools aufrufen kann, protokollieren Sie die Retrieval-Anfrage, die gewählte Quelle, gegebenenfalls die Version des Extraktors und die Dokumentrevision. So lässt sich eine irreführende Antwort oder ein Prompt-Injection-Versuch untersuchen, ohne in jedem Kontextfenster den gesamten Rohinhalt aufzubewahren. [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

## Die Kontextstrategie bewerten {#evaluate-the-context-strategy}

Bewerten Sie Änderungen am Kontext mit einem festen Aufgabensatz und einem definierten Fehlermodell:

| Frage | Evidenz |
|---|---|
| Findet der Agent die erforderliche maßgebliche Quelle? | Quellenangabe und Retrieval-Trace |
| Bleiben Aufgabenvorgaben nach der Verdichtung erhalten? | Wiederholung oder unabhängige Prüfung gegen dasselbe Aufgabenartefakt |
| Vermeidet er verbotene Daten- oder Tool-Nutzung? | Berechtigungs- und Tool-Call-Audit |
| Bewahrt ein kürzerer Kontext die Abnahmeergebnisse? | vergleichbare Fixture- und Validator-Ausgabe |
| Kann eine neue Sitzung sicher fortgesetzt werden? | Zustandsartefakt plus Evidenzverweise, nicht mündliche Überlieferung |

Eine geringere Token-Anzahl ist nicht automatisch eine Verbesserung. Behalten Sie eine Änderung nur, wenn sie das geforderte Ergebnis, die Autoritätsgrenzen und die Reproduzierbarkeit bewahrt.

## Häufige Fehlermuster {#common-failure-modes}

- **Kontext als Datenbank:** wichtiger Zustand existiert nur in einem Chat-Verlauf.
- **Quellenlose Zusammenfassung:** eine verdichtete Aussage hat keine rückverfolgbare Evidenz.
- **Alles per Retrieval:** unpassendes oder veraltetes Material verdrängt die aktuelle Aufgabe.
- **Prompt-Injection durch Retrieval:** nicht vertrauenswürdiger Text wird als ausführbare Richtlinie behandelt.
- **Folklore fester Budgets:** eine modellspezifische Token-Aufteilung wird als allgemeingültige Empfehlung veröffentlicht.
- **Verdichtung ohne Checkpoint:** ein Neustart verliert den einzigen Nachweis von Freigaben oder Seiteneffekten.

## Referenzen {#references}

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
