---
title: Connection Pooling
category: concepts
tags: [sql-databases, connection-pooling, pgbouncer, proxysql, pool-sizing, postgresql, mysql]
---

# Connection Pooling

Each database connection is expensive: TCP handshake, TLS negotiation, authentication, and backend process spawn (PostgreSQL) or thread allocation (MySQL). Connection pooling reuses pre-established connections across application requests.

## Why Pool

- PostgreSQL: each connection = a separate OS process (fork)
- MySQL: each connection = a thread
- Opening/closing per request wastes resources and adds latency
- 10 app instances x 20 connections each = 200 DB connections without external pooler

## PgBouncer (PostgreSQL)

Lightweight proxy between application and PostgreSQL.

### Pooling Modes

| Mode | Behavior | Compatibility |
|------|----------|---------------|
| **Session** | Connection held for entire client session | Full - all features work |
| **Transaction** | Connection returned after each transaction | No prepared statements, no session-level SET, no LISTEN/NOTIFY |
| **Statement** | Connection returned after each statement | Breaks multi-statement transactions |

Transaction mode is recommended for most production use - best balance of pooling efficiency and compatibility.

### Pool Sizing Formula

```
connections = (cpu_cores * 2) + effective_spindle_count
```

For SSD with 4 cores: ~9-10 connections. More connections != more throughput (context switching, lock contention overhead).

PgBouncer `default_pool_size = 20` per user/database pair.

## ProxySQL (MySQL)

Connection multiplexing, query routing, read/write splitting, query caching. Richer feature set than PgBouncer equivalent for MySQL ecosystem.

## Application-Level Pooling

```javascript
// Node.js with pg (node-postgres)
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: 'postgresql://user:pass@host:5432/db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Transaction pattern
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO orders ...');
  await client.query('UPDATE inventory ...');
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}
```

## Key Facts

- PgBouncer is single-threaded (use multiple instances for high throughput)
- Odyssey (Yandex) is multi-threaded alternative to PgBouncer
- pgcat is a newer Rust-based pooler with sharding support
- Connection pool too small: requests queue waiting for available connections
- Connection pool too large: database overwhelmed, context switching overhead

## Gotchas

- **Prepared statements** broken in PgBouncer transaction mode (connection reused, prepared statement gone)
- **SET commands** lost when connection returned to pool (session settings reset)
- **Advisory session locks** released when PgBouncer reassigns connection in transaction mode
- **Long transactions** hold connections, starving other requests
- **Connection leaks** from forgetting to release connections back to pool
- **LISTEN/NOTIFY** requires session-mode pooling (persistent connection)

## See Also

- [[postgresql-configuration-tuning]] - max_connections setting
- [[postgresql-ha-patroni]] - HAProxy for connection routing
- [[transactions-and-acid]] - transaction behavior with poolers
- [[concurrency-and-locking]] - lock behavior across pooled connections
