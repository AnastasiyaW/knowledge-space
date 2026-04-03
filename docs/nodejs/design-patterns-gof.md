---
title: Design Patterns (GoF) in JavaScript
category: patterns
tags: [nodejs, gof, design-patterns, factory, strategy, observer, adapter, facade, proxy, decorator]
---

# Design Patterns (GoF) in JavaScript

The Gang of Four patterns apply differently in JavaScript than in class-based languages. First-class functions, closures, and dynamic typing simplify many patterns to plain functions or objects. In functional programming, all GoF patterns reduce to function composition: `G(f(x))`. ~20% of patterns cover ~80% of real-world use cases.

## Creational Patterns

### Factory Method

Replace direct `new` calls with method invocations for polymorphic instantiation:

```js
// JavaScript simplified - no abstract classes needed
const creators = {
  electronics: (data) => ({ type: 'electronics', ...data }),
  clothing: (data) => ({ type: 'clothing', ...data }),
};
const create = (type, data) => creators[type](data);

// Factorify - factory from class
const factorify = (Entity) => (...args) => new Entity(...args);
const createUser = factorify(User);
const user = createUser('John', 25); // no `new` needed
```

### Object Pool / AsyncPool

```js
class AsyncPool {
  constructor(factory, size) {
    this.instances = Array.from({ length: size }, () => factory());
    this.free = new Array(size).fill(true);
    this.queue = [];
  }

  async getInstance() {
    for (let i = 0; i < this.instances.length; i++) {
      if (this.free[i]) { this.free[i] = false; return this.instances[i]; }
    }
    return new Promise((resolve) => this.queue.push(resolve));
  }

  release(instance) {
    const i = this.instances.indexOf(instance);
    if (this.queue.length > 0) this.queue.shift()(instance);
    else this.free[i] = true;
  }
}
```

Design: factory passed to constructor (not pre-made instances) so pool can grow on demand.

### Flyweight (Timer Optimization)

Problem: 2 million `setInterval` calls is extremely expensive.

```js
class Interval {
  static cache = new Map();
  constructor(duration, callback) {
    const cached = Interval.cache.get(duration);
    if (cached) { cached.callbacks.push(callback); return Object.setPrototypeOf(this, cached); }
    this.callbacks = [callback];
    this.timer = setInterval(() => { for (const cb of this.callbacks) cb(); }, duration);
    Interval.cache.set(duration, this);
  }
}
```

Result: 2 million instances but only 2 real `setInterval` calls (one per unique duration). Trade-off: polymorphic V8 dispatch (2 extra CMP per `new`).

## Structural Patterns

### Adapter vs Facade vs Proxy

| Pattern | Wraps | Interface | Purpose |
|---------|-------|-----------|---------|
| **Adapter** | ONE abstraction | Changes interface | Convert contracts (promisify, callbackify) |
| **Facade** | Entire SUBSYSTEM | Simplifies interface | Hide complex internals |
| **Proxy** | ONE abstraction | Same interface | Add behavior (caching, logging, access) |

Adapter is extremely common - async contract conversion is everywhere in Node.js.

### Observer / Observable

```js
class Observable {
  #observers = [];
  subscribe(observer) { this.#observers.push(observer); }
  notify(data) { for (const o of this.#observers) o.update(data); }
  complete() { for (const o of this.#observers) o.complete?.(); }
}
```

JavaScript simplification: use plain callback functions instead of abstract Observer classes. **Signals** (modern frameworks) are also derived from Observable.

## Behavioral Patterns

### Strategy

```js
const renderers = {
  console: (data) => console.table(data),
  web: (data) => `<table>${data.map(r => `<tr><td>${r.name}</td></tr>`).join('')}</table>`,
  markdown: (data) => data.map(r => `| ${r.name} |`).join('\n'),
};
const createContext = (type) => ({ process: (data) => renderers[type](data) });
```

In JS, a strategy can be: a function, a class, an object, or a module.

### State

```js
const states = {
  idle: { process: () => { /* idle behavior */ }, next: 'processing' },
  processing: { process: () => { /* work */ }, next: 'complete' },
  complete: { process: () => { /* noop */ }, next: 'idle' },
};
```

### Chain of Responsibility

Middleware in Express/Fastify is a practical implementation. Each handler decides whether to process or pass to `next()`.

### Command (with Actor Model)

In the Actor model, messages are commands; the actor's message queue is a command queue. Combined with undo capability, enables transaction-like behavior.

## FP Equivalents

| GoF Pattern | FP Equivalent |
|-------------|--------------|
| Strategy | Passing a function as argument |
| Observer | Callback composition |
| Decorator | Function wrapping |
| Chain of Responsibility | Function pipeline |

## Gotchas

- Facades tend to grow into God Objects over time - discipline needed to keep the interface minimal
- Adapter can have multiple inputs/outputs (USB-C to USB-A + Lightning is still an adapter)
- Pareto Principle: ~20% of patterns cover ~80% of use cases - focus on patterns you'll actually use
- All paradigms are highly variable internally - there's no single "OOP way" or "FP way"

## See Also

- [[solid-and-grasp]] - principles behind pattern selection
- [[async-patterns]] - promisify/callbackify as Adapter pattern
- [[dependency-injection]] - DI vs module system patterns
- [[closures-and-scope]] - closures as the foundation for many patterns
