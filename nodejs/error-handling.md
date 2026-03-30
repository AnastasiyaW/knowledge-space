---
title: Error Handling
category: concepts
tags: [error, exception, try-catch, operational, programmer, domains, result-type]
---
# Error Handling

Node.js distinguishes operational errors (expected failures like network timeouts) from programmer errors (bugs like null dereference). Different async patterns require different error propagation strategies.

## Key Facts

- **Operational errors**: recoverable, expected (ECONNREFUSED, ENOENT, timeout, validation) - handle gracefully
- **Programmer errors**: bugs (TypeError, undefined access, wrong arguments) - crash and restart
- Error-first callback pattern: `callback(err, data)` - always check `err` first
- In Promises: rejections propagate through the chain until caught by `.catch()` or `try/catch` with `await`
- Synchronous code: use `try/catch`; async code: `try/catch` with `await` or `.catch()`
- `process.on('uncaughtException', handler)` - last resort; process state may be corrupted, log and exit
- `process.on('unhandledRejection', handler)` - catches unhandled Promise rejections; in Node 15+ this terminates the process by default
- Custom error classes should extend `Error` and set `this.name` and `this.code`
- `Error.captureStackTrace(this, Constructor)` removes the constructor frame from the stack trace
- Aggregate errors: `AggregateError` wraps multiple errors (from `Promise.any()` rejection)
- EventEmitter: unhandled `error` event crashes the process; always add an `error` listener

## Patterns

```javascript
// Custom error hierarchy
class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(entity, id) {
    super(`${entity} ${id} not found`, 'NOT_FOUND', 404);
  }
}

class ValidationError extends AppError {
  constructor(details) {
    super('Validation failed', 'VALIDATION', 400);
    this.details = details;
  }
}

// Async error handling
async function getUser(id) {
  const user = await db.findById(id);
  if (!user) throw new NotFoundError('User', id);
  return user;
}

// Express error middleware
app.use((err, req, res, next) => {
  const status = err.statusCode || 500;
  const body = {
    error: err.code || 'INTERNAL',
    message: status < 500 ? err.message : 'Internal server error',
  };
  if (err instanceof ValidationError) {
    body.details = err.details;
  }
  res.status(status).json(body);
});

// Safe wrapper (eliminates try/catch repetition)
function tryCatch(fn) {
  return async function (req, res, next) {
    try {
      await fn(req, res, next);
    } catch (err) {
      next(err);
    }
  };
}
app.get('/users/:id', tryCatch(async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
}));

// Result type pattern (algebraic, no exceptions)
class Result {
  constructor(ok, value, error) {
    this.ok = ok;
    this.value = value;
    this.error = error;
  }
  static success(value) { return new Result(true, value, null); }
  static failure(error) { return new Result(false, null, error); }

  map(fn) {
    return this.ok ? Result.success(fn(this.value)) : this;
  }
  unwrap() {
    if (!this.ok) throw this.error;
    return this.value;
  }
}

async function safeParse(json) {
  try {
    return Result.success(JSON.parse(json));
  } catch (e) {
    return Result.failure(e);
  }
}

// Process-level handlers (safety net only)
process.on('uncaughtException', (err) => {
  console.error('FATAL:', err);
  process.exit(1); // always exit after uncaughtException
});

process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
  process.exit(1);
});
```

## Gotchas

- **Symptom**: EventEmitter crashes the process - **Cause**: no `error` event listener; Node throws unhandled `error` events - **Fix**: always add `.on('error', handler)` to every EventEmitter
- **Symptom**: error swallowed silently - **Cause**: `.catch(() => {})` empty handler or missing `await` on async function - **Fix**: log or re-throw; never ignore errors
- **Symptom**: stack trace missing useful frames - **Cause**: async stack traces can be fragmented across event loop turns - **Fix**: use `--enable-source-maps` flag; set meaningful error messages; `Error.captureStackTrace`
- **Symptom**: `try/catch` does not catch async error - **Cause**: forgot `await` on the Promise - **Fix**: always `await` the Promise inside `try/catch`

## See Also

- [[async-patterns]] - error propagation in Promises and async/await
- [[algebraic-types]] - Result/Maybe/Either containers as alternative to exceptions
- [[event-loop]] - uncaughtException behavior in the loop
- [Node.js Error docs](https://nodejs.org/api/errors.html)
- [Node.js error handling best practices](https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production#error-handling)
