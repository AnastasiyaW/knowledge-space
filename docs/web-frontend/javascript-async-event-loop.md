---
title: JavaScript Async Patterns and Event Loop
category: concepts
tags: [javascript, async, promises, event-loop, node-js, streams]
---

# JavaScript Async Patterns and Event Loop

Comprehensive reference for JavaScript asynchronous programming - from callbacks through async/await to streams and signals. Covers V8 event loop internals, Node.js-specific APIs, and modern reactive patterns.

## Key Facts

- JavaScript async has a contract hierarchy: callbacks -> promises -> async/await -> events -> streams -> signals -> locks -> iterators
- The event loop drains the microtask queue (Promise `.then`, `queueMicrotask`) between every phase
- `process.nextTick` runs before any other microtask, before the next event loop phase
- `await` suspends function execution and yields to event loop - it does NOT block the thread
- Unhandled rejections crash Node.js 15+ by default
- libuv default thread pool size = 4 threads (`UV_THREADPOOL_SIZE` env var to change)

## Patterns

### Event Loop Phases

The event loop executes phases sequentially per tick:

1. **timers** - `setTimeout` and `setInterval` callbacks
2. **pending callbacks** - deferred I/O callbacks from previous iteration
3. **idle/prepare** - internal use
4. **poll** - retrieve new I/O events; blocks here if no timers pending
5. **check** - `setImmediate` callbacks
6. **close callbacks** - socket close events

Between each phase: microtask queue is fully drained.

**Reactor pattern**: libuv notifies event loop when I/O is ready (non-blocking).
**Proactor pattern**: completion-based - operation completes before notification.

### Callback Contract

```js
// Callback-last, error-first convention
function doAsync(arg, callback) {
  callback(null, result);     // success
  callback(new Error('msg')); // failure
}
```

Key rule: a callback must be called **either synchronously or asynchronously, never both** (Zalgo problem). Use `process.nextTick` or `queueMicrotask` to force async.

### Promise API

Promise states: `pending` -> `fulfilled` | `rejected` (immutable once settled).

```js
Promise.all(iterable)         // rejects on first rejection
Promise.allSettled(iterable)  // always resolves with {status, value|reason} array
Promise.race(iterable)        // settles with first settlement (any direction)
Promise.any(iterable)         // resolves with first fulfillment; AggregateError if all reject
Promise.withResolvers()       // returns {promise, resolve, reject} (newer API)
Promise.try(fn)               // wraps sync-or-async, catches sync throws too
```

**Thenable contract**: any object with `.then(onFulfilled, onRejected)`. `await` works on any thenable, not just native Promises.

### Node.js Streams

Four stream types:
- **Readable** - source of data (`read()`, `on('data')`, `for await...of`)
- **Writable** - destination (`write()`, `end()`)
- **Duplex** - both readable and writable (TCP socket)
- **Transform** - Duplex that transforms data (gzip, cipher)

**Backpressure**: when consumer is slower than producer, `write()` returns `false`, emit `drain` when ready. Automatic with `pipe()`.

**Web Streams API** (browser + Node 18+): `ReadableStream`, `WritableStream`, `TransformStream`. Works natively in `fetch` Response.body.

### Generators and Async Iterators

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

`for...of` uses iterator protocol. Spread `[...iter]`, destructuring, and `Array.from()` all consume iterables.

### Signals (Reactive State)

Modern reactive primitive (Angular Signals, Solid.js, Preact Signals, TC39 proposal):

- `signal(initialValue)` - reactive state container
- `computed(fn)` - derived value, lazily recomputed when dependencies change
- `effect(fn)` - side effect that re-runs when dependencies change

Signals track dependencies automatically at access time. Unlike RxJS - synchronous propagation, no subscription management.

### AbortController Cancellation

```js
const controller = new AbortController();
const { signal } = controller;

fetch(url, { signal })
  .catch(err => {
    if (err.name === 'AbortError') { /* cancelled */ }
  });

setTimeout(() => controller.abort(), 5000);
```

Pass `signal` through async chains. Check `signal.aborted` or `signal.throwIfAborted()` in custom async code.

### AsyncLocalStorage

Thread-local-storage equivalent for async code:

```js
const als = new AsyncLocalStorage();
als.run({ userId: 123 }, async () => {
  await someAsyncOp();
  als.getStore(); // { userId: 123 } - available in callbacks too
});
```

Use for request context propagation (tracing, auth, logging) without parameter threading.

## Gotchas

- A callback must never be called both sync and async (Zalgo problem) - always pick one
- `process.nextTick` can starve the event loop if called recursively
- libuv thread pool (default 4) is shared across file I/O, DNS, and crypto - can become a bottleneck
- `Error.cause` option (`new Error('context', { cause: originalError })`) is the modern way to wrap errors
- Web Locks API (`navigator.locks.request(name, fn)`) works in browser + Node 18+ for named exclusive/shared locks
- Legacy patterns to avoid: `function*/yield` for async, Deferred, Async.js, RxJS for simple cases

## See Also

- [[javascript-concurrency-primitives]] - Semaphore, Mutex, AsyncQueue, Worker Threads
- [[go/concurrency-patterns]] - comparison: goroutines vs JS event loop model
