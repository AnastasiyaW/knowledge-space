---
title: "JavaScript-Funktionen"
category: concepts
tags: [web-frontend, javascript, functions, arrow-functions, callbacks]
level: 3
source_sha256: 8d8784ff92ac0f7a810a6263a2d68bffa9b039376a29f2dcce767446092561ff
translation: machine
translated_at: '2026-10-24'
---
# JavaScript-Funktionen {#javascript-functions}

Funktionen sind in JavaScript First-Class-Citizens: Sie können in Variablen gespeichert, als Argumente übergeben und aus anderen Funktionen zurückgegeben werden.

## Deklarationsarten {#declaration-types}

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

### Arrow vs. Regular {#arrow-vs-regular}

| Merkmal | Regular | Arrow |
|---------|---------|-------|
| `this` | Eigenes (dynamisch) | Geerbt (lexikalisch) |
| `arguments` | Ja | Nein (stattdessen `...args` verwenden) |
| `new` | Konstruktor | Nicht möglich |
| Hoisting | Deklarationen ja | Nein |
| Geeignet für | Methoden, Konstruktoren | Callbacks, funktional |

## Parameter {#parameters}

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

## Rückgabewerte {#return-values}

```javascript
function divide(a, b) {
  if (b === 0) return null;   // Early return
  return a / b;
}
// No explicit return = undefined
```

## Higher-Order Functions {#higher-order-functions}

Funktionen, die Funktionen als Argument entgegennehmen oder zurückgeben:

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

## Callbacks {#callbacks}

```javascript
function fetchData(callback) {
  setTimeout(() => {
    callback({ name: "Alice" });
  }, 1000);
}
fetchData((data) => console.log(data.name));
```

Verschachtelte Callbacks werden schnell unlesbar („Callback-Hölle“). Abhilfe schaffen [[js-async-and-fetch|Promises und async/await]].

## IIFE (Immediately Invoked) {#iife-immediately-invoked}

```javascript
(function() {
  const secret = "hidden";
  console.log("Runs immediately");
})();

(() => { console.log("Arrow IIFE"); })();
```

Sie erzeugt eine Scope-Isolation. Mit `let`/`const` und Modulen wird sie seltener benötigt, für einmalige Initialisierungen wird sie aber weiterhin verwendet.

## Pure Functions {#pure-functions}

```javascript
// Pure: same input = same output, no side effects
function add(a, b) { return a + b; }

// Impure: modifies external state
let total = 0;
function addToTotal(n) { total += n; return total; }
```

Pure Functions sind vorhersagbar, testbar und cachebar. Wo möglich, sollten sie bevorzugt werden.

## Gotchas {#gotchas}

- **Arrow-`this`**: Arrow-Funktionen übernehmen `this` aus dem umgebenden Scope – nicht als Objektmethoden verwenden
- **Aufrufen vs. Übergeben**: `onClick={handleClick}` (Referenz übergeben) vs. `onClick={handleClick()}` (sofort aufrufen)
- **Objektliteral als Rückgabe**: Der Arrow-Body muss in Klammern stehen: `() => ({ key: value })`
- **`arguments` in Arrows**: Existiert nicht; stattdessen Rest-Parameter `...args` verwenden
- **Default-Parameter werden zur Aufrufzeit ausgewertet**: `function f(arr = [])` erzeugt bei jedem Aufruf ein neues Array

## Siehe auch {#see-also}

- [[js-scope-closures-this]] - Scope-Kette, Closures, `this`-Bindung
- [[js-arrays]] - Array-Methoden als Higher-Order Functions
- [[js-async-and-fetch]] - Async-Muster als Ersatz für Callbacks
- [[react-state-and-hooks]] - React-Hooks als Funktionsmuster
