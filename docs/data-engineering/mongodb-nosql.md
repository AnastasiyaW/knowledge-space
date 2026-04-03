---
title: MongoDB and NoSQL
category: tools
tags: [data-engineering, mongodb, nosql, document-database, cap-theorem]
---

# MongoDB and NoSQL

MongoDB is a document-oriented NoSQL database designed for scenarios where relational databases hit scalability limits. NoSQL ("Not Only SQL") databases handle the 3V challenges of big data: Volume, Velocity, Variety.

## NoSQL Models

| Model | Structure | Use Case | Examples |
|-------|-----------|----------|----------|
| **Key-Value** | key -> value | Caching, sessions | Redis, DynamoDB |
| **Document** | JSON/BSON documents | Content, catalogs | MongoDB, CouchDB |
| **Column Family** | Column groups | Time-series, analytics | Cassandra, HBase |
| **Graph** | Nodes + edges | Social networks | Neo4j, JanusGraph |

## CAP Theorem

In any distributed system, you can guarantee at most two of three: **Consistency**, **Availability**, **Partition tolerance**. MongoDB is CP (Consistency + Partition Tolerance) by default.

## MongoDB Architecture

- **Replica Set:** 3 mongod processes, automatic failover
- **Sharding:** distributes data by shard key for horizontal scaling
- 1 shard = 1 replica set

## CRUD Operations

```javascript
// Filtering
{ capital: "Moscow" }
{ area: { $gt: 5000000 } }
{ borders: { $size: 2 } }
{ $and: [{ "languages.eng": { $exists: true } }, { region: "Asia" }] }
```

## Aggregation Pipelines

```javascript
[
  { "$unwind": { "path": "$scores" } },
  { "$group": { "_id": "$scores.type", "avg": { "$avg": "$scores.score" } } }
]
```

Key stages: `$unwind`, `$group`, `$addFields`, `$sort`, `$match`, `$lookup` (JOIN equivalent)

## SQL to MongoDB Mapping

| SQL | MongoDB |
|-----|---------|
| SELECT | `find()` / `$project` |
| WHERE | `$match` |
| GROUP BY | `$group` |
| ORDER BY | `$sort` |
| JOIN | `$lookup` |

## See Also
- [[hbase]] - columnar NoSQL in Hadoop
- [[dwh-architecture]] - NoSQL in data platform context
- [[data-lake-lakehouse]] - schema-on-read patterns
