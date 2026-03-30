---
title: Spring IoC Container and Dependency Injection
category: concepts
tags: [spring, ioc, dependency-injection, beans, scopes, annotations, conditional]
---
# Spring IoC Container and Dependency Injection

## Key Facts

- **IoC** (Inversion of Control): Spring container creates and manages object lifecycle, not the developer
- **DI** (Dependency Injection): container injects dependencies into beans via constructor, setter, or field injection
- Constructor injection is preferred - makes dependencies explicit, supports immutability, easier to test
- `@Component` marks a class as Spring-managed bean; specialized: `@Service`, `@Repository`, `@Controller`
- `@Autowired` triggers injection; optional on constructors in single-constructor classes (Spring 4.3+)
- `@Configuration` + `@Bean` allows manual bean creation for third-party classes
- **Bean scopes**: `singleton` (default - one per container), `prototype` (new per injection), `request`, `session`
- `@ConditionalOnProperty`, `@ConditionalOnBean`, `@ConditionalOnClass` - conditional bean registration
- `@Qualifier` disambiguates when multiple beans match the injection type
- See [[spring-boot-setup]] for how auto-configuration leverages these concepts
- See [[design-patterns-creational]] for how Spring replaces manual Singleton/Factory

## Patterns

### Component scanning and stereotypes

```java
// Auto-detected via component scanning
@Component          // generic bean
@Service            // business logic layer
@Repository         // data access layer (adds exception translation)
@Controller         // MVC controller
@RestController     // REST API controller (@Controller + @ResponseBody)

// Example
@Service
public class UserService {
    private final UserRepository repo;

    // Constructor injection (preferred)
    public UserService(UserRepository repo) {
        this.repo = repo;
    }

    public User findById(Long id) {
        return repo.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

### @Configuration and @Bean

```java
@Configuration
public class AppConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}
```

### Bean scopes

```java
@Component
@Scope("singleton")   // default - one instance per container
public class SingleService { }

@Component
@Scope("prototype")   // new instance every injection / getBean()
public class PrototypeService { }

// Web scopes (require web-aware context)
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean { }

@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionScopedBean { }
```

### Qualifier for disambiguation

```java
public interface PaymentGateway {
    void charge(BigDecimal amount);
}

@Component("stripe")
public class StripeGateway implements PaymentGateway { /* ... */ }

@Component("paypal")
public class PaypalGateway implements PaymentGateway { /* ... */ }

@Service
public class OrderService {
    private final PaymentGateway gateway;

    public OrderService(@Qualifier("stripe") PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```

### Conditional bean registration

```java
// Register only if property is set
@Configuration
@ConditionalOnProperty(name = "cache.enabled", havingValue = "true")
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() { return new ConcurrentMapCacheManager(); }
}

// Register only if class is on classpath
@Configuration
@ConditionalOnClass(name = "com.mongodb.client.MongoClient")
public class MongoConfig {
    @Bean
    public MongoTemplate mongoTemplate() { /* ... */ }
}

// Register only if another bean exists
@Bean
@ConditionalOnBean(DataSource.class)
public JdbcTemplate jdbcTemplate(DataSource ds) {
    return new JdbcTemplate(ds);
}
```

### Lifecycle callbacks

```java
@Component
public class CacheWarmer {

    @PostConstruct
    public void init() {
        // called after DI is complete
        loadCacheFromDatabase();
    }

    @PreDestroy
    public void cleanup() {
        // called before bean destruction
        flushCacheToDisk();
    }
}
```

## Gotchas

- **Symptom**: `NullPointerException` on injected field -> **Cause**: Using `new MyService()` instead of letting Spring create it; or field injection without `@Autowired` -> **Fix**: Always get beans from container; prefer constructor injection
- **Symptom**: Prototype bean inside singleton doesn't create new instances -> **Cause**: Singleton holds single reference to prototype -> **Fix**: Use `ObjectFactory<T>`, `Provider<T>`, or `@Lookup` method
- **Symptom**: Circular dependency error -> **Cause**: Bean A depends on B, B depends on A via constructor -> **Fix**: Redesign to remove cycle; use setter injection as last resort; `@Lazy` on one dependency
- **Symptom**: `@Transactional` or `@Cacheable` doesn't work -> **Cause**: Self-invocation bypasses Spring proxy -> **Fix**: Call annotated method from another bean, not `this.method()`

## See Also

- [[spring-boot-setup]] - Auto-configuration that builds on IoC
- [[spring-mvc]] - Controllers as Spring beans
- [[spring-security]] - Security configuration via beans
- [[design-patterns-creational]] - Singleton and Factory patterns that Spring replaces
- Spring Docs: [IoC Container](https://docs.spring.io/spring-framework/reference/core/beans.html)
