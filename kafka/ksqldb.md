---
title: ksqlDB
category: concepts
tags: [kafka, ksqldb, sql, streaming, materialized-views, pull-queries, push-queries]
---

# ksqlDB

SQL engine for stream processing on Apache Kafka. Built on top of [[kafka-streams]] internally - every ksqlDB query compiles down to a Kafka Streams topology. Provides a SQL interface for creating streams, tables, persistent queries, windowed aggregations, joins, and connectors without writing Java code. Exposes a REST API, a CLI client, and client libraries (Java, Python, Go, .NET).

## Architecture

```
                    +-----------------+
                    |   ksqlDB CLI    |
                    +--------+--------+
                             |
  +------------+    +--------v--------+    +------------------+
  | REST API   +--->|  ksqlDB Server  +--->| Kafka Cluster    |
  | (HTTP/2)   |    |  (JVM process)  |    | (source/sink)    |
  +------------+    +--------+--------+    +------------------+
                             |
                    +--------v--------+
                    | Kafka Streams   |
                    | (internal)      |
                    | State: RocksDB  |
                    +-----------------+
```

**ksqlDB Server**: JVM process that parses SQL, builds Kafka Streams topologies, manages persistent queries. Multiple servers form a cluster sharing the same `ksql.service.id` - they coordinate via Kafka's consumer group protocol.

**CLI** (`ksql`): Interactive shell connecting to the server's REST endpoint. Sends SQL statements, receives results.

**REST API**: Primary programmatic interface. Default port 8088. Supports `/ksql` (statements), `/query` (push queries via HTTP/1.1 streaming or HTTP/2), `/query-stream` (HTTP/2 streaming).

**State stores**: Persistent queries maintain local state in RocksDB (same as Kafka Streams). Backed by changelog topics for fault tolerance.

## STREAM vs TABLE

Core abstractions mirroring [[kafka-streams]] KStream and KTable.

### STREAM - Unbounded Event Sequence

Each record is an independent, immutable event. INSERT semantics. Append-only.

```sql
-- Create a stream backed by an existing topic
CREATE STREAM orders (
  order_id VARCHAR KEY,
  customer_id VARCHAR,
  product VARCHAR,
  amount DOUBLE,
  region VARCHAR,
  order_ts TIMESTAMP
) WITH (
  KAFKA_TOPIC = 'orders',
  VALUE_FORMAT = 'JSON',
  TIMESTAMP = 'order_ts'
);

-- Create a stream with a new topic (auto-created)
CREATE STREAM pageviews (
  user_id VARCHAR KEY,
  page VARCHAR,
  view_time BIGINT
) WITH (
  KAFKA_TOPIC = 'pageviews',
  VALUE_FORMAT = 'AVRO',
  PARTITIONS = 6,
  REPLICAS = 3
);
```

### TABLE - Materialized Current State

Each record is an upsert keyed by the primary key. Latest value per key wins. DELETE via tombstone (null value).

```sql
-- Create a table backed by an existing compacted topic
CREATE TABLE customers (
  customer_id VARCHAR PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  tier VARCHAR
) WITH (
  KAFKA_TOPIC = 'customers',
  VALUE_FORMAT = 'JSON'
);

-- Create a table from a query (materialized view)
CREATE TABLE order_counts AS
  SELECT customer_id, COUNT(*) AS total_orders
  FROM orders
  GROUP BY customer_id
  EMIT CHANGES;
```

### CREATE SOURCE Variants

```sql
-- SOURCE STREAM: read-only, cannot be target of INSERT INTO
CREATE SOURCE STREAM events (...)
  WITH (KAFKA_TOPIC='events', VALUE_FORMAT='AVRO');

-- SOURCE TABLE: read-only, enables pull queries without persistent query
CREATE SOURCE TABLE products (...)
  WITH (KAFKA_TOPIC='products', VALUE_FORMAT='JSON');
```

`SOURCE` keyword marks the object as read-only and backed directly by an external topic. Source tables automatically support pull queries.

### INSERT INTO

```sql
-- Insert individual records
INSERT INTO orders (order_id, customer_id, product, amount, region, order_ts)
VALUES ('ORD-999', 'CUST-42', 'Widget', 29.99, 'US', '2026-03-30T10:00:00');

-- Insert from another stream (creates a persistent query)
INSERT INTO enriched_orders
  SELECT o.order_id, o.product, c.name AS customer_name
  FROM orders o
  LEFT JOIN customers c ON o.customer_id = c.customer_id
  EMIT CHANGES;
```

### Key Differences

| Aspect | STREAM | TABLE |
|--------|--------|-------|
| Semantics | INSERT (all events) | UPSERT (latest per key) |
| Source topic | Any | Should be compacted |
| Supports INSERT INTO | Yes | Via persistent query only |
| Pull queries | No (unless materialized) | Yes |
| Push queries | Yes | Yes |

## Push Queries vs Pull Queries

### Push Queries (EMIT CHANGES)

Long-running, server-sent subscription. Client receives a continuous stream of new results as input data arrives. Backed by a persistent query (Kafka Streams topology).

```sql
-- Subscribe to all new orders in real-time
SELECT * FROM orders EMIT CHANGES;

-- Filtered push query
SELECT order_id, amount
FROM orders
WHERE region = 'EU' AND amount > 100.0
EMIT CHANGES;

-- Aggregation push query
SELECT region, COUNT(*) AS cnt, SUM(amount) AS total
FROM orders
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY region
EMIT CHANGES;
```

Push queries stream results indefinitely until the client disconnects. Useful for real-time dashboards, event-driven applications, CDC pipelines.

### Pull Queries (Point-in-Time Lookup)

Request-response. Returns the current materialized state and terminates. Analogous to a traditional SQL SELECT.

```sql
-- Lookup current state of a specific key
SELECT * FROM order_counts WHERE customer_id = 'CUST-42';

-- Range scan (ksqlDB 0.27+)
SELECT * FROM order_counts WHERE total_orders > 100;

-- Table scan (ksqlDB 0.27+, full scan of materialized state)
SELECT * FROM order_counts;
```

Pull queries only work against materialized views (tables created from aggregations) or SOURCE tables. They query the local RocksDB state store. For distributed pull queries across multiple ksqlDB servers, enable `ksql.query.pull.enable.standby.reads=true`.

### Comparison

| Aspect | Push Query | Pull Query |
|--------|-----------|------------|
| Keyword | `EMIT CHANGES` | No `EMIT` clause |
| Duration | Continuous (until disconnect) | Immediate response |
| Data freshness | Real-time | Point-in-time snapshot |
| Source | STREAM or TABLE | Materialized TABLE only |
| Scalability | One topology per query | Stateless lookup |
| HTTP protocol | Streaming (chunked/HTTP2) | Standard request-response |

## Persistent Queries vs Transient Queries

### Persistent Queries

Created by `CREATE STREAM AS SELECT` (CSAS), `CREATE TABLE AS SELECT` (CTAS), or `INSERT INTO ... SELECT`. Persist across server restarts. Each persistent query runs a Kafka Streams topology.

```sql
-- CSAS: creates a new stream + persistent query writing to it
CREATE STREAM high_value_orders AS
  SELECT * FROM orders WHERE amount > 500.0
  EMIT CHANGES;

-- CTAS: creates a materialized table + persistent query
CREATE TABLE customer_spend AS
  SELECT customer_id,
         SUM(amount) AS total_spend,
         COUNT(*) AS order_count
  FROM orders
  GROUP BY customer_id
  EMIT CHANGES;

-- List all persistent queries
SHOW QUERIES;

-- Describe a query
EXPLAIN CSAS_HIGH_VALUE_ORDERS_0;

-- Terminate a persistent query
TERMINATE CSAS_HIGH_VALUE_ORDERS_0;

-- Terminate all queries writing to a stream/table
DROP STREAM high_value_orders DELETE TOPIC;
DROP TABLE customer_spend DELETE TOPIC;
```

Persistent queries consume CPU, memory (RocksDB state), and network continuously. Each one is an independent Kafka Streams application. Monitor via JMX and `SHOW QUERIES EXTENDED`.

### Transient Queries

Ad-hoc `SELECT` statements (push or pull) that do not create new topics or persist across restarts. Used for debugging, exploration, and lightweight lookups.

```sql
-- Transient push query (streams results until Ctrl+C)
SELECT * FROM orders EMIT CHANGES LIMIT 10;

-- Transient pull query
SELECT * FROM customer_spend WHERE customer_id = 'CUST-42';
```

## Windowed Aggregations

Same window semantics as [[kafka-streams]]. Windowsed results have a composite key: `(original_key, window_start, window_end)`.

### TUMBLING Window

Fixed-size, non-overlapping.

```sql
CREATE TABLE orders_per_hour AS
  SELECT region,
         COUNT(*) AS order_count,
         SUM(amount) AS total_amount,
         WINDOWSTART AS window_start,
         WINDOWEND AS window_end
  FROM orders
  WINDOW TUMBLING (SIZE 1 HOUR)
  GROUP BY region
  EMIT CHANGES;
```

### HOPPING Window

Fixed-size, overlapping. Each record falls into multiple windows.

```sql
CREATE TABLE orders_hopping AS
  SELECT region,
         COUNT(*) AS order_count
  FROM orders
  WINDOW HOPPING (SIZE 10 MINUTES, ADVANCE BY 2 MINUTES)
  GROUP BY region
  EMIT CHANGES;
```

### SESSION Window

Dynamic, activity-based. Gap of inactivity closes the window.

```sql
CREATE TABLE user_sessions AS
  SELECT user_id,
         COUNT(*) AS event_count,
         WINDOWSTART AS session_start,
         WINDOWEND AS session_end
  FROM pageviews
  WINDOW SESSION (30 MINUTES)
  GROUP BY user_id
  EMIT CHANGES;
```

### GRACE Period

Controls how long a window accepts late-arriving records after the window's end time.

```sql
-- Tumbling with grace period
CREATE TABLE orders_tumbling_grace AS
  SELECT region, COUNT(*) AS cnt
  FROM orders
  WINDOW TUMBLING (SIZE 5 MINUTES, GRACE PERIOD 2 MINUTES)
  GROUP BY region
  EMIT CHANGES;

-- Session with grace period
CREATE TABLE sessions_grace AS
  SELECT user_id, COUNT(*) AS cnt
  FROM pageviews
  WINDOW SESSION (30 MINUTES, GRACE PERIOD 5 MINUTES)
  GROUP BY user_id
  EMIT CHANGES;
```

Records arriving after `window_end + grace_period` are dropped silently. Default grace period is 24 hours (changed in some versions). Always set explicitly.

### Querying Windowed Tables

```sql
-- Pull query: specific key + time range
SELECT * FROM orders_per_hour
WHERE region = 'US'
  AND WINDOWSTART >= '2026-03-30T00:00:00'
  AND WINDOWEND <= '2026-03-30T12:00:00';

-- Push query: continuous updates
SELECT region, order_count, window_start, window_end
FROM orders_per_hour
EMIT CHANGES;
```

`WINDOWSTART` and `WINDOWEND` are pseudo-columns available on windowed tables. Both are `BIGINT` (epoch ms) but can be compared to `TIMESTAMP` strings.

## Joins

All joins require matching keys. If keys differ, repartition with a CSAS first.

### Stream-Stream Join (Windowed, Required)

Both sides are event streams. WITHIN clause is mandatory (defines the join window).

```sql
-- Inner join: emit when both sides match within 1 hour
CREATE STREAM orders_with_payments AS
  SELECT o.order_id, o.amount, p.payment_method, p.status
  FROM orders o
  INNER JOIN payments p
    WITHIN 1 HOUR
    ON o.order_id = p.order_id
  EMIT CHANGES;

-- Left join with GRACE PERIOD
CREATE STREAM orders_left_payments AS
  SELECT o.order_id, o.amount,
         p.payment_method, p.status
  FROM orders o
  LEFT JOIN payments p
    WITHIN 1 HOUR GRACE PERIOD 10 MINUTES
    ON o.order_id = p.order_id
  EMIT CHANGES;

-- Full outer join
CREATE STREAM orders_full_payments AS
  SELECT o.order_id, p.payment_id,
         COALESCE(o.amount, 0.0) AS amount
  FROM orders o
  FULL OUTER JOIN payments p
    WITHIN 30 MINUTES
    ON o.order_id = p.order_id
  EMIT CHANGES;
```

### Stream-Table Join (Non-Windowed)

Enrich stream events with current table state. No WITHIN clause - table always represents current state.

```sql
-- Inner join: enrich orders with customer data
CREATE STREAM enriched_orders AS
  SELECT o.order_id, o.product, o.amount,
         c.name AS customer_name, c.tier
  FROM orders o
  INNER JOIN customers c
    ON o.customer_id = c.customer_id
  EMIT CHANGES;

-- Left join: emit even if customer not found
CREATE STREAM enriched_orders_left AS
  SELECT o.order_id, o.product, o.amount,
         c.name AS customer_name
  FROM orders o
  LEFT JOIN customers c
    ON o.customer_id = c.customer_id
  EMIT CHANGES;
```

Stream drives output: each new stream record triggers a lookup in the table. Table updates alone do not produce output. Requires co-partitioning (same partition count, same partitioning key).

### Table-Table Join

Both sides are tables. Result is a table. Updates from either side trigger re-evaluation.

```sql
CREATE TABLE customer_with_address AS
  SELECT c.customer_id, c.name, c.email,
         a.street, a.city, a.country
  FROM customers c
  INNER JOIN addresses a
    ON c.customer_id = a.customer_id
  EMIT CHANGES;
```

### Join Types Summary

| Join | WITHIN Required | Co-partitioned | Result |
|------|-----------------|----------------|--------|
| Stream-Stream | Yes | Yes | STREAM |
| Stream-Table | No | Yes | STREAM |
| Table-Table | No | Yes | TABLE |

### Repartitioning for Joins

If join keys differ from partition keys, create an intermediate repartitioned stream:

```sql
-- Original stream keyed by order_id, need to join on customer_id
CREATE STREAM orders_by_customer
  WITH (KAFKA_TOPIC='orders_by_customer', PARTITIONS=6)
  AS SELECT * FROM orders
  PARTITION BY customer_id
  EMIT CHANGES;

-- Now join on matching keys
CREATE STREAM enriched AS
  SELECT o.order_id, c.name
  FROM orders_by_customer o
  JOIN customers c ON o.customer_id = c.customer_id
  EMIT CHANGES;
```

## Connectors via ksqlDB

ksqlDB can manage Kafka Connect connectors directly through SQL, without using the Connect REST API. Requires a Kafka Connect cluster accessible to the ksqlDB server.

### Source Connector

```sql
CREATE SOURCE CONNECTOR jdbc_source WITH (
  'connector.class'          = 'io.confluent.connect.jdbc.JdbcSourceConnector',
  'connection.url'           = 'jdbc:postgresql://db:5432/mydb',
  'connection.user'          = 'app',
  'connection.password'      = '${file:/secrets/db.properties:password}',
  'table.whitelist'          = 'orders,customers',
  'mode'                     = 'timestamp+incrementing',
  'timestamp.column.name'    = 'updated_at',
  'incrementing.column.name' = 'id',
  'topic.prefix'             = 'db.',
  'poll.interval.ms'         = '5000',
  'tasks.max'                = '4'
);
```

### Sink Connector

```sql
CREATE SINK CONNECTOR es_sink WITH (
  'connector.class'    = 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
  'connection.url'     = 'http://elasticsearch:9200',
  'topics'             = 'enriched_orders',
  'type.name'          = '_doc',
  'key.ignore'         = 'false',
  'schema.ignore'      = 'true',
  'write.method'       = 'upsert',
  'batch.size'         = '2000',
  'tasks.max'          = '4'
);
```

### Connector Management

```sql
-- List connectors
SHOW CONNECTORS;

-- Describe a connector
DESCRIBE CONNECTOR jdbc_source;

-- Drop a connector
DROP CONNECTOR jdbc_source;
```

Under the hood, ksqlDB forwards these commands to the Connect REST API. The connector lifecycle is managed by Connect, not ksqlDB. If ksqlDB restarts, connectors continue running in Connect.

## Custom Functions: UDF, UDAF, UDTF

### UDF - User-Defined Function (Scalar)

One row in, one value out. Stateless.

```java
@UdfDescription(name = "MASK_EMAIL", description = "Masks an email address")
public class MaskEmailUdf {

    @Udf(description = "Replace local part with ***")
    public String maskEmail(
        @UdfParameter(value = "email") final String email
    ) {
        if (email == null) return null;
        int at = email.indexOf('@');
        if (at < 0) return "***";
        return "***" + email.substring(at);
    }
}
```

```sql
SELECT order_id, MASK_EMAIL(customer_email) AS masked_email
FROM orders EMIT CHANGES;
```

### UDAF - User-Defined Aggregate Function

Accumulates state across multiple rows. Used in GROUP BY.

```java
@UdafDescription(name = "STDDEV", description = "Standard deviation")
public class StdDevUdaf {

    @UdafFactory(description = "stddev for doubles")
    public static Udaf<Double, Struct, Double> createUdaf() {
        return new Udaf<>() {
            // Struct schema for intermediate state
            private static final Schema SCHEMA = SchemaBuilder.struct()
                .field("COUNT", Schema.INT64_SCHEMA)
                .field("SUM", Schema.FLOAT64_SCHEMA)
                .field("SUM_SQ", Schema.FLOAT64_SCHEMA)
                .build();

            @Override
            public Struct initialize() {
                return new Struct(SCHEMA)
                    .put("COUNT", 0L)
                    .put("SUM", 0.0)
                    .put("SUM_SQ", 0.0);
            }

            @Override
            public Struct aggregate(Double val, Struct agg) {
                if (val == null) return agg;
                return new Struct(SCHEMA)
                    .put("COUNT", agg.getInt64("COUNT") + 1)
                    .put("SUM", agg.getFloat64("SUM") + val)
                    .put("SUM_SQ", agg.getFloat64("SUM_SQ") + val * val);
            }

            @Override
            public Struct merge(Struct a, Struct b) {
                return new Struct(SCHEMA)
                    .put("COUNT", a.getInt64("COUNT") + b.getInt64("COUNT"))
                    .put("SUM", a.getFloat64("SUM") + b.getFloat64("SUM"))
                    .put("SUM_SQ", a.getFloat64("SUM_SQ") + b.getFloat64("SUM_SQ"));
            }

            @Override
            public Double map(Struct agg) {
                long n = agg.getInt64("COUNT");
                if (n < 2) return 0.0;
                double sum = agg.getFloat64("SUM");
                double sumSq = agg.getFloat64("SUM_SQ");
                return Math.sqrt((sumSq - sum * sum / n) / (n - 1));
            }
        };
    }
}
```

```sql
SELECT region, STDDEV(amount) AS amount_stddev
FROM orders
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY region
EMIT CHANGES;
```

### UDTF - User-Defined Table Function

One row in, zero or more rows out. Used with `LATERAL JOIN` or `CROSS APPLY` semantics (automatically via `SELECT` with the UDTF).

```java
@UdtfDescription(name = "SPLIT_TAGS", description = "Splits comma-separated tags")
public class SplitTagsUdtf {

    @Udtf(description = "Split string by delimiter")
    public List<String> splitTags(
        @UdfParameter(value = "tags") final String tags
    ) {
        if (tags == null) return Collections.emptyList();
        return Arrays.asList(tags.split(","));
    }
}
```

```sql
-- Explode comma-separated tags into individual rows
SELECT order_id, EXPLODE(SPLIT_TAGS(tags)) AS tag
FROM orders EMIT CHANGES;
```

### Deploying Custom Functions

1. Build a JAR with the annotated classes.
2. Place the JAR in the ksqlDB `ext/` directory (configured via `ksql.extension.dir`).
3. Restart ksqlDB server.
4. Verify: `SHOW FUNCTIONS;` and `DESCRIBE FUNCTION MASK_EMAIL;`.

## Deployment Modes

### Interactive Mode (Default)

Developers submit SQL via CLI or REST API. Queries can be added, modified, terminated at runtime.

```bash
ksql-server-start /etc/ksqldb/ksql-server.properties
```

```properties
# ksql-server.properties
bootstrap.servers=broker1:9092,broker2:9092
ksql.service.id=my-ksqldb-cluster
listeners=http://0.0.0.0:8088
ksql.schema.registry.url=http://schema-registry:8081
```

### Headless Mode (Production Deployments)

SQL statements loaded from a file at startup. No CLI/REST writes allowed (read-only REST API). Deterministic, reproducible deployments. Treat the SQL file as code - version control it.

```bash
ksql-server-start /etc/ksqldb/ksql-server.properties \
  --queries-file /etc/ksqldb/queries.sql
```

```sql
-- queries.sql
CREATE STREAM orders (...) WITH (...);
CREATE TABLE customer_spend AS
  SELECT customer_id, SUM(amount) AS total
  FROM orders GROUP BY customer_id EMIT CHANGES;
CREATE SINK CONNECTOR es_sink WITH (...);
```

Changes require updating the SQL file and restarting the server. Rolling restarts are safe - each server replays the SQL file and converges to the same topology.

### Comparison

| Aspect | Interactive | Headless |
|--------|------------|----------|
| Query submission | CLI, REST API, client libs | SQL file at startup |
| Runtime changes | Yes | No (restart required) |
| REST API writes | Yes | Blocked (403) |
| Use case | Development, exploration | Production, CI/CD |
| Reproducibility | Manual tracking | SQL file in version control |
| Safety | Risk of ad-hoc changes | Immutable after start |

## Key Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ksql.service.id` | Unique cluster ID. Used as prefix for internal topics and consumer groups. All servers with the same ID share workload. | `default_` |
| `ksql.streams.auto.offset.reset` | Where to start reading when no committed offset: `earliest` or `latest`. Applies to new persistent queries. | `latest` |
| `ksql.streams.num.stream.threads` | Kafka Streams threads per server. Scale up to partition count. | 4 |
| `ksql.streams.state.dir` | Directory for RocksDB state stores. | `/tmp/kafka-streams` |
| `ksql.schema.registry.url` | URL of [[schema-registry]]. Required for AVRO/PROTOBUF/JSON_SCHEMA formats. | none |
| `ksql.extension.dir` | Directory for UDF/UDAF/UDTF JARs. | `ext/` |
| `ksql.connect.url` | Kafka Connect REST URL for connector management. | none |
| `ksql.query.pull.enable.standby.reads` | Allow pull queries to read from standby replicas (HA). | `false` |
| `ksql.streams.processing.guarantee` | `at_least_once` or `exactly_once_v2`. Same as Kafka Streams. | `at_least_once` |
| `ksql.streams.commit.interval.ms` | Kafka Streams commit interval. | 2000 |
| `ksql.query.pull.max.allowed.offset.lag` | Max offset lag for pull queries on standbys. Queries fail if lag exceeds this. | `Long.MAX_VALUE` |
| `ksql.heartbeat.enable` | Enable heartbeat mechanism between ksqlDB servers. Required for lag-aware routing. | `false` |
| `ksql.lag.reporting.enable` | Report per-store lag to other servers. Enables smarter pull query routing. | `false` |
| `ksql.suppress.enabled` | Allow `EMIT FINAL` (suppression) in queries. | `false` |

### EMIT FINAL (Suppression)

When enabled via `ksql.suppress.enabled=true`, use `EMIT FINAL` instead of `EMIT CHANGES` to suppress intermediate results and emit only the final result when a window closes.

```sql
CREATE TABLE hourly_totals AS
  SELECT region, SUM(amount) AS total
  FROM orders
  WINDOW TUMBLING (SIZE 1 HOUR, GRACE PERIOD 10 MINUTES)
  GROUP BY region
  EMIT FINAL;
```

## REST API

### Endpoints

```bash
# --- Execute a SQL statement ---
curl -X POST http://localhost:8088/ksql \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{
    "ksql": "SHOW STREAMS;",
    "streamsProperties": {
      "ksql.streams.auto.offset.reset": "earliest"
    }
  }'

# --- Push query (streaming response) ---
curl -X POST http://localhost:8088/query \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"ksql": "SELECT * FROM orders EMIT CHANGES;"}' \
  --no-buffer

# --- Pull query ---
curl -X POST http://localhost:8088/query \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"ksql": "SELECT * FROM customer_spend WHERE customer_id = '\''CUST-42'\'';"}'

# --- HTTP/2 streaming endpoint (preferred for new clients) ---
curl -X POST http://localhost:8088/query-stream \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"sql": "SELECT * FROM orders EMIT CHANGES;", "properties": {}}'

# --- Server info ---
curl http://localhost:8088/info

# --- Server health ---
curl http://localhost:8088/healthcheck

# --- Cluster status ---
curl http://localhost:8088/clusterStatus

# --- Terminate a cluster (deletes all queries and internal topics) ---
curl -X POST http://localhost:8088/ksql/terminate \
  -H "Content-Type: application/vnd.ksql.v1+json" \
  -d '{"deleteTopicList": ["_confluent-ksql-my-ksqldb-cluster"]}'
```

### Java Client

```java
ClientOptions options = ClientOptions.create()
    .setHost("localhost")
    .setPort(8088);

Client client = Client.create(options);

// Pull query
List<Row> rows = client.executeQuery(
    "SELECT * FROM customer_spend WHERE customer_id = 'CUST-42';"
).get();

for (Row row : rows) {
    System.out.println(row.getString("customer_id") + ": " +
                       row.getDouble("total_spend"));
}

// Push query (streaming)
StreamedQueryResult result = client.streamQuery(
    "SELECT * FROM orders EMIT CHANGES;"
).get();

for (int i = 0; i < 100; i++) {
    Row row = result.poll();  // blocks until next row
    if (row != null) {
        System.out.println(row);
    }
}

// Execute DDL/DML
client.executeStatement(
    "CREATE STREAM filtered AS SELECT * FROM orders WHERE amount > 100 EMIT CHANGES;"
).get();

// Insert values
KsqlObject row = new KsqlObject()
    .put("order_id", "ORD-999")
    .put("customer_id", "CUST-42")
    .put("amount", 150.0);
client.insertInto("orders", row).get();

client.close();
```

## Monitoring

### JMX Metrics

ksqlDB exposes Kafka Streams metrics plus its own:

```
# Query-level metrics
io.confluent.ksql.metrics:type=ksql-engine-query-stats
  num-persistent-queries       # total persistent queries
  num-active-queries           # currently running queries
  num-idle-queries             # paused queries
  bytes-consumed-total         # total bytes read
  messages-consumed-per-sec    # input throughput
  messages-produced-per-sec    # output throughput
  error-rate                   # query errors/sec

# Per-query metrics
io.confluent.ksql.metrics:type=_confluent-ksql-{service_id}ksql-engine-query-stats,
    query-id="{query_id}"
  messages-consumed-per-sec
  messages-produced-per-sec
  total-messages-consumed
  total-messages-produced

# Pull query metrics
io.confluent.ksql.metrics:type=_confluent-ksql-{service_id}pull-query
  pull-query-requests-total
  pull-query-requests-rate
  pull-query-requests-error-total
  pull-query-requests-error-rate
  pull-query-requests-local
  pull-query-requests-remote
  latency-avg
  latency-max
```

### SQL-Based Monitoring

```sql
-- List all queries with their status
SHOW QUERIES EXTENDED;

-- Describe a specific query's topology
EXPLAIN <query_id>;

-- Show runtime stats per query
DESCRIBE EXTENDED enriched_orders;

-- List all streams and tables
SHOW STREAMS;
SHOW TABLES;

-- Show server properties
SHOW PROPERTIES;
```

## Gotchas

- **ksql.streams.auto.offset.reset defaults to `latest`.** New persistent queries skip all existing data in the topic. Set to `earliest` in the query's `SET` clause or server config to process historical data. This only affects new consumer groups - existing queries are unaffected.

- **Each persistent query is a full Kafka Streams app.** Creates internal topics (repartition, changelog), state stores, consumer groups. 50 persistent queries = 50 independent topologies competing for resources. Plan capacity accordingly.

- **Pull queries only work on materialized state.** You cannot pull-query a raw STREAM. Create a CTAS with GROUP BY to materialize it, or use a SOURCE TABLE. Attempting a pull query on a STREAM returns an error.

- **Co-partitioning is required for joins.** Both sides must have the same number of partitions and the same partitioning key. Use `PARTITION BY` in a CSAS to repartition before joining. Missing this produces wrong results silently.

- **WITHIN clause is mandatory for stream-stream joins.** Without it, the query fails. Too small a window misses valid matches; too large a window accumulates excessive state.

- **Headless mode blocks all writes.** REST API returns 403 for any DDL/DML. Useful for production safety but makes debugging harder. Use interactive mode for development.

- **Internal topic naming.** ksqlDB creates internal topics prefixed with `_confluent-ksql-{ksql.service.id}`. Deleting these topics breaks persistent queries. The topic naming includes the query ID, which is auto-generated.

- **Schema evolution.** Adding/removing fields in AVRO/PROTOBUF requires compatible [[schema-registry]] evolution. ksqlDB does not auto-migrate existing persistent queries to new schemas. You may need to terminate and recreate queries after schema changes.

- **EMIT FINAL requires ksql.suppress.enabled=true.** Without it, the query fails with a config error. Suppression holds all window results in memory until the window closes + grace period. Large windows with many keys can cause OOM.

- **Connector management via ksqlDB is a passthrough to Connect REST API.** ksqlDB does not store connector state. If ksqlDB restarts, the connector keeps running in Connect. `SHOW CONNECTORS` may show stale info if the Connect cluster has changed.

- **Time zones.** ksqlDB uses UTC internally. `WINDOWSTART`/`WINDOWEND` are epoch milliseconds. Timestamp strings in `WHERE` clauses are parsed as UTC unless explicitly formatted with timezone.

## See Also

- [[kafka-streams]] - underlying library; ksqlDB compiles SQL to Kafka Streams topologies
- [[schema-registry]] - required for AVRO, PROTOBUF, JSON_SCHEMA value formats
- [[topics-and-partitions]] - partitioning affects query parallelism, co-partitioning requirements, and state store locality
