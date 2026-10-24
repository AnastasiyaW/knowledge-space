---
title: "Agent-Entwurfsmuster"
description: "Begrenzte Kontrollfluss-Muster für LLM-Systeme auswählen: direkte Tools, ReAct, Pläne, Zustandsautomaten und Spezialisten-Übergaben"
level: 3
source_sha256: 10ea5509dcc00d4f660247200511dced99b7128863072a7e6a83d210bcba895d
translation: machine
translated_at: '2026-10-24'
---
# Agent-Entwurfsmuster (September 2026) {#agent-design-patterns-september-2026}

Versionskontext: Muster sind architektonische Entscheidungen, keine Framework-Funktionen. Fixieren Sie das Modell, die Tool-Schemata, die Richtlinienrevision und die Evaluierungs-Suite, die ein produktiv eingesetzter Ablauf verwendet.

Ein gutes Agent-Muster macht die Entscheidungsgrenze explizit: Das Modell darf die nächste Aktion vorschlagen, während deterministischer Code entscheidet, ob diese Aktion erlaubt ist, das Ergebnis protokolliert und den Endzustand wählt.

## So wenig Agentik wie möglich {#start-below-agency}

Verwenden Sie die am wenigsten dynamische Form, die die Aufgabe erfüllt:

| Form | Modell entscheidet | System entscheidet |
|---|---|---|
| Direkter Tool-Aufruf | Nichts über den Eingabeinhalt hinaus | Tool, Parameter, Autorisierung, Antwort |
| Feste Workflow | Inhalt innerhalb eines bekannten Schritts | Schrittreihenfolge, Wiederholungen, Zustandsübergänge |
| Begrenzte ReAct-Schleife | Nächster erlaubter Lese- bzw. Denkschritt | Tool-Allowlist, Budget, Terminierung |
| Planen und ausführen | Kandidatenplan und Anfrage zur Neuplanung | Planvalidierung, Schrittausführung, Freigabe |
| Spezialisten-Übergabe | Geeigneter, autorisierter Spezialist | Identität, Projektion des Verlaufs, Fähigkeit |
| DAG | Knotenlokaler Vorschlag | Abhängigkeiten, Joins, Nebenläufigkeit, Belege |

Ein fester Workflow ist in der Regel leichter zu testen und sicherer zu betreiben. Fügen Sie eine Agent-Schleife nur hinzu, wenn der nächste Schritt tatsächlich von Informationen abhängt, die sich vorab nicht aufzählen lassen.

## Begrenztes ReAct {#bounded-react}

Das ReAct-Paper beschreibt das Verschränken von Denkspuren mit Aktionen und Beobachtungen. In der Produktion sollten Sie die rohe Begründung des Modells weder als Audit-Protokoll noch als Berechtigung behandeln. Speichern Sie stattdessen strukturierte Aktionsvorschläge und Tool-Belege.

```text
input -> model proposes an allowed action -> policy validates
      -> tool executes -> receipt persists -> next state or terminal result
```

Jede Schleife braucht eine Abbruchbedingung: ausreichende Belege, unzureichende Informationen, abgelehnte Aktion, erschöpftes Versuchs-, Kosten- oder Zeitbudget oder erforderliche externe Freigabe.

## Vertrag für Aktionsvorschläge {#action-proposal-contract}

Verlangen Sie vom Modell ein Schema, das unabhängig von jedem Provider-SDK ist:

```json
{
  "action": "search_documents",
  "arguments": {"query": "invoice INV-42"},
  "purpose": "find the authorized invoice record",
  "expected_receipt": "document-list-v1"
}
```

Das `purpose` ist eine für Betreiber sichtbare Zusammenfassung und keine verborgene Gedankenkette. Die Richtlinienschicht prüft Aktionsname, Argumentschema, Akteursbereich und verbleibendes Budget, bevor ein Tool läuft.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionProposal:
    action: str
    arguments: dict[str, Any]
    purpose: str


ALLOWED_ACTIONS = {"search_documents", "get_invoice"}


def authorize(proposal: ActionProposal, remaining_steps: int) -> None:
    if remaining_steps <= 0:
        raise RuntimeError("step budget exhausted")
    if proposal.action not in ALLOWED_ACTIONS:
        raise PermissionError(f"action is not allowed: {proposal.action}")
    if not proposal.purpose.strip():
        raise ValueError("operator-visible purpose is required")
```

## Planen und Ausführen {#plan-and-execute}

Ein Plan ist eine veränderliche Hypothese, kein Befehl. Verwenden Sie einen Plan, wenn:

- die Aufgabe mehrere voneinander abhängige Ziele hat;
- ein Betreiber einen vorgeschlagenen Ansatz vor Seiteneffekten prüfen muss;
- Zwischenergebnisse eine autorisierte Neuplanung auslösen können;
- jeder Schritt einen Beleg und einen definierten Fehlerzustand erzeugen kann.

Halten Sie Planung und Ausführung getrennt. Validieren Sie einen Plan unmittelbar vor jedem Schritt gegen aktuelle Berechtigungen und Fakten; führen Sie niemals einen alten Plan blind aus, nachdem sich Tools, Daten oder Richtlinien geändert haben.

## Reflexion und Verifikation {#reflection-and-verification}

Ein Modellaufruf zur Selbstkritik kann nützliche Hypothesen liefern, ist aber keine Verifikation. Verwenden Sie ihn, um Prüfkandidaten zu erzeugen, und führen Sie dann deterministische Tests, Quellenabruf, Schemavalidierung oder einen unabhängigen Evaluator aus.

| Bedarf | Geeigneter Mechanismus |
|---|---|
| JSON / typisierte Ausgabe validieren | Schema-Validator |
| Berechnung verifizieren | Deterministischer Code |
| Quellenbehauptung verifizieren | Abgerufene Primärquelle mit Zitat |
| Codeänderung verifizieren | Test/Build plus unabhängiges Review |
| Alternative Strategie erzeugen | Modellkritik oder Planer |
| Hochwirksame Aktion freigeben | Autorisierter Mensch oder Richtliniendienst |

## Tool-Erkennung und -Komposition {#tool-discovery-and-composition}

Dynamische Tool-Erkennung vergrößert die Angriffsfläche und den Entscheidungsraum des Modells. Bevorzugen Sie eine kleine, aufgabenbezogene Allowlist. Falls Erkennung nötig ist, behandeln Sie Tool-Metadaten als nicht vertrauenswürdig, bis Identität, Schema, Berechtigungen und Seiteneffektklasse geprüft sind.

Tool-Komposition benötigt an jeder Kante einen Vertrag: Ausgabeschema, Mandanten- und Akteursbereich, Fehlerverhalten, Frist, Idempotenzschlüssel und Beleg. Eine Beobachtung ohne Herkunftsnachweis darf keinen schreibenden Schritt auslösen.

## Übergaben {#handoffs}

Eine Übergabe ist angebracht, wenn eine eigenständige Fähigkeit oder Zuständigkeit die nächste Aufgabe verantwortet. Sie muss eine typisierte Anfrage, eine freigegebene Kontextprojektion, eine Frist, eine Trace-Referenz und einen definierten Verantwortlichen für die finale Antwort enthalten.

Übergeben Sie standardmäßig nicht die gesamte Unterhaltung an einen Spezialisten. Reduzieren Sie sie auf die Fakten und Artefakte, die der Spezialist sehen darf.

## Checkliste zur Musterauswahl {#pattern-selection-checklist}

1. Legen Sie das Endergebnis und die Belege fest, die es als abgeschlossen ausweisen.
2. Identifizieren Sie jeden Seiteneffekt und jede Autorisierungsgrenze.
3. Implementieren Sie den kürzesten deterministischen Workflow, der die Aufgabe erfüllt.
4. Fügen Sie eine begrenzte Agent-Entscheidung nur dort hinzu, wo der nächste Schritt wirklich unbekannt ist.
5. Instrumentieren Sie Aktionsvorschläge, Richtlinienentscheidungen, Tool-Belege und Stoppgrund.
6. Evaluieren Sie den gesamten Ablauf anhand repräsentativer und adversarieller Fälle.

## Fallstricke {#gotchas}

- **Ein vom Modell erzeugter Plan kann veralten.** Tool-Ausgaben und Berechtigungen ändern sich nach der Planung. **Abhilfe:** Unmittelbar vor jeder Aktion autorisieren und validieren, dann auf Basis aktueller Belege neu planen.
- **Rohe Begründung ist keine Sicherheitskontrolle.** Sie kann unvollständig, sensibel oder irreführend sein. **Abhilfe:** Strukturierte Vorschläge, Richtlinien und Belege speichern, statt sich auf verborgenen Begründungstext zu verlassen.
- **Reflexion kann denselben Fehler verstärken.** Dasselbe Modell kann eine falsche Antwort rationalisieren. **Abhilfe:** Unabhängige deterministische Prüfungen oder einen separat kalibrierten Evaluator verwenden.
- **Dynamische Erkennung ist keine Autorisierung.** Ein angebotenes Tool kann ungeeignet oder bösartig sein. **Abhilfe:** Identität, Schema und aufgabenbezogene Berechtigungsprüfungen außerhalb des Modells erzwingen.

## Quellen {#sources}

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenAI model guidance: tool orchestration](https://developers.openai.com/api/docs/guides/latest-model)

## Siehe auch {#see-also}

- [[agent-fundamentals]]
- [[agent-architectures]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
