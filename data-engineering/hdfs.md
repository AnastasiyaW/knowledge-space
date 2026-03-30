---
title: HDFS (Hadoop Distributed File System)
category: concepts
tags: [hdfs, hadoop, distributed-storage, namenode, datanode, replication]
---

# HDFS (Hadoop Distributed File System)

HDFS is a distributed file system designed to store very large files across a cluster of commodity machines. It provides high throughput access to application data and is the default storage layer for the [[hadoop-ecosystem]].

## Key Facts

- **NameNode**: master server storing filesystem metadata (file-to-block mapping, block locations, permissions). Does NOT store actual data. Single point of failure in non-HA setups
- **DataNode**: worker server storing actual data blocks. Sends periodic **heartbeats** to NameNode reporting status and block lists
- **Secondary NameNode**: creates fresh checkpoints of filesystem metadata (merges edit log with fsimage). NOT a hot standby - does not take over if NameNode fails
- **Standby NameNode** (HA mode): true failover partner. Uses shared edit log (JournalNodes or NFS) for continuous synchronization
- Default block size: **128 MB** (configurable per file). Block size can be set at write time
- Default **replication factor**: 3. Each block is replicated to 3 different DataNodes. Can be configured per file (not just globally)
- A 2 GB file with RF=3 occupies **6 GB** of physical disk across the cluster
- HDFS is optimized for **throughput over latency** (large sequential reads, not random access)
- NOT POSIX-compatible. Does not support in-place file modification (append-only, write-once-read-many)
- **Small files problem**: millions of small files consume excessive NameNode memory (each file/block = ~150 bytes of metadata). Combine small files with HAR (Hadoop Archive) or SequenceFiles

## Patterns

### Basic HDFS operations

```bash
# List files
hdfs dfs -ls /data/

# Upload local file to HDFS
hdfs dfs -put localfile.csv /data/input/

# Download from HDFS
hdfs dfs -get /data/output/result.parquet ./

# Set replication factor for a specific file
hdfs dfs -setrep 2 /data/temp/scratch.csv

# Check filesystem health
hdfs fsck /data/ -files -blocks -locations
```

### Block distribution across DataNodes

```
File: /data/events.parquet (384 MB, RF=3)

Block 0 (128 MB): DataNode-1, DataNode-3, DataNode-5
Block 1 (128 MB): DataNode-2, DataNode-4, DataNode-1
Block 2 (128 MB): DataNode-3, DataNode-5, DataNode-2
```

### NameNode HA architecture

```
NameNode (Active)  <--->  JournalNodes (3+)  <--->  NameNode (Standby)
        |                                                  |
   DataNode-1   DataNode-2   DataNode-3   DataNode-4
   (heartbeats to both NameNodes)
```

## Gotchas

- NameNode restart requires loading entire metadata into RAM - can take minutes on large clusters. Size the NameNode with enough memory (1 GB heap per million blocks as rough estimate)
- DataNode heartbeat interval is 3 seconds by default; NameNode marks a DataNode dead after 10 missed heartbeats (~30s). Under-replication triggers automatic re-replication
- HDFS is not suitable for workloads requiring low-latency random reads/writes. Use HBase (on top of HDFS) or a different storage system for such patterns
- Block size is NOT the minimum file size. A 1 KB file still creates one block but consumes only 1 KB of disk + metadata overhead

## See Also

- [[hadoop-ecosystem]] - HDFS's role in the broader ecosystem
- [[data-lake]] - HDFS as on-prem data lake storage
- [[data-formats]] - Parquet/ORC for efficient HDFS storage
- https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html - HDFS architecture documentation
