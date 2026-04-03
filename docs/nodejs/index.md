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
- [[concurrency-patterns]] - Actor model, CRDT, SharedWorker, binary protocols, deployment

## Language & Type System
- [[modules-and-packages]] - CommonJS vs ESM, interop, package-lock, npm, module cache
- [[solid-and-grasp]] - SOLID/GRASP in JavaScript, algebraic types, immutable records, LSP
- [[design-patterns-gof]] - Factory, Strategy, Observer, Adapter, Facade, Proxy, Flyweight, State

## Architecture
- [[application-architecture]] - DDD structure, layers, transport abstraction, context isolation
- [[data-access-patterns]] - Repository, Active Record, cursors, transactions, DAL
- [[dependency-injection]] - DI vs module system, coupling reduction, platform abstraction
- [[middleware-and-http]] - HTTP/WS transport, middleware as Chain of Responsibility, multi-framework

## Operations
- [[error-handling]] - AppError, AggregateError, Error.cause, fail-fast, error types
- [[security-and-sandboxing]] - Crypto, password hashing, vm sandbox, macaroons vs JWT
- [[performance-optimization]] - Round-trip reduction, Map vs Object, buffer optimization, DSL vs imperative
