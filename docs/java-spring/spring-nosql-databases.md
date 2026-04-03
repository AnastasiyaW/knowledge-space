---
title: Spring Data NoSQL - Cassandra, MongoDB, Redis, Neo4j
category: concepts
tags: [java-spring, spring, nosql, cassandra, mongodb, redis, neo4j, spring-data]
---

# Spring Data NoSQL - Cassandra, MongoDB, Redis, Neo4j

Spring Data abstractions for NoSQL databases: Cassandra (column-family), MongoDB (document), Redis (key-value), and Neo4j (graph). Same repository pattern across all.

## Key Facts

- Spring Data provides consistent CrudRepository interface across all NoSQL databases
- Entity annotation differs: `@Entity` (JPA), `@Table` (Cassandra), `@Document` (MongoDB), `@RedisHash` (Redis), `@Node` (Neo4j)
- ID types vary: `Long` (JPA), `UUID` (Cassandra), `String/ObjectId` (MongoDB), `String` (Redis), `Long` (Neo4j)
- Cassandra: no JOINs, partition key determines data distribution, supports collection columns
- MongoDB: flexible schema, BSON documents, horizontal scaling via sharding
- Redis: in-memory sub-millisecond reads, ideal for caching/sessions
- Neo4j: graph traversal via Cypher, ideal for connected data (social, recommendations)

## Patterns

### Cassandra
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

### MongoDB
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

### Redis
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

### Neo4j
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

### Comparison Table
| | PostgreSQL | Cassandra | MongoDB | Redis | Neo4j |
|---|-----------|-----------|---------|-------|-------|
| Model | Tables | Column families | Documents | Key-value | Graph |
| Schema | Fixed | Fixed/table | Flexible | Schemaless | Nodes+Rels |
| Scaling | Vertical | Horizontal | Horizontal | In-memory | Vertical |
| JOINs | Full SQL | None | Limited | None | Graph traversal |
| Best for | ACID, complex queries | High write, time-series | Rapid iteration | Cache, sessions | Connected data |

### Swappable Data Layer
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

Same domain layer, different data adapters. This is the practical benefit of clean architecture.

## Gotchas

- Cassandra: cannot ORDER BY non-key columns - sort in Java with Streams
- Cassandra: UUID <-> Long conversion needed when domain uses Long IDs
- MongoDB: `@Document` not `@Entity`; String IDs not Long
- Redis: limited query capabilities compared to JPA/Mongo - mostly key-based lookup
- Neo4j: relationships have direction and type - model carefully for efficient traversal
- All NoSQL: no JOINs means denormalization or multiple queries for related data

## See Also

- [[spring-data-jpa-hibernate]] - Relational alternative
- [[spring-data-access-evolution]] - SQL-based data access
- [[spring-boot-configuration]] - Connection properties per database
