---
title: Data Access Patterns
category: patterns
tags: [nodejs, repository, active-record, cursor, transaction, dal, orm]
---

# Data Access Patterns

The data access layer (DAL) separates business logic from physical storage, providing abstract CRUD operations, connection pool management, and session-scoped connections. Node.js applications benefit from Repository, Active Record, Cursor, and Transaction patterns for both database and in-memory data.

## Key Facts

- Business logic should NEVER contain raw database queries
- DAL provides: API functions, cached schemas/data, connection pools, session/user-scoped connections
- Different users may have different DB permissions - connection pools must support user-scoped connections
- **Repository** preferred for complex domains: multiple repositories per entity (User for HR, billing, access control)
- **Active Record** simpler but mixes concerns: object maps directly to DB row with save/delete built in
- Cache in DAO layer if it depends on implementation details (cache by ID); cache in service layer if it depends on business logic
- ORM criticism: TypeORM forces unnecessary boilerplate; Prisma generates type-unsafe code (`any` returns)

## Patterns

### Repository Pattern

```js
// Clean separation of domain and persistence
class UserRepository {
  #pool;
  constructor(pool) { this.#pool = pool; }

  async findById(id) {
    const { rows } = await this.#pool.query(
      'SELECT * FROM users WHERE id = $1', [id]
    );
    return rows[0] ? this.#toDomain(rows[0]) : null;
  }

  async save(user) {
    await this.#pool.query(
      'INSERT INTO users (id, name, email) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET name = $2, email = $3',
      [user.id, user.name, user.email]
    );
  }

  #toDomain(row) { return { id: row.id, name: row.name, email: row.email }; }
}
```

### In-Memory Transactions

```js
class Transaction {
  #operations = [];
  #committed = false;

  add(operation) { this.#operations.push(operation); }

  commit() {
    for (const op of this.#operations) op.execute();
    this.#committed = true;
  }

  rollback() {
    if (this.#committed) {
      for (const op of this.#operations.reverse()) op.undo();
    }
    this.#operations = [];
  }
}
```

Even pure-JavaScript applications benefit from transactional patterns for complex state mutations.

### Template Method for Business Operations

```js
class MoneyTransfer {
  async process(request) {
    await this.validate(request);     // overridable
    await this.checkBalance(request); // overridable
    await this.execute(request);      // overridable
    await this.notify(request);       // overridable
  }
}

class InternationalTransfer extends MoneyTransfer {
  async validate(request) { /* compliance checks */ }
  async execute(request) { /* SWIFT/correspondent bank */ }
}
```

## Database Integration Anti-patterns

### Shared Database Problem

When multiple services write to the same database:
- No one knows which table/column belongs to which service
- Tables only grow (no one dares delete unknown columns)
- Within 5 years, the database becomes unmaintainable legacy

**Solution:** Each service owns its data. Integration through APIs/events, not shared tables.

### PostgreSQL Indexing

- Does NOT auto-create composite indexes
- Defining 3 fields does NOT create all possible combinations
- Data may be duplicated between table and indexes (by design)
- Query planner automatically chooses which indexes for JOINs, ORDER BY, GROUP BY

## Gotchas

- Don't do metaprogramming in TypeScript - write meta-heavy libraries in JS, type them with `.d.ts`; 100 lines of JS replaces 500+ lines of TypeScript
- Connection pools needed because Node.js serves multiple concurrent users in one process
- Active Record's `save()` mixes persistence with domain logic, making it unclear where to put cross-cutting concerns

## See Also

- [[application-architecture]] - how DAL fits into layered architecture
- [[dependency-injection]] - injecting repositories vs using module singletons
- [[design-patterns-gof]] - Template Method, Repository as GoF applications
