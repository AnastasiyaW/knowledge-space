---
title: YARN Resource Management
category: tools
tags: [data-engineering, yarn, hadoop, resource-management, cluster]
---

# YARN Resource Management

YARN (Yet Another Resource Negotiator) replaced Hadoop v1's monolithic JobTracker with a distributed resource management architecture. It separates resource allocation from job coordination.

## Evolution from Hadoop v1

**v1 (JobTracker/TaskTracker):**
- JobTracker: single coordinator for ALL jobs - submission, monitoring, resources
- TaskTracker: per-node, rigid Map/Reduce slots
- **Problem:** JobTracker = single point of failure. At scale, DDoS-ed by status updates

**v2+ (YARN):**
- **ResourceManager (RM):** manages cluster resources via abstract containers
- **NodeManager:** per-node agent, reports status to RM
- **ApplicationMaster (AM):** per-job coordinator. Manages its own tasks
- **Container:** isolated Java process with allocated CPU + RAM

**Key improvement:** RM only allocates containers. AM handles job-specific logic. Distributes the centralized load that killed JobTracker.

## Queue Configuration

```
root
  |-- engineering (40%)
  |-- marketing (30%)
  |-- support (30%)
```

Each queue has minimum guaranteed resources, maximum cap, ability to borrow from less-loaded queues.

## Scheduler Types

| Scheduler | Behavior | Trade-off |
|-----------|----------|-----------|
| **FIFO** | Strict sequential | Rarely used |
| **Capacity** | Parallel if resources available | Default in many distros |
| **Fair** | Preempts running jobs for new ones | Best utilization, but wastes work |

**Fair Scheduler gotcha:** preemption kills containers near completion, causing wasted work.

## Key Facts
- Containers can run anything: MapReduce, Spark, HTTP servers
- ResourceManager does NOT track individual task progress - only AM does
- Time-based scheduling possible (90% to ETL at night, more to analytics by day)
- Queue-level priorities configured per-queue

## Gotchas
- Fair Scheduler preemption can kill nearly-completed tasks
- Container initialization overhead dominates for small data
- YARN replaced rigid Map/Reduce slots with flexible containers
- RM is still a potential SPOF - use HA configuration

## See Also
- [[hadoop-hdfs]] - storage layer
- [[mapreduce]] - processing paradigm
- [[apache-spark-core]] - Spark on YARN
- [[kubernetes-for-de]] - modern alternative for resource management
