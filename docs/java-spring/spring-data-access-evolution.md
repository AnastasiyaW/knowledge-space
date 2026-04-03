---
title: Spring Data Access - From JDBC to Spring Data
category: concepts
tags: [java-spring, spring, jdbc, jdbctemplate, jooq, spring-data, crud-repository, sql]
---

# Spring Data Access - From JDBC to Spring Data

Evolution of data access in Spring: raw JDBC -> PreparedStatement -> JdbcTemplate -> NamedParameterJdbcTemplate -> JOOQ -> Spring Data JDBC (CrudRepository). Each level reduces boilerplate and increases safety.

## Key Facts

- Raw Statement = SQL injection vulnerable; PreparedStatement separates SQL from data
- JdbcTemplate handles connection management, exception translation, result mapping
- NamedParameterJdbcTemplate replaces positional `?` with `:paramName`
- JOOQ provides compile-time SQL type safety via generated code from DB schema
- Spring Data CrudRepository generates SQL from method names - zero manual SQL for CRUD
- `CrudRepository.save()`: null ID = INSERT, non-null ID = UPDATE
- N+1 problem: use JOIN queries or batch fetching to avoid per-entity sub-queries

## Patterns

### Level 1: JdbcTemplate
```java
@Repository
public class UserRepoJdbc implements UserRepo {
    private final JdbcTemplate jdbc;

    public User getUserByEmail(String email) {
        return jdbc.queryForObject(
            "SELECT * FROM users WHERE email = ?",
            new BeanPropertyRowMapper<>(UserEntity.class), email);
    }

    public void saveUser(User user) {
        jdbc.update("INSERT INTO users (name, email) VALUES (?, ?)",
            user.getName(), user.getEmail());
    }
}
```

Key methods: `update()` (INSERT/UPDATE/DELETE), `queryForObject()` (single row), `query()` (list), `batchUpdate()` (batch ops).

### Level 2: NamedParameterJdbcTemplate
```java
String sql = "INSERT INTO users (name, email) VALUES (:name, :email)";
MapSqlParameterSource params = new MapSqlParameterSource()
    .addValue("name", user.getName())
    .addValue("email", user.getEmail());
namedJdbc.update(sql, params);
```

### Level 3: JOOQ (Type-Safe SQL)
```java
@Repository
public class UserRepoJooq implements UserRepo {
    private final DSLContext dsl;

    public User getUserByEmail(String email) {
        return dsl.selectFrom(USERS)
                  .where(USERS.EMAIL.eq(email))
                  .fetchOneInto(UserEntity.class);
    }

    public void saveUser(User user) {
        dsl.insertInto(USERS)
           .set(USERS.NAME, user.getName())
           .set(USERS.EMAIL, user.getEmail())
           .execute();
    }
}
```

JOOQ generates Java classes from DB schema: `USERS.EMAIL.eq(email)` catches typos at compile time.

### Level 4: Spring Data CrudRepository
```java
public interface UserCrudRepository extends ListCrudRepository<UserEntity, Long> {
    UserEntity findByEmail(String email);
    List<UserEntity> findByNameContaining(String part);
    void deleteByEmail(String email);
}
```

### Method Name Conventions
| Method Name | Generated SQL |
|------------|---------------|
| `findByEmail(email)` | `WHERE email = ?` |
| `findByNameContaining(part)` | `WHERE name LIKE '%part%'` |
| `findByPriceGreaterThan(n)` | `WHERE price > ?` |
| `countByStatus(s)` | `SELECT COUNT(*) WHERE status = ?` |
| `deleteByEmail(email)` | `DELETE WHERE email = ?` |

### Custom @Query
```java
@Query("SELECT * FROM orders WHERE status = :status ORDER BY date_time DESC")
List<OrderEntity> findByStatus(@Param("status") String status);
```

### Solving N+1 with JOINs
```sql
SELECT o.*, u.name as user_name, mi.name as item_name
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_menu_items omi ON o.id = omi.order_id
LEFT JOIN menu_items mi ON omi.menu_item_id = mi.id
WHERE o.status = :status
```

### Comparison Table
| Feature | JdbcTemplate | NamedParameterJdbc | JOOQ | CrudRepository |
|---------|-------------|-------------------|------|----------------|
| SQL safety | String | String | Type-safe DSL | Generated from method name |
| Compile-time checks | None | None | Full | Partial |
| IDE support | None | None | Autocomplete | Method name hints |
| Learning curve | Low | Low | Medium | Low |
| SQL flexibility | Full | Full | Full | Limited (use @Query) |

## Gotchas

- `BeanPropertyRowMapper` maps by column name convention (`user_name` -> `setUserName()`) - mismatch = null
- `queryForObject` throws `EmptyResultDataAccessException` if no rows - wrap with try/catch or use `query()` + stream
- JOOQ requires code generation step - run after schema changes
- CrudRepository method names are convention-sensitive: `findByNameContaining` works, `findByNameLike` needs `%` in parameter
- Deprecated: `queryForObject(sql, args, rowMapper)` - use `queryForObject(sql, rowMapper, args...)`

## See Also

- [[spring-data-jpa-hibernate]] - JPA/Hibernate ORM approach
- [[spring-boot-configuration]] - DataSource and connection pool config
- [[database-migrations]] - Schema evolution with Flyway/Liquibase
