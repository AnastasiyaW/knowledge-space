---
title: Dependency Injection
category: architecture
tags: [dependency-injection, di, ioc, inversion-of-control, container, testability, factory]
---
# Dependency Injection

Dependency Injection (DI) in Node.js means passing dependencies to a module/class from the outside instead of hardcoding `require()` calls. This enables testability, loose coupling, and configurable application composition.

## Key Facts

- DI is the practical application of the Dependency Inversion Principle ([[solid-and-grasp]])
- Three injection styles: **constructor injection** (most common), **parameter injection**, **property injection**
- In Node.js, the simplest DI is the **factory function**: `createService(dep1, dep2) => service`
- Module-level `require()` creates hard coupling; inject via constructor for testability
- **Composition root**: the single place where all dependencies are wired together (usually `app.js` or `main.js`)
- IoC containers (awilix, tsyringe, inversify) automate resolution but add complexity
- For most Node.js apps, manual DI (factory functions) is sufficient and more debuggable
- DI makes testing trivial: pass mocks/stubs instead of real implementations
- Avoid "service locator" anti-pattern: don't pass the container around; resolve at the root
- In TypeScript: interfaces define the dependency contract; runtime injection provides the implementation

## Patterns

```javascript
// Manual DI with factory functions (recommended for most apps)
// services/user-service.js
function createUserService({ userRepo, hasher, eventBus }) {
  return {
    async register(email, password) {
      const hash = await hasher.hash(password);
      const user = await userRepo.create({ email, passwordHash: hash });
      eventBus.emit('user:registered', user);
      return user;
    },
    async authenticate(email, password) {
      const user = await userRepo.findByEmail(email);
      if (!user) return null;
      const valid = await hasher.verify(password, user.passwordHash);
      return valid ? user : null;
    },
  };
}
module.exports = createUserService;

// Composition root (app.js)
const createUserService = require('./services/user-service');
const createUserRepo = require('./repos/user-repo');
const { createHasher } = require('./lib/hasher');
const { EventEmitter } = require('events');

function createApp(config) {
  const db = createPool(config.db);
  const eventBus = new EventEmitter();
  const hasher = createHasher({ rounds: 12 });
  const userRepo = createUserRepo(db);
  const userService = createUserService({ userRepo, hasher, eventBus });

  return { userService, eventBus, shutdown: () => db.end() };
}

// Testing with mocks
const { test } = require('node:test');
const assert = require('node:assert');

test('register hashes password and stores user', async () => {
  const mockRepo = {
    create: async (data) => ({ id: 1, ...data }),
  };
  const mockHasher = {
    hash: async (pw) => `hashed_${pw}`,
  };
  const mockBus = { emit: () => {} };

  const service = createUserService({
    userRepo: mockRepo,
    hasher: mockHasher,
    eventBus: mockBus,
  });

  const user = await service.register('a@b.com', 'secret');
  assert.strictEqual(user.passwordHash, 'hashed_secret');
});

// Class-based DI
class NotificationService {
  #mailer;
  #sms;
  #logger;

  constructor({ mailer, sms, logger }) {
    this.#mailer = mailer;
    this.#sms = sms;
    this.#logger = logger;
  }

  async notify(user, message) {
    try {
      if (user.prefersSms) {
        await this.#sms.send(user.phone, message);
      } else {
        await this.#mailer.send(user.email, message);
      }
    } catch (err) {
      this.#logger.error('Notification failed', { userId: user.id, err });
      throw err;
    }
  }
}

// IoC container with awilix (for larger apps)
const { createContainer, asClass, asFunction } = require('awilix');

const container = createContainer();
container.register({
  db: asFunction(createPool).singleton(),
  userRepo: asClass(UserRepository).scoped(),
  userService: asClass(UserService).scoped(),
});

const userService = container.resolve('userService');
```

## Gotchas

- **Symptom**: hard to trace where a dependency comes from - **Cause**: IoC container magic; dependencies resolved by name matching - **Fix**: use explicit factory functions for small-to-medium apps; containers only for large codebases
- **Symptom**: circular dependency between services - **Cause**: Service A depends on Service B and vice versa - **Fix**: introduce an event bus or mediator; restructure so one depends on an abstraction
- **Symptom**: test setup is extremely verbose - **Cause**: too many dependencies to mock - **Fix**: service has too many responsibilities (SRP violation); split into focused services
- **Symptom**: service locator pattern - passing the container to all services - **Cause**: resolving deps inside business logic instead of at composition root - **Fix**: resolve all deps at the root; pass only what each service needs

## See Also

- [[solid-and-grasp]] - DIP principle behind DI
- [[design-patterns-gof]] - factory pattern enables DI
- [[modules-and-packages]] - module system as implicit DI (and its limitations)
- [awilix - IoC container for Node.js](https://github.com/jeffijoe/awilix)
