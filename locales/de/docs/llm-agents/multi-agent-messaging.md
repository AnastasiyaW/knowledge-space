---
title: "Nachrichtenaustausch und Koordination mehrerer Agenten"
description: "Wählen Sie die richtige Grenze für Agent-zu-Agent-Arbeit, Tool-Zugriff, dauerhafte Nachrichten, Empfangsbestätigungen und gleichzeitige Repository-Änderungen."
tags: [llm-agents, multi-agent, messaging, a2a, mcp, coordination, observability]
level: 3
source_sha256: 42ce38c4b865e34f3fc39a7f4004e9f180002b736b1742d5ab8427f75e3363c6
translation: machine
translated_at: '2026-10-24'
---
# Multi-Agent-Messaging und Koordination (September 2026) {#multi-agent-messaging-and-coordination-september-2026}

Versionskontext: Agent-Runtimes, IDE-Funktionen, Protokollrevisionen und Transport-Adapter entwickeln sich schnell. Diese Seite beschreibt dauerhafte Koordinationsverträge und behauptet nicht, dass ein bestimmtes Client-Flag, Plugin, Broker, Polling-Intervall oder experimentelles Feature allgemein verfügbar ist.

Kommunikation ist nur ein Teil der Koordination. Ein zuverlässiges System unterscheidet zwischen einer Nachricht, einem Aufgabenzustand, einer Autoritätsentscheidung, einem gemeinsam genutzten Artefakt und einer exklusiven Sperre. Wenn all diese Elemente als Chattext behandelt werden, sind doppelte Ausführung und nicht überprüfbare Abschlüsse wahrscheinlich.

## Die richtige Grenze wählen {#choose-the-correct-boundary}

| Bedarf | Geeignete Primitive | Was sie nicht beweist |
|---|---|---|
| Ein Agent benötigt ein Tool, eine API oder eine Datenressource | MCP-Client/Server-Grenze | dass ein anderer unabhängiger Agent eine Aufgabe angenommen hat |
| Ein Agent delegiert ein Ziel an einen unabhängigen Agenten | A2A oder ein anwendungsspezifisches Aufgabenprotokoll | dass ein Seiteneffekt sicher abgeschlossen wurde |
| Zwei lokale Sitzungen teilen Projektwissen | versioniertes Artefakt, Übergabe oder Repository-Referenz | exklusiven Besitz einer veränderlichen Ressource |
| Genau ein Worker darf eine Ressource verändern | Lease oder Sperre mit externer Abstimmung | dauerhafte Zustellung einer Nachricht |
| Ein Reviewer benötigt Nachweise | unveränderlicher Beleg, der von der Aufgabe verlinkt wird | dass die Beschreibung des Absenders korrekt war |

Die aktuelle A2A-Dokumentation beschreibt A2A als Agent-zu-Agent-Kommunikation und MCP als Agent-zu-Tool-Kommunikation. Beide ergänzen sich: Ein Agent kann MCP-Tools nutzen, während er über A2A mit einem anderen Agenten zusammenarbeitet. [A2A-Protokoll](https://a2a-protocol.org/latest/)

MCP selbst verwendet eine Host-Client-Server-Architektur. Der Host verwaltet Verbindungen, Richtlinien, Zustimmung und Benutzerautorisierung. Ein MCP-Server gewährt einem entfernten Agenten nicht automatisch Befugnisse über Ressourcen eines Benutzers. [MCP-Architektur](https://modelcontextprotocol.io/specification/latest/architecture)

## Ein dauerhaftes Nachrichten-Envelope {#a-durable-message-envelope}

Verwenden Sie ein typisiertes Envelope mit Idempotenzschlüssel, Routing-Metadaten, Ablaufzeit und Referenzen auf kontrollierte Artefakte. Legen Sie keine Anmeldedaten, unbeschränkten Anweisungen oder rohen privaten Kontext in das Envelope.

```json
{
  "schema_version": "agent-message/v1",
  "message_id": "msg_01...",
  "trace_id": "tr_01...",
  "idempotency_key": "research:source-set-44:v1",
  "sender": {"agent_id": "researcher@release-12", "role": "research"},
  "recipient": {"queue": "editorial-review", "role": "review"},
  "intent": "review_claim_set",
  "allowed_actions": ["read_artifact", "write_review_receipt"],
  "input_refs": ["artifact:claim-set-44"],
  "expires_at": "2026-09-04T12:00:00Z",
  "sent_at": "2026-09-03T12:00:00Z"
}
```

Der Empfänger validiert Schema, Identität, Ablaufzeit, erlaubte Aktionen und Artefaktzugriff, bevor er Arbeit annimmt. Der Absender kann Berechtigungen nicht allein dadurch gewähren, dass er sie in eine Nachricht schreibt.

## Aufgabe und Zustellung getrennt modellieren {#model-the-task-separately-from-delivery}

Eine Transport-Bestätigung bedeutet nur, dass eine Nachricht den Transport erreicht hat. Sie ist kein Beleg dafür, dass der Empfänger sie gelesen, die Befugnis dazu hatte, sie abgeschlossen oder ein gültiges Ergebnis erzeugt hat.

Verfolgen Sie Aufgabenzustand und Verifikation getrennt. Eine Aufgabe hat sich gegenseitig ausschließende Endzustände. Die Verifikation ist eine Prüfung des Endbelegs und kein weiterer Aufgabenübergang.

```text
non-terminal task states: PENDING -> ACCEPTED -> RUNNING
terminal task state: COMPLETED | FAILED | CANCELLED
verification receipt: PENDING -> VERIFIED | REJECTED
```

Jeder Aufgabenübergang trägt einen passenden Beleg. Ein Endzustand erfordert einen Endbeleg:

- **ACCEPTED:** Empfängeridentität, angenommener Umfang, Frist und Aufgabenrevision;
- **COMPLETED:** Referenz auf das Ausgabeartefakt, Validierungsergebnis sowie Beleg über keinen Seiteneffekt bzw. über den Seiteneffekt;
- **FAILED:** klassifizierter Fehler, Wiederholbarkeit, gesicherte Nachweise und nächster sicherer Schritt;
- **CANCELLED:** Akteur, Grund und Abstimmungsergebnis für jeden laufenden Effekt;
- **Verifikationsbeleg:** unabhängige Kriterienversion, Identität des Reviewers und Urteil.

Eine Abbruchanforderung kann aus jedem nicht-endgültigen Zustand erfolgen. Wenn eine Nachricht zu einer Zahlung, Veröffentlichung, Bereitstellung oder einem anderen externen Effekt führen könnte, benötigt dieser Effekt eine eigene Autorisierung auf Anwendungsebene und einen eigenen Idempotenzschlüssel.

## Transportoptionen {#transport-choices}

| Transport | Gute Eignung | Vertrag, den Sie selbst ergänzen müssen |
|---|---|---|
| Append-only-Dateien | lokale, nachvollziehbare Übergaben und asynchrone Recherche | atomares Schreiben, Schemavalidierung, Ablaufzeit, Beleg über Verarbeitung |
| Queue oder Datenbank | Wiederholungen, Backpressure, viele Worker | Deduplizierung, Lease, Dead-Letter-Richtlinie, Endzustands-Aufzeichnung der Aufgabe |
| A2A-Endpunkt | interoperable Delegation zwischen unabhängigen Agentensystemen | Autorisierung auf Anwendungsebene, lokales Arbeitsprotokoll, Effektkontrollen |
| Direkter Prozessaufruf | begrenzte In-Process-Teilaufgabe | Timeout, Abbruch, Ergebnisvalidierung, Beleg beim Elternprozess |

Beginnen Sie mit dem kleinsten Transport, der die benötigten Nachweise erhält. Ein repository-gestütztes Artefakt ist für Recherche, Planung oder Review oft stärker als eine Echtzeitnachricht, weil alle Empfänger dieselbe versionierte Eingabe erhalten.

## Empfangene Inhalte als nicht vertrauenswürdige Eingaben behandeln {#treat-received-content-as-untrusted-input}

Eine Agentennachricht, eine abgerufene Datei, ein Tool-Ergebnis oder ein Issue-Kommentar kann Anweisungen enthalten, die der Richtlinie des Empfängers widersprechen. Ein Empfänger sollte:

1. das Envelope parsen, ohne seinen Freitext auszuführen;
2. Artefaktreferenzen über einen zugriffskontrollierten Speicher auflösen;
3. seine eigene Aufgaben- und Autorisierungsrichtlinie anwenden;
4. Tools auf die deklarierte und lokal genehmigte Aktionsmenge beschränken;
5. die Ausgabe gegen den Aufgabenvertrag validieren;
6. einen Endbeleg schreiben, bevor er den Absender benachrichtigt.

So wird Delegation zu einer kontrollierten Schnittstelle und nicht zu einem Tunnel für Prompt-Injection.

## Gleichzeitige Repository-Arbeit koordinieren {#coordinate-concurrent-repository-work}

Bei Code- oder Dokumentationsänderungen weisen Sie jedem Pfad bzw. jeder Feature-Grenze genau einen Schreiber zu. Verwenden Sie pro Schreiber einen eigenen Branch und ein eigenes Worktree und tauschen Sie nur Commit-Referenzen, Review-Artefakte und abgegrenzte Änderungsanfragen aus. Git-Worktrees sind dafür ausgelegt, mehrere Arbeitsbäume an ein Repository anzubinden. [git-worktree](https://git-scm.com/docs/git-worktree)

Eine knappe Übergabe sollte Folgendes benennen:

```text
objective + scope + base commit + branch + changed paths
+ verification commands + receipts + known gaps + owner
```

Ein gemeinsames Chat-Protokoll ist kein Integrationsartefakt. Es hat keine unveränderliche Basisrevision, keine Merge-Semantik und keine Garantie, dass ein späterer Leser die richtige Eingabe sieht.

## Observability {#observability}

Versehen Sie jede Nachricht, jede Aufgabe und jedes Ergebnis mit einer gemeinsamen Trace-ID. Messen Sie Warteschlangenalter, Verzögerung bis zur Annahme, Ausführungsdauer, Wiederholungen, Schemafehler, Autorisierungsablehnungen und verifizierte Endergebnisse. Messen Sie nicht nur den Nachrichtendurchsatz: Eine schnelle Queue, die Belege verliert, ist kein funktionierendes Koordinationssystem.

## Fallstricke {#gotchas}

- **Zustellung ist kein Abschluss.** Eine Broker-Bestätigung sagt nichts über die Arbeit des Empfängers aus. **Abhilfe:** Verlangen Sie einen Zustand „accepted“ und einen separaten Endbeleg.
- **Eine Sperre ist keine Nachrichtenwarteschlange.** Sie kann parallele Schreiber ausschließen, aber keine Aufgabenbeschreibung oder kein Ergebnis bewahren. **Abhilfe:** Behandeln Sie Sperren, Nachrichten und Aufgabenaufzeichnungen als getrennte Primitive.
- **Ein Absender kann keine Befugnis delegieren, die er nicht besitzt.** Die in einer Nachricht deklarierten Berechtigungen sind nur eine Anfrage. **Abhilfe:** Autorisieren Sie unabhängig beim Empfänger und an jeder wirksamen Tool-Grenze.
- **Polling-Intervalle sind keine Zuverlässigkeitsgarantien.** Ein Prozess kann schlafen, abgestürzt sein oder veraltete Daten lesen. **Abhilfe:** Verwenden Sie dauerhaften Zustand, Ablaufzeiten und Abstimmung statt zeitlicher Annahmen.
- **Vollständige Kontext-Dumps sind ein Zugriffskontrollversagen.** Sie verbreiten private Inhalte und erschweren die Prüfung der Relevanz. **Abhilfe:** Senden Sie eng gefasste Artefaktreferenzen mit Herkunftsnachweis und einem richtliniengesteuerten Leser.

## Quellen {#sources}

- [A2A-Protokoll](https://a2a-protocol.org/latest/)
- [Model Context Protocol – Architektur](https://modelcontextprotocol.io/specification/latest/architecture)
- [Dokumentation zu git worktree](https://git-scm.com/docs/git-worktree)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Siehe auch {#see-also}

- [[multi-session-coordination]]
- [[agent-orchestration]]
- [[agent-design-patterns]]
- [[agent-security]]
- [[agent-observability-dashboards]]
- [[llmops]]
