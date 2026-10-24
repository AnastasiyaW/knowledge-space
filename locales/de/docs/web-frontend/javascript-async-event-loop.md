---
title: "JavaScript-Async-Muster und Event Loop"
category: concepts
tags: [javascript, async, promises, event-loop, node-js, streams]
level: 3
source_sha256: 9669c00530aea1d18181e7959d95ed0f0b555d4cda55305412d2ae6ffc8866aa
translation: machine
translated_at: '2026-10-24'
---
# JavaScript-Async-Muster und Event Loop {#javascript-async-patterns-and-event-loop}

Umfassende Referenz zur asynchronen Programmierung in JavaScript, von Callbacks über async/await bis zu Streams und Signals. Behandelt die internen Mechanismen des V8-Event-Loops, Node.js-spezifische APIs und moderne reaktive Muster.

## Kernfakten {#key-facts}

- Die asynchrone Programmierung in JavaScript folgt einer Vertragshierarchie: Callbacks -> Promises -> async/await -> Events -> Streams -> Signals -> Locks -> Iteratoren
- Der Event Loop leert die Microtask-Queue (Promise-`.then`, `queueMicrotask`) zwischen jeder Phase
- `process.nextTick` wird vor allen anderen Microtasks und vor der nächsten Event-Loop-Phase ausgeführt
- `await` unterbricht die Funktionsausführung und gibt die Kontrolle an den Event Loop zurück – es blockiert den Thread **nicht**
- Unbehandelte Rejections bringen Node.js 15+ standardmäßig zum Absturz
- Die Standardgröße des libuv-Thread-Pools beträgt 4 Threads (Änderung über die Umgebungsvariable `UV_THREADPOOL_SIZE`)

## Muster {#patterns}

### Event-Loop-Phasen {#event-loop-phases}

Der Event Loop durchläuft die Phasen pro Tick sequenziell:

1. **timers** – Callbacks von `setTimeout` und `setInterval`
2. **pending callbacks** – verzögerte I/O-Callbacks aus der vorherigen Iteration
3. **idle/prepare** – interne Verwendung
4. **poll** – neue I/O-Ereignisse abrufen; blockiert hier, wenn keine Timer ausstehen
5. **check** – Callbacks von `setImmediate`
6. **close callbacks** – Socket-Close-Ereignisse

Zwischen den einzelnen Phasen wird die Microtask-Queue vollständig geleert.

**Reactor-Muster**: libuv benachrichtigt den Event Loop, sobald I/O bereit ist (nicht blockierend).
**Proactor-Muster**: abschlussbasiert – die Operation ist bereits abgeschlossen, bevor die Benachrichtigung erfolgt.

### Callback-Vertrag {#callback-contract}

```js
// Callback-last, error-first convention
function doAsync(arg, callback) {
  callback(null, result);     // success
  callback(new Error('msg')); // failure
}
```

Wichtige Regel: Ein Callback muss **entweder synchron oder asynchron** aufgerufen werden, niemals beides (Zalgo-Problem). Verwenden Sie `process.nextTick` oder `queueMicrotask`, um asynchronen Aufruf zu erzwingen.

### Promise-API {#promise-api}

Zustände eines Promise: `pending` -> `fulfilled` | `rejected` (nach dem Abschluss unveränderlich).

```js
Promise.all(iterable)         // rejects on first rejection
Promise.allSettled(iterable)  // always resolves with {status, value|reason} array
Promise.race(iterable)        // settles with first settlement (any direction)
Promise.any(iterable)         // resolves with first fulfillment; AggregateError if all reject
Promise.withResolvers()       // returns {promise, resolve, reject} (newer API)
Promise.try(fn)               // wraps sync-or-async, catches sync throws too
```

**Thenable-Vertrag**: jedes Objekt mit `.then(onFulfilled, onRejected)`. `await` funktioniert mit jedem Thenable, nicht nur mit nativen Promises.

### Node.js-Streams {#nodejs-streams}

Vier Stream-Typen:
- **Readable** – Datenquelle (`read()`, `on('data')`, `for await...of`)
- **Writable** – Datenziel (`write()`, `end()`)
- **Duplex** – sowohl lesbar als auch schreibbar (TCP-Socket)
- **Transform** – Duplex, das Daten transformiert (gzip, Verschlüsselung)

**Backpressure**: Ist der Consumer langsamer als der Producer, gibt `write()` `false` zurück und `drain` wird ausgelöst, sobald wieder geschrieben werden kann. Bei Verwendung von `pipe()` erfolgt dies automatisch.

**Web-Streams-API** (Browser sowie Node 18+): `ReadableStream`, `WritableStream`, `TransformStream`. Funktioniert nativ mit `Response.body` von `fetch`.

### Generatoren und asynchrone Iteratoren {#generators-and-async-iterators}

```js
function* generator() {
  yield 1;
  yield 2;
  return 3; // done:true
}

// Async generator for paginated APIs, event streams
async function* asyncGen() {
  yield await fetch('/api');
}
for await (const item of asyncGen()) { ... }
```

`for...of` verwendet das Iterator-Protokoll. Spread (`[...iter]`), Destrukturierung und `Array.from()` konsumieren alle Iterables.

### Signals (reaktiver Zustand) {#signals-reactive-state}

Modernes reaktives Primitiv (Angular Signals, Solid.js, Preact Signals, TC39-Vorschlag):

- `signal(initialValue)` – Container für reaktiven Zustand
- `computed(fn)` – abgeleiteter Wert, der bei Änderung der Abhängigkeiten lazy neu berechnet wird
- `effect(fn)` – Seiteneffekt, der bei Änderung der Abhängigkeiten erneut ausgeführt wird

Signals erfassen ihre Abhängigkeiten automatisch beim Zugriff. Anders als bei RxJS erfolgt die Propagation synchron, und es ist keine Verwaltung von Subscriptions nötig.

### AbortController-Abbruch {#abortcontroller-cancellation}

```js
const controller = new AbortController();
const { signal } = controller;

fetch(url, { signal })
  .catch(err => {
    if (err.name === 'AbortError') { /* cancelled */ }
  });

setTimeout(() => controller.abort(), 5000);
```

Übergeben Sie `signal` durch alle asynchronen Ketten. Prüfen Sie `signal.aborted` oder `signal.throwIfAborted()` in eigenem asynchronem Code.

### AsyncLocalStorage {#asynclocalstorage}

Äquivalent zu Thread-Local-Storage für asynchronen Code:

```js
const als = new AsyncLocalStorage();
als.run({ userId: 123 }, async () => {
  await someAsyncOp();
  als.getStore(); // { userId: 123 } - available in callbacks too
});
```

Verwenden Sie es zur Weitergabe von Anfragekontext (Tracing, Authentifizierung, Logging), ohne Parameter durchreichen zu müssen.

## Fallstricke {#gotchas}

- Ein Callback darf niemals sowohl synchron als auch asynchron aufgerufen werden (Zalgo-Problem) – wählen Sie immer eine Variante
- `process.nextTick` kann den Event Loop aushungern, wenn es rekursiv aufgerufen wird
- Der libuv-Thread-Pool (Standard: 4) wird von Datei-I/O, DNS und Kryptografie gemeinsam genutzt und kann zum Engpass werden
- Die Option `Error.cause` (`new Error('context', { cause: originalError })`) ist der moderne Weg, Fehler zu verpacken
- Die Web-Locks-API (`navigator.locks.request(name, fn)`) funktioniert im Browser sowie in Node 18+ für benannte exklusive und geteilte Locks
- Zu vermeidende Legacy-Muster: `function*/yield` für asynchrone Logik, Deferred, Async.js, RxJS in einfachen Fällen

## Siehe auch {#see-also}

- [[javascript-concurrency-primitives]] – Semaphore, Mutex, AsyncQueue, Worker Threads
- [[go/concurrency-patterns]] – Vergleich: Goroutinen vs. JavaScript-Event-Loop-Modell
