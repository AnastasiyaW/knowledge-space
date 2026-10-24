---
title: "Anwendungsarchitektur"
category: concepts
tags: [nodejs, architecture, ddd, layers, transport, context-isolation, server-structure]
level: 3
source_sha256: 87dfd82c028d8beaead5a4502d949b620488e886714576a8802269fc6246bf2a
translation: machine
translated_at: '2026-10-24'
---
# Anwendungsarchitektur {#application-architecture}

Die Architektur von Node.js-Anwendungen basiert auf Schichtentrennung, Transport-Abstraktion und Kontextisolation. Die DDD-inspirierte Struktur hält die Geschäftslogik rein, transport-agnostisch und schemagesteuert. Die größte Herausforderung für Entwickler sind nicht Framework-Wissen oder asynchrone Muster, sondern die Strukturierung der Anwendung.

## Wichtige Fakten {#key-facts}

- Die Geschäftslogik muss rein sein: keine I/O-Operationen, keine Framework-Abhängigkeiten
- Die Transportschicht unterscheidet sich nur darin, wie Daten gesendet und empfangen werden (HTTP vs. WebSocket vs. gRPC)
- Schemagesteuerte Entwicklung: Schemas zuerst definieren, dann DB-Tabellen, Validatoren, Typen, Dokumentation und SDKs generieren
- Schemas als single source of truth verhindern Abweichungen zwischen den Schichten
- Die Konfiguration bestimmt den Transport zur Laufzeit, was A/B-Tests verschiedener Protokolle ermöglicht
- Dieselbe Chat-Anwendung, implementiert in Pure Node.js, Fastify, NestJS und Metarhia, zeigt: Die Domänenlogik bleibt identisch, nur das Framework-Boilerplate unterscheidet sich

## Vier Kontextebenen {#four-context-levels}

Node.js-Server benötigen isolierten Zustand auf vier Ebenen mit unterschiedlicher Lebensdauer:

```text
Application Context (global, persistent)
  └─ Session Context (per-user, persistent, TTL)
      └─ Connection Context (per-socket, transient)
          └─ Call Context (per-request, shortest-lived)
```

1. **Aufruf-Kontext** – ein Request bzw. ein RPC-Aufruf. Request- und Response-Objekte. Wird nach der Antwort zerstört
2. **Verbindungs-Kontext** – eine TCP- bzw. WebSocket-Verbindung. Metadaten. Wird beim Verbindungsabbau zerstört
3. **Sitzungs-Kontext** – bleibt über mehrere Verbindungen hinweg bestehen (gestützt durch eine DB). Authentifizierung, konfigurierbare TTL
4. **Anwendungs-Kontext** – globales Singleton. Konfiguration, Caches, Connection-Pools

### Implementierung mit privaten Feldern {#implementation-with-private-fields}

```js
class Context {
  #session;
  #connection;
  #call;

  constructor(session, connection) {
    this.#session = session;
    this.#connection = connection;
  }

  startCall(request) {
    this.#call = { request, startTime: Date.now() };
    return this;
  }
}
```

Ab Node.js 16 gilt: Verwenden Sie die `#privateField`-Syntax anstelle von Closures oder symbolbasierter Privatsphäre.

## Muster {#patterns}

### Transport-Abstraktion {#transport-abstraction}

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js
const transport = require(`./${config.transport}.js`);
// Domain logic is transport-agnostic
```

### Kontext pro Request (Fastify) {#per-request-context-fastify}

```js
fastify.addHook('preHandler', (request) => {
  request.context = {
    logger: createLogger({ requestId: request.id }),
    db: connectionPool,
  };
});

async function transferMoney(context, from, to, amount) {
  const tx = await context.db.beginTransaction();
  // All queries use same connection; logger auto-injects requestId
  await tx.commit();
}
```

Der Logger erhält `request.id` automatisch, sodass jeder Log-Eintrag ohne manuelles Weiterreichen nachvollziehbar ist.

### Scaffold – Dynamischer API-Client {#scaffold-dynamic-api-client}

```js
const scaffold = (url, structure) => {
  const api = {};
  for (const [entity, methods] of Object.entries(structure)) {
    api[entity] = {};
    for (const method of methods) {
      api[entity][method] = (...args) =>
        fetch(`${url}/${entity}/${method}`, {
          method: 'POST', body: JSON.stringify(args),
        }).then(r => r.json());
    }
  }
  return api;
};
```

## Management technischer Schulden {#technical-debt-management}

- Wenn Sie spüren, dass etwas nicht stimmt, aber die richtige Lösung nicht kennen, NICHT sofort umschreiben. Lernen Sie zuerst die passenden Muster
- Verbesserungen schrittweise mit jedem neuen Feature einführen
- Neuen Code sauber schreiben, auch wenn der umgebende Code unordentlich ist
- Wenn Sie nicht der Tech Lead sind, liegt es nicht in Ihrer Verantwortung, auf Refactoring zu drängen

## Fallstricke {#gotchas}

- Funktional vs. OOP: Für die meisten Geschäftsaufgaben sollte ein prozeduraler Stil verwendet werden. Angular orientiert sich an GoF/SOLID, React eher am funktionalen Stil
- Überengineering (striktes DDD) ist ebenso schädlich wie Unterengineering (God-Objekte). Der sinnvolle Mittelweg ist ein deklaratives Schema plus universelle Muster
- Eine gemeinsame ESLint-Konfiguration (ein Repository für Regeln, die von allen Projekt-Repositories geteilt werden) verhindert Stilabweichungen

## Siehe auch {#see-also}

- [[dependency-injection]] – DI vs. Module zur Entkopplung von Schichten
- [[data-access-patterns]] – DAL als eigenständige Architekturschicht
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) – Muster zur Schichtisolation (Adapter, Facade, Proxy)
- [[modules-and-packages]] – wie das Modulsystem die Architektur unterstützt
