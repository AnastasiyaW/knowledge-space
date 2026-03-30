---
title: Concurrency Patterns
category: architecture
tags: [concurrency, mutex, semaphore, rate-limit, queue, pool, atomics, race-condition]
---
# Concurrency Patterns

While Node.js is single-threaded for JS execution, concurrency issues arise from async interleaving, shared resources, and multi-thread/process architectures. These patterns manage concurrent access to resources.

## Key Facts

- Node.js async code is concurrent (interleaved) but not parallel (unless using [[worker-threads]])
- **Race condition**: two async operations read-modify-write shared state; last write wins
- **Mutex** (mutual exclusion): ensures only one async operation accesses a resource at a time
- **Semaphore**: like mutex but allows N concurrent accessors (connection pool, rate limiter)
- **Queue**: serialize async operations; process one at a time (or N at a time with concurrency limit)
- Even in single-threaded code, `await` yields control, allowing other code to run and modify shared state
- `Atomics` and `SharedArrayBuffer` provide true thread-safe primitives for [[worker-threads]]
- **Debounce**: delay execution until input stops for N ms (search input, resize events)
- **Throttle**: execute at most once per N ms (scroll, API rate limits)
- Connection pooling (pg, redis) is a semaphore pattern: fixed pool of reusable connections
- `AbortController`/`AbortSignal` (Node 16+) for cooperative cancellation of async operations
- Avoid starvation: ensure all waiting operations eventually get their turn

## Patterns

```javascript
// Async Mutex (single-threaded, protects against interleaved awaits)
class Mutex {
  #queue = [];
  #locked = false;

  async acquire() {
    if (this.#locked) {
      await new Promise(resolve => this.#queue.push(resolve));
    }
    this.#locked = true;
  }

  release() {
    if (this.#queue.length > 0) {
      const next = this.#queue.shift();
      next(); // wake up next waiter
    } else {
      this.#locked = false;
    }
  }

  async runExclusive(fn) {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

const dbMutex = new Mutex();
// Prevents race condition on read-modify-write
async function incrementCounter(id) {
  return dbMutex.runExclusive(async () => {
    const row = await db.query('SELECT count FROM counters WHERE id = $1', [id]);
    const newCount = row.count + 1;
    await db.query('UPDATE counters SET count = $1 WHERE id = $2', [newCount, id]);
    return newCount;
  });
}

// Semaphore (concurrency limiter)
class Semaphore {
  #permits;
  #queue = [];

  constructor(permits) { this.#permits = permits; }

  async acquire() {
    if (this.#permits > 0) {
      this.#permits--;
      return;
    }
    await new Promise(resolve => this.#queue.push(resolve));
  }

  release() {
    if (this.#queue.length > 0) {
      this.#queue.shift()();
    } else {
      this.#permits++;
    }
  }
}

// Rate-limited API calls
const apiSemaphore = new Semaphore(5); // 5 concurrent requests max
async function rateLimitedFetch(url) {
  await apiSemaphore.acquire();
  try {
    return await fetch(url);
  } finally {
    apiSemaphore.release();
  }
}

// Debounce
function debounce(fn, ms) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), ms);
  };
}

// Throttle
function throttle(fn, ms) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= ms) {
      lastCall = now;
      return fn.apply(this, args);
    }
  };
}

// AbortController for cancellation
async function fetchWithCancel(url, timeoutMs = 5000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

// Task Queue (process N items concurrently)
class TaskQueue {
  #concurrency;
  #running = 0;
  #queue = [];

  constructor(concurrency = 1) { this.#concurrency = concurrency; }

  push(task) {
    return new Promise((resolve, reject) => {
      this.#queue.push({ task, resolve, reject });
      this.#process();
    });
  }

  #process() {
    while (this.#running < this.#concurrency && this.#queue.length > 0) {
      const { task, resolve, reject } = this.#queue.shift();
      this.#running++;
      task()
        .then(resolve, reject)
        .finally(() => {
          this.#running--;
          this.#process();
        });
    }
  }
}
```

## Gotchas

- **Symptom**: data corruption with concurrent async updates - **Cause**: read-modify-write pattern without mutex; another async op modifies data between read and write - **Fix**: use mutex for critical sections, or use atomic database operations (UPDATE ... SET x = x + 1)
- **Symptom**: AbortController abort() does nothing - **Cause**: the async operation does not check the signal - **Fix**: pass `signal` to APIs that support it (fetch, fs, stream); check `signal.aborted` in custom code
- **Symptom**: deadlock in mutex - **Cause**: acquiring mutex inside code that already holds it (non-reentrant) - **Fix**: use reentrant mutex, or restructure to avoid nested acquisition
- **Symptom**: semaphore permits never released - **Cause**: error in async operation skips `release()` - **Fix**: always release in `finally` block

## See Also

- [[event-loop]] - why async interleaving creates concurrency issues
- [[worker-threads]] - Atomics for true thread-level synchronization
- [[async-patterns]] - Promise.all and concurrency
- [MDN AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
