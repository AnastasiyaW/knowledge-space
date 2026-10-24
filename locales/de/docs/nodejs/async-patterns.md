---
title: "Async-Muster"
category: concepts
tags: [nodejs, async, promises, callbacks, await, thenable, abort-controller]
level: 3
source_sha256: 1b5aac4ff44971ffc20907dad6d799972b0bcf171b43b5538c6621d92f54340a
translation: machine
translated_at: '2026-10-24'
---
# Async-Muster {#async-patterns}

Das asynchrone Programmiermodell von JavaScript umfasst Callbacks, Promises, async/await, EventEmitter und Streams. Jedes Muster hat spezifische Anwendungsfälle, Leistungsmerkmale und Interop-Mechanismen. Der Weg von Callbacks zu async/await stellt eine zunehmende Abstraktion dar, keine Veralterung – alle Muster existieren nebeneinander.

## Wichtige Fakten {#key-facts}

- **Callback-last**: Der Callback ist immer das letzte Argument
- **Error-first**: Das erste Callback-Argument ist der Fehler (oder null), danach folgen die Daten
- Das Schlüsselwort `async` lässt eine Funktion ein Promise zurückgeben; `await` entpackt es
- `Promise.withResolvers()` wurde für Fälle entworfen, in denen resolve/reject den Konstruktor-Gültigkeitsbereich verlassen müssen – in V8 effizienter, als sie manuell zu speichern
- Thenable-Objekte (Objekte mit einer `.then()`-Methode) sind deutlich schneller als vollständige Promises und vollständig mit `await` kompatibel
- Abbrechbare Promises sind nun über `AbortController` integriert (vorher eigene Implementierung)
- Die Promise-Implementierung hängt teilweise von der Host-Umgebung ab (Node.js/Browser), nicht nur von V8

## Priorität der Async-Muster {#priority-of-async-patterns}

**Pflichtwissen:**
- Callbacks (Callback-last, Error-first)
- Promises (then/catch/finally)
- async/await
- EventEmitter / EventTarget
- Streams (Readable, Writable, Transform, Duplex)

**Fortgeschritten/Systemprogrammierung:**
- Thenable-Objekte, AsyncIterator/AsyncGenerator
- Worker-Threads, MessagePort, SharedArrayBuffer
- Atomics, Mutex, Semaphore, Actor-Modell

**Veraltet (kann übersprungen werden):** Async.js-Bibliothek, Generatoren als asynchroner Kontrollfluss, Domain (veraltet)

## Muster {#patterns}

### Promisify- / Callbackify-Adapter {#promisify-callbackify-adapters}

```js
// Promisify: callback-last → Promise
const promisify = (fn) => (...args) =>
  new Promise((resolve, reject) =>
    fn(...args, (err, data) => err ? reject(err) : resolve(data))
  );

// Callbackify: Promise → callback-last
const callbackify = (fn) => (...args) => {
  const callback = args.pop();
  fn(...args)
    .then((data) => callback(null, data))
    .catch((err) => callback(err));
};
```

### Thenable-Objekte (leichtgewichtige Promise-Alternative) {#thenable-objects-lightweight-promise-alternative}

```js
// Thenable - lightweight, V8-optimized
const thenable = {
  then(resolve) { resolve(42); }
};

const result = await thenable; // 42

// Works everywhere Promises are accepted per spec
// Created at V8 level with full optimizations
// Significantly faster than full Promises
```

### EventEmitter captureRejections {#eventemitter-capturerejections}

```js
const { EventEmitter } = require('events');

const ee = new EventEmitter({ captureRejections: true });
ee.on('event', async () => {
  throw new Error('async error'); // caught automatically
});
ee[Symbol.for('nodejs.rejection')] = (err) => console.error(err);
// Not available in browser's EventTarget
```

### WebSocket-Datenbündelung {#websocket-data-batching}

Problem: 2000+ Echtzeit-Instrumentenabonnements verursachen bei einzelnen Nachrichten Einfrieren auf der Client-Seite.

```js
class BatchedSender {
  #buffer = [];
  #interval;

  constructor(ws, intervalMs = 100) {
    this.#interval = setInterval(() => {
      if (this.#buffer.length > 0) {
        ws.send(JSON.stringify(this.#buffer));
        this.#buffer = [];
      }
    }, intervalMs);
  }

  send(data) { this.#buffer.push(data); }
}
```

Lösungen: nach Zeitfenster bündeln, Aktualisierungen zusammenfassen, Backpressure implementieren, binäre Protokolle für hochfrequente Daten verwenden.

## Fallstricke {#gotchas}

- Go-artige Fehlerrückgaben `{ error, data }` in JS sind ein Anti-Pattern: Sie führen zurück zum Stil der Callback-Ära, erzwingen `if (error)`-Prüfungen nach jedem Aufruf und zerstören asynchrone Stack-Traces
- Race Conditions existieren auch im Single-Thread-Modell von Node.js: Mehrere asynchrone Operationen, die gemeinsamen Zustand verändern, können sich überlappen
- `await` in einer Schleife serialisiert Operationen – für nebenläufige Ausführung `Promise.all()` verwenden

## Siehe auch {#see-also}

- [[streams]] – Readable, Writable, Transform, Duplex mit Backpressure
- [Fehlerbehandlung](error-handling.md) – AppError, AggregateError, Fail-Fast-Muster
- [Entwurfsmuster (GoF) in JavaScript](design-patterns-gof.md) – EventEmitter als asynchrones Kommunikationsmuster
- [[event-loop-and-architecture]] – wie die Event Loop asynchrone Callbacks verarbeitet
