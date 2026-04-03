---
title: Spring Data JPA and Hibernate
category: concepts
tags: [java-spring, spring, jpa, hibernate, orm, entity, relationships, transactions]
---

# Spring Data JPA and Hibernate

JPA (Jakarta Persistence API) specification, Hibernate ORM implementation, entity mapping, relationships, inheritance strategies, transactions, and caching.

## Key Facts

- JPA is a specification; Hibernate is the most popular implementation
- `@Entity` marks a class as mapped to a DB table; requires no-arg constructor
- `GenerationType.IDENTITY` = DB auto-increment; `SEQUENCE` = DB sequence
- `@Enumerated(EnumType.STRING)` stores enum name (not ordinal) - always use STRING
- `@Transactional` ensures atomicity - any exception rolls back all operations
- First-level cache is automatic within a session; second-level cache requires configuration
- `JpaRepository` extends `ListCrudRepository` + pagination + flush + query-by-example

## Patterns

### Entity Mapping
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

### Relationships
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

### JPA Repository
```java
public interface UserJpaRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByEmail(String email);
    void deleteByEmail(String email);
}
```

### Auditing
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

### @Transactional
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

Properties: `readOnly`, `propagation` (REQUIRED default, REQUIRES_NEW), `isolation`, `rollbackFor`.

### Inheritance Strategies
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

### Second-Level Cache
```java
@Entity @Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class MenuItemEntity { }  // frequently read, rarely changed
```

## Gotchas

- `@Enumerated` default is `ORDINAL` (integer) - adding enum values changes existing data. Always use `STRING`
- `@Transactional` only works on public methods and when called through Spring proxy (not `this.method()`)
- `ddl-auto=update` is for dev only - use Flyway/Liquibase for production schema management
- LazyInitializationException: accessing lazy collection outside transaction - use `@Transactional` or fetch eagerly
- `@JoinTable` ownership: the entity with `@JoinTable` is the owning side; the other uses `mappedBy`
- `save()` on detached entity without version field can overwrite concurrent changes - use optimistic locking with `@Version`

## See Also

- [[spring-data-access-evolution]] - JDBC and lower-level alternatives
- [[database-migrations]] - Flyway and Liquibase for schema management
- [[spring-nosql-databases]] - NoSQL alternatives to JPA
