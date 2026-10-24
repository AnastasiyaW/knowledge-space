---
title: "Node.js & JavaScript-Backend"
type: MOC
level: 3
source_sha256: 6969a856c822a20871790101b6c7e9b8f17a4e46034df8854e1f01d26d0da0c5
translation: machine
translated_at: '2026-10-24'
---
# Node.js & JavaScript-Backend {#nodejs-javascript-backend}

## Laufzeitumgebung & Interna {#runtime-internals}
- [[event-loop-and-architecture]] - V8, libuv, Event Loop, Clustering, wo Node.js passt und wo nicht
- [[v8-optimization]] - Hidden Classes, monomorpher/polymorpher Code, JIT, Inlining kleiner Funktionen
- [[closures-and-scope]] - Lexikalischer Scope, Closures als Heap-Datenstrukturen, Modul-Scope

## Asynchrone Programmierung {#async-programming}
- [[async-patterns]] - Callbacks, Promises, async/await, Thenable-Objekte, AbortController
- [[streams]] - Readable/Writable/Transform/Duplex, Backpressure, Buffer-Optimierung
- [Concurrency-Muster](concurrency-patterns.md) - Actor-Modell, CRDT, SharedWorker, Binärprotokolle, Deployment

## Sprache & Typsystem {#language-type-system}
- [[modules-and-packages]] - CommonJS vs. ESM, Interop, package-lock, npm, Modul-Cache
- [[solid-and-grasp]] - SOLID/GRASP in JavaScript, algebraische Typen, unveränderliche Records, LSP
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - Factory, Strategy, Observer, Adapter, Facade, Proxy, Flyweight, State

## Architektur {#architecture}
- [[application-architecture]] - DDD-Struktur, Schichten, Transport-Abstraktion, Kontextisolation
- [[data-access-patterns]] - Repository, Active Record, Cursor, Transaktionen, DAL
- [[dependency-injection]] - DI vs. Modulsystem, Reduzierung der Kopplung, Plattform-Abstraktion
- [[middleware-and-http]] - HTTP/WS-Transport, Middleware als Chain of Responsibility, Multi-Framework

## Betrieb {#operations}
- [Fehlerbehandlung](error-handling.md) - AppError, AggregateError, Error.cause, Fail-Fast, Fehlertypen
- [[security-and-sandboxing]] - Kryptografie, Passwort-Hashing, vm-Sandbox, Macaroons vs. JWT
- [Performance-Optimierung](performance-optimization.md) - Reduzierung von Round-Trips, Map vs. Object, Buffer-Optimierung, DSL vs. imperativ
