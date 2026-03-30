---
title: Event Loop
category: internals
tags: [event-loop, libuv, async, non-blocking, phases, microtasks, macrotasks]
---
# Event Loop

The event loop is the core mechanism that enables Node.js to perform non-blocking I/O despite JavaScript being single-threaded. It delegates operations to the OS kernel or libuv thread pool and processes callbacks when operations complete.

## Key Facts

- Node.js runs on a single main thread; the event loop continuously checks for pending callbacks
- Built on top of **libuv** - a C library that provides the event loop, async I/O, and thread pool
- The loop has 6 phases executed in order: timers, pending callbacks, idle/prepare, poll, check, close callbacks
- **Timers phase**: executes `setTimeout()` and `setInterval()` callbacks whose threshold has elapsed
- **Poll phase**: retrieves new I/O events; executes I/O-related callbacks (almost all except timers, close, and `setImmediate`)
- **Check phase**: `setImmediate()` callbacks execute here, always after poll
- **Microtasks** (`Promise.then`, `queueMicrotask`, `process.nextTick`) run between every phase transition
- `process.nextTick()` fires before any other microtask (before Promises); use sparingly to avoid I/O starvation
- `setImmediate()` vs `setTimeout(fn, 0)`: inside an I/O callback, `setImmediate` always fires first
- libuv maintains a default thread pool of 4 threads (`UV_THREADPOOL_SIZE`), used for DNS lookups, file system ops, crypto, zlib
- The event loop exits when there are no more pending callbacks, timers, or open handles

## Patterns

```javascript
// Phase ordering demonstration
const fs = require('fs');

// Inside I/O callback: setImmediate fires before setTimeout
fs.readFile(__filename, () => {
  setTimeout(() => console.log('timeout'), 0);
  setImmediate(() => console.log('immediate'));
  // Output: immediate, timeout (deterministic)
});

// Outside I/O: order is non-deterministic
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
// Output: could be either order

// Microtask priority
Promise.resolve().then(() => console.log('promise'));
process.nextTick(() => console.log('nextTick'));
setTimeout(() => console.log('timeout'), 0);
// Output: nextTick, promise, timeout

// Starving the event loop with nextTick (anti-pattern)
function recurse() {
  process.nextTick(recurse); // I/O callbacks never execute
}

// Proper async recursion
function properRecurse() {
  setImmediate(properRecurse); // yields to I/O between calls
}

// Increase thread pool for I/O-heavy apps
// Set BEFORE requiring any module
process.env.UV_THREADPOOL_SIZE = 16; // max 1024
```

## Gotchas

- **Symptom**: `setTimeout(fn, 0)` fires before `setImmediate()` sometimes - **Cause**: outside I/O context, timer resolution depends on system clock granularity (~1ms) - **Fix**: use `setImmediate()` when you need "next iteration" semantics
- **Symptom**: server stops responding under load - **Cause**: CPU-intensive synchronous code blocks the event loop; no callbacks can fire - **Fix**: offload to [[worker-threads]], use `setImmediate()` to break up work, or move to a separate process
- **Symptom**: `process.nextTick()` recursive calls freeze the app - **Cause**: nextTick queue drains completely before moving to next phase, starving I/O - **Fix**: replace with `setImmediate()` for recursive patterns
- **Symptom**: DNS resolution slow under load - **Cause**: default libuv thread pool is only 4 threads; DNS lookups queue up - **Fix**: increase `UV_THREADPOOL_SIZE` before any `require()`

## See Also

- [[async-patterns]] - Promises, async/await built on top of the event loop
- [[streams]] - streaming I/O leverages the event loop's poll phase
- [[worker-threads]] - offloading CPU work from the main loop
- [Node.js Event Loop docs](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [libuv design overview](http://docs.libuv.org/en/v1.x/design.html)
