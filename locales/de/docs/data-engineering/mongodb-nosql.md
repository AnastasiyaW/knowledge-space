---
title: "MongoDB und NoSQL"
category: tools
tags: [data-engineering, mongodb, nosql, document-database, cap-theorem]
level: 4
source_sha256: 868b800507c06b8d8e2bc062f96188b25ea5e4649f9769ed81b259b8b14f1a15
translation: machine
translated_at: '2026-10-24'
---
# MongoDB und NoSQL {#mongodb-and-nosql}

MongoDB ist eine dokumentenorientierte NoSQL-Datenbank, die für Szenarien entwickelt wurde, in denen relationale Datenbanken an ihre Skalierungsgrenzen stoßen. NoSQL („Not Only SQL“)-Datenbanken bewältigen die 3V-Herausforderungen von Big Data: Volume, Velocity, Variety.

## NoSQL-Modelle {#nosql-models}

| Modell | Struktur | Anwendungsfall | Beispiele |
|-------|-----------|----------|----------|
| **Key-Value** | Schlüssel -> Wert | Caching, Sessions | Redis, DynamoDB |
| **Dokument** | JSON/BSON-Dokumente | Inhalte, Kataloge | MongoDB, CouchDB |
| **Column Family** | Spaltengruppen | Zeitreihen, Analytik | Cassandra, HBase |
| **Graph** | Knoten + Kanten | Soziale Netzwerke | Neo4j, JanusGraph |

## CAP-Theorem {#cap-theorem}

In jedem verteilten System lassen sich von drei Eigenschaften höchstens zwei garantieren: **Consistency** (Konsistenz), **Availability** (Verfügbarkeit), **Partition Tolerance** (Partitionstoleranz). MongoDB ist standardmäßig CP (Consistency + Partition Tolerance).

## MongoDB-Architektur {#mongodb-architecture}

- **Replica Set:** 3 mongod-Prozesse, automatisches Failover
- **Sharding:** verteilt Daten anhand des Shard-Schlüssels zur horizontalen Skalierung
- 1 Shard = 1 Replica Set

## CRUD-Operationen {#crud-operations}

```javascript
// Filtering
{ capital: "Moscow" }
{ area: { $gt: 5000000 } }
{ borders: { $size: 2 } }
{ $and: [{ "languages.eng": { $exists: true } }, { region: "Asia" }] }
```

## Aggregation Pipelines {#aggregation-pipelines}

```javascript
[
  { "$unwind": { "path": "$scores" } },
  { "$group": { "_id": "$scores.type", "avg": { "$avg": "$scores.score" } } }
]
```

Wichtige Stages: `$unwind`, `$group`, `$addFields`, `$sort`, `$match`, `$lookup` (JOIN-Entsprechung)

## Zuordnung von SQL zu MongoDB {#sql-to-mongodb-mapping}

| SQL | MongoDB |
|-----|---------|
| SELECT | `find()` / `$project` |
| WHERE | `$match` |
| GROUP BY | `$group` |
| ORDER BY | `$sort` |
| JOIN | `$lookup` |

## Siehe auch {#see-also}
- [[hbase]] - spaltenorientierte NoSQL-Datenbank in Hadoop
- [[dwh-architecture]] - NoSQL im Kontext der Datenplattform
- [[data-lake-lakehouse]] - Schema-on-Read-Muster
