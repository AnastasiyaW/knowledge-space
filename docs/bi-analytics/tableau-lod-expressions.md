---
title: Tableau LOD Expressions
category: tools
tags: [bi-analytics, tableau, lod, fixed, include, exclude, level-of-detail]
---

# Tableau LOD Expressions

Level of Detail (LOD) expressions compute aggregations at a different granularity than what is shown in the current view. They create subqueries independent of the view context, enabling cross-granularity analysis without complex workarounds.

## Key Facts

- Three LOD types: FIXED, INCLUDE, EXCLUDE
- LOD creates subqueries independent of the current view
- FIXED ignores the view completely; INCLUDE adds granularity; EXCLUDE removes granularity
- FIXED LOD evaluates at context filter level (step 4 in filter order)
- INCLUDE/EXCLUDE LOD evaluate at dimension filter level (step 5)
- LOD inside complex nested calculations causes performance issues (extra JOINs)

## Patterns

### FIXED LOD

Computes at specified dimension(s), completely ignoring the view:

```
{FIXED [Customer ID] : SUM([Sales])}
-- Total sales per customer, regardless of view

{FIXED [Region], [Year] : AVG([Revenue])}
-- Average revenue per region per year

{FIXED [User ID] : MIN([Event Date])}
-- First event date per user (for cohort analysis)
```

Use cases: cohort analysis, customer LTV, finding first/last purchase date, per-entity totals displayed in any view context.

### INCLUDE LOD

Computes at a finer granularity than the view (adds dimensions):

```
{INCLUDE [Order ID] : SUM([Quantity])}
-- Per-order sum while viewing by month
```

The view might show monthly aggregates, but INCLUDE calculates at the order level first, then aggregates up.

**Performance note**: INCLUDE adds 2 JOINs when used in a complex calculation.

### EXCLUDE LOD

Computes at coarser granularity (removes dimensions from context):

```
{EXCLUDE [Region] : SUM([Sales])}
-- Total ignoring region, while view shows by region
```

Use case: show % of grand total while broken down by subcategory.

### Classic Pattern: Percent of Total

```
SUM([Sales]) / {FIXED : SUM([Sales])} * 100
```

The `{FIXED : SUM([Sales])}` with no dimensions computes the grand total, unaffected by any view-level dimensions.

### LOD in Filter Order

Understanding where LOD sits in the filter order of operations:

1. Extract Filters
2. Data Source Filters
3. Context Filters
4. **FIXED LOD** evaluated here (with Dimension Filters)
5. **INCLUDE/EXCLUDE LOD** evaluated here (with Measure Filters)
6. Table Calculation Filters

This means FIXED LOD is affected by context filters but NOT by dimension filters, while INCLUDE/EXCLUDE LOD is affected by both.

### Cohort Analysis with LOD

```
-- Cohort month (first activity)
{FIXED [User ID] : MIN(DATETRUNC('month', [Event Date]))}

-- Period since first activity
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### Nested LOD

LOD inside another LOD is possible but use carefully due to performance impact. Each nesting level adds JOINs to the generated query.

## Gotchas

- Avoid LOD inside complex nested calculations - each LOD adds JOINs:
  ```
  -- Slow (3+ JOINs):
  SUM({FIXED DATEPART('year', [Order Date]) : SUM([Sales])})

  -- Better: pre-aggregate in data source or use table calculation
  ```
- FIXED LOD is not affected by dimension filters on the view - this can cause confusion when a filter appears to not work on a FIXED calculation
- Context filters DO affect FIXED LOD - promote a filter to context filter if you need FIXED LOD to respect it
- INCLUDE/EXCLUDE are more intuitive but slower than FIXED in most cases
- When possible, materialize calculated fields in Extract before publishing rather than computing LOD at query time

## See Also

- [[tableau-calculations]] - row-level, aggregated, and table calculations
- [[tableau-fundamentals]] - filter order of operations, data connections
- [[tableau-performance-optimization]] - optimizing LOD performance
- [[cohort-retention-analysis]] - cohort analysis patterns using LOD
