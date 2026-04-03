---
title: Error Handling
category: concepts
tags: [nodejs, errors, aggregate-error, error-cause, app-error, fail-fast]
---

# Error Handling

Effective error handling in Node.js distinguishes between application errors (business logic violations) and system errors (infrastructure failures). The fail-fast pattern, custom error classes, and modern error chaining features (AggregateError, Error.cause) provide structured error propagation.

## Key Facts

- Always separate application errors from system errors - never expose system error details to clients
- `AggregateError` combines multiple errors into one (missing file + expired cache + invalid key)
- `Error.cause` chains errors for causal tracking (added in ES2022)
- Both consume memory - keep chains short
- `EventEmitter({ captureRejections: true })` catches async callback errors automatically (Node.js only)
- Logical errors (code runs without throwing but produces wrong results) are the most dangerous - no error message to find

## Error Types

### Application Errors vs System Errors

```js
class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

// In request handler:
if (err instanceof AppError) {
  reply(err.code, err.message); // 4xx - safe to expose
} else {
  reply(500, 'Internal error');  // Don't expose system errors
}
```

### Error Chaining

```js
// AggregateError - multiple simultaneous failures
throw new AggregateError([err1, err2, err3], 'Multiple failures');

// Error.cause - causal chain
throw new Error('Operation failed', { cause: originalError });
```

## Patterns

### Fail Fast / Return Early

```js
async function processUser(id) {
  if (!id) throw new Error('ID required');
  const user = await db.find(id);
  if (!user) throw new Error('User not found');
  // ... proceed with happy path only
}
```

### Simplified Error Response Extraction

```js
// Before: duplicated error handling
try {
  const result = await process();
  reply(200, result);
} catch (err) {
  if (err instanceof AppError) reply(err.code, err.message);
  else reply(500, 'Error');
}

// After: extract error code/message pair
const getErrorResponse = (err) =>
  err instanceof AppError
    ? [err.code, err.message]
    : [500, 'Internal error'];
```

### Sandbox Error Isolation

```js
const vm = require('vm');
const context = vm.createContext({
  AppError,
  // Only expose safe APIs to untrusted code
});
const result = vm.runInContext(userCode, context, { timeout: 5000 });
// instanceof AppError distinguishes app errors from system errors
```

## Gotchas

- Go-style error returns `{ error, data }` in JS is an anti-pattern: loses structured error propagation, breaks async stack traces
- Hardcoded values (file paths, line endings, buffer sizes) should be parameters, not magic strings - except `-1` for "not found" and `0` for first index (language conventions)
- AggregateError arrays and cause chains need to be unwound during debugging - keep them short

## See Also

- [[async-patterns]] - error handling in async code, captureRejections
- [[security-and-sandboxing]] - vm module and safe error propagation
- [[application-architecture]] - error handling layers in server architecture
