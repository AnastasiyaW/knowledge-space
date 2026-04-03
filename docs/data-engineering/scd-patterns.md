---
title: Slowly Changing Dimensions (SCD)
category: concepts
tags: [data-engineering, scd, dimensions, data-modeling, history-tracking]
---

# Slowly Changing Dimensions (SCD)

SCD patterns handle changes to dimension attributes over time. SCD2 is the most common in data warehouses, preserving full history by adding new rows with validity dates.

## SCD Types

| Type | Behavior | History | Use Case |
|------|----------|---------|----------|
| **SCD0** | Never change | None | Static reference data |
| **SCD1** | Overwrite old value | Lost | Corrections, non-historical attributes |
| **SCD2** | Add new row with dates | Full | Most dimension changes |
| **SCD3** | Add column for previous value | Limited (1 prior) | Rarely used |
| **SCD6** | Hybrid (1 + 2 + 3) | Full + current flag | Quick current-value access |

## SCD2 Pattern

```sql
-- SCD2 table structure
customer_id | name    | city      | valid_from | valid_to   | is_current
1           | Alice   | New York  | 2023-01-01 | 2023-06-15 | false
1           | Alice   | Boston    | 2023-06-15 | 9999-12-31 | true
```

### SCD2 Merge Logic

```sql
-- Step 1: Close existing records
UPDATE dim_customer
SET valid_to = CURRENT_DATE, is_current = false
WHERE customer_bk = 'C001' AND is_current = true
  AND (name != 'New Name' OR city != 'New City');

-- Step 2: Insert new version
INSERT INTO dim_customer (customer_bk, name, city, valid_from, valid_to, is_current)
SELECT 'C001', 'New Name', 'New City', CURRENT_DATE, '9999-12-31', true
WHERE EXISTS (
    SELECT 1 FROM staging WHERE customer_bk = 'C001'
      AND (name != 'New Name' OR city != 'New City')
);
```

### Point-in-Time Query

```sql
-- What was the customer's city on 2023-03-15?
SELECT * FROM dim_customer
WHERE customer_bk = 'C001'
  AND '2023-03-15' BETWEEN valid_from AND valid_to;
```

## Gotchas
- SCD2 joins across satellites with different change frequencies produce Cartesian explosion on overlapping date ranges
- `valid_to = '9999-12-31'` convention marks current records - always filter on `is_current = true` for latest state
- Hash keys in Data Vault SCD2 must be computed consistently across all ETL processes
- SCD2 tables grow continuously - plan for storage and query performance

## See Also
- [[data-vault]] - SCD2 in satellite tables
- [[dimensional-modeling]] - dimension design patterns
- [[data-modeling]] - normalization context
