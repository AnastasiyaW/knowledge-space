---
title: "Node.js & JavaScript Backend"
type: MOC
---

# Node.js & JavaScript Backend

## Runtime & Internals
- [[event-loop-and-architecture]] - V8, libuv, event loop, clustering, where Node.js fits and doesn't
- [[v8-optimization]] - Hidden classes, monomorphic/polymorphic code, JIT, small function inlining
- [[closures-and-scope]] - Lexical scope, closures as heap data structures, module scope

## Async Programming
- [[async-patterns]] - Callbacks, Promises, async/await, thenable objects, AbortController
- [[streams]] - Readable/Writable/Transform/Duplex, backpressure, buffer optimization
- [Concurrency Patterns](concurrency-patterns.md) - Actor model, CRDT, SharedWorker, binary protocols, deployment

## Language & Type System
- [[modules-and-packages]] - CommonJS vs ESM, interop, package-lock, npm, module cache
- [[solid-and-grasp]] - SOLID/GRASP in JavaScript, algebraic types, immutable records, LSP
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - Factory, Strategy, Observer, Adapter, Facade, Proxy, Flyweight, State

## Architecture
- [[application-architecture]] - DDD structure, layers, transport abstraction, context isolation
- [[data-access-patterns]] - Repository, Active Record, cursors, transactions, DAL
- [[dependency-injection]] - DI vs module system, coupling reduction, platform abstraction
- [[middleware-and-http]] - HTTP/WS transport, middleware as Chain of Responsibility, multi-framework

## Operations
- [Error Handling](error-handling.md) - AppError, AggregateError, Error.cause, fail-fast, error types
- [[security-and-sandboxing]] - Crypto, password hashing, vm sandbox, macaroons vs JWT
- [Performance Optimization](performance-optimization.md) - Round-trip reduction, Map vs Object, buffer optimization, DSL vs imperative
