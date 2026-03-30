---
title: SOLID and GRASP Principles
category: architecture
tags: [solid, grasp, srp, ocp, lsp, isp, dip, coupling, cohesion, information-expert]
---
# SOLID and GRASP Principles

SOLID and GRASP principles adapted for JavaScript, TypeScript, and async Node.js programming. The dynamic nature of JS requires reinterpretation: interfaces become protocols, DI uses factories and closures, and async boundaries create new coupling concerns.

## Key Facts

- **SRP (Single Responsibility)**: a module/class should have one reason to change; in Node.js, this maps to one module = one concern
- **OCP (Open/Closed)**: open for extension, closed for modification; in JS: use strategy pattern, event hooks, plugin registries
- **LSP (Liskov Substitution)**: subtypes must be substitutable; in JS: duck typing makes this about behavioral contracts, not type hierarchies
- **ISP (Interface Segregation)**: don't depend on methods you don't use; in JS: export granular functions instead of large utility objects
- **DIP (Dependency Inversion)**: depend on abstractions, not concretions; in JS: inject dependencies via constructor/factory, not `require()` at top level
- **GRASP Information Expert**: assign responsibility to the class/module that has the information needed to fulfill it
- **GRASP Creator**: assign creation responsibility to the class that contains/aggregates instances
- **GRASP Low Coupling**: minimize dependencies between modules; in Node.js: use event-driven communication between subsystems
- **GRASP High Cohesion**: keep related functionality together; one module should not mix HTTP handling with business logic with DB queries
- **GRASP Indirection**: introduce intermediary to reduce direct coupling (middleware, adapter, facade)
- **GRASP Polymorphism**: in JS, achieved via duck typing, strategy functions, or class hierarchy
- Over-engineering SOLID in JS is a common anti-pattern; principles should reduce complexity, not add ceremony

## Patterns

```javascript
// SRP: separate concerns into modules
// user-validator.js - only validation
const validateUser = (data) => {
  const errors = [];
  if (!data.email?.includes('@')) errors.push('Invalid email');
  if (!data.name?.trim()) errors.push('Name required');
  return errors;
};

// user-repository.js - only persistence
class UserRepository {
  constructor(db) { this.db = db; }
  async findById(id) { return this.db.query('SELECT * FROM users WHERE id = $1', [id]); }
  async create(data) { return this.db.query('INSERT INTO users ...', [data]); }
}

// user-service.js - orchestration
class UserService {
  constructor(repo, validator, eventBus) {
    this.repo = repo;
    this.validator = validator;
    this.eventBus = eventBus;
  }
  async createUser(data) {
    const errors = this.validator(data);
    if (errors.length) throw new ValidationError(errors);
    const user = await this.repo.create(data);
    this.eventBus.emit('user:created', user);
    return user;
  }
}

// OCP: extension via plugin registry
class Processor {
  #plugins = new Map();
  register(type, handler) { this.#plugins.set(type, handler); }
  process(item) {
    const handler = this.#plugins.get(item.type);
    if (!handler) throw new Error(`No handler for ${item.type}`);
    return handler(item);
  }
}
// Adding new types doesn't modify Processor code
processor.register('image', handleImage);
processor.register('video', handleVideo);

// DIP: dependency injection via factory
function createApp({ db, cache, logger }) {
  const userRepo = new UserRepository(db);
  const userService = new UserService(userRepo, validateUser, new EventEmitter());

  return {
    userService,
    async shutdown() {
      await db.close();
      await cache.close();
    }
  };
}
// In production:
const app = createApp({ db: pgPool, cache: redis, logger: pino() });
// In tests:
const app = createApp({ db: mockDb, cache: mockCache, logger: noopLogger });

// ISP: granular exports
// Bad: module.exports = { parseJSON, parseXML, parseCSV, parseYAML, ... }
// Good: separate modules
// parsers/json.js  -> exports parseJSON
// parsers/csv.js   -> exports parseCSV
// parsers/index.js -> re-exports all (optional)

// GRASP Low Coupling: events instead of direct calls
class OrderService extends EventEmitter {
  async complete(orderId) {
    const order = await this.repo.complete(orderId);
    this.emit('order:completed', order); // decoupled
  }
}
// Listeners registered elsewhere, not in OrderService
orderService.on('order:completed', (order) => emailService.sendReceipt(order));
orderService.on('order:completed', (order) => analytics.track('purchase', order));
```

## Gotchas

- **Symptom**: over-abstracted code with too many layers - **Cause**: applying SOLID dogmatically without cost-benefit analysis - **Fix**: principles serve readability and maintainability; if abstraction adds complexity without reducing it elsewhere, remove it
- **Symptom**: hard to test due to `require()` at top level - **Cause**: DIP violation; module creates its own dependencies - **Fix**: inject dependencies via constructor/factory; use the module factory pattern
- **Symptom**: changing one feature requires touching 10 files - **Cause**: poor cohesion; related code scattered across too many modules - **Fix**: group by feature/domain, not by technical layer
- **Symptom**: "god module" that handles everything - **Cause**: SRP violation - **Fix**: extract responsibilities into focused modules

## See Also

- [[dependency-injection]] - DIP implementation strategies in Node.js
- [[design-patterns-gof]] - patterns that implement SOLID principles
- [[data-access-patterns]] - Repository as SRP + ISP example
- [SOLID explained for Node.js (Shemsedinov)](https://github.com/nicoschmdt/SOLID-In-JavaScript)
