---
title: Database Migrations - Flyway and Liquibase
category: reference
tags: [java-spring, spring, flyway, liquibase, migrations, schema, database]
---

# Database Migrations - Flyway and Liquibase

Controlled, versioned database schema evolution using Flyway (SQL-based) and Liquibase (multi-format). Essential for production deployments where `ddl-auto` is insufficient.

## Key Facts

- Both track applied changes in a metadata table to prevent re-execution
- Flyway: SQL files with versioned naming convention `V{n}__{description}.sql`
- Liquibase: XML/YAML/JSON/SQL changesets, supports rollback, database-agnostic
- For production, use `ddl-auto=none` or `validate` and let migration tools manage schema
- Migrations are immutable once applied - never edit an already-executed migration file

## Patterns

### Flyway
```
src/main/resources/db/migration/
  V1__initial_schema.sql
  V2__add_phone_column.sql
  V3__create_deliveries_table.sql
```

Naming: `V{version}__{description}.sql` (two underscores). Versions are ordered and immutable.

```properties
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

Tracks in `flyway_schema_history` table.

### Liquibase
```xml
<databaseChangeLog>
    <changeSet id="1" author="dev">
        <createTable tableName="users">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true"/>
            </column>
            <column name="name" type="VARCHAR(255)"/>
            <column name="email" type="VARCHAR(255)">
                <constraints unique="true"/>
            </column>
        </createTable>
    </changeSet>
</databaseChangeLog>
```

```properties
spring.liquibase.enabled=true
spring.liquibase.change-log=classpath:db/changelog/changelog.xml
```

Tracks in `DATABASECHANGELOG` table.

### Comparison
| Feature | Flyway | Liquibase |
|---------|--------|-----------|
| Format | SQL only | XML/YAML/JSON/SQL |
| Rollback | Paid feature | Built-in |
| DB-agnostic | SQL per DB | Abstract changesets |
| Complexity | Simple, convention-based | More flexible, more config |
| Naming | Version-ordered files | Changeset IDs |

## Gotchas

- Flyway: editing an already-applied migration causes checksum mismatch error at startup
- Liquibase: changeset `id` + `author` must be unique within a changelog
- Both tools run during application startup by default - failed migration blocks startup
- `baseline-on-migrate` (Flyway) is needed when adding Flyway to existing DB with data

## See Also

- [[spring-data-jpa-hibernate]] - Entity mapping that migrations support
- [[spring-boot-configuration]] - DDL-auto settings
- [[spring-nosql-databases]] - NoSQL databases typically don't need migration tools
