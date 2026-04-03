---
title: Kafka Connect
category: concepts
tags: [kafka, connect, source, sink, connector, smt, debezium, distributed, worker, task]
---

# Kafka Connect

Kafka Connect is a framework for streaming data between Kafka and external systems (databases, search indexes, file systems, cloud storage) using pluggable connectors, with built-in fault tolerance, task distribution, and offset management.

## Key Facts

- Part of Apache Kafka - provides a runtime for connector plugins
- **Source connectors**: pull data from external systems into Kafka topics
- **Sink connectors**: push data from Kafka topics to external systems
- **Connector** = coordinator; determines task count, splits work, receives config from workers
- **Task** = actual data mover; runs in its own Java thread; connector splits one job into multiple tasks for parallelism
- **Worker** = container process for connectors and tasks; handles REST requests, config storage, task reassignment
- **Converter** = transforms between byte arrays and Connect's internal data format
- **SMT (Single Message Transform)** = lightweight per-message transformations
- **Dead Letter Queue** = topic for failed messages (sink connectors only)
- Distributed mode stores configs, offsets, and status in internal Kafka topics: `connect-configs`, `connect-offsets`, `connect-status`

## Patterns

### Running Kafka Connect

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

Key properties:
```properties
bootstrap.servers=broker1:9092,broker2:9092
group.id=connect-cluster
plugin.path=/opt/connectors
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
rest.host.name=0.0.0.0
rest.port=8083
```

### REST API

```bash
# List connector plugins
curl http://localhost:8083/connector-plugins | jq

# Create connector
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  --data-binary "@connector-config.json"

# List / Status / Delete
curl http://localhost:8083/connectors
curl http://localhost:8083/connectors/{name}/status
curl -X DELETE http://localhost:8083/connectors/{name}

# Pause / Resume / Restart
curl -X PUT http://localhost:8083/connectors/{name}/pause
curl -X PUT http://localhost:8083/connectors/{name}/resume
curl -X POST http://localhost:8083/connectors/{name}/restart
curl -X POST http://localhost:8083/connectors/{name}/tasks/{id}/restart
```

### JDBC Source Connector (PostgreSQL)

```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://localhost:5432/db",
    "table.whitelist": "clients,orders",
    "mode": "timestamp",
    "timestamp.column.name": "modified_date",
    "topic.prefix": "postgres."
  }
}
```

### Debezium CDC Source (PostgreSQL WAL)

```json
{
  "name": "postgres-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "mydb",
    "topic.prefix": "cdc",
    "plugin.name": "pgoutput"
  }
}
```

### Built-in SMTs

| SMT | Purpose |
|-----|---------|
| `Cast` | Change field types |
| `MaskField` | Mask sensitive data |
| `Filter` | Drop/keep messages by condition |
| `Flatten` | Flatten nested structures |
| `InsertField` | Add fields (e.g., timestamp, topic name) |
| `InsertHeader` | Add message headers |
| `ReplaceField` | Rename or remove fields |
| `TimestampConverter` | Convert timestamp formats |
| `TimestampRouter` | Route to topic based on timestamp |
| `RegexRouter` | Route to topic based on regex match |
| `ExtractField` | Extract single field from complex message |

### Dead Letter Queue Configuration

```json
{
  "errors.tolerance": "all",
  "errors.deadletterqueue.topic.name": "dlq-connector-errors",
  "errors.deadletterqueue.topic.replication.factor": 3,
  "errors.deadletterqueue.context.headers.enable": true
}
```

- `errors.tolerance=none` (default): error causes immediate task failure
- `errors.tolerance=all`: errors silently ignored unless DLQ configured

### Custom Connector Development

```java
// Source Connector
public class MySourceConnector extends SourceConnector {
    public Class<? extends Task> taskClass() { return MySourceTask.class; }
    public List<Map<String, String>> taskConfigs(int maxTasks) { /* split work */ }
    public void start(Map<String, String> props) { }
    public void stop() { }
}

public class MySourceTask extends SourceTask {
    public List<SourceRecord> poll() { /* read from source, return records */ }
}

// Sink Connector
public class MySinkTask extends SinkTask {
    public void put(Collection<SinkRecord> records) { /* write to target */ }
}
```

### Standalone vs Distributed

| Mode | Use Case | Fault Tolerance |
|------|----------|----------------|
| **Standalone** | Development, testing | None (single process) |
| **Distributed** | Production | Automatic failover, task rebalancing |

## Gotchas

- **Task failure does NOT trigger rebalancing** - individual failed tasks must be restarted manually via REST API
- **Worker failure DOES trigger rebalancing** - tasks are redistributed to remaining active workers
- **DLQ only works for sink connectors** - source connectors have no DLQ mechanism
- **Converter mismatch = silent data corruption** - ensure producer and Connect use the same serialization format
- **Schema handling in custom connectors** - use `SchemaBuilder.struct()` to define record schemas; records carry schema for downstream consumers
- **JDBC polling vs CDC** - JDBC source polls with timestamps (has delay); Debezium reads WAL for real-time capture (no delay, no additional DB load)

## See Also

- [[schema-registry]] - schema management for Avro/Protobuf connectors
- [[transactional-outbox]] - CDC as alternative to explicit outbox pattern
- [[ksqldb]] - ksqlDB can create/manage connectors via SQL
- [[kafka-cluster-operations]] - monitoring Connect clusters
- [Apache Kafka Connect Documentation](https://kafka.apache.org/documentation/#connect)
- [Confluent Hub - Connector Marketplace](https://www.confluent.io/hub/)
