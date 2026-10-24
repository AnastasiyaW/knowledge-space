---
title: "Kommunikationsmuster in Microservices"
category: patterns
tags: [microservices, api-gateway, bff, cqrs, saga, event-sourcing]
level: 3
source_sha256: 982fe5e58c1aa1049184e877502bb14037faa7cdfe6ff60f0bc6e6f38588d4cf
translation: machine
translated_at: '2026-10-24'
---
# Kommunikationsmuster in Microservices {#microservices-communication-patterns}

Wie Microservices untereinander und mit externen Clients kommunizieren. Die Wahl zwischen synchroner und asynchroner Kommunikation bestimmt grundlegend das Systemverhalten, die Kopplung und die Fehlerszenarien.

## Synchrone Kommunikation (API-basiert) {#synchronous-communication-api-based}

Service A ruft die API von Service B direkt auf. Einfach, erzeugt aber starke Kopplung – wenn B langsam ist oder ausfällt, leidet A darunter.

**Protokolle:** REST, gRPC, GraphQL. Außerdem möglich: WebSocket, Webhooks, asynchrones HTTP.

## Asynchrone Kommunikation (nachrichtenbasiert) {#asynchronous-communication-message-based}

Services kommunizieren über Message Broker (RabbitMQ, Kafka). Service A sendet eine Nachricht, Service B verarbeitet sie, sobald er bereit ist. Ermöglicht lose Kopplung und unabhängigen Betrieb.

### Asynchrone Stile {#async-styles}

| Stil | Verhalten | Anwendungsfall |
|------|-----------|----------------|
| **Request/Response** | Nicht blockierend, schnelle Antwort erwartet | Service-übergreifende Abfragen |
| **Notifications** | Fire and Forget, keine Antwort | Event-Broadcasting |
| **Request/Async Response** | Antwort zu einem späteren Zeitpunkt erwartet | Lang laufende Operationen |

## API-Gateway-Muster {#api-gateway-pattern}

Zentraler Einstiegspunkt für alle externen Clients. Verbirgt die interne Systemstruktur.

**Funktionen:**
1. **Request-Routing** – leitet Anfragen an den passenden Microservice weiter
2. **Datenaggregation** – kombiniert Antworten mehrerer Services
3. **Authentifizierung** – zentrale Authentifizierung/Autorisierung
4. **Rate Limiting** – verhindert Überlastung
5. **Caching** – reduziert die Last im Backend
6. **Monitoring/Logging** – sammelt Statistiken und Request-Logs
7. **Fehlerbehandlung** – standardisierte Antworten, verbirgt interne Details

**Nachteile:** Single Point of Failure (HA erforderlich), Performance-Engpass (sämtlicher Traffic läuft darüber), Risiko einer Vendor-Lock-in-Abhängigkeit.

## Backend for Frontend (BFF) {#backend-for-frontend-bff}

Ein separates Gateway pro Client-Typ (Mobile, Web, Desktop). Jedes BFF ist auf die Bedürfnisse, Datenanforderungen und Performance-Eigenschaften seines spezifischen Clients optimiert.

**Warum BFF statt eines einzelnen Gateways:** Mobile Clients benötigen weniger Daten und ein anderes Format als Web-Clients. Ein einzelnes Gateway für alle Clients wird aufgebläht. Ein BFF hält die API jedes Clients schlank und zweckgebunden.

## API-Komposition {#api-composition}

Ein Service (meist BFF oder Gateway) aggregiert Daten aus mehreren Backend-Services über synchrone Aufrufe. Einfach, aber anfällig für Kaskadenausfälle.

## CQRS (Command Query Responsibility Segregation) {#cqrs-command-query-responsibility-segregation}

Getrennte Services für Lese- und Schreibzugriffe auf Daten. Schreib-Services enthalten die Geschäftslogik. Der Lese-Service verwaltet eine eigene, für schnelle Abfragen optimierte Datenbank, die asynchron über einen Message Broker befüllt wird.

```php
[Client] --write--> [Command Service] --event--> [Message Broker] --event--> [Read Service/Query DB]
[Client] --read---> [Read Service] --query--> [Query DB (optimized)]
```

**Wann welche Variante:**
- API-Komposition: einfache Aggregation, synchron, geringere Komplexität
- CQRS: hochlastige Systeme, komplexe Abfragen, Bedarf an Leseoptimierung, asynchrone Datensynchronisation akzeptabel

## Saga-Muster {#saga-pattern}

Koordiniert verteilte Transaktionen über mehrere Services hinweg ohne 2PC (Two-Phase Commit). Jeder Service führt eine lokale Transaktion aus und veröffentlicht Events bzw. Commands. Bei einem Fehler machen kompensierende Transaktionen die vorherigen Schritte rückgängig.

### Orchestrierung (zentralisiert) {#orchestration-centralized}
```php
[Orchestrator] --command--> [Service A] --response--> [Orchestrator]
[Orchestrator] --command--> [Service B] --response--> [Orchestrator]
[Orchestrator] --compensate--> [Service A]  (on failure)
```
- Pro: zentrale Steuerung, einfacheres Debugging, klarer Ablauf
- Contra: Single Point of Failure, Orchestrator wird komplex

### Choreografie (dezentralisiert) {#choreography-decentralized}
```php
[Service A] --event--> [Service B] --event--> [Service C]
                                     (failure) --compensating event-->
```
- Pro: kein SPOF, einfachere einzelne Services, bessere Skalierbarkeit
- Contra: schwieriger zu debuggen und zu überwachen, impliziter Workflow

## Event Sourcing {#event-sourcing}

Statt des aktuellen Zustands wird eine Folge von Events gespeichert. Jede Änderung ist ein unveränderliches Event in einem Append-only-Log. Der aktuelle Zustand ergibt sich durch das Wiederabspielen der Events.

**Vorteile:** vollständige Audit-Spur, zeitbezogene Abfragen, Event-Replay zum Debugging.
**Kosten:** höherer Speicherbedarf, zusätzliche Komplexität, eventuelle Konsistenz, Evolution des Event-Schemas.

## Circuit Breaker {#circuit-breaker}

Verhindert Kaskadenausfälle, wenn ein nachgelagerter Service ausfällt.

```php
[Closed] --failures exceed threshold--> [Open] --timeout--> [Half-Open]
  ^                                                              |
  |              success                                         |
  <--------------------------------------------------------------
```

1. **Closed** – normaler Betrieb, Anfragen werden durchgelassen
2. **Open** – Service fällt aus, Anfragen schlagen sofort fehl (Fail-Fast)
3. **Half-Open** – nach Ablauf des Timeouts werden begrenzt Anfragen zugelassen, um die Erholung zu prüfen

## Idempotenz {#idempotency}

Entscheidend für synchrone und asynchrone Muster gleichermaßen. Netzwerkfehler können doppelte Nachrichten verursachen. Services müssen Duplikate korrekt behandeln.

**Umsetzung:** eindeutige Request-IDs und Deduplizierung auf Empfängerseite. Eine idempotente Operation liefert unabhängig davon, wie oft sie aufgerufen wird, dasselbe Ergebnis.

## Fallstricke {#gotchas}

- **Synchrone Ketten** (A ruft B, B ruft C auf) bergen das Risiko kaskadierender Ausfälle – ein langsamer Service blockiert die gesamte Kette
- **Saga-Rollback** ist kein echtes Rollback – kompensierende Transaktionen können Seiteneffekte haben
- **Event Sourcing ohne Snapshots** bedeutet, dass bei jedem Lesezugriff die gesamte Event-Historie neu abgespielt wird
- **Circuit Breaker muss abgestimmt werden** – ein zu niedriger Schwellenwert führt zu Fehlalarmen, ein zu hoher bietet keinen Schutz
- **BFF pro Client-Typ** kann zu Code-Duplizierung führen – eine gemeinsame Core-Bibliothek für alle BFFs nutzen

## Siehe auch {#see-also}

- [[architectural-styles]] – Spektrum von Monolith zu Microservices
- [[message-broker-patterns]] – Pub/Sub vs. Queue, Push vs. Pull
- [[kafka-architecture]] – Event-Streaming-Plattform
- [[rabbitmq-architecture]] – Message-Queue-Broker
- [[async-event-apis]] – WebSockets, SSE, Webhooks, Nebenläufigkeit
