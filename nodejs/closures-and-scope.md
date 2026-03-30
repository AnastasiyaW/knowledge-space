---
title: Closures and Scope
category: language
tags: [closure, scope, lexical, hoisting, iife, encapsulation, context]
---
# Closures and Scope

A closure is a function that retains access to its lexical scope even after the outer function has returned. Closures are the foundation of encapsulation, factories, middlewares, and most Node.js patterns.

## Key Facts

- **Lexical scope**: variables are resolved based on where functions are defined, not where they are called
- A closure captures the **binding** (reference to variable), not the **value** at creation time
- JavaScript has 4 scope levels: global, module, function, block (`let`/`const` in `{}`)
- `var` is function-scoped; `let`/`const` are block-scoped (introduced in ES6)
- **Hoisting**: `var` declarations move to the top of their function; `let`/`const` exist in a "temporal dead zone" (TDZ) from block start until declaration
- Function declarations are hoisted fully (callable before definition); function expressions are not
- IIFE (Immediately Invoked Function Expression) creates a private scope: `(function() { ... })()`
- Closures in loops with `var` capture the same variable (classic bug); `let` creates a new binding per iteration
- In Node.js, each file is wrapped in a function: `(function(exports, require, module, __filename, __dirname) { ... })` - this is why top-level `var` is module-scoped, not global
- Arrow functions inherit `this` from the enclosing lexical scope (no own `this`)

## Patterns

```javascript
// Basic closure - counter
function createCounter(initial = 0) {
  let count = initial;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}
const counter = createCounter(10);
counter.increment(); // 11
// count is inaccessible from outside

// Factory with closure (middleware pattern)
function createLogger(prefix) {
  return function log(message) {
    console.log(`[${prefix}] ${new Date().toISOString()}: ${message}`);
  };
}
const dbLog = createLogger('DB');
dbLog('Connected'); // [DB] 2025-...: Connected

// Closure pitfall with var in loops
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3 (all reference same `i`)

// Fix with let
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2 (each iteration has own `i`)

// Module pattern via closure
const cache = (() => {
  const store = new Map();
  return {
    get: (key) => store.get(key),
    set: (key, val) => store.set(key, val),
    has: (key) => store.has(key),
    clear: () => store.clear(),
    get size() { return store.size; },
  };
})();

// Partial application via closure
function partial(fn, ...presetArgs) {
  return function (...laterArgs) {
    return fn(...presetArgs, ...laterArgs);
  };
}
const add = (a, b) => a + b;
const add10 = partial(add, 10);
add10(5); // 15

// Closure for memoization
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

## Gotchas

- **Symptom**: all callbacks in a loop produce the same value - **Cause**: `var` is function-scoped; loop body shares one binding - **Fix**: use `let` or wrap in IIFE
- **Symptom**: memory leak from closures holding references to large objects - **Cause**: closure captures entire scope, including unneeded variables - **Fix**: nullify large variables after use; restructure to minimize captured scope
- **Symptom**: `this` is undefined in a callback - **Cause**: regular functions have dynamic `this`; callback loses context - **Fix**: use arrow function (lexical `this`) or `.bind()`
- **Symptom**: temporal dead zone error with `let`/`const` - **Cause**: accessing variable before its declaration in the block - **Fix**: move variable access after declaration

## See Also

- [[prototypes-and-classes]] - closures vs class-based encapsulation
- [[design-patterns-gof]] - many GoF patterns use closures in JS
- [[modules-and-packages]] - Node.js module wrapper is itself a closure
- [MDN Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
