---
title: Greenplum and MPP Databases
category: concepts
tags: [greenplum, mpp, distributed-database, parallel-query, vertica, redshift]
---

# Greenplum and MPP Databases

MPP (Massively Parallel Processing) databases distribute data and query execution across multiple nodes to process analytical workloads at scale. Greenplum is a PostgreSQL-based open-source MPP database; Vertica, Amazon Redshift, and Azure Synapse are commercial alternatives.

## Key Facts

- **MPP architecture**: a coordinator node (master) distributes queries to segment nodes (workers). Each segment processes its local data partition in parallel, results are aggregated at the master
- **Greenplum** is built on PostgreSQL, so most PG SQL syntax works. Adds: distributed tables, parallel query execution, resource queues, external tables (gpfdist)
- **Distribution policies**: how data is spread across segments
  - `DISTRIBUTED BY (column)` - hash distribution on a column. Choose high-cardinality column to avoid skew
  - `DISTRIBUTED RANDOMLY` - round-robin. Good when no obvious distribution key
  - `DISTRIBUTED REPLICATED` - full copy on every segment. For small dimension tables (broadcast join)
- **Interconnect**: high-speed network between segments for data redistribution during JOINs and aggregations
- **Resource queues/groups**: manage concurrent query workloads. Prevent one heavy query from starving others
- **gpfdist**: parallel file distribution utility. Streams external files to all segments simultaneously for fast bulk loading
- Greenplum and similar MPP databases are used as on-prem [[data-warehouse]] engines. Cloud equivalents: Redshift (AWS), BigQuery (GCP), Synapse (Azure)

## Patterns

### Greenplum table creation

```sql
CREATE TABLE fact_orders (
    order_id     BIGINT,
    customer_id  INT,
    order_date   DATE,
    total_amount NUMERIC(12,2)
)
DISTRIBUTED BY (customer_id)
PARTITION BY RANGE (order_date)
    (START ('2025-01-01') END ('2027-01-01') EVERY (INTERVAL '1 month'));
```

### Loading with gpfdist

```bash
# Start gpfdist on the load server
gpfdist -d /data/files -p 8080 &

# Create external table pointing to gpfdist
CREATE EXTERNAL TABLE ext_orders (
    order_id     BIGINT,
    customer_id  INT,
    order_date   DATE,
    total_amount NUMERIC(12,2)
)
LOCATION ('gpfdist://loadserver:8080/orders*.csv')
FORMAT 'CSV' (HEADER);

-- Load into target table
INSERT INTO fact_orders SELECT * FROM ext_orders;
```

### Airflow integration

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

pg_hook = PostgresHook(postgres_conn_id='conn_greenplum_write')
conn = pg_hook.get_conn()
cursor = conn.cursor()
cursor.execute("INSERT INTO target_table SELECT * FROM staging_table")
conn.commit()
```

## Gotchas

- **Data skew** is the #1 performance killer in MPP. If distribution key has low cardinality or uneven distribution, one segment does most of the work while others idle. Check with `SELECT gp_segment_id, COUNT(*) FROM table GROUP BY 1`
- JOINing two tables distributed on different keys requires data redistribution (shuffle). Distribute frequently joined tables on the same key
- Greenplum uses PostgreSQL hooks in Airflow (`PostgresHook`), but connection strings differ (default port 5432 vs Greenplum's typical 5432/6432)
- `VACUUM` and `ANALYZE` are critical for Greenplum performance. Unlike single-node PG, these operations run in parallel across all segments
- MPP databases are not good at point queries (single-row lookup by PK). They excel at full table scans with aggregations

## See Also

- [[data-warehouse]] - MPP databases as DWH engines
- [[partitioning-and-sharding]] - data distribution strategies
- [[postgresql-for-data-engineering]] - base PostgreSQL knowledge
- https://docs.vmware.com/en/VMware-Greenplum/ - Greenplum documentation
- https://docs.aws.amazon.com/redshift/ - Amazon Redshift documentation
