---
title: "Android-Dependency-Injection mit Hilt"
category: concepts
tags: [java-spring, android, hilt, dagger, dependency-injection, di]
level: 3
source_sha256: fe06830ce381515e8c2580b8a7f36566a7f4416914b0e49760ec71fb433859b7
translation: machine
translated_at: '2026-10-24'
---
# Android-Dependency-Injection mit Hilt {#android-dependency-injection-with-hilt}

Hilt (aufbauend auf Dagger) als empfohlenes DI-Framework für Android. Vergleichbar mit Springs IoC-Container, bietet aber Android-Lifecycle-Bewusstsein.

## Wichtige Fakten {#key-facts}

- Hilt ist Googles empfohlenes DI-Framework für Android – aufbauend auf Dagger 2 mit weniger Boilerplate-Code
- `@HiltAndroidApp` in der Application-Klasse aktiviert Hilt
- `@AndroidEntryPoint` in Activity/Fragment aktiviert die Injektion
- `@HiltViewModel` mit `@Inject constructor` für die ViewModel-Injektion
- `@Module` + `@InstallIn` zur Bereitstellung von Abhängigkeiten aus Drittbibliotheken
- `@Singleton`, `@ActivityScoped`, `@ViewModelScoped` steuern den Lebenszyklus
- Entspricht dem Muster `@Component`/`@Service`/`@Bean` aus Spring

## Muster {#patterns}

### Application-Setup {#application-setup}
```kotlin
@HiltAndroidApp
class MyApp : Application()
```

### Activity/Fragment-Injektion {#activityfragment-injection}
```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject lateinit var repository: UserRepository
}
```

### ViewModel-Injektion {#viewmodel-injection}
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // No ViewModelFactory needed!
}
```

### Modul für Drittbibliotheks-Abhängigkeiten {#module-for-third-party-dependencies}
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

### Vergleich: Spring IoC vs. Hilt {#spring-ioc-vs-hilt-comparison}
| Spring | Hilt | Zweck |
|--------|------|---------|
| `@Component` | `@Inject constructor` | Automatisch erkannte Bean |
| `@Service` | `@Inject constructor` | Geschäftslogik |
| `@Bean` in `@Configuration` | `@Provides` in `@Module` | Explizite Erzeugung |
| `@Autowired` | `@Inject` | Feld-/Konstruktorinjektion |
| `@Scope("singleton")` | `@Singleton` | Steuerung des Scopes |
| `@Qualifier` | `@Qualifier` + `@Named` | Eindeutige Zuordnung |

## Fallstricke {#gotchas}

- `@Inject lateinit var`-Felder dürfen in Activities/Fragments NICHT `private` sein
- `@HiltViewModel` erfordert `@Inject constructor` – ein Konstruktor ohne Argumente ist nicht möglich
- Hilt-Module müssen `@InstallIn` mit der passenden Komponente angeben (`SingletonComponent`, `ActivityComponent` usw.)
- Fehlendes `@AndroidEntryPoint` an der Host-Activity eines Fragments führt zu einem Laufzeitabsturz

## Siehe auch {#see-also}

- [[spring-ioc-beans]] - Das Spring-Pendant zum IoC-Container
- [[android-architecture-mvvm]] - Injektionsmuster für ViewModels
- [[kotlin-coroutines]] - Coroutines in injizierten Services
