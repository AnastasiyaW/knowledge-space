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

ksqlDB est un moteur SQL de traitement de flux construit sur Kafka Streams. Il traduit les instructions SQL en topologies Kafka Streams, ce qui permet de faire du traitement de flux sans programmation en JVM.

## Faits clés {#key-facts}

- Fait partie de Confluent Platform (et non du cœur d'Apache Kafka)
- S'exécute comme une application JVM connectée à un cluster Kafka ; chaque requête persistante s'exécute comme une application Kafka Streams
- Les instructions SQL sont converties en topologies Kafka Streams en interne
- **STREAM** = collection partitionnée, immuable et en ajout seul (correspond à KStream)
- **TABLE** = collection partitionnée et mutable, où les mises à jour remplacent les valeurs précédentes (correspond à KTable)
- **Requêtes push** : s'exécutent en continu et émettent des résultats à mesure que de nouvelles données arrivent (`EMIT CHANGES`)
- **Requêtes pull** : résultat ponctuel à un instant donné sur des tables matérialisées (comme un SELECT SQL classique)
- Modes de déploiement : **Interactif** (CLI/REST) et **Headless/Autonome** (requêtes lues uniquement depuis un fichier, mode production)
- Formats supportés : JSON, AVRO, PROTOBUF, DELIMITED (CSV), KAFKA (octets bruts)
- S'intègre automatiquement à [[schema-registry]] lors de l'utilisation d'AVRO/PROTOBUF
- Port par défaut : 8088 (API REST)
- ksqlDB n'est PAS un remplacement d'une base de données : il traite des flux

## Modèles {#patterns}

### DDL - Créer un stream et une table {#ddl-create-stream-and-table}

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

### Requêtes persistantes (traitement continu) {#persistent-queries-continuous-processing}

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

### Agrégations par fenêtre {#windowed-aggregations}

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

### Jointures {#joins}

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

### API REST {#rest-api}

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

### Commandes utiles {#useful-commands}

```sql
SHOW TOPICS;                    SHOW STREAMS;
SHOW TABLES;                    SHOW QUERIES;
DESCRIBE stream_name;           DESCRIBE EXTENDED stream_name;
PRINT 'topic_name' FROM BEGINNING;
DROP STREAM stream_name;        TERMINATE query_id;
INSERT INTO stream_name (col1) VALUES ('val1');
```

### Pseudo-colonnes de métadonnées d'événements {#event-metadata-pseudo-columns}

```sql
SELECT ROWTIME, ROWPARTITION, ROWOFFSET, HEADERS FROM stream EMIT CHANGES;
```

### Intégration avec Kafka Connect {#kafka-connect-integration}

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

### Fonctions {#functions}

Scalaires intégrées : `SUBSTRING`, `CONCAT`, `CAST`, `TIMESTAMPTOSTRING`, `LEN`, `ABS`, `UCASE`, `LCASE`
Agrégats : `COUNT`, `SUM`, `MIN`, `MAX`, `AVG`, `COLLECT_LIST`, `COLLECT_SET`, `TOPK`, `TOPKDISTINCT`
UDF personnalisées : à implémenter en Java, puis à déployer sous forme de fichiers JAR.

## Pièges courants {#gotchas}

- **Les requêtes pull ne fonctionnent que sur les tables matérialisées**, pas sur les streams bruts ; il faut d'abord créer une requête d'agrégation persistante
- **Exigences pour les jointures** : les événements doivent avoir le même type de clé, et les collections doivent avoir le même nombre de partitions et la même stratégie de partitionnement
- **Chaque requête persistante crée des topics internes et des state stores** : la consommation de ressources croît avec le nombre de requêtes
- **Mode headless en production** : `queries.file=/path/to/query.sql` désactive l'API REST et empêche la modification des requêtes à l'exécution
- **La période de grâce (grace period) par défaut est de 24 heures** : elle peut consommer beaucoup de mémoire pour les agrégations par fenêtre ; ajustez-la en fonction des schémas réels de données tardives

## Voir aussi {#see-also}

- [[kafka-streams]] - bibliothèque sous-jacente sur laquelle ksqlDB est construit
- [[kafka-streams-windowing]] - types de fenêtres et sémantique temporelle
- [[kafka-connect]] - intégration des connecteurs depuis ksqlDB
- [[schema-registry]] - gestion des schémas pour les formats AVRO/PROTOBUF
- [Documentation ksqlDB](https://docs.ksqldb.io/)
