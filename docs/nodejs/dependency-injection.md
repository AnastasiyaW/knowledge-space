---
title: Dependency Injection and Coupling
category: concepts
tags: [nodejs, dependency-injection, coupling, modules, layer-isolation, di]
---

# Dependency Injection and Coupling

Coupling occurs whenever one module calls methods, creates instances, or reads/writes properties of another module's entities. In JavaScript, many traditional DI patterns are replaceable by the module system itself. Layer isolation through safe interfaces and unidirectional communication prevents coupling from becoming unmanageable.

## Key Facts

- **Coupling** occurs when one module: calls another's method, creates another's instance, reads/writes another's properties
- JavaScript module cache guarantees single instance per `require()`/`import` - built-in singleton
- Every dependency (import, require, API call) increases coupling - minimize them
- Rule of thumb: don't do metaprogramming in TypeScript - write meta-heavy libraries in JS, provide `.d.ts` declarations

## Module System as DI

| Traditional DI | JS Module Equivalent |
|---------------|---------------------|
| Singleton container | Module cache (`require()` returns same instance) |
| Strategy injection | Exported objects/Maps from modules |
| Config injection | Export config object, import where needed |
| Factory injection | Export factory functions |
| Constructor injection | Pass module references as constructor params |

## Patterns

### Layer Isolation

Layers should interact through safe interfaces (contracts):
- **Unidirectional:** layer A calls layer B, but not vice versa
- **Bidirectional:** both layers call each other (use events/callbacks to avoid circular deps)

Structural patterns for isolation: [[design-patterns-gof]] (convert interfaces), Proxy (control access), Facade (simplify subsystem), Composite (uniform tree traversal).

### Platform Abstraction

Abstract away platform-specific APIs so implementations are swappable:

```js
// Storage abstraction - works on server and browser
const createStorage = (backend) => ({
  async read(key) { return backend.get(key); },
  async write(key, value) { return backend.set(key, value); },
});

// Server: filesystem or S3
const serverStorage = createStorage(new S3Backend(config));
// Browser: OPFS, IndexedDB, or Cache API
const browserStorage = createStorage(new OPFSBackend());
```

Abstract: network protocols (HTTP, WebSocket, gRPC), databases (PostgreSQL, MongoDB), cryptography providers, file storage (local, S3, OPFS, IndexedDB), notification services.

### Schema-Driven Development

Define schemas first, generate everything:
- Database tables
- API validators
- TypeScript types
- Documentation
- Client SDKs

Schemas as single source of truth prevent drift between layers.

## Gotchas

- Singletons via module cache means mutations to exported objects are visible everywhere - can be a feature or a bug
- Circular dependencies work in CJS (partially loaded module returned) but cause subtle initialization issues
- Over-engineering DI in JavaScript leads to Java-style boilerplate without the benefits - use modules first, reach for DI containers only when module system isn't enough

## See Also

- [[modules-and-packages]] - CommonJS vs ESM, module cache behavior
- [[application-architecture]] - how DI fits into layered server architecture
- [[solid-and-grasp]] - Dependency Inversion Principle
- [[data-access-patterns]] - injecting repositories
