---
title: "Koordination von Multi-Agenten-Systemen"
description: "Koordiniere mehrere Agenten über Aufgabenverträge, Verantwortlichkeiten, Berechtigungen, Zustand und Grenzen der Nachweise; füge Agenten nur hinzu, wenn eine gemessene Zerlegung sie erfordert."
tags: [llm-agents, multi-agent, orchestration, delegation, governance, evidence]
level: 4
source_sha256: 1ffe0801345085a3b71865858c3efce0d6e973d2e1859490fc38255358443c3f
translation: machine
translated_at: '2026-10-24'
---
# Koordination von Multi-Agenten-Systemen {#multi-agent-system-coordination}

**Stand der Prüfung: 2026-09-04.** Ein Multi-Agenten-System ist ein Workflow mit mehr als einer autonomen Entscheidungsinstanz oder mehr als einer Ausführungsrolle. Es ist nicht automatisch leistungsfähiger als ein einzelner Agent. Füge eine Rolle nur hinzu, wenn die Aufgabe eine klar erkennbare Zerlegung, eine eigene Berechtigungs- oder Werkzeuggrenze und eine Möglichkeit zur Bewertung des zusätzlichen Koordinationsaufwands aufweist.

## Beginne mit dem Arbeitsvertrag {#start-with-the-work-contract}

Jede delegierte Aufgabe braucht einen Datensatz, der Nachrichten und Neustarts überdauert.

```json
{
  "task_id": "docs-review-001",
  "input_revision": "immutable source revision",
  "owner": "named coordinator",
  "acceptance": ["named checks pass", "evidence is attached"],
  "authority": "read-only review",
  "allowed_tools": ["read", "search", "named test"],
  "side_effect_policy": "no external actions",
  "handoff": "structured findings with source references"
}
```

Der Vertrag verhindert, dass eine Spezialistenrolle zu einer vagen Persona wird. Er ermöglicht dem Koordinator, eine abgeschlossene Aufgabe von einer Nachricht zu unterscheiden, die lediglich vollständig klingt.

## Verwende die einfachste Koordinationsform {#use-the-simplest-coordination-shape}

| Form | Geeignet für | Hauptrisiko |
|---|---|---|
| einzelner Agent mit deterministischen Werkzeugen | eine zusammenhängende Aufgabe und eine Berechtigungsgrenze | unnötige Delegation verschleiert die Verantwortung |
| sequenzielle Pipeline | jedes Artefakt ist die Eingabe der nächsten definierten Stufe | ein früher Fehler wird zu ungeprüftem nachgelagertem Kontext |
| parallele Untersuchung | unabhängige Quellen, Tests oder Kandidatenentwürfe | doppelte Arbeit und korrelierte Annahmen |
| Supervisor mit begrenzten Workern | mehrere unterschiedliche Aufgabenverträge erfordern einen abschließenden Verantwortlichen | der Supervisor wird zu einem nicht testbaren Engpass |
| unabhängiger Reviewer | eine wesentliche Änderung erfordert eine unvoreingenommene Bewertung | der Reviewer soll ohne Zugang zu den Nachweisen freigeben |

Wähle die Anzahl der Agenten nicht anhand einer Vorlage. Miss, ob der aktuelle Engpass fehlende Nachweise, unzureichenden Werkzeugzugriff oder tatsächlich den Bedarf an einer unabhängigen Prüfung ist. Eine deterministische Transformation sollte Code bleiben, auch wenn ein Agent sie beschreiben kann.

## Trenne den Zustand nach Nebenläufigkeitsmodell {#separate-state-by-concurrency-model}

| Zustandsart | Sichere Koordinationsform |
|---|---|
| unveränderliche Eingabe oder Nachweise | Inhalts-Digest und schreibgeschützte Referenzen |
| nur anhängbare Befunde oder Belege | ein Datensatz pro Erzeuger mit stabilen Kennungen |
| veränderliche Aufgabenzuständigkeit | ein Lease oder ein expliziter alleiniger Schreiber |
| gemeinsames, bearbeitetes Artefakt | isolierter Worktree oder Branch mit geprüftem Merge |
| gerichtete Frage | adressierte Nachricht mit Absender, Empfänger und Antwortprotokoll |
| externe Nebenwirkung | Idempotenzschlüssel, benannter Verantwortlicher und Zielbeleg |

Vermeide einen einzigen gemeinsamen Notizblock, den jeder Agent überschreiben kann. Verluste, Konflikte und versehentlich eingeschleuste Anweisungen lassen sich darin kaum zuordnen. Benötigt ein Agent eine Sperre, halte Ressource, Halter, Heartbeat, Ablaufzeit und Wiederherstellungsprüfung fest.

## Berechtigungen gehen nicht durch eine Übergabe über {#authority-does-not-flow-through-a-handoff}

Ein Koordinator kann einen Agenten bitten, ein Produktionsproblem zu untersuchen, ohne ihm Deployment-Rechte zu gewähren. Werkzeugberechtigungen, Datenzugriff, Freigaberichtlinie und Zielumgebung sind pro Rolle zuzuweisen. Eine weitergeleitete Nachricht, eine Zusammenfassung oder ein Konfidenzwert des Agenten kann keine Berechtigung erweitern.

Claude-Code-Subagenten sind ein konkretes Beispiel für ein System, in dem delegierte Rollen mit eingeschränkten Anweisungen und Werkzeugbeschränkungen definiert werden können; die genauen Felder und die Rangfolge entnimmst du der aktuellen Produktdokumentation. [Create custom subagents](https://code.claude.com/docs/en/subagents)

Bei einem System mit externen Wirkungen nutze ein Freigabe-Gate außerhalb der Diskussionsschleife:

1. der Worker erstellt einen Kandidaten und die Nachweise;
2. ein Verifier vergleicht die Nachweise mit dem Abnahmevertrag;
3. ein benannter Verantwortlicher erteilt gegebenenfalls die erforderliche Freigabe;
4. der berechtigte Executor führt die Aktion gegebenenfalls mit einem Idempotenzschlüssel aus;
5. der Workflow protokolliert den tatsächlichen Zielbeleg.

## Prüfung und Aggregation {#review-and-aggregation}

Parallele Arbeit sollte über Nachweise konvergieren, nicht über Stimmenzahlen. Der Koordinator kann unabhängig gesammelte Quellen, deterministische Testergebnisse und begrenzte Abwägungen vergleichen. Er muss „nicht nachgewiesen“ zurückgeben können, wenn kein Kandidat den Vertrag erfüllt.

Bei Sicherheits- oder Sicherheitsbedenken behalte die Vereinigung der Befunde als Triage und verifiziere jeden Befund, bevor du ihn als Fehler wertest oder ein Ziel änderst. Das NIST-Profil für generative KI bietet einen nützlichen Rahmen, um Risiko- und Governance-Nachweise über den gesamten Lebenszyklus eines Systems hinweg zu pflegen. [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Bewerte die Zerlegung {#evaluate-the-decomposition}

Ein Multi-Agenten-Workflow braucht eine Bewertung auf zwei Ebenen:

| Ebene | Frage |
|---|---|
| Rolle | erzeugt jeder Worker das erforderliche Artefakt innerhalb seiner Berechtigung? |
| System | bewahrt die Übergabe Eingaben, Randbedingungen und Nachweise bis zum Abschluss? |
| Betrieb | bleiben Wiederholungen, Fehler, Sperren und Nebenwirkungen sichtbar und wiederherstellbar? |
| Vergleich | verbessert das Team das Abnahmeergebnis der Aufgabe gegenüber einer einfacheren Baseline? |

Behalte die einfachste Anordnung bei, die den Abnahmevertrag erfüllt. Mehr Nachrichten, Rollen und Modellaufrufe können Latenz, Kosten und inkonsistenten Zustand erhöhen, ohne neue Nachweise zu liefern.

## Häufige Fehlermuster {#common-failure-modes}

- **Rollentheater:** Bezeichnungen wie „Researcher“ oder „Critic“ ersetzen einen konkreten Ein- und Ausgabevertrag.
- **Gemeinsamer veränderlicher Speicher:** Agenten überschreiben gegenseitig ihren Zustand oder behandeln Notizen als maßgeblich.
- **Delegierte Berechtigung:** Eine Übergabe wird als Freigabe zur Nutzung eines Geheimnisses oder eines Produktionsziels missverstanden.
- **Konsens als Beweis:** Mehrere Agenten wiederholen dieselbe unbelegte Behauptung.
- **Unbegrenzte Wiederholungen:** Ein fehlgeschlagener Worker startet ohne Versuchsgrenze oder Wiederherstellungsbedingung neu.
- **Kein Integrationsnachweis:** Jede Rolle besteht lokal, doch dem kombinierten Workflow fehlt ein Zielbeleg.

## Referenzen {#references}

- [Create custom subagents](https://code.claude.com/docs/en/subagents)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
