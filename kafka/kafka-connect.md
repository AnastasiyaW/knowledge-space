---
title: Kafka Connect
category: concepts
tags: [kafka, connect, source, sink, connector, SMT, distributed, standalone]
---

# Kafka Connect

Kafka Connect is the built-in integration framework for scalable, fault-tolerant data movement between Kafka and external systems. It provides a standardized runtime for **source connectors** (external system -> Kafka) and **sink connectors** (Kafka -> external system), handling offset management, serialization, parallelism, and error recovery without custom producer/consumer code.

## Source Connectors vs Sink Connectors

### Data Flow Direction

```
                Source Connectors                    Sink Connectors
  [Database] -----> [Kafka Topic]       [Kafka Topic] -----> [Elasticsearch]
  [Files]    -----> [Kafka Topic]       [Kafka Topic] -----> [S3]
  [REST API] -----> [Kafka Topic]       [Kafka Topic] -----> [JDBC Database]
```

| Aspect | Source Connector | Sink Connector |
|--------|-----------------|----------------|
| Direction | External system -> Kafka | Kafka -> External system |
| Base class | `SourceConnector` / `SourceTask` | `SinkConnector` / `SinkTask` |
| Core method | `poll()` returns `List<SourceRecord>` | `put(Collection<SinkRecord>)` |
| Offset storage | Connector-managed offsets in `connect-offsets` topic | Consumer group offsets (standard Kafka mechanism) |
| DLQ support | No | Yes |
| Parallelism unit | Input partitions (tables, files, shards) | Kafka topic partitions |

Source connectors define their own notion of "partitions" and "offsets" - e.g., for JDBC, each table is a partition and the timestamp/incrementing column value is the offset. Sink connectors consume from Kafka partitions directly and use standard consumer group offset tracking.

## Standalone vs Distributed Mode

### Standalone Mode

Single worker process. Config files passed on the command line. Offsets stored in a local file.

```bash
bin/connect-standalone.sh \
  config/connect-standalone.properties \
  config/my-source-connector.properties \
  config/my-sink-connector.properties
```

```properties
# connect-standalone.properties
bootstrap.servers=localhost:9092
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
offset.storage.file.filename=/tmp/connect.offsets
```

**When to use**: development, testing, single-machine pipelines, edge deployments where only one worker is needed.

### Distributed Mode

Multiple workers form a cluster via `group.id`. Connectors configured via REST API. Offsets, configs, and status stored in internal Kafka topics.

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

```properties
# connect-distributed.properties
bootstrap.servers=broker1:9092,broker2:9092,broker3:9092
group.id=connect-cluster

# Internal topics for distributed state
config.storage.topic=connect-configs
config.storage.replication.factor=3
offset.storage.topic=connect-offsets
offset.storage.replication.factor=3
offset.storage.partitions=25
status.storage.topic=connect-status
status.storage.replication.factor=3
status.storage.partitions=5

key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter

plugin.path=/opt/kafka/connect-plugins
rest.host.name=0.0.0.0
rest.port=8083
```

**When to use**: production. Provides fault tolerance (task rebalancing on worker failure), scalability (add workers), and centralized management (REST API).

### Key Differences

| Aspect | Standalone | Distributed |
|--------|-----------|-------------|
| Workers | 1 | N (cluster) |
| Configuration | Properties files on CLI | REST API |
| Offset storage | Local file | Kafka topic (`connect-offsets`) |
| Config storage | N/A | Kafka topic (`connect-configs`) |
| Fault tolerance | None | Automatic task rebalancing |
| Scaling | Vertical only | Horizontal (add workers) |
| REST API | Available but single-node | Full cluster management |

## Connector Configuration

### Essential Config Properties

```json
{
  "name": "my-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "tasks.max": "4",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "transforms": "route,mask",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "(.*)",
    "transforms.route.replacement": "prod-$1",
    "transforms.mask.type": "org.apache.kafka.connect.transforms.MaskField$Value",
    "transforms.mask.fields": "ssn,credit_card"
  }
}
```

| Property | Description |
|----------|-------------|
| `connector.class` | Fully qualified class name or alias of the connector |
| `tasks.max` | Maximum number of tasks the connector can create. Actual count may be lower (e.g., fewer tables than `tasks.max`) |
| `key.converter` | Converter for record keys. Overrides worker-level default |
| `value.converter` | Converter for record values. Overrides worker-level default |
| `transforms` | Comma-separated list of SMT aliases applied in order |
| `header.converter` | Converter for record headers (default: `SimpleHeaderConverter`) |
| `errors.tolerance` | `none` (default, fail on error) or `all` (skip bad records) |
| `errors.retry.timeout` | Max time in ms to retry a failed operation (default: 0, no retry) |
| `errors.retry.delay.max.ms` | Max backoff between retries (default: 60000) |

### Converter Configuration

Converters can be set at worker level (global default) or per-connector:

```properties
# Worker-level defaults
key.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter=io.confluent.connect.avro.AvroConverter
value.converter.schema.registry.url=http://schema-registry:8081
```

Common converters:
- `JsonConverter` - human-readable, no schema registry required. Set `schemas.enable=false` to omit inline schema.
- `AvroConverter` - compact binary, requires [[schema-registry]]
- `ProtobufConverter` - compact binary, requires Schema Registry
- `StringConverter` - raw string, no schema
- `ByteArrayConverter` - passthrough, no conversion

## Single Message Transforms (SMTs)

SMTs are lightweight, stateless, per-record transformations applied before a record reaches the converter (source) or after deserialization (sink). Chained in order via the `transforms` property.

### Built-in SMTs

#### InsertField

Add static or metadata fields to records.

```properties
transforms=addTopic
transforms.addTopic.type=org.apache.kafka.connect.transforms.InsertField$Value
transforms.addTopic.topic.field=kafka_topic
transforms.addTopic.partition.field=kafka_partition
transforms.addTopic.offset.field=kafka_offset
transforms.addTopic.timestamp.field=kafka_ts
transforms.addTopic.static.field=environment
transforms.addTopic.static.value=production
```

Available metadata fields: `topic.field`, `partition.field`, `offset.field`, `timestamp.field`. Static fields via `static.field`/`static.value`.

#### ReplaceField

Include, exclude, or rename fields.

```properties
# Drop fields
transforms=dropSensitive
transforms.dropSensitive.type=org.apache.kafka.connect.transforms.ReplaceField$Value
transforms.dropSensitive.exclude=internal_id,debug_info

# Rename fields
transforms=rename
transforms.rename.type=org.apache.kafka.connect.transforms.ReplaceField$Value
transforms.rename.renames=old_name:new_name,ts:timestamp
```

#### MaskField

Replace field values with type-appropriate zero/null values (0 for numerics, empty string for strings, false for booleans).

```properties
transforms=maskPII
transforms.maskPII.type=org.apache.kafka.connect.transforms.MaskField$Value
transforms.maskPII.fields=ssn,credit_card,phone
transforms.maskPII.replacement=REDACTED
```

#### TimestampRouter

Route records to different topics based on the record timestamp. Commonly used for time-partitioned sinks (e.g., daily S3 prefixes).

```properties
transforms=timeRoute
transforms.timeRoute.type=org.apache.kafka.connect.transforms.TimestampRouter
transforms.timeRoute.topic.format=${topic}-${timestamp}
transforms.timeRoute.timestamp.format=yyyyMMdd
# Input topic "events" -> output topic "events-20260330"
```

#### RegexRouter

Rewrite the destination topic name using regex.

```properties
transforms=route
transforms.route.type=org.apache.kafka.connect.transforms.RegexRouter
transforms.route.regex=^raw-(.*)$
transforms.route.replacement=processed-$1
# "raw-orders" -> "processed-orders"
```

#### Cast

Change field types. Accepts a comma-separated list of `field:type` pairs.

```properties
transforms=cast
transforms.cast.type=org.apache.kafka.connect.transforms.Cast$Value
transforms.cast.spec=price:float64,quantity:int32,active:boolean
```

Supported types: `boolean`, `int8`, `int16`, `int32`, `int64`, `float32`, `float64`, `string`.

#### HeaderFrom

Move or copy fields from the record value/key into headers.

```properties
transforms=toHeader
transforms.toHeader.type=org.apache.kafka.connect.transforms.HeaderFrom$Value
transforms.toHeader.fields=correlation_id,trace_id
transforms.toHeader.headers=X-Correlation-Id,X-Trace-Id
transforms.toHeader.operation=copy
# operation: "copy" (keep in value) or "move" (remove from value)
```

#### Filter

Drop records based on a predicate. Requires a `Predicate` configuration.

```properties
# Drop tombstone records (null values)
predicates=isTombstone
predicates.isTombstone.type=org.apache.kafka.connect.transforms.predicates.RecordIsTombstone

transforms=dropTombstones
transforms.dropTombstones.type=org.apache.kafka.connect.transforms.Filter
transforms.dropTombstones.predicate=isTombstone

# Drop records from specific topic
predicates=isAudit
predicates.isAudit.type=org.apache.kafka.connect.transforms.predicates.TopicNameMatches
predicates.isAudit.pattern=audit-.*

transforms=dropAudit
transforms.dropAudit.type=org.apache.kafka.connect.transforms.Filter
transforms.dropAudit.predicate=isAudit

# Negate: keep only records matching predicate
transforms.keepOnlyAudit.type=org.apache.kafka.connect.transforms.Filter
transforms.keepOnlyAudit.predicate=isAudit
transforms.keepOnlyAudit.negate=true
```

Built-in predicates:
- `RecordIsTombstone` - true when value is null
- `TopicNameMatches` - regex match on topic name
- `HasHeaderKey` - true when a specific header exists

### SMT Key vs Value

Every SMT has `$Key` and `$Value` variants:

```properties
# Apply to value (most common)
transforms.mask.type=org.apache.kafka.connect.transforms.MaskField$Value

# Apply to key
transforms.mask.type=org.apache.kafka.connect.transforms.MaskField$Key
```

### SMT Chaining

SMTs execute in the order listed. Order matters when transforms depend on fields added/removed by earlier transforms.

```properties
transforms=insertEnv,maskPII,routeByTime
# 1. InsertField adds "environment" field
# 2. MaskField masks SSN
# 3. TimestampRouter rewrites topic name
```

## Common Connectors

### JDBC Source Connector

Polls a relational database and writes rows to Kafka topics.

```json
{
  "name": "jdbc-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://db:5432/mydb",
    "connection.user": "app",
    "connection.password": "${file:/secrets/db.properties:password}",
    "table.whitelist": "orders,customers",
    "mode": "timestamp+incrementing",
    "timestamp.column.name": "updated_at",
    "incrementing.column.name": "id",
    "topic.prefix": "db.",
    "poll.interval.ms": "5000",
    "tasks.max": "4"
  }
}
```

Modes: `bulk` (full table each poll), `incrementing` (new rows only), `timestamp` (updated rows), `timestamp+incrementing` (both - recommended).

### JDBC Sink Connector

Writes records from Kafka topics into a relational database.

```json
{
  "name": "jdbc-sink",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url": "jdbc:postgresql://db:5432/mydb",
    "connection.user": "app",
    "connection.password": "${file:/secrets/db.properties:password}",
    "topics": "db.orders",
    "insert.mode": "upsert",
    "pk.mode": "record_value",
    "pk.fields": "id",
    "auto.create": "true",
    "auto.evolve": "true",
    "tasks.max": "2"
  }
}
```

Insert modes: `insert`, `upsert`, `update`.

### FileStream (Source/Sink)

Bundled with Kafka. Reads lines from a file (source) or writes records to a file (sink). Intended for development and testing only.

```json
{
  "name": "file-source",
  "config": {
    "connector.class": "FileStreamSource",
    "tasks.max": "1",
    "file": "/tmp/input.txt",
    "topic": "file-data"
  }
}
```

### Debezium (CDC)

Change Data Capture from database transaction logs. Captures inserts, updates, deletes in real-time without polling.

```json
{
  "name": "pg-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "db",
    "database.port": "5432",
    "database.user": "replicator",
    "database.password": "${file:/secrets/db.properties:password}",
    "database.dbname": "inventory",
    "database.server.name": "dbserver1",
    "schema.include.list": "public",
    "table.include.list": "public.orders,public.customers",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "dbz_publication",
    "topic.prefix": "cdc",
    "snapshot.mode": "initial",
    "tombstones.on.delete": "true",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false"
  }
}
```

Debezium supports: PostgreSQL, MySQL, MongoDB, SQL Server, Oracle, Cassandra, Db2, Vitess.

`snapshot.mode` options: `initial` (snapshot then stream), `never` (stream only), `when_needed`, `schema_only`.

### S3 Sink Connector

Writes Kafka records to S3 as files (JSON, Avro, Parquet).

```json
{
  "name": "s3-sink",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "s3.bucket.name": "data-lake",
    "s3.region": "us-east-1",
    "topics": "events",
    "flush.size": "10000",
    "rotate.interval.ms": "3600000",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "partition.duration.ms": "3600000",
    "path.format": "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH",
    "locale": "en-US",
    "timezone": "UTC",
    "tasks.max": "4"
  }
}
```

Format classes: `JsonFormat`, `AvroFormat`, `ParquetFormat`, `ByteArrayFormat`.

### Elasticsearch Sink Connector

Indexes Kafka records into Elasticsearch.

```json
{
  "name": "es-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "connection.url": "http://elasticsearch:9200",
    "topics": "events",
    "type.name": "_doc",
    "key.ignore": "false",
    "schema.ignore": "true",
    "behavior.on.null.values": "delete",
    "write.method": "upsert",
    "batch.size": "2000",
    "max.buffered.records": "20000",
    "linger.ms": "1000",
    "flush.timeout.ms": "180000",
    "max.retries": "5",
    "retry.backoff.ms": "100",
    "tasks.max": "4"
  }
}
```

`behavior.on.null.values`: `ignore`, `delete` (tombstone -> ES delete), `fail`.

## REST API

All operations in distributed mode go through the Connect REST API (default port 8083).

### Full Endpoint Reference

```bash
# --- Cluster info ---
curl http://localhost:8083/
# Returns: {"version":"3.6.0","commit":"...","kafka_cluster_id":"..."}

# --- Connector plugins ---
curl http://localhost:8083/connector-plugins | jq '.[].class'

# --- Create connector ---
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-connector",
    "config": {
      "connector.class": "FileStreamSource",
      "tasks.max": "1",
      "file": "/tmp/input.txt",
      "topic": "data"
    }
  }'

# --- List active connectors ---
curl http://localhost:8083/connectors
# With status info:
curl "http://localhost:8083/connectors?expand=status&expand=info"

# --- Get connector config ---
curl http://localhost:8083/connectors/my-connector/config

# --- Update connector config (full replace) ---
curl -X PUT http://localhost:8083/connectors/my-connector/config \
  -H "Content-Type: application/json" \
  -d '{
    "connector.class": "FileStreamSource",
    "tasks.max": "2",
    "file": "/tmp/new-input.txt",
    "topic": "data"
  }'

# --- PATCH connector config (partial update, Kafka 3.7+) ---
curl -X PATCH http://localhost:8083/connectors/my-connector/config \
  -H "Content-Type: application/json" \
  -d '{"tasks.max": "4"}'

# --- Get connector status ---
curl http://localhost:8083/connectors/my-connector/status | jq
# Returns:
# {
#   "name": "my-connector",
#   "connector": {"state": "RUNNING", "worker_id": "worker1:8083"},
#   "tasks": [
#     {"id": 0, "state": "RUNNING", "worker_id": "worker1:8083"},
#     {"id": 1, "state": "FAILED", "worker_id": "worker2:8083", "trace": "..."}
#   ]
# }

# --- Restart connector ---
curl -X POST http://localhost:8083/connectors/my-connector/restart
# With options (Kafka 3.1+):
curl -X POST "http://localhost:8083/connectors/my-connector/restart?includeTasks=true&onlyFailed=true"

# --- Restart specific task ---
curl -X POST http://localhost:8083/connectors/my-connector/tasks/0/restart

# --- Pause connector ---
curl -X PUT http://localhost:8083/connectors/my-connector/pause

# --- Resume connector ---
curl -X PUT http://localhost:8083/connectors/my-connector/resume

# --- Delete connector ---
curl -X DELETE http://localhost:8083/connectors/my-connector

# --- Validate connector config ---
curl -X PUT http://localhost:8083/connector-plugins/FileStreamSource/config/validate \
  -H "Content-Type: application/json" \
  -d '{"connector.class": "FileStreamSource", "tasks.max": "1", "file": "/tmp/input.txt", "topic": "data"}'
```

### Summary Table

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Cluster info, version |
| `GET` | `/connector-plugins` | List installed plugins |
| `POST` | `/connectors` | Create connector |
| `GET` | `/connectors` | List connectors (supports `?expand=status&expand=info`) |
| `GET` | `/connectors/{name}` | Get connector info |
| `GET` | `/connectors/{name}/config` | Get connector config |
| `PUT` | `/connectors/{name}/config` | Update config (full replace) |
| `PATCH` | `/connectors/{name}/config` | Partial config update (3.7+) |
| `GET` | `/connectors/{name}/status` | Get connector and task status |
| `POST` | `/connectors/{name}/restart` | Restart connector |
| `PUT` | `/connectors/{name}/pause` | Pause connector |
| `PUT` | `/connectors/{name}/resume` | Resume connector |
| `DELETE` | `/connectors/{name}` | Delete connector |
| `GET` | `/connectors/{name}/tasks` | List tasks |
| `GET` | `/connectors/{name}/tasks/{id}/status` | Get task status |
| `POST` | `/connectors/{name}/tasks/{id}/restart` | Restart specific task |
| `PUT` | `/connector-plugins/{class}/config/validate` | Validate config |

## Offset Management

### Source Connector Offsets

Source connectors track their own offsets (not Kafka consumer offsets). Offsets are stored in the `connect-offsets` topic (distributed mode) or a local file (standalone mode).

Each source connector defines a partition/offset structure specific to its data source:

```
JDBC Source:  partition = {"table": "orders"}
              offset = {"timestamp": 1711800000000, "incrementing": 42}

Debezium:     partition = {"server": "dbserver1"}
              offset = {"lsn": 123456789, "txId": 500}

FileStream:   partition = {"filename": "/tmp/input.txt"}
              offset = {"position": 4096}
```

### Resetting Source Connector Offsets

```bash
# Delete connector first
curl -X DELETE http://localhost:8083/connectors/my-connector

# Reset offsets via API (Kafka 3.6+)
curl -X DELETE http://localhost:8083/connectors/my-connector/offsets

# Or alter offsets (Kafka 3.6+)
curl -X PATCH http://localhost:8083/connectors/my-connector/offsets \
  -H "Content-Type: application/json" \
  -d '{
    "offsets": [
      {
        "partition": {"table": "orders"},
        "offset": {"timestamp": 0, "incrementing": 0}
      }
    ]
  }'

# Manual method: produce a tombstone to connect-offsets topic for the connector's key
# (use kafka-console-producer with null value for the connector's offset key)
```

### Sink Connector Offsets

Sink connectors use standard Kafka consumer group offsets. The consumer group ID follows the pattern `connect-{connector-name}`.

```bash
# Check sink connector offsets
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group connect-my-sink-connector --describe

# Reset sink connector offsets
# 1. Delete the connector
# 2. Reset the consumer group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group connect-my-sink-connector \
  --topic my-topic \
  --reset-offsets --to-earliest --execute
# 3. Recreate the connector
```

## Error Handling

### Error Tolerance and DLQ

Applicable to **sink connectors only**.

```properties
# Fail on first error (default)
errors.tolerance=none

# Skip bad records, continue processing
errors.tolerance=all

# Dead Letter Queue - capture failed records
errors.deadletterqueue.topic.name=my-connector-dlq
errors.deadletterqueue.topic.replication.factor=3

# Include error context in DLQ record headers
errors.deadletterqueue.context.headers.enable=true
# Headers added: __connect.errors.topic, __connect.errors.partition,
# __connect.errors.offset, __connect.errors.connector.name,
# __connect.errors.task.id, __connect.errors.stage,
# __connect.errors.class.name, __connect.errors.exception.class.name,
# __connect.errors.exception.message, __connect.errors.exception.stacktrace

# Retry configuration
errors.retry.timeout=300000       # retry for up to 5 minutes
errors.retry.delay.max.ms=60000   # max 60s between retries (exponential backoff)

# Log errors
errors.log.enable=true
errors.log.include.messages=true  # include record content in log (PII risk!)
```

### DLQ Pattern

```
[Kafka Topic] --> [Sink Connector]
                      |
                   success --> [External System]
                      |
                   failure --> [DLQ Topic] --> [DLQ Consumer / Alert / Retry Pipeline]
```

The DLQ topic receives the original Kafka record as-is (same key, value, timestamp). Error details are in the headers when `errors.deadletterqueue.context.headers.enable=true`.

Common DLQ processing patterns:
1. **Alert and manual fix**: monitor DLQ topic size, investigate failures
2. **Automated retry**: separate consumer reads DLQ, attempts reprocessing after fix
3. **Redirect**: route DLQ records to a different sink after transformation

### Source Connector Errors

Source connectors do not support `errors.tolerance` or DLQ. Error handling strategies:
- Connector retries internally based on its implementation
- On persistent failure, the task transitions to `FAILED` state
- Monitor via REST API and restart manually or automatically

## Monitoring

### JMX Metrics

```
# --- Connector-level metrics ---
kafka.connect:type=connector-metrics,connector="{connector}"
  connector-type                     # "source" or "sink"
  connector-class                    # fully qualified class
  connector-version                  # connector version
  status                             # RUNNING, PAUSED, FAILED, UNASSIGNED

# --- Task-level metrics ---
kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"
  status                             # RUNNING, PAUSED, FAILED, UNASSIGNED
  running-ratio                      # fraction of time task spent running (0.0-1.0)
  pause-ratio                        # fraction of time task spent paused
  batch-size-avg                     # average batch size
  batch-size-max                     # max batch size
  offset-commit-avg-time-ms          # avg offset commit latency
  offset-commit-max-time-ms          # max offset commit latency
  offset-commit-success-percentage   # % successful commits
  offset-commit-failure-percentage   # % failed commits

# --- Source task metrics ---
kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"
  source-record-poll-rate            # records/sec polled from source
  source-record-poll-total           # total records polled
  source-record-write-rate           # records/sec written to Kafka
  source-record-write-total          # total records written
  source-record-active-count         # records polled but not yet committed
  source-record-active-count-max     # max active count
  poll-batch-avg-time-ms             # avg time per poll() call
  poll-batch-max-time-ms             # max time per poll() call

# --- Sink task metrics ---
kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"
  sink-record-read-rate              # records/sec read from Kafka
  sink-record-read-total             # total records read
  sink-record-send-rate              # records/sec sent to external system
  sink-record-send-total             # total records sent
  sink-record-active-count           # records read but not yet committed
  sink-record-active-count-max       # max active count
  put-batch-avg-time-ms              # avg time per put() call
  put-batch-max-time-ms              # max time per put() call
  offset-commit-seq-no               # current offset commit sequence number
  offset-commit-completion-rate      # offset commits/sec
  partition-count                    # number of partitions assigned
  dead-letter-queue-produce-requests # total DLQ records produced

# --- Worker-level metrics ---
kafka.connect:type=connect-worker-metrics
  connector-count                    # number of connectors on this worker
  connector-startup-attempts-total   # total startup attempts
  connector-startup-success-total    # successful startups
  connector-startup-failure-total    # failed startups
  task-count                         # number of tasks on this worker
  task-startup-attempts-total
  task-startup-success-total
  task-startup-failure-total

# --- Worker rebalance metrics ---
kafka.connect:type=connect-worker-rebalance-metrics
  leader-name                        # current leader worker
  epoch                              # rebalance epoch
  rebalancing                        # true if currently rebalancing
  rebalance-avg-time-ms
  rebalance-max-time-ms
  time-since-last-rebalance-ms
```

### Connector States

| State | Meaning | Action |
|-------|---------|--------|
| `RUNNING` | Operating normally | None |
| `PAUSED` | Manually paused via REST API | Resume when ready: `PUT /connectors/{name}/resume` |
| `FAILED` | Unrecoverable error | Check `trace` in status, fix config/data, restart |
| `UNASSIGNED` | Task not yet assigned to a worker | Wait for rebalance; if persistent, check worker health |
| `RESTARTING` | Restart in progress (transient, Kafka 3.1+) | Wait |
| `STOPPED` | Connector stopped (Kafka 3.5+) | Resume or delete |

### Health Check Script

```bash
#!/bin/bash
CONNECT_URL="http://localhost:8083"

for connector in $(curl -s "$CONNECT_URL/connectors" | jq -r '.[]'); do
  status=$(curl -s "$CONNECT_URL/connectors/$connector/status")
  conn_state=$(echo "$status" | jq -r '.connector.state')
  failed_tasks=$(echo "$status" | jq '[.tasks[] | select(.state=="FAILED")] | length')

  if [ "$conn_state" != "RUNNING" ]; then
    echo "ALERT: Connector $connector is $conn_state"
  fi

  if [ "$failed_tasks" -gt 0 ]; then
    echo "ALERT: Connector $connector has $failed_tasks failed task(s)"
    # Auto-restart failed tasks
    echo "$status" | jq -r '.tasks[] | select(.state=="FAILED") | .id' | while read task_id; do
      curl -s -X POST "$CONNECT_URL/connectors/$connector/tasks/$task_id/restart"
      echo "Restarted task $task_id of $connector"
    done
  fi
done
```

## Gotchas

- **Failed tasks do NOT auto-restart.** Unlike worker failures that trigger rebalancing, individual task failures require manual restart via `POST /connectors/{name}/tasks/{id}/restart`. The `restart` endpoint with `?includeTasks=true&onlyFailed=true` (Kafka 3.1+) simplifies this.

- **DLQ only works for sink connectors.** Source connector errors must be handled by the connector's own retry logic or by restarting the task.

- **`errors.tolerance=all` silently drops records without a DLQ.** Always pair with `errors.deadletterqueue.topic.name`. Monitor the DLQ topic size.

- **Converter mismatch is the #1 error source.** If producers write Avro but the connector expects JSON, deserialization fails. Ensure `key.converter` and `value.converter` match the actual data format in the [[topics-and-partitions|topic]].

- **Plugin path isolation.** Each connector plugin must be in its own subdirectory under `plugin.path`. Mixing JARs causes classpath conflicts.

- **`tasks.max` is a ceiling, not a guarantee.** A JDBC connector with 3 tables will create at most 3 tasks regardless of `tasks.max=10`.

- **Debezium reads WAL, not queries.** Schema changes in the source DB can break the connector. Monitor Debezium's `schema.history` topic.

- **Standalone mode loses offsets on crash.** The local offset file is flushed periodically, not on every commit. Use distributed mode for production.

- **Rebalancing storms.** Adding/removing connectors or workers triggers a full rebalance of all tasks across all workers. In large clusters, use incremental cooperative rebalancing (`connect.protocol=compatible` or `connect.protocol=sessioned`).

- **Secret management.** Never put passwords in plain text connector configs. Use the `ConfigProvider` interface: `${file:/path/to/secrets.properties:password}` or external providers (Vault, AWS Secrets Manager).

## See Also

- [[schema-registry]] - schema management for connector data formats, Avro/Protobuf/JSON Schema converters
- [[broker-architecture]] - broker internals, the cluster that Connect relies on
- [[topics-and-partitions]] - topic configuration, partitioning strategies that affect connector parallelism
