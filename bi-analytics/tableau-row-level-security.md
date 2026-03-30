---
title: Tableau Row & Column Level Security
category: BI Tools - Tableau
tags: [tableau, security, RLS, CLS, row-level-security, user-filter, permissions, tableau-server]
---

# Tableau Row & Column Level Security

Controlling data visibility per user in Tableau dashboards. Row-level security (RLS) restricts which rows users see; column-level security (CLS) restricts which dimensions are visible.

## Key Facts

- **Row-level security (RLS)**: show different rows to different users (e.g., regional managers see only their region)
- **Column-level security (CLS)**: show different columns/dimensions to different users
- Two implementation approaches: built-in user filters and fact-table-based filtering
- USERNAME() and ISMEMBEROF() functions are used for runtime filtering - but have performance cost
- Must use Physical JOIN (not Logical) when joining security tables to avoid row multiplication
- Connected to [[tableau-performance-optimization]] - RLS filters affect query performance
- Connected to [[tableau-data-connections]] - security tables require specific join configuration

## Patterns

**Method 1: Built-in user filters (simple):**

```
1. Server menu > Create User Filter
2. Select dimension (e.g., Region)
3. Map users to allowed values
4. Rename filter for clarity
5. Apply filter to worksheet or dashboard

Pros: Quick setup, flexible rules
Cons: Hard to manage with many users,
      rules embedded in workbook
```

**Method 2: Fact table approach (scalable):**

```
1. Create security table in DB:
   | username      | region    |
   |---------------|-----------|
   | john.smith    | West      |
   | jane.doe      | East      |
   | jane.doe      | Central   |

2. Physical JOIN security table to data:
   orders JOIN security ON orders.region = security.region

3. Add data source filter:
   [username] = USERNAME()
   Apply to ALL worksheets

4. Set filter to apply before dashboard loads

CRITICAL: Must use Physical JOIN, not Logical
  Logical JOIN would multiply rows by number of managers
```

**Filter configuration:**

```
-- In calculated field or data source filter:
[Regional Manager] = USERNAME()

-- Apply as context filter for performance:
Right-click filter > Add to Context

-- For group-based access:
ISMEMBEROF("Sales Team")
```

## Gotchas

- **Symptom**: Dashboard shows duplicate data, totals are inflated -> **Cause**: Logical JOIN with security table multiplies rows by number of user-region mappings -> **Fix**: Switch to Physical JOIN, or restructure security table to avoid many-to-many
- **Symptom**: Dashboard loads very slowly for certain users -> **Cause**: USERNAME()/ISMEMBEROF() runtime filters are expensive -> **Fix**: Use context filters to push RLS evaluation earlier in order of operations, cache where possible
- **Symptom**: User sees all data instead of filtered subset -> **Cause**: Filter not set to "All worksheets" or username doesn't match server username -> **Fix**: Verify exact username format matches Tableau Server usernames, apply filter globally
- **Symptom**: Security works on Desktop but not on Server -> **Cause**: USERNAME() returns different values in Desktop vs Server environments -> **Fix**: Test with Tableau Server username format, use FULLNAME() as fallback

## See Also

- [[tableau-performance-optimization]] - runtime filter performance impact
- [[tableau-data-connections]] - physical vs logical joins for security tables
- [[lod-expressions-calculated-fields]] - FIXED LOD interaction with security filters
- Tableau RLS docs: https://help.tableau.com/current/pro/desktop/en-us/publish_userfilters.htm
