---
title: JavaScript Async and Fetch API
category: concepts
tags: [web-frontend, javascript, async, promises, fetch, api]
---

# JavaScript Async and Fetch API

JavaScript is single-threaded. Async operations (network, timers) execute in the background and notify via callbacks, Promises, or async/await.

## Event Loop

1. **Call Stack**: synchronous code
2. **Web APIs**: handle async (setTimeout, fetch, DOM events)
3. **Microtask Queue**: Promise callbacks (higher priority)
4. **Task Queue**: setTimeout, setInterval callbacks
5. **Event Loop**: moves tasks to stack when empty

Microtasks (Promises) run BEFORE macrotasks (setTimeout).

```javascript
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("sync");
// Output: sync, promise, timeout
```

## Promises

A Promise represents a future value: pending -> fulfilled or rejected.

```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    if (success) resolve("Data");
    else reject(new Error("Failed"));
  }, 1000);
});

promise
  .then(data => transform(data))
  .then(result => console.log(result))
  .catch(error => console.error(error))
  .finally(() => console.log("Done"));
```

### Static Methods
```javascript
// Wait for ALL to fulfill (or first rejection)
Promise.all([p1, p2, p3]).then(([r1, r2, r3]) => { });

// Wait for ALL to settle
Promise.allSettled([p1, p2]).then(results => {
  results.forEach(r => console.log(r.status, r.value || r.reason));
});

// First to fulfill (ignores rejections unless ALL reject)
Promise.any([p1, p2, p3]);

// First to settle (fulfill or reject)
Promise.race([p1, p2, p3]);

Promise.resolve("value")
Promise.reject(new Error("reason"))
```

## async/await

Syntactic sugar over Promises - async code looks synchronous.

```javascript
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed:", error);
    throw error;
  }
}
```

### Parallel Execution
```javascript
// Sequential (slow)
const user = await fetchUser(1);
const posts = await fetchPosts(1);

// Parallel (fast)
const [user, posts] = await Promise.all([
  fetchUser(1),
  fetchPosts(1)
]);
```

## Fetch API

```javascript
// GET
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// POST
await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Alice", age: 25 })
});

// DELETE, PATCH
await fetch("/api/users/1", { method: "DELETE" });
await fetch("/api/users/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Updated" })
});
```

### Response Object
```javascript
response.ok          // true for 200-299
response.status      // HTTP code
response.headers

// Body (can only read ONCE)
await response.json()      // Parse JSON
await response.text()      // Plain text
await response.blob()      // Binary
await response.formData()
```

### Error Handling
**fetch does NOT throw on HTTP errors** (404, 500). Only throws on network failure.

```javascript
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) console.error("Network error");
    else console.error("Request failed:", error);
  }
}
```

### Abort / Timeout
```javascript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal: controller.signal });
} catch (error) {
  if (error.name === "AbortError") console.error("Timed out");
} finally {
  clearTimeout(timeout);
}
```

### FormData Upload
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);
await fetch("/upload", {
  method: "POST",
  body: formData  // Content-Type set automatically
});
```

## Gotchas

- **fetch doesn't throw on 404/500**: must check `response.ok` manually
- **Response body read once**: calling `.json()` twice throws; store the result
- **`setTimeout(fn, 0)` isn't instant**: deferred to next event loop tick (after microtasks)
- **Missing `await`**: forgetting `await` returns a Promise object, not the value
- **Race conditions**: component unmounts during fetch; check cancellation flag or use AbortController
- **Promise.all fails fast**: one rejection rejects all; use `allSettled` if you need all results

## See Also

- [[js-functions]] - Callbacks, higher-order functions
- [[js-dom-and-events]] - DOM events are async
- [[react-state-and-hooks]] - useEffect for data fetching
- [[typescript-fundamentals]] - Typing async functions
- [[nodejs]] - Server-side async patterns
