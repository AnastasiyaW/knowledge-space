---
title: "Spring-Datenzugriff – Von JDBC zu Spring Data"
category: concepts
tags: [java-spring, spring, jdbc, jdbctemplate, jooq, spring-data, crud-repository, sql]
level: 3
source_sha256: c6ea483f5ff34cfce47f9991769a4a74f48e154e304b896851352d222c42d04c
translation: machine
translated_at: '2026-10-24'
---
# Spring-Datenzugriff – Von JDBC zu Spring Data {#spring-data-access-from-jdbc-to-spring-data}

Entwicklung des Datenzugriffs in Spring: reines JDBC -> PreparedStatement -> JdbcTemplate -> NamedParameterJdbcTemplate -> JOOQ -> Spring Data JDBC (CrudRepository). Jede Stufe reduziert den Boilerplate-Code und erhöht die Sicherheit.

## Kernfakten {#key-facts}

- Ein roher Statement ist anfällig für SQL-Injection; PreparedStatement trennt SQL von Daten
- JdbcTemplate übernimmt Verbindungsverwaltung, Übersetzung von Exceptions und Mapping der Ergebnisse
- NamedParameterJdbcTemplate ersetzt positionale `?` durch `:paramName`
- JOOQ bietet typsichere SQL-Prüfung zur Kompilierzeit durch aus dem DB-Schema generierten Code
- Spring Data CrudRepository erzeugt SQL aus Methodennamen – kein manuelles SQL für CRUD
- `CrudRepository.save()`: ID null = INSERT, ID nicht null = UPDATE
- N+1-Problem: JOIN-Abfragen oder Batch-Fetching verwenden, um Sub-Abfragen pro Entität zu vermeiden

## Muster {#patterns}

### Stufe 1: JdbcTemplate {#level-1-jdbctemplate}
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

Wichtige Methoden: `update()` (INSERT/UPDATE/DELETE), `queryForObject()` (einzelne Zeile), `query()` (Liste), `batchUpdate()` (Batch-Operationen).

### Stufe 2: NamedParameterJdbcTemplate {#level-2-namedparameterjdbctemplate}
```java
String sql = "INSERT INTO users (name, email) VALUES (:name, :email)";
MapSqlParameterSource params = new MapSqlParameterSource()
    .addValue("name", user.getName())
    .addValue("email", user.getEmail());
namedJdbc.update(sql, params);
```

### Stufe 3: JOOQ (typsicheres SQL) {#level-3-jooq-type-safe-sql}
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

JOOQ generiert Java-Klassen aus dem DB-Schema: `USERS.EMAIL.eq(email)` fängt Tippfehler zur Kompilierzeit ab.

### Stufe 4: Spring Data CrudRepository {#level-4-spring-data-crudrepository}
```java
public interface UserCrudRepository extends ListCrudRepository<UserEntity, Long> {
    UserEntity findByEmail(String email);
    List<UserEntity> findByNameContaining(String part);
    void deleteByEmail(String email);
}
```

### Konventionen für Methodennamen {#method-name-conventions}
| Methodenname | Generiertes SQL |
|------------|---------------|
| `findByEmail(email)` | `WHERE email = ?` |
| `findByNameContaining(part)` | `WHERE name LIKE '%part%'` |
| `findByPriceGreaterThan(n)` | `WHERE price > ?` |
| `countByStatus(s)` | `SELECT COUNT(*) WHERE status = ?` |
| `deleteByEmail(email)` | `DELETE WHERE email = ?` |

### Eigene @Query {#custom-query}
```java
@Query("SELECT * FROM orders WHERE status = :status ORDER BY date_time DESC")
List<OrderEntity> findByStatus(@Param("status") String status);
```

### N+1 mit JOINs lösen {#solving-n1-with-joins}
```sql
SELECT o.*, u.name as user_name, mi.name as item_name
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_menu_items omi ON o.id = omi.order_id
LEFT JOIN menu_items mi ON omi.menu_item_id = mi.id
WHERE o.status = :status
```

### Vergleichstabelle {#comparison-table}
| Merkmal | JdbcTemplate | NamedParameterJdbc | JOOQ | CrudRepository |
|---------|-------------|-------------------|------|----------------|
| SQL-Sicherheit | String | String | Typsicherer DSL | Aus Methodenname generiert |
| Prüfungen zur Kompilierzeit | Keine | Keine | Vollständig | Teilweise |
| IDE-Unterstützung | Keine | Keine | Autovervollständigung | Hinweise zu Methodennamen |
| Lernkurve | Gering | Gering | Mittel | Gering |
| SQL-Flexibilität | Vollständig | Vollständig | Vollständig | Eingeschränkt (@Query verwenden) |

## Stolperfallen {#gotchas}

- `BeanPropertyRowMapper` ordnet nach Spaltennamen-Konvention zu (`user_name` -> `setUserName()`) – Abweichung = null
- `queryForObject` wirft `EmptyResultDataAccessException`, wenn keine Zeilen vorhanden sind – mit try/catch abfangen oder `query()` + Stream verwenden
- JOOQ benötigt einen Code-Generierungsschritt – nach Schemaänderungen ausführen
- CrudRepository-Methodennamen sind konventionsabhängig: `findByNameContaining` funktioniert, `findByNameLike` benötigt `%` im Parameter
- Veraltet: `queryForObject(sql, args, rowMapper)` – stattdessen `queryForObject(sql, rowMapper, args...)` verwenden

## Siehe auch {#see-also}

- [[spring-data-jpa-hibernate]] - JPA/Hibernate-ORM-Ansatz
- [[spring-boot-configuration]] - DataSource- und Connection-Pool-Konfiguration
- [[database-migrations]] - Schema-Evolution mit Flyway/Liquibase
