---
title: "Spring Data NoSQL – Cassandra, MongoDB, Redis, Neo4j"
category: concepts
tags: [java-spring, spring, nosql, cassandra, mongodb, redis, neo4j, spring-data]
level: 3
source_sha256: 8e6e457b11142780184a35961b9063a80e29f14499d84193310a3505a03a0990
translation: machine
translated_at: '2026-10-24'
---
# Spring Data NoSQL – Cassandra, MongoDB, Redis, Neo4j {#spring-data-nosql-cassandra-mongodb-redis-neo4j}

Spring-Data-Abstraktionen für NoSQL-Datenbanken: Cassandra (Column-Family), MongoDB (Dokument), Redis (Key-Value) und Neo4j (Graph). Dasselbe Repository-Muster gilt für alle.

## Kernfakten {#key-facts}

- Spring Data bietet eine einheitliche CrudRepository-Schnittstelle für alle NoSQL-Datenbanken
- Die Entity-Annotation unterscheidet sich: `@Entity` (JPA), `@Table` (Cassandra), `@Document` (MongoDB), `@RedisHash` (Redis), `@Node` (Neo4j)
- ID-Typen variieren: `Long` (JPA), `UUID` (Cassandra), `String/ObjectId` (MongoDB), `String` (Redis), `Long` (Neo4j)
- Cassandra: keine JOINs, der Partitionsschlüssel bestimmt die Datenverteilung, unterstützt Collection-Spalten
- MongoDB: flexibles Schema, BSON-Dokumente, horizontale Skalierung über Sharding
- Redis: In-Memory mit Lesezugriffen im Sub-Millisekundenbereich, ideal für Caching und Sessions
- Neo4j: Graph-Traversierung über Cypher, ideal für vernetzte Daten (Soziale Netzwerke, Empfehlungen)

## Muster {#patterns}

### Cassandra {#cassandra}
```java
@Table("users")
public class UserEntity {
    @PrimaryKey
    private UUID id;           // Cassandra uses UUID
    private String name;
    private String email;
}

@Table("orders")
public class OrderEntity {
    @PrimaryKeyColumn(type = PrimaryKeyType.PARTITIONED)
    private UUID userId;       // partition key
    @PrimaryKeyColumn(type = PrimaryKeyType.CLUSTERED, ordinal = 0)
    private UUID id;
    private List<UUID> menuItemIds;  // collection column
}

public interface UserCassandraRepo extends ListCrudRepository<UserEntity, UUID> {
    UserEntity findByEmail(String email);
}
```

### MongoDB {#mongodb}
```java
@Document(collection = "users")
public class UserEntity {
    @Id
    private String id;         // MongoDB ObjectId
    private String name;
    private String email;
}

@Document(collection = "orders")
public class OrderEntity {
    @Id private String id;
    private String userId;              // reference by ID
    private List<String> menuItemIds;   // embedded list
}

public interface UserMongoRepo extends MongoRepository<UserEntity, String> {
    UserEntity findByEmail(String email);
}
```

### Redis {#redis}
```java
@RedisHash("users")
public class UserEntity {
    @Id private String id;
    private String name;
    private String email;
    // Stored as hash: users:{id} -> {name, email, ...}
}

// RedisTemplate for advanced operations
redisTemplate.opsForValue().set("key", value);
redisTemplate.opsForHash().put("hash", "field", value);
redisTemplate.opsForList().rightPush("list", value);
```

### Neo4j {#neo4j}
```java
@Node("User")
public class UserEntity {
    @Id @GeneratedValue
    private Long id;
    private String name;
    @Relationship(type = "PLACED_ORDER", direction = OUTGOING)
    private List<OrderEntity> orders;
}
// Graph: (User)-[:PLACED_ORDER]->(Order)-[:CONTAINS]->(MenuItem)
```

### Vergleichstabelle {#comparison-table}
| | PostgreSQL | Cassandra | MongoDB | Redis | Neo4j |
|---|-----------|-----------|---------|-------|-------|
| Modell | Tabellen | Column-Families | Dokumente | Key-Value | Graph |
| Schema | Fest | Fest/Tabelle | Flexibel | Schemalos | Nodes+Relationships |
| Skalierung | Vertikal | Horizontal | Horizontal | In-Memory | Vertikal |
| JOINs | Volles SQL | Keine | Eingeschränkt | Keine | Graph-Traversierung |
| Ideal für | ACID, komplexe Abfragen | Hohe Schreiblast, Zeitreihen | Schnelle Iteration | Cache, Sessions | Vernetzte Daten |

### Austauschbare Datenschicht {#swappable-data-layer}
```java
@Service
public class UserService {
    private final UserRepo userRepo;
    // Switch DB by changing qualifier:
    public UserService(@Qualifier("userRepoCassandra") UserRepo repo) {
        this.userRepo = repo;
    }
}
```

Dieselbe Domänenschicht, unterschiedliche Datenadapter. Darin liegt der praktische Nutzen einer sauberen Architektur.

## Stolperfallen {#gotchas}

- Cassandra: ORDER BY auf Nicht-Schlüsselspalten ist nicht möglich – in Java mit Streams sortieren
- Cassandra: UUID-<->-Long-Konvertierung ist nötig, wenn die Domäne Long-IDs verwendet
- MongoDB: `@Document` statt `@Entity`; String-IDs statt Long
- Redis: im Vergleich zu JPA/Mongo eingeschränkte Abfragemöglichkeiten – überwiegend schlüsselbasierte Suche
- Neo4j: Beziehungen haben Richtung und Typ – für effiziente Traversierung sorgfältig modellieren
- Alle NoSQL-Datenbanken: ohne JOINs bedeutet das Denormalisierung oder mehrere Abfragen für zusammenhängende Daten

## Siehe auch {#see-also}

- [[spring-data-jpa-hibernate]] - Relationale Alternative
- [[spring-data-access-evolution]] - SQL-basierter Datenzugriff
- [[spring-boot-configuration]] - Verbindungseigenschaften je Datenbank
