---
title: Design Patterns (GoF)
category: patterns
tags: [design-patterns, gof, singleton, factory, observer, strategy, decorator, chain-of-responsibility, adapter]
---
# Design Patterns (GoF)

The Gang of Four patterns adapted for JavaScript and Node.js. JS's dynamic nature, first-class functions, and closures simplify many patterns compared to classical OOP languages.

## Key Facts

- **Singleton**: module caching in Node.js makes every `require()`'d module a natural singleton
- **Factory**: functions returning objects; in JS, factory functions often replace class hierarchies
- **Observer**: built into Node.js via `EventEmitter`; also: DOM events, RxJS, pub/sub
- **Strategy**: pass functions as arguments; JS first-class functions make this trivial
- **Decorator**: wrap an object/function to add behavior; middleware chains are decorators
- **Chain of Responsibility**: Express/Koa middleware pipeline is this pattern
- **Adapter**: wrapping one interface to match another; common when integrating third-party APIs
- **Proxy**: `new Proxy(target, handler)` is a native JS language feature for meta-programming
- In JS, many GoF patterns collapse to passing functions or using closures
- Anti-pattern: over-engineering with patterns that add ceremony without benefit (YAGNI)
- Patterns should emerge from need, not be applied preemptively

## Patterns

```javascript
// Singleton via module cache (Node.js natural pattern)
// db.js
class Database {
  constructor() {
    if (Database.instance) return Database.instance;
    this.pool = createPool({ /* config */ });
    Database.instance = this;
  }
}
module.exports = new Database();
// Every require('./db') returns the same instance

// Factory
function createTransport(type, config) {
  switch (type) {
    case 'http': return new HttpTransport(config);
    case 'ws':   return new WebSocketTransport(config);
    case 'tcp':  return new TcpTransport(config);
    default: throw new Error(`Unknown transport: ${type}`);
  }
}

// Abstract Factory with registry
class TransportRegistry {
  #factories = new Map();
  register(type, factory) { this.#factories.set(type, factory); }
  create(type, config) {
    const factory = this.#factories.get(type);
    if (!factory) throw new Error(`Unknown transport: ${type}`);
    return factory(config);
  }
}

// Strategy pattern (JS: just pass a function)
function processData(data, strategy) {
  return strategy(data);
}
const compress = (data) => zlib.gzipSync(data);
const encrypt = (data) => crypto.createCipheriv(/*...*/).update(data);
processData(buffer, compress);
processData(buffer, encrypt);

// Observer (EventEmitter)
const { EventEmitter } = require('events');
class OrderService extends EventEmitter {
  async createOrder(data) {
    const order = await db.insert(data);
    this.emit('order:created', order);
    return order;
  }
}
const orders = new OrderService();
orders.on('order:created', (order) => sendEmail(order));
orders.on('order:created', (order) => updateInventory(order));

// Decorator pattern
function withRetry(fn, retries = 3) {
  return async function (...args) {
    for (let i = 0; i <= retries; i++) {
      try {
        return await fn.apply(this, args);
      } catch (err) {
        if (i === retries) throw err;
        await new Promise(r => setTimeout(r, 2 ** i * 100));
      }
    }
  };
}
const resilientFetch = withRetry(fetch, 3);

// Chain of Responsibility (middleware)
function compose(middlewares) {
  return function (ctx) {
    let index = -1;
    function dispatch(i) {
      if (i <= index) throw new Error('next() called multiple times');
      index = i;
      const fn = middlewares[i];
      if (!fn) return;
      return fn(ctx, () => dispatch(i + 1));
    }
    return dispatch(0);
  };
}

// Proxy pattern (native JS)
function createTrackedObject(target) {
  return new Proxy(target, {
    get(obj, prop) {
      console.log(`GET ${String(prop)}`);
      return Reflect.get(obj, prop);
    },
    set(obj, prop, value) {
      console.log(`SET ${String(prop)} = ${value}`);
      return Reflect.set(obj, prop, value);
    },
  });
}
```

## Gotchas

- **Symptom**: Singleton state leaks between tests - **Cause**: module cache persists across test files - **Fix**: provide `.reset()` method; or use factory + DI instead of module-level singleton
- **Symptom**: observer memory leak - **Cause**: listeners not removed; too many listeners added per request - **Fix**: remove listeners (`off`/`removeListener`); check `maxListeners` warning
- **Symptom**: decorator breaks `this` context - **Cause**: using arrow function in decorator loses original `this` - **Fix**: use `fn.apply(this, args)` or `fn.call(this, ...args)` to preserve context
- **Symptom**: excessive abstraction, hard to debug - **Cause**: applying patterns preemptively without concrete need - **Fix**: start simple, refactor to patterns when duplication or complexity demands it

## See Also

- [[solid-and-grasp]] - principles that guide pattern selection
- [[closures-and-scope]] - closures replace many OOP patterns in JS
- [[dependency-injection]] - IoC container as a pattern orchestrator
- [[middleware-and-http]] - Chain of Responsibility in practice
