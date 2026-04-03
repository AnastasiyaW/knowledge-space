---
title: Spring IoC Container, DI, and Bean Management
category: concepts
tags: [java-spring, spring, ioc, dependency-injection, beans, configuration, lifecycle]
---

# Spring IoC Container, DI, and Bean Management

Inversion of Control (IoC) principle, dependency injection types, bean scopes, lifecycle callbacks, conditional beans, and Spring Boot auto-configuration fundamentals.

## Key Facts

- IoC = framework controls object creation and lifecycle, not the developer
- Spring IoC Container (Application Context) manages all beans
- Constructor injection is recommended: immutability, clear deps, testable, fails fast
- Field injection (`@Autowired` on fields) hides dependencies and prevents `final` - avoid in production
- Singleton scope (default) = one instance per container; Prototype = new instance every request
- `@ComponentScan` (auto in `@SpringBootApplication`) discovers annotated classes at startup
- `@Bean` in `@Configuration` for explicit bean creation (third-party classes, complex logic)

## Patterns

### Dependency Injection Types
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

### Stereotype Annotations
```java
@Component      // generic managed component
@Repository     // data access (adds exception translation)
@Service        // business logic
@Controller     // MVC web controller
@RestController // @Controller + @ResponseBody
@Configuration  // contains @Bean definitions
```

### Resolving Ambiguity
```java
// @Qualifier - specify by name
public UserService(@Qualifier("userRepoJdbc") UserRepo repo) { ... }

// @Primary - mark default implementation
@Repository @Primary
public class UserRepoJpa implements UserRepo { ... }
```

### Bean Scopes
```java
@Scope("singleton")   // default - one instance per container
@Scope("prototype")   // new instance on every injection
@Scope("request")     // per HTTP request (web only)
@Scope("session")     // per HTTP session (web only)

// Session-scoped bean in singleton requires proxy
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ShoppingCart { ... }
```

### Bean Lifecycle Callbacks
```java
@Component
public class MyBean {
    @PostConstruct
    public void init() { /* after DI complete, before use */ }

    @PreDestroy
    public void cleanup() { /* before destruction */ }
}
```

Order: Instantiation -> DI -> `@PostConstruct` -> Ready -> `@PreDestroy` -> Destruction

### @Bean in @Configuration
```java
@Configuration
public class AppConfig {
    @Bean(name = "userRepoBean")
    public UserRepo userRepo() {
        return new UserRepoImplArrayList();
    }
}
```

### Conditional Bean Registration
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

### @Lazy Initialization
```java
@Component @Lazy
public class HeavyService { }  // created on first use, not at startup
```

### Logging (SLF4J + Logback)
```java
// Manual
private static final Logger log = LoggerFactory.getLogger(UserService.class);
log.info("Saving user: {}", user.getEmail());

// With Lombok
@Slf4j
@Service
public class UserService { log.info("..."); }
```

## Gotchas

- Singleton beans with mutable state cause concurrency issues - keep singletons stateless
- Session-scoped bean injected into singleton requires `proxyMode = TARGET_CLASS`
- `@PostConstruct` runs AFTER all DI is complete - safe to use injected dependencies
- Field injection works but makes unit testing harder (need reflection or Spring context)
- Multiple implementations without `@Qualifier` or `@Primary` causes `NoUniqueBeanDefinitionException`
- `@Bean` methods in `@Configuration` classes are proxied - calling one `@Bean` method from another returns the same singleton instance

## See Also

- [[spring-boot-configuration]] - Application properties, profiles, externalized config
- [[spring-mvc-rest]] - Controllers that consume these beans
- [[spring-security]] - Security beans and filter chain configuration
