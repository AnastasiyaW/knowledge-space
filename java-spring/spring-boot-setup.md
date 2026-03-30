---
title: Spring Boot Setup and Project Structure
category: reference
tags: [spring-boot, maven, gradle, spring-initializr, project-structure, application-properties]
---
# Spring Boot Setup and Project Structure

## Key Facts

- Spring Initializr at [start.spring.io](https://start.spring.io) generates project scaffolding with chosen dependencies
- Two build systems: **Maven** (XML-based `pom.xml`) or **Gradle** (Groovy/Kotlin DSL `build.gradle`)
- Spring Boot auto-configuration reduces boilerplate - detects classpath and configures beans automatically
- `application.properties` or `application.yml` in `src/main/resources/` configures application behavior
- Main class annotated with `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`
- Embedded server (Tomcat/Jetty/Undertow) - no separate WAR deployment needed
- Spring Boot DevTools enables hot reload during development
- Profiles (`spring.profiles.active`) allow environment-specific configuration (dev, staging, prod)
- See [[spring-ioc-container]] for how beans and dependency injection work
- See [[spring-mvc]] for building web controllers

## Patterns

### Project generation (start.spring.io)

```
Project:    Maven / Gradle
Language:   Java / Kotlin
Spring Boot: 3.x (latest stable)
Group:      com.example
Artifact:   myapp
Dependencies:
  - Spring Web
  - Spring Data JPA
  - Spring Security (if needed)
  - H2 Database (for dev)
  - PostgreSQL Driver (for prod)
  - Lombok
  - Spring Boot DevTools
```

### Standard project structure

```
src/
  main/
    java/com/example/myapp/
      MyappApplication.java          # @SpringBootApplication entry point
      controller/
        UserController.java          # REST / MVC controllers
      service/
        UserService.java             # Business logic
      repository/
        UserRepository.java          # Data access
      model/ (or entity/)
        User.java                    # Domain objects / JPA entities
      config/
        SecurityConfig.java          # Configuration classes
      dto/
        UserDto.java                 # Data transfer objects
    resources/
      application.properties         # Configuration
      application-dev.properties     # Dev profile config
      static/                        # Static files (CSS, JS)
      templates/                     # Thymeleaf templates
  test/
    java/com/example/myapp/
      MyappApplicationTests.java
pom.xml  (or build.gradle)
```

### Main application class

```java
@SpringBootApplication
public class MyappApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyappApplication.class, args);
    }
}
```

### application.properties

```properties
# Server
server.port=8080
server.servlet.context-path=/api

# Database (PostgreSQL)
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=pass
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect

# Logging
logging.level.root=INFO
logging.level.com.example=DEBUG

# Active profile
spring.profiles.active=dev
```

### Maven pom.xml (key dependencies)

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

### Gradle Kotlin DSL (build.gradle.kts)

```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.20"
    kotlin("plugin.spring") version "1.9.20"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

## Gotchas

- **Symptom**: Application won't start, `BeanCreationException` -> **Cause**: Missing dependency in pom.xml/build.gradle, or misconfigured database URL -> **Fix**: Check dependency versions match Spring Boot parent; verify database is running
- **Symptom**: `@ComponentScan` doesn't find beans -> **Cause**: Beans are in packages outside the main application's package hierarchy -> **Fix**: Place main class in root package, or explicitly set `@ComponentScan(basePackages = "...")`
- **Symptom**: Profile-specific properties not loading -> **Cause**: File named `application-dev.properties` but profile not activated -> **Fix**: Set `spring.profiles.active=dev` in base properties, env var, or JVM arg `-Dspring.profiles.active=dev`

## See Also

- [[spring-ioc-container]] - Dependency injection and bean management
- [[spring-mvc]] - Building web layer on top of this setup
- [[spring-data-jpa]] - Database access configuration
- [[kotlin-fundamentals]] - Using Kotlin with Spring Boot
- Spring Docs: [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- Spring Docs: [Spring Initializr](https://start.spring.io)
