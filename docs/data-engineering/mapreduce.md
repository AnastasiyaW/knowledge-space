---
title: MapReduce
category: concepts
tags: [mapreduce, hadoop, distributed-processing, batch, map, reduce, shuffle]
---

# MapReduce

MapReduce is a programming model for processing large datasets in parallel across a distributed cluster. It breaks computation into two phases: Map (transform/filter) and Reduce (aggregate), with an implicit Shuffle-Sort step in between.

## Key Facts

- Created at Google (2004 paper), implemented in [[hadoop-ecosystem]]
- Processes data as **key-value pairs** throughout all phases
- **Map phase**: each mapper receives an input split (not a full HDFS block; splits can differ from blocks), applies a function to each record, emits (key, value) pairs
- **Shuffle-Sort phase** (between Map and Reduce): framework sorts mapper output by key, partitions keys across reducers, copies data from mappers to reducers. Often the most resource-intensive phase
- **Reduce phase**: each reducer receives all values for a specific key group, applies aggregation function, writes output
- **Guarantee**: all values with the same key go to the same reducer; data arrives at reducer pre-sorted by key
- **Partitioner** determines which reducer gets which key (default: hash(key) % num_reducers). Custom partitioners enable skew-aware distribution
- **Combiner**: optional local aggregation on the mapper side before shuffle (mini-reducer). Reduces network transfer. Must be commutative and associative (e.g., sum, count, max - but NOT average)
- MapReduce writes intermediate results to disk after each phase, making it slow compared to [[apache-spark]] which keeps data in memory
- Largely replaced by Spark for most workloads, but still runs under the hood in legacy Hive queries

## Patterns

### Word count (canonical example)

```python
# Mapper
def mapper(key, value):
    # key = line offset, value = line of text
    for word in value.split():
        emit(word.lower(), 1)

# Reducer
def reducer(key, values):
    # key = word, values = iterator of counts
    emit(key, sum(values))

# Combiner (same as reducer for sum)
combiner = reducer
```

### MapReduce execution flow

```
Input Splits                                   Output
    |                                             ^
    v                                             |
[Mapper 1] --+                           +-- [Reducer 1]
[Mapper 2] --+--> Shuffle-Sort-Copy -->--+-- [Reducer 2]
[Mapper 3] --+                           +-- [Reducer 3]

Within Shuffle:
  1. Mapper output partitioned by key (Partitioner)
  2. Each partition sorted by key
  3. Spilled to local disk (if memory exceeded)
  4. Reducers copy their partitions from all mappers
  5. Merge-sort on reducer side
```

### Hadoop Streaming (Python)

```bash
hadoop jar hadoop-streaming.jar \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /data/input/ \
    -output /data/output/
```

## Gotchas

- Combiner is NOT guaranteed to run. It is an optimization hint - the framework may skip it, run it once, or run it multiple times. Logic must be associative and commutative
- MapReduce does NOT send mapper output to reducers. In Hadoop v2/YARN, reducers pull data from mappers (preventing DDoS of reducers that happened in v1)
- Data skew: if one key has disproportionately many values, its reducer becomes a bottleneck. Solutions: salted keys, two-pass aggregation, custom partitioner
- Intermediate disk I/O between stages is the primary reason MapReduce is 10-100x slower than [[apache-spark]] for iterative algorithms

## See Also

- [[hadoop-ecosystem]] - MapReduce within the broader Hadoop stack
- [[apache-spark]] - in-memory replacement for MapReduce
- [[hdfs]] - storage layer MapReduce reads from
- https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html
