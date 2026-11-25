---
title: "Asynchrone und ereignisbasierte APIs"
category: reference
tags: [async, websocket, sse, webhooks, polling, concurrency, api]
level: 3
source_sha256: d558e9bd367f1be6bd172925626a6f9c51feefabf36c1126c0de8106012eab6e
translation: machine
translated_at: '2026-10-24'
---
# Asynchrone und ereignisbasierte APIs {#async-and-event-based-apis}

Asynchrone APIs ermöglichen nicht-blockierende Kommunikation. Sie sind entscheidend für Echtzeitfunktionen, langlaufende Operationen und skalierbare Architekturen.

## Vergleich: synchron vs. asynchron {#sync-vs-async-comparison}

| Merkmal | Synchron | Asynchron |
|-----------|------------|--------------|
| Ausführung | Wartet auf die Antwort | Läuft ohne Warten weiter |
| Ressourcenverbrauch | Weniger effizient (im Leerlauf während der Wartezeit) | Effizienter (parallel) |
| Skalierbarkeit | Geringer (blockierend) | Höher (parallele Verarbeitung) |
| Code-Komplexität | Einfacher, sequenziell | Komplexer, nicht-linear |
| Datenkonsistenz | Weniger Probleme | Mögliche Probleme bei der Reihenfolge |

## HTTP-basierte asynchrone Mechanismen {#http-based-async-mechanisms}

### Callback {#callback}
Der Client stellt eine URL bereit, die der Server aufruft, sobald die Antwort vorliegt.
- **Niedrige Latenz**, mittlere Komplexität
- Problem: "Callback-Hölle" bei verschachtelten Callbacks, Sicherheitsbedenken

### Polling {#polling}
Der Client sendet in regelmäßigen Abständen wiederholt Anfragen.
- **Einfache** Implementierung, hohe Latenz, hohe Serverlast
- Anwendungsfall: Monitoring-Dashboards, Nachrichten-Feeds

### Long Polling {#long-polling}
Der Server hält die Anfrage offen, bis neue Daten verfügbar sind.
- **Niedrige bis mittlere Latenz**, mittlere Serverlast
- Anwendungsfall: Chat-Apps, Live-Ergebnisse von Sportereignissen

| Merkmal | Callback | Polling | Long Polling |
|---------|----------|---------|--------------|
| Komplexität | Mittel | Einfach | Mittel |
| Latenz | Niedrig | Hoch | Niedrig bis mittel |
| Serverlast | Niedrig bis mittel | Hoch | Mittel |

## Fortgeschrittene asynchrone Technologien {#advanced-async-technologies}

### Webhooks {#webhooks}
Der Server sendet einen HTTP-POST an einen vordefinierten Client-Endpunkt, sobald ein Ereignis eintritt. Ereignisgesteuert, Polling entfällt.

**Anwendungsfälle:** Zahlungsbenachrichtigungen, CI/CD-Trigger, Abonnement-Aktualisierungen.

**Zu beachten:**
- Retry-Logik für fehlgeschlagene Zustellungen
- HMAC-Signatur zur Absicherung
- Idempotenz-Schlüssel für die Behandlung von Duplikaten

### WebSockets {#websockets}
Vollduplex-Kommunikation in beide Richtungen über eine einzelne, langlebige Verbindung. Unterstützt Text- und Binärdaten.

```php
HTTP upgrade handshake -> persistent WebSocket connection
Client <---> Server (bidirectional)
```

**Anwendungsfälle:** Echtzeit-Chat, Online-Auktionen, kollaboratives Bearbeiten, Gaming.

**Nachteile:** Komplexeres Verbindungsmanagement, zustandsbehaftete Verbindungen sind schwerer zu skalieren, Berücksichtigung von Load Balancern erforderlich.

### Server-Sent Events (SSE) {#server-sent-events-sse}
Unidirektionaler Datenstrom vom Server zum Client über HTTP. Einfacher als WebSockets.

**Anwendungsfälle:** Börsenticker, Benachrichtigungen, Live-Feeds, Fortschrittsanzeigen.

**Vorteile gegenüber WebSockets:** Funktioniert mit der standardmäßigen HTTP-Infrastruktur, automatische Wiederverbindung, einfachere Implementierung.

## Nebenläufigkeit und Konsistenz {#concurrency-and-consistency}

### Optimistic Locking (bevorzugt für Web-APIs) {#optimistic-locking-preferred-for-web-apis}

**ETag-basiert (empfohlen bei hoher Last):**
```bash
GET /resource -> ETag: "v5"
PUT /resource + If-Match: "v5"
  Success: 200 OK + new ETag
  Conflict: 412 Precondition Failed
```

**Zeitstempelbasiert (einfacher):**
```bash
GET /resource -> Last-Modified: timestamp
PUT /resource + If-Unmodified-Since: timestamp
  Conflict: 412 Precondition Failed
```

### Pessimistic Locking (bei Konflikten mit hohen Kosten) {#pessimistic-locking-for-high-cost-conflicts}
```bash
POST /resource?lock=true -> lockToken
PUT /resource + X-Lock-Token: token -> update + release
Already locked -> 409 Conflict
```

Pessimistic Locking verwenden Sie für Finanztransaktionen, bei denen Konflikte sehr kostspielig sind.

## AsyncAPI-Spezifikation {#asyncapi-specification}

Ähnlich wie OpenAPI, jedoch für ereignisgesteuerte APIs. Beschreibt Channels (Topics/Queues), Nachrichten, Schemata und Server-Bindings für Kafka, RabbitMQ, WebSocket und MQTT.

## Stolperfallen {#gotchas}

- **WebSocket hinter Load Balancern** - Sticky Sessions oder verbindungsbewusstes Routing erforderlich
- **SSE-Verbindungslimit** - Browser begrenzen die gleichzeitigen SSE-Verbindungen pro Domain (ca. 6)
- **Webhook-Sicherheit** - HMAC-Signaturen immer prüfen, Payloads niemals ungeprüft vertrauen
- **Polling-Intervall** - zu häufig verschwendet Ressourcen, zu selten führt zu veralteten Daten
- **Zeitstempel beim Optimistic Locking** - unter hoher Last nicht genau genug, ETags bevorzugen

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] - Grundlagen des HTTP-Protokolls
- [[microservices-communication]] - Muster für die Kommunikation zwischen Services
- [[message-broker-patterns]] - Kafka, RabbitMQ für asynchrone Backends
- [[api-documentation-specs]] - AsyncAPI-Spezifikation
