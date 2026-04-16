---
title: Database Selection and Design
category: reference
tags: [database, postgresql, redis, mongodb, cassandra, nosql, sql, orm]
---

# Database Selection and Design

Choosing the right database is an architectural decision with long-term consequences. Consider data type, consistency requirements, performance needs, team skills, and budget.

## OLTP vs OLAP

| Aspect | OLTP | OLAP |
|--------|------|------|
| Purpose | Real-time transactions | Analytical queries, reporting |
| Transactions | Many short | Few long-running |
| Examples | PostgreSQL, MySQL, Oracle | ClickHouse, BigQuery, Greenplum |
| Use case | Service operational data | DWH, analytics, reports |

## Selection by Data Type

| Data Type | DB Type | Example | Best For |
|-----------|---------|---------|----------|
| Structured | Relational | PostgreSQL | Orders, users, transactions |
| Documents/JSON | Document | MongoDB | Hierarchical, semi-structured |
| High-volume fast-changing | Key-Value | Redis | Sessions, caching |
| Analytics/reports | Columnar | ClickHouse, Cassandra | TB/PB aggregations |
| Binary/large files | Object storage | S3, MinIO | Images, video, audio |
| Relationships | Graph | Neo4j | Social networks, recommendations |

## Decision Tree

```rust
Need ACID transactions?
  Yes -> PostgreSQL (or MySQL)
Need flexible schema?
  Yes -> MongoDB
Need high write throughput (>500K TPS)?
  Yes -> Cassandra / ScyllaDB
Need sub-ms latency for simple keys?
  Yes -> Redis
Need full-text search?
  Yes -> Elasticsearch
Need relationship traversal?
  Yes -> Neo4j
Need analytical aggregations?
  Yes -> ClickHouse / BigQuery
```

## Database Deep Dives

### PostgreSQL
High write throughput, fast reads, JSON/XML support. Requires careful schema design.
- Use for: order processing, ACID-critical data, OLTP workloads
- OLAP extensions: GreenPlum, ClickHouse for analytical layer

### Redis
In-memory, key-value. Extremely fast reads/writes. Built-in TTL.
- Use for: sessions, caching, rate limiting, leaderboards
- Caveat: resource-intensive for large datasets (everything in RAM)

### MongoDB / CouchDB
Flexible schema (JSON documents). Fast development.
- Use for: hierarchical data, rapid prototyping, schema evolution
- Caveat: not ideal for complex transactions

### Cassandra
Column families, TB/PB scale. Excellent horizontal scalability.
- Use for: analytics, time-series, IoT data
- Caveat: not for frequent writes or complex transactions

### S3 / MinIO
Object storage. Scalable, granular access control.
- Use for: unstructured files (images, video, documents)
- Caveat: can be expensive at scale

## Database Design Fundamentals

### Normalization
- **1NF** - atomic values, no repeating groups
- **2NF** - all non-key attributes depend on entire primary key
- **3NF** - no transitive dependencies

### Keys
- **Primary Key** - unique row identifier
- **Foreign Key** - reference to PK in another table
- **Composite Key** - multiple columns as PK
- **Surrogate** - auto-generated (no business meaning)
- **Natural** - business-meaningful (email, SSN)

### Indexes
| Type | Best For |
|------|----------|
| B-Tree | Range queries, equality (default) |
| Hash | Fast equality lookups |
| GIN | Full-text search, JSONB |
| Partial | Subset of rows (WHERE clause) |

### ACID Transactions
- **Atomicity** - all or nothing
- **Consistency** - valid state to valid state
- **Isolation** - concurrent transactions don't interfere
- **Durability** - committed data survives failures

### Isolation Levels
| Level | Dirty Reads | Non-Repeatable | Phantom |
|-------|------------|----------------|---------|
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes |
| Serializable | No | No | No |

PostgreSQL default: Read Committed.

## ORM Considerations

**When to use:** Rapid development, standard CRUD, reducing boilerplate. One migration cut 1500 classes of manual SQL to 5x less code.

**When NOT to use:** Reports (raw SQL), high-load critical paths, complex analytical queries.

**Hybrid approach:** ORM for business logic, raw SQL for reports. Migration tools: Flyway, Liquibase (Java), Entity Framework migrations (.NET).

## Query Optimization

1. **EXPLAIN ANALYZE** - understand execution plan
2. **Index usage** - ensure queries hit indexes
3. **Avoid SELECT *** - retrieve only needed columns
4. **JOIN optimization** - proper order, indexes on join columns
5. **Connection pooling** - PgBouncer for PostgreSQL
6. **Partitioning** - split large tables (range/list/hash)
7. **Materialized views** - pre-computed for complex reports

## Scaling Patterns

- **Read replicas** - distribute read load
- **Sharding** - split data across DBs by key
- **Partitioning** - split tables within single DB
- **Hot/cold storage** - recent data on SSD, old data on cheap storage

## Gotchas

- **Shared database between microservices** is an anti-pattern - tight coupling, schema coordination problems
- **Premature NoSQL** - start with PostgreSQL unless you have clear NoSQL requirements
- **Redis as primary store** without persistence config = data loss on restart
- **N+1 query problem** - ORM lazy loading causes N+1 queries in loops. Use eager loading or batch fetching
- **Schema migration without rollback plan** - every migration needs corresponding rollback script
- **Confusing sharding with replication** - sharding splits data across machines; replication copies same data to multiple machines

## See Also

- [[solution-architecture-process]] - Database selection in architecture context
- [[caching-and-performance]] - Redis as cache, connection pooling
- [[distributed-systems-fundamentals]] - Sharding, replication, CAP
- [[bigdata-ml-architecture]] - OLAP, data warehousing
- [[devops-cicd]] - Zero-downtime database migrations
