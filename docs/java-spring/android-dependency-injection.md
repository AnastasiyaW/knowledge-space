---
title: Android Dependency Injection with Hilt
category: concepts
tags: [java-spring, android, hilt, dagger, dependency-injection, di]
---

# Android Dependency Injection with Hilt

Hilt (built on Dagger) as the recommended DI framework for Android. Parallels Spring's IoC container but with Android lifecycle awareness.

## Key Facts

- Hilt is Google's recommended DI for Android - built on Dagger 2 with less boilerplate
- `@HiltAndroidApp` on Application class enables Hilt
- `@AndroidEntryPoint` on Activity/Fragment enables injection
- `@HiltViewModel` with `@Inject constructor` for ViewModel injection
- `@Module` + `@InstallIn` for providing third-party dependencies
- `@Singleton`, `@ActivityScoped`, `@ViewModelScoped` control lifecycle
- Parallels Spring's `@Component`/`@Service`/`@Bean` pattern

## Patterns

### Application Setup
```kotlin
@HiltAndroidApp
class MyApp : Application()
```

### Activity/Fragment Injection
```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject lateinit var repository: UserRepository
}
```

### ViewModel Injection
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // No ViewModelFactory needed!
}
```

### Module for Third-Party Dependencies
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides @Singleton
    fun provideApiService(): ApiService {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }

    @Provides @Singleton
    fun provideUserRepository(api: ApiService, dao: UserDao): UserRepository {
        return UserRepository(api, dao)
    }

    @Provides @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(context, AppDatabase::class.java, "app_db").build()
    }

    @Provides
    fun provideUserDao(db: AppDatabase): UserDao = db.userDao()
}
```

### Spring IoC vs Hilt Comparison
| Spring | Hilt | Purpose |
|--------|------|---------|
| `@Component` | `@Inject constructor` | Auto-discovered bean |
| `@Service` | `@Inject constructor` | Business logic |
| `@Bean` in `@Configuration` | `@Provides` in `@Module` | Explicit creation |
| `@Autowired` | `@Inject` | Field/constructor injection |
| `@Scope("singleton")` | `@Singleton` | Scope control |
| `@Qualifier` | `@Qualifier` + `@Named` | Disambiguation |

## Gotchas

- `@Inject lateinit var` fields must NOT be private in Activities/Fragments
- `@HiltViewModel` requires `@Inject constructor` - cannot use no-arg constructor
- Hilt modules must specify `@InstallIn` with appropriate component (`SingletonComponent`, `ActivityComponent`, etc.)
- Missing `@AndroidEntryPoint` on Fragment's host Activity causes runtime crash

## See Also

- [[spring-ioc-beans]] - Spring's equivalent IoC container
- [[android-architecture-mvvm]] - ViewModel injection patterns
- [[kotlin-coroutines]] - Coroutines in injected services
