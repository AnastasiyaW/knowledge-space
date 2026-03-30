---
title: Clean Architecture in Spring
category: patterns
tags: [spring, clean-architecture, hexagonal, ports-adapters, domain-driven, layered]
---
# Clean Architecture in Spring

## Key Facts

- Clean Architecture separates code into layers with strict dependency rules: outer layers depend on inner layers, NEVER the reverse
- **Domain layer** (innermost): entities, value objects, repository interfaces - zero framework dependencies
- **Application layer**: use cases / service interfaces - orchestrates domain logic
- **Infrastructure layer** (outermost): Spring controllers, JPA repositories, external APIs, configs
- Also known as Hexagonal Architecture or Ports & Adapters pattern
- Domain repo interfaces (ports) are defined in domain layer; Spring Data repos (adapters) implement them
- Mapper classes convert between domain models, JPA entities, DTOs, and API response objects
- Benefits: testable domain logic, swappable database/framework, clear responsibility boundaries
- See [[spring-ioc-container]] for how DI wires adapter implementations to domain interfaces
- See [[spring-data-nosql]] for how adapters support multiple database technologies

## Patterns

### Package structure

```
com.example.delivery/
  domain/
    model/
      User.java             # Domain entity (POJO, no annotations)
      Order.java
      MenuItem.java
      OrderStatus.java       # Enum
    repository/
      UserRepo.java          # Interface (port) - no Spring
      OrderRepo.java
    exception/
      UserNotFoundException.java
  application/
    service/
      UserService.java       # Uses domain repos, contains business logic
      OrderService.java
  infrastructure/
    persistence/
      jpa/
        entity/
          UserJpaEntity.java   # @Entity - JPA specific
          OrderJpaEntity.java
        repository/
          UserJpaRepository.java  # extends JpaRepository
        adapter/
          UserJpaAdapter.java     # implements UserRepo using JPA
        mapper/
          UserJpaMapper.java      # domain <-> JPA entity
      mongo/
        entity/
          UserMongoDocument.java  # @Document - Mongo specific
        adapter/
          UserMongoAdapter.java   # implements UserRepo using Mongo
    web/
      controller/
        UserController.java   # @RestController
      dto/
        UserDto.java          # API response model
        CreateUserRequest.java
      mapper/
        UserDtoMapper.java    # domain <-> DTO
    config/
      SecurityConfig.java
      DatabaseConfig.java
```

### Domain layer (no framework dependencies)

```java
// Domain model - plain Java, no annotations
public class User {
    private final UUID id;
    private final String name;
    private final String email;
    private final UserRole role;

    public User(UUID id, String name, String email, UserRole role) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.role = role;
    }
    // getters only - immutable
}

// Domain repository interface (port)
public interface UserRepo {
    User findById(UUID id);
    User findByEmail(String email);
    User save(User user);
    void deleteById(UUID id);
    List<User> findAll();
}

// Domain exception
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(UUID id) {
        super("User not found: " + id);
    }
}
```

### Application service layer

```java
@Service
@Transactional(readOnly = true)
public class UserService {
    private final UserRepo userRepo;
    private final PasswordEncoder encoder;

    public UserService(UserRepo userRepo, PasswordEncoder encoder) {
        this.userRepo = userRepo;
        this.encoder = encoder;
    }

    public User findById(UUID id) {
        return userRepo.findById(id);
    }

    @Transactional
    public User register(String name, String email, String rawPassword) {
        User existing = userRepo.findByEmail(email);
        if (existing != null) {
            throw new EmailAlreadyExistsException(email);
        }
        User user = new User(
            UUID.randomUUID(),
            name,
            email,
            UserRole.USER
        );
        return userRepo.save(user);
    }
}
```

### Infrastructure adapter (JPA implementation)

```java
@Repository
public class UserJpaAdapter implements UserRepo {
    private final UserJpaRepository jpaRepo;
    private final UserJpaMapper mapper;

    public UserJpaAdapter(UserJpaRepository jpaRepo, UserJpaMapper mapper) {
        this.jpaRepo = jpaRepo;
        this.mapper = mapper;
    }

    @Override
    public User findById(UUID id) {
        return jpaRepo.findById(id)
            .map(mapper::toDomain)
            .orElseThrow(() -> new UserNotFoundException(id));
    }

    @Override
    public User save(User user) {
        UserJpaEntity entity = mapper.toEntity(user);
        UserJpaEntity saved = jpaRepo.save(entity);
        return mapper.toDomain(saved);
    }

    @Override
    public List<User> findAll() {
        return jpaRepo.findAll().stream()
            .map(mapper::toDomain)
            .toList();
    }
}

// Mapper between domain and JPA entity
@Component
public class UserJpaMapper {
    public User toDomain(UserJpaEntity entity) {
        return new User(
            entity.getId(),
            entity.getName(),
            entity.getEmail(),
            entity.getRole()
        );
    }

    public UserJpaEntity toEntity(User user) {
        UserJpaEntity entity = new UserJpaEntity();
        entity.setId(user.getId());
        entity.setName(user.getName());
        entity.setEmail(user.getEmail());
        entity.setRole(user.getRole());
        return entity;
    }
}
```

### Swapping database implementations

```java
// Switch from JPA to MongoDB by changing one config
@Configuration
@Profile("jpa")
public class JpaConfig {
    @Bean
    public UserRepo userRepo(UserJpaRepository jpaRepo, UserJpaMapper mapper) {
        return new UserJpaAdapter(jpaRepo, mapper);
    }
}

@Configuration
@Profile("mongo")
public class MongoConfig {
    @Bean
    public UserRepo userRepo(UserMongoRepository mongoRepo, UserMongoMapper mapper) {
        return new UserMongoAdapter(mongoRepo, mapper);
    }
}

// Domain service doesn't change - it depends on UserRepo interface
```

## Gotchas

- **Symptom**: Domain model has `@Entity`, `@Column` annotations -> **Cause**: Mixing domain with persistence concern -> **Fix**: Create separate JPA entity classes; map between domain and entity in adapter
- **Symptom**: Service directly returns JPA entity to controller -> **Cause**: No DTO layer; changes to entity break API contract -> **Fix**: Use DTOs for API layer, map in controller or mapper service
- **Symptom**: Too many mapper classes / boilerplate -> **Cause**: Manual mapping between 4 layers -> **Fix**: Use MapStruct library for compile-time mapping, or reduce layers for simple CRUD apps
- **Symptom**: Domain tests require Spring context -> **Cause**: Domain classes use Spring annotations -> **Fix**: Domain layer must have ZERO Spring dependencies; only infrastructure uses Spring

## See Also

- [[spring-ioc-container]] - DI wires adapters to domain ports
- [[spring-data-jpa]] - JPA adapter implementation details
- [[spring-data-nosql]] - NoSQL adapter implementations
- [[android-architecture]] - Same Clean Architecture principles on Android
- Robert C. Martin: [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
