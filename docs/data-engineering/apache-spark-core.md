---
title: Apache Spark Core Architecture
category: tools
tags: [data-engineering, spark, distributed-computing, pyspark, architecture]
---

# Apache Spark Core Architecture

Apache Spark is an open-source distributed data processing framework. Key advantages over MapReduce: in-memory computation, unified API for batch/streaming/ML/graph, support for Python/Scala/Java/R.

## Cluster Components

| Component | Role |
|-----------|------|
| **Cluster Manager** | Allocates resources. Options: Standalone, YARN, Kubernetes, Mesos |
| **Driver** | Master process - converts app into tasks, schedules, tracks progress |
| **SparkContext / SparkSession** | Entry point for interacting with the cluster |
| **Worker Node** | Server/VM running Executor processes |
| **Executor** | Process on Worker that executes Tasks |
| **Task** | Minimum unit of work - one operation on one Partition |
| **Partition** | Minimum logical data unit. Default shuffle partitions: 200 |

## Deploy Modes

- **Client mode:** Driver on submitting machine; stopping client kills all executors
- **Cluster mode:** Driver and executors both on cluster; client only for submission
- **Local mode:** All on one JVM. `--master local[*]` uses all cores. For dev/testing

## Execution Hierarchy

```
Application -> Job(s) -> Stage(s) -> Task(s)
```

- **Job:** created by an Action call
- **Stage:** set of Tasks without Shuffle boundary
- **Task:** one operation on one Partition
- **Shuffle:** data redistribution across nodes. Triggered by `join`, `groupBy`, `distinct`, `repartition`

## Spark Stack

| Module | Purpose |
|--------|---------|
| **Spark Core** | Task scheduling, memory management, fault tolerance |
| **Spark SQL + DataFrames** | Structured data via SQL or DataFrame API |
| **Spark Streaming** | Real-time micro-batch processing |
| **MLlib** | Distributed ML |
| **GraphX** | Graph processing |

## Data Structures

### RDD (Resilient Distributed Dataset)
Lowest-level API. Immutable, lazy evaluation, fault-tolerant via DAG lineage. Use for unstructured data or media files.

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
```

### DataFrame
Distributed named-column collection. Primary PySpark object. Catalyst optimizer for query planning.

### Dataset
Typed DataFrame (Scala/Java only). Not available in Python.

## Lazy Evaluation

Spark builds a logical plan optimized by **Catalyst Optimizer** (predicate pushdown, constant folding, filter reordering). Execution starts only when an Action is called.

**Transformations (lazy):**
- **Narrow** (no shuffle): `map`, `filter`, `select`, `withColumn`
- **Wide** (trigger shuffle): `join`, `groupBy`, `distinct`, `repartition`, `orderBy`

**Actions (trigger execution):**
```python
df.show()              # display rows
df.count()             # count rows
df.collect()           # all to driver (OOM risk!)
df.toPandas()          # convert to Pandas (all to driver)
df.write.parquet(path) # write to file
```

## Catalyst Optimizer Pipeline

1. **Logical Planning:** parse -> analyze -> optimize (predicate pushdown, constant folding)
2. **Physical Planning:** generate multiple plans -> cost-based selection
3. **Tungsten:** whole-stage code generation for CPU efficiency

## spark-submit

```bash
spark-submit \
  --master spark://master:7077 \
  --deploy-mode cluster \
  --executor-memory 4g \
  --executor-cores 4 \
  --num-executors 10 \
  app.py [args]
```

## PySpark vs Pandas

| Feature | PySpark | Pandas |
|---------|---------|--------|
| Execution | Distributed | Single machine |
| Evaluation | Lazy | Eager |
| Mutability | Immutable | Mutable |
| Scale | TB+ | Limited by RAM |

## Gotchas
- `collect()` and `toPandas()` bring all data to driver - OOM risk on large datasets
- UDFs bypass Catalyst optimizer and cause Python-JVM serialization overhead
- `inferSchema=True` reads entire CSV to determine types - slow on large files
- Spark Streaming Structured API does not allow terminal actions mid-pipeline
- Spark on Kubernetes production-ready since Spark 3.1 (March 2021)

## See Also
- [[pyspark-dataframe-api]] - DataFrame operations reference
- [[spark-optimization]] - performance tuning
- [[spark-streaming]] - real-time processing
- [[etl-elt-pipelines]] - Spark as ETL engine
