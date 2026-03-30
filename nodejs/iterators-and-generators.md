---
title: Iterators and Generators
category: language
tags: [iterator, generator, yield, symbol-iterator, async-generator, lazy-evaluation, iterable]
---
# Iterators and Generators

Iterators provide a standard protocol for sequentially accessing elements. Generators are functions that can pause and resume, producing values lazily. Together with async iterators, they enable memory-efficient processing of unbounded sequences.

## Key Facts

- **Iterator protocol**: object with `.next()` method returning `{ value, done }`
- **Iterable protocol**: object with `[Symbol.iterator]()` method that returns an iterator
- `for...of`, spread `[...]`, destructuring, `Array.from()`, `Promise.all()` all consume iterables
- **Generator function**: `function*` - execution pauses at each `yield`; caller drives via `.next()`
- `yield*` delegates to another iterable/generator (composition)
- Generators are both iterators AND iterables
- `.next(value)` sends a value back into the generator (resumes after the paused `yield`)
- `.return(value)` forces generator to finish; `.throw(error)` injects error at the yield point
- **Async generator**: `async function*` + `yield` + can `await`; consumed with `for await...of`
- Generators enable **lazy evaluation**: compute values on demand, not all at once
- Use cases: pagination, infinite sequences, custom iterables, cooperative scheduling, CSP-style channels
- `Symbol.asyncIterator` protocol for async iterables; used by Node.js streams since v10+

## Patterns

```javascript
// Basic generator
function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}
for (const n of range(0, 10, 2)) {
  console.log(n); // 0, 2, 4, 6, 8
}

// Infinite sequence (lazy)
function* fibonacci() {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}
// Take first 10
const first10 = [...take(fibonacci(), 10)];

function* take(iterable, n) {
  let i = 0;
  for (const value of iterable) {
    if (i++ >= n) return;
    yield value;
  }
}

// Generator composition with yield*
function* concat(...iterables) {
  for (const iterable of iterables) {
    yield* iterable;
  }
}
const all = [...concat([1, 2], [3, 4], range(5, 8))]; // [1,2,3,4,5,6,7]

// Two-way communication
function* accumulator() {
  let total = 0;
  while (true) {
    const value = yield total;
    total += value;
  }
}
const acc = accumulator();
acc.next();       // { value: 0, done: false } - init
acc.next(10);     // { value: 10, done: false }
acc.next(20);     // { value: 30, done: false }

// Async generator for paginated API
async function* fetchAllPages(url) {
  let nextUrl = url;
  while (nextUrl) {
    const res = await fetch(nextUrl);
    const data = await res.json();
    yield* data.items;
    nextUrl = data.nextPage || null;
  }
}
for await (const item of fetchAllPages('/api/items?page=1')) {
  await processItem(item);
}

// Custom iterable class
class FileLines {
  #path;
  constructor(path) { this.#path = path; }

  async *[Symbol.asyncIterator]() {
    const rl = require('readline').createInterface({
      input: require('fs').createReadStream(this.#path),
      crlfDelay: Infinity,
    });
    for await (const line of rl) {
      yield line;
    }
  }
}
for await (const line of new FileLines('data.csv')) {
  console.log(line);
}

// Lazy pipeline with generator utilities
function* map(iterable, fn) {
  for (const item of iterable) yield fn(item);
}
function* filter(iterable, pred) {
  for (const item of iterable) if (pred(item)) yield item;
}

const result = [...take(
  filter(
    map(range(0, Infinity), x => x * x),
    x => x % 2 === 0
  ),
  5
)]; // [0, 4, 16, 36, 64]
```

## Gotchas

- **Symptom**: generator does not run - **Cause**: calling `gen()` returns an iterator object; must call `.next()` or use `for...of` - **Fix**: always consume the generator with a loop or spread
- **Symptom**: `for await...of` hangs - **Cause**: async generator never returns/yields and never ends - **Fix**: ensure generator has a termination condition or `return` statement
- **Symptom**: generator's `finally` block not executing - **Cause**: breaking out of `for...of` before generator completes - **Fix**: `for...of` calls `.return()` on break, which does trigger `finally`; check your cleanup logic
- **Symptom**: memory leak with infinite generators - **Cause**: storing all yielded values (e.g., spread into array) - **Fix**: consume lazily with `for...of` or `take()` utility; never spread an infinite generator

## See Also

- [[async-patterns]] - async iterators for paginated data
- [[streams]] - Node.js streams implement the async iterable protocol
- [[closures-and-scope]] - generators capture enclosing scope
- [MDN Iterators and generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_Generators)
- [MDN for-await...of](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of)
