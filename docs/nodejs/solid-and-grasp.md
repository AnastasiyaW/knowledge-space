---
title: SOLID and GRASP Principles
category: concepts
tags: [nodejs, solid, grasp, lsp, srp, dip, composition, inheritance]
---

# SOLID and GRASP Principles

SOLID and GRASP principles guide code organization in JavaScript, but their application differs from class-based languages. Closures, first-class functions, and the module system provide alternative mechanisms for achieving the same goals. Most experienced developers develop these intuitions through practice without knowing the formal names.

## Key Facts

- The `extends` keyword is misleading: in type theory, subclasses should *narrow* the parent type, but `extends` implies *widening*
- **LSP**: A reference to a subclass must be substitutable wherever the parent class is expected
- **Composition vs Inheritance**: the same functionality can be written in 32+ different paradigms (pure functions, classes, prototypes, closures, actors, monads, mixins, etc.)
- In FP, all GoF patterns reduce to function composition `G(f(x))`
- Angular aligns better with GoF/GRASP/SOLID (class-based); React leans functional
- There's no comprehensive "GoF for FP in JavaScript" resource
- The choice between paradigms is pragmatic, not religious

## Algebraic Data Types (ADT) in JavaScript

ADT = types created via algebraic operations (sum, product) on other types. Not to be confused with "Abstract Data Types."

### Immutable Records

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

- `Object.create(null)` for clean prototype chain
- Updates have priority over instance values
- TypeScript union types disappear at compile time - runtime ADT implementations persist

## Patterns

### Composition vs Inheritance - Multiple Paradigms

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

All paradigms have dozens of sub-approaches. Learning patterns teaches trade-off evaluation, not template application.

### Protocols as Interfaces (Contract Programming)

```js
// Built-in JavaScript protocols act as abstract interfaces:
// Iterable: Symbol.iterator → { next() → { value, done } }
// Thenable: .then() method → Promise compatibility
// Async Iterable: Symbol.asyncIterator → async iterator

// Conformance verified by tests, not type system
// All Promises are thenables, not all thenables are Promises
```

Objects sharing the same contract (same fields, types, order) get identical V8 hidden classes, enabling monomorphic optimization. Contract programming matters for performance in JS.

## Two Architecture Extremes

1. **Overengineered**: strict SOLID/GRASP/DDD - many classes, layers, separation - complex and verbose
2. **Minimal**: single class handles everything, violates SRP - but more features in less code
3. **Sweet spot**: declarative schema + universal repository pattern

## Gotchas

- Breaking LSP (adding incompatible methods to subclasses) loses the flexibility that inheritance was supposed to provide
- Package-lock.json MUST be committed - even patch versions can break transitive dependencies
- LLMs cannot do application structure/architecture - the developer must be MORE skilled than the LLM, acting as senior architect

## See Also

- [[design-patterns-gof]] - concrete pattern implementations in JavaScript
- [[dependency-injection]] - Dependency Inversion Principle in practice
- [[closures-and-scope]] - closures as alternative to class-based encapsulation
- [[application-architecture]] - layered architecture as SOLID application
