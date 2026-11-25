---
title: "Spring IoC-Container, DI und Bean-Verwaltung"
category: concepts
tags: [java-spring, spring, ioc, dependency-injection, beans, configuration, lifecycle]
level: 3
source_sha256: 0363351615e1c11bc9649ab0079817d862aaf9689ab073d4ac6c5cc344c84ecb
translation: machine
translated_at: '2026-10-24'
---
# Spring IoC-Container, DI und Bean-Verwaltung {#spring-ioc-container-di-and-bean-management}

Das Inversion-of-Control-Prinzip (IoC), Arten der Dependency Injection, Bean-Scopes, Lifecycle-Callbacks, bedingte Beans und die Grundlagen der Auto-Konfiguration in Spring Boot.

## Wichtige Fakten {#key-facts}

- IoC = Das Framework steuert die Erzeugung und den Lebenszyklus von Objekten, nicht der Entwickler
- Der Spring IoC-Container (Application Context) verwaltet alle Beans
- Constructor Injection wird empfohlen: Unveränderlichkeit, klare Abhängigkeiten, testbar, schlägt früh fehl
- Field Injection (`@Autowired` auf Feldern) verbirgt Abhängigkeiten und verhindert `final` - in Produktivcode vermeiden
- Singleton-Scope (Standard) = eine Instanz pro Container; Prototype = bei jeder Anforderung eine neue Instanz
- `@ComponentScan` (automatisch in `@SpringBootApplication`) erkennt annotierte Klassen beim Start
- `@Bean` in `@Configuration` für die explizite Bean-Erzeugung (Klassen von Drittanbietern, komplexe Logik)

## Muster {#patterns}

### Arten der Dependency Injection {#dependency-injection-types}
```java
// 1. Constructor Injection (RECOMMENDED)
@Service
public class UserService {
    private final UserRepo userRepo;  // final = immutable
    public UserService(UserRepo userRepo) {
        this.userRepo = userRepo;     // @Autowired optional with single constructor
    }
}

// 2. Setter Injection (for optional deps)
@Service
public class UserService {
    private UserRepo userRepo;
    @Autowired
    public void setUserRepo(UserRepo userRepo) { this.userRepo = userRepo; }
}

// 3. Field Injection (AVOID - testing difficulties)
@Service
public class UserService {
    @Autowired private UserRepo userRepo;
}
```

### Stereotype-Annotationen {#stereotype-annotations}
```java
@Component      // generic managed component
@Repository     // data access (adds exception translation)
@Service        // business logic
@Controller     // MVC web controller
@RestController // @Controller + @ResponseBody
@Configuration  // contains @Bean definitions
```

### Auflösung von Mehrdeutigkeiten {#resolving-ambiguity}
```java
// @Qualifier - specify by name
public UserService(@Qualifier("userRepoJdbc") UserRepo repo) { ... }

// @Primary - mark default implementation
@Repository @Primary
public class UserRepoJpa implements UserRepo { ... }
```

### Bean-Scopes {#bean-scopes}
```java
@Scope("singleton")   // default - one instance per container
@Scope("prototype")   // new instance on every injection
@Scope("request")     // per HTTP request (web only)
@Scope("session")     // per HTTP session (web only)

// Session-scoped bean in singleton requires proxy
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ShoppingCart { ... }
```

### Lifecycle-Callbacks einer Bean {#bean-lifecycle-callbacks}
```java
@Component
public class MyBean {
    @PostConstruct
    public void init() { /* after DI complete, before use */ }

    @PreDestroy
    public void cleanup() { /* before destruction */ }
}
```

Reihenfolge: Instanziierung -> DI -> `@PostConstruct` -> Bereit -> `@PreDestroy` -> Zerstörung

### @Bean in @Configuration {#bean-in-configuration}
```java
@Configuration
public class AppConfig {
    @Bean(name = "userRepoBean")
    public UserRepo userRepo() {
        return new UserRepoImplArrayList();
    }
}
```

### Bedingte Bean-Registrierung {#conditional-bean-registration}
```java
@Bean
@ConditionalOnProperty(name = "feature.delivery", havingValue = "true")
public DeliveryService deliveryService() { ... }

@Bean
@ConditionalOnMissingBean(UserRepo.class)
public UserRepo defaultRepo() { ... }  // fallback only

@Bean
@ConditionalOnClass(name = "com.example.SomeClass")
public MyBean myBean() { ... }  // only if class on classpath
```

### Lazy Initialization mit @Lazy {#lazy-initialization}
```java
@Component @Lazy
public class HeavyService { }  // created on first use, not at startup
```

### Logging (SLF4J + Logback) {#logging-slf4j-logback}
```java
// Manual
private static final Logger log = LoggerFactory.getLogger(UserService.class);
log.info("Saving user: {}", user.getEmail());

// With Lombok
@Slf4j
@Service
public class UserService { log.info("..."); }
```

## Fallstricke {#gotchas}

- Singleton-Beans mit veränderlichem Zustand führen zu Nebenläufigkeitsproblemen - Singletons zustandslos halten
- Eine Session-scoped Bean, die in ein Singleton injiziert wird, erfordert `proxyMode = TARGET_CLASS`
- `@PostConstruct` läuft NACH Abschluss der gesamten DI - die injizierten Abhängigkeiten können dort sicher verwendet werden
- Field Injection funktioniert, erschwert aber Unit-Tests (Reflection oder Spring-Kontext nötig)
- Mehrere Implementierungen ohne `@Qualifier` oder `@Primary` führen zu einer `NoUniqueBeanDefinitionException`
- `@Bean`-Methoden in `@Configuration`-Klassen werden per Proxy umhüllt - ruft man eine `@Bean`-Methode aus einer anderen auf, erhält man dieselbe Singleton-Instanz zurück

## Siehe auch {#see-also}

- [[spring-boot-configuration]] - Anwendungseigenschaften, Profile, externalisierte Konfiguration
- [[spring-mvc-rest]] - Controller, die diese Beans verwenden
- [[spring-security]] - Security-Beans und Konfiguration der Filterkette
