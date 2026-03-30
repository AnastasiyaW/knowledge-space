---
title: Spring Data NoSQL
category: concepts
tags: [spring, nosql, mongodb, redis, cassandra, neo4j, spring-data]
---
# Spring Data NoSQL

## Key Facts

- Spring Data provides unified repository abstraction across SQL and NoSQL databases
- **MongoDB** - document database, stores JSON-like documents, `@Document` annotation, very fast for complex nested data
- **Redis** - in-memory key-value store, highest performance, `@RedisHash` annotation, ideal for caching and sessions
- **Cassandra** - wide-column store, massive horizontal scaling, `@Table` with `@PrimaryKey`, eventual consistency
- **Neo4j** - graph database, stores nodes and relationships, `@Node` annotation, Cypher query language
- Each NoSQL module has its own starter dependency: `spring-boot-starter-data-mongodb`, `spring-boot-starter-data-redis`, etc.
- Repository interfaces follow same pattern: extend `MongoRepository`, `CassandraRepository`, `Neo4jRepository`
- Clean Architecture pattern: domain repo interfaces with separate adapters for each database technology
- See [[spring-data-jpa]] for relational database access
- See [[spring-boot-setup]] for configuring database connections

## Patterns

### MongoDB setup and entity

```properties
# application.properties
spring.data.mongodb.uri=mongodb://localhost:27017/myapp
```

```java
@Document(collection = "users")
public class UserDocument {
    @Id
    private String id;

    @Indexed(unique = true)
    private String email;

    private String name;
    private String password;

    // Embedded document (nested)
    private Address address;

    @CreatedDate
    private LocalDateTime createdAt;
}

public interface UserMongoRepository extends MongoRepository<UserDocument, String> {
    Optional<UserDocument> findByEmail(String email);
    List<UserDocument> findByNameContaining(String name);

    @Query("{ 'address.city': ?0 }")
    List<UserDocument> findByCity(String city);
}
```

### Redis setup and entity

```properties
# application.properties
spring.data.redis.host=localhost
spring.data.redis.port=6379
```

```java
@RedisHash("users")
public class UserRedis {
    @Id
    private String id;

    @Indexed
    private String email;

    private String name;

    @TimeToLive
    private Long ttl;  // expiration in seconds
}

public interface UserRedisRepository extends CrudRepository<UserRedis, String> {
    Optional<UserRedis> findByEmail(String email);
}

// Redis as cache (more common use)
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10));
        return RedisCacheManager.builder(factory)
            .cacheDefaults(config)
            .build();
    }
}

@Service
public class ProductService {
    @Cacheable("products")
    public Product findById(Long id) {
        return productRepo.findById(id).orElseThrow();
    }

    @CacheEvict(value = "products", key = "#id")
    public void update(Long id, Product product) {
        productRepo.save(product);
    }
}
```

### Cassandra setup and entity

```properties
# application.properties
spring.cassandra.contact-points=localhost
spring.cassandra.port=9042
spring.cassandra.keyspace-name=myapp
spring.cassandra.local-datacenter=datacenter1
```

```java
@Table("orders")
public class OrderCassandra {
    @PrimaryKey
    private UUID orderId;

    private UUID userId;
    private BigDecimal totalPrice;
    private String status;

    @Column("created_at")
    private Instant createdAt;
}

public interface OrderCassandraRepository
        extends CassandraRepository<OrderCassandra, UUID> {
    List<OrderCassandra> findByUserId(UUID userId);
}
```

### Neo4j setup and entity

```properties
# application.properties
spring.neo4j.uri=bolt://localhost:7687
spring.neo4j.authentication.username=neo4j
spring.neo4j.authentication.password=secret
```

```java
@Node("User")
public class UserNode {
    @Id @GeneratedValue
    private Long id;

    private String name;
    private String email;

    @Relationship(type = "PLACED", direction = Relationship.Direction.OUTGOING)
    private List<OrderNode> orders;

    @Relationship(type = "FRIEND_OF")
    private Set<UserNode> friends;
}

@Node("Order")
public class OrderNode {
    @Id @GeneratedValue
    private Long id;
    private BigDecimal totalPrice;
    private String status;
}

public interface UserNeo4jRepository extends Neo4jRepository<UserNode, Long> {
    Optional<UserNode> findByEmail(String email);

    @Query("MATCH (u:User)-[:FRIEND_OF]-(friend:User) WHERE u.email = $email RETURN friend")
    List<UserNode> findFriends(@Param("email") String email);
}
```

### Clean Architecture adapter pattern

```java
// Domain repository interface (database-agnostic)
public interface UserRepo {
    User findById(UUID id);
    User save(User user);
    void delete(UUID id);
}

// Adapter for MongoDB implementation
@Repository
public class UserMongoAdapter implements UserRepo {
    private final UserMongoRepository mongoRepo;

    @Override
    public User findById(UUID id) {
        return mongoRepo.findById(id.toString())
            .map(this::toDomain)
            .orElseThrow(() -> new UserNotFoundException(id));
    }

    @Override
    public User save(User user) {
        UserDocument doc = toDocument(user);
        return toDomain(mongoRepo.save(doc));
    }

    private User toDomain(UserDocument doc) { /* mapping */ }
    private UserDocument toDocument(User user) { /* mapping */ }
}
```

## Gotchas

- **Symptom**: MongoDB `@Id` field doesn't match expected format -> **Cause**: MongoDB generates `ObjectId` by default; UUID field requires string conversion -> **Fix**: Use `String` as ID type or configure custom ID generation
- **Symptom**: Redis data disappears -> **Cause**: `@TimeToLive` set too low, or Redis memory full with eviction policy -> **Fix**: Check TTL values; configure `maxmemory-policy` in Redis
- **Symptom**: Cassandra query fails with "ALLOW FILTERING" error -> **Cause**: Query not using partition key -> **Fix**: Design tables around query patterns; Cassandra requires queries to use partition key
- **Symptom**: Neo4j relationship loading causes infinite recursion -> **Cause**: Bidirectional relationship without depth control -> **Fix**: Set `@Relationship` direction properly; use `@Depth` annotation or query with explicit depth

## See Also

- [[spring-data-jpa]] - Relational database access with same repository pattern
- [[spring-boot-setup]] - Configuring database connections
- [[spring-ioc-container]] - How Spring manages repository beans
- Spring Data MongoDB: [Reference](https://docs.spring.io/spring-data/mongodb/docs/current/reference/html/)
- Spring Data Redis: [Reference](https://docs.spring.io/spring-data/redis/docs/current/reference/html/)
- Spring Data Neo4j: [Reference](https://docs.spring.io/spring-data/neo4j/docs/current/reference/html/)
