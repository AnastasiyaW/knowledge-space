---
title: Spark SQL and DataFrames
category: concepts
tags: [spark-sql, dataframe, pyspark, catalyst, sql, query-optimization]
---

# Spark SQL and DataFrames

Spark SQL is the module for structured data processing in [[apache-spark]]. It provides a DataFrame API (programmatic) and SQL interface (declarative) that both compile down to the same optimized execution plan via the Catalyst optimizer.

## Key Facts

- **DataFrame** = distributed collection of Row objects with a schema (column names + types). Equivalent to a table in relational databases
- **Catalyst optimizer** converts logical plan -> optimized logical plan -> physical plan. Applies predicate pushdown, column pruning, join reordering automatically
- **Spark SQL** can execute standard SQL queries via `spark.sql("SELECT ...")` alongside DataFrame API operations
- Data sources: Parquet (default, recommended), ORC, JSON, CSV, JDBC, Avro, Delta Lake, Iceberg
- **Temp views**: `df.createOrReplaceTempView("events")` registers a DataFrame as a SQL-queryable table within the SparkSession
- **UDF (User Defined Function)**: extend SQL/DataFrame with custom Python/Scala functions. Python UDFs are slow (serialization overhead); use Pandas UDFs (vectorized) for better performance
- **Window functions**: `F.row_number().over(Window.partitionBy("user").orderBy("ts"))` for ranking, running totals, lag/lead - same semantics as SQL window functions
- **Broadcast join**: when one side of a join is small (<10 MB default), Spark broadcasts it to all executors avoiding shuffle. Force with `F.broadcast(small_df)`

## Patterns

### Reading and writing data

```python
# Read Parquet
df = spark.read.parquet("s3://bucket/events/")

# Read CSV with schema inference
df = spark.read.option("header", True).option("inferSchema", True).csv("data.csv")

# Read from JDBC
df = spark.read.jdbc(
    url="jdbc:postgresql://host:5432/db",
    table="orders",
    properties={"user": "admin", "password": "secret"}
)

# Write partitioned Parquet
df.write.mode("overwrite").partitionBy("dt").parquet("output/")
```

### SQL + DataFrame interop

```python
df.createOrReplaceTempView("orders")

# SQL query
result = spark.sql("""
    SELECT customer_id, SUM(revenue) AS total
    FROM orders
    WHERE dt >= '2026-01-01'
    GROUP BY customer_id
    HAVING SUM(revenue) > 1000
""")

# Equivalent DataFrame API
from pyspark.sql import functions as F

result = (df
    .filter(F.col("dt") >= "2026-01-01")
    .groupBy("customer_id")
    .agg(F.sum("revenue").alias("total"))
    .filter(F.col("total") > 1000)
)
```

### Window functions

```python
from pyspark.sql.window import Window

w = Window.partitionBy("user_id").orderBy(F.desc("score"))
df_ranked = df.withColumn("rank", F.row_number().over(w))
top_per_user = df_ranked.filter(F.col("rank") == 1)
```

### Pandas UDF (vectorized)

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def normalize(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()

df = df.withColumn("score_norm", normalize(F.col("score")))
```

## Gotchas

- `spark.sql()` returns a DataFrame - it does NOT execute immediately (lazy evaluation). Call `.show()`, `.collect()`, or `.write` to trigger
- Python UDFs (non-vectorized) are 10-100x slower than native Spark functions. Always check if `pyspark.sql.functions` has a built-in alternative before writing a UDF
- `inferSchema=True` on CSV reads the entire file twice (first pass infers types). Provide explicit schema for production pipelines
- `df.cache()` and `df.persist()` store DataFrames in memory/disk for reuse. Forgetting to `unpersist()` leaks memory across the session

## See Also

- [[apache-spark]] - architecture and core concepts
- [[spark-ml]] - ML pipelines built on DataFrames
- [[data-formats]] - Parquet as recommended Spark format
- https://spark.apache.org/docs/latest/sql-programming-guide.html
