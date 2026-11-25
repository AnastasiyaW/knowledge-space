---
title: "API DataFrame PySpark"
category: reference
tags: [data-engineering, pyspark, spark, dataframe, sql]
level: 3
source_sha256: 41974eb24cadab59866577c7dc0da30b64608f7d231bd79d8ef2c340e8c44d6a
translation: machine
translated_at: '2026-10-24'
---
# API DataFrame PySpark {#pyspark-dataframe-api}

Référence complète des opérations sur les DataFrames PySpark - l'API principale pour le traitement de données structurées dans Spark.

## Création de SparkSession {#sparksession-creation}

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("my-app") \
    .master("spark://master-ip:7077") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", 4) \
    .getOrCreate()
```

## Création de DataFrames {#creating-dataframes}

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# With explicit schema (preferred for large datasets)
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.createDataFrame(data, schema)

# From files
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df = spark.read.json("data.json")
df = spark.read.parquet("data.parquet")

# From JDBC
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://host/db") \
    .option("dbtable", "schema.table") \
    .option("user", "user").option("password", "pass") \
    .load()

# From Pandas (caution: all data to driver)
df = spark.createDataFrame(pandas_df)
```

## Opérations courantes {#common-operations}

```python
from pyspark.sql import functions as F

# Select & rename
df.select("col1", "col2")
df.withColumnRenamed("old", "new")

# Filter
df.filter(F.col("age") > 25)
df.filter("status = 'active'")

# Add/modify columns
df.withColumn("new_col", F.col("price") * 1.2)

# Sorting
df.orderBy(F.col("date").desc())

# Aggregation
df.groupBy("category").agg(
    F.count("*").alias("cnt"),
    F.sum("amount").alias("total"),
    F.avg("amount").alias("avg_amount")
)

# Joins
df1.join(df2, on="key", how="inner")  # inner, left, right, full, cross, semi, anti

# Window functions
from pyspark.sql.window import Window
w = Window.partitionBy("dept").orderBy("salary")
df.withColumn("rank", F.rank().over(w))

# Date functions
df.withColumn("month", F.month("date_col"))
df.withColumn("trunc_month", F.trunc("date_col", "MM"))
```

## Types de données {#data-types}

**Simples :** `StringType()`, `BooleanType()`, `IntegerType()`, `LongType()`, `FloatType()`, `DoubleType()`, `DateType()`, `TimestampType()`

**Complexes :** `ArrayType(elementType)`, `MapType(keyType, valueType)`, `StructType()` / `StructField()`

## Lecture et écriture {#reading-and-writing}

```python
# Read from S3
df = spark.read.parquet("s3a://bucket/path/")

# Write with partitioning
df.write.mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("s3a://bucket/output/")

# Write modes: overwrite, append, ignore, error (default)
```

## Spark SQL {#spark-sql}

```python
df.createOrReplaceTempView("orders")
result = spark.sql("""
    SELECT customer, SUM(amount) AS total
    FROM orders
    GROUP BY customer
""")
```

## Accès S3 avec boto3 {#s3-access-with-boto3}

```python
import boto3
s3 = boto3.client('s3',
    endpoint_url='https://storage.example.com',
    aws_access_key_id='KEY',
    aws_secret_access_key='SECRET')

s3.upload_file('local.csv', 'bucket', 'prefix/file.csv')
s3.download_file('bucket', 'prefix/file.csv', 'local.csv')
```

## Bonnes pratiques {#best-practices}
- Toujours spécifier explicitement le schéma pour les grands jeux de données
- Utiliser `inferSchema=True` uniquement sur les petits jeux de données
- Privilégier Parquet/ORC pour le big data (orienté colonnes, compressé, predicate pushdown)
- Lors de la conversion depuis Pandas, surveiller `spark.driver.memory`
- Utiliser les fonctions natives de Spark plutôt que les UDF

## Voir aussi {#see-also}
- [[apache-spark-core]] - architecture et concepts
- [[spark-optimization]] - optimisation des performances
- [[etl-elt-pipelines]] - Spark comme moteur ETL
