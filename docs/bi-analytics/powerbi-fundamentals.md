---
title: Power BI Fundamentals
category: tools
tags: [bi-analytics, power-bi, dax, power-query, data-model, microsoft]
---

# Power BI Fundamentals

Power BI is Microsoft's BI platform (Desktop + Cloud) with tight Microsoft ecosystem integration, a generous free tier, and the DAX calculation engine. It excels in organizations already using Azure, Excel, Teams, and SharePoint.

## Key Facts

- Three workspace views: Report View (canvas), Data View (table inspection), Model View (relationships)
- Two connection modes: Import (data loaded into in-memory engine) and DirectQuery (live queries to source)
- Star schema recommended: fact table at center, dimension tables around it
- DAX (Data Analysis Expressions) = formula language for calculated columns and measures
- Power Query Editor = built-in ETL tool with M language
- Supports 100+ data sources: Excel, CSV, JSON, PDF, SQL Server, PostgreSQL, MySQL, Azure, SharePoint, Web, OData

## Patterns

### Connection Workflow

1. Home -> Get Data -> select source type
2. Enter connection parameters / browse to file
3. Navigator: select tables/sheets to load
4. Transform Data (opens Power Query) or Load directly

**Import mode**: data loaded into `.pbix` file, always fast, but stale until refreshed.
**DirectQuery**: live queries on each interaction, always fresh, but slower.

### Power Query (M Language) Transformations

| Operation | SQL Equivalent |
|-----------|---------------|
| Change data type | CAST |
| Remove rows | WHERE + DELETE |
| Filter rows | WHERE |
| Split column | SUBSTRING / SPLIT |
| Merge columns | CONCAT |
| Add custom column | Calculated column |
| Pivot/Unpivot | PIVOT / UNPIVOT |
| Merge queries | JOIN |
| Append queries | UNION |

Applied Steps panel: every transformation recorded as a reversible step. Underlying M code visible in Advanced Editor.

### Data Model: Relationships

Relationship properties:
- **Cardinality**: One-to-Many (most common), Many-to-Many, One-to-One
- **Cross-filter direction**: Single (from 1 to Many), Both (bidirectional)
- **Active/Inactive**: only one active relationship per table pair

Create: drag field from one table to matching field in another in Model View.

### DAX Basics

**Calculated Column** - computed at data load, stored per row:
```dax
Full Name = Customers[First Name] & " " & Customers[Last Name]
Profit = Sales[Revenue] - Sales[Cost]
```

**Measure** - computed at query time based on filter context:
```dax
Total Sales = SUM(Sales[Revenue])
Average Order = AVERAGE(Sales[OrderValue])
Num Customers = DISTINCTCOUNT(Sales[CustomerID])
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Date[Date]))
YoY Growth % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])
```

### Key DAX Functions

| Function | Purpose |
|----------|---------|
| `SUM()` | Aggregate sum |
| `AVERAGE()` | Aggregate average |
| `COUNT()` / `COUNTA()` | Count rows / non-blank |
| `DISTINCTCOUNT()` | Count unique values |
| `CALCULATE()` | Modify filter context |
| `FILTER()` | Return filtered table |
| `ALL()` | Remove filters from column/table |
| `RELATED()` | Get value from related table |
| `DIVIDE(num, den)` | Safe division (BLANK on div/0) |
| `IF(cond, true, false)` | Conditional logic |
| `SWITCH()` | Multiple conditions |
| `SAMEPERIODLASTYEAR()` | Time intelligence - same period LY |
| `DATEADD()` | Time intelligence - shift dates |

**Filter context**: measures automatically respect active slicers, page filters, visual filters. `CALCULATE` changes this context.

### Filter Types (by precedence)

1. **Visual-level** - applies to one chart
2. **Page-level** - all visuals on page
3. **Report-level** - all pages
4. **Drillthrough** - automatically passed when drilling

Slicer visual = interactive filter widget. Types: list, dropdown, between (date range), relative date.

### Common Visualizations

- Bar/Column chart - category comparisons
- Line chart - time trends
- Pie/Donut - part-to-whole (max 5 slices)
- Matrix - cross-tabulation
- Card - single KPI number
- Table - raw data
- Treemap - hierarchical size comparison
- Map/Filled Map - geographic data
- Gauge - progress to goal

## Gotchas

- DAX is a powerful but distinct paradigm from SQL - the learning curve is steep
- Calculated columns increase file size (stored per row); prefer measures when possible
- Bidirectional relationships can cause unexpected filter propagation - avoid unless required
- `.pbix` files are binary and git-unfriendly; use Azure DevOps for version control
- Import mode `.pbix` files can grow very large with big datasets - consider DirectQuery or aggregation

## See Also

- [[powerbi-advanced-features]] - themes, bookmarks, drill-through, DAX advanced
- [[bi-tools-comparison]] - Power BI vs Tableau vs alternatives
- [[dashboard-design-patterns]] - design principles that apply across tools
- [[sql-for-analytics]] - SQL foundations for DAX users
