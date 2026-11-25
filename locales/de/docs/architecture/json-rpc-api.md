---
title: "JSON-RPC-API-Design"
category: reference
tags: [json-rpc, rpc, api, protocol]
level: 3
source_sha256: 08af5358e15b92b0d38a80f07f33b2c3de5a6960d368075824a7063eb3e29318
translation: machine
translated_at: '2026-10-24'
---
# JSON-RPC-API-Design {#json-rpc-api-design}

JSON-RPC ist ein leichtgewichtiges RPC-Protokoll, das in JSON kodiert wird. Der Client sendet Funktionsname und Parameter; der Server führt die Funktion aus und gibt das Ergebnis zurück. Alle Anfragen gehen an einen einzigen Endpunkt. Aktuelle Version: 2.0.

## Anfrage-/Antwortformat {#requestresponse-format}

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getMenu",
  "params": {"category": "pizza"}
}

// Success response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {"items": ["Margherita", "Pepperoni"]}
}

// Error response
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {"code": -32601, "message": "Method not found"}
}
```

Felder: `jsonrpc` (erforderlich, "2.0"), `id` (eindeutige Anfrage-ID), `method` (Funktionsname), `params` (optional).

## Standard-Fehlercodes {#standard-error-codes}

| HTTP | JSON-RPC-Code | Bedeutung |
|------|--------------|---------|
| 500 | -32700 | Parse-Fehler |
| 400 | -32600 | Ungültige Anfrage |
| 404 | -32601 | Methode nicht gefunden |
| 500 | -32602 | Ungültige Parameter |
| 500 | -32603 | Interner Fehler |
| 500 | -32099..-32000 | Benutzerdefinierte Serverfehler |

Spezifikation: https://www.jsonrpc.org/specification

## Batch-Anfragen {#batch-requests}

JSON-RPC unterstützt Batch-Anfragen nativ – mehrere Operationen in einer einzigen HTTP-Anfrage. Eleganter als REST, wo jede Operation typischerweise eine separate Anfrage erfordert.

## Vorteile {#advantages}

- **Leichtgewichtig und performant** – kompaktes JSON, schnell bei kleinen Datenmengen
- **Einfache Implementierung** – unkomplizierte Struktur, Parameter nur im Body
- **Transportunabhängigkeit** – HTTP, TCP, WebSocket
- **Native Batch-Unterstützung** – mehrere Operationen pro Anfrage

## Nachteile {#disadvantages}

- **Kein eingebautes Caching** – selbst wenn dieselben Daten zweimal angezeigt werden, ist eine neue Anfrage nötig
- **Begrenzte Fehlerbehandlung** – der Server liefert HTTP 200 auch bei Geschäftsfehlern
- **Kein Standard für komplexe Schemata** – weniger ausgereift als REST/GraphQL

## Wann verwenden {#when-to-use}

- Interne Service-zu-Service-Kommunikation
- Blockchain-Projekte (Ethereum JSON-RPC)
- IoT-APIs (Sensor -> Controller)
- Einfache offene APIs (Chat-Messenger)
- Hochperformante komplexe Operationen

## Stolperfallen {#gotchas}

- **HTTP 200 bei Fehlern** – der Client muss den Antwortkörper prüfen, nicht nur den Statuscode
- **Kein Caching** bedeutet höhere Serverlast bei wiederholten Abfragen
- **Parameterübergabe** – positionell (Array) vs. benannt (Objekt). Benannt ist lesbarer; positionell erfordert weniger Code

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] – Vergleich REST vs. JSON-RPC
- [[async-event-apis]] – WebSocket-Transport für JSON-RPC
