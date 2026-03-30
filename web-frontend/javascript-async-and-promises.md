---
title: JavaScript Async and Promises
category: javascript
tags: [javascript, async, await, promise, event-loop, fetch, callback]
---

# JavaScript Async and Promises

## Key Facts

- JavaScript is **single-threaded** with an **event loop**; async operations are non-blocking callbacks
- **Event loop order**: call stack -> microtasks (Promises, queueMicrotask) -> macrotasks (setTimeout, I/O, DOM events)
- `Promise` has three states: **pending** -> **fulfilled** (resolved) or **rejected**
- `async function` always returns a Promise; `await` pauses execution until Promise settles
- `Promise.all([p1, p2])` - resolves when ALL resolve; rejects on first rejection
- `Promise.allSettled([p1, p2])` - waits for all to settle; never rejects; returns `[{status, value/reason}]`
- `Promise.race([p1, p2])` - resolves/rejects with first settled promise
- `fetch()` returns a Promise; response body methods (`json()`, `text()`) also return Promises
- `AbortController` cancels fetch requests and other async operations
- Related: [[javascript-fundamentals]], [[javascript-dom-and-events]]

## Patterns

### Async/Await with Error Handling

```javascript
async function fetchUser(id) {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Failed to fetch user:", err.message);
    throw err; // re-throw for caller to handle
  }
}
```

### Parallel Execution

```javascript
// Parallel - all start immediately
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);

// Sequential - each waits for previous (slower, use when dependent)
const user = await fetchUser(id);
const posts = await fetchPosts(user.id);
```

### Fetch with Timeout via AbortController

```javascript
async function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);

  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timeout);
  }
}
```

### Promise.allSettled for Graceful Degradation

```javascript
const results = await Promise.allSettled([
  fetchCritical(),
  fetchOptional(),
  fetchAnalytics(),
]);

const data = results
  .filter(r => r.status === "fulfilled")
  .map(r => r.value);

const errors = results
  .filter(r => r.status === "rejected")
  .map(r => r.reason);
```

### Retry Pattern

```javascript
async function retry(fn, maxAttempts = 3, delay = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxAttempts) throw err;
      await new Promise(r => setTimeout(r, delay * attempt));
    }
  }
}
```

## Gotchas

- `await` in a `forEach` does NOT wait: iterations run in parallel; use `for...of` or `for await...of` for sequential async loops
- Unhandled Promise rejections crash Node.js (v15+) and log warnings in browsers; always `.catch()` or `try/catch`
- `fetch()` does NOT reject on HTTP errors (404, 500); check `response.ok` or `response.status`
- `return await promise` inside `try/catch` is necessary to catch rejection; `return promise` bypasses the catch block
- Microtasks (Promise callbacks) execute before the next macrotask; a long chain of microtasks blocks rendering

## See Also

- [MDN: Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN: async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)
