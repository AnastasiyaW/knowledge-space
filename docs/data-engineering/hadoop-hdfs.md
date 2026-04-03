---
title: Hadoop and HDFS
category: tools
tags: [data-engineering, hadoop, hdfs, distributed-storage, big-data]
---

# Hadoop and HDFS

Hadoop is a framework for distributed storage and processing of large datasets. HDFS (Hadoop Distributed File System) provides fault-tolerant storage across commodity hardware.

## Hadoop Architecture

```
Application Layer: MapReduce | Spark | Tez | Hive | Pig
Resource Layer:    YARN (Resource Management)
Storage Layer:     HDFS (Distributed File System)
```

**Ecosystem tools:** Ambari (management UI), ZooKeeper (coordination), Sqoop/Flume (ingestion), Oozie (scheduling), HBase (NoSQL), Mahout (ML).

## HDFS Architecture

```
Client -> NameNode (Active) -- Standby NameNode (HA)
              |                 Secondary NameNode (checkpoints)
    +---------+---------+
    DN1     DN2     DN3     (DataNodes)
```

| Component | Role |
|-----------|------|
| **NameNode** | Stores metadata - file locations, block locations, permissions. Does NOT store data |
| **DataNode** | Stores data blocks on local disk |
| **Secondary NameNode** | Merges edit logs with checkpoint. NOT a failover |
| **Standby NameNode** | HA failover for Active NameNode |

**Critical:** If all NameNodes lost, HDFS data becomes inaccessible (metadata gone).

## Block Storage

- Default block size: **128 MB** (configurable per file)
- Default replication factor: **3** (each block on 3 DataNodes)
- Disk usage: 2 GB file with replication 3 = **6 GB** physical
- **Rack awareness:** replicate to different racks for fault tolerance

## HDFS Properties

| Property | Detail |
|----------|--------|
| Append-only | Files cannot be modified after write |
| Optimized for throughput | At expense of latency |
| Not POSIX-compliant | Different semantics than local FS |
| Configurable per-file | Block size and replication factor |

## Small Files Problem

10M files totaling 1 GB: each file = 1 block. NameNode stores ~150 bytes metadata per block. 10M * 150 bytes = ~1.5 GB metadata > actual data.

**Solutions:** Combine into larger files (SequenceFiles, HAR archives).

## HDFS Commands

```bash
hadoop fs -ls /path                # list files
hadoop fs -put local.txt /hdfs/    # upload
hadoop fs -get /hdfs/file.txt ./   # download
hadoop fs -cat /hdfs/file.txt      # view content
hadoop fs -text /hdfs/file.txt     # view (handles compression)
hadoop fs -mkdir /hdfs/dir         # create directory
hadoop fs -rm -r /hdfs/output/     # delete recursively
hdfs dfsadmin -report              # cluster health
hdfs fsck file -files -blocks -locations  # check blocks

# Custom block size and replication
hadoop fs -D dfs.blocksize=67108864 -D dfs.replication=2 -put file.txt /hdfs/
```

## DataNode Heartbeats
- DataNodes periodically send heartbeats TO NameNode (not reverse)
- Missing heartbeats trigger NameNode check, then re-replication
- DataNode knows its blocks and checksums, but NOT which files they belong to

## Data Locality Principle
Move computation to data, not data to computation. Avoids network bottleneck. This is why functional patterns (map, reduce, filter) dominate in big data.

## Big Data 5V

| V | Meaning |
|---|---------|
| **Volume** | Data size (TB, PB) |
| **Velocity** | Processing speed requirement |
| **Value** | Business significance |
| **Veracity** | Data trustworthiness |
| **Variety** | Data type diversity |

## Gotchas
- HDFS splits != HDFS blocks: splits are logical (MapReduce), blocks are physical
- Small files are problematic - NameNode memory overhead
- `hadoop distcp` for S3-to-HDFS copying (distributed copy via MR)
- S3 is 5-10x cheaper than HDFS and practically unlimited

## See Also
- [[mapreduce]] - processing paradigm
- [[yarn-resource-management]] - cluster resource management
- [[apache-hive]] - SQL on Hadoop
- [[hbase]] - NoSQL on HDFS
- [[file-formats]] - Parquet, ORC, Avro
