---
title: Subqueries and Derived Tables
category: syntax
tags: [sql, subquery, derived-table, correlated, exists, in, any, all]
---

# Subqueries and Derived Tables

Subqueries are SELECT statements nested within another SQL statement. They can appear in SELECT (scalar), FROM (derived table), WHERE/HAVING (filter), and with operators like EXISTS, IN, ANY, ALL. Understanding when the optimizer can flatten subqueries vs when they execute row-by-row is key to performance.

## Key Facts

- **Scalar subquery** - returns exactly one row and one column; can appear anywhere a single value is expected
- **Derived table** (inline view) - subquery in FROM clause; must be aliased
- **Correlated subquery** - references columns from the outer query; conceptually re-executed for each outer row (but optimizer may transform it)
- **EXISTS** - returns TRUE if subquery returns at least one row; stops scanning on first match (semi-join)
- **IN** vs **EXISTS** - traditionally EXISTS was faster for correlated checks, but modern optimizers (PostgreSQL 10+, MySQL 8.0+) transform IN to semi-join, making them equivalent
- See [[common-table-expressions]] for rewriting complex subqueries as CTEs
- See [[query-optimization-explain]] for understanding subquery execution plans

## Patterns

### Scalar subquery

```sql
-- Subquery in SELECT (returns one value per row)
SELECT name, salary,
       salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;

-- Subquery in WHERE
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

### Correlated subquery

```sql
-- Find employees earning more than their department average
SELECT e.name, e.salary, e.department
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department = e.department  -- references outer query
);
```

### EXISTS vs IN

```sql
-- EXISTS: check if customer has any orders
SELECT c.name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- IN: same result, different style
SELECT c.name FROM customers c
WHERE c.id IN (SELECT customer_id FROM orders);

-- NOT EXISTS: customers without orders (anti-join)
SELECT c.name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### Derived tables

```sql
-- Derived table in FROM (must have alias)
SELECT dept_stats.department, dept_stats.avg_salary
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_stats
WHERE dept_stats.avg_salary > 60000;

-- Multiple derived tables joined
SELECT a.category, a.total_revenue, b.total_cost
FROM (SELECT category, SUM(revenue) AS total_revenue FROM sales GROUP BY category) a
JOIN (SELECT category, SUM(cost) AS total_cost FROM expenses GROUP BY category) b
    ON a.category = b.category;
```

### ANY / ALL operators

```sql
-- ANY: salary greater than ANY manager salary (i.e., greater than the minimum)
SELECT name FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE role = 'manager');

-- ALL: salary greater than ALL manager salaries (i.e., greater than the maximum)
SELECT name FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE role = 'manager');
```

## Gotchas

- **Scalar subquery returning multiple rows** - runtime error. Always ensure scalar subqueries return exactly 0 or 1 row
- **IN with NULLs** - `NOT IN (1, 2, NULL)` always returns empty set because `x <> NULL` is UNKNOWN. Use `NOT EXISTS` instead when the subquery can return NULLs
- **Correlated subquery performance** - without optimizer transformation, correlated subqueries execute once per outer row. Check EXPLAIN output to verify the optimizer converts to a join
- **MySQL derived table limitations** - in MySQL < 8.0, derived tables were always materialized; MySQL 8.0+ can merge derived tables into the outer query
- **Subquery in UPDATE/DELETE** - PostgreSQL allows subqueries in SET/WHERE of UPDATE. Both PostgreSQL and MySQL support this

## See Also

- [[common-table-expressions]] - CTEs as alternative to complex subqueries
- [[joins-and-set-operations]] - when to use joins instead of subqueries
- [PostgreSQL subquery docs](https://www.postgresql.org/docs/current/functions-subquery.html)
- [MySQL subquery docs](https://dev.mysql.com/doc/refman/8.0/en/subqueries.html)
