---
title: Tableau Performance Optimization
category: tools
tags: [bi-analytics, tableau, performance, optimization, extract, query-tuning]
---

# Tableau Performance Optimization

Performance tuning in Tableau spans four layers: server load, data source, calculations, and view-level. The target is initial load < 10 seconds and filter switch < 6 seconds. Use the built-in Performance Recorder to identify bottlenecks.

## Key Facts

- Target performance: primary load < 10 sec, filter change < 6 sec
- Performance Recorder: Help -> Settings and Performance -> Start Performance Recording
- Server: add `?:record_performance=yes` to URL
- Report quality formula: `(Informative content x Credibility x Engagement) / Load time`
- Peak load is non-linear - one heavy report can consume 75% of server CPU
- Solution: optimize individual reports, not just scale the server

## Patterns

### Performance Recording Events

| Event | Description |
|-------|-------------|
| Compiling query | Generating SQL based on filters/calculations |
| Executing query | Sending query to DB or Extract |
| Computing layouts | Computing row-level calculated fields |
| Blending | Data blending operations |
| Geocoding | Placing points on map |
| Table Calculations | Computing table calculations |
| Rendering | Visual rendering |

### Server Load Optimizations

- Fix dashboard sizes for frequently used dashboards (enables caching)
- Delete unused reports, Extracts, and their scheduled refreshes
- Reduce Extract size: Hide unused fields -> recreate Extract
- Remove stale books from scheduled refreshes
- No duplicate books or data sources
- Group individual access permissions (reduces permission checking overhead)

### Data Source Optimizations

- **Extract > Live** in almost all cases (materialized data is faster)
- Avoid Custom SQL in LIVE connections
- Avoid GROUP BY and ORDER BY in Custom SQL
- Use INNER JOIN with Referential Integrity flag enabled
- Reduce row count: aggregate if not visualizing finest granularity
- Non-additive data: store pre-aggregated by scale/slice rather than raw rows
- For cross-granularity data: use Relations over Data Blending (or pre-join in DWH)

### Calculation Optimizations

- Prefer type hierarchy (faster to slower): `Boolean > Numeric > Date > String`
- Use `STARTSWITH` over `CONTAINS` for string matching
- Avoid LOD in complex nested calculations (each adds JOINs)
- Materialize calculated fields in Extract before publishing
- Move complex calculations to data source (SQL/ETL) when possible

### View-Level Optimizations

- Fewer sheets per workbook (>6 -> consider reducing)
- Unique sheets over similar ones (duplicates = redundant queries)
- Each worksheet generates one query to the source
- Minimize marks on a single view (thousands of points = slow rendering)

### Published vs Embedded Extract

- **Published Extract**: shared across workbooks, but loses cache when used with relevant filters
- **Embedded Extract**: embedded in workbook, better cache retention for that specific workbook

### Data Blending Performance

Data Blending is inherently slow - avoid it. It creates multiple queries. Prefer:
1. Relations (Tableau 2020+)
2. Pre-prepared JOINs in the data warehouse
3. Only use Blending when truly independent sources need per-worksheet flexibility

## Gotchas

- Dashboard sizing affects caching: auto-sized dashboards can't be cached as effectively as fixed-size ones
- Hiding unused fields and recreating Extract is a quick win that's often overlooked
- Performance Recorder output shows time per event - focus on the longest bar first
- Extract optimization (filter rows and columns at extract time) reduces file size but is a manual step that's easy to forget
- Custom SQL in Live mode bypasses Tableau's query optimizer entirely

## See Also

- [[tableau-fundamentals]] - Live vs Extract, filter order
- [[tableau-lod-expressions]] - LOD performance implications
- [[tableau-calculations]] - calculation type performance
- [[bi-development-process]] - report quality properties
