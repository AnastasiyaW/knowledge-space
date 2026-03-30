---
title: Tableau Performance Optimization
category: BI Tools - Tableau
tags: [tableau, performance, optimization, extract, query, rendering, performance-recording, filters, order-of-operations]
---

# Tableau Performance Optimization

Techniques for diagnosing and fixing slow Tableau dashboards. Covers the full optimization stack: data sources, calculations, filters, and rendering.

## Key Facts

- Target: initial load < 10 seconds, filter switch < 6 seconds
- Performance Recording: Help > Settings and Performance > Start Performance Recording
- On Tableau Server: append `?:record_performance=yes` to dashboard URL
- Tableau Log Viewer (github.com/tableau/tableau-log-viewer) parses Desktop logs for query analysis
- Peak load from individual reports can consume up to 75% of server CPU
- [[tableau-data-connections]] choice (Live vs Extract) has the biggest impact on speed
- [[lod-expressions-calculated-fields]] have significant performance implications

## Order of Operations (Filter Hierarchy)

```
1. Extract Filters            <- fastest, reduces data at source
2. Data Source Filters         <- applied before query
3. Context Filters             <- create temporary table
4. Sets, conditional, Top N, FIXED LOD
5. Dimension Filters
6. INCLUDE/EXCLUDE LOD, Data Blending
7. Measure Filters
8. Forecasts, Table Calcs, Clusters, Totals
9. Trend Lines, Reference Lines
10. Table Calc Filters          <- slowest, applied last

Rule: move filters UP the hierarchy for better performance
```

## Performance Recording Events

| Event | What Tableau Does | Optimization Target |
|-------|------------------|---------------------|
| Compiling query | Generates SQL from filters + calcs | Simplify calculations, reduce filters |
| Executing query | Sends query to DB/extract | Optimize data source, indexes |
| Computing layouts | Row-level calculated fields | Simplify formulas |
| Blending | Merges blended data sources | Replace with Relations or pre-joined tables |
| Geocoding | Places points on map | Filter data before geocoding |
| Table Calculations | Computes table calcs | Simplify nested calcs |
| Rendering | Draws visual elements | Reduce marks count |

## Patterns

**Data source optimization:**

```
Extract settings:
  [ ] Hide all unused fields -> recreate extract
  [ ] Apply extract filters (date range, region)
  [ ] Aggregate to visible granularity level
  [ ] Use incremental refresh for large datasets
  [ ] Materialize calculated fields in extract

Live connection:
  [ ] Avoid Custom SQL in LIVE mode
  [ ] Avoid GROUP BY / ORDER BY in Custom SQL
  [ ] Enable referential integrity for INNER JOINs
  [ ] Use Relations instead of Data Blending
  [ ] Pre-aggregate in database views/materialized tables
```

**Calculation optimization:**

```
Prefer built-in features over calculated fields:
  - Grouping / Sets instead of IF/CASE
  - Bins instead of calculated ranges
  - Field formatting instead of DATENAME()
  - Aliases instead of new dimensions

Performance tips:
  - DATEPART() > DATENAME() (numeric > string)
  - STARTSWITH() > CONTAINS() (faster string match)
  - ELSEIF > ELSE IF (single vs nested evaluation)
  - MIN()/MAX() > ATTR() (simpler aggregation)
  - FIND() > CONTAINS() (returns position, more flexible)
  - Put most probable IF branches first
  - Stay at row level as long as possible

AVOID:
  - NOW() and TODAY() - blocks Query Fusion, prevents materialization
  - Nested Table Calculations on large datasets
  - LOD in complex calculations (generates extra JOINs)
```

**Filter optimization:**

```
  [ ] Limit to 5 filters per dashboard
  [ ] Use continuous date filters over discrete
  [ ] Avoid "Only Relevant Values" on large tables
  [ ] Replace runtime USERNAME()/ISMEMBEROF() filters where possible
  [ ] Use Relative Date Filter instead of TODAY()-based calc
  [ ] Replace filters with Filter Actions for drill-down
  [ ] Create separate (small) data source for filter value lists
```

**Rendering optimization:**

```
  [ ] Limit marks count per view
  [ ] Use JPEG custom shapes, not PNG
  [ ] Avoid large tables with low granularity
  [ ] Limit tooltip content (Viz in Tooltip renders on hover)
  [ ] Use Hidden Containers for drill-down views
  [ ] Fix dashboard size for caching
  [ ] Show TOP-N records in tables, not full data
```

## Gotchas

- **Symptom**: Multiple sequential "Executing query" events -> **Cause**: Too many visualizations OR TODAY()/NOW() blocking Query Fusion -> **Fix**: Reduce sheet count, replace NOW() with parameter
- **Symptom**: Extract refresh takes hours -> **Cause**: Full extract of huge table -> **Fix**: Use incremental refresh, filter extract, aggregate to needed granularity
- **Symptom**: Data Blending is extremely slow -> **Cause**: Blending filters all secondary data per primary row -> **Fix**: Replace with Relations, or pre-join in SQL
- **Symptom**: Published Extract slower than Embedded -> **Cause**: "Relevant filters" invalidate cache on published extracts -> **Fix**: Use embedded extracts or remove relevant-value filters

## See Also

- [[tableau-data-connections]] - Live vs Extract, join types
- [[lod-expressions-calculated-fields]] - LOD performance impact
- [[dashboard-design-patterns]] - reducing visual complexity
- Tableau performance guide: https://help.tableau.com/current/pro/desktop/en-us/perf_record_create_desktop.htm
