---
title: "JavaScript-Concurrency-Primitive und Worker"
category: concepts
tags: [javascript, concurrency, semaphore, mutex, worker-threads, design-patterns]
level: 3
source_sha256: 3a43d9f64ac3e15a0b958bd15d7e0b1e807f56a708dfa76f7c45b947dbf9b18f
translation: machine
translated_at: '2026-10-24'
---
# JavaScript-Concurrency-Primitive und Worker {#javascript-concurrency-primitives-and-workers}

Fortgeschrittene asynchrone Koordination in JavaScript – Semaphoren, Mutexe, asynchrone Queues/Pools, Worker Threads und GoF-Muster, angewendet auf asynchronen Code. Behandelt sowohl Node.js- als auch Browser-APIs.

## Key Facts {#key-facts}

- Node.js ist für die JS-Ausführung single-threaded, unterstützt aber Worker Threads (echte OS-Threads)
- `SharedArrayBuffer` + `Atomics` ermöglichen gemeinsamen Speicher zwischen Workern
- Semaphore begrenzen gleichzeitige Operationen; ein Mutex ist eine binäre Semaphore für exklusiven Zugriff
- `MessageChannel` erzeugt verbundene Port-Paare; `BroadcastChannel` ist eins-zu-viele
- Das Cluster-Modul forkt Kopien des Hauptprozesses zur Lastverteilung per Round-Robin des Betriebssystems

## Patterns {#patterns}

### Semaphore {#semaphore}

Begrenzt gleichzeitige Operationen auf N:

```js
class Semaphore {
  constructor(count) { this.count = count; this.queue = []; }
  async acquire() {
    if (this.count > 0) { this.count--; return; }
    await new Promise(resolve => this.queue.push(resolve));
  }
  release() {
    this.count++;
    if (this.queue.length) { this.count--; this.queue.shift()(); }
  }
}
```

### AsyncQueue {#asyncqueue}

Producer/Consumer mit Backpressure und Nebenläufigkeitskontrolle. Zentral für Worker-Pools und Rate Limiting. Implementierungsstrategien: Ringpuffer (cache-freundlich), entrollte Liste (geringerer GC-Druck).

### AsyncPool {#asyncpool}

Verwaltet einen Pool teurer Ressourcen (DB-Verbindungen, Worker Threads). Das Factory-Method-Muster erzeugt die Instanzen. Das Pool-Muster verwendet vorhandene Instanzen wieder und reiht Anfragen in eine Warteschlange ein, wenn der Pool erschöpft ist.

### AsyncCollector {#asynccollector}

Sammelt asynchrone Ergebnisse, bis alle bereit sind. Anders als `Promise.all` unterstützt er das dynamische Hinzufügen von Quellen und Strategien für partielle Timeouts.

### Worker Threads vs. Child Processes {#worker-threads-vs-child-processes}

**Worker Threads** (`worker_threads`): echte OS-Threads, die denselben Prozessspeicher teilen. Kommunikation über `postMessage()` oder `SharedArrayBuffer`. Einsatz für CPU-intensive Arbeit (Bildverarbeitung, Komprimierung, ML-Inferenz).

**Child Processes** (`child_process`): separate Prozesse ohne gemeinsamen Speicher. Einsatz für Isolation, unterschiedliche Runtimes, CLI-Tools.

**SharedArrayBuffer + Atomics**: `Atomics.add/sub/load/store/exchange` sind atomar. `Atomics.wait/notify` dienen der Synchronisation.

**SpinLock**: Busy-Wait-Schleife mit `Atomics.wait()/notify()` auf einem SharedArrayBuffer. Nur für Worker Threads und sehr kurze kritische Abschnitte.

### GoF-Muster für asynchrones JS {#gof-patterns-for-async-js}

**Adapter (asyncify/callbackify)**:
```js
util.promisify(cbFn)       // callback-based -> Promise
util.callbackify(asyncFn)  // async -> callback-last-error-first
```

**Chain of Responsibility**: Vermeide Express-artiges `(req, res, next)` – die Fehlerweitergabe ist fragil. Bevorzuge explizite Ketten: `compose(fn1, fn2, fn3)(value)`.

**Observer/EventEmitter**: `EventEmitter` (Node.js), `EventTarget` (Browser + Node 14+). `EventTarget` unterstützt `{once: true}` und Abbruch über `AbortSignal`.

**Revealing Constructor**: verwendet bei Promises und Streams – der Executor erhält private Fähigkeiten (resolve/reject bzw. push/done), Konsumenten erhalten eine eingeschränkte Schnittstelle.

### SOLID und GRASP für JS {#solid-and-grasp-for-js}

**SOLID**: Single Responsibility, Open/Closed (Komposition statt Vererbung), Liskov Substitution, Interface Segregation, Dependency Inversion.

**GRASP**: Information Expert, Creator, Controller, High Cohesion / Low Coupling.

**Contractual Programming**: Vor-, Nachbedingungen und Invarianten spezifizieren. Im Debug-Modus validieren, in der Produktion weglassen.

### Fehlerbehandlung {#error-handling}

**Operative Fehler** (Netzwerk-Timeout, ungültige Eingabe) – erwartet, behebbar, explizit behandeln.
**Programmierfehler** (TypeError, ReferenceError) – Bugs, nicht behebbar; abstürzen lassen und neu starten.

```js
// Graceful shutdown
process.on('SIGTERM', async () => {
  server.close(() => { process.exit(0); });
});
process.on('uncaughtException', (err) => {
  logger.fatal(err);
  process.exit(1); // must exit - state is unknown
});
```

## Gotchas {#gotchas}

- Senden auf einen geschlossenen Channel in Go löst eine Panic aus; das JS-Äquivalent – Schreiben in einen beendeten Stream – wirft einen Fehler
- `BroadcastChannel` funktioniert eins-zu-viele nur innerhalb desselben Prozesses/Origins, nicht prozessübergreifend
- SpinLock mit `Atomics.wait` funktioniert nur in Worker Threads, nicht im Hauptthread (der Browser blockiert)
- Das Express-Middleware-Muster hat eine fragile Fehlerweitergabe – explizite Komposition bevorzugen

## See Also {#see-also}

- [[javascript-async-event-loop]] – Event Loop, Promises, Streams, Generatoren
- [[go/concurrency-patterns]] – Goroutinen, Channels, Sync-Primitive
