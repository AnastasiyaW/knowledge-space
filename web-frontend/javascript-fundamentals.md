---
title: JavaScript Fundamentals
category: javascript
tags: [javascript, variables, types, scope, hoisting, closures, es6]
---

# JavaScript Fundamentals

## Key Facts

- **Primitive types**: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`
- **Reference types**: `object`, `array`, `function`, `Map`, `Set`, `Date`, `RegExp`
- `let` = block-scoped, reassignable; `const` = block-scoped, not reassignable (object contents mutable); `var` = function-scoped, hoisted
- **Hoisting**: `var` declarations hoisted (value = `undefined`); `let`/`const` hoisted but in "temporal dead zone" until declaration
- **Closures**: inner function retains access to outer function's variables even after outer returns
- `===` strict equality (type + value); `==` loose equality (type coercion) - always use `===`
- **Template literals**: `` `Hello ${name}` `` with backticks for interpolation and multiline strings
- **Destructuring**: `const { a, b } = obj;` / `const [x, y] = arr;`
- **Spread/rest**: `...arr` spreads elements; `...rest` collects remaining into array
- **Nullish coalescing**: `a ?? b` returns `b` only if `a` is `null`/`undefined` (not `0` or `""`)
- Related: [[javascript-async-and-promises]], [[javascript-dom-and-events]], [[javascript-array-methods]]

## Patterns

### Variable Declarations

```javascript
const PI = 3.14;        // cannot reassign
let count = 0;          // block-scoped, reassignable
count++;

const user = { name: "Ana" };
user.name = "Anastasia"; // OK - mutating object, not reassigning
// user = {};            // Error - cannot reassign const
```

### Destructuring and Spread

```javascript
// Object destructuring with rename and default
const { name: userName, age = 25 } = user;

// Array destructuring
const [first, , third] = [1, 2, 3]; // skip second

// Spread - shallow copy
const copy = { ...original, updated: true };
const merged = [...arr1, ...arr2];

// Rest parameters
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### Arrow Functions

```javascript
// Concise body (implicit return)
const double = (x) => x * 2;

// Block body (explicit return needed)
const process = (data) => {
  const result = transform(data);
  return result;
};

// Arrow functions do NOT have their own `this`
const timer = {
  seconds: 0,
  start() {
    setInterval(() => {
      this.seconds++; // `this` = timer object (inherited from start)
    }, 1000);
  }
};
```

### Optional Chaining and Nullish Coalescing

```javascript
const city = user?.address?.city;       // undefined if any part is null/undefined
const first = arr?.[0];                 // safe array access
const result = obj?.method?.();         // safe method call

const port = config.port ?? 3000;       // 3000 only if port is null/undefined
// vs config.port || 3000 which also replaces 0
```

### Closures

```javascript
function createCounter(initial = 0) {
  let count = initial;
  return {
    increment: () => ++count,
    decrement: () => --count,
    value: () => count,
  };
}
const counter = createCounter(10);
counter.increment(); // 11
counter.value();     // 11
```

## Gotchas

- `typeof null === "object"` is a historical bug; check `value === null` explicitly
- `NaN !== NaN`; use `Number.isNaN(x)` to check (not global `isNaN()` which coerces)
- `0.1 + 0.2 !== 0.3` (floating point); compare with `Math.abs(a - b) < Number.EPSILON`
- `const` prevents reassignment, not mutation; `const arr = []; arr.push(1)` works
- Arrow functions cannot be used as constructors (no `new`), have no `arguments` object, and cannot be generators

## See Also

- [MDN: JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
