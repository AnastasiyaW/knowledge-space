---
title: Performance Optimization
category: operations
tags: [nodejs, performance, benchmarking, map-vs-object, round-trips, buffer-optimization]
---

# Performance Optimization

Node.js performance optimization focuses on reducing round-trips, choosing efficient data structures, optimizing buffer allocations, and understanding V8 internals. Measurement is mandatory - every application's performance profile is unique.

## Key Facts

- Minimizing round-trips is more important than raw speed
- System A processes 2x faster but requires 50 requests; System B is slower but handles everything in 1 request - System B often wins
- Even on localhost (same machine), socket communication has measurable cost
- Map is consistently faster than Object for 1M+ entries
- Run benchmarks sequentially (not in parallel) to avoid resource contention skewing results
- PostgreSQL can be configured for aggressive in-memory caching, but in-process caching (Node.js Map/Object) avoids even cross-process overhead

## Patterns

### Round-Trip Reduction

```javascript
// BAD: 50 separate requests
for (const id of ids) {
  const user = await api.getUser(id);
}

// GOOD: batch request
const users = await api.getUsers(ids);
```

No serialization/deserialization overhead per request, no network latency, no connection management.

### Buffer Optimization

```js
// Before: two allocations
const header = new Uint8Array(8);
const body = new Uint8Array(data);
const packet = Buffer.concat([header, body]);

// After: single allocation
const packet = Buffer.allocUnsafe(8 + data.length);
packet.writeInt32BE(streamId, 0);
packet.writeInt32BE(data.length, 4);
data.copy(packet, 8);
```

### Map vs Object Benchmarking

```js
// Benchmark methodology:
// - Separate threads for each test
// - Run GC between tests
// - Generate keys once, reuse
// - Run sequentially, not in parallel

const map = new Map();
const obj = Object.create(null);

// For 1M+ entries: Map wins consistently
// Object has overhead from prototype chain and hidden class management
```

### DSL vs Imperative (Performance and Maintainability)

```js
// LLM-generated: verbose imperative IndexedDB code
db.createObjectStore('users', { keyPath: 'id', autoIncrement: true });
const usersStore = transaction.objectStore('users');
usersStore.createIndex('name', 'name', { unique: false });
// ... repeated for every entity

// Human-written DSL: declarative, shorter, reusable, with migrations
const schema = {
  users: { keyPath: 'id', autoIncrement: true,
    indexes: { name: {}, email: { unique: true } } },
};
const db = await openDatabase('myApp', schema);
```

One generic function handles all entities. LLM generates imperative code manually for each store.

## Gotchas

- `Buffer.allocUnsafe()` is faster but contains uninitialized memory - always fill all bytes
- Binary protocols (protobuf-like) outperform JSON in both size and speed for high-frequency data
- Flyweight pattern for timers trades 2 extra CMP instructions (polymorphic dispatch) for millions of saved allocations - always measure the trade-off

## See Also

- [[v8-optimization]] - hidden classes, monomorphic code, JIT internals
- [[streams]] - stream optimization and chunk handling
- [[concurrency-patterns]] - WebSocket batching, binary protocols
- [[event-loop-and-architecture]] - performance factors in Node.js
