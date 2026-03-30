---
title: Data Access Patterns
category: architecture
tags: [repository, active-record, dto, orm, query-builder, data-mapper, database, sql]
---
# Data Access Patterns

Data access patterns define how application code interacts with databases. The choice between Repository, Active Record, DTO, and Query Builder affects testability, coupling, and how business logic relates to persistence.

## Key Facts

- **Repository**: interface for collection-like access to domain objects; hides query details behind methods
- **Active Record**: domain object knows how to save/load itself (`user.save()`, `User.find(id)`)
- **Data Mapper**: separate mapper object handles persistence; domain objects have no DB knowledge (Sequelize, TypeORM)
- **DTO (Data Transfer Object)**: plain object for moving data between layers; no behavior, only fields
- **Query Builder**: programmatic SQL construction; more control than ORM, less error-prone than raw strings
- Repository pattern separates business logic from data access (testable with mock repos)
- Active Record couples domain + persistence (simpler but harder to test/refactor)
- ORM (Sequelize, TypeORM, Prisma, Drizzle) provides Active Record or Data Mapper patterns
- **Prisma**: schema-first, generates typed client; not an ORM in traditional sense; query builder + code gen
- **Drizzle**: TypeScript-first, SQL-like syntax, lightweight, supports raw SQL escape hatches
- **Knex.js**: pure query builder; no model layer; use with Repository pattern
- N+1 query problem: eager loading (`include`/`join`) vs lazy loading (separate queries)
- Connection pooling is essential: `pg.Pool`, `mysql2.createPool`; set `max` connections based on load

## Patterns

```javascript
// Repository pattern (clean architecture)
class UserRepository {
  #db;
  constructor(db) { this.#db = db; }

  async findById(id) {
    const { rows } = await this.#db.query(
      'SELECT * FROM users WHERE id = $1', [id]
    );
    return rows[0] || null;
  }

  async findByEmail(email) {
    const { rows } = await this.#db.query(
      'SELECT * FROM users WHERE email = $1', [email]
    );
    return rows[0] || null;
  }

  async create(data) {
    const { rows } = await this.#db.query(
      `INSERT INTO users (name, email, password_hash)
       VALUES ($1, $2, $3) RETURNING *`,
      [data.name, data.email, data.passwordHash]
    );
    return rows[0];
  }

  async update(id, data) {
    const fields = Object.keys(data);
    const values = Object.values(data);
    const sets = fields.map((f, i) => `${f} = $${i + 2}`);
    const { rows } = await this.#db.query(
      `UPDATE users SET ${sets.join(', ')} WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    return rows[0];
  }
}

// DTO for API responses (strip internal fields)
function toUserDTO(user) {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    createdAt: user.created_at,
    // No password_hash, no internal flags
  };
}

// Query builder with Knex
const knex = require('knex')({ client: 'pg', connection: config.db });

class OrderRepository {
  async findWithFilters({ status, userId, fromDate, limit = 20 }) {
    const query = knex('orders').select('*');
    if (status) query.where('status', status);
    if (userId) query.where('user_id', userId);
    if (fromDate) query.where('created_at', '>=', fromDate);
    return query.orderBy('created_at', 'desc').limit(limit);
  }
}

// Transaction pattern
async function transferFunds(db, fromId, toId, amount) {
  const client = await db.connect();
  try {
    await client.query('BEGIN');
    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );
    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

// Prisma usage
// const user = await prisma.user.findUnique({
//   where: { id: 1 },
//   include: { posts: true }, // eager loading
// });
// const users = await prisma.user.findMany({
//   where: { active: true },
//   orderBy: { createdAt: 'desc' },
//   take: 20,
// });

// Connection pool configuration
const { Pool } = require('pg');
const pool = new Pool({
  host: process.env.DB_HOST,
  max: 20,              // max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

## Gotchas

- **Symptom**: N+1 queries (100 users = 101 queries) - **Cause**: lazy loading related data in a loop - **Fix**: use `JOIN` or batch queries (`WHERE id = ANY($1)`); ORM: use `include`/`eager` loading
- **Symptom**: connection pool exhausted - **Cause**: connections not released after use, or pool too small for load - **Fix**: always release connections in `finally`; use pool properly; tune `max` setting
- **Symptom**: SQL injection - **Cause**: string concatenation in queries - **Fix**: always use parameterized queries (`$1`, `?`); never interpolate user input into SQL
- **Symptom**: ORM generates inefficient queries - **Cause**: ORM abstraction hides actual SQL; complex joins produce suboptimal plans - **Fix**: log generated SQL; use raw queries or query builder for complex cases

## See Also

- [[solid-and-grasp]] - Repository implements SRP for data access
- [[dependency-injection]] - inject repository instances for testability
- [[nodejs/error-handling]] - database error classification
- [Node.js pg driver](https://node-postgres.com/)
- [Prisma docs](https://www.prisma.io/docs)
- [Drizzle ORM](https://orm.drizzle.team/)
