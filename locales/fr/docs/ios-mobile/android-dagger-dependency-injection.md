---
title: "Injection de dépendances Android avec Dagger 2"
category: concepts
tags: [ios-mobile, android, dagger, dependency-injection, di, module, component, singleton]
level: 3
source_sha256: 70bf69ea65d4fb663479354f041ae3d2bdac2c351041ec221f367d871b63b6e9
translation: machine
translated_at: '2026-10-24'
---
# Injection de dépendances Android avec Dagger 2 {#android-dagger-2-dependency-injection}

Dagger 2 génère le code d'injection de dépendances à la compilation, sans réflexion ni surcoût à l'exécution. Il relie les fournisseurs (Modules) aux consommateurs (@Inject) par l'intermédiaire d'une interface Component.

## Points clés {#key-facts}

- Dagger 2 génère le code DI à la compilation : pas de réflexion, pas de surcoût à l'exécution
- Les classes `@Module` contiennent des méthodes `@Provides` qui créent les instances de dépendances
- L'interface `@Component` relie les demandes `@Inject` aux fournisseurs `@Module`
- La portée `@Singleton` crée une seule instance et la réutilise partout
- `@Inject` demande l'injection d'une dépendance (constructeur ou champ)
- `@Named("qualifier")` lève l'ambiguïté lorsque plusieurs dépendances du même type existent
- Compilez le projet pour générer la classe `DaggerAppComponent`

## Modèles {#patterns}

### Annotations principales {#core-annotations}

| Annotation | Rôle |
|------------|------|
| `@Module` | Classe qui fournit des dépendances |
| `@Provides` | Méthode d'un Module qui crée une instance |
| `@Singleton` | Créée une seule fois, réutilisée partout |
| `@Component` | Interface reliant les demandes d'injection aux fournisseurs |
| `@Inject` | Demande l'injection d'une dépendance |
| `@Named("x")` | Qualifier lorsque plusieurs dépendances du même type existent |
| `@Binds` | Méthode abstraite liant une implémentation à une interface |
| `@IntoMap` | Contribue à une Map de dépendances |

### Exemples de modules {#module-examples}

```kotlin
@Module
class AppModule(private val app: App) {
    @Provides
    @Singleton
    fun provideContext(): Context = app
}

@Module
class RestModule {
    @Provides
    @Singleton
    fun provideGson(): Gson = GsonBuilder().setLenient().create()

    @Provides
    @Singleton
    @Named("COINGECKO_API")
    fun provideRetrofit(gson: Gson, client: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl("https://api.coingecko.com/api/v3/")
            .addConverterFactory(GsonConverterFactory.create(gson))
            .client(client)
            .build()
}
```

### Interface Component {#component-interface}

```kotlin
@Singleton
@Component(modules = [
    AppModule::class,
    RestModule::class,
    ViewModelModule::class
])
interface AppComponent {
    fun inject(activity: MainActivity)
    fun inject(fragment: CurrenciesListFragment)
}
```

### Configuration de la classe Application {#application-class-setup}

```kotlin
class App : Application() {
    lateinit var appComponent: AppComponent

    override fun onCreate() {
        super.onCreate()
        appComponent = DaggerAppComponent.builder()
            .appModule(AppModule(this))
            .build()
    }
}
```

Déclarer dans AndroidManifest.xml :
```xml
<application android:name=".di.App" ...>
```

### Injection dans le ViewModel {#viewmodel-injection}

```kotlin
@Module
abstract class ViewModelModule {
    @Binds
    @IntoMap
    @ViewModelKey(AccountViewModel::class)
    abstract fun bindAccountViewModel(
        viewModel: AccountViewModel
    ): ViewModel
}

// In Fragment
@Inject lateinit var viewModelFactory: ViewModelProvider.Factory

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    (requireActivity().application as App).appComponent.inject(this)
    viewModel = ViewModelProviders.of(this, viewModelFactory)
        .get(AccountViewModel::class.java)
}
```

### Injection dans un Fragment {#injection-in-fragment}

```kotlin
class CurrenciesListFragment : Fragment() {
    @Inject lateinit var apiService: CoinGeckoApi

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        (requireActivity().application as App).appComponent.inject(this)
    }
}
```

## Pièges courants {#gotchas}

- `DaggerAppComponent` est généré à la compilation : compilez le projet après avoir défini le Component
- Chaque Fragment ou Activity qui utilise `@Inject` doit avoir une méthode `inject()` correspondante dans le Component
- La portée `@Singleton` est liée à la durée de vie du Component : elle n'est pas réellement globale si le Component est recréé
- Le qualifier `@Named` est une chaîne de caractères : une faute de frappe provoque des échecs d'injection à l'exécution
- Les messages d'erreur de Dagger 2 peuvent être obscurs : vérifiez que toutes les dépendances ont un fournisseur
- Alternative moderne : Hilt (construit sur Dagger) simplifie la configuration avec `@HiltAndroidApp` et `@AndroidEntryPoint`

## Voir aussi {#see-also}

- [[android-mvvm-architecture]] - ViewModels consommant les dépendances injectées
- [[android-retrofit-networking]] - fourniture de Retrofit via les modules Dagger
- [[android-room-database]] - fourniture de la base Room via Dagger
- [[kotlin-android-fundamentals]] - companion object, lateinit
