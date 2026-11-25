---
title: "Kafka Connect"
category: concepts
tags: [kafka, connect, source, sink, connector, smt, debezium, distributed, worker, task]
level: 4
source_sha256: 10c1374eda9c6f9982c5e62b846ae88bd9938725569d8c7ba41f41d6e5315287
translation: machine
translated_at: '2026-10-24'
---
# Kafka Connect {#kafka-connect}

Kafka Connect ist ein Framework für den Datenstrom zwischen Kafka und externen Systemen (Datenbanken, Suchindizes, Dateisysteme, Cloud-Speicher) mit austauschbaren Connectors sowie integrierter Fehlertoleranz, Task-Verteilung und Offset-Verwaltung.

## Wichtige Fakten {#key-facts}

- Teil von Apache Kafka, stellt eine Laufzeitumgebung für Connector-Plugins bereit
- **Source-Connectors**: lesen Daten aus externen Systemen in Kafka-Topics
- **Sink-Connectors**: schreiben Daten aus Kafka-Topics in externe Systeme
- **Connector** = Koordinator; bestimmt die Anzahl der Tasks, teilt die Arbeit auf und erhält die Konfiguration von den Workern
- **Task** = eigentlicher Datenverarbeiter; läuft in einem eigenen Java-Thread; der Connector teilt einen Job für die Parallelisierung in mehrere Tasks auf
- **Worker** = Container-Prozess für Connectors und Tasks; verarbeitet REST-Anfragen, speichert Konfigurationen und übernimmt die Neuzuweisung von Tasks
- **Converter** = wandelt zwischen Byte-Arrays und dem internen Datenformat von Connect um
- **SMT (Single Message Transform)** = leichtgewichtige Transformationen pro Nachricht
- **Dead Letter Queue** = Topic für fehlgeschlagene Nachrichten (nur bei Sink-Connectors)
- Der Distributed-Modus speichert Konfigurationen, Offsets und Status in internen Kafka-Topics: `connect-configs`, `connect-offsets`, `connect-status`

## Muster {#patterns}

### Kafka Connect ausführen {#running-kafka-connect}

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

Wichtige Eigenschaften:
```properties
bootstrap.servers=broker1:9092,broker2:9092
group.id=connect-cluster
plugin.path=/opt/connectors
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
rest.host.name=0.0.0.0
rest.port=8083
```

### REST API {#rest-api}

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

### JDBC-Source-Connector (PostgreSQL) {#jdbc-source-connector-postgresql}

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

### Debezium-CDC-Source (PostgreSQL-WAL) {#debezium-cdc-source-postgresql-wal}

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

### Integrierte SMTs {#built-in-smts}

| SMT | Zweck |
|-----|---------|
| `Cast` | Ändert Feldtypen |
| `MaskField` | Maskiert sensible Daten |
| `Filter` | Verwirft bzw. behält Nachrichten anhand einer Bedingung |
| `Flatten` | Flacht verschachtelte Strukturen ab |
| `InsertField` | Fügt Felder hinzu (z. B. Zeitstempel, Topic-Name) |
| `InsertHeader` | Fügt Nachrichten-Header hinzu |
| `ReplaceField` | Benennt Felder um oder entfernt sie |
| `TimestampConverter` | Konvertiert Zeitstempelformate |
| `TimestampRouter` | Leitet anhand des Zeitstempels an ein Topic weiter |
| `RegexRouter` | Leitet anhand eines Regex-Treffers an ein Topic weiter |
| `ExtractField` | Extrahiert ein einzelnes Feld aus einer komplexen Nachricht |

### Konfiguration der Dead Letter Queue {#dead-letter-queue-configuration}

```json
{
  "errors.tolerance": "all",
  "errors.deadletterqueue.topic.name": "dlq-connector-errors",
  "errors.deadletterqueue.topic.replication.factor": 3,
  "errors.deadletterqueue.context.headers.enable": true
}
```

- `errors.tolerance=none` (Standard): ein Fehler führt sofort zum Task-Fehlschlag
- `errors.tolerance=all`: Fehler werden stillschweigend ignoriert, sofern keine DLQ konfiguriert ist

### Entwicklung eigener Connectors {#custom-connector-development}

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

### Standalone vs. Distributed {#standalone-vs-distributed}

| Modus | Anwendungsfall | Fehlertoleranz |
|------|----------|----------------|
| **Standalone** | Entwicklung, Tests | Keine (einzelner Prozess) |
| **Distributed** | Produktion | Automatisches Failover, Task-Rebalancing |

## Fallstricke {#gotchas}

- **Ein Task-Fehler löst KEIN Rebalancing aus**: fehlgeschlagene Tasks müssen manuell über die REST API neu gestartet werden
- **Ein Worker-Ausfall löst ein Rebalancing aus**: Tasks werden auf die verbleibenden aktiven Worker verteilt
- **Die DLQ funktioniert nur für Sink-Connectors**: Source-Connectors besitzen keinen DLQ-Mechanismus
- **Nicht passender Converter = stille Datenkorruption**: Producer und Connect müssen dasselbe Serialisierungsformat verwenden
- **Schema-Handhabung in eigenen Connectors**: mit `SchemaBuilder.struct()` werden Record-Schemas definiert; Records enthalten das Schema für nachgelagerte Consumer
- **JDBC-Polling vs. CDC**: JDBC-Source fragt anhand von Zeitstempeln ab (mit Verzögerung); Debezium liest das WAL und erfasst Änderungen in Echtzeit (ohne Verzögerung und ohne zusätzliche Datenbanklast)

## Siehe auch {#see-also}

- [[schema-registry]] - Schema-Verwaltung für Avro-/Protobuf-Connectors
- [[transactional-outbox]] - CDC als Alternative zum expliziten Outbox-Pattern
- [[ksqldb]] - ksqlDB kann Connectors per SQL anlegen und verwalten
- [[kafka-monitoring-and-tuning]] - Überwachung von Connect-Clustern
- [Apache Kafka Connect Documentation](https://kafka.apache.org/documentation/#connect)
- [Confluent Hub - Connector Marketplace](https://www.confluent.io/hub/)
