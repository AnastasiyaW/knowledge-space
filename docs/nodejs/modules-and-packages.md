---
title: Modules and Packages
category: concepts
tags: [nodejs, modules, commonjs, esm, require, import, package-lock, npm]
---

# Modules and Packages

Node.js supports two module systems: CommonJS (`require`/`module.exports`) and ESM (`import`/`export`). Both coexist and will continue to do so indefinitely - removing `require` from Node.js would require a full rewrite. The module system provides built-in singleton behavior, DI capabilities, and scope isolation.

## Key Facts

- `require()` is synchronous, `import` is asynchronous
- Node.js provides good interop between both systems
- Module cache in CommonJS provides singleton behavior by default - `require()` returns the same instance
- In Node.js there is no true global scope for user code - each module is wrapped in a function, creating module-level scope
- In browser JS, all files share one scope unless wrapped in IIFEs or using module bundlers
- `import.meta.url` gives the file URL in ESM; use `createRequire(import.meta.url)` to get `require()` in ESM
- Always commit `package-lock.json` - even patch versions can break things via transitive dependencies

### Modules as DI Alternative

JavaScript module system can replace many DI patterns:
- **Singleton:** module cache returns same instance
- **Strategy:** export object/Map with strategy implementations
- **Configuration:** export config object, import where needed
- **Factory:** export factory functions

## Patterns

### ESM in Node.js with CommonJS Interop

```js
// Using require() inside ESM
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const fs = require('fs'); // CommonJS require inside ESM
```

### Config as Module

```js
// config.js
module.exports = {
  port: 8000,
  db: { host: 'localhost', port: 5432, database: 'app' },
  crypto: { saltLength: 16, keyLength: 64 },
  session: { timeout: 3600000 },
  transport: 'ws', // 'http' or 'ws'
};

// main.js - dynamic transport loading
const config = require('./config');
const transport = require(`./${config.transport}.js`);
```

### Package-lock.json Importance

`package.json` uses semver ranges. Lock file ensures deterministic builds because:
- A dependency can pull in a changed transitive dependency
- Multiple packages may have conflicting version requirements
- A bugfix in one package can inadvertently change behavior another package depends on

## Gotchas

- ESM came from the frontend ecosystem as a unification effort - both CJS and ESM will coexist indefinitely in Node.js
- `require()` returns cached module on second call - mutations to the exported object are visible everywhere
- Circular dependencies work in CJS (partially loaded module returned) but can cause subtle bugs

## See Also

- [[dependency-injection]] - DI vs module system for decoupling
- [[application-architecture]] - how modules fit into layered architecture
- [[solid-and-grasp]] - SRP applied to module design
