---
title: Tableau Geo Functions
category: BI Tools - Tableau
tags: [tableau, geo, spatial, map, MAKEPOINT, MAKELINE, BUFFER, DISTANCE, spatial-join]
---

# Tableau Geo Functions

Spatial data functions in Tableau for map visualizations: creating points, lines, buffers, computing distances, and performing spatial joins.

## Key Facts

- Four core geo functions: MAKEPOINT, MAKELINE, DISTANCE, BUFFER
- Spatial data type is faster than raw lat/lon coordinates for map rendering
- Spatial joins use BUFFER + Intersects condition
- New Tableau versions support multiple map layers from different data sources
- [[lod-expressions-calculated-fields]] can be combined with geo functions
- [[tableau-performance-optimization]] - MAKELINE is faster than path-based routing

## Core Functions

| Function | Syntax | Purpose |
|----------|--------|---------|
| `MAKEPOINT` | `MAKEPOINT([LAT], [LON])` | Create spatial point from coordinates |
| `MAKELINE` | `MAKELINE([Start], [End])` | Draw line between two spatial points |
| `DISTANCE` | `DISTANCE([P1], [P2], 'km')` | Distance between points (km, mi, m, ft) |
| `BUFFER` | `BUFFER([Spatial], 8, 'km')` | Create circular area around point |

## Patterns

**Map visualization (recommended approach):**

```
Method 1 (NOT recommended - slow):
  Drag Longitude -> Columns, Latitude -> Rows
  Add ID to Detail
  Problem: points are not spatial type, Tableau works slower

Method 2 (RECOMMENDED - fast):
  Create calculated field: MAKEPOINT([Latitude], [Longitude])
  Drag calculated field to sheet
  Add ID to Detail
  Result: proper spatial data type, faster rendering
```

**Spatial join for proximity analysis:**

```
Task: Find bus stops with most apartments within 300m

Step 1: Create MAKEPOINT for stops table
  stop_point = MAKEPOINT([stop_lat], [stop_lon])

Step 2: Create BUFFER around stops
  stop_area = BUFFER([stop_point], 300, 'm')

Step 3: Create MAKEPOINT for apartments table
  apt_point = MAKEPOINT([apt_lat], [apt_lon])

Step 4: Join setup:
  Left table join calc:  stop_area (BUFFER)
  Right table join calc: apt_point (MAKEPOINT)
  Join condition: Intersects

Step 5: Count apartments per stop:
  COUNTD([apartment_id])

Step 6: Compute distance:
  DISTANCE([stop_point], [apt_point], 'm')
```

**Interactive buffer with parameter:**

```
1. Create parameter: Buffer_Size (integer, range 100-2000, step 100)
2. Use in BUFFER: BUFFER([stop_point], [Buffer_Size], 'm')
3. Use in count filter: DISTANCE(...) <= [Buffer_Size]
4. Show parameter control on dashboard
-> User can interactively adjust radius
```

**Route visualization with MAKELINE:**

```
Method 1 (slow - path marks):
  Add Route to Detail, Sequence to Path
  Problem: each stop is a separate mark

Method 2 (fast - MAKELINE):
  1. Self-join table with offset (next stop coords on same row)
  2. Create start_point = MAKEPOINT([lat], [lon])
  3. Create end_point = MAKEPOINT([next_lat], [next_lon])
  4. Create route_line = MAKELINE([start_point], [end_point])
  5. Add route_line to sheet, Route to Detail

  Why faster: routes (lines) << stops (points) in count
```

**Multiple map layers (new Tableau):**

```
- Drag first spatial field to map
- Add second source via "Add a Marks Layer"
- Each layer can have independent data source
- Control visibility and selection blocking per layer
- No joins needed between layers
```

## Gotchas

- **Symptom**: Map with thousands of points is very slow -> **Cause**: Using raw lat/lon instead of MAKEPOINT spatial type -> **Fix**: Create calculated field with MAKEPOINT, use it instead of lat/lon pills
- **Symptom**: Spatial join "explodes" row count -> **Cause**: Many-to-many relationship (points in overlapping buffers) -> **Fix**: Use Physical JOIN (not Logical) for spatial joins, aggregate after join
- **Symptom**: Route lines look wrong or connect wrong points -> **Cause**: Self-join offset not matching sequence order -> **Fix**: Verify self-join condition: same route ID, sequence = sequence + 1
- **Symptom**: Dual axis map layers not aligned -> **Cause**: Axes not synchronized -> **Fix**: Right-click axis > Synchronize Axis

## See Also

- [[lod-expressions-calculated-fields]] - calculated fields for spatial data
- [[tableau-performance-optimization]] - map rendering optimization
- [[tableau-data-connections]] - spatial data source connections
- Tableau spatial docs: https://help.tableau.com/current/pro/desktop/en-us/maps_howto_spatial.htm
