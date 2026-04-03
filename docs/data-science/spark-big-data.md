---
title: Apache Spark and Big Data Processing
category: tools
tags: [data-science, spark, big-data, distributed, optimization]
---

# Apache Spark and Big Data Processing

When data exceeds single-machine memory, Spark distributes computation across clusters. Understanding Spark's execution model is critical for performance.

## Architecture

- **SparkContext**: entry point for functionality
- **Driver**: orchestrates execution
- **Worker Node -> Executor -> Task**: execution hierarchy
- **Partition**: unit of data parallelism
- **Job -> Stage -> Task**: computation hierarchy

## Core Optimization Rules

- **2-3 tasks per CPU core** for optimal parallelism
- **~128 MB per partition** recommended
- Monitor data skew via Spark UI
- Push filters as early as possible (predicate pushdown)
- Avoid Python UDFs (break Catalyst optimizer) - use built-in functions

## Shuffle

Data redistribution across nodes. **Most expensive operation.**

Triggers: `groupBy`, `join`, `distinct`, `repartition`, `orderBy`

Minimizing shuffle:
- Filter before joining
- Broadcast small tables
- Use `coalesce` (no shuffle) instead of `repartition` when reducing partitions

## Key Techniques

### Broadcast Join
Send small table to all executors, avoid shuffle.
```python
from pyspark.sql.functions import broadcast
result = big_df.join(broadcast(small_df), 'key')
```

Use when one side is small (< 10MB default, configurable).

### Caching
```python
df.cache()     # in memory
df.persist()   # configurable storage level
df.unpersist() # free memory
```

Cache DataFrames that are reused multiple times. Don't cache everything - memory is limited.

### Repartition vs Coalesce
```python
df.repartition(100)     # full shuffle, any number of partitions
df.repartition('key')   # partition by column (useful before groupBy)
df.coalesce(10)         # reduce partitions without shuffle
```

## Data Skew

**Problem**: one partition much larger than others -> one task takes disproportionately long.

**Detection**: Spark UI shows task durations. If max >> median, you have skew.

**Solutions**:
- **Salting**: add random prefix to skewed key, join with exploded dimension
- **Broadcast join**: for skewed side if small enough
- **Repartition by different key**: redistribute data

## Small File Problem

Too many small files = too many tasks = scheduling overhead.

**Fix**: compact files via `coalesce()` or repartition before writing.

```python
df.coalesce(10).write.parquet('output/')
```

## Executor Sizing

- **Memory**: too small = spill to disk (slow), too large = GC pauses
- **Cores**: 5 cores per executor is a good default
- Balance: more executors with moderate resources vs fewer with more

## Gotchas
- Spark is lazy - transformations don't execute until an action (collect, count, write)
- `collect()` brings all data to driver - OOM for large datasets. Use `take()` or `show()`
- Python UDFs are 10-100x slower than built-in Spark functions due to serialization overhead
- Joins on skewed keys can run forever without intervention
- Always check partition count after reading: `df.rdd.getNumPartitions()`

## See Also
- [[sql-for-data-science]] - Spark SQL uses same concepts
- [[pandas-eda]] - Spark DataFrame API is pandas-inspired
- [[ds-workflow]] - Spark in the data pipeline
