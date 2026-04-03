---
title: Tableau Calculations
category: tools
tags: [bi-analytics, tableau, calculated-fields, table-calculations, window-functions, parameters]
---

# Tableau Calculations

Tableau offers multiple calculation types that operate at different levels of granularity. Understanding when to use each type is essential for building accurate and performant dashboards.

## Key Facts

- Six calculation types: row-level, aggregated, quick table calculations, table calculations, window calculations, LOD
- Row-level calculations run per row; aggregated require aggregation functions
- Table calculations compute over values visible in the current view
- Window calculations are a sub-type of table calculations that operate over a window of visible values
- Quick table calculations are wrappers around window functions applied in 2 clicks
- Parameters are user-controlled variables that modify dashboard behavior

## Patterns

### Calculation Types Overview

| Type | Description | Example |
|------|-------------|---------|
| **Row-level** | Per row (observation) | `[Price] * [Quantity]` |
| **Aggregated** | Uses aggregation function | `SUM([Sales]) / COUNT([Orders])` |
| **Quick Table Calc** | Built-in table calcs (2 clicks) | Running Total, Percent of Total |
| **Table Calculation** | Custom formula over visible values | `INDEX()`, `RANK()`, `LOOKUP()` |
| **Window Calculation** | Over window of visible values | `WINDOW_AVG(SUM([Sales]), -2, 0)` |
| **LOD** | At specified granularity | `{FIXED [Customer] : SUM([Sales])}` |

### Date Functions

```
DATEPART('month', [Order Date])    -- extracts integer (3 for March)
DATETRUNC('month', [Order Date])   -- returns first date of period (2023-03-01)
DATEDIFF('day', [Order Date], TODAY())  -- difference between dates
DATENAME('weekday', [Order Date])  -- returns string ("Monday")
```

Note: Tableau wraps DATETRUNC in DATEBAR by default. Choose "exact date" from field dropdown to see actual date.

### String Functions

```
SPLIT([Product Name], '-', 1)      -- split by delimiter, first part
FIND([String], 'word')             -- position of substring
REPLACE([String], 'old', 'new')    -- replace substring
CONTAINS([String], 'word')         -- true/false
STARTSWITH([Category], 'word')     -- true/false (faster than CONTAINS)
REGEXP_MATCH / REGEXP_EXTRACT / REGEXP_REPLACE  -- regex
```

**Performance tip**: `STARTSWITH` is faster than `CONTAINS` when possible.

### Aggregated Calculations

```
SUM([Sales])
AVG([Profit])
MEDIAN([Revenue])
COUNTD([User ID])               -- count distinct
ATTR([Region])                  -- checks if unique; marks * if multiple values
SUM([Revenue] - [Cost]) / SUM([Revenue])  -- margin calculation
```

### Table Calculations

**Indexing and ranking:**
```
INDEX()                -- row number within partition (1, 2, 3...)
FIRST()                -- offset from first row (0 for first)
LAST()                 -- offset from last row (0 for last)
RANK(expression)       -- rank by value
RANK_UNIQUE(), RANK_DENSE(), RANK_PERCENTILE()
```

**Running totals:**
```
RUNNING_SUM(SUM([Sales]))
RUNNING_AVG(SUM([Profit]))
RUNNING_MAX(SUM([Revenue]))
```

**Lookup and reference:**
```
LOOKUP(SUM([Sales]), -1)       -- value from 1 row earlier
LOOKUP(SUM([Sales]), FIRST())  -- value from first row in partition
PREVIOUS_VALUE(0)              -- previous value or 0 if none
```

**Partition and Address**: "Compute Using" settings define which dimension to address (calculate along) and which to partition (reset the calculation).

### Window Calculations

```
WINDOW_SUM(SUM([Sales]), -2, 0)    -- rolling 3-period sum
WINDOW_AVG(SUM([Sales]), -2, 0)    -- rolling 3-period average
WINDOW_MAX(SUM([Profit]))           -- max in entire window
WINDOW_MIN(SUM([Profit]))           -- min in entire window
WINDOW_STDEV(SUM([Sales]))         -- std deviation
```

Offsets: `FIRST()` = beginning, `LAST()` = end, `0` = current row. Second and third params are relative start and end.

### Quick Table Calculations

Applied via right-click measure on shelf -> Quick Table Calculation:

| Function | Description |
|----------|-------------|
| Running Total | Cumulative sum |
| Difference | Difference from previous period |
| Percent Difference | `(current - previous) / previous * 100%` |
| Percent of Total | Share in overall total |
| Moving Average | Rolling average over N periods |
| YTD Total | Year-to-date running total |
| Compound Growth Rate | CAGR |
| Rank | Ranking within partition |

Show last month filter: `LAST() = 0` as table calculation filter.

### Parameters

Create: right-click data panel -> Create Parameter. Types: String, Integer, Float, Boolean, Date.

```
IF [Sales] > [Parameter: Sales Threshold] THEN 'Above' ELSE 'Below' END
```

**Metric switcher pattern**: Parameter + IF/CASE to show different metrics based on dropdown selection.

### Logical Functions

```
// IF
IF [Profit] > 0 THEN 'Profitable'
ELSEIF [Profit] = 0 THEN 'Break Even'
ELSE 'Loss'
END

// CASE (cleaner for multiple fixed values)
CASE [Region]
  WHEN 'North' THEN 'Northern Division'
  WHEN 'South' THEN 'Southern Division'
  ELSE 'Other'
END
```

## Gotchas

- Aggregation direction matters: configure whether calculation runs across columns or down rows from the "Compute Using" menu
- Quick table calculations are actually window functions - they wrap formulas so you don't write them manually
- Mixing aggregated and non-aggregated fields in a calculation causes errors - all must be at the same level
- String type operations are the slowest; prefer type hierarchy: `String > Date > Numeric > Boolean`
- `DUPLICATE_AS_CROSSTAB` reveals the underlying data table beneath a visualization - useful for debugging

## See Also

- [[tableau-lod-expressions]] - FIXED/INCLUDE/EXCLUDE for cross-granularity
- [[tableau-fundamentals]] - data connections and filter order
- [[tableau-performance-optimization]] - calculation performance tuning
- [[powerbi-fundamentals]] - DAX equivalent calculations
