---
title: Database Cursors
category: concepts
tags: [sql-databases, cursor, server-side-cursor, client-side-cursor, batch-processing, postgresql, psycopg2]
---

# Database Cursors

A cursor is a pointer to a result set that enables row-by-row or batch processing instead of fetching all results at once. The choice between client-side and server-side cursors has significant performance implications.

## Client-Side Cursors (Default)

Database executes query and transfers ALL results to client. Client holds result set in memory and iterates locally.

```python
# Default psycopg2 cursor (client-side)
cur = conn.cursor()
cur.execute("SELECT * FROM large_table")
rows = cur.fetchall()  # ALL rows loaded into Python memory
```

**Pros:** Frees server resources after transfer, fast local iteration.
**Cons:** High network bandwidth (entire result set), client memory pressure, slow initial execution.

## Server-Side Cursors

Database holds results on server. Client fetches in small batches via FETCH requests.

```python
# psycopg2 named cursor (server-side)
cur = conn.cursor(name='server_cursor')
cur.execute("SELECT * FROM large_table")
batch = cur.fetchmany(1000)  # fetch 1000 rows at a time
```

```sql
-- SQL-level cursor
DECLARE my_cursor CURSOR FOR SELECT * FROM large_table;
FETCH 100 FROM my_cursor;
CLOSE my_cursor;
```

**Pros:** ~3ms initial execution, minimal client memory, low per-batch network.
**Cons:** Each FETCH = network round-trip, server holds state in memory, cursor leak risk.

## When to Use Which

| Scenario | Recommendation |
|----------|---------------|
| Small result set, need all data | Client-side |
| Large result set, only need partial | Server-side |
| Streaming/pipeline processing | Server-side |
| Simple CRUD operations | Client-side (default) |

## Key Facts

- Server-side cursors keep server resources allocated until explicitly closed
- Always close/deallocate cursors explicitly to prevent leaks
- Avoid cursors when set-based operations work (UPDATE...SET, INSERT...SELECT)
- In PgBouncer transaction mode, server-side cursors must be opened and closed within same transaction
- PostgreSQL server-side cursors require an active transaction (BEGIN/COMMIT)

## Gotchas

- Cursor leaks with many concurrent clients can exhaust server memory
- Connection pooling complicates server-side cursors - cursor state tied to connection
- Set-based operations (JOINs, UPDATEs) are almost always faster than cursor-based row-by-row processing
- Named cursors in psycopg2 auto-create server-side cursors with `itersize` controlling batch size

## See Also

- [[connection-pooling]] - cursor behavior with pooled connections
- [[query-optimization-explain]] - prefer set-based operations over cursors
- [[select-fundamentals]] - LIMIT/OFFSET as alternative to cursors
