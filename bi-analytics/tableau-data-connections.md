---
title: Tableau Data Connections
category: BI Tools - Tableau
tags: [tableau, data-source, join, union, relation, blending, extract, live, custom-sql, ETL]
---

# Tableau Data Connections

Connection types, data joining strategies, and ETL capabilities within Tableau Desktop and Server.

## Key Facts

- Four connection methods: Tableau Server published sources, local files (Excel/CSV/JSON/PDF), database servers, cloud storage
- Two connection modes: **Live** (query DB on each interaction) and **Extract** (.hyper file snapshot)
- Extract is almost always faster than Live
- Tableau compiles visualizations into SQL queries - can be inspected via Performance Recording or Tableau Log Viewer
- Custom SQL is not optimized by Tableau query compiler - use visual editor for simple operations
- [[tableau-performance-optimization]] depends heavily on connection type choice
- Tableau Prep is a visual ETL tool for data preparation, cleaning, merging before loading into Tableau

## Join Types

| Type | Scope | Use Case |
|------|-------|----------|
| **Join** | Physical table level | Combine tables by matching keys (inner/left/right/full) |
| **Union** | Physical table level | Stack tables vertically (same schema, different data) |
| **Relations** | Logical model level | Smart joins that aggregate at correct detail level during analysis |
| **Blending** | Worksheet level | Combine independent data sources per worksheet |

## Patterns

**Extract optimization settings:**

```
Extract > Edit:
  - Filters (e.g., by region, date range) -> reduce volume
  - Aggregate to visible level -> speed and size
  - Incremental refresh -> update only new rows
  - Hide unused fields -> reduce extract size
  - Physical vs Logical table mode -> affects join timing
```

**Live vs Extract decision:**

```
Use Live when:
  - Data freshness is critical (real-time dashboards)
  - Database is fast and well-indexed
  - Data volume is small

Use Extract when:
  - Dashboard speed is priority
  - Complex calculations needed
  - Multiple joins or large datasets
  - Offline access required
```

**Relations vs Blending:**

```
Relations:
  - Configured at data source level (global)
  - Handles multi-granularity joins automatically
  - Better for related tables with shared keys

Blending:
  - Configured per worksheet (flexible)
  - Works for independent sources needing shared filters
  - Primary source (blue) vs secondary (green) markers
  - Better for "same filter, different data" dashboards
```

**Custom SQL with parameters:**

```sql
-- In Tableau Custom SQL editor:
SELECT * FROM orders
WHERE order_date >= <Parameters.Start Date>
  AND region = <Parameters.Region>
```

**Custom palette in Preferences.tps:**

```xml
<!-- My Tableau Repository/Preferences.tps -->
<workbook>
  <preferences>
    <color-palette name="My Palette" type="regular">
      <color>#1f77b4</color>
      <color>#ff7f0e</color>
      <color>#2ca02c</color>
    </color-palette>
  </preferences>
</workbook>
```

## Gotchas

- **Symptom**: Join produces duplicated rows, metrics are inflated -> **Cause**: Physical join on different granularity (1-to-many) -> **Fix**: Use Relations instead of Joins, or pre-aggregate in SQL
- **Symptom**: Custom SQL runs very slowly in Live mode -> **Cause**: Tableau wraps Custom SQL in subquery, adds its own GROUP BY -> **Fix**: Materialize the query as a view/table in the DB, or use Extract
- **Symptom**: Blending shows NULL for secondary source metrics -> **Cause**: Linking field names don't match between sources -> **Fix**: Rename fields to match, or configure linking via Data > Edit Blend Relationships
- **Symptom**: ClickHouse connection fails out of the box -> **Cause**: No native connector in Tableau -> **Fix**: Use ODBC Driver for ClickHouse or ClickHouse JDBC driver

## See Also

- [[tableau-performance-optimization]] - extract vs live performance implications
- [[lod-expressions-calculated-fields]] - calculations that interact with data granularity
- [[tableau-geo-functions]] - spatial joins
- Tableau connection docs: https://help.tableau.com/current/pro/desktop/en-us/basicconnectoverview.htm
