---
title: "Accès aux données Spring - De JDBC à Spring Data"
category: concepts
tags: [java-spring, spring, jdbc, jdbctemplate, jooq, spring-data, crud-repository, sql]
level: 3
source_sha256: c6ea483f5ff34cfce47f9991769a4a74f48e154e304b896851352d222c42d04c
translation: machine
translated_at: '2026-10-24'
---
# Accès aux données Spring - De JDBC à Spring Data {#spring-data-access-from-jdbc-to-spring-data}

Évolution de l'accès aux données dans Spring : JDBC brut -> PreparedStatement -> JdbcTemplate -> NamedParameterJdbcTemplate -> JOOQ -> Spring Data JDBC (CrudRepository). Chaque niveau réduit le code répétitif et renforce la sécurité.

## Points clés {#key-facts}

- Statement brut = vulnérable à l'injection SQL ; PreparedStatement sépare le SQL des données
- JdbcTemplate gère la gestion des connexions, la traduction des exceptions et le mapping des résultats
- NamedParameterJdbcTemplate remplace les `?` positionnels par `:paramName`
- JOOQ apporte une sécurité de type SQL à la compilation grâce au code généré à partir du schéma de la base
- Spring Data CrudRepository génère le SQL à partir des noms de méthodes : aucun SQL manuel pour le CRUD
- `CrudRepository.save()` : ID null = INSERT, ID non null = UPDATE
- Problème N+1 : utiliser des requêtes JOIN ou un chargement par lots pour éviter les sous-requêtes par entité

## Patrons {#patterns}

### Niveau 1 : JdbcTemplate {#level-1-jdbctemplate}
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

Méthodes principales : `update()` (INSERT/UPDATE/DELETE), `queryForObject()` (une seule ligne), `query()` (liste), `batchUpdate()` (opérations par lots).

### Niveau 2 : NamedParameterJdbcTemplate {#level-2-namedparameterjdbctemplate}
```java
String sql = "INSERT INTO users (name, email) VALUES (:name, :email)";
MapSqlParameterSource params = new MapSqlParameterSource()
    .addValue("name", user.getName())
    .addValue("email", user.getEmail());
namedJdbc.update(sql, params);
```

### Niveau 3 : JOOQ (SQL type-safe) {#level-3-jooq-type-safe-sql}
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

JOOQ génère des classes Java à partir du schéma de la base : `USERS.EMAIL.eq(email)` détecte les fautes de frappe à la compilation.

### Niveau 4 : Spring Data CrudRepository {#level-4-spring-data-crudrepository}
```java
public interface UserCrudRepository extends ListCrudRepository<UserEntity, Long> {
    UserEntity findByEmail(String email);
    List<UserEntity> findByNameContaining(String part);
    void deleteByEmail(String email);
}
```

### Conventions de nommage des méthodes {#method-name-conventions}
| Nom de méthode | SQL généré |
|------------|---------------|
| `findByEmail(email)` | `WHERE email = ?` |
| `findByNameContaining(part)` | `WHERE name LIKE '%part%'` |
| `findByPriceGreaterThan(n)` | `WHERE price > ?` |
| `countByStatus(s)` | `SELECT COUNT(*) WHERE status = ?` |
| `deleteByEmail(email)` | `DELETE WHERE email = ?` |

### @Query personnalisé {#custom-query}
```java
@Query("SELECT * FROM orders WHERE status = :status ORDER BY date_time DESC")
List<OrderEntity> findByStatus(@Param("status") String status);
```

### Résoudre le problème N+1 avec des JOIN {#solving-n1-with-joins}
```sql
SELECT o.*, u.name as user_name, mi.name as item_name
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_menu_items omi ON o.id = omi.order_id
LEFT JOIN menu_items mi ON omi.menu_item_id = mi.id
WHERE o.status = :status
```

### Tableau comparatif {#comparison-table}
| Critère | JdbcTemplate | NamedParameterJdbc | JOOQ | CrudRepository |
|---------|-------------|-------------------|------|----------------|
| Sécurité SQL | Chaînes de caractères | Chaînes de caractères | DSL type-safe | Généré à partir du nom de méthode |
| Vérifications à la compilation | Aucune | Aucune | Complètes | Partielles |
| Support IDE | Aucun | Aucun | Autocomplétion | Indices sur le nom de méthode |
| Courbe d'apprentissage | Faible | Faible | Moyenne | Faible |
| Flexibilité SQL | Complète | Complète | Complète | Limitée (utiliser @Query) |

## Pièges {#gotchas}

- `BeanPropertyRowMapper` associe les colonnes selon une convention de nommage (`user_name` -> `setUserName()`) : une non-correspondance donne `null`
- `queryForObject` lève `EmptyResultDataAccessException` si aucune ligne n'est retournée : l'encapsuler dans un try/catch ou utiliser `query()` + stream
- JOOQ nécessite une étape de génération de code : l'exécuter après chaque modification du schéma
- Les noms de méthodes CrudRepository sont sensibles aux conventions : `findByNameContaining` fonctionne, alors que `findByNameLike` exige le `%` dans le paramètre
- Obsolète : `queryForObject(sql, args, rowMapper)` : utiliser `queryForObject(sql, rowMapper, args...)`

## Voir aussi {#see-also}

- [[spring-data-jpa-hibernate]] - Approche ORM JPA/Hibernate
- [[spring-boot-configuration]] - Configuration du DataSource et du pool de connexions
- [[database-migrations]] - Évolution du schéma avec Flyway/Liquibase
