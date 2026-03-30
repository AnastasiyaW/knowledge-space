---
title: "Node.js & JavaScript Backend - Knowledge Map"
category: moc
tags: [nodejs, javascript, backend, index]
---
# Node.js & JavaScript Backend

Map of Content for Node.js runtime, JavaScript language patterns, and backend architecture.

## Language Fundamentals

- [[closures-and-scope]] - lexical scope, closures, hoisting, IIFE, module wrapper
- [[prototypes-and-classes]] - prototype chain, ES6 classes, mixins, composition vs inheritance
- [[iterators-and-generators]] - iterator/iterable protocol, generators, async generators, lazy evaluation
- [[collections-and-data-structures]] - Map, Set, WeakMap, WeakSet, Buffer, TypedArray

## Async Programming

- [[event-loop]] - libuv, phases, microtasks/macrotasks, timers, setImmediate
- [[async-patterns]] - callbacks, Promises, async/await, Promise combinators, concurrency limiters
- [[streams]] - Readable, Writable, Transform, Duplex, backpressure, pipeline
- [[concurrency-patterns]] - mutex, semaphore, rate limiting, debounce/throttle, AbortController

## Node.js Internals

- [[v8-and-memory]] - JIT compilation, hidden classes, garbage collection, heap profiling, memory leaks
- [[worker-threads]] - worker_threads, child_process, cluster, SharedArrayBuffer, Atomics
- [[modules-and-packages]] - CommonJS, ES Modules, package.json exports, resolution algorithm

## Architecture & Patterns

- [[solid-and-grasp]] - SOLID/GRASP principles adapted for JavaScript and async
- [[design-patterns-gof]] - Singleton, Factory, Observer, Strategy, Decorator, Chain of Responsibility
- [[dependency-injection]] - factory-based DI, composition root, IoC containers, testability
- [[middleware-and-http]] - middleware chain, Express/Koa, HTTP server, graceful shutdown

## Type Safety & Data

- [[typescript-integration]] - strict mode, generics, discriminated unions, Zod, type-safe events
- [[algebraic-types]] - Result, Maybe, Either, railway-oriented programming
- [[data-access-patterns]] - Repository, Active Record, DTO, Query Builder, transactions, connection pooling
