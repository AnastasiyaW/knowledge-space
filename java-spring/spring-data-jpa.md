---
title: Spring Data JPA
category: concepts
tags: [spring, jpa, hibernate, orm, repository, entity, queries]
---
# Spring Data JPA

## Key Facts

- JPA (Java Persistence API) is a specification; Hibernate is the most common implementation
- Spring Data JPA generates repository implementations automatically from interface method names
- `@Entity` marks a class as JPA entity mapped to a database table
- `@Id` marks the primary key; `@GeneratedValue(strategy = GenerationType.IDENTITY)` for auto-increment
- Repository interfaces extend `JpaRepository<Entity, IdType>` - provides CRUD + pagination + sorting
- Query derivation: `findByEmailAndAge(String email, int age)` generates SQL automatically from method name
- `@Query` annotation allows custom JPQL or native SQL queries on repository methods
- `spring.jpa.hibernate.ddl-auto` controls schema management: `none`, `validate`, `update`, `create`, `create-drop`
- `@Transactional` on service methods ensures atomic database operations; rollback on unchecked exceptions
- See [[spring-ioc-container]] for how repositories are registered as beans
- See [[spring-data-nosql]] for non-relational data access

## Patterns

### Entity definition

```java
@Entity
@Table(name = "users")
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String password;

    @Enumerated(EnumType.STRING)
    private UserRole role;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Getters, setters, constructors
}
```

### Entity relationships

```java
// One-to-Many
@Entity
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private UserEntity user;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    private BigDecimal totalPrice;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;
}

@Entity
public class OrderItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_item_id")
    private MenuItem menuItem;

    private int quantity;
    private BigDecimal price;
}
```

### Repository interface

```java
public interface UserRepository extends JpaRepository<UserEntity, Long> {

    // Derived queries (generated from method name)
    Optional<UserEntity> findByEmail(String email);
    List<UserEntity> findByRole(UserRole role);
    boolean existsByEmail(String email);
    List<UserEntity> findByNameContainingIgnoreCase(String namePart);

    // Custom JPQL query
    @Query("SELECT u FROM UserEntity u WHERE u.createdAt > :date")
    List<UserEntity> findUsersCreatedAfter(@Param("date") LocalDateTime date);

    // Native SQL query
    @Query(value = "SELECT * FROM users WHERE role = :role LIMIT :limit",
           nativeQuery = true)
    List<UserEntity> findTopByRole(@Param("role") String role,
                                   @Param("limit") int limit);

    // Modifying query
    @Modifying
    @Query("UPDATE UserEntity u SET u.role = :role WHERE u.id = :id")
    int updateRole(@Param("id") Long id, @Param("role") UserRole role);
}
```

### Service layer with transactions

```java
@Service
@Transactional(readOnly = true)  // default read-only for all methods
public class OrderService {

    private final OrderRepository orderRepo;
    private final UserRepository userRepo;

    public OrderService(OrderRepository orderRepo, UserRepository userRepo) {
        this.orderRepo = orderRepo;
        this.userRepo = userRepo;
    }

    public Order findById(Long id) {
        return orderRepo.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }

    @Transactional  // read-write for mutations
    public Order createOrder(Long userId, List<OrderItemRequest> items) {
        UserEntity user = userRepo.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId));

        Order order = new Order();
        order.setUser(user);
        order.setStatus(OrderStatus.CREATED);
        order.setItems(mapToOrderItems(items, order));
        order.setTotalPrice(calculateTotal(items));

        return orderRepo.save(order);
    }

    @Transactional
    public Order updateStatus(Long orderId, OrderStatus newStatus) {
        Order order = findById(orderId);
        order.setStatus(newStatus);
        return orderRepo.save(order);
    }
}
```

### Pagination and sorting

```java
// Repository supports Pageable
Page<UserEntity> findByRole(UserRole role, Pageable pageable);

// Controller usage
@GetMapping("/users")
public Page<UserDto> getUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size,
    @RequestParam(defaultValue = "name") String sortBy) {

    Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
    return userRepo.findAll(pageable).map(this::toDto);
}
```

## Gotchas

- **Symptom**: `LazyInitializationException` -> **Cause**: Accessing lazy-loaded relation outside transaction/session -> **Fix**: Use `@Transactional` on service method, or `JOIN FETCH` in JPQL, or `@EntityGraph`
- **Symptom**: N+1 query problem - fetching list then each relation individually -> **Cause**: Default lazy loading triggers separate query per entity -> **Fix**: `@Query("SELECT o FROM Order o JOIN FETCH o.items")` or `@EntityGraph`
- **Symptom**: `ddl-auto=update` drops columns -> **Cause**: Renaming entity field generates DROP + ADD -> **Fix**: Use Flyway or Liquibase for production migrations; `ddl-auto=validate` only
- **Symptom**: `@Transactional` doesn't rollback -> **Cause**: Method catches and swallows exception, or exception is checked -> **Fix**: Re-throw, or use `@Transactional(rollbackFor = Exception.class)`
- **Symptom**: `save()` doesn't generate INSERT -> **Cause**: Entity has non-null `@Id` - JPA thinks it's an update -> **Fix**: Use `@GeneratedValue` for auto-generated IDs, or implement `Persistable<ID>` interface

## See Also

- [[spring-data-nosql]] - MongoDB, Redis, Cassandra, Neo4j data access
- [[spring-ioc-container]] - Repository beans and transaction proxies
- [[spring-mvc]] - Controllers that use repository data
- Spring Docs: [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- Hibernate Docs: [User Guide](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html)
