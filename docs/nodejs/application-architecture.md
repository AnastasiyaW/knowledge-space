---
title: Application Architecture
category: concepts
tags: [nodejs, architecture, ddd, layers, transport, context-isolation, server-structure]
---

# Application Architecture

Node.js application architecture centers on layer separation, transport abstraction, and context isolation. The DDD-inspired structure keeps business logic pure, transport-agnostic, and schema-driven. The #1 challenge for developers is not framework knowledge or async patterns - it's structuring the application.

## Key Facts

- Business logic must be pure - no I/O, no framework dependencies
- Transport layer only differs in how data is sent/received (HTTP vs WebSocket vs gRPC)
- Schema-driven development: define schemas first, generate DB tables, validators, types, docs, SDKs
- Schemas as single source of truth prevent drift between layers
- Config determines transport at runtime - enables A/B testing different protocols
- Same chat app implemented across Pure Node.js, Fastify, NestJS, and Metarhia demonstrates that domain logic stays identical, only framework boilerplate differs

## Four Context Levels

Node.js servers need isolated state at four levels with different lifetimes:

```text
Application Context (global, persistent)
  └─ Session Context (per-user, persistent, TTL)
      └─ Connection Context (per-socket, transient)
          └─ Call Context (per-request, shortest-lived)
```

1. **Call context** - one request/RPC call. Request/response objects. Destroyed after response
2. **Connection context** - one TCP/WebSocket connection. Metadata. Destroyed on disconnect
3. **Session context** - persists across connections (backed by DB). Authentication, configurable TTL
4. **Application context** - global singleton. Configuration, caches, connection pools

### Implementation with Private Fields

```js
class Context {
  #session;
  #connection;
  #call;

  constructor(session, connection) {
    this.#session = session;
    this.#connection = connection;
  }

  startCall(request) {
    this.#call = { request, startTime: Date.now() };
    return this;
  }
}
```

Modern Node.js (16+): use `#privateField` syntax instead of closures or Symbol-based privacy.

## Patterns

### Transport Abstraction

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js
const transport = require(`./${config.transport}.js`);
// Domain logic is transport-agnostic
```

### Per-Request Context (Fastify)

```js
fastify.addHook('preHandler', (request) => {
  request.context = {
    logger: createLogger({ requestId: request.id }),
    db: connectionPool,
  };
});

async function transferMoney(context, from, to, amount) {
  const tx = await context.db.beginTransaction();
  // All queries use same connection; logger auto-injects requestId
  await tx.commit();
}
```

Logger gets `request.id` automatically - every log entry traceable without manual threading.

### Scaffold - Dynamic API Client

```js
const scaffold = (url, structure) => {
  const api = {};
  for (const [entity, methods] of Object.entries(structure)) {
    api[entity] = {};
    for (const method of methods) {
      api[entity][method] = (...args) =>
        fetch(`${url}/${entity}/${method}`, {
          method: 'POST', body: JSON.stringify(args),
        }).then(r => r.json());
    }
  }
  return api;
};
```

## Technical Debt Management

- If you feel something is wrong but don't know the proper fix, DON'T rewrite yet - learn proper patterns first
- Introduce improvements incrementally with each new feature
- Write new code properly even if surrounding code is messy
- If you're not the tech lead, it's not your responsibility to push for refactoring

## Gotchas

- Functional vs OOP: most business tasks should use procedural style; Angular aligns with GoF/SOLID, React leans functional
- Overengineering (strict DDD) is as harmful as underengineering (God objects) - the sweet spot is declarative schema + universal patterns
- ESLint shared config (single repo for rules shared across all project repos) prevents style drift

## See Also

- [[dependency-injection]] - DI vs modules for decoupling layers
- [[data-access-patterns]] - DAL as a separate architecture layer
- [[design-patterns-gof]] - patterns for layer isolation (Adapter, Facade, Proxy)
- [[modules-and-packages]] - how module system supports architecture
