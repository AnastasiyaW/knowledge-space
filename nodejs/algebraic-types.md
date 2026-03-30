---
title: Algebraic and Container Types
category: patterns
tags: [result, maybe, either, sum-type, monad, container, error-handling, functional]
---
# Algebraic and Container Types

Algebraic types (Result, Maybe, Either) bring type-safe error handling and null elimination to JavaScript/TypeScript. Instead of throwing exceptions or returning null, wrap values in containers that force callers to handle both success and failure paths.

## Key Facts

- **Maybe** (Option): represents a value that may or may not exist; eliminates `null`/`undefined` checks
- **Result** (Either): represents success or failure; replaces exceptions for expected errors
- **Sum types**: a type that can be one of several variants (like `Result<T, E> = Ok<T> | Err<E>`)
- In TypeScript, sum types are modeled with discriminated unions: `{ tag: 'ok', value: T } | { tag: 'err', error: E }`
- Container types are **composable**: `.map()`, `.flatMap()` (chain), `.unwrap()`, `.match()`
- **Railway-oriented programming**: chain operations that may fail; first failure short-circuits the chain
- Algebraic types make error handling **explicit** in the function signature (no hidden throws)
- JavaScript has no built-in Result/Maybe; libraries: `neverthrow`, `fp-ts`, `effect`, or roll your own (50 lines)
- Key advantage over try/catch: errors are values, not control flow; compose with `map`/`chain`
- TypeScript's strict mode + Result type = exhaustive error handling at compile time
- Combines well with [[dependency-injection]] - services return `Result` instead of throwing

## Patterns

```javascript
// Minimal Result implementation
class Result {
  #ok; #value; #error;

  constructor(ok, value, error) {
    this.#ok = ok;
    this.#value = value;
    this.#error = error;
    Object.freeze(this);
  }

  static ok(value) { return new Result(true, value, null); }
  static err(error) { return new Result(false, null, error); }

  get isOk() { return this.#ok; }
  get isErr() { return !this.#ok; }

  map(fn) {
    return this.#ok ? Result.ok(fn(this.#value)) : this;
  }

  flatMap(fn) {
    return this.#ok ? fn(this.#value) : this;
  }

  mapErr(fn) {
    return this.#ok ? this : Result.err(fn(this.#error));
  }

  unwrap() {
    if (!this.#ok) throw new Error(`Unwrap on Err: ${this.#error}`);
    return this.#value;
  }

  unwrapOr(defaultValue) {
    return this.#ok ? this.#value : defaultValue;
  }

  match({ ok, err }) {
    return this.#ok ? ok(this.#value) : err(this.#error);
  }
}

// Usage: parsing without exceptions
function safeParseJSON(str) {
  try {
    return Result.ok(JSON.parse(str));
  } catch (e) {
    return Result.err(`Invalid JSON: ${e.message}`);
  }
}

function extractField(obj, field) {
  return field in obj
    ? Result.ok(obj[field])
    : Result.err(`Missing field: ${field}`);
}

// Railway-oriented: chain operations
const result = safeParseJSON('{"name": "Alice", "age": 30}')
  .flatMap(obj => extractField(obj, 'name'))
  .map(name => name.toUpperCase());

result.match({
  ok: (name) => console.log(`Hello, ${name}`),
  err: (error) => console.error(`Failed: ${error}`),
});

// Maybe type
class Maybe {
  #value;
  constructor(value) { this.#value = value; }

  static of(value) {
    return value == null ? Maybe.none() : new Maybe(value);
  }
  static none() { return new Maybe(null); }

  get isNone() { return this.#value == null; }

  map(fn) {
    return this.isNone ? this : Maybe.of(fn(this.#value));
  }

  flatMap(fn) {
    return this.isNone ? this : fn(this.#value);
  }

  unwrapOr(defaultValue) {
    return this.isNone ? defaultValue : this.#value;
  }
}

// Safe nested property access
const city = Maybe.of(user)
  .map(u => u.address)
  .map(a => a.city)
  .unwrapOr('Unknown');

// TypeScript: discriminated union (compile-time exhaustiveness)
// type Result<T, E> = { tag: 'ok'; value: T } | { tag: 'err'; error: E };
// function divide(a: number, b: number): Result<number, string> {
//   if (b === 0) return { tag: 'err', error: 'Division by zero' };
//   return { tag: 'ok', value: a / b };
// }

// Async Result
async function safeAsync(fn) {
  try {
    return Result.ok(await fn());
  } catch (e) {
    return Result.err(e);
  }
}

const data = await safeAsync(() => fetch('/api/data').then(r => r.json()));
data.match({
  ok: (d) => renderData(d),
  err: (e) => showError(e),
});
```

## Gotchas

- **Symptom**: Result chains become deeply nested - **Cause**: mixing Result with try/catch or Promises - **Fix**: use `flatMap` consistently; convert Promise rejections to Result at boundaries
- **Symptom**: TypeScript doesn't narrow the type after `isOk` check - **Cause**: method return type not narrowing properly - **Fix**: use discriminated unions with `tag` field, or use `neverthrow` library with proper type guards
- **Symptom**: performance overhead from wrapping every value - **Cause**: creating objects for every operation - **Fix**: use Result at service boundaries, not inside tight loops; for hot paths, use plain returns
- **Symptom**: team unfamiliar with algebraic types, code hard to read - **Cause**: paradigm shift from imperative error handling - **Fix**: introduce gradually; wrap only critical paths first; document patterns

## See Also

- [[nodejs/error-handling]] - traditional exception-based approach vs algebraic types
- [[typescript-integration]] - discriminated unions for compile-time safety
- [neverthrow - Result for TypeScript](https://github.com/supermacro/neverthrow)
- [Railway Oriented Programming](https://fsharpforfunandprofit.com/rop/)
