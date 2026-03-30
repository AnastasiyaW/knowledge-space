---
title: Prototypes and Classes
category: language
tags: [prototype, class, inheritance, constructor, new, extends, mixin, composition]
---
# Prototypes and Classes

JavaScript uses prototypal inheritance: objects delegate property lookups to their prototype chain. ES6 `class` syntax is syntactic sugar over this mechanism. Understanding the prototype chain is essential for debugging, extending built-ins, and designing APIs.

## Key Facts

- Every object has an internal `[[design-patterns-creational]]` slot (accessed via `Object.getPrototypeOf()` or `__proto__`)
- Property lookup walks the prototype chain: own properties -> prototype -> prototype's prototype -> ... -> `null`
- `class` keyword creates a constructor function + prototype object; it is NOT a different paradigm
- `new` operator: creates empty object, sets its `[[design-patterns-creational]]` to Constructor.prototype, calls constructor with `this` bound to new object, returns object (unless constructor returns an object)
- `extends` sets up two prototype links: subclass.prototype -> superclass.prototype AND subclass -> superclass (for static methods)
- `super()` must be called before `this` in derived constructor
- Private fields: `#field` is truly private (not on prototype, not accessible via reflection)
- `static` methods belong to the constructor function, not instances
- `instanceof` checks the prototype chain: `obj instanceof Cls` is true if `Cls.prototype` is in obj's chain
- **Prefer composition over inheritance**: mixins, delegation, and factory functions scale better
- `Object.create(proto)` creates an object with specified prototype (no constructor call)

## Patterns

```javascript
// ES6 class with private fields
class EventEmitter {
  #listeners = new Map();

  on(event, fn) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, []);
    }
    this.#listeners.get(event).push(fn);
    return this;
  }

  emit(event, ...args) {
    const handlers = this.#listeners.get(event) || [];
    for (const fn of handlers) fn(...args);
    return handlers.length > 0;
  }

  off(event, fn) {
    const handlers = this.#listeners.get(event);
    if (handlers) {
      const idx = handlers.indexOf(fn);
      if (idx !== -1) handlers.splice(idx, 1);
    }
    return this;
  }
}

// Inheritance
class TypedEmitter extends EventEmitter {
  #schema;
  constructor(schema) {
    super();
    this.#schema = schema;
  }
  emit(event, ...args) {
    if (!this.#schema[event]) {
      throw new Error(`Unknown event: ${event}`);
    }
    return super.emit(event, ...args);
  }
}

// Mixin pattern (composition > inheritance)
const Serializable = (Base) => class extends Base {
  toJSON() {
    const result = {};
    for (const [key, value] of Object.entries(this)) {
      result[key] = value;
    }
    return result;
  }
  static fromJSON(data) {
    return Object.assign(new this(), data);
  }
};

const Timestamped = (Base) => class extends Base {
  constructor(...args) {
    super(...args);
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }
  touch() { this.updatedAt = new Date(); }
};

class User extends Timestamped(Serializable(EventEmitter)) {
  constructor(name) {
    super();
    this.name = name;
  }
}

// Factory function (no class, no prototype chain)
function createUser(name, role) {
  const state = { name, role, active: true };
  return Object.freeze({
    getName: () => state.name,
    getRole: () => state.role,
    deactivate: () => { state.active = false; },
    isActive: () => state.active,
  });
}

// Prototype-based delegation
const animal = {
  speak() { return `${this.name} makes a sound`; }
};
const dog = Object.create(animal);
dog.bark = function () { return `${this.name} barks`; };
dog.name = 'Rex';
dog.speak(); // Rex makes a sound
dog.bark();  // Rex barks
```

## Gotchas

- **Symptom**: `this` is undefined in a method callback - **Cause**: method was detached from its object; `this` is dynamic - **Fix**: use arrow function in class field, or `.bind(this)` in constructor
- **Symptom**: `super()` not called error - **Cause**: derived class constructor must call `super()` before using `this` - **Fix**: call `super()` as the first statement
- **Symptom**: `instanceof` returns false for objects from different realms (iframes, vm contexts) - **Cause**: different prototype objects per realm - **Fix**: use `Symbol.hasInstance` or duck-typing checks
- **Symptom**: modifying `Array.prototype` or `Object.prototype` causes iteration bugs - **Cause**: added properties show up in `for...in` loops - **Fix**: never modify built-in prototypes; use `Object.defineProperty` with `enumerable: false` if absolutely necessary

## See Also

- [[closures-and-scope]] - factory functions use closures for privacy
- [[design-patterns-gof]] - GoF patterns adapted to prototypal OOP
- [[typescript-integration]] - classes with TypeScript type safety
- [MDN Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
- [MDN Inheritance and prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
