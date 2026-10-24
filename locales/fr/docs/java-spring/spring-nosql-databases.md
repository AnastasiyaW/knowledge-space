---
title: "Spring Data NoSQL - Cassandra, MongoDB, Redis, Neo4j"
category: concepts
tags: [java-spring, spring, nosql, cassandra, mongodb, redis, neo4j, spring-data]
level: 3
source_sha256: 8e6e457b11142780184a35961b9063a80e29f14499d84193310a3505a03a0990
translation: machine
translated_at: '2026-10-24'
---
# Spring Data NoSQL - Cassandra, MongoDB, Redis, Neo4j {#spring-data-nosql-cassandra-mongodb-redis-neo4j}

Abstractions Spring Data pour les bases NoSQL : Cassandra (familles de colonnes), MongoDB (documents), Redis (clé-valeur) et Neo4j (graphe). Le même patron de repository s'applique à toutes.

## Points clés {#key-facts}

- Spring Data fournit une interface CrudRepository cohérente pour toutes les bases NoSQL
- L'annotation d'entité diffère : `@Entity` (JPA), `@Table` (Cassandra), `@Document` (MongoDB), `@RedisHash` (Redis), `@Node` (Neo4j)
- Les types d'ID varient : `Long` (JPA), `UUID` (Cassandra), `String/ObjectId` (MongoDB), `String` (Redis), `Long` (Neo4j)
- Cassandra : pas de JOIN, la clé de partition détermine la distribution des données, prise en charge des colonnes de collection
- MongoDB : schéma flexible, documents BSON, mise à l'échelle horizontale via le sharding
- Redis : lectures en mémoire en moins d'une milliseconde, idéal pour le cache et les sessions
- Neo4j : parcours de graphe via Cypher, idéal pour les données connectées (réseaux sociaux, recommandations)

## Patterns {#patterns}

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

### Tableau comparatif {#comparison-table}
| | PostgreSQL | Cassandra | MongoDB | Redis | Neo4j |
|---|-----------|-----------|---------|-------|-------|
| Modèle | Tables | Familles de colonnes | Documents | Clé-valeur | Graphe |
| Schéma | Fixe | Fixe/table | Flexible | Sans schéma | Nœuds+relations |
| Mise à l'échelle | Verticale | Horizontale | Horizontale | En mémoire | Verticale |
| JOIN | SQL complet | Aucun | Limité | Aucun | Parcours de graphe |
| Idéal pour | ACID, requêtes complexes | Écriture intensive, séries temporelles | Itération rapide | Cache, sessions | Données connectées |

### Couche de données interchangeable {#swappable-data-layer}
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

Même couche domaine, adaptateurs de données différents. C'est l'avantage concret de l'architecture propre.

## Pièges courants {#gotchas}

- Cassandra : impossible de faire un ORDER BY sur une colonne qui n'est pas une clé, il faut trier en Java avec des Streams
- Cassandra : une conversion UUID <-> Long est nécessaire lorsque le domaine utilise des ID de type Long
- MongoDB : `@Document` et non `@Entity` ; IDs de type String et non Long
- Redis : capacités de requête limitées par rapport à JPA/Mongo, principalement des recherches par clé
- Neo4j : les relations ont une direction et un type, à modéliser avec soin pour des parcours efficaces
- Toutes les bases NoSQL : l'absence de JOIN impose une dénormalisation ou plusieurs requêtes pour les données liées

## Voir aussi {#see-also}

- [[spring-data-jpa-hibernate]] - Alternative relationnelle
- [[spring-data-access-evolution]] - Accès aux données basé sur SQL
- [[spring-boot-configuration]] - Propriétés de connexion par base de données
