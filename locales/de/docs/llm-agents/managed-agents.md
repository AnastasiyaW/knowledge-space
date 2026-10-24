---
title: "Claude Managed Agents"
description: "Eine versionsbewusste Anleitung zum verwalteten Agent-Harness von Anthropic: Agent-Konfiguration, Umgebungen, Sessions, Events, Berechtigungsrichtlinien und Datengrenzen."
tags: [llm-agents, claude, managed-agents, sandboxes, permissions, orchestration]
level: 3
source_sha256: 1e19b92c130db3a7c893965c363749ff53bf025ad2a092bea883d48da5b32d40
translation: machine
translated_at: '2026-10-24'
---
# Claude Managed Agents {#claude-managed-agents}

**Stand der Prüfung: 2026-09-03.** Claude Managed Agents ist das Beta-Angebot von Anthropic für ein verwaltetes Harness für langlaufende, asynchrone Agenten-Aufgaben. Es stellt die Agent-Schleife, Umgebungen, Tool-Ausführung, persistierte Event-Historie und den Session-Lebenszyklus bereit; die Anwendung bleibt für ihre geschäftliche Autorisierung, Freigabeentscheidungen und Veröffentlichungskriterien selbst verantwortlich. [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

## Was verwaltet wird {#what-is-managed}

| Konzept | Aktuelle Bedeutung | Verantwortung der Anwendung |
|---|---|---|
| Agent | Modell, System-Prompt, Tools, MCP-Server, Skills | Konfiguration versionieren und prüfen |
| Environment | Anthropic-Cloud-Sandbox oder selbst gehostete Sandbox-Konfiguration | Datenresidenz und Netzwerkgrenze festlegen |
| Session | laufende Agent-Instanz für eine Aufgabe | erstellen, steuern, unterbrechen, Ergebnisse abgleichen |
| Events | Nachrichten, Tool-Ergebnisse, Status- und Fortschrittsdatensätze | maßgeblichen Event-Stream auswerten |

Verwaltete Infrastruktur reduziert den Aufwand für den Aufbau der Laufzeit. Sie macht einen Tool-Aufruf nicht autorisiert, ein Ergebnis nicht sachlich korrekt und eine Veröffentlichung nicht sicher freigabefähig.

## Lebenszyklus-Vertrag {#lifecycle-contract}

```text
versioned agent + reviewed environment
          -> create session
          -> send user event
          -> stream authoritative events
          -> approval / denial / interrupt as required
          -> reconcile external effects
          -> terminal receipt
```

Die Plattform unterstützt persistierte Session-Historie und Ausgaben, Server-Sent-Events-Streaming sowie Steuerung oder Unterbrechung während der Ausführung. Eine UI-Vorschau ist nicht das Protokoll: Ob eine Aufgabe tatsächlich abgeschlossen ist, entscheiden persistierte Session-Events und ein Anwendungsbeleg. [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Minimale Konfiguration {#minimum-configuration}

Man beginnt mit einer expliziten Definition nach dem Prinzip der geringsten Berechtigung:

```yaml
name: Editorial Research Agent
model:
  id: claude-opus-5
system: Draft from approved public sources. Do not publish.
tools:
  - type: agent_toolset_20260401
    default_config:
      permission_policy:
        type: always_ask
```

Die aktuelle API ist Beta und erfordert den Header `managed-agents-2026-04-01`; unterstützte SDKs setzen ihn automatisch. Das SDK fest versionieren und die aktuelle Request-Struktur vor dem Deployment testen. [Managed Agents quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Berechtigungsrichtlinie ist keine Zugriffskontrolle {#permission-policy-is-not-access-control}

Berechtigungsrichtlinien entscheiden, ob serverseitig ausgeführte Tools sofort laufen oder auf eine Freigabe warten:

| Richtlinie | Ergebnis |
|---|---|
| `always_allow` | aktiviertes Server-Tool wird ohne Bestätigung ausgeführt |
| `always_ask` | Session pausiert, bis die Anwendung Allow oder Deny zurückgibt |

Das vorgefertigte Agent-Toolset verwendet standardmäßig `always_allow`; MCP-Toolsets verwenden standardmäßig `always_ask`. Benutzerdefinierte Tools laufen in der Anwendung und benötigen daher eine eigene Autorisierungsschicht. Laufende Sessions behalten die Tool-Konfiguration, mit der sie erstellt wurden. Eine Änderung der Richtlinie wirkt sich deshalb nur auf spätere Sessions aus, sofern die Anwendung die Migration nicht ausdrücklich behandelt. [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)

Für einen Workflow mit öffentlichen Inhalten empfiehlt sich eine enge Aufteilung:

| Phase | Fähigkeit | Standard |
|---|---|---|
| Recherche | freigegebene Quellen lesen, strukturierte Notizen erstellen | erlaubt |
| Entwurf | Überarbeitungsvorschlag erstellen | erlaubt |
| Prüfung | Quellen und Entwurf prüfen | erlaubt |
| Veröffentlichung | öffentliche Wirkung erzeugen | verweigert bis zu einem konkreten Freigabe-Event |
| Wiederherstellung | Aufgabe und Beleg prüfen | erlaubt, keine neue Wirkung |

Eine Freigabe-Oberfläche muss den genauen Tool-Aufruf, die Argumente, das Zielkonto und das Ablaufdatum ausweisen. „Der Agent wurde früher freigegeben“ reicht als Nachweis für eine neue Veröffentlichung nicht aus.

## Umgebung und Datengrenze {#environment-and-data-boundary}

Eine Cloud-Sandbox sollte erst gewählt werden, wenn Folgendes dokumentiert ist:

- Netzwerk-Allowlist und Egress-Richtlinie;
- Dateien, Repository- und Artefakt-Mounts;
- welche Zugangsdaten der Session zur Verfügung stehen;
- Datenklassifizierung und Aufbewahrung;
- ob für Residenz oder Compliance eine selbst gehostete Sandbox erforderlich ist;
- wie hochgeladene Dateien und Session-Daten gelöscht werden.

Managed-Agents-Sessions sind bewusst zustandsbehaftet. Anthropic dokumentiert, dass diese Funktion im aktuellen Beta-Stadium nicht für Zero Data Retention oder die HIPAA-BAA-Abdeckung infrage kommt. Diese Grenze ist zu bewerten, bevor sensible Korpora oder Lernendendaten in eine Session gelangen. [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

## Event-Verarbeitung {#event-handling}

Events werden als Zustandsmaschine verarbeitet, nicht als Chat-Text:

1. Session-ID, Task-ID, erwartete Eingaben und aktuelle Richtlinienrevision persistieren;
2. die Aufgabe als `user.message`-Event senden;
3. Status-, Agent- und Tool-Events streamen;
4. wenn eine `always_ask`-Aktion pausiert, die konkrete Anfrage prüfen und ein Allow- oder Deny-Event senden;
5. bei einer Unterbrechung auf den protokollierten Übergang in den Idle-Zustand warten;
6. vor der Zuweisung eines Endzustands jede externe Wirkung abgleichen.

Die Preview-Deltas der Plattform dienen nur der Anzeige; das gepufferte, persistierte Event ist der maßgebliche Datensatz. [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Wann es passt {#when-it-fits}

Managed Agents eignen sich, wenn die Aufgabe von einer verwalteten Umgebung profitiert, mehrere Tool-Aufrufe über Minuten oder Stunden umfasst, persistierte Sessions erfordert oder geplant ausgeführt wird. Die Messages API oder ein lokales Harness ist die bessere Wahl, wenn die Anwendung die volle Kontrolle über Schleife, Umgebung, Datenpfad und jeden Tool-Executor braucht.

## Stolperfallen {#gotchas}

- **Das Agent-Toolset ist standardmäßig freizügig.** Der Standard ist `always_allow`. **Abhilfe:** `always_ask` konfigurieren oder nicht benötigte Tools deaktivieren, bevor jede produktive Agent-Version erstellt wird.
- **Eine MCP-Freigabe ist keine Anwendungsautorisierung.** Ein Benutzer kann ein Tool freigeben und trotzdem keine Befugnis für die geschäftliche Aktion besitzen. **Abhilfe:** Mandant, Ziel, Umfang und Freigabe am nachgelagerten Executor prüfen.
- **Eine Session im Idle-Zustand beweist keinen Erfolg.** Sie kann auf eine Bestätigung warten, unterbrochen worden sein oder eine Nebenwirkung nicht abgleichen können. **Abhilfe:** einen fachlichen Endbeleg verlangen.
- **Zustandsbehaftete Sessions behalten mehr als einen Prompt.** Historie, Sandbox-Zustand und Ausgaben gehören zur Datengrenze. **Abhilfe:** Daten klassifizieren, Aufbewahrung festlegen und Löschvorgänge überprüfen.
- **Beta-Oberflächen entwickeln sich weiter.** Ein kopierter Quickstart kann veralten. **Abhilfe:** Abhängigkeiten fixieren, den aktuellen Beta-Header dokumentieren und nach Änderungen einen kontrollierten Canary-Lauf durchführen.

## Quellen {#sources}

- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Claude Managed Agents quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Siehe auch {#see-also}

- [[agent-orchestration]]
- [[agent-safety-alignment]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
