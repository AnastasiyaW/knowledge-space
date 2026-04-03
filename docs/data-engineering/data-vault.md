---
title: Data Vault 2.0
category: concepts
tags: [data-engineering, data-vault, data-modeling, dwh, scd2]
---

# Data Vault 2.0

Data Vault is a data modeling methodology designed for agile DWH environments with many sources, frequent schema changes, and audit requirements. It solves the rigidity of 3NF and duplication issues with dimensional modeling.

## Core Table Types

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **Hub** | Business entities (customer, product) | Hash key, business key, load timestamp, source code |
| **Link** | Relationships/transactions between 2+ hubs | Hash key, hub foreign keys, load timestamp, source |
| **Satellite** | Descriptive attributes with SCD2 history | Hub/Link hash key, attributes, valid_from, valid_to, source |

## Key Principles
- Data enters as-is from sources (no business transformation in core)
- Business rules applied only in mart layer
- All tables **append-only** - history tracked via SCD2 in satellites
- **Hash keys** for joins (deterministic, no sequences)
- Separates structure (hubs/links) from content (satellites)

## Advantages
- Easy to add new sources (just add new satellites)
- Full auditability (every change tracked with timestamps and source codes)
- Parallelizable loading (hubs, links, satellites load independently)
- Handles many sources with different schemas
- Resilient to source changes

## Disadvantages
- Complex for direct querying (need hub + satellite + link joins)
- Typically feeds dimensional marts for BI consumption
- SCD2 joins across satellites with different change frequencies = complexity

## SCD2 (Slowly Changing Dimension Type 2)

Tracks historical changes by adding new rows with validity dates:

```sql
customer_id | name    | valid_from | valid_to   | is_current
1           | Alice   | 2023-01-01 | 2023-06-15 | false
1           | Alice B | 2023-06-15 | 9999-12-31 | true
```

When joining satellites from different hubs/links, date ranges must overlap - can cause Cartesian explosion.

## Anchor Modeling

Extreme form of Data Vault where every attribute gets its own table (6NF-like):

| Component | Similar To | Description |
|-----------|-----------|-------------|
| **Anchor** | Hub | Entity identified by surrogate ID |
| **Attribute** | Satellite | Single attribute per table, with timestamp |
| **Tie** | Link | Relationship between anchors |
| **Knot** | Reference | Shared reference data (enums, lookups) |

### Key Differences from Data Vault
- More granular: one attribute = one table (vs satellites grouping attributes)
- Easier schema evolution (add attribute = add table, no ALTER)
- Results in many tables and many JOINs
- Better for environments with frequent schema changes

## Choosing a Methodology

| Methodology | Best For | Trade-off |
|-------------|---------|-----------|
| **3NF (Inmon)** | Enterprise DWH core layer | Complex to query, good for integration |
| **Dimensional (Kimball)** | Marts, BI, fast queries | Denormalized, harder to maintain |
| **Data Vault** | Agile DWH, multiple sources, audit | Complex to query, needs marts on top |
| **Anchor** | Frequently changing schemas | Very many tables, many JOINs |

## Gotchas
- Data Vault adds many joins - mart layer must pre-join for acceptable performance
- SCD2 date range joins across different satellites can produce unexpected Cartesian products
- Hash keys must use consistent hashing across all loading processes
- Without proper mart layer, analysts cannot query Data Vault directly

## See Also
- [[data-modeling]] - normalization fundamentals
- [[dimensional-modeling]] - star/snowflake schemas for marts
- [[scd-patterns]] - slowly changing dimension techniques
- [[dwh-architecture]] - architectural context
