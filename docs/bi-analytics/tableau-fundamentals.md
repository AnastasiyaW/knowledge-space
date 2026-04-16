---
title: Tableau Fundamentals
category: tools
tags: [bi-analytics, tableau, data-connections, joins, extract, live]
---

# Tableau Fundamentals

Tableau is an enterprise BI platform (Desktop + Server/Cloud) with the most powerful visualization engine in the BI market. This entry covers data connections, join types, filter order, and core architecture concepts.

## Key Facts

- Tableau connects via: Tableau Server (published sources), Files (Excel/CSV/JSON/PDF), Server/Database (200+ native connectors), Cloud storage
- Two connection modes: Live (real-time queries) and Extract (`.hyper` snapshot file)
- Visual indicator: Live = one barrel icon, Extract = two barrels
- Custom SQL available but Tableau does NOT optimize it before sending to DB
- ClickHouse not natively supported - requires ODBC or JDBC driver
- Ecosystem: Tableau Prep (visual ETL), Tableau Catalog (data governance), Data Management Add-on

## Patterns

### Live vs Extract

**Live mode**: every worksheet action sends a query to the database. Always fresh data, performance depends on DB speed.

**Extract mode**: data snapshot saved as `.hyper` file with high compression. Stored in `Datasources` folder.

Extract settings:
- Logical vs physical table mode
- Filters (e.g., by city or geo)
- Aggregation at extract level (optimizes speed and size)
- Row limit
- **Incremental refresh** - refresh only new data
- **Hide all unused fields** - removes unused fields for optimization

**Rule**: Extract > Live in almost all cases (materialized data is faster).

### Custom SQL vs Visual Editor

Custom SQL pros: quick ad-hoc source creation; can embed parameters.

Custom SQL cons:
- No syntax highlighting in editor
- Transformation invisible to team members
- Tableau does NOT optimize Custom SQL before sending to DB
- Avoid GROUP BY and ORDER BY in Custom SQL

**Rule**: for simple operations, use the visual editor. Use Custom SQL only when flexibility is truly needed.

### Table Combining Methods

**Join**: standard relational join. Auto-creates join on same-name fields. Types: inner, left, right, full outer.
- Logical join: Tableau joins first, then creates Extract (data merged, then snapshot)
- Physical join: Extract per table, then joins on query

**Union**: stack tables with identical schema. Supports auto-union by sheet/table name pattern.

**Relations** (Tableau 2020+): analyze data across tables at different granularities. Relations join and aggregate during analysis at the required detail level. Resolves data duplication without LOD calculations.

For date granularity mismatch (orders by day, plan by month):
```sql
DATE(DATETRUNC("month", [Order Date]))
```

**Blending**: mix data from different sources per worksheet. Primary source = first field dragged; secondary source = marked with different color.

When to use Blending over Relations:
1. Need per-worksheet flexibility (Blending = per sheet, Relations = per data source)
2. Two independent sources, no cross-calculations needed, but want one filter to control both

**Data Blending = performance issue**: creates multiple queries; avoid when possible.

### Filter Order of Operations

Filters apply in this order (critical for LOD calculations):

1. Extract Filters
2. Data Source Filters
3. Context Filters
4. Dimension Filters (includes: Sets, conditional, Top N, **FIXED LOD**)
5. Measure Filters (includes: **INCLUDE/EXCLUDE LOD**, Data Blending)
6. Table Calculation Filters (includes: forecasts, table calcs, clusters, totals)

### Row/Column Security

**Row Level Security (RLS)**: show different rows to different users.
- Built-in: Server tab -> create user filters, assign users to regions
- Scalable: access table (user + region pairs), physical join with fact table, filter where `regional_manager = USERNAME()`

**Column Level Security**: show different dimensions to different user groups.

**Important**: RLS requires physical JOIN (not logical) to avoid data explosion.

## Gotchas

- Relations are preferred over Blending for cross-granularity data (or pre-join in DWH)
- FIXED LOD evaluates at context filter level (step 4), INCLUDE/EXCLUDE at dimension filter level (step 5) - this distinction matters for dashboard behavior
- Custom SQL in LIVE connections is especially problematic for performance
- Each worksheet generates one query to the source - more sheets = more queries
- Published Extract loses cache when used with relevant filters; Embedded Extract has better cache retention

## See Also

- [[tableau-calculations]] - calculated fields and table calculations
- [[tableau-lod-expressions]] - FIXED/INCLUDE/EXCLUDE detail
- [[tableau-performance-optimization]] - performance tuning
- [[bi-tools-comparison]] - Tableau vs Power BI vs alternatives
