---
title: Middleware and HTTP
category: concepts
tags: [nodejs, middleware, http, fastify, express, transport, static-files]
---

# Middleware and HTTP

HTTP handling in Node.js ranges from pure Node.js servers to framework-based approaches (Fastify, NestJS, Metarhia). Middleware implements the Chain of Responsibility pattern, and transport abstraction enables switching between HTTP and WebSocket without changing business logic.

## Key Facts

- Middleware in Express/Fastify is Chain of Responsibility: each handler decides to process or pass to `next()`
- Transport abstraction: HTTP and WebSocket handlers share domain logic, differ only in data transport
- Static file serving: always check file existence before sending (404 vs 500)
- Same application implemented across Pure Node.js, Fastify, NestJS, and Metarhia shows: domain logic identical, only framework boilerplate differs

## Patterns

### Multi-Framework Comparison

```javascript
metatech-university/
  NodeJS-Pure/         # Pure Node.js (no framework)
  NodeJS-Fastify/      # Fastify - lightweight, good DX
  NodeJS-Nest/         # NestJS - enterprise-grade, TypeScript-first
  NodeJS-Metarhia/     # Metarhia - schema-driven, transport-abstracted

All implement: user registration, authentication, session management,
messaging, file upload, room management, push notifications
```

### Transport Config Switching

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js - load transport module dynamically
const transport = require(`./${config.transport}.js`);
// Enables: per-environment transport, A/B testing, fallback mechanisms
```

### ESLint Shared Configuration

```javascript
eslint-config-metarhia/     # Shared rules package
  index.js                  # Rules in JavaScript (not JSON)
  browser.js                # Browser-specific overrides
  node.js                   # Node-specific overrides
```

Each project extends and optionally overrides. Centralized rule management with per-repo flexibility.

## Gotchas

- Pure Node.js server is minimal code but complex to maintain at scale
- Framework choice matters less than architecture quality - all frameworks can produce the same result
- Pull request workflow for infrastructure libraries should stabilize structure before writing tests (avoid test churn)

## See Also

- [[application-architecture]] - transport abstraction, layered server design
- [[design-patterns-gof]] - Chain of Responsibility as middleware pattern
- [[error-handling]] - error handling in request pipelines
