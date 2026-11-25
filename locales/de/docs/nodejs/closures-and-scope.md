---
title: "Closures und Scope"
category: concepts
tags: [nodejs, javascript, closures, scope, lexical-environment, block-scope, module-scope]
level: 3
source_sha256: 330da0f5fd5c43ceb75c676b8c5ed07375ed1d8fd2bc1d9d7229e4e72f0a7a33
translation: machine
translated_at: '2026-10-24'
---
# Closures und Scope {#closures-and-scope}

Eine Closure ist eine Funktion, die auch dann noch einen Verweis auf Variablen aus dem Scope ihrer äußeren Funktion behält, wenn die äußere Funktion bereits ausgeführt wurde. Die Closure ist eine Datenstruktur, die im Heap innerhalb der JS-Laufzeitumgebung gespeichert wird – nur die innere Funktion kann auf sie lesend und schreibend zugreifen. Das Verständnis von Scope und Closures ist essenziell für Kapselung, Factory-Funktionen und Modulentwurf in Node.js.

## Key Facts {#key-facts}

- **Scope (Sichtbarkeitsbereich)**: aus der Perspektive eines Bezeichners betrachtet – wo er sichtbar ist (Funktions-, Block-, Modul- oder globaler Scope)
- **Lexikalischer Kontext/Environment**: aus der Perspektive einer Position im Programm betrachtet – welche Bezeichner an dieser Stelle zugänglich sind
- Eine Closure ist eine Heap-Datenstruktur; es gibt keine externe Referenz – nur die innere Funktion kann darauf zugreifen
- Ähnlich wie `this` in Objekten, aber anders als bei `this` lassen sich von außen keine Felder zu einer Closure hinzufügen

### Drei Bedingungen für eine Closure {#three-conditions-for-a-closure}

Alle drei müssen gleichzeitig erfüllt sein:
1. Eine äußere Funktion definiert Variablen
2. Eine innere Funktion referenziert diese Variablen
3. Die innere Funktion wird zurückgegeben oder nach außen übergeben

Fehlt ein Teil, liegt keine vollständige Closure vor. Der Zugriff auf eine globale Variable aus einer Funktion heraus ist KEINE Closure.

### Modul-Scope in Node.js {#nodejs-module-scope}

- Jedes Modul wird in eine Funktion eingebettet, wodurch ein modulweiter Scope entsteht – für Benutzercode gibt es keinen echten globalen Scope
- In browserbasiertem JS teilen sich alle Dateien einen Scope, sofern sie nicht in IIFEs eingeschlossen sind oder Module-Bundler verwendet werden

## Patterns {#patterns}

### Closure-basierte Kapselung {#closure-based-encapsulation}

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

### Block-Scope als Vererbung {#block-scope-as-inheritance}

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

### Modul-Wrapping (wie Node.js Scope erzeugt) {#module-wrapping-how-nodejs-creates-scope}

```js
// Node.js wraps each module:
// (function(exports, require, module, __filename, __dirname) {
//   ... your module code ...
// });
// This is why top-level variables are module-scoped, not global
```

## Gotchas {#gotchas}

- Closures behalten Referenzen auf das gesamte lexikalische Environment, nicht nur auf die tatsächlich verwendeten Variablen – das kann zu Speicherretention führen
- In Schleifen mit `var` teilen sich alle Closures dieselbe Variable; `let` (blockbezogen) verwenden, um pro Iteration einen eigenen Scope zu erhalten
- Der Zugriff auf eine globale Variable aus einer Funktion heraus ist KEINE Closure – wer beides verwechselt, entwickelt falsche Vorstellungen über die Architektur

## See Also {#see-also}

- [[v8-optimization]] – wie V8 Closure-Datenstrukturen auf dem Heap speichert
- [[modules-and-packages]] – Modul-Wrapping erzeugt den umschließenden Scope
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) – Closures als Grundlage vieler Patterns
- [[solid-and-grasp]] – Closure-basierte unveränderliche Records
