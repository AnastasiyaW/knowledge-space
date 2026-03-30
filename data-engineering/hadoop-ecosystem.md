---
title: Hadoop Ecosystem
category: concepts
tags: [hadoop, hdfs, yarn, mapreduce, hive, big-data, distributed]
---

# Hadoop Ecosystem

Apache Hadoop is a framework for distributed storage and processing of large datasets across clusters of commodity hardware. The ecosystem includes HDFS (storage), YARN (resource management), MapReduce (batch processing), and numerous projects built on top (Hive, Spark, HBase, etc.).

## Key Facts

- **Three core components**: [[hdfs]] (distributed storage), YARN (resource negotiation), [[mapreduce]] (computation model)
- **YARN (Yet Another Resource Negotiator)** replaced MapReduce v1's JobTracker/TaskTracker architecture. Manages cluster resources via containers, not fixed map/reduce slots
  - ResourceManager: cluster-wide resource allocator, works with containers on demand
  - NodeManager: per-node agent managing local resources
  - ApplicationMaster: per-application lifecycle manager (launched by RM, monitors tasks)
- YARN does NOT track task progress directly - it allocates a container for ApplicationMaster, which then manages executors (this is what enabled Spark to run on YARN)
- **Hive**: SQL interface over Hadoop. Translates HiveQL into MapReduce/Tez/Spark jobs. Uses Hive Metastore for schema management (reused by Spark, Presto, Trino)
- **Capacity Scheduler / Fair Scheduler**: YARN schedulers that allow multi-tenant resource sharing. Capacity Scheduler guarantees minimum allocation per queue; Fair Scheduler distributes resources evenly
- Spark has largely replaced MapReduce for processing (10-100x faster due to in-memory computation), but HDFS and YARN remain relevant as storage and resource layers
- Hadoop development complexity is higher than [[apache-spark]]; Spark provides a higher level of abstraction

## Patterns

### Running a Spark job on YARN

```bash
spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --num-executors 10 \
    --executor-memory 4g \
    --executor-cores 2 \
    my_spark_job.py
```

### Hive table over HDFS data

```sql
CREATE EXTERNAL TABLE events (
    event_id    STRING,
    user_id     STRING,
    event_type  STRING,
    created_at  TIMESTAMP
)
STORED AS PARQUET
LOCATION 'hdfs:///data/events/'
PARTITIONED BY (dt STRING);

-- Register existing partitions
MSCK REPAIR TABLE events;
```

### YARN resource allocation

```
ResourceManager (1 per cluster)
    |
    +-- NodeManager (1 per node)
    |       +-- Container (AppMaster for Job 1)
    |       +-- Container (Executor for Job 1)
    |       +-- Container (Executor for Job 2)
    |
    +-- NodeManager (1 per node)
            +-- Container (Executor for Job 1)
            +-- Container (AppMaster for Job 2)
```

## Gotchas

- YARN ResourceManager is NOT the same as old JobTracker. RM only allocates containers; it does not plan or schedule map/reduce tasks (ApplicationMaster does this)
- Do not confuse HDFS replication with backup. HDFS replicates blocks for fault tolerance (default RF=3), but does not protect against accidental deletion or corruption at the file level
- Hadoop ecosystem requires significant ops overhead (ZooKeeper, NameNode HA, capacity planning). Cloud-managed alternatives (EMR, Dataproc, HDInsight) reduce this burden
- Hive Metastore is critical infrastructure even outside Hadoop - it powers schema management for Spark, Presto/Trino, and lake table formats

## See Also

- [[hdfs]] - distributed file system details
- [[mapreduce]] - programming model
- [[apache-spark]] - modern replacement for MapReduce processing
- https://hadoop.apache.org/docs/stable/ - Apache Hadoop documentation
