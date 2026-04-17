---
title: Go Database Patterns - PostgreSQL, MongoDB, Redis
category: concepts
tags: [go, golang, postgresql, mongodb, redis, database, caching, transactions]
---

# Go Database Patterns - PostgreSQL, MongoDB, Redis

Production database patterns in Go - PostgreSQL with pgx, MongoDB with official driver, Redis caching, transactional outbox, and migration management.

## Key Facts

- pgx is the recommended PostgreSQL driver for Go (pure Go, connection pooling, prepared statements)
- goqu/Squirrel provide type-safe SQL building that prevents injection
- Goose handles migrations with `-- +goose Up` / `-- +goose Down` annotations
- BSON (Binary JSON) is MongoDB's wire format - use `bson.M`, `bson.D`, or typed structs
- Redis cache-aside pattern: check cache first, fall back to DB, write-through on miss
- Transactional outbox solves atomic DB update + message publish without two-phase commit

## Patterns

### PostgreSQL with pgx

```go
// Connection pool
pool, err := pgxpool.New(ctx, os.Getenv("DB_URI"))

// Transaction helper - transaction from context
func getTx(ctx context.Context) pgx.Tx {
    tx, ok := ctx.Value(txKey).(pgx.Tx)
    if !ok { return nil }
    return tx
}

// Run in transaction
func (r *Repo) RunInTransaction(ctx context.Context, fn func(ctx context.Context) error) error {
    tx, err := r.pool.Begin(ctx)
    if err != nil { return err }
    ctx = context.WithValue(ctx, txKey, tx)
    if err := fn(ctx); err != nil {
        tx.Rollback(ctx)
        return err
    }
    return tx.Commit(ctx)
}
```

### Migrations with Goose

```sql
-- +goose Up
CREATE TABLE users (...);

-- +goose Down
DROP TABLE IF EXISTS users;
```

Run via `goose up/down/status`. Embed migration files in binary with `//go:embed migrations/*.sql`.

### MongoDB with mongo-driver

```go
client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
db := client.Database("mydb")
coll := db.Collection("notes")

result, err := coll.InsertOne(ctx, bson.M{"title": "test"})
cursor, err := coll.Find(ctx, bson.M{"title": bson.M{"$regex": "^test"}})
```

Create indexes explicitly on startup for query patterns you rely on. Text indexes for full-text search.

### Redis Cache-Aside

```go
type CacheRepository interface {
    Get(ctx context.Context, key string) (*model.Item, error)
    Set(ctx context.Context, key string, item *model.Item, ttl time.Duration) error
    Delete(ctx context.Context, key string) error
}

func (s *Service) GetItem(ctx context.Context, id string) (*model.Item, error) {
    if item, err := s.cache.Get(ctx, id); err == nil {
        return item, nil
    }
    item, err := s.repo.Get(ctx, id)
    if err != nil { return nil, err }
    s.cache.Set(ctx, id, item, 15*time.Minute)
    return item, nil
}
```

**Key patterns**:
- `{service}:{entity}:{id}` naming convention
- Set TTL on all cache entries (avoid stale data)
- `SETNX` (SET if Not eXists) for distributed locks
- `DEL` or `UNLINK` (async delete) on invalidation

**Graceful degradation**: if Redis is unavailable, service continues from primary DB.

### Transactional Outbox

Problem: need to atomically update DB and send Kafka message. Two-phase commit is impractical.

Solution:
1. Same DB transaction: update domain entity + insert event to `outbox` table
2. Background poller reads unsent outbox events, publishes to Kafka, marks sent
3. Deduplication: consumer uses idempotency keys for duplicate delivery

Poller can be a goroutine with `time.Ticker` or triggered by DB `LISTEN/NOTIFY`.

## Gotchas

- pgx connection pool must be closed on shutdown to avoid connection leaks
- MongoDB indexes must be created explicitly - there are no automatic indexes beyond `_id`
- Redis `SETNX` for locks needs TTL to prevent deadlock on crash
- Goose migration ordering is by filename timestamp prefix - keep them sequential
- `bson.M` is unordered; use `bson.D` when order matters (e.g., compound indexes)

## See Also

- [[microservices]] - clean architecture, DI, project layout
- [[kafka-messaging-fundamentals]] - delivery semantics for outbox consumers
- [[sql-databases/advanced-patterns]] - window functions, subqueries (PostgreSQL)
