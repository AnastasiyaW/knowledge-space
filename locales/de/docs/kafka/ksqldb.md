---
title: "ksqlDB"
category: concepts
tags: [kafka, ksqldb, sql, streaming, push-query, pull-query, materialized-view]
level: 3
source_sha256: 9df4e04b0255200c01192717204e61b5909578218952e8c54aa13e6d8a96cdb5
translation: machine
translated_at: '2026-10-24'
---
# ksqlDB {#ksqldb}

ksqlDB ist eine Streaming-SQL-Engine auf Basis von Kafka Streams. Sie übersetzt SQL-Anweisungen in Kafka-Streams-Topologien und ermöglicht Stream-Processing ohne JVM-Programmierung.

## Wichtige Fakten {#key-facts}

- Teil der Confluent Platform (nicht Teil des Apache-Kafka-Kerns)
- Läuft als JVM-Anwendung und verbindet sich mit einem Kafka-Cluster; jede persistente Query läuft als eigene Kafka-Streams-Anwendung
- SQL-Anweisungen werden intern in Kafka-Streams-Topologien umgewandelt
- **STREAM** = partitionierte, unveränderliche, nur anfügbare (append-only) Sammlung (entspricht KStream)
- **TABLE** = veränderliche, partitionierte Sammlung, bei der Aktualisierungen vorherige Werte überschreiben (entspricht KTable)
- **Push-Queries**: laufen kontinuierlich und liefern neue Ergebnisse, sobald neue Daten eintreffen (`EMIT CHANGES`)
- **Pull-Queries**: einmalige Momentaufnahme des Ergebnisses auf materialisierten Tables (wie ein klassisches SQL-SELECT)
- Deployment-Modi: **Interactive** (CLI/REST) und **Headless/Autonomous** (Queries nur aus einer Datei, Produktionsmodus)
- Unterstützte Formate: JSON, AVRO, PROTOBUF, DELIMITED (CSV), KAFKA (Rohbytes)
- Integriert sich automatisch mit der [[schema-registry]], wenn AVRO oder PROTOBUF verwendet wird
- Standardport: 8088 (REST-API)
- ksqlDB ist KEIN Ersatz für eine Datenbank – es verarbeitet Streams

## Muster {#patterns}

### DDL – Stream und Table erstellen {#ddl-create-stream-and-table}

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

### Persistente Queries (kontinuierliche Verarbeitung) {#persistent-queries-continuous-processing}

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

### Fensterbasierte Aggregationen {#windowed-aggregations}

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

### Joins {#joins}

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

### REST-API {#rest-api}

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

### Nützliche Befehle {#useful-commands}

```sql
SHOW TOPICS;                    SHOW STREAMS;
SHOW TABLES;                    SHOW QUERIES;
DESCRIBE stream_name;           DESCRIBE EXTENDED stream_name;
PRINT 'topic_name' FROM BEGINNING;
DROP STREAM stream_name;        TERMINATE query_id;
INSERT INTO stream_name (col1) VALUES ('val1');
```

### Pseudospalten für Ereignis-Metadaten {#event-metadata-pseudo-columns}

```sql
SELECT ROWTIME, ROWPARTITION, ROWOFFSET, HEADERS FROM stream EMIT CHANGES;
```

### Integration mit Kafka Connect {#kafka-connect-integration}

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

### Funktionen {#functions}

Eingebaute Skalarfunktionen: `SUBSTRING`, `CONCAT`, `CAST`, `TIMESTAMPTOSTRING`, `LEN`, `ABS`, `UCASE`, `LCASE`
Aggregatfunktionen: `COUNT`, `SUM`, `MIN`, `MAX`, `AVG`, `COLLECT_LIST`, `COLLECT_SET`, `TOPK`, `TOPKDISTINCT`
Eigene UDFs: in Java implementieren und als JAR-Dateien bereitstellen.

## Stolperfallen {#gotchas}

- **Pull-Queries funktionieren nur auf materialisierten Tables** – nicht auf rohen Streams; zuerst muss eine persistente Aggregationsquery erstellt werden
- **Anforderungen an Joins** – Ereignisse müssen denselben Schlüsseltyp haben, Sammlungen müssen dieselbe Partitionsanzahl und dieselbe Partitionierungsstrategie besitzen
- **Jede persistente Query erzeugt interne Topics und State Stores** – der Ressourcenverbrauch wächst mit der Anzahl der Queries
- **Headless-Modus für die Produktion** – `queries.file=/path/to/query.sql` deaktiviert die REST-API und verhindert Änderungen zur Laufzeit
- **Die Standard-Grace-Period beträgt 24 Stunden** – sie kann bei fensterbasierten Aggregationen erheblich Speicher belegen; sie sollte anhand der tatsächlichen Muster verspäteter Daten abgestimmt werden

## Siehe auch {#see-also}

- [[kafka-streams]] – zugrunde liegende Bibliothek, auf der ksqlDB aufbaut
- [[kafka-streams-windowing]] – Fenstertypen und Zeitsemantik
- [[kafka-connect]] – Connector-Integration aus ksqlDB heraus
- [[schema-registry]] – Schema-Verwaltung für die Formate AVRO und PROTOBUF
- [ksqlDB-Dokumentation](https://docs.ksqldb.io/)
