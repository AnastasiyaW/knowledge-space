---
title: "Conteneur IoC de Spring, DI et gestion des beans"
category: concepts
tags: [java-spring, spring, ioc, dependency-injection, beans, configuration, lifecycle]
level: 3
source_sha256: 0363351615e1c11bc9649ab0079817d862aaf9689ab073d4ac6c5cc344c84ecb
translation: machine
translated_at: '2026-10-24'
---
# Conteneur IoC de Spring, DI et gestion des beans {#spring-ioc-container-di-and-bean-management}

Principe d'inversion de contrôle (IoC), types d'injection de dépendances, portées des beans, callbacks du cycle de vie, beans conditionnels et fondamentaux de l'auto-configuration de Spring Boot.

## Points clés {#key-facts}

- IoC = le framework contrôle la création des objets et leur cycle de vie, et non le développeur
- Le conteneur IoC de Spring (Application Context) gère tous les beans
- L'injection par constructeur est recommandée : immutabilité, dépendances explicites, testabilité, échec rapide
- L'injection par champ (`@Autowired` sur les champs) masque les dépendances et empêche l'usage de `final` - à éviter en production
- Portée Singleton (par défaut) = une instance par conteneur ; Prototype = une nouvelle instance à chaque requête
- `@ComponentScan` (automatique dans `@SpringBootApplication`) détecte les classes annotées au démarrage
- `@Bean` dans `@Configuration` pour la création explicite de beans (classes tierces, logique complexe)

## Modèles {#patterns}

### Types d'injection de dépendances {#dependency-injection-types}
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

### Annotations de stéréotype {#stereotype-annotations}
```java
@Component      // generic managed component
@Repository     // data access (adds exception translation)
@Service        // business logic
@Controller     // MVC web controller
@RestController // @Controller + @ResponseBody
@Configuration  // contains @Bean definitions
```

### Résolution des ambiguïtés {#resolving-ambiguity}
```java
// @Qualifier - specify by name
public UserService(@Qualifier("userRepoJdbc") UserRepo repo) { ... }

// @Primary - mark default implementation
@Repository @Primary
public class UserRepoJpa implements UserRepo { ... }
```

### Portées des beans {#bean-scopes}
```java
@Scope("singleton")   // default - one instance per container
@Scope("prototype")   // new instance on every injection
@Scope("request")     // per HTTP request (web only)
@Scope("session")     // per HTTP session (web only)

// Session-scoped bean in singleton requires proxy
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ShoppingCart { ... }
```

### Callbacks du cycle de vie des beans {#bean-lifecycle-callbacks}
```java
@Component
public class MyBean {
    @PostConstruct
    public void init() { /* after DI complete, before use */ }

    @PreDestroy
    public void cleanup() { /* before destruction */ }
}
```

Ordre : Instanciation -> DI -> `@PostConstruct` -> Prêt -> `@PreDestroy` -> Destruction

### @Bean dans @Configuration {#bean-in-configuration}
```java
@Configuration
public class AppConfig {
    @Bean(name = "userRepoBean")
    public UserRepo userRepo() {
        return new UserRepoImplArrayList();
    }
}
```

### Enregistrement conditionnel de beans {#conditional-bean-registration}
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

### Initialisation @Lazy {#lazy-initialization}
```java
@Component @Lazy
public class HeavyService { }  // created on first use, not at startup
```

### Journalisation (SLF4J + Logback) {#logging-slf4j-logback}
```java
// Manual
private static final Logger log = LoggerFactory.getLogger(UserService.class);
log.info("Saving user: {}", user.getEmail());

// With Lombok
@Slf4j
@Service
public class UserService { log.info("..."); }
```

## Pièges {#gotchas}

- Les beans singleton à état mutable provoquent des problèmes de concurrence - gardez les singletons sans état
- Un bean à portée session injecté dans un singleton nécessite `proxyMode = TARGET_CLASS`
- `@PostConstruct` s'exécute APRÈS la fin de toute l'injection de dépendances - il est sûr d'utiliser les dépendances injectées
- L'injection par champ fonctionne, mais rend les tests unitaires plus difficiles (réflexion ou contexte Spring nécessaires)
- Plusieurs implémentations sans `@Qualifier` ni `@Primary` provoquent une `NoUniqueBeanDefinitionException`
- Les méthodes `@Bean` des classes `@Configuration` sont proxifiées - appeler une méthode `@Bean` depuis une autre renvoie la même instance singleton

## Voir aussi {#see-also}

- [[spring-boot-configuration]] - Propriétés de l'application, profils, configuration externalisée
- [[spring-mvc-rest]] - Contrôleurs qui consomment ces beans
- [[spring-security]] - Beans de sécurité et configuration de la chaîne de filtres
