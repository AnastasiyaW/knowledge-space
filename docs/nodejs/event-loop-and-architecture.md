---
title: Event Loop and Architecture
category: concepts
tags: [nodejs, event-loop, v8, libuv, architecture, runtime]
---

# Event Loop and Architecture

Node.js is a JavaScript runtime for server-side applications built on three pillars: V8 (JavaScript engine), libuv (async I/O with event loop and thread pool), and the standard library (fs, http, crypto, etc.). The event loop is the core mechanism enabling non-blocking I/O in a single-threaded environment.

## Key Facts

- V8 is the JavaScript engine, but Node.js could theoretically use a different engine
- libuv provides the event loop, thread pool for file/network operations, and cross-platform async I/O
- Node.js is single-threaded for JavaScript execution but uses the thread pool for blocking I/O
- Primary role: application server, network server, or service orchestrator
- NOT ideal for: CPU-intensive computation (use Worker Threads or native addons), hard real-time systems, or systems requiring shared memory between threads (use Go, Rust, C++)
- Performance depends entirely on application code quality - **must measure, cannot estimate**

## Event Loop Mechanics

1. Application code calls a standard library function (e.g., `fs.readFile`)
2. Standard library may use libuv thread pool for I/O operations
3. When operation completes, callback is placed in the callback queue
4. Event loop continuously reads from the callback queue
5. Each callback is pushed onto the call stack and executed in V8
6. When the callback queue is empty AND no pending operations remain, the Node.js process exits

## Performance Factors

- Async patterns used (callbacks vs Promises vs async/await)
- CPU-bound operations (long loops, in-memory JOINs)
- Proper use of JS data structures (Map vs Object for large collections)
- Quality of npm dependencies
- Database query efficiency
- Memory management (buffer pooling, avoiding leaks)

## Patterns

### Graceful Shutdown

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

### Application Structure - DDD Server

```
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

Application structure is the #1 difficulty in Node.js development - not frameworks, async patterns, or internals, but splitting code into layers and managing coupling between abstractions.

## Gotchas

- Despite being single-threaded, Node.js CAN have race conditions: multiple async operations modifying shared state can interleave (e.g., two requests checking a balance, both finding sufficient funds, both deducting)
- `process.exit()` without graceful shutdown may lose in-flight requests and corrupt data
- Worker Threads share memory via SharedArrayBuffer but require Atomics for synchronization

## See Also

- [[v8-optimization]] - V8 hidden classes, monomorphic code, JIT compilation
- [[async-patterns]] - callbacks, Promises, async/await mechanics
- [[streams]] - stream types and backpressure handling
- [[performance-optimization]] - round-trip reduction, Map vs Object benchmarks
