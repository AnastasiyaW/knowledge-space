---
title: "Configuration et initialisation d'un projet Spring Boot"
category: reference
tags: [java-spring, spring-boot, configuration, properties, maven, gradle]
level: 3
source_sha256: 7ecb1b0b81ab51b7fa84294e1a085982c855078527616c38bf1c878050bbd160
translation: machine
translated_at: '2026-10-24'
---
# Configuration et initialisation d'un projet Spring Boot {#spring-boot-project-setup-and-configuration}

Initialisation d'un projet Spring Boot, propriétés de l'application, outils de build (Maven/Gradle), structure du projet et séparation en couches de l'architecture propre.

## Points clés {#key-facts}

- Spring Initializr (start.spring.io) génère le squelette du projet avec les dépendances sélectionnées
- `@SpringBootApplication` combine `@Configuration`, `@EnableAutoConfiguration`, `@ComponentScan`
- `application.properties` ou `application.yml` pour la configuration externalisée
- Maven (pom.xml) ou Gradle Kotlin (build.gradle.kts) pour la gestion des dépendances
- HikariCP est le pool de connexions par défaut de Spring Boot
- `spring.jpa.hibernate.ddl-auto` : `none`/`validate` pour la production, `update`/`create` pour le développement

## Patterns {#patterns}

### Couches de l'architecture propre {#clean-architecture-layers}
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

### Propriétés de l'application {#application-properties}
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

### Pattern Adapter - Découplage du domaine et des données {#adapter-pattern-decoupling-domain-from-data}
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

### Modèles de domaine (sans dépendances au framework) {#domain-models-no-framework-deps}
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

### ModelMapper pour la conversion entité-domaine {#modelmapper-for-entity-domain-conversion}
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

## Pièges à éviter {#gotchas}

- N'écrivez pas de code que vous n'utiliserez pas : ajoutez des méthodes de repository uniquement en cas de besoin
- Les modèles de domaine ne doivent contenir aucune annotation Spring/JPA : elles appartiennent aux entités
- Utilisez `Long` (wrapper) et non `long` (primitif) pour les identifiants : les génériques exigent des types wrapper
- Pour les prix, utilisez `Integer` dans les cas simples et `BigDecimal` en production (monnaie avec décimales)
- `ddl-auto=update` ne supprime jamais de colonnes ni de tables : c'est sûr pour le développement, mais utilisez des migrations en production

## Voir aussi {#see-also}

- [[spring-ioc-beans]] - Conteneur IoC et gestion des beans
- [[spring-data-jpa-hibernate]] - Configuration des entités JPA
- [[spring-data-access-evolution]] - Évolution de JDBC vers JPA
- [[database-migrations]] - Flyway et Liquibase
