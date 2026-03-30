---
title: Database Selection
category: reference
tags: [database, postgresql, mongodb, cassandra, redis, storage]
---
# Database Selection

Choosing the right database requires matching data access patterns, consistency needs, scalability requirements, and team expertise against storage engine characteristics.

## Key Facts

- Database choice is step 5-6 of [[system-design-template]]: driven by access patterns from step 2 and quality attributes from step 3
- "I like ClickHouse" is not a valid justification. Correct: "ClickHouse fits our read-heavy analytics profile with columnar compression"
- MongoDB documentation uses terms loosely - "transactions" in Mongo are not equivalent to ACID transactions in PostgreSQL. Verify behavior against your consistency needs
- Redis documentation has similar terminological liberties. Always test actual behavior
- Multi-tenancy strategy (shared DB, schema-per-tenant, DB-per-tenant) affects database choice significantly
- Team expertise is a heavily weighted factor: a team proficient in PostgreSQL will deliver faster and with fewer bugs than switching to Cassandra for marginal benefits
- See [[cap-theorem]] for consistency vs availability tradeoffs
- See [[quality-attributes]] for deriving requirements that drive selection

## Patterns

### Database categories and use cases

```
Relational (PostgreSQL, MySQL):
  ACID transactions, complex queries, joins
  Use: orders, financial data, user accounts
  Scale: vertical + read replicas + sharding

Document (MongoDB, CouchDB):
  Flexible schema, nested documents
  Use: product catalogs, CMS, user profiles
  Scale: horizontal (sharding by key)

Wide-Column (Cassandra, ScyllaDB):
  High write throughput, tunable consistency
  Use: IoT data, time series, activity feeds
  Scale: linear horizontal (add nodes)

Key-Value (Redis, DynamoDB):
  Sub-millisecond latency, simple access
  Use: sessions, caches, counters, queues
  Scale: clustering + sharding

Graph (Neo4j, Amazon Neptune):
  Relationship traversal
  Use: social networks, recommendations, fraud
  Scale: limited horizontal

Time-Series (InfluxDB, TimescaleDB):
  Optimized for time-ordered data
  Use: metrics, monitoring, IoT sensors
  Scale: partitioned by time

Search (Elasticsearch, Meilisearch):
  Full-text search, faceted search
  Use: product search, log analysis
  Scale: index sharding

Vector (Pinecone, pgvector):
  Similarity search on embeddings
  Use: semantic search, recommendations, LLM RAG
  Scale: varies by implementation
```

### Selection comparison matrix

```
                  | PostgreSQL | MongoDB  | Cassandra | Redis
------------------+------------+----------+-----------+--------
Consistency       | Strong     | Tunable  | Tunable   | Strong*
Transactions      | Full ACID  | Multi-doc| No        | Pseudo
Query flexibility | SQL, rich  | MQL, ok  | Limited   | Key only
Write throughput  | ~100K TPS  | ~200K    | ~1M+      | ~100K
Read throughput   | ~500K TPS  | ~300K    | ~500K     | ~500K
Horizontal scale  | Limited    | Good     | Excellent | Cluster
JSON support      | Excellent  | Native   | Limited   | JSON type
Team learning     | Low        | Medium   | High      | Low
Operational cost  | Medium     | Medium   | High      | Low
```

*Redis: strong consistency in single instance; cluster mode introduces caveats

### Multi-tenancy strategies

```
Strategy 1: Shared tables (discriminator column)
  + Cheapest infrastructure
  + Simplest operations
  - Noisy neighbor risk
  - Schema changes affect all tenants
  Use when: <100 tenants, uniform workload

Strategy 2: Schema per tenant (same DB)
  + Better isolation
  + Schema changes per tenant possible
  - Connection pool management
  - Backup/restore per tenant is harder
  Use when: 100-1000 tenants, moderate isolation

Strategy 3: Database per tenant
  + Full isolation
  + Independent scaling
  + Easy tenant migration
  - Most expensive
  - Operational complexity
  Use when: >1000 tenants, strict SLA/compliance

Cross-tenant relationships:
  If tenants need to interact (rare), manage at
  application layer. DB-level cross-tenant queries
  are complex and often indicate wrong strategy.
```

### File storage decision

```
<1GB files, rare access:    Object store (S3/MinIO)
<1GB files, frequent:       CDN + Object store
>1GB files (video/backup):  Object store + streaming
Metadata about files:       Relational DB
Full-text file content:     Search engine (ES)
Big data analytics:         Data lake (Parquet/Delta)

Cost at scale:
  Object storage is cheapest per GB
  Block storage for DBs that need IOPS
  File system overhead increases with file count
```

## Gotchas

- **Symptom**: MongoDB "transactions" behave differently than expected -> **Cause**: Mongo multi-document transactions have different guarantees than PostgreSQL. Terms are used loosely in docs -> **Fix**: Test actual transactional behavior under failure conditions. For financial data, use PostgreSQL or another ACID-compliant DB
- **Symptom**: Redis runs out of memory, data lost -> **Cause**: Using Redis as primary store without persistence/eviction config -> **Fix**: If primary store: enable AOF persistence. If cache: configure maxmemory + eviction policy. Redis is single-threaded; plan capacity accordingly
- **Symptom**: Cassandra read latency is high -> **Cause**: Using Cassandra for relational query patterns (joins, aggregations) -> **Fix**: Cassandra is write-optimized with denormalized data model. Design tables around query patterns, not entity relationships. One table per query pattern
- **Symptom**: PostgreSQL cannot scale writes beyond single node -> **Cause**: Vertical scaling limit reached -> **Fix**: Consider logical partitioning (pg_partman), Citus extension for sharding, or CQRS pattern with separate write/read stores. Consider if you actually need this scale

## See Also

- [[cap-theorem]] - Consistency/availability tradeoffs by database type
- [[quality-attributes]] - Requirements driving database choice
- [[system-design-template]] - Database selection is step 5-6
- [[caching-strategies]] - Redis as cache vs database
- [[architectural-decision-records]] - Document the database choice as ADR
- Microsoft: [Choose a data store](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-overview)
