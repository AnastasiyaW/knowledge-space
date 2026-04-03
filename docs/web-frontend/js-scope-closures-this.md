---
title: JavaScript Scope, Closures, and this
category: concepts
tags: [web-frontend, javascript, scope, closures, this]
---

# JavaScript Scope, Closures, and this

Scope determines variable accessibility. Closures enable data privacy and state. `this` binding depends on how a function is called.

## Scope Types

**Global**: declared outside any function/block, accessible everywhere.
**Function**: declared inside function with `var`, `let`, or `const`.
**Block**: declared inside `{}` with `let`/`const`. `var` ignores block scope!

```javascript
if (true) {
  let x = 10;    // Block-scoped
  var z = 30;    // Function-scoped (leaks out!)
}
console.log(z);   // 30
console.log(x);   // ReferenceError
```

### Scope Chain
Variable lookup: current scope -> parent -> grandparent -> global. Determined by where code is WRITTEN (lexical scope), not where called.

## Hoisting

```javascript
greet();  // Works (function declarations fully hoisted)
function greet() { console.log("Hi"); }

console.log(x);  // undefined (var hoisted, not initialized)
var x = 5;

console.log(y);  // ReferenceError: TDZ
let y = 5;
```

## Strict Mode

```javascript
"use strict";  // Top of file or function
// Undeclared variables throw, duplicate params throw, this=undefined in standalone calls
```

ES modules and classes are always in strict mode.

## Closures

A function "remembers" variables from its outer scope even after the outer function returns.

```javascript
function createCounter() {
  let count = 0;
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; }
  };
}
const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
// count is inaccessible directly - data privacy
```

### Closure Uses
1. **Data privacy**: variables inaccessible from outside
2. **State preservation**: maintain state between calls
3. **Factory functions**: create specialized functions

```javascript
function createMultiplier(factor) {
  return (number) => number * factor;
}
const double = createMultiplier(2);
```

### Loop Variable Pitfall
```javascript
// Bug: all callbacks share same 'i'
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Prints: 3, 3, 3

// Fix: use let (new binding per iteration)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Prints: 0, 1, 2
```

## The `this` Keyword

### Binding Rules (precedence order)

**1. `new`**: `this` = newly created object
```javascript
function User(name) { this.name = name; }
const u = new User("Alice");  // this = new object
```

**2. Explicit**: `call`, `apply`, `bind`
```javascript
greet.call(user);              // this = user
greet.apply(user, [args]);     // this = user, args as array
const bound = greet.bind(user); // Returns function with fixed this
```

**3. Implicit**: method call
```javascript
user.greet();  // this = user
const fn = user.greet;
fn();          // this = undefined (method detached!)
```

**4. Default**: standalone call
```javascript
function test() { console.log(this); }
test();  // window (non-strict) or undefined (strict)
```

### Arrow Functions and this
Arrows DON'T have their own `this` - they inherit from enclosing scope.

```javascript
const user = {
  name: "Alice",
  greet: () => console.log(this.name),       // undefined! (inherits from module/global)
  delayedGreet() {
    setTimeout(() => console.log(this.name), 100);  // "Alice" (inherits from method)
  }
};
```

**Rule**: Don't use arrows as object methods. DO use inside methods for callbacks.

### call / apply / bind
```javascript
func.call(thisArg, arg1, arg2);           // Invoke with this + args
func.apply(thisArg, [arg1, arg2]);        // Same, args as array
const boundFn = func.bind(thisArg, arg1); // New function, fixed this
```

## Gotchas

- **Method detachment**: `const fn = obj.method; fn()` loses `this` binding
- **Arrow methods**: `{ greet: () => this.name }` - `this` is NOT the object
- **Closure loop bug**: `var` in loops shares single binding; use `let`
- **`this` in nested functions**: regular nested function has its own `this` (usually undefined); use arrow or `const self = this`
- **`bind` returns new function**: `element.removeEventListener("click", handler.bind(obj))` won't work - different function reference

## See Also

- [[js-functions]] - Arrow vs regular, IIFE
- [[js-objects-and-data]] - Object methods and `this`
- [[react-state-and-hooks]] - Hooks replace class component `this`
