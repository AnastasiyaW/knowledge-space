---
title: "Datenbankmigrationen - Flyway und Liquibase"
category: reference
tags: [java-spring, spring, flyway, liquibase, migrations, schema, database]
level: 3
source_sha256: 3484660a00c719a5fe26873f60348a6e2069fa3a907d0614f12d5182fa41fe16
translation: machine
translated_at: '2026-10-24'
---
# Datenbankmigrationen - Flyway und Liquibase {#database-migrations-flyway-and-liquibase}

Kontrollierte, versionierte Weiterentwicklung von Datenbankschemata mit Flyway (SQL-basiert) und Liquibase (mehrere Formate). Unverzichtbar für Produktivumgebungen, in denen `ddl-auto` nicht ausreicht.

## Wichtige Fakten {#key-facts}

- Beide Tools erfassen angewendete Änderungen in einer Metadatentabelle, um eine erneute Ausführung zu verhindern
- Flyway: SQL-Dateien mit versionierter Namenskonvention `V{n}__{description}.sql`
- Liquibase: XML-/YAML-/JSON-/SQL-Changesets, unterstützt Rollback, datenbankunabhängig
- Für Produktivbetrieb `ddl-auto=none` oder `validate` verwenden und das Schema den Migrationstools überlassen
- Migrationen sind nach der Anwendung unveränderlich - eine bereits ausgeführte Migrationsdatei niemals bearbeiten

## Muster {#patterns}

### Flyway {#flyway}
```text
src/main/resources/db/migration/
  V1__initial_schema.sql
  V2__add_phone_column.sql
  V3__create_deliveries_table.sql
```

Namenskonvention: `V{version}__{description}.sql` (zwei Unterstriche). Versionen sind geordnet und unveränderlich.

```properties
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

Verfolgt wird in der Tabelle `flyway_schema_history`.

### Liquibase {#liquibase}
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

Verfolgt wird in der Tabelle `DATABASECHANGELOG`.

### Vergleich {#comparison}
| Merkmal | Flyway | Liquibase |
|---------|--------|-----------|
| Format | Nur SQL | XML/YAML/JSON/SQL |
| Rollback | Kostenpflichtige Funktion | Integriert |
| DB-unabhängig | SQL pro DB | Abstrakte Changesets |
| Komplexität | Einfach, konventionsbasiert | Flexibler, mehr Konfiguration |
| Benennung | Versionsgeordnete Dateien | Changeset-IDs |

## Fallstricke {#gotchas}

- Flyway: Das Bearbeiten einer bereits angewendeten Migration führt beim Start zu einem Checksum-Mismatch-Fehler
- Liquibase: `id` und `author` eines Changesets müssen innerhalb eines Changelogs eindeutig sein
- Beide Tools laufen standardmäßig beim Anwendungsstart - eine fehlgeschlagene Migration blockiert den Start
- `baseline-on-migrate` (Flyway) wird benötigt, wenn Flyway zu einer bestehenden Datenbank mit Daten hinzugefügt wird

## Siehe auch {#see-also}

- [[spring-data-jpa-hibernate]] - Entity-Mapping, das durch Migrationen unterstützt wird
- [[spring-boot-configuration]] - DDL-auto-Einstellungen
- [[spring-nosql-databases]] - NoSQL-Datenbanken benötigen in der Regel keine Migrationstools
