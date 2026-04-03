---
title: Dimensional Modeling (Kimball)
category: concepts
tags: [data-engineering, dimensional-modeling, star-schema, snowflake-schema, kimball]
---

# Dimensional Modeling (Kimball)

Dimensional modeling organizes data into fact tables (measures/events) surrounded by dimension tables (descriptive context). It is the standard approach for data marts and BI-optimized analytical layers.

## Star Schema

```
         dim_date
            |
dim_product--fact_sales--dim_customer
            |
         dim_store
```

- **Fact table:** Foreign keys to dimensions + measures (amount, quantity, duration)
- **Dimension tables:** Descriptive attributes (name, category, address) - denormalized for query performance

## Snowflake Schema

Dimensions are normalized (broken into sub-tables). Reduces storage but requires more JOINs. Less common in practice due to query complexity.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Surrogate keys** | System-generated integer PKs in dimensions (not business keys) |
| **Degenerate dimension** | Dimension value stored directly in fact table (e.g., invoice number) |
| **Junk dimension** | Groups low-cardinality flags/indicators into single dimension |
| **Conformed dimension** | Shared across multiple fact tables/marts for consistency |

## Design Process

1. Choose the business process to model
2. Declare the grain (what does one row represent?)
3. Identify the dimensions (who, what, when, where)
4. Identify the facts (measures - additive, semi-additive, non-additive)

## Patterns

### Star Schema DDL

```sql
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY,  -- surrogate key
    customer_bk VARCHAR(50),          -- business key
    name VARCHAR(200),
    segment VARCHAR(50),
    valid_from DATE,
    valid_to DATE DEFAULT '9999-12-31'
);

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_sk INT REFERENCES dim_date(date_sk),
    customer_sk INT REFERENCES dim_customer(customer_sk),
    product_sk INT REFERENCES dim_product(product_sk),
    quantity INT,
    amount NUMERIC(12,2)
);
```

## Gotchas
- Star schema denormalization trades storage for query performance - acceptable for OLAP
- Each mart may define metrics differently without conformed dimensions
- Surrogate keys decouple DWH from source system key changes
- Always define the grain first - unclear grain leads to incorrect aggregations

## See Also
- [[data-modeling]] - normalization theory
- [[data-vault]] - alternative for core DWH layer
- [[scd-patterns]] - handling dimension changes
- [[dwh-architecture]] - Kimball vs Inmon approaches
