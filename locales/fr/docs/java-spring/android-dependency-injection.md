---
title: "Injection de dépendances Android avec Hilt"
category: concepts
tags: [java-spring, android, hilt, dagger, dependency-injection, di]
level: 3
source_sha256: fe06830ce381515e8c2580b8a7f36566a7f4416914b0e49760ec71fb433859b7
translation: machine
translated_at: '2026-10-24'
---
# Injection de dépendances Android avec Hilt {#android-dependency-injection-with-hilt}

Hilt (construit sur Dagger) est le framework d'injection de dépendances recommandé pour Android. Il est comparable au conteneur IoC de Spring, mais prend en compte le cycle de vie Android.

## Points clés {#key-facts}

- Hilt est le framework d'injection de dépendances recommandé par Google, construit sur Dagger 2 avec moins de code répétitif
- `@HiltAndroidApp` sur la classe Application active Hilt
- `@AndroidEntryPoint` sur une Activity ou un Fragment active l'injection
- `@HiltViewModel` avec `@Inject constructor` pour l'injection dans un ViewModel
- `@Module` + `@InstallIn` pour fournir des dépendances tierces
- `@Singleton`, `@ActivityScoped`, `@ViewModelScoped` contrôlent le cycle de vie
- Équivalent du modèle `@Component`/`@Service`/`@Bean` de Spring

## Modèles {#patterns}

### Configuration de l'Application {#application-setup}
```kotlin
@HiltAndroidApp
class MyApp : Application()
```

### Injection dans une Activity/un Fragment {#activityfragment-injection}
```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject lateinit var repository: UserRepository
}
```

### Injection dans un ViewModel {#viewmodel-injection}
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // No ViewModelFactory needed!
}
```

### Module pour les dépendances tierces {#module-for-third-party-dependencies}
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

### Comparaison Spring IoC et Hilt {#spring-ioc-vs-hilt-comparison}
| Spring | Hilt | Rôle |
|--------|------|---------|
| `@Component` | `@Inject constructor` | Bean découvert automatiquement |
| `@Service` | `@Inject constructor` | Logique métier |
| `@Bean` dans `@Configuration` | `@Provides` dans `@Module` | Création explicite |
| `@Autowired` | `@Inject` | Injection par champ/constructeur |
| `@Scope("singleton")` | `@Singleton` | Contrôle de portée |
| `@Qualifier` | `@Qualifier` + `@Named` | Désambiguïsation |

## Pièges courants {#gotchas}

- Les champs `@Inject lateinit var` ne doivent PAS être privés dans les Activities/Fragments
- `@HiltViewModel` exige un `@Inject constructor` : un constructeur sans argument ne convient pas
- Les modules Hilt doivent spécifier `@InstallIn` avec le composant approprié (`SingletonComponent`, `ActivityComponent`, etc.)
- L'absence de `@AndroidEntryPoint` sur l'Activity hôte d'un Fragment provoque un plantage à l'exécution

## Voir aussi {#see-also}

- [[spring-ioc-beans]] - Équivalent Spring du conteneur IoC
- [[android-architecture-mvvm]] - Modèles d'injection pour les ViewModels
- [[kotlin-coroutines]] - Coroutines dans les services injectés
