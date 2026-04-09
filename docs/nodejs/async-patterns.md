---
title: Async Patterns
category: concepts
tags: [nodejs, async, promises, callbacks, await, thenable, abort-controller]
---

# Async Patterns

JavaScript's async programming model spans callbacks, Promises, async/await, EventEmitter, and streams. Each pattern has specific use cases, performance characteristics, and interop mechanisms. The progression from callbacks to async/await represents increasing abstraction, not obsolescence - all patterns coexist.

## Key Facts

- **Callback-last**: callback is always the last argument
- **Error-first**: first callback argument is error (or null), data follows
- `async` keyword makes a function return a Promise; `await` unwraps it
- `Promise.withResolvers()` was designed for cases where resolve/reject need to escape the constructor scope - more efficient in V8 than manually storing them
- Thenable objects (objects with `.then()` method) are significantly faster than full Promises and fully compatible with `await`
- Cancelable Promises are now built-in via `AbortController` (was custom implementation)
- The Promise implementation depends partly on the host environment (Node.js/browser), not just V8

## Priority of Async Patterns

**Mandatory knowledge:**
- Callbacks (callback-last, error-first)
- Promises (then/catch/finally)
- async/await
- EventEmitter / EventTarget
- Streams (Readable, Writable, Transform, Duplex)

**Advanced/System programming:**
- Thenable objects, AsyncIterator/AsyncGenerator
- Worker threads, MessagePort, SharedArrayBuffer
- Atomics, Mutex, Semaphore, Actor model

**Legacy (can skip):** Async.js library, generators as async control flow, Domain (deprecated)

## Patterns

### Promisify / Callbackify Adapters

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

### Thenable Objects (Lightweight Promise Alternative)

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

### EventEmitter captureRejections

```js
const { EventEmitter } = require('events');

const ee = new EventEmitter({ captureRejections: true });
ee.on('event', async () => {
  throw new Error('async error'); // caught automatically
});
ee[Symbol.for('nodejs.rejection')] = (err) => console.error(err);
// Not available in browser's EventTarget
```

### WebSocket Data Batching

Problem: 2000+ real-time instrument subscriptions cause client-side freezing with individual messages.

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

Solutions: batch by time window, combine updates, implement backpressure, use binary protocols for high-frequency data.

## Gotchas

- Go-style error returns `{ error, data }` in JS is an anti-pattern: regresses to callback-era style, forces `if (error)` checks after every call, breaks async stack traces
- Race conditions exist in single-threaded Node.js: multiple async operations modifying shared state can interleave
- `await` in a loop serializes operations - use `Promise.all()` for concurrent execution

## See Also

- [[streams]] - Readable, Writable, Transform, Duplex with backpressure
- [[error-handling]] - AppError, AggregateError, fail-fast patterns
- [[design-patterns-gof]] - EventEmitter as async communication pattern
- [[event-loop-and-architecture]] - how the event loop processes async callbacks
