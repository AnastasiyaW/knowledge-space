---
title: B-Tree and Index Internals
category: concepts
tags: [sql-databases, btree, b-plus-tree, index, page-split, uuid, clustered-index, bloom-filter]
---

# B-Tree and Index Internals

B+Trees are the backbone of database indexing in all major RDBMS. Understanding their structure explains why some queries are fast and others are not, and why primary key choice matters enormously.

## B-Tree vs B+Tree

**B-Tree:** Internal nodes store both keys AND values (data pointers). Data can be found at any level.

**B+Tree (used by all major RDBMS):** Only leaf nodes store values. Internal nodes contain only keys for navigation. Leaf nodes linked as doubly-linked list.

**B+Tree advantages:**
- More keys per internal node (no data) = shallower tree = fewer I/Os
- Range queries: follow leaf linked list (sequential I/O)
- Predictable I/O cost: all data at same depth
- Better cache utilization: small internal nodes more likely cached

**Quantified:** 8KB page with 100-byte keys = ~80 keys per internal node. 3-level B+Tree: 80^3 = 512,000 leaf pages reachable in 3 I/Os.

## Clustered vs Non-Clustered Indexes

**MySQL InnoDB:** Primary key IS the clustered index. Data physically sorted by PK. Secondary indexes store PK value as row locator - requires double lookup (secondary index -> find PK -> clustered index -> row).

**PostgreSQL:** No clustered indexes by default. All indexes point directly to `ctid` (page, offset) in heap. Any tuple move (UPDATE, VACUUM) invalidates ctid, requiring index update.

**SQL Server:** One clustered index per table (PK by default). Non-clustered index leaf = RID for heaps, or clustered key for clustered tables.

## Page Splits

When inserting into a full leaf page, a page split occurs: page divided, entries redistributed, parent nodes updated. Most expensive index operation.

**Sequential inserts** (auto-increment, UUID v7/ULID): Always go to rightmost leaf. Minimal splits, sequential I/O, excellent cache hit ratio.

**Random inserts** (UUID v4): Each insert targets random leaf page. Frequent splits, random I/O, buffer pool thrashing.

## UUID v4 vs Ordered IDs

Random UUIDs cause:
- Frequent page splits (entries rarely append to end)
- Random I/O patterns (pages from all over disk)
- Buffer pool thrashing (pages evicted then needed again)
- Poor cache utilization

**Shopify case study:** Switched from UUID v4 to ULID. Purchase-related queries are naturally time-ordered, so both reads and writes improved.

**MySQL caveat:** ALL secondary indexes store the PK. Random UUID PK spreads randomness across every secondary index.

**When randomness doesn't hurt:** PostgreSQL heap tables without clustered indexes - random values just append to heap end. The problem is in index maintenance.

## Bloom Filters

Probabilistic data structure: "possibly exists" or "definitely does not exist." Zero false negatives, possible false positives.

```
Hash(value) % array_size = bit position
Bit = 0 -> definitely absent
Bit = 1 -> might exist (could be collision)
```

Use case: check username availability without DB query. False positives cause unnecessary lookups but no correctness issues. Multiple hash functions reduce false positive rate.

## Key Facts

- B+Tree fanout: 8KB page / key size = keys per node. More fanout = shallower tree
- PostgreSQL 13+ added B-tree deduplication (multiple duplicate keys in single leaf)
- Fill factor < 100% reserves space for future inserts, reducing splits
- `REINDEX CONCURRENTLY` rebuilds index without blocking writes
- Index fragmentation from page splits degraded performance - REBUILD or REORGANIZE to fix

## Gotchas

- Small tables (< 1 page): index scan slower than sequential scan (optimizer overhead)
- Functions on indexed columns disable index use: `WHERE YEAR(col) = 2024` cannot use index on `col`
- UUID v4 as InnoDB PK: worst case for both clustered and all secondary indexes
- PostgreSQL weak lock fast-path: 16 slots per backend - heavily partitioned tables can exceed this

## See Also

- [[index-strategies]] - composite, covering, partial indexes
- [[database-storage-internals]] - pages, heaps, I/O
- [[schema-design-normalization]] - primary key strategy choice
- [[query-optimization-explain]] - how optimizer chooses between index types
