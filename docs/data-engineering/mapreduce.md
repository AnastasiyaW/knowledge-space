---
title: MapReduce
category: concepts
tags: [data-engineering, mapreduce, hadoop, distributed-computing, batch]
---

# MapReduce

MapReduce is a programming model for distributed data processing. Two user-defined operations: Map (transform/filter) and Reduce (aggregate). The framework guarantees all records with the same key arrive at the same Reducer.

## Paradigm

```
Map:    (K1, V1) -> list(K2, V2)    -- transform each record
Reduce: (K2, list(V2)) -> list(K3, V3)  -- aggregate by key
```

## Execution Pipeline

```
Input -> Split -> Map -> Spill -> Sort/Merge -> Shuffle -> Reduce -> Output
```

1. **Split:** InputFormat splits data into chunks. Each split -> one Mapper
2. **Map:** Each Mapper processes split via RecordReader. Output to circular buffer
3. **Spill:** Buffer fills -> data spilled to local disk (NOT HDFS). Partitioned by `hash(key) % numReducers`
4. **Sort/Merge:** Mapper sorts and merge-sorts spill files per Reducer partition
5. **Shuffle:** Reducers **pull** data from Mappers (v2 reversed direction from v1)
6. **Reduce:** Merge-sort received files, process sorted key-value stream
7. **Output:** One output file per Reducer on HDFS

## Hadoop Streaming (Python)

```bash
hadoop jar $HADOOP_MAPRED_HOME/hadoop-streaming.jar \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /local/path/mapper.py \
  -file /local/path/reducer.py \
  -input /hdfs/input/ \
  -output /hdfs/output/
```

## Key Details
- **Split != HDFS block:** Splits are logical (can be from DB, S3); blocks are physical
- **InputFormat types:** TextInputFormat (default), NLineInputFormat (N lines per mapper), DBInputFormat
- **Number of Mappers:** determined by InputFormat split logic, not directly configurable
- **Number of Reducers:** configurable via `mapreduce.job.reduces`
- **`_SUCCESS` file:** empty marker indicating job completion. Files starting with `_` or `.` ignored by subsequent jobs
- **Output directory must NOT exist** before job launch (safety against overwriting)

## MapReduce v1 vs v2
- **v1:** Mappers pushed data to Reducers -> DDoS on Reducers
- **v2:** Reducers pull from Mappers (reversed direction)

## Gotchas
- Container initialization overhead dominates for small datasets (40s for 100KB with 31 mappers vs 9s with 3)
- Split is NOT the same as HDFS block - different abstraction layers
- Hadoop Streaming (Python) lacks some Java MR features (no setup/cleanup hooks)
- MapReduce is legacy - prefer Spark for new workloads

## See Also
- [[hadoop-hdfs]] - storage layer
- [[yarn-resource-management]] - resource allocation
- [[apache-hive]] - SQL interface to MapReduce
- [[apache-spark-core]] - modern replacement
