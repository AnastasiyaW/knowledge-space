---
title: Spark Performance Optimization
category: reference
tags: [data-engineering, spark, optimization, partitioning, skew, broadcast]
---

# Spark Performance Optimization

Spark optimization revolves around minimizing shuffles, managing partitions, and leveraging the Catalyst optimizer effectively.

## Partition Management

**Default shuffle partitions:** 200. Configure:

```python
spark.conf.set("spark.sql.shuffle.partitions", 400)
spark.conf.set("spark.default.parallelism", 400)
```

**Optimal partition count:**
```
num_executors * executor_cores * (2 to 4)
```

**Target partition size:** ~128 MB (range: 64-256 MB).

### Repartition vs Coalesce

```python
df = df.repartition(1000)                    # by count (triggers full shuffle)
df = df.repartition("col1", "col2")          # by columns
df = df.coalesce(10)                         # reduce without full shuffle
```

**Rule:** `coalesce` for shrinking, `repartition` for expanding.

## Small File Problem

Many small files (< 128 MB HDFS block) cause: NameNode overhead, slow reads, too many small tasks.

**Solutions:**
- `repartition(N)` - creates N equal files (shuffle)
- `coalesce(N)` - reduces partitions without full shuffle (may be unequal)

## Data Skew

When some partitions have much more data than others - overloaded executors, idle resources, potential OOM.

### Solution 1: Broadcast Hash Join

For joining large table with small table (small must fit in executor memory):

```python
spark.table("big").join(spark.table("small").hint("broadcast"), "key")
# Auto-broadcast threshold:
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 104857600)  # 100MB
```

### Solution 2: Key Salting

Add random suffix to skewed keys to distribute evenly:

```python
df_big = df_big.withColumn('city', F.concat(
    F.col('city'), F.lit('_'),
    F.floor(F.rand(seed=17) * 5 + 1).cast('string')
))
# Explode corresponding keys in smaller table to match
```

### Solution 3: Adaptive Query Execution (AQE)

Automatic since Spark 3.0:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Skew threshold: partition > 5x median AND > 256MB
```

## Other Optimization Techniques

| Technique | Details |
|-----------|---------|
| **Early filtering** | Filter before shuffles to reduce data volume |
| **Avoid UDFs** | UDFs bypass Catalyst, cause Python-JVM serialization. Use native functions |
| **Caching** | `df.cache()` or `df.persist(StorageLevel.MEMORY_AND_DISK)` for reused DataFrames |
| **Columnar formats** | Parquet/ORC support predicate pushdown, column pruning |
| **Executor sizing** | 3-5 cores per executor; leave 1 core for OS; 2-3 tasks per CPU core |

## Gotchas
- `repartition` always triggers full shuffle; `coalesce` does not but may produce uneven partitions
- Broadcast join: smaller table must fit in both driver AND executor memory
- Default 200 shuffle partitions may be too few for large data or too many for small data
- Caching is not always beneficial - test before committing; visible in Spark UI Storage tab
- AQE in Spark 3.0+ handles many skew cases automatically

## See Also
- [[apache-spark-core]] - architecture fundamentals
- [[pyspark-dataframe-api]] - DataFrame operations
- [[file-formats]] - Parquet/ORC advantages
