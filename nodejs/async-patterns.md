---
title: Async Patterns
category: concepts
tags: [async, await, promise, callback, error-first, concurrency, async-iterator]
---
# Async Patterns

Node.js async programming evolved through three eras: callbacks (error-first convention), Promises, and async/await. Understanding all three is essential because legacy APIs, library internals, and modern code intermix them.

## Key Facts

- **Error-first callback**: `(err, result) => {}` - the foundational Node.js pattern; `err` is always the first argument
- **Promise** wraps an eventual result; states: pending -> fulfilled/rejected; immutable once settled
- `async function` always returns a Promise; `await` pauses execution until the Promise settles
- `Promise.all([p1, p2])` - parallel execution, rejects on first failure (fast-fail)
- `Promise.allSettled([p1, p2])` - parallel, waits for all, returns `{status, value/reason}` for each
- `Promise.race([p1, p2])` - resolves/rejects with the first settled promise
- `Promise.any([p1, p2])` - resolves with first fulfilled; rejects only if ALL reject (AggregateError)
- `util.promisify(fn)` converts error-first callback API to Promise-based
- `for await (const chunk of asyncIterable)` - async iteration over streams, paginated APIs
- Unhandled promise rejections terminate the process since Node.js v15+ (`unhandledRejection` event)
- Top-level `await` works in ES modules (`.mjs` or `"type": "module"` in package.json)
- `Promise.withResolvers()` (ES2024) returns `{ promise, resolve, reject }` - useful for bridging callback APIs

## Patterns

```javascript
// Error-first callback (legacy)
const fs = require('fs');
fs.readFile('/path', 'utf8', (err, data) => {
  if (err) return console.error(err);
  console.log(data);
});

// Promisify callback API
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
// or use fs.promises directly:
const { readFile } = require('fs').promises;

// async/await with proper error handling
async function loadConfig(path) {
  try {
    const data = await readFile(path, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') return {}; // default config
    throw err; // re-throw unexpected errors
  }
}

// Parallel execution
async function fetchAll(urls) {
  const results = await Promise.all(
    urls.map(url => fetch(url).then(r => r.json()))
  );
  return results;
}

// Parallel with error tolerance
async function fetchAllSafe(urls) {
  const results = await Promise.allSettled(
    urls.map(url => fetch(url).then(r => r.json()))
  );
  return results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);
}

// Concurrency limiter (no external deps)
async function pMap(items, fn, concurrency = 5) {
  const results = [];
  const executing = new Set();
  for (const [i, item] of items.entries()) {
    const p = fn(item, i).then(r => {
      executing.delete(p);
      return r;
    });
    executing.add(p);
    results.push(p);
    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }
  return Promise.all(results);
}

// Async iterator for paginated API
async function* fetchPages(baseUrl) {
  let page = 1;
  while (true) {
    const res = await fetch(`${baseUrl}?page=${page}`);
    const data = await res.json();
    if (data.items.length === 0) return;
    yield* data.items;
    page++;
  }
}
for await (const item of fetchPages('/api/users')) {
  process.stdout.write(item.name + '\n');
}

// Promise.withResolvers (ES2024)
function createDeferred() {
  const { promise, resolve, reject } = Promise.withResolvers();
  return { promise, resolve, reject };
}

// Timeout wrapper
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

## Gotchas

- **Symptom**: unhandled promise rejection crashes the process - **Cause**: missing `.catch()` or `try/catch` around `await` - **Fix**: always handle errors; add global `process.on('unhandledRejection', handler)` as safety net
- **Symptom**: `await` in a `forEach` does not wait - **Cause**: `Array.forEach` ignores return values (Promises) - **Fix**: use `for...of` loop or `Promise.all(arr.map(async ...))`
- **Symptom**: sequential execution when parallel is intended - **Cause**: `await` inside a loop serializes calls - **Fix**: collect promises first, then `await Promise.all(promises)`
- **Symptom**: memory grows with large parallel Promise.all - **Cause**: all results held in memory simultaneously - **Fix**: use concurrency limiter or async iterator pattern

## See Also

- [[event-loop]] - the runtime that drives async execution
- [[nodejs/error-handling]] - error propagation in async code
- [[streams]] - streaming alternative to buffered async
- [Node.js async/await guide](https://nodejs.org/en/learn/asynchronous-work/modern-asynchronous-javascript)
- [MDN Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
