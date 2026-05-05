# OIS Multi-environment Task Monitoring Architecture

The OIS infrastructure utilizes a uniform monorepo deployment across staging and production environments (RU and EN). While code paths are identical, environments are isolated by unique database hosts, S3 credentials, and Redis instances. Monitoring tasks across these environments requires aggregating data from two distinct state stores: PostgreSQL for persistence and Redis for live execution state.

## Data Sources and Environment Parity
Each environment runs the same service images (`oisgold/<service>`). Per-environment differences are strictly configuration-based (environment variables).

- **Database Persistence:** PostgreSQL stores task metadata within the `chat_message` table.
- **Live Queue State:** Redis BullMQ manages the execution lifecycle of jobs across five priority tiers.
- **Admin API:** Mounted under `/api/chat/admin/`, protected by `checkAdmin` middleware requiring a JWT or session cookie with `role: 'admin'`.

## PostgreSQL Message-Based State Persistence
The system does not use a dedicated `tasks` table. Instead, tasks are specialized `chat_message` rows identified by a JSON blob in the `text` field.

### Task Detection and Status Derivation
A row is considered a task if the `text` field is a JSON object containing an `items` array. Status is not stored as a column but is derived dynamically from JSON properties: `done`, `stopped`, `canceled`, and `items[].output`.

```sql
-- Query to identify active (not-done) tasks across all environments
SELECT id, chat_id, created_at, text
FROM chat_message
WHERE text LIKE '{%' 
  AND text::jsonb ? 'items'
  AND coalesce((text::jsonb->>'done')::boolean, false) = false
  AND coalesce((text::jsonb->>'stopped')::boolean, false) = false
  AND coalesce((text::jsonb->>'canceled')::boolean, false) = false
ORDER BY created_at DESC;
```

## Redis BullMQ Queue Management
Live job states (`waiting`, `active`, `delayed`, `paused`, `failed`) reside in BullMQ. OIS uses five specific queues to handle different priority levels and system tasks.

| Queue | Priority Tier | Target Users / Use Case |
|---|---|---|
| `image-high` | High | Enterprise and Corporate tiers |
| `image-medium` | Medium | Standard and Pro users |
| `image-low` | Low | Free plan users |
| `main` | System | Billing, webhooks, and email dispatch |
| `dead-letter` | N/A | Retried jobs (10 attempts, exponential backoff) |

### Job Identification
BullMQ jobs carry a payload in `job.data` that includes `{messageId, inputFileId}`. This metadata is essential for cross-referencing Redis jobs with PostgreSQL rows to detect "orphaned" tasks (DB rows marked as queued but missing a corresponding Redis job).

## Aggregation Strategy: The Collector Pattern
To provide a unified view without modifying production services, a pull-model aggregator (Collector) is implemented.

1. **Redis Subscription:** Collectors use BullMQ `QueueEvents` to listen for `waiting`, `active`, and `completed` events in real-time.
2. **PostgreSQL Polling:** A periodic poll (30-60s) identifies orphans and updates the unified dashboard state.
3. **Internal Trust Boundary:** The aggregator should ideally run within the VPC or use long-lived service JWTs to bypass standard session cookie requirements.

## Administrative Action API
Operators manage stuck or failed jobs via the `/api/chat/admin/tasks` endpoints.

### Restart and Recovery
- **Bulk Restart:** `POST /tasks/restart` with `messageIds[]` re-enqueues all incomplete files for specific messages.
- **Granular Restart:** `POST /tasks/restart-file` targets a single `inputFileId`.
- **DLQ Recovery:** `POST /tasks/dlq/retry` strips DLQ metadata and returns the job to its original queue.

### Stopping and Throttling
- **Stop Task:** `POST /tasks/stop` marks the DB row as `stopped=true` and removes the job from Redis while preserving existing outputs.
- **Queue Pause:** `Queue.pause()` is available via the BullMQ API but requires a custom admin endpoint to toggle execution for an entire priority tier (e.g., pausing `image-low` during peak load).

## Gotchas
- **Issue:** Task status is hidden in JSON → **Fix:** Use `jsonb` indexing or a PostgreSQL view to prevent sequential scans when filtering thousands of rows.
- **Issue:** Redis events can be missed during collector downtime → **Fix:** Always perform a full PostgreSQL snapshot and Redis queue scan (`getJobs`) upon collector startup to resynchronize state.
- **Issue:** BullMQ per-job pause is not native in OIS → **Fix:** Use the `/tasks/stop` endpoint; it effectively pauses work by removing the job from the queue and allows for later `restart`.
- **Issue:** Auth cookie expiration → **Fix:** For long-running monitors, use a Bearer JWT signed with the environment's private key rather than a human operator's session cookie.

## See Also
- [[monitoring-and-observability]]
- [[docker-fundamentals]]
- [[microservices-patterns]]
- [[runpod-production]]

