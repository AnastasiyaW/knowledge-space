---
title: "Spring-Boot-Projekteinrichtung und Konfiguration"
category: reference
tags: [java-spring, spring-boot, configuration, properties, maven, gradle]
level: 3
source_sha256: 7ecb1b0b81ab51b7fa84294e1a085982c855078527616c38bf1c878050bbd160
translation: machine
translated_at: '2026-10-24'
---
# Spring-Boot-Projekteinrichtung und Konfiguration {#spring-boot-project-setup-and-configuration}

Initialisierung von Spring-Boot-Projekten, Anwendungseigenschaften, Build-Werkzeuge (Maven/Gradle), Projektstruktur und die Schichtung einer Clean Architecture.

## Wichtige Fakten {#key-facts}

- Spring Initializr (start.spring.io) erzeugt das Projektgerüst mit den ausgewählten Abhängigkeiten
- `@SpringBootApplication` kombiniert `@Configuration`, `@EnableAutoConfiguration`, `@ComponentScan`
- `application.properties` oder `application.yml` für externalisierte Konfiguration
- Maven (pom.xml) oder Gradle Kotlin (build.gradle.kts) für das Abhängigkeitsmanagement
- HikariCP ist der Standard-Verbindungspool von Spring Boot
- `spring.jpa.hibernate.ddl-auto`: `none`/`validate` für Produktion, `update`/`create` für die Entwicklung

## Muster {#patterns}

### Schichten der Clean Architecture {#clean-architecture-layers}
```php
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

### Anwendungseigenschaften {#application-properties}
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

### Adapter-Muster – Entkopplung von Domäne und Datenhaltung {#adapter-pattern-decoupling-domain-from-data}
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

### Domänenmodelle (ohne Framework-Abhängigkeiten) {#domain-models-no-framework-deps}
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

### ModelMapper für die Konvertierung zwischen Entität und Domänenmodell {#modelmapper-for-entity-domain-conversion}
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

## Fallstricke {#gotchas}

- Keinen Code schreiben, der nicht verwendet wird – Repository-Methoden erst hinzufügen, wenn sie benötigt werden
- Domänenmodelle sollten keine Spring-/JPA-Annotationen enthalten – diese gehören auf die Entitäten
- `Long` (Wrapper) statt `long` (Primitiv) für IDs verwenden – Generics erfordern Wrapper-Typen
- Für Preise `Integer` in einfachen Fällen, `BigDecimal` für Produktion verwenden (gebrochene Währungsbeträge)
- `ddl-auto=update` löscht niemals Spalten oder Tabellen – für die Entwicklung unbedenklich, für Produktion sollten jedoch Migrationen verwendet werden

## Siehe auch {#see-also}

- [[spring-ioc-beans]] - IoC-Container und Bean-Verwaltung
- [[spring-data-jpa-hibernate]] - Konfiguration von JPA-Entitäten
- [[spring-data-access-evolution]] - Weg von JDBC zu JPA
- [[database-migrations]] - Flyway und Liquibase
