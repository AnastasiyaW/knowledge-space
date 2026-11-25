---
title: "Event Loop und Architektur"
category: concepts
tags: [nodejs, event-loop, v8, libuv, architecture, runtime]
level: 3
source_sha256: e49c9d4b1b18b13f3e2d298de92af4e230df1dbb786a4c7aa53b316f6641ed08
translation: machine
translated_at: '2026-10-24'
---
# Event Loop und Architektur {#event-loop-and-architecture}

Node.js ist eine JavaScript-Laufzeitumgebung für serverseitige Anwendungen, die auf drei Säulen aufbaut: V8 (JavaScript-Engine), libuv (asynchrone I/O mit Event Loop und Thread Pool) und der Standardbibliothek (fs, http, crypto usw.). Der Event Loop ist der zentrale Mechanismus, der nicht-blockierende I/O in einer single-threaded Umgebung ermöglicht.

## Wichtige Fakten {#key-facts}

- V8 ist die JavaScript-Engine, theoretisch könnte Node.js aber auch eine andere Engine verwenden
- libuv stellt den Event Loop, den Thread Pool für Datei- und Netzwerkoperationen sowie plattformübergreifende asynchrone I/O bereit
- Node.js ist für die Ausführung von JavaScript single-threaded, nutzt den Thread Pool aber für blockierende I/O
- Primäre Rolle: Application Server, Netzwerkserver oder Service-Orchestrator
- NICHT ideal für: CPU-intensive Berechnungen (stattdessen Worker Threads oder native Addons verwenden), harte Echtzeitsysteme oder Systeme, die gemeinsamen Speicher zwischen Threads benötigen (stattdessen Go, Rust, C++ verwenden)
- Die Performance hängt vollständig von der Qualität des Anwendungscodes ab - **messen, nicht schätzen**

## Mechanik des Event Loops {#event-loop-mechanics}

1. Anwendungscode ruft eine Funktion der Standardbibliothek auf (z. B. `fs.readFile`)
2. Die Standardbibliothek kann für I/O-Operationen den libuv Thread Pool verwenden
3. Wenn die Operation abgeschlossen ist, wird der Callback in die Callback-Queue gestellt
4. Der Event Loop liest kontinuierlich aus der Callback-Queue
5. Jeder Callback wird auf den Call Stack gelegt und in V8 ausgeführt
6. Ist die Callback-Queue leer UND stehen keine offenen Operationen mehr aus, wird der Node.js-Prozess beendet

## Performance-Faktoren {#performance-factors}

- Verwendete asynchrone Muster (Callbacks vs. Promises vs. async/await)
- CPU-gebundene Operationen (lange Schleifen, In-Memory-JOINs)
- Sachgerechte Nutzung der JS-Datenstrukturen (Map vs. Object bei großen Sammlungen)
- Qualität der npm-Abhängigkeiten
- Effizienz der Datenbankabfragen
- Speicherverwaltung (Buffer-Pooling, Vermeidung von Lecks)

## Muster {#patterns}

### Graceful Shutdown {#graceful-shutdown}

```js
const server = http.createServer(app);

process.on('SIGTERM', async () => {
  // 1. Stop accepting new connections
  server.close();
  // 2. Wait for in-flight requests to complete
  await drainConnections();
  // 3. Close database connections
  await db.end();
  // 4. Flush logs
  await logger.flush();
  // 5. Exit
  process.exit(0);
});
```

### Anwendungsstruktur - DDD-Server {#application-structure-ddd-server}

```javascript
project/
  schemas/         # Domain schemas (JSON Schema / metaschema)
    auth.schema
    messenger.schema
  db/              # Database creation scripts (NOT ORM)
    create.sql
  api/             # API layer
    auth/
    messenger/
  domain/          # Business logic (pure functions)
  transport/       # HTTP and WebSocket handlers
  config.js        # Centralized configuration
  main.js          # Entry point
```

Die Anwendungsstruktur ist die größte Schwierigkeit in der Node.js-Entwicklung - nicht Frameworks, asynchrone Muster oder Interna, sondern die Aufteilung des Codes in Schichten und die Verwaltung der Kopplung zwischen Abstraktionen.

## Fallstricke {#gotchas}

- Trotz Single-Threading KANN Node.js Race Conditions haben: Mehrere asynchrone Operationen, die gemeinsamen Zustand verändern, können sich überlappen (z. B. zwei Requests prüfen einen Kontostand, beide stellen ausreichende Deckung fest und buchen beide ab)
- `process.exit()` ohne Graceful Shutdown kann laufende Requests verlieren und Daten beschädigen
- Worker Threads teilen Speicher über SharedArrayBuffer, benötigen für die Synchronisation aber Atomics

## Siehe auch {#see-also}

- [[v8-optimization]] - V8 Hidden Classes, monomorpher Code, JIT-Kompilierung
- [[async-patterns]] - Callbacks, Promises, Mechanik von async/await
- [[streams]] - Stream-Typen und Backpressure-Behandlung
- [Performance-Optimierung](performance-optimization.md) - Reduktion von Round-Trips, Benchmarks zu Map vs. Object
