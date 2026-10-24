---
title: "Spring Data JPA und Hibernate"
category: concepts
tags: [java-spring, spring, jpa, hibernate, orm, entity, relationships, transactions]
level: 3
source_sha256: 226164e5c5108a53d0670573c98d6c4d113c6f8294dfb3a66e414c84cd82a20c
translation: machine
translated_at: '2026-10-24'
---
# Spring Data JPA und Hibernate {#spring-data-jpa-and-hibernate}

JPA (Jakarta Persistence API) ist die Spezifikation, Hibernate ORM die Implementierung. Behandelt werden Entity-Mapping, Beziehungen, Vererbungsstrategien, Transaktionen und Caching.

## Key Facts {#key-facts}

- JPA ist eine Spezifikation; Hibernate ist die verbreitetste Implementierung
- `@Entity` markiert eine Klasse als auf eine DB-Tabelle abgebildet; erfordert einen Konstruktor ohne Argumente
- `GenerationType.IDENTITY` = DB-Auto-Increment; `SEQUENCE` = DB-Sequenz
- `@Enumerated(EnumType.STRING)` speichert den Enum-Namen (nicht den Ordinalwert) - immer STRING verwenden
- `@Transactional` garantiert Atomizität - jede Exception rollt alle Operationen zurück
- Der First-Level-Cache ist innerhalb einer Session automatisch aktiv; der Second-Level-Cache erfordert Konfiguration
- `JpaRepository` erweitert `ListCrudRepository` um Paginierung, Flush und Query-by-Example

## Patterns {#patterns}

### Entity Mapping {#entity-mapping}
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

### Relationships {#relationships}
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

### JPA Repository {#jpa-repository}
```java
public interface UserJpaRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByEmail(String email);
    void deleteByEmail(String email);
}
```

### Auditing {#auditing}
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

Properties: `readOnly`, `propagation` (REQUIRED als Standard, REQUIRES_NEW), `isolation`, `rollbackFor`.

### Inheritance Strategies {#inheritance-strategies}
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

### Second-Level Cache {#second-level-cache}
```java
@Entity @Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class MenuItemEntity { }  // frequently read, rarely changed
```

## Gotchas {#gotchas}

- Der Standardwert von `@Enumerated` ist `ORDINAL` (Integer) - das Hinzufügen von Enum-Werten ändert bestehende Daten. Immer `STRING` verwenden
- `@Transactional` funktioniert nur bei öffentlichen Methoden und wenn der Aufruf über den Spring-Proxy erfolgt (nicht `this.method()`)
- `ddl-auto=update` ist nur für die Entwicklung gedacht - für Produktion Flyway/Liquibase zur Schema-Verwaltung verwenden
- LazyInitializationException: Zugriff auf eine Lazy-Collection außerhalb der Transaktion - `@Transactional` verwenden oder eager laden
- `@JoinTable` und Ownership: Die Entity mit `@JoinTable` ist die besitzende Seite; die andere Seite verwendet `mappedBy`
- `save()` auf einer detachten Entity ohne Versionsfeld kann gleichzeitige Änderungen überschreiben - optimistisches Locking mit `@Version` verwenden

## See Also {#see-also}

- [[spring-data-access-evolution]] - JDBC und weniger abstrahierte Alternativen
- [[database-migrations]] - Flyway und Liquibase für die Schema-Verwaltung
- [[spring-nosql-databases]] - NoSQL-Alternativen zu JPA
