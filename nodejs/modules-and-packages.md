---
title: Modules and Packages
category: concepts
tags: [modules, commonjs, esm, require, import, package-json, node-modules, resolution]
---
# Modules and Packages

Node.js has two module systems: the original CommonJS (`require`/`module.exports`) and the standard ECMAScript Modules (`import`/`export`). Understanding both and their interop is critical for any Node.js project.

## Key Facts

- **CommonJS (CJS)**: synchronous `require()`, `module.exports` / `exports`, runs at load time
- **ES Modules (ESM)**: async `import`/`export`, static analysis, tree-shaking, top-level `await`
- ESM is the standard; CJS is the legacy default. Node determines format by: `.mjs`/`.cjs` extension, or `"type": "module"/"commonjs"` in package.json
- Each CJS module is wrapped in: `(function(exports, require, module, __filename, __dirname) { ... })`
- `require()` has a **cache** (`require.cache`): modules are loaded once and cached by resolved filename
- `require.resolve(id)` returns the resolved path without executing the module
- CJS can `require()` ESM only via dynamic `import()` (returns Promise)
- ESM can import CJS via default import: `import pkg from 'cjs-package'`; named imports may not work
- `__dirname` / `__filename` are CJS-only; in ESM use `import.meta.url` and `import.meta.dirname` (Node 21+)
- **Conditional exports** in package.json: `"exports"` field maps subpaths and conditions (`import`, `require`, `default`)
- Node.js resolution algorithm: exact file -> file + extension (.js, .json, .node) -> directory (package.json main / index.js)
- `node_modules` resolution: walks up directory tree looking for `node_modules/` at each level

## Patterns

```javascript
// CommonJS
// math.js
const add = (a, b) => a + b;
const multiply = (a, b) => a * b;
module.exports = { add, multiply };

// app.js
const { add, multiply } = require('./math');

// ES Modules
// math.mjs
export const add = (a, b) => a + b;
export const multiply = (a, b) => a * b;
export default { add, multiply };

// app.mjs
import { add, multiply } from './math.mjs';
import math from './math.mjs';

// Dual CJS/ESM package (package.json)
{
  "name": "my-lib",
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    },
    "./utils": {
      "import": "./dist/utils.mjs",
      "require": "./dist/utils.cjs"
    }
  }
}

// Dynamic import (works in both CJS and ESM)
const { default: chalk } = await import('chalk');

// Module factory pattern (for testability)
function createService(db, logger) {
  return {
    async getUser(id) {
      logger.info(`Fetching user ${id}`);
      return db.findById(id);
    }
  };
}
module.exports = createService;

// Clearing require cache (for hot-reload in dev)
function clearModule(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
}

// __dirname equivalent in ESM
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const configPath = join(__dirname, 'config.json');

// Node 21+: simpler
const dir = import.meta.dirname;
```

## Gotchas

- **Symptom**: `require is not defined` in ESM - **Cause**: CJS globals don't exist in ES modules - **Fix**: use `import`/`export`; or use `createRequire` from `module` for edge cases
- **Symptom**: `ERR_REQUIRE_ESM` - **Cause**: trying to `require()` an ES module package - **Fix**: use dynamic `import()` or switch your package to ESM
- **Symptom**: circular dependency returns empty object - **Cause**: CJS exports are evaluated partially when circular `require()` occurs - **Fix**: restructure to avoid circular deps; or use late binding (access property at call time, not import time)
- **Symptom**: `__dirname is not defined` - **Cause**: using ESM where CJS globals don't exist - **Fix**: use `import.meta.dirname` (Node 21+) or `fileURLToPath(import.meta.url)`

## See Also

- [[closures-and-scope]] - module wrapper is a closure
- [[dependency-injection]] - module factories for testable code
- [[typescript-integration]] - TypeScript module resolution
- [Node.js Modules: CJS](https://nodejs.org/api/modules.html)
- [Node.js Modules: ESM](https://nodejs.org/api/esm.html)
- [Node.js Packages](https://nodejs.org/api/packages.html)
