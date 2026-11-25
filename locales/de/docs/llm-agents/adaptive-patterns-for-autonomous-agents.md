---
title: "Adaptive Muster für autonome Agenten"
description: "Explizite Task-Zustände, begrenzte Hooks, fähigkeitsbeschränkte Subagenten und evidenzbasierte Gates verwenden, statt undurchsichtige Schlüsselwort-Trigger oder willkürliche Mehrdeutigkeitswerte einzusetzen."
tags: [agents, orchestration, hooks, subagents, task-state, verification]
level: 3
source_sha256: 738a2f89a78e98f8f22921f17616444542f2a1087a38edc94f4d6845748d170f
translation: machine
translated_at: '2026-10-24'
---
# Adaptive Muster für autonome Agenten {#adaptive-patterns-for-autonomous-agents}

**Stand der Prüfung: 2026-09-04.** Ein adaptives Agentensystem sollte sein Verhalten nur ändern, weil eine beobachtbare Bedingung und eine deklarierte Richtlinie es verlangen, nicht weil ein vages Schlüsselwort oder eine Vermutung des Modells gegriffen hat. Die aktuellen Erweiterungspunkte von Claude Code bieten Skills, Hooks, Subagenten, Agent-Teams und Plugins; sie machen beliebige Automatisierung aber nicht von sich aus sicher. [Extension overview](https://code.claude.com/docs/en/features-overview) [Hooks guide](https://code.claude.com/docs/en/hooks-guide)

## Den Mechanismus an den Bedarf anpassen {#match-the-mechanism-to-the-need}

| Bedarf | Kleinster sinnvoller Mechanismus | Nachweis des Erfolgs |
|---|---|---|
| wiederkehrende Projektvorgaben | committete Anweisungs- oder Regeldatei | eine Aufgabe folgt der deklarierten Invariante |
| wiederverwendbare Prozedur | Skill mit eng gefasstem Trigger | die Prozedur erzeugt das erwartete Artefakt |
| deterministische Vor- oder Nachbedingung | Command-Hook | Exit-Status oder strukturierter Receipt |
| fokussierte Nebenaufgabe | fähigkeitsbeschränkter Subagent | begrenztes Ergebnis plus Quellen- bzw. Testnachweis |
| parallele unabhängige Arbeit | Agent-Team oder isolierter Worktree | keine Kollision im gemeinsamen Zustand und zusammengeführtes Review |
| langlaufende Auslieferung | dauerhafter Task-Eintrag | jedes Element erreicht einen terminalen Receipt |

Füge keinen Hook nur hinzu, weil ein Verhalten nützlich sein könnte. Ein Lifecycle-Hook ist angemessen, wenn Auslöser, erlaubte Aktion, Ausgabe, Fehlersignal und Verantwortliche alle bekannt sind.

## Deklarierte Aktivierung statt Schlüsselwort-Raten bevorzugen {#prefer-declared-activation-over-keyword-guessing}

Claude Code kann Skills bei Bedarf laden und Hooks für Lifecycle-Ereignisse wie UserPromptSubmit, PreToolUse, PostToolUse und SubagentStop ausführen. Ein Hook kann einen Befehl, eine HTTP-Anfrage, ein MCP-Tool, einen Prompt oder einen agentischen Verifizierer ausführen. Command-Hooks sind die stabile Wahl für deterministische Durchsetzung; Agent-Hooks sind als experimentell dokumentiert. [Hooks reference](https://code.claude.com/docs/en/hooks) [Agent-based hooks](https://code.claude.com/docs/en/hooks-guide)

Verwende eine kleine Richtlinientabelle statt eines Regex, der Berechtigungen stillschweigend verändert:

```json
{
  "event": "PreToolUse",
  "condition": "requested action writes to a production target",
  "action": "require approved change record",
  "on_unknown": "block with a visible reason",
  "receipt": "change-record id and tool outcome"
}
```

Schlüsselwortabgleich kann nur für die Auswahl nicht-mutierenden Kontexts nützlich sein. Er darf niemals allein Zugangsdaten gewähren, einen Mandanten auswählen, den Werkzeugzugriff erweitern oder eine externe Nebenwirkung auslösen.

## Fragen als Risiko-Gate statt als Punkteritual nutzen {#use-questions-as-a-risk-gate-not-a-score-ritual}

Ein willkürlicher Schwellenwert wie „20 % Mehrdeutigkeit“ ist weder ein Sicherheitsnachweis noch eine Produktanforderung. Frage nach einer Klärung, wenn eine Antwort nötig ist, um ein nicht rückgängig zu machendes Ziel zu wählen, eine Autorisierungsgrenze zu interpretieren oder das Akzeptanzkriterium festzulegen. Andernfalls führe die nächste reversible, im Rahmen liegende Aktion aus und berichte den Nachweis.

| Beobachtung | Sichere Reaktion |
|---|---|
| Ziel oder Löschumfang ist unbekannt | vor der Mutation anhalten und das genaue Ziel anfordern |
| Nutzerabsicht ist klar, die Umsetzung hat aber Wahlmöglichkeiten | die kleinste reversible Umsetzung wählen und sie verifizieren |
| Test oder Receipt fehlt | die echte Validierung der Aufgabe erstellen oder ausführen, bevor Erfolg gemeldet wird |
| Quellenaussage ist zeitkritisch | die primäre Dokumentation abrufen und das Ergebnis datieren |
| Teilaufgabe würde den Hauptkontext überlasten | mit expliziten Werkzeugen, Umfang und erwartetem Receipt delegieren |

So werden sowohl stilles Raten als auch eine endlose Rückfrageschleife vermieden.

## Dauerhafter Task-Zustand {#durable-task-state}

Der Konversationsverlauf ist kein verlässliches Transaktionsprotokoll. Halte Arbeitselemente in einem im Repository sichtbaren Datensatz mit stabiler ID, Quellrevision, Verantwortlichem, terminalem Status und Verweis auf den Nachweis:

```json
{
  "task_id": "DOC-042",
  "source_revision": "immutable-git-sha",
  "status": "RUNNING",
  "acceptance": ["strict build passes", "fresh review passes"],
  "attempt": 1,
  "idempotency_key": "docs:la051-055:revision",
  "evidence": ["reports/doc-042/links.txt"],
  "next_recheck": "named command or external event"
}
```

Gültige Zustandsübergänge sollten explizit sein, etwa PENDING zu RUNNING zu PASS, BLOCKED_EXTERNAL oder FAILED_RETRYABLE. Eine grün wirkende Chat-Nachricht ist ohne den benannten Receipt kein terminaler Zustand.

## Den Zustand an den tatsächlichen Workspace koppeln {#couple-state-to-the-actual-workspace}

Halte die Git-Revision, den Worktree und den Validierungsbefehl fest, die ein Ergebnis erzeugt haben. Ändert sich ein Branch, gilt ein früheres Bestehen unter Umständen nicht mehr. Bei parallelen Änderungen gilt:

1. Gib jedem Schreibenden einen isolierten Worktree oder exklusive Verantwortung für Dateien;
2. halte gemeinsam veränderliche Ressourcen hinter einem sichtbaren Lock und einer externen Zustandsprüfung;
3. reserviere externe IDs oder URLs vor Arbeitsbeginn, wenn Duplikate schädlich wären;
4. führe die kausale Validierung nach einer Integration oder einem Rebase erneut aus;
5. verwende für wesentliche öffentliche, sicherheitsrelevante oder Release-Arbeiten einen frischen, unabhängigen Reviewer.

Subagenten sind nützlich, weil jeder einen unabhängigen Kontext, eigene Anweisungen und beschränkte Werkzeuge erhält. Sie ersetzen kein Merge-Gate, und ihre Schlussfolgerungen sind nicht automatisch maßgeblich. [Subagents](https://code.claude.com/docs/en/subagents)

## Speicher ist ein veröffentlichbarer Input {#memory-is-a-publishable-input}

Halte operatives Wissen navigierbar:

- indexiere dauerhafte Projektentscheidungen und den aktuellen Stand;
- binde Aussagen an Quellrevisionen, Logs, Tests oder externe Receipts;
- unterscheide eine datierte Beobachtung von einer wiederverwendbaren Regel;
- mache veraltete Einträge sichtbar, statt sie stillschweigend als aktuell zu behandeln;
- validiere Links und Verantwortlichkeiten für Dokumente, auf die sich die Automatisierung stützt.

Ein Agent kann nicht sicher auf Informationen handeln, die er mit seinen verfügbaren Werkzeugen nicht abrufen und prüfen kann.

## Fallstricke {#gotchas}

- **Ein Schlüsselwort aktiviert ein mächtiges Werkzeug.** Natürliche Sprache ist mehrdeutig und kann vom Angreifer gesteuert werden. **Abhilfe:** Schlüsselwörter nur für nicht-mutierendes Routing verwenden; Berechtigungen und externe Effekte explizit machen.
- **Ein Prompt-Hook lässt ein LLM über eine Invariante entscheiden.** Das Ergebnis kann schwanken und ist schwer zu prüfen. **Abhilfe:** für harte Richtlinien deterministische Hooks verwenden; modellbasiertes Urteil nur beratend einsetzen.
- **Eine Task-Datei meldet „erledigt“ nach einem teilweisen Lauf.** Ein Prozess kann vor der letzten Nebenwirkung abgebrochen sein. **Abhilfe:** einen terminalen Receipt verlangen, der das angeforderte Ergebnis belegt.
- **Ein Subagent meldet ein sauberes Review seines eigenen Outputs.** Das ist keine unabhängige Verifikation. **Abhilfe:** für wesentliche Arbeiten einen separaten, frischen Reviewer einsetzen.
- **Ein veralteter Lock wird allein anhand seines Zeitstempels freigegeben.** Der ursprüngliche Prozess könnte die Ressource noch besitzen. **Abhilfe:** vor dem Freigeben den tatsächlichen Prozess bzw. den externen Dienst prüfen.

## Quellen {#sources}

- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview)
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## Siehe auch {#see-also}

- [[agent-design-patterns]]
- [[context-engineering]]
- [[agent-memory]]
- [[agent-orchestration]]
