---
title: Apache Spark
category: concepts
tags: [spark, pyspark, distributed, rdd, dataframe, spark-sql, big-data]
---

# Apache Spark

Apache Spark is a unified analytics engine for large-scale data processing. It provides in-memory computation, a rich API (Scala, Python, Java, R), and modules for SQL, streaming, ML, and graph processing. Spark is 10-100x faster than [[mapreduce]] for iterative workloads.

## Key Facts

- **SparkSession** is the unified entry point (since Spark 2.0), replacing SparkContext + SQLContext + HiveContext
- **Architecture**: Driver program creates SparkSession, communicates with Cluster Manager (YARN/Standalone/Mesos/K8s), which allocates Executors on worker nodes
- **RDD (Resilient Distributed Dataset)**: low-level immutable distributed collection. Supports transformations (lazy) and actions (trigger computation). Largely superseded by DataFrame API
- **DataFrame API**: distributed collection of rows with named columns. Higher-level than RDD, enables Catalyst query optimizer. Preferred for most workloads
- **Lazy evaluation**: transformations (map, filter, join) build a DAG of operations; execution happens only when an action (count, collect, write) is called
- **Partitions**: data is divided into partitions distributed across executors. Number of partitions = parallelism level
- **Deploy modes**: `cluster` (driver runs on a cluster node) vs `client` (driver runs on the submitting machine). Use cluster mode for production, client for interactive development
- **spark-submit**: CLI tool for launching Spark applications on a cluster
- Spark uses RAM primarily (not disk like MapReduce), with disk spillover for data exceeding memory

## Patterns

### SparkSession creation

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()
```

### spark-submit command

```bash
spark-submit \
    --master spark://10.10.172.08:7077 \
    --deploy-mode cluster \
    --num-executors 5 \
    --executor-memory 4g \
    --executor-cores 2 \
    PySparkJob.py input.parquet output/
```

### DataFrame operations

```python
# Read
df = spark.read.parquet("hdfs:///data/events/")

# Transform
result = (df
    .filter(df.event_type == "click")
    .groupBy("user_id")
    .agg(
        F.count("*").alias("click_count"),
        F.sum("revenue").alias("total_revenue")
    )
    .orderBy(F.desc("click_count"))
)

# Write with partitioning
result.write \
    .mode("overwrite") \
    .partitionBy("dt") \
    .parquet("hdfs:///data/output/clicks_agg/")
```

### Train/test/validate split

```python
train, test, validate = df.randomSplit([0.5, 0.25, 0.25], seed=42)
train.write.parquet("output/train")
test.write.parquet("output/test")
validate.write.parquet("output/validate")
```

## Gotchas

- `collect()` pulls all data to the driver. On large datasets this causes OOM. Use `take(n)`, `show()`, or write to storage instead
- Spark DataFrame operations are lazy - calling `.filter().groupBy()` does nothing until an action triggers execution. This enables Catalyst to optimize the entire query plan
- Number of partitions matters: too few = underutilized cores; too many = scheduling overhead. Rule of thumb: 2-4 partitions per CPU core
- Shuffle operations (groupBy, join, repartition) are expensive: they move data across the network. Minimize shuffles by using broadcast joins for small tables (`F.broadcast(small_df)`)
- `--deploy-mode cluster` means the driver runs remotely - you cannot access local files or see stdout directly. Use HDFS/S3 for I/O and Spark UI for logs

## See Also

- [[spark-sql-and-dataframes]] - SQL API and DataFrame operations in depth
- [[spark-ml]] - machine learning pipeline in Spark
- [[hadoop-ecosystem]] - Spark on YARN
- [[data-formats]] - Parquet as preferred Spark format
- https://spark.apache.org/docs/latest/ - Apache Spark documentation
