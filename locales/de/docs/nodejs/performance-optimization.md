---
title: "Performance-Optimierung"
category: operations
tags: [nodejs, performance, benchmarking, map-vs-object, round-trips, buffer-optimization]
level: 5
source_sha256: 4277af90b6c3e9a61ebd4be7d37dd9e8b3be34582bf2ee308f212c5c5f29898f
translation: machine
translated_at: '2026-10-24'
---
# Performance-Optimierung {#performance-optimization}

Die Performance-Optimierung in Node.js konzentriert sich auf die Reduzierung von Round-Trips, die Wahl effizienter Datenstrukturen, die Optimierung von Buffer-Allokationen und das Verständnis der V8-Interna. Messung ist unverzichtbar, denn das Performance-Profil jeder Anwendung ist einzigartig.

## Wichtige Fakten {#key-facts}

- Die Minimierung von Round-Trips ist wichtiger als die reine Geschwindigkeit
- System A verarbeitet doppelt so schnell, benötigt aber 50 Requests; System B ist langsamer, erledigt aber alles in einem Request – System B gewinnt oft
- Selbst auf localhost (derselbe Rechner) verursacht die Socket-Kommunikation messbaren Aufwand
- Map ist bei 1M+ Einträgen konsistent schneller als Object
- Benchmarks sequenziell (nicht parallel) ausführen, damit Ressourcenkonkurrenz die Ergebnisse nicht verfälscht
- PostgreSQL kann für aggressives In-Memory-Caching konfiguriert werden, doch ein Caching im Prozess (Node.js Map/Object) vermeidet selbst den prozessübergreifenden Overhead

## Muster {#patterns}

### Round-Trip-Reduktion {#round-trip-reduction}

```javascript
// BAD: 50 separate requests
for (const id of ids) {
  const user = await api.getUser(id);
}

// GOOD: batch request
const users = await api.getUsers(ids);
```

Kein Serialisierungs-/Deserialisierungs-Overhead pro Request, keine Netzwerklatenz, kein Verbindungsmanagement.

### Buffer-Optimierung {#buffer-optimization}

```js
// Before: two allocations
const header = new Uint8Array(8);
const body = new Uint8Array(data);
const packet = Buffer.concat([header, body]);

// After: single allocation
const packet = Buffer.allocUnsafe(8 + data.length);
packet.writeInt32BE(streamId, 0);
packet.writeInt32BE(data.length, 4);
data.copy(packet, 8);
```

### Map vs. Object-Benchmarking {#map-vs-object-benchmarking}

```js
// Benchmark methodology:
// - Separate threads for each test
// - Run GC between tests
// - Generate keys once, reuse
// - Run sequentially, not in parallel

const map = new Map();
const obj = Object.create(null);

// For 1M+ entries: Map wins consistently
// Object has overhead from prototype chain and hidden class management
```

### DSL vs. imperativer Code (Performance und Wartbarkeit) {#dsl-vs-imperative-performance-and-maintainability}

```js
// LLM-generated: verbose imperative IndexedDB code
db.createObjectStore('users', { keyPath: 'id', autoIncrement: true });
const usersStore = transaction.objectStore('users');
usersStore.createIndex('name', 'name', { unique: false });
// ... repeated for every entity

// Human-written DSL: declarative, shorter, reusable, with migrations
const schema = {
  users: { keyPath: 'id', autoIncrement: true,
    indexes: { name: {}, email: { unique: true } } },
};
const db = await openDatabase('myApp', schema);
```

Eine generische Funktion behandelt alle Entitäten. Das LLM erzeugt den imperativen Code für jeden Store manuell.

## Fallstricke {#gotchas}

- `Buffer.allocUnsafe()` ist schneller, enthält aber nicht initialisierten Speicher – daher immer alle Bytes befüllen
- Binärprotokolle (protobuf-ähnlich) übertreffen JSON bei hochfrequenten Daten sowohl in Größe als auch in Geschwindigkeit
- Das Flyweight-Muster für Timer tauscht 2 zusätzliche CMP-Instruktionen (polymorphes Dispatching) gegen Millionen eingesparter Allokationen – den Trade-off immer messen

## Siehe auch {#see-also}

- [[v8-optimization]] - Hidden Classes, monomorpher Code, JIT-Interna
- [[streams]] - Stream-Optimierung und Chunk-Behandlung
- [Concurrency Patterns](concurrency-patterns.md) - WebSocket-Batching, Binärprotokolle
- [[event-loop-and-architecture]] - Performance-Faktoren in Node.js
