---
title: "Go-Datenbankmuster - PostgreSQL, MongoDB, Redis"
category: concepts
tags: [go, golang, postgresql, mongodb, redis, database, caching, transactions]
level: 3
source_sha256: 112314f32db3db529523fb49021810eb42bae42d637140b36243bad85af4418f
translation: machine
translated_at: '2026-10-24'
---
# Go-Datenbankmuster - PostgreSQL, MongoDB, Redis {#go-database-patterns-postgresql-mongodb-redis}

Produktionsreife Datenbankmuster in Go - PostgreSQL mit pgx, MongoDB mit dem offiziellen Treiber, Redis-Caching, Transactional Outbox und Migrationsverwaltung.

## Wichtige Fakten {#key-facts}

- pgx ist der empfohlene PostgreSQL-Treiber für Go (reines Go, Connection-Pooling, Prepared Statements)
- goqu/Squirrel bieten typsicheren SQL-Aufbau, der Injection verhindert
- Goose verwaltet Migrationen mit `-- +goose Up` / `-- +goose Down`-Annotationen
- BSON (Binary JSON) ist das Wire-Format von MongoDB - verwende `bson.M`, `bson.D` oder typisierte Structs
- Redis-Cache-Aside-Muster: zuerst den Cache prüfen, bei Miss auf die DB zurückfallen und per Write-Through schreiben
- Transactional Outbox löst das atomare Aktualisieren der DB und das Veröffentlichen einer Nachricht ohne Two-Phase Commit

## Muster {#patterns}

### PostgreSQL mit pgx {#postgresql-with-pgx}

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

### Migrationen mit Goose {#migrations-with-goose}

```sql
-- +goose Up
CREATE TABLE users (...);

-- +goose Down
DROP TABLE IF EXISTS users;
```

Ausführung über `goose up/down/status`. Migrationsdateien mit `//go:embed migrations/*.sql` in das Binary einbetten.

### MongoDB mit mongo-driver {#mongodb-with-mongo-driver}

```go
client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
db := client.Database("mydb")
coll := db.Collection("notes")

result, err := coll.InsertOne(ctx, bson.M{"title": "test"})
cursor, err := coll.Find(ctx, bson.M{"title": bson.M{"$regex": "^test"}})
```

Indizes für die benötigten Abfragemuster beim Start explizit anlegen. Text-Indizes für die Volltextsuche.

### Redis Cache-Aside {#redis-cache-aside}

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

**Zentrale Muster**:
- Namenskonvention `{service}:{entity}:{id}`
- TTL für alle Cache-Einträge setzen (vermeidet veraltete Daten)
- `SETNX` (SET if Not eXists) für verteilte Locks
- `DEL` oder `UNLINK` (asynchrones Löschen) bei Invalidierung

**Graceful Degradation**: Ist Redis nicht erreichbar, arbeitet der Service weiter mit der primären DB.

### Transactional Outbox {#transactional-outbox}

Problem: DB-Aktualisierung und Kafka-Nachricht müssen atomar erfolgen. Two-Phase Commit ist unpraktikabel.

Lösung:
1. Gleiche DB-Transaktion: Domänenentität aktualisieren und Ereignis in die Tabelle `outbox` einfügen
2. Ein Hintergrund-Poller liest nicht gesendete Outbox-Ereignisse, veröffentlicht sie in Kafka und markiert sie als gesendet
3. Deduplizierung: Der Consumer verwendet Idempotenzschlüssel für doppelt zugestellte Nachrichten

Der Poller kann eine Goroutine mit `time.Ticker` sein oder durch `LISTEN/NOTIFY` der DB ausgelöst werden.

## Fallstricke {#gotchas}

- Der pgx-Connection-Pool muss beim Herunterfahren geschlossen werden, um Connection-Leaks zu vermeiden
- MongoDB-Indizes müssen explizit angelegt werden - außer `_id` gibt es keine automatischen Indizes
- `SETNX` für Locks benötigt eine TTL, um bei einem Absturz einen Deadlock zu verhindern
- Die Reihenfolge der Goose-Migrationen richtet sich nach dem Zeitstempel-Präfix des Dateinamens - sie sollten fortlaufend bleiben
- `bson.M` ist ungeordnet; verwende `bson.D`, wenn die Reihenfolge wichtig ist (z. B. bei zusammengesetzten Indizes)

## Siehe auch {#see-also}

- [[microservices]] - Clean Architecture, DI, Projektstruktur
- [[kafka-messaging-fundamentals]] - Zustellungssemantik für Outbox-Consumer
- [[sql-databases/advanced-patterns]] - Window Functions, Subqueries (PostgreSQL)
