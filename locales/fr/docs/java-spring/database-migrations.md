---
title: "Migrations de base de données - Flyway et Liquibase"
category: reference
tags: [java-spring, spring, flyway, liquibase, migrations, schema, database]
level: 3
source_sha256: 3484660a00c719a5fe26873f60348a6e2069fa3a907d0614f12d5182fa41fe16
translation: machine
translated_at: '2026-10-24'
---
# Migrations de base de données - Flyway et Liquibase {#database-migrations-flyway-and-liquibase}

Évolution contrôlée et versionnée du schéma de base de données avec Flyway (basé sur SQL) et Liquibase (multi-format). Indispensable pour les déploiements en production où `ddl-auto` ne suffit pas.

## Points clés {#key-facts}

- Les deux outils enregistrent les changements appliqués dans une table de métadonnées pour éviter leur réexécution
- Flyway : fichiers SQL suivant la convention de nommage versionnée `V{n}__{description}.sql`
- Liquibase : changesets en XML/YAML/JSON/SQL, prend en charge le rollback, indépendant de la base de données
- En production, utiliser `ddl-auto=none` ou `validate` et laisser les outils de migration gérer le schéma
- Les migrations sont immuables une fois appliquées : ne jamais modifier un fichier de migration déjà exécuté

## Modèles {#patterns}

### Flyway {#flyway}
```text
src/main/resources/db/migration/
  V1__initial_schema.sql
  V2__add_phone_column.sql
  V3__create_deliveries_table.sql
```

Nommage : `V{version}__{description}.sql` (deux underscores). Les versions sont ordonnées et immuables.

```properties
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

Suivi dans la table `flyway_schema_history`.

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

Suivi dans la table `DATABASECHANGELOG`.

### Comparaison {#comparison}
| Fonctionnalité | Flyway | Liquibase |
|---------|--------|-----------|
| Format | SQL uniquement | XML/YAML/JSON/SQL |
| Rollback | Fonctionnalité payante | Intégré |
| Indépendant de la BD | SQL par BD | Changesets abstraits |
| Complexité | Simple, basé sur des conventions | Plus flexible, plus de configuration |
| Nommage | Fichiers ordonnés par version | Identifiants de changesets |

## Pièges à éviter {#gotchas}

- Flyway : modifier une migration déjà appliquée provoque une erreur de checksum au démarrage
- Liquibase : les `id` + `author` d'un changeset doivent être uniques au sein d'un changelog
- Par défaut, les deux outils s'exécutent au démarrage de l'application : une migration en échec bloque le démarrage
- `baseline-on-migrate` (Flyway) est nécessaire pour ajouter Flyway à une base existante contenant des données

## Voir aussi {#see-also}

- [[spring-data-jpa-hibernate]] - Mapping des entités que les migrations prennent en charge
- [[spring-boot-configuration]] - Paramètres DDL-auto
- [[spring-nosql-databases]] - Les bases NoSQL n'ont généralement pas besoin d'outils de migration
