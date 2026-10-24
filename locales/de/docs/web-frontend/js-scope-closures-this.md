---
title: "JavaScript Scope, Closures und this"
category: concepts
tags: [web-frontend, javascript, scope, closures, this]
level: 3
source_sha256: 89fd7a2f9120cec11ed4fa38dee8feb376cbe5ccdbcd6d2878b8dde7e1f43321
translation: machine
translated_at: '2026-10-24'
---
# JavaScript Scope, Closures und this {#javascript-scope-closures-and-this}

Der Scope bestimmt, wo Variablen sichtbar sind. Closures ermöglichen Datenkapselung und Zustandsverwaltung. Die Bindung von `this` hängt davon ab, wie eine Funktion aufgerufen wird.

## Scope-Typen {#scope-types}

**Global**: außerhalb jeder Funktion und jedes Blocks deklariert, überall zugänglich.
**Funktion**: innerhalb einer Funktion mit `var`, `let` oder `const` deklariert.
**Block**: innerhalb von `{}` mit `let` oder `const` deklariert. `var` ignoriert Block-Scopes!

```javascript
if (true) {
  let x = 10;    // Block-scoped
  var z = 30;    // Function-scoped (leaks out!)
}
console.log(z);   // 30
console.log(x);   // ReferenceError
```

### Scope-Kette {#scope-chain}
Variablensuche: aktueller Scope -> übergeordneter Scope -> Großelternscope -> global. Maßgeblich ist der Ort, an dem der Code GESCHRIEBEN wird (lexikalischer Scope), nicht der Ort des Aufrufs.

## Hoisting {#hoisting}

```javascript
greet();  // Works (function declarations fully hoisted)
function greet() { console.log("Hi"); }

console.log(x);  // undefined (var hoisted, not initialized)
var x = 5;

console.log(y);  // ReferenceError: TDZ
let y = 5;
```

## Strict Mode {#strict-mode}

```javascript
"use strict";  // Top of file or function
// Undeclared variables throw, duplicate params throw, this=undefined in standalone calls
```

ES-Module und Klassen laufen immer im Strict Mode.

## Closures {#closures}

Eine Funktion „merkt sich“ Variablen aus ihrem äußeren Scope, auch nachdem die äußere Funktion zurückgekehrt ist.

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

### Einsatzzwecke von Closures {#closure-uses}
1. **Datenkapselung**: Variablen sind von außen nicht zugänglich
2. **Zustandserhalt**: Zustand zwischen Aufrufen beibehalten
3. **Factory-Funktionen**: spezialisierte Funktionen erzeugen

```javascript
function createMultiplier(factor) {
  return (number) => number * factor;
}
const double = createMultiplier(2);
```

### Fallstrick bei Schleifenvariablen {#loop-variable-pitfall}
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

## Das Schlüsselwort `this` {#the-this-keyword}

### Bindungsregeln (Prioritätsreihenfolge) {#binding-rules-precedence-order}

**1. `new`**: `this` = neu erzeugtes Objekt
```javascript
function User(name) { this.name = name; }
const u = new User("Alice");  // this = new object
```

**2. Explizit**: `call`, `apply`, `bind`
```javascript
greet.call(user);              // this = user
greet.apply(user, [args]);     // this = user, args as array
const bound = greet.bind(user); // Returns function with fixed this
```

**3. Implizit**: Methodenaufruf
```javascript
user.greet();  // this = user
const fn = user.greet;
fn();          // this = undefined (method detached!)
```

**4. Default**: eigenständiger Aufruf
```javascript
function test() { console.log(this); }
test();  // window (non-strict) or undefined (strict)
```

### Arrow-Funktionen und this {#arrow-functions-and-this}
Arrow-Funktionen haben KEIN eigenes `this`. Sie übernehmen es aus dem umgebenden Scope.

```javascript
const user = {
  name: "Alice",
  greet: () => console.log(this.name),       // undefined! (inherits from module/global)
  delayedGreet() {
    setTimeout(() => console.log(this.name), 100);  // "Alice" (inherits from method)
  }
};
```

**Regel**: Verwende Arrow-Funktionen nicht als Objektmethoden. Innerhalb von Methoden eignen sie sich dagegen gut für Callbacks.

### call / apply / bind {#call-apply-bind}
```javascript
func.call(thisArg, arg1, arg2);           // Invoke with this + args
func.apply(thisArg, [arg1, arg2]);        // Same, args as array
const boundFn = func.bind(thisArg, arg1); // New function, fixed this
```

## Fallstricke {#gotchas}

- **Verlust der Methodenbindung**: `const fn = obj.method; fn()` verliert die `this`-Bindung
- **Arrow-Methoden**: `{ greet: () => this.name }` – `this` ist NICHT das Objekt
- **Closure-Schleifenfehler**: `var` in Schleifen teilt sich eine einzige Bindung; verwende `let`
- **`this` in verschachtelten Funktionen**: Eine reguläre verschachtelte Funktion hat ein eigenes `this` (meist `undefined`); verwende eine Arrow-Funktion oder `const self = this`
- **`bind` gibt eine neue Funktion zurück**: `element.removeEventListener("click", handler.bind(obj))` funktioniert nicht, da es sich um eine andere Funktionsreferenz handelt

## Siehe auch {#see-also}

- [[js-functions]] - Arrow vs. reguläre Funktionen, IIFE
- [[js-objects-and-data]] - Objektmethoden und `this`
- [[react-state-and-hooks]] - Hooks ersetzen das `this` von Klassenkomponenten
