---
title: Write Buffering Patterns
category: reference
tags: [write-buffer, durable-objects, d1, queues, event-sourcing, offline-first, batch-insert, dirty-flag]
---

# Write Buffering Patterns

Durability and throughput patterns for absorbing high-frequency writes before a slow or
rate-limited canonical datastore. Covers pattern selection, single-writer coordination,
constraint tables, and concrete edge-stack mechanics.

## Key Facts

- D1 (SQLite-at-edge) write latency: **200-300 ms** (global primary routing, single-writer
  SQLite); read P99 ~8 ms. Source: production post-mortems, 2026.
- D1 `.batch()` benchmark: 5 000 rows in **14 ms** batched vs **78 ms** sequential. Source:
  rxliuli.com D1 optimization study.
- D1 hard cap: **10 GB** per database. Plan migrations before approaching this limit.
- D1 batch constraint: **max 100 bound parameters per statement**; at 10 columns → 10 rows
  per statement → chunk accordingly.
- [[caching-and-performance]] covers write-through/write-behind definitions at a conceptual
  level; this article focuses on durability mechanics and coordination primitives.
- Cloudflare KV eventual-consistency window: **60 s** global propagation; **1 write/s** per
  key rate limit; read-your-own-write only within a single PoP.
- Durable Object (DO) in-memory write: **< 1 ms**; ~500-1 000 req/s per instance for
  moderate logic; instances are co-located with routing Worker at same PoP.
- Cloudflare Queues: `max_batch_size` 1-100 (default 10), `max_batch_timeout` 0-60 s
  (default 5 s); at-least-once delivery; 1 M ops/month included then $0.40/M.
  Source: [Cloudflare Queues docs](https://developers.cloudflare.com/queues/configuration/batching-retries/).
- DO pricing: $0.15/M requests, 50 M rows written/month included then $1.00/M.
  Source: [Cloudflare DO pricing](https://developers.cloudflare.com/durable-objects/platform/pricing/).
- Offline-first sync batch size: **50 items/chunk** is an empirically validated sweet spot
  balancing request size and partial-failure recovery.

## Pattern Catalog

### Write-Through
Every write hits the fast store (cache/buffer) **and** the canonical datastore synchronously
before the client receives an ACK.

- **Latency:** full datastore round-trip visible to client (e.g. 200-300 ms for D1)
- **Durability:** strong - no separate flush needed
- **When to use:** low-volume writes where consistency matters more than speed; financial
  ledgers; operations that must be immediately readable by other services

### Write-Back (Write-Behind)
Client writes to a fast buffer; an asynchronous process flushes accumulated entries to the
canonical store in batches.

- **Latency for client:** sub-millisecond (buffer write only)
- **Durability risk:** buffer loss between write and flush
- **Coalescing benefit:** 100 updates to the same key = 1 datastore write
- **When to use:** high-frequency user-state writes (progress, preferences, counters);
  game state; any workload where per-operation DB latency is unacceptable
- Mitigation for loss risk: persist buffer to durable storage (DO Storage / Redis) immediately
  on receipt; in-memory copy serves reads, durable copy survives eviction

### Dirty-Flag (Game-Server Tick Pattern)
Server holds a mutable in-memory state object. Fields are tagged dirty on mutation. A
periodic flush ("tick") writes only dirty fields to the datastore and clears flags.

- **Granularity:** field-level, not operation-level - reduces write amplification
- **Conflict resolution:** last-write-wins (LWW) by timestamp is the standard resolution
  strategy when multiple clients may update the same field independently
- **When to use:** entity state that changes many times between persists (word-learning
  status, game entity position, form drafts); multi-device sync where a single canonical
  field value per entity is acceptable

```javascript
// Conceptual dirty-flag flush inside a single-writer coordinator
class EntityBuffer {
  state = {};    // { fieldName: { value, ts, dirty } }

  mutate(field, value, ts) {
    const current = this.state[field];
    if (!current || ts > current.ts) {
      this.state[field] = { value, ts, dirty: true };
    }
  }

  dirtyFields() {
    return Object.entries(this.state)
      .filter(([, v]) => v.dirty)
      .map(([k, v]) => ({ field: k, value: v.value, ts: v.ts }));
  }

  markClean() {
    for (const k of Object.keys(this.state)) this.state[k].dirty = false;
  }
}
```

### Batch-Flush
Accumulate writes in a buffer (in-memory or durable queue) and drain to the datastore in
a single transactional batch on a time or size trigger.

- **Trigger options:** elapsed time (alarm/cron), buffer size threshold, explicit client
  signal (navigation, tab close, reconnect)
- **Atomicity:** use DB-level batch/transaction so partial failures leave no half-written
  state; idempotent inserts (`INSERT OR REPLACE` / `ON CONFLICT DO UPDATE`) protect against
  at-least-once re-delivery
- **When to use:** any write-back implementation; queue consumer writing to DB;
  ETL micro-batch; sync-on-reconnect for offline clients

```sql
-- LWW upsert: newer timestamp wins, avoids overwriting fresher data
INSERT INTO entity_state (user_id, key, value, updated_at)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id, key)
DO UPDATE SET
  value      = CASE WHEN excluded.updated_at > entity_state.updated_at
                    THEN excluded.value ELSE entity_state.value END,
  updated_at = MAX(excluded.updated_at, entity_state.updated_at);
```

### Event Sourcing for User State
Append-only event log; current state is derived by replaying or compacting the log.
Periodic snapshots cap replay cost.

- **Write path:** every state change is an immutable append (e.g. `{userId, event: "saved",
  wordId, ts}`) - never an in-place update
- **Read path:** replay from last snapshot + subsequent events, or query materialized view
- **Coalescing via log compaction:** "user saved word X" then "user ignored word X" →
  compaction retains only the latter; reduces canonical store size
- **Offline-first fit:** client accumulates events in local store (IndexedDB / SQLite);
  syncs the entire event batch on reconnect; server merges by timestamp
- **When to use:** audit trail requirements; multi-device conflict resolution where full
  history matters; workloads where replaying events is acceptable over maintaining a
  mutable state table
- **When NOT to use:** simple CRUD state with no history value; high-volume counters where
  compaction overhead exceeds benefit

### Queues vs Single-Writer Coordinator

| Dimension | Message Queue (e.g. CF Queues) | DO-style Coordinator |
|---|---|---|
| Delivery guarantee | At-least-once | Exactly-once (single writer) |
| Client ACK | Fire-and-forget; no read-after-write guarantee | Synchronous ACK; client can read own writes |
| Ordering | Per-message FIFO within queue; no entity-level ordering | Per-entity serial (one instance = one entity) |
| Coalescing | None - each message is discrete | Full coalescing in-memory buffer |
| Cost @ 750 K writes/day | ~$0.50/month (after free tier) | ~$3/month (request cost) |
| Best for | One-way pipelines, analytics, audit logs, at-least-once acceptable | Interactive writes, user state, read-after-write required |

## Single-Writer Buffering — Durable Object Coordinator

A single DO instance per entity (user, session, game entity) serializes all writes,
holds an in-memory buffer, and uses a scheduled alarm to flush to the canonical store.

### Why single-writer matters
SQLite and similar single-writer stores serialize concurrent writes internally, causing
queuing under load. Pre-serializing at the coordinator layer converts N concurrent
client writes into a single scheduled batch, removing contention.

### Alarm-flush pattern

```javascript
// Cloudflare Durable Object - UserStateBuffer
export class UserStateBuffer extends DurableObject {
  buffer = [];  // in-memory; fast, lost on eviction

  async sync(payload) {
    // Persist to DO Storage first for durability across evictions
    const id = crypto.randomUUID();
    this.ctx.storage.sql.exec(
      'INSERT INTO pending (id, data) VALUES (?, ?)',
      id, JSON.stringify(payload)
    );
    this.buffer.push({ id, ...payload });

    // Schedule flush only if no alarm is already set
    if (!(await this.ctx.storage.getAlarm())) {
      await this.ctx.storage.setAlarm(Date.now() + 30_000); // 30 s window
    }
    return { ok: true };  // client ACK before D1 write
  }

  async alarm() {
    // Drain DO Storage (covers eviction scenario where in-memory buffer was lost)
    const rows = [...this.ctx.storage.sql.exec('SELECT id, data FROM pending').results];
    if (rows.length === 0) return;

    const stmts = rows.flatMap(r => buildD1Statements(JSON.parse(r.data)));
    await this.env.DB.batch(stmts);

    // Remove flushed entries
    const ids = rows.map(r => r.id);
    for (const id of ids) {
      this.ctx.storage.sql.exec('DELETE FROM pending WHERE id = ?', id);
    }
    this.buffer = this.buffer.filter(b => !ids.includes(b.id));

    // Reschedule if new writes arrived during flush
    if (this.buffer.length > 0) {
      await this.ctx.storage.setAlarm(Date.now() + 5_000);
    }
  }
}
```

```javascript
// Worker: route to per-user DO
async function handleSync(request, env) {
  const { userId, ...payload } = await request.json();
  const stub = env.USER_BUFFER.get(env.USER_BUFFER.idFromName(userId));
  return Response.json(await stub.sync(payload));
}
```

```javascript
// Helper: chunk rows respecting D1's 100 bound-parameter limit
function buildD1Statements(payload) {
  const stmts = [];
  if (payload.words) {
    for (const chunk of chunkArray(payload.words, 10)) { // 10 rows × 10 cols = 100 params
      stmts.push(buildUpsert('entity_state', chunk));
    }
  }
  return stmts;
}

function chunkArray(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}
```

### Output gates and visibility
DO storage writes without an intervening `await` are automatically coalesced into a single
implicit transaction (Cloudflare write coalescing). The client ACK returns before D1
commit, so optimistic UI updates must reconcile on reconnect using server timestamps.

## Constraints Table

| Store | Write Latency | Size Cap | Consistency Window | Rate Limit |
|---|---|---|---|---|
| D1 (SQLite-at-edge) | 200-300 ms (global primary) | 10 GB hard | Strong (single-writer) | Concurrent write contention |
| DO Storage (SQLite) | < 5 ms (local to PoP) | 1 GB per instance | Strong (local) | ~500-1 000 req/s per instance |
| Cloudflare KV | 5-10 ms write | No hard cap | 60 s eventual global | 1 write/s per key |
| Cloudflare Queues | 5-10 ms enqueue | Per-queue limits | At-least-once; no read-after-write | 400 msg/s default |
| Redis (self-hosted) | < 1 ms | RAM-bound | Configurable (AOF/RDB) | Depends on instance |

## Offline-First Sync Batch

Client accumulates writes locally (IndexedDB for PWA, SQLite for native mobile) and
replays the batch on reconnect or navigation events.

```typescript
// Client-side sync trigger
async function syncPendingWrites() {
  const pending = await localDb.getAll('pending_writes'); // IndexedDB
  if (pending.length === 0) return;

  // Chunk to 50 items per request to limit payload and enable partial retry
  for (const chunk of chunkArray(pending, 50)) {
    const res = await fetch('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client_ts: Date.now(), items: chunk }),
    });
    if (res.ok) {
      const ids = chunk.map(w => w.id);
      await localDb.deleteBatch('pending_writes', ids);
    }
    // On failure: leave chunk in local store, retry on next sync cycle
  }
}

// Trigger points
window.addEventListener('online', syncPendingWrites);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') syncPendingWrites();
});
```

**Conflict resolution:** LWW by `client_ts` is sufficient for independent per-user state
(vocabulary, preferences). For collaborative entities, prefer vector clocks or operational
transforms (see [[distributed-systems-fundamentals]]).

## Gotchas

- **Issue:** DO evicted from memory before alarm fires; in-memory buffer lost, writes
  silently dropped. -> **Fix:** Always write to DO Storage (durable SQLite) on receipt,
  keep in-memory copy only as a read-optimization. `alarm()` drains Storage, not
  `this.buffer`. Verify: restart the DO (let it idle 60 s) and confirm Storage still
  contains pending rows.

- **Issue:** KV used as a write queue; at peak load (> 1 write/s per key) the rate limit
  triggers 429s; 60 s eventual-consistency window breaks read-after-write assumptions
  (client writes, immediately reads, gets stale value from a different PoP). -> **Fix:**
  Do not use KV as a mutable write queue. Use Queues (one-way pipeline, no read-after-write)
  or DO (serialized per-entity with immediate local read). KV is appropriate for
  coarse-grained shared config, not per-user mutable state.

- **Issue:** D1 10 GB hard cap reached without warning; all writes begin failing. -> **Fix:**
  Monitor `d1_storage_bytes` metric; plan shard or migrate to Postgres/Hyperdrive before
  reaching ~8 GB. D1 is suitable for apps with bounded or archivable datasets; high-growth
  user-state tables need a migration path defined upfront.

- **Issue:** At-least-once Queue delivery causes duplicate rows when consumer crashes mid-batch.
  Idempotency not implemented, resulting in phantom duplicates. -> **Fix:** Use
  `INSERT OR REPLACE` / `ON CONFLICT DO UPDATE` keyed on a stable `(entity_id, event_ts)`
  composite. Never use plain `INSERT` for Queue-sourced writes.

- **Issue:** D1 batch silently truncates when a single statement exceeds 100 bound parameters
  (e.g. bulk-inserting 15 rows with 10 columns = 150 params). The batch proceeds for other
  statements but the oversized statement is dropped. -> **Fix:** Chunk input at `floor(100 /
  column_count)` rows per statement before constructing the batch. Enforce this in the helper
  that builds D1 statements, not at the call site.

## See Also

- [[caching-and-performance]] — write-through/write-behind conceptual definitions; cache
  hierarchy and invalidation strategies
- [[async-event-apis]] — delivery semantics (at-least-once, webhooks, polling); not
  covered here
- [[message-broker-patterns]] — Kafka log compaction, event sourcing at scale, consumer
  group coordination
- [[distributed-systems-fundamentals]] — vector clocks, LWW clock skew, replication lag
- [[database-selection]] — when to migrate from D1/SQLite to Postgres or a distributed store
- [[quality-attributes-reliability]] — durability SLOs, recovery time objectives
- [[queueing-theory]] — why write-burst latency is nonlinear; Little's Law applied to
  batch flush sizing

**Source research:**
- [Cloudflare DO: Rules of Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/)
- [Cloudflare Blog: SQLite in every Durable Object](https://blog.cloudflare.com/sqlite-in-durable-objects/)
- [Cloudflare D1 Limits](https://developers.cloudflare.com/d1/platform/limits/)
- [Cloudflare Queues: Batching and Retries](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Cloudflare KV: How KV Works](https://developers.cloudflare.com/kv/concepts/how-kv-works/)
- [Microsoft Azure: Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [AWS: Database Caching Strategies Using Redis](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
