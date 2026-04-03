---
title: Spring Boot Project Setup and Configuration
category: reference
tags: [java-spring, spring-boot, configuration, properties, maven, gradle]
---

# Spring Boot Project Setup and Configuration

Spring Boot project initialization, application properties, build tools (Maven/Gradle), project structure, and clean architecture layering.

## Key Facts

- Spring Initializr (start.spring.io) generates project skeleton with selected dependencies
- `@SpringBootApplication` combines `@Configuration`, `@EnableAutoConfiguration`, `@ComponentScan`
- `application.properties` or `application.yml` for externalized configuration
- Maven (pom.xml) or Gradle Kotlin (build.gradle.kts) for dependency management
- HikariCP is Spring Boot's default connection pool
- `spring.jpa.hibernate.ddl-auto`: `none`/`validate` for production, `update`/`create` for dev

## Patterns

### Clean Architecture Layers
```
domain/          Business logic, models, repository interfaces
  ├── model/     Plain domain objects (no framework annotations)
  ├── repo/      Repository interfaces (WHAT, not HOW)
  └── service/   Business rules (interactors)
data/            Database implementations
  ├── entity/    JPA/JDBC entities with persistence annotations
  ├── repo/      Repository implementations (adapters)
  └── mapper/    Entity <-> Domain model mapping
presentation/    Controllers, DTOs, view templates
  ├── controller/
  ├── dto/       Request/response objects with validation
  └── config/    Spring configurations
```

### Application Properties
```properties
# Server
server.port=8080

# DataSource
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=postgres
spring.datasource.password=postgres
spring.datasource.driver-class-name=org.postgresql.Driver

# HikariCP connection pool
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.connection-timeout=30000

# JPA
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

### Adapter Pattern - Decoupling Domain from Data
```java
// Domain interface
public interface UserRepo {
    User saveUser(User user);
    User getUserByEmail(String email);
}

// Data layer adapter
@Repository
public class UserRepoAdapter implements UserRepo {
    private final UserCrudRepository crudRepo;
    private final ModelMapper mapper;

    @Override
    public User saveUser(User user) {
        UserEntity entity = mapper.map(user, UserEntity.class);
        UserEntity saved = crudRepo.save(entity);
        return mapper.map(saved, User.class);
    }
}
```

### Domain Models (No Framework Deps)
```java
// Java with Lombok
@Data
public class User {
    private Long id;
    private String name;
    private String email;
    private String password;
}

// Kotlin
data class User(
    val id: Long? = null,
    val name: String,
    val email: String,
    val password: String
)
```

### ModelMapper for Entity-Domain Conversion
```java
@Configuration
public class MapperConfig {
    @Bean
    public ModelMapper modelMapper() {
        ModelMapper mapper = new ModelMapper();
        mapper.getConfiguration().setMatchingStrategy(MatchingStrategies.STRICT);
        return mapper;
    }
}
```

## Gotchas

- Don't write code you won't use - add repository methods only when needed
- Domain models should have no Spring/JPA annotations - that belongs on entities
- Use `Long` (wrapper) not `long` (primitive) for IDs - generics require wrapper types
- For prices use `Integer` for simple cases, `BigDecimal` for production (fractional currency)
- `ddl-auto=update` never drops columns/tables - safe for dev but use migrations for production

## See Also

- [[spring-ioc-beans]] - IoC container and bean management
- [[spring-data-jpa-hibernate]] - JPA entity configuration
- [[spring-data-access-evolution]] - JDBC to JPA progression
- [[database-migrations]] - Flyway and Liquibase
