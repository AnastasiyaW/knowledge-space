---
title: "Spring Data JPA et Hibernate"
category: concepts
tags: [java-spring, spring, jpa, hibernate, orm, entity, relationships, transactions]
level: 3
source_sha256: 226164e5c5108a53d0670573c98d6c4d113c6f8294dfb3a66e414c84cd82a20c
translation: machine
translated_at: '2026-10-24'
---
# Spring Data JPA et Hibernate {#spring-data-jpa-and-hibernate}

Spécification JPA (Jakarta Persistence API), implémentation ORM Hibernate, mapping d'entités, relations, stratégies d'héritage, transactions et mise en cache.

## Points clés {#key-facts}

- JPA est une spécification ; Hibernate est l'implémentation la plus répandue
- `@Entity` marque une classe comme mappée sur une table de la base de données ; elle nécessite un constructeur sans argument
- `GenerationType.IDENTITY` = auto-incrémentation de la base de données ; `SEQUENCE` = séquence de la base de données
- `@Enumerated(EnumType.STRING)` stocke le nom de l'énumération (et non son ordinal) - toujours utiliser STRING
- `@Transactional` garantit l'atomicité - toute exception annule l'ensemble des opérations
- Le cache de premier niveau est automatique au sein d'une session ; le cache de second niveau nécessite une configuration
- `JpaRepository` étend `ListCrudRepository` + pagination + flush + query-by-example

## Modèles {#patterns}

### Mapping d'entités {#entity-mapping}
```java
@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @Enumerated(EnumType.STRING)
    private UserRole role;

    public UserEntity() {}  // JPA requires no-arg constructor
}
```

### Relations {#relationships}
```java
// @ManyToOne / @OneToMany
@Entity public class OrderEntity {
    @ManyToOne
    @JoinColumn(name = "user_id")
    private UserEntity user;
}
@Entity public class UserEntity {
    @OneToMany(mappedBy = "user")
    private List<OrderEntity> orders;
}

// @ManyToMany
@Entity public class OrderEntity {
    @ManyToMany
    @JoinTable(name = "order_menu_items",
        joinColumns = @JoinColumn(name = "order_id"),
        inverseJoinColumns = @JoinColumn(name = "menu_item_id"))
    private List<MenuItemEntity> items;
}

// @OneToOne
@Entity public class DeliveryEntity {
    @OneToOne
    @JoinColumn(name = "order_id")
    private OrderEntity order;
}
```

### Repository JPA {#jpa-repository}
```java
public interface UserJpaRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByEmail(String email);
    void deleteByEmail(String email);
}
```

### Audit {#auditing}
```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class OrderEntity {
    @CreatedDate @Column(updatable = false)
    private LocalDateTime createdAt;
    @LastModifiedDate
    private LocalDateTime updatedAt;
}

@Configuration @EnableJpaAuditing
public class JpaConfig {}
```

### @Transactional {#transactional}
```java
@Service
public class OrderService {
    @Transactional
    public Order createOrder(OrderDto dto) {
        User user = userRepo.findById(dto.getUserId()).orElseThrow();
        Order order = new Order(user, resolveItems(dto.getItemIds()));
        orderRepo.save(order);
        deliveryRepo.save(new Delivery(order));
        // If any step fails, everything rolls back
        return order;
    }

    @Transactional(readOnly = true)  // optimization for read-only
    public List<Order> getOrders() { return orderRepo.findAll(); }
}
```

Propriétés : `readOnly`, `propagation` (REQUIRED par défaut, REQUIRES_NEW), `isolation`, `rollbackFor`.

### Stratégies d'héritage {#inheritance-strategies}
```java
// SINGLE_TABLE (default) - all types in one table, discriminator column
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "user_type")
public class UserEntity { ... }
@DiscriminatorValue("ADMIN")
public class AdminEntity extends UserEntity { ... }

// TABLE_PER_CLASS - each class gets own table
// JOINED - base table + subclass tables with FK joins
```

### Cache de second niveau {#second-level-cache}
```java
@Entity @Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class MenuItemEntity { }  // frequently read, rarely changed
```

## Pièges {#gotchas}

- La valeur par défaut de `@Enumerated` est `ORDINAL` (entier) - ajouter des valeurs à l'énumération modifie les données existantes. Toujours utiliser `STRING`
- `@Transactional` ne fonctionne que sur les méthodes publiques et lorsqu'elle est appelée via le proxy Spring (pas `this.method()`)
- `ddl-auto=update` est réservé au développement - utiliser Flyway/Liquibase pour la gestion du schéma en production
- LazyInitializationException : accès à une collection paresseuse en dehors d'une transaction - utiliser `@Transactional` ou charger la collection en mode eager
- Propriété de `@JoinTable` : l'entité portant `@JoinTable` est le côté propriétaire ; l'autre côté utilise `mappedBy`
- `save()` sur une entité détachée sans champ de version peut écraser des modifications concurrentes - utiliser le verrouillage optimiste avec `@Version`

## Voir aussi {#see-also}

- [[spring-data-access-evolution]] - JDBC et alternatives de plus bas niveau
- [[database-migrations]] - Flyway et Liquibase pour la gestion du schéma
- [[spring-nosql-databases]] - alternatives NoSQL à JPA
