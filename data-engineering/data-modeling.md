---
title: Dimensional Data Modeling
category: concepts
tags: [star-schema, snowflake-schema, scd, dimensions, facts, kimball, data-vault]
---

# Dimensional Data Modeling

Dimensional modeling organizes [[data-warehouse]] tables into facts (measurable events) and dimensions (descriptive context). The goal is fast analytical queries and intuitive structure for business users.

## Key Facts

- **Fact table** stores quantitative measures (revenue, quantity, clicks) plus foreign keys to dimension tables. Typically the largest table, append-heavy, partitioned by date
- **Dimension table** stores descriptive attributes (customer name, product category, region). Changes slowly, usually small enough to fit in memory
- **Star schema**: fact table at center, dimension tables around it with direct FK relationships. Simple, fast (fewer JOINs), most common in practice
- **Snowflake schema**: dimensions further normalized into sub-dimensions (e.g., product -> category -> department). Saves storage but adds JOIN complexity
- **SCD (Slowly Changing Dimensions)**: strategies for handling dimension attribute changes over time
  - **Type 0**: Never change (e.g., date dimension)
  - **Type 1**: Overwrite old value. Loses history
  - **Type 2**: Add new row with version/validity dates. Preserves full history, most common
  - **Type 3**: Add column for previous value. Tracks limited history
- **Surrogate keys**: auto-increment integers replacing natural keys in dimensions. Required for SCD Type 2 (multiple rows per natural key)
- **Degenerate dimension**: dimension attribute stored directly in the fact table (e.g., order_number) without a separate dimension table
- **Conformed dimensions**: shared across multiple fact tables (e.g., date, customer) to enable cross-process analysis

## Patterns

### Star schema DDL

```sql
-- Fact table
CREATE TABLE fact_sales (
    sale_id      BIGSERIAL PRIMARY KEY,
    date_key     INT REFERENCES dim_date(date_key),
    product_key  INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    quantity     INT NOT NULL,
    revenue      NUMERIC(12,2) NOT NULL,
    discount     NUMERIC(5,2) DEFAULT 0
);

-- Dimension table
CREATE TABLE dim_product (
    product_key  SERIAL PRIMARY KEY,   -- surrogate key
    product_id   VARCHAR(50) NOT NULL, -- natural key
    name         VARCHAR(200),
    category     VARCHAR(100),
    brand        VARCHAR(100)
);
```

### SCD Type 2 implementation

```sql
CREATE TABLE dim_customer (
    customer_key   SERIAL PRIMARY KEY,
    customer_id    VARCHAR(50) NOT NULL, -- natural key
    name           VARCHAR(200),
    segment        VARCHAR(50),
    valid_from     DATE NOT NULL,
    valid_to       DATE DEFAULT '9999-12-31',
    is_current     BOOLEAN DEFAULT TRUE
);

-- On attribute change: close old row, insert new
UPDATE dim_customer SET valid_to = CURRENT_DATE - 1, is_current = FALSE
    WHERE customer_id = 'C001' AND is_current = TRUE;

INSERT INTO dim_customer (customer_id, name, segment, valid_from, is_current)
    VALUES ('C001', 'Acme Corp', 'Enterprise', CURRENT_DATE, TRUE);
```

## Gotchas

- Star schema seems "denormalized" vs 3NF, but this is intentional for OLAP. Do not normalize a DWH into 3NF - it kills query performance
- SCD Type 2 requires JOINing on `is_current = TRUE` for latest state or on `valid_from <= event_date AND valid_to >= event_date` for historical analysis
- Date dimension should always be a physical table, not computed on the fly. Pre-populate with holidays, fiscal periods, day-of-week flags
- Fact tables with NULL FKs indicate a missing or unknown dimension row. Create explicit "Unknown" rows in each dimension (key = -1) instead of NULLs

## See Also

- [[data-warehouse]] - where dimensional models live
- [[normalization]] - contrasting approach (3NF) for OLTP
- [[postgresql-for-data-engineering]] - implementing dimensional models in PG
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ - Kimball techniques reference
