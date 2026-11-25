---
title: "Streams"
category: concepts
tags: [nodejs, streams, readable, writable, transform, duplex, backpressure]
level: 3
source_sha256: 0dabfc9d2aac717b71a96cbc7a1e75e0d86cc9f424d6bdf3f41036aba75a49c9
translation: machine
translated_at: '2026-10-24'
---
# Streams {#streams}

Node.js-Streams bieten eine Schnittstelle für die Arbeit mit Daten, die inkrementell eintreffen oder verbraucht werden. Anstatt ganze Datensätze in den Speicher zu laden, verarbeiten Streams Daten in Blöcken, wodurch sich Dateien und Netzwerkdaten verarbeiten lassen, die größer sind als der verfügbare RAM.

## Key Facts {#key-facts}

- **Readable** - Datenquelle (Dateilesevorgang, HTTP-Request-Body)
- **Writable** - Datensenke (Dateischreibvorgang, HTTP-Response)
- **Transform** - liest und schreibt und verändert die Daten dazwischen (Komprimierung, Verschlüsselung)
- **Duplex** - sowohl readable als auch writable, unabhängig voneinander (WebSocket, TCP-Socket)
- Streams implementieren Backpressure automatisch: Ist ein Writable langsamer als ein Readable, pausiert das Readable
- Wenn ein Socket pausiert ist, puffert der OS-Kernel eingehende Daten - die Event-Loop des Hauptthreads verarbeitet weiterhin andere Ereignisse

## Patterns {#patterns}

### Stream Backpressure Flow {#stream-backpressure-flow}

1. Ein Readable liefert Daten schneller, als ein Writable sie verbrauchen kann
2. Der interne Puffer füllt sich
3. Das Readable pausiert automatisch (Backpressure-Signal)
4. Sobald das Writable den Puffer abgearbeitet hat, setzt das Readable fort

### Optimized Chunk Streaming {#optimized-chunk-streaming}

```js
// Optimized: single buffer allocation for streaming over WebSocket
const sendChunk = (streamId, data) => {
  const packet = Buffer.allocUnsafe(8 + data.length);
  packet.writeInt32BE(streamId, 0);
  packet.writeInt32BE(data.length, 4);
  data.copy(packet, 8);
  return packet;
};

// Before optimization: two typed arrays, copied into one
// const header = new Uint8Array(8);
// const body = new Uint8Array(data);
// const packet = Buffer.concat([header, body]); // 2 allocations
```

### Cursor Pattern (Stream-like In-Memory) {#cursor-pattern-stream-like-in-memory}

```js
class Cursor {
  constructor(data) { this.data = data; }

  select(fields) {
    return new Cursor(this.data.map(row =>
      fields.reduce((obj, f) => ({ ...obj, [f]: row[f] }), {})
    ));
  }

  order(field) {
    return new Cursor([...this.data].sort((a, b) =>
      a[field] > b[field] ? 1 : -1
    ));
  }

  union(other) {
    return new Cursor([...this.data, ...other.data]);
  }

  intersect(other) {
    const keys = new Set(other.data.map(r => JSON.stringify(r)));
    return new Cursor(this.data.filter(r => keys.has(JSON.stringify(r))));
  }

  fetch() { return this.data; }
}

// Chaining mimics SQL:
// cursor.select(['name', 'age']).order('name').fetch()
```

Erweitert: `Symbol.iterator` für `for...of`, `Symbol.asyncIterator` für asynchrone Iteration und eine Stream-Schnittstelle für `.pipe()` implementieren.

## Gotchas {#gotchas}

- `Buffer.allocUnsafe()` ist schneller, enthält aber nicht initialisierten Speicher - immer alle Bytes beschreiben, bevor gesendet wird
- Das Verständnis von Backpressure erfordert Kenntnisse sowohl der Node.js-Interna als auch des Netzwerkbetriebs auf Betriebssystemebene (Kernel-Puffer)
- Das Streamen von Dateiblöcken über WebSocket benötigt IDs, um mehrere Streams über dieselbe Verbindung zu multiplexen

## See Also {#see-also}

- [[async-patterns]] - asynchrone Iteratoren und Generatoren als Alternativen zu Streams
- [Performance Optimization](performance-optimization.md) - Techniken zur Pufferoptimierung
- [[event-loop-and-architecture]] - wie libuv I/O im Thread-Pool behandelt
