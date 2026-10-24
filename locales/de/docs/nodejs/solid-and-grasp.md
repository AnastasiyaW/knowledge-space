---
title: "SOLID- und GRASP-Prinzipien"
category: concepts
tags: [nodejs, solid, grasp, lsp, srp, dip, composition, inheritance]
level: 3
source_sha256: d37c2ac94503201a8d5c0b8b2097edddb7da79a7d4e3cfb56fafefc9d24a7e2d
translation: machine
translated_at: '2026-10-24'
---
# SOLID- und GRASP-Prinzipien {#solid-and-grasp-principles}

SOLID- und GRASP-Prinzipien leiten die Code-Organisation in JavaScript an, doch ihre Anwendung unterscheidet sich von klassenbasierten Sprachen. Closures, First-Class-Funktionen und das Modulsystem bieten alternative Mechanismen, um dieselben Ziele zu erreichen. Die meisten erfahrenen Entwickler entwickeln diese Intuitionen durch Praxis, ohne die formalen Namen zu kennen.

## Kernfakten {#key-facts}

- Das Schlüsselwort `extends` ist irreführend: In der Typentheorie sollten Subklassen den Elterntyp *einschränken* (narrow), `extends` impliziert jedoch *Erweiterung* (widening)
- **LSP**: Eine Referenz auf eine Subklasse muss überall dort ersetzbar sein, wo die Elternklasse erwartet wird
- **Komposition vs. Vererbung**: Dieselbe Funktionalität lässt sich in über 32 verschiedenen Paradigmen umsetzen (reine Funktionen, Klassen, Prototypen, Closures, Actors, Monaden, Mixins usw.)
- In FP lassen sich alle GoF-Muster auf Funktionskomposition `G(f(x))` zurückführen
- Angular orientiert sich stärker an GoF/GRASP/SOLID (klassenbasiert); React neigt zum Funktionalen
- Es gibt keine umfassende Ressource „GoF für FP in JavaScript"
- Die Wahl des Paradigmas ist pragmatisch, nicht dogmatisch

## Algebraische Datentypen (ADT) in JavaScript {#algebraic-data-types-adt-in-javascript}

ADT = Typen, die durch algebraische Operationen (Summe, Produkt) auf anderen Typen entstehen. Nicht zu verwechseln mit „Abstract Data Types".

### Unveränderliche Records {#immutable-records}

```js
const record = (schema) => {
  const obj = Object.create(null);
  for (const [key, defaultVal] of Object.entries(schema)) {
    obj[key] = defaultVal;
  }
  return Object.freeze(obj);
};

// Fork: create a modified copy
const fork = (instance, updates) => {
  const copy = Object.create(null);
  for (const key of Object.keys(instance)) {
    copy[key] = Reflect.has(updates, key) ? updates[key] : instance[key];
  }
  if (Object.isFrozen(instance)) Object.freeze(copy);
  return copy;
};
```

- `Object.create(null)` für eine saubere Prototypenkette
- Aktualisierungen haben Vorrang vor Instanzwerten
- TypeScript-Union-Typen verschwinden zur Kompilierzeit – Laufzeitimplementierungen von ADTs bleiben bestehen

## Muster {#patterns}

### Komposition vs. Vererbung – Mehrere Paradigmen {#composition-vs-inheritance-multiple-paradigms}

```js
// 1. Pure functions with composition
const move = (point, dx, dy) => ({ x: point.x + dx, y: point.y + dy });

// 2. Class-based
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  move(dx, dy) { return new Point(this.x + dx, this.y + dy); }
}

// 3. Closure-based (values hidden in closures)
const createPoint = (x, y) => ({
  move: (dx, dy) => createPoint(x + dx, y + dy),
  toString: () => `(${x}, ${y})`,
});

// 4. Actor model
class PointActor extends Actor {
  #x; #y;
  async handle({ type, dx, dy }) {
    if (type === 'move') { this.#x += dx; this.#y += dy; }
  }
}
```

Alle Paradigmen haben Dutzende Unteransätze. Muster zu lernen vermittelt die Abwägung von Kompromissen, nicht die Anwendung von Vorlagen.

### Protokolle als Schnittstellen (Contract Programming) {#protocols-as-interfaces-contract-programming}

```js
// Built-in JavaScript protocols act as abstract interfaces:
// Iterable: Symbol.iterator → { next() → { value, done } }
// Thenable: .then() method → Promise compatibility
// Async Iterable: Symbol.asyncIterator → async iterator

// Conformance verified by tests, not type system
// All Promises are thenables, not all thenables are Promises
```

Objekte, die denselben Vertrag teilen (gleiche Felder, Typen, Reihenfolge), erhalten identische V8-Hidden-Classes, was monomorphe Optimierung ermöglicht. Contract Programming ist in JS für die Performance relevant.

## Zwei Architektur-Extreme {#two-architecture-extremes}

1. **Überentwickelt**: strikte SOLID/GRASP/DDD – viele Klassen, Schichten, Trennungen – komplex und ausufernd
2. **Minimal**: eine einzige Klasse übernimmt alles und verletzt SRP – dafür mehr Funktionalität in weniger Code
3. **Optimaler Mittelweg**: deklaratives Schema + universelles Repository-Muster

## Stolperfallen {#gotchas}

- Verletzung von LSP (Hinzufügen inkompatibler Methoden in Subklassen) verliert die Flexibilität, die Vererbung eigentlich bieten sollte
- Package-lock.json MUSS committet werden – selbst Patch-Versionen können transitive Abhängigkeiten brechen
- LLMs können Anwendungsstruktur/Architektur nicht übernehmen – der Entwickler muss KOMPETENTER sein als das LLM und als Senior-Architekt agieren

## Siehe auch {#see-also}

- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) – konkrete Mustersimplementierungen in JavaScript
- [[dependency-injection]] – Dependency Inversion Principle in der Praxis
- [[closures-and-scope]] – Closures als Alternative zur klassenbasierten Kapselung
- [[application-architecture]] – Schichtenarchitektur als SOLID-Anwendung
