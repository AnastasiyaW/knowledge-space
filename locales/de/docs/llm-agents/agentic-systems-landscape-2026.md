---
title: "Landschaft agentischer Systeme (September 2026)"
description: "Protokollgrenzen, Laufzeitentscheidungen und Kontrollebenen-Muster für den Produktiveinsatz agentischer Systeme; geprüft am 2026-09-03."
level: 3
source_sha256: 7f059e9e0243ea8b32639b80fb3be82ed0567e293498b354e9632cf021d89a77
translation: machine
translated_at: '2026-10-24'
---
# Landschaft agentischer Systeme (September 2026) {#agentic-systems-landscape-september-2026}

Geprüft am 2026-09-03. Betrachten Sie ein Agentensystem als Anwendungs-Kontrollebene rund um probabilistische Modellaufrufe und nicht als Sammlung autonomer Personas. Die dauerhaften Einheiten sind Verträge, Zustand, Berechtigungen, Nachweise und Rollback-Grenzen.

## Protokollgrenzen {#protocol-boundaries}

| Grenze | Verwendung für | Verantwortet den Lebenszyklus | Nicht verwenden als |
|---|---|---|---|
| MCP | Anbindung eines anwendungsgehosteten Agenten an Werkzeuge, Datenquellen und Kontextanbieter | Die Host-Anwendung | Allgemeine Workflow-Engine für Agent-zu-Agent-Kommunikation |
| A2A | Austausch von Aufgaben und Ergebnissen zwischen separat betriebenen Agenten | Jeder beteiligte Agent bzw. Dienst | Ersatz für Werkzeugautorisierung oder lokale Funktionsaufrufe |
| Anwendungs-API | Interne Aufrufe zwischen Komponenten, die gemeinsam ausgeliefert werden | Ihre Anwendung | Öffentliches Interoperabilitätsprotokoll ohne Kompatibilitätsvertrag |

MCP beschreibt eine Host-Client-Server-Architektur: Der Host erzeugt Clients, steuert Berechtigungen und verwaltet den Lebenszyklus. [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

A2A ist ein Interoperabilitätsprotokoll für die Kommunikation zwischen Agenten. Es ergänzt MCP, ersetzt es aber nicht: Ein Agent kann MCP nutzen, um seine Werkzeuge zu erreichen, und A2A, um Arbeit mit einem anderen Agenten auszutauschen. [A2A specification](https://a2a-protocol.org/latest/)

## Wahl der Laufzeit {#runtime-choice}

Wählen Sie die kleinste Laufzeit, die die benötigte Kontrolle bietet.

| Bedarf | Geeigneter Ausgangspunkt | Erforderliche Kontrolle |
|---|---|---|
| Eine begrenzte Aufgabe mit wenigen Werkzeugen | Eine Agentenschleife im Anwendungscode | Werkzeugschemata, Fristen, strukturierte Endausgabe |
| Ein Spezialist unterstützt einen Manager | Manager ruft Spezialisten als Werkzeug auf | Der Manager bleibt alleinige Instanz für die Endausgabe |
| Der Nutzer soll mit einem Spezialisten weiterarbeiten | Expliziter Handoff | Routing-Regel, für den Nutzer sichtbare Zuständigkeit, Kontextvertrag |
| Unabhängige Arbeitseinheiten | Deterministisches Fan-out und Fan-in | Idempotenzschlüssel, Parallelitätsobergrenze, Reducer |
| Lang laufende oder wiederaufnehmbare Arbeit | Dauerhafter Workflow bzw. Zustandsspeicher | Checkpoints, Lease, Wiederholungsrichtlinie, abschließender Beleg |

Das OpenAI Agents SDK dokumentiert zwei unterschiedliche Kompositionsmuster: Spezialisten, die als Werkzeuge genutzt werden, lassen einen Manager die Kontrolle behalten, während Handoffs die aktive Konversation an einen Spezialisten übergeben. Die Anleitung unterscheidet außerdem zwischen modellgesteuerter und codegesteuerter Orchestrierung. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

Verwaltete Laufzeiten können die Verantwortung für die Infrastruktur verringern, heben jedoch nicht die Notwendigkeit auf, Datenzugriff, Freigabe, Validierung der Ausgaben und Incident-Behandlung zu definieren. Claude Managed Agents etwa modelliert einen Agenten als versionierte Konfiguration zusammen mit einer Umgebung und einer Session. [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Kontrollebene für den Produktiveinsatz {#production-control-plane}

Ein Agentenaufruf sollte genau einen dauerhaften Datensatz besitzen. Speichern Sie Referenzen auf große Ein- und Ausgaben, statt sie durch jeden Prompt zu kopieren.

```json
{
  "run_id": "run_01J...",
  "work_item_id": "news-2026-09-03-001",
  "parent_run_id": null,
  "attempt": 1,
  "input_ref": "s3://private-bucket/intake/001.json",
  "agent_version": "news-curator@2026-09-03",
  "tool_policy_id": "news-read-only-v3",
  "status": "running",
  "output_ref": null,
  "evidence": [],
  "idempotency_key": "news-2026-09-03-001:curate:v3"
}
```

### Verbindliche Invarianten {#required-invariants}

- Jede veränderliche Datenstruktur gehört genau einer Komponente. Worker dürfen Nachweise anhängen, aber nur der Workflow-Controller ändert den Endstatus.
- Ein Wiederholungsversuch verwendet dieselbe Arbeitseinheit und eine neue Versionsnummer. Er erzeugt niemals stillschweigend einen zweiten Veröffentlichungskandidaten.
- Ein Werkzeugaufruf besitzt eine auf der Positivliste stehende Fähigkeit, eine Frist, eine Identität des Aufrufers und einen Beleg. Unbekannte Ergebnisse von Werkzeugaufrufen führen zum sicheren Abbruch (fail closed).
- Eine generierte Antwort ist kein Beleg. Ein Beleg identifiziert Eingabe, Version von Agent und Konfiguration, Werkzeugergebnisse, Ergebnis der Validierung und Zeitstempel.
- Die öffentliche Veröffentlichung ist nach der Prüfung ein eigener Zustandsübergang. Setzen Sie erfolgreiche Extraktion nicht mit Freigabe gleich.

## Reihenfolge beim Aufbau {#build-order}

1. Implementieren Sie einen Einzelagenten-Pfad mit typisierter Eingabe und typisierter Ausgabe.
2. Ergänzen Sie deterministische Validierung, bevor Sie einen weiteren Agenten hinzufügen.
3. Fügen Sie einen separat abgegrenzten Evaluator hinzu, wenn eine fehlerhafte Ausgabe erheblich kostspielig ist.
4. Fügen Sie parallele Worker nur für unabhängige, partitionierte Arbeitseinheiten hinzu.
5. Ergänzen Sie dauerhafte Wiederherstellung erst, wenn die Arbeit einen einzelnen Prozess überdauern kann.
6. Setzen Sie serviceübergreifendes A2A erst ein, wenn unabhängig verantwortete Agenten eine stabile Interoperabilitätsgrenze benötigen.

Diese Reihenfolge hält die Fehlerfläche beobachtbar. Ein Multi-Agenten-Design ist durch einen konkreten Bedarf an unabhängiger Arbeit, Trennung von Zuständigkeiten oder einer anderen Vertrauensgrenze gerechtfertigt, nicht durch eine Rollenbezeichnung.

## Modell- und Werkzeugrouting {#model-and-tool-routing}

Routen Sie anhand des Vertrags, nicht anhand einer Produktbezeichnung.

| Arbeitsklasse | Routing-Kriterium | Beispiel für einen Validator |
|---|---|---|
| Extraktion | Schema ist bekannt | JSON-Schema- und Quellenreferenzprüfungen |
| Klassifikation | Erlaubte Labels sind endlich | Enum-Validierung und Konfidenzrichtlinie |
| Entwurf | Menschliche Prüfung ist erforderlich | Redaktionelle Checkliste und Freigabeprotokoll |
| Codeänderung | Repository-Zustand ist maßgeblich | Gezielter Test plus Diff-Prüfung |
| Externe Aktion | Nebenwirkung ist erheblich | Explizite Freigabe und Idempotenzschlüssel |

Verwenden Sie modellgesteuertes Routing nur dann, wenn die Route selbst eine offene Denkaufgabe ist. Verwenden Sie Anwendungscode, wenn die Route eine Richtlinienentscheidung, eine Autorisierungsgrenze oder ein Budgetlimit darstellt.

## Wann kein Agent hinzugefügt werden sollte {#when-not-to-add-an-agent}

Fügen Sie keinen Spezialisten nur hinzu, um einen Prompt umzubenennen. Behalten Sie einen einzelnen Agenten bei, wenn:

- die Aufgabe sequenziell ist und dieselben Berechtigungen durchgängig gelten;
- das Ergebnis einen einzigen deterministischen Validator hat;
- das Teilen des vollständigen Kontexts günstiger und sicherer ist als dessen Serialisierung zwischen Agenten;
- kein unabhängiger Prüfer und keine externe Vertrauensgrenze benötigt wird.

Aufgabenteilung bringt Kontextverlust, zusätzliche Kosten, mehr Traces zur Auswertung und an jedem Handoff eine weitere Fehlerquelle mit sich.

## Fallstricke {#gotchas}

- **Problem: MCP und A2A werden als austauschbar behandelt.** Die Autorisierung bei MCP liegt an der Grenze zwischen Host und Werkzeug; A2A regelt die Kommunikation zwischen Agenten. **Lösung:** Dokumentieren Sie beide Grenzen getrennt und verwenden Sie das Protokoll, das die jeweilige Beziehung verantwortet.
- **Problem: Ein Modell entscheidet über eine richtlinienpflichtige Route.** Eine Anweisung in natürlicher Sprache ist kein Autorisierungssystem. **Lösung:** Halten Sie Budgets, Veröffentlichungsfreigaben und Sperren für destruktive Aktionen in deterministischem Anwendungscode.
- **Problem: Wiederholung mit einer neuen Identität.** Ein Timeout kann eine externe Nebenwirkung unbestimmt lassen. **Lösung:** Speichern Sie einen Idempotenzschlüssel und gleichen Sie den vorherigen Versuch ab, bevor Sie erneut senden.
- **Problem: Eine Modellantwort wird als Abschluss gewertet.** Eine flüssige Antwort kann erforderliche Nachweise auslassen. **Lösung:** Lassen Sie den Workflow erst dann enden, wenn der Validator einen PASS-Beleg protokolliert hat.

## Grenzen {#limitations}

Protokolle machen Grenzen explizit; sie machen Agenten nicht zuverlässig, sicher oder gegenseitig vertrauenswürdig. Werkzeugverhalten, Quellenqualität, Nicht-Determinismus des Modells und Prüfrichtlinien bleiben Aufgabe der Anwendung. Testen Sie den tatsächlichen Workflow mit repräsentativen Fehlerfällen, bevor Sie die Autonomie erhöhen.

## Siehe auch {#see-also}

- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]
- [[llmops]]

## Quellen {#sources}

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [Claude Managed Agents Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
