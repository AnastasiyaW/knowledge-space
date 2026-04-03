---
title: ksqlDB
category: concepts
tags: [kafka, ksqldb, sql, streaming, push-query, pull-query, materialized-view]
---

# ksqlDB

ksqlDB is a streaming SQL engine built on Kafka Streams that translates SQL statements into Kafka Streams topologies, enabling stream processing without JVM programming.

## Key Facts

- Part of Confluent Platform (not Apache Kafka core)
- Runs as JVM application connecting to Kafka cluster; each persistent query runs as a Kafka Streams application
- SQL statements are converted into Kafka Streams topologies under the hood
- **STREAM** = partitioned, immutable, append-only collection (maps to KStream)
- **TABLE** = mutable, partitioned collection where updates overwrite previous values (maps to KTable)
- **Push queries**: run continuously, emit results as new data arrives (`EMIT CHANGES`)
- **Pull queries**: one-time point-in-time result on materialized tables (like traditional SQL SELECT)
- Deployment modes: **Interactive** (CLI/REST) and **Headless/Autonomous** (queries from file only, production mode)
- Supports formats: JSON, AVRO, PROTOBUF, DELIMITED (CSV), KAFKA (raw bytes)
- Integrates with [[schema-registry]] automatically when using AVRO/PROTOBUF
- Default port: 8088 (REST API)
- ksqlDB is NOT a replacement for a database - it processes streams

## Patterns

### DDL - Create Stream and Table

```sql
CREATE STREAM pageviews (
  viewtime BIGINT,
  userid VARCHAR,
  pageid VARCHAR
) WITH (KAFKA_TOPIC='pageviews', VALUE_FORMAT='JSON');

CREATE TABLE users (
  userid VARCHAR PRIMARY KEY,
  regionid VARCHAR,
  gender VARCHAR
) WITH (KAFKA_TOPIC='users', VALUE_FORMAT='JSON');
```

### Persistent Queries (Continuous Processing)

```sql
-- Continuous aggregation with join
CREATE TABLE pageviews_per_region AS
  SELECT regionid, COUNT(*) AS numusers
  FROM pageviews LEFT JOIN users ON pageviews.userid = users.userid
  GROUP BY regionid
  EMIT CHANGES;

-- Filtering stream
CREATE STREAM pageviews_female AS
  SELECT * FROM pageviews
  LEFT JOIN users ON pageviews.userid = users.userid
  WHERE gender = 'FEMALE'
  EMIT CHANGES;
```

### Windowed Aggregations

```sql
CREATE TABLE order_count AS
  SELECT customerid, COUNT(*) AS cnt, SUM(amount) AS total
  FROM orders
  WINDOW TUMBLING (SIZE 1 HOUR)
  GROUP BY customerid
  EMIT CHANGES;

-- Hopping window with retention
WINDOW HOPPING (SIZE 30 SECONDS, ADVANCE BY 10 SECONDS,
                RETENTION 7 DAYS, GRACE PERIOD 30 MINUTES)

-- Session window
WINDOW SESSION (5 MINUTES)
```

### Joins

```sql
-- Stream-Table join (enrichment, no window needed)
CREATE STREAM enriched_orders AS
  SELECT o.orderid, o.amount, c.name, c.region
  FROM orders o LEFT JOIN customers c ON o.customerid = c.id
  EMIT CHANGES;

-- Stream-Stream join (must be windowed)
CREATE STREAM combined AS
  SELECT * FROM stream1 s1
  INNER JOIN stream2 s2 WITHIN 1 HOUR ON s1.id = s2.id
  EMIT CHANGES;
```

### REST API

```bash
# Execute statement
curl -X POST http://localhost:8088/ksql \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"ksql": "SHOW STREAMS;", "streamsProperties": {}}'

# Run query
curl -X POST http://localhost:8088/query \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"ksql": "SELECT * FROM pageviews EMIT CHANGES;"}'
```

### Useful Commands

```sql
SHOW TOPICS;                    SHOW STREAMS;
SHOW TABLES;                    SHOW QUERIES;
DESCRIBE stream_name;           DESCRIBE EXTENDED stream_name;
PRINT 'topic_name' FROM BEGINNING;
DROP STREAM stream_name;        TERMINATE query_id;
INSERT INTO stream_name (col1) VALUES ('val1');
```

### Event Metadata Pseudo-Columns

```sql
SELECT ROWTIME, ROWPARTITION, ROWOFFSET, HEADERS FROM stream EMIT CHANGES;
```

### Kafka Connect Integration

```sql
-- External Connect cluster
-- Server config: ksql.connect.url=http://localhost:8083

-- Or embedded mode: ksql.connect.worker.config=...

CREATE SOURCE CONNECTOR `postgres-source` WITH (
  'connector.class' = 'io.confluent.connect.jdbc.JdbcSourceConnector',
  'connection.url' = 'jdbc:postgresql://localhost:5432/db',
  'table.whitelist' = 'orders',
  'mode' = 'incrementing'
);
SHOW CONNECTORS;
DESCRIBE CONNECTOR `postgres-source`;
```

### Functions

Built-in scalar: `SUBSTRING`, `CONCAT`, `CAST`, `TIMESTAMPTOSTRING`, `LEN`, `ABS`, `UCASE`, `LCASE`
Aggregate: `COUNT`, `SUM`, `MIN`, `MAX`, `AVG`, `COLLECT_LIST`, `COLLECT_SET`, `TOPK`, `TOPKDISTINCT`
Custom UDFs: implement in Java, deploy as JAR files.

## Gotchas

- **Pull queries only work on materialized tables** - not on raw streams; must create a persistent aggregate query first
- **Join requirements** - events must have same key type, collections must have same partition count and partitioning strategy
- **Each persistent query creates internal topics and state stores** - resource usage scales with query count
- **Headless mode for production** - `queries.file=/path/to/query.sql` disables REST API, prevents runtime modification
- **Grace period default is 24 hours** - can consume significant memory for windowed aggregations; tune based on actual late-data patterns

## See Also

- [[kafka-streams]] - underlying library ksqlDB is built on
- [[kafka-streams-windowing]] - window types and time semantics
- [[kafka-connect]] - connector integration from ksqlDB
- [[schema-registry]] - schema management for AVRO/PROTOBUF formats
- [ksqlDB Documentation](https://docs.ksqldb.io/)
