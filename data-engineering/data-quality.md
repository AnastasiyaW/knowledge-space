---
title: Data Quality
category: concepts
tags: [data-quality, testing, validation, great-expectations, dbt-tests, scd, observability]
---

# Data Quality

Data quality ensures that data is accurate, complete, consistent, timely, and valid throughout the [[etl-and-elt]] pipeline. Poor data quality cascades into incorrect analytics, broken models, and lost business trust.

## Key Facts

- **Data quality dimensions**: accuracy (matches reality), completeness (no missing values where required), consistency (no contradictions across tables), timeliness (fresh enough for use case), uniqueness (no duplicates), validity (conforms to schema/rules)
- **Schema validation**: verify column types, nullability, allowed values at ingestion time. Catch drift before it propagates
- **Row-level tests**: assertions on individual records (non-null, within range, format match)
- **Aggregate tests**: assertions on dataset-level metrics (row count within expected range, uniqueness of key columns, referential integrity between tables)
- **dbt tests**: built-in (`unique`, `not_null`, `accepted_values`, `relationships`) and custom SQL tests. Run as part of the transformation pipeline
- **Great Expectations**: Python framework for declarative data validation. Creates "expectations" (assertions) organized in suites, generates data docs
- **Data observability**: automated monitoring of data freshness, volume, schema changes, and distribution drift. Tools: Monte Carlo, Soda, Elementary
- **SCD (Slowly Changing Dimensions)** testing: verify Type 2 dimension rows have non-overlapping validity ranges and exactly one `is_current=TRUE` row per natural key. See [[data-modeling]]

## Patterns

### dbt built-in tests (schema.yml)

```yaml
models:
  - name: fact_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customer')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
```

### Custom dbt test (SQL)

```sql
-- tests/assert_positive_revenue.sql
SELECT order_id, revenue
FROM {{ ref('fact_orders') }}
WHERE revenue < 0
-- Test passes if query returns 0 rows
```

### Great Expectations (Python)

```python
import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_csv("orders.csv")

validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_between("quantity", min_value=1, max_value=10000)
validator.expect_column_values_to_be_unique("order_id")
validator.expect_table_row_count_to_be_between(min_value=1000, max_value=1_000_000)

results = validator.validate()
```

### Airflow data quality task

```python
def validate_load(**kwargs):
    hook = PostgresHook(postgres_conn_id='dwh')
    count = hook.get_first("SELECT COUNT(*) FROM fact_orders WHERE dt = %(dt)s",
                           parameters={'dt': kwargs['ds']})[0]
    if count < 100:
        raise ValueError(f"Only {count} rows loaded for {kwargs['ds']}, expected >100")

validate = PythonOperator(
    task_id='validate_load',
    python_callable=validate_load,
    provide_context=True
)

# DAG flow: extract >> transform >> load >> validate
```

## Gotchas

- Data quality checks should run AFTER load but BEFORE downstream consumers (place between load and mart/dashboard refresh in [[apache-airflow]] DAGs)
- Row count checks alone are insufficient. A pipeline can load the correct number of duplicate rows. Always include uniqueness tests on key columns
- Schema validation at ingestion prevents silent type coercion (e.g., "123" becoming a string in a numeric column). Fail fast, not silently
- Great Expectations suites should be version-controlled alongside pipeline code, not managed manually through the UI
- Monitoring data distribution (mean, stddev, percentiles) catches subtle issues that pass hard-threshold tests (e.g., gradual drift in user demographics)
- SCD Type 2 validity ranges must be contiguous and non-overlapping. A common bug: closing old row's `valid_to` as `CURRENT_DATE` and opening new row's `valid_from` as `CURRENT_DATE` creates a 1-day overlap

## See Also

- [[etl-and-elt]] - where quality checks fit in the pipeline
- [[apache-airflow]] - orchestrating validation tasks
- [[data-modeling]] - SCD patterns that need quality enforcement
- https://docs.getdbt.com/docs/build/data-tests - dbt tests documentation
- https://docs.greatexpectations.io/ - Great Expectations documentation
