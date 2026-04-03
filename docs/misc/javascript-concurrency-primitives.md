---
title: JavaScript Concurrency Primitives and Workers
category: concepts
tags: [misc, javascript, concurrency, semaphore, mutex, worker-threads, design-patterns]
---

# JavaScript Concurrency Primitives and Workers

Advanced async coordination in JavaScript - semaphores, mutexes, async queues/pools, worker threads, and GoF patterns applied to async code. Covers both Node.js and browser APIs.

## Key Facts

- Node.js is single-threaded for JS execution but supports Worker Threads (true OS threads)
- `SharedArrayBuffer` + `Atomics` enable shared memory between workers
- Semaphore limits concurrent operations; Mutex is a binary semaphore for exclusive access
- `MessageChannel` creates connected port pairs; `BroadcastChannel` is one-to-many
- Cluster module forks copies of main process for load balancing via OS round-robin

## Patterns

### Semaphore

Limits concurrent operations to N:

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

### AsyncQueue

Producer/consumer with backpressure and concurrency control. Key for worker pools and rate limiting. Implementation strategies: circular buffer (cache-friendly), unrolled list (lower GC pressure).

### AsyncPool

Manages a pool of expensive resources (DB connections, worker threads). Factory Method pattern creates instances. Pool pattern reuses existing instances, queues requests when exhausted.

### AsyncCollector

Gathers async results until all are ready. Unlike `Promise.all`, supports dynamic addition of sources and partial timeout strategies.

### Worker Threads vs Child Processes

**Worker Threads** (`worker_threads`): true OS threads sharing same process memory. Communicate via `postMessage()` or `SharedArrayBuffer`. Use for CPU-intensive work (image processing, compression, ML inference).

**Child Processes** (`child_process`): separate processes, no shared memory. Use for isolation, different runtimes, CLI tools.

**SharedArrayBuffer + Atomics**: `Atomics.add/sub/load/store/exchange` are atomic. `Atomics.wait/notify` for synchronization.

**SpinLock**: busy-wait loop using `Atomics.wait()/notify()` on SharedArrayBuffer. Only for Worker Threads, very short critical sections.

### GoF Patterns for Async JS

**Adapter (asyncify/callbackify)**:
```js
util.promisify(cbFn)       // callback-based -> Promise
util.callbackify(asyncFn)  // async -> callback-last-error-first
```

**Chain of Responsibility**: avoid Express-style `(req, res, next)` - error propagation is fragile. Prefer explicit chains: `compose(fn1, fn2, fn3)(value)`.

**Observer/EventEmitter**: `EventEmitter` (Node.js), `EventTarget` (browser + Node 14+). `EventTarget` supports `{once: true}` and `AbortSignal` cancellation.

**Revealing Constructor**: used in Promises and streams - executor receives private capabilities (resolve/reject or push/done), consumers get restricted interface.

### SOLID and GRASP for JS

**SOLID**: Single Responsibility, Open/Closed (use composition not inheritance), Liskov Substitution, Interface Segregation, Dependency Inversion.

**GRASP**: Information Expert, Creator, Controller, High Cohesion / Low Coupling.

**Contractual programming**: specify preconditions, postconditions, invariants. Validate in debug mode, omit in production.

### Error Handling

**Operational errors** (network timeout, invalid input) - expected, recoverable, handle explicitly.
**Programmer errors** (TypeError, ReferenceError) - bugs, unrecoverable, let crash and restart.

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

## Gotchas

- Sending to a closed channel in Go panics; equivalent in JS - writing to ended stream throws
- `BroadcastChannel` is one-to-many within same process/origin only, not cross-process
- SpinLock with `Atomics.wait` only works in Worker Threads, not main thread (browser blocks)
- Express middleware pattern has fragile error propagation - prefer explicit composition

## See Also

- [[javascript-async-patterns]] - event loop, promises, streams, generators
- [[go-concurrency]] - goroutines, channels, sync primitives
