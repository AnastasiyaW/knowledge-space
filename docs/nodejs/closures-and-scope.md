---
title: Closures and Scope
category: concepts
tags: [nodejs, javascript, closures, scope, lexical-environment, block-scope, module-scope]
---

# Closures and Scope

A closure is a function that retains a reference to variables from its outer function's scope even after the outer function has finished executing. The closure is a data structure stored on the heap inside the JS runtime - only the inner function can read/write to it. Understanding scope and closures is essential for encapsulation, factory functions, and module design in Node.js.

## Key Facts

- **Scope (visibility area)**: viewed from an identifier's perspective - where it is visible (function, block, module, global scope)
- **Lexical context/environment**: viewed from a position in the program - which identifiers are accessible at that point
- A closure is a heap data structure; there is no external reference - only the inner function can access it
- Similar to `this` in objects, but unlike `this`, you cannot add fields to a closure from outside

### Three Conditions for a Closure

All three must be present simultaneously:
1. An outer function defining variables
2. An inner function referencing those variables
3. The inner function being returned or passed outside

If any part is missing, it is not a full closure. Accessing a global variable from a function is NOT a closure.

### Node.js Module Scope

- Each module is wrapped in a function, creating module-level scope - no true global scope for user code
- In browser JS, all files share one scope unless wrapped in IIFEs or using module bundlers

## Patterns

### Closure-Based Encapsulation

```js
function createCounter(initial = 0) {
  let count = initial; // only accessible through returned methods
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; },
  };
}

const counter = createCounter(10);
counter.increment(); // 11
// counter.count → undefined (truly private)
```

### Block Scope as Inheritance

```js
function processUser(user) {
  let greeting = 'Hello'; // default "base" behavior
  if (user.isVIP) {
    let greeting = 'Welcome, esteemed'; // "override" in nested scope
    console.log(`${greeting} ${user.name}`);
    return;
  }
  console.log(`${greeting} ${user.name}`);
}
```

### Module Wrapping (How Node.js Creates Scope)

```js
// Node.js wraps each module:
// (function(exports, require, module, __filename, __dirname) {
//   ... your module code ...
// });
// This is why top-level variables are module-scoped, not global
```

## Gotchas

- Closures retain references to the entire lexical environment, not just used variables - can cause memory retention
- In loops with `var`, all closures share the same variable; use `let` (block-scoped) for per-iteration scope
- Accessing a global variable from a function is NOT a closure - confusing these leads to architectural misunderstandings

## See Also

- [[v8-optimization]] - how V8 stores closure data structures on the heap
- [[modules-and-packages]] - module wrapping creates the enclosing scope
- [[design-patterns-gof]] - closures as foundation for many patterns
- [[solid-and-grasp]] - closure-based immutable records
