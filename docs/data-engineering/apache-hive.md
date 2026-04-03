---
title: Apache Hive
category: tools
tags: [data-engineering, hive, sql-on-hadoop, metastore, data-warehouse]
---

# Apache Hive

Hive is a SQL-on-Hadoop warehouse system. It translates SQL queries into MapReduce/Tez/Spark jobs. Not a database - it is a query translation layer over HDFS data.

## Architecture

```
Hive Client (CLI/JDBC/Thrift)
       |
   Hive Driver -> Compiler (uses Metastore) -> Executor -> HDFS
```

- **Metastore:** table schemas, column types, partition info, SerDe config. Backed by RDBMS (MySQL/PostgreSQL)
- **Compiler:** translates HiveQL to MapReduce/Tez DAG using metadata
- **Driver:** receives SQL, orchestrates compilation and execution

## Table Types

| Type | DROP TABLE behavior |
|------|-------------------|
| **Managed** | Deletes metadata AND data |
| **External** | Deletes only metadata, data remains on HDFS/S3 |

## JOIN Strategies

### Reduce Side Join (Default)
- Mappers emit join key + value from both tables
- Reducers receive matching keys, perform join
- Works for small-medium tables. Fails for two very large tables (OOM)

### Map Side Join (MapJoin)
- Small table loaded into HashMap, distributed via HDFS
- Each Mapper joins with its split of large table
- No Reduce stage needed for join
- Hint: `SELECT /*+ MAPJOIN(small_table) */ ...`

### Sort-Merge-Bucket Join (SMB)
- Most efficient for two large tables
- **Requirements:**
  1. Both tables bucketed by join key (`CLUSTERED BY`)
  2. Bucket counts must be multiples (2:4, 5:10)
  3. Config: `hive.auto.convert.sortmerge.join=true`
- Join entirely in Map phase - no shuffle, no reduce

## Hive Specifics
- Uses HiveQL (SQL-like with extensions)
- Transactions: ORC format only, delta files applied on read, compaction merges
- No BEGIN/COMMIT/ROLLBACK - auto-commit per statement
- Virtual columns: `INPUT__FILE__NAME`, `BLOCK__OFFSET__INSIDE__FILE`

## Gotchas
- SMB Join: if data inserted without enforcing bucketing, silent wrong results (worse than errors). Always `hive.enforce.bucketing=true`
- Complex queries (JOIN + GROUP BY) generate multiple chained MapReduce jobs
- Hive is being replaced by Spark SQL and Trino/Presto for interactive queries
- Metastore is still widely used as schema catalog (even without Hive queries)

## See Also
- [[hadoop-hdfs]] - underlying storage
- [[mapreduce]] - execution engine
- [[apache-spark-core]] - modern alternative
- [[file-formats]] - ORC format for Hive
