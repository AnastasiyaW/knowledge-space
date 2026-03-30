---
title: LOD Expressions & Calculated Fields
category: BI Tools - Tableau
tags: [tableau, LOD, FIXED, INCLUDE, EXCLUDE, calculated-field, table-calculation, performance]
---

# LOD Expressions & Calculated Fields

Level of Detail (LOD) expressions control aggregation granularity independent of the visualization. Combined with calculated fields and table calculations, they form Tableau's computation layer.

## Key Facts

- LOD expressions compute at a specified level of detail, regardless of what dimensions are in the view
- Three LOD types: FIXED, INCLUDE, EXCLUDE
- FIXED LOD generates additional JOINs in the compiled query - heavier than INCLUDE/EXCLUDE
- LOD expressions sit at different levels in the [[tableau-performance-optimization]] order of operations
- Relations can replace some LOD use cases with better performance
- Table calculations happen after the query returns - no DB load but limited to visible data
- [[tableau-data-connections]] affects whether LOD runs on DB side or extract side

## LOD Expression Types

| Type | Syntax | Behavior | Order of Ops |
|------|--------|----------|-------------|
| **FIXED** | `{FIXED [Dim]: AGG([Measure])}` | Computes at specified dimensions, ignoring view | With Context Filters |
| **INCLUDE** | `{INCLUDE [Dim]: AGG([Measure])}` | Adds dimension to current view granularity | With Dimension Filters |
| **EXCLUDE** | `{EXCLUDE [Dim]: AGG([Measure])}` | Removes dimension from current view granularity | With Dimension Filters |

## Patterns

**Common LOD use cases:**

```
-- Customer's first purchase date (ignoring view granularity)
{FIXED [Customer ID]: MIN([Order Date])}

-- Total sales per category (regardless of sub-category in view)
{FIXED [Category]: SUM([Sales])}

-- Average of detail-level totals (e.g., avg order size)
AVG({INCLUDE [Order ID]: SUM([Sales])})

-- Total excluding current dimension
{EXCLUDE [Region]: SUM([Sales])}
-- If view has [Region, Category], this gives total per Category only
```

**Performance comparison:**

```
HEAVY (generates JOINs):
  SUM({FIXED DATEPART('year', [Order Date]): SUM([Sales])})
  -> Generates 3 JOINs

LIGHTER (fewer JOINs):
  SUM({INCLUDE DATEPART('year', [Order Date]): SUM([Sales])})
  -> Generates 2 JOINs

ALTERNATIVE (no LOD):
  -> Pre-join the needed columns in data source
  -> Use RAWSQL() window functions
  -> Use table calculations when possible
```

**Calculated field best practices:**

```
Data type hierarchy (fastest to slowest):
  Boolean > Numeric > Date/Time > String

Prefer:
  DATEPART() over DATENAME()     -- numeric vs string
  STARTSWITH() over CONTAINS()   -- prefix match vs full scan
  ELSEIF over ELSE IF           -- flat vs nested evaluation
  MIN()/MAX() over ATTR()       -- simpler aggregation

Avoid in calcs:
  NOW(), TODAY()                 -- blocks Query Fusion
  Nested Table Calculations      -- slow on large data
  Complex IF chains              -- use groups/sets instead
```

**Table calculations vs LOD:**

```
Table Calculations:
  + Run after query (no DB load)
  + Good for: running totals, percentages, rank, moving averages
  - Limited to returned data
  - Partition/addressing can be confusing

LOD Expressions:
  + Control granularity precisely
  + Work with filtered data
  - Generate extra SQL JOINs
  - Heavier on DB/extract
```

**Geo-related calculated field:**

```
-- Truncate order dates to month for Relations join
DATE(DATETRUNC("month", [Order Date]))

-- Create spatial point from coordinates
MAKEPOINT([Latitude], [Longitude])
```

## Gotchas

- **Symptom**: FIXED LOD returns unexpected values when filters are applied -> **Cause**: FIXED ignores dimension filters (it's above them in order of operations) -> **Fix**: Use Context Filters to make dimension filters affect FIXED, or use INCLUDE/EXCLUDE instead
- **Symptom**: Dashboard slows down after adding LOD expression -> **Cause**: FIXED generates additional JOINs in the query -> **Fix**: Pre-compute in data source, use INCLUDE/EXCLUDE, or use RAWSQL window functions
- **Symptom**: ATTR() shows asterisk (*) -> **Cause**: Multiple values exist at the current aggregation level -> **Fix**: Use MIN() or MAX() instead of ATTR() for both clarity and performance
- **Symptom**: Table calculation returns NULL for some cells -> **Cause**: Partition/addressing configuration doesn't match the intended scope -> **Fix**: Right-click > Compute Using, verify table direction matches intent

## See Also

- [[tableau-performance-optimization]] - LOD position in order of operations
- [[tableau-data-connections]] - pre-joining data to avoid LOD
- [[tableau-geo-functions]] - spatial calculated fields
- LOD docs: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm
