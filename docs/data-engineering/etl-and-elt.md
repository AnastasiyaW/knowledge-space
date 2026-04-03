---
title: ETL and ELT Patterns
category: concepts
tags: [etl, elt, pipeline, data-integration, transformation, staging]
---

# ETL and ELT Patterns

ETL (Extract-Transform-Load) and ELT (Extract-Load-Transform) are the two fundamental approaches to moving data from source systems into analytical storage. The choice between them depends on where transformation compute happens and the maturity of the target platform.

## Key Facts

- **ETL** transforms data in a staging area (or dedicated compute) before loading into the [[data-warehouse]]. Traditional approach; well-suited when target storage is expensive or has limited compute (e.g., on-prem RDBMS)
- **ELT** loads raw data first, then transforms inside the target system using its own compute engine. Dominant in cloud data platforms (BigQuery, Snowflake, Redshift) where storage is cheap and compute scales elastically
- Both patterns require an orchestrator (e.g., [[apache-airflow]], Prefect, Dagster) to schedule and monitor pipeline execution
- **Staging layer** (raw/landing zone) holds ingested data as-is before transformation, regardless of ETL or ELT
- Transformation typically involves: deduplication, type casting, joining reference data, applying business rules, computing aggregates
- **Incremental loads** process only new/changed records (using watermarks, timestamps, or [[partitioning-and-sharding]] keys). Full refreshes are simpler but do not scale
- CDC (Change Data Capture) enables near-real-time incremental extraction by reading database transaction logs (e.g., Debezium reading PostgreSQL WAL)

## Patterns

### Classic ETL Pipeline (Python + SQL)

```python
# Extract
df = pd.read_sql("SELECT * FROM orders WHERE updated_at > %s", conn, params=[watermark])

# Transform
df['revenue'] = df['quantity'] * df['unit_price']
df = df.drop_duplicates(subset=['order_id'], keep='last')
df['load_ts'] = datetime.utcnow()

# Load
df.to_sql('fact_orders', dwh_engine, if_exists='append', index=False)
```

### ELT with dbt-style SQL transformation

```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
)
SELECT
    order_id,
    customer_id,
    quantity * unit_price AS revenue,
    updated_at,
    CURRENT_TIMESTAMP AS loaded_at
FROM source
WHERE updated_at > '{{ var("watermark") }}'
```

### Airflow DAG skeleton for ETL

```python
with DAG('etl_orders', schedule_interval='@daily', catchup=False) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)
    extract >> transform >> load
```

## Gotchas

- **Idempotency** is critical: re-running a pipeline must produce the same result. Use `INSERT ... ON CONFLICT` or `MERGE`/`DELETE+INSERT` patterns; never blind `INSERT` for incremental loads
- ETL tools that transform in-memory (pandas) hit RAM limits on large datasets. Use [[apache-spark]] or push transformation to the database (ELT) for tables >1M rows
- Timestamp-based watermarks miss late-arriving data. Consider a lookback window (e.g., `WHERE updated_at > watermark - INTERVAL '1 hour'`)
- Schema drift in source systems silently breaks pipelines. Validate schema at extract time or use schema registries

## See Also

- [[apache-airflow]] - orchestrating ETL/ELT workflows
- [[data-warehouse]] - target storage for transformed data
- [[data-quality]] - validating pipeline output
- https://docs.getdbt.com/docs/introduction - dbt documentation
- https://airflow.apache.org/docs/ - Apache Airflow documentation
