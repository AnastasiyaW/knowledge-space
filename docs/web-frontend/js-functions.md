---
title: JavaScript Functions
category: concepts
tags: [web-frontend, javascript, functions, arrow-functions, callbacks]
---

# JavaScript Functions

Functions are first-class citizens in JavaScript - they can be stored in variables, passed as arguments, and returned from other functions.

## Declaration Types

```javascript
// Function declaration (hoisted)
function add(a, b) { return a + b; }

// Function expression (NOT hoisted)
const add = function(a, b) { return a + b; };

// Arrow function
const add = (a, b) => a + b;              // Implicit return
const add = (a, b) => { return a + b; };  // Explicit (block body)
const square = x => x * x;                // Single param: no parens
const greet = () => "Hello!";             // No params
const getUser = () => ({ name: "Alice" }); // Return object: wrap in ()
```

### Arrow vs Regular

| Feature | Regular | Arrow |
|---------|---------|-------|
| `this` | Own (dynamic) | Inherited (lexical) |
| `arguments` | Yes | No (use `...args`) |
| `new` | Constructor | Cannot |
| Hoisting | Declarations yes | No |
| Best for | Methods, constructors | Callbacks, functional |

## Parameters

```javascript
// Default
function greet(name = "World") { return `Hello, ${name}!`; }

// Rest (must be last)
function sum(...numbers) { return numbers.reduce((a, b) => a + b, 0); }

// Destructuring
function createUser({ name, age, role = "user" }) {
  return { name, age, role };
}
```

## Return Values

```javascript
function divide(a, b) {
  if (b === 0) return null;   // Early return
  return a / b;
}
// No explicit return = undefined
```

## Higher-Order Functions

Functions that take or return functions:

```javascript
// Takes function as argument
function repeat(n, action) {
  for (let i = 0; i < n; i++) action(i);
}

// Returns function (factory)
function multiplier(factor) {
  return (number) => number * factor;
}
const double = multiplier(2);
double(5);   // 10
```

## Callbacks

```javascript
function fetchData(callback) {
  setTimeout(() => {
    callback({ name: "Alice" });
  }, 1000);
}
fetchData((data) => console.log(data.name));
```

Nested callbacks become unreadable ("callback hell"). Solved by [[js-async-and-fetch|Promises and async/await]].

## IIFE (Immediately Invoked)

```javascript
(function() {
  const secret = "hidden";
  console.log("Runs immediately");
})();

(() => { console.log("Arrow IIFE"); })();
```

Creates scope isolation. Less needed with `let`/`const` and modules, still used for one-time setup.

## Pure Functions

```javascript
// Pure: same input = same output, no side effects
function add(a, b) { return a + b; }

// Impure: modifies external state
let total = 0;
function addToTotal(n) { total += n; return total; }
```

Pure functions are predictable, testable, cacheable. Prefer when possible.

## Gotchas

- **Arrow `this`**: arrow functions inherit `this` from enclosing scope - don't use as object methods
- **Calling vs passing**: `onClick={handleClick}` (pass reference) vs `onClick={handleClick()}` (call immediately)
- **Object literal return**: arrow must wrap in parens: `() => ({ key: value })`
- **`arguments` in arrows**: doesn't exist; use rest params `...args`
- **Default params evaluated at call time**: `function f(arr = [])` creates new array each call

## See Also

- [[js-scope-closures-this]] - Scope chain, closures, `this` binding
- [[js-arrays]] - Array methods as higher-order functions
- [[js-async-and-fetch]] - Async patterns replacing callbacks
- [[react-state-and-hooks]] - React hooks as function patterns
