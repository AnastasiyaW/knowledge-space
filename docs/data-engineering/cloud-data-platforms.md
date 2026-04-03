---
title: Cloud Data Platforms
category: tools
tags: [data-engineering, cloud, aws, gcp, snowflake, bigquery, s3]
---

# Cloud Data Platforms

Cloud platforms separate compute from storage, enabling elastic scaling and pay-per-use pricing. The "Big Three" (AWS, GCP, Azure) plus Snowflake provide the foundation for modern data engineering.

## Service Model Comparison

| On-Premise | AWS | GCP | Purpose |
|-----------|-----|-----|---------|
| HDFS | S3 | Cloud Storage | Object storage |
| Spark | EMR | Dataproc | Distributed compute |
| Kafka | MSK / Kinesis | Pub/Sub | Event streaming |
| PostgreSQL | RDS | Cloud SQL | Managed RDBMS |

## Cloud DWH Options

| System | Type | Key Feature |
|--------|------|-------------|
| **Athena** | Query service | Managed Presto, queries S3 without loading |
| **Redshift** | MPP DWH | Closest to Greenplum architecture |
| **BigQuery** | Serverless DWH | No compute control - true serverless |
| **Snowflake** | Separated compute/storage | Spins up clusters per query, data in S3 |
| **Presto/Trino** | Federated query engine | Queries data in source systems without ETL |

## S3 - Simple Storage Service
- 5-10x cheaper than HDFS
- 99.999999999% durability (11 nines)
- Practically unlimited elasticity
- Separates storage from compute
- Access via `boto3` (Python), CLI, or Spark (`s3a://`)

## Cloud Service Models for DE

| Approach | Examples | DE Responsibility |
|----------|---------|-------------------|
| **IaaS** | Self-managed ClickHouse on VMs | OS, database, monitoring, backups |
| **PaaS** | Managed ClickHouse, RDS | Service configuration |
| **SaaS** | BigQuery, Snowflake | Query writing only |

## Snowflake Architecture
- Three layers: Storage, Compute, Services
- No direct access to storage layer
- Automatic micro-partitioning
- Virtual clusters (warehouses) for different workloads
- Pay per query compute time

## VM and Disk Best Practices

**Disk performance scales with size (QoS).** A 50GB SSD may be slow because IOPS are throttled proportionally. Fix: increase disk size for more IOPS.

| Disk Type | Best For |
|-----------|---------|
| HDD | Cheapest, archives |
| SSD | Dev/test (cost-effective) |
| High-IOPS SSD | Production workloads |
| Local NVMe | Maximum performance, no replication |

## Cost Management
- **Always pause/stop** unused VMs, databases, K8s clusters
- Transient clusters for one-off jobs - create, use, destroy
- HDD for dev/test, SSD for staging, High-IOPS for production
- Monitor QoS limits - small disks have lower IOPS quotas

## Cloud-Native Data Pattern
```
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto run here)
```
Separation enables elastic compute independent of storage.

## Gotchas
- Redshift nodes include compute + storage by default; Snowflake separates natively
- Vertical scaling requires VM restart (downtime)
- Always configure firewall - any VM with public IP is a target
- Network latency kills cross-datacenter cluster performance with synchronous replication
- BigQuery: no compute control means unexpected costs on complex queries

## See Also
- [[dwh-architecture]] - DWH design context
- [[kubernetes-for-de]] - compute orchestration
- [[docker-for-de]] - containerization basics
- [[data-lake-lakehouse]] - lakehouse on cloud
