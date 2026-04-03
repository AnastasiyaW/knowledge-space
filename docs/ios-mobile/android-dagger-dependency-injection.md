---
title: Android Dagger 2 Dependency Injection
category: concepts
tags: [ios-mobile, android, dagger, dependency-injection, di, module, component, singleton]
---

# Android Dagger 2 Dependency Injection

Dagger 2 generates dependency injection code at compile time with zero reflection and zero runtime overhead. It connects providers (Modules) to consumers (@Inject) through a Component interface.

## Key Facts

- Dagger 2 generates DI code at compile time - no reflection, no runtime overhead
- `@Module` classes contain `@Provides` methods that create dependency instances
- `@Component` interface connects `@Inject` requests to `@Module` providers
- `@Singleton` scope creates one instance and reuses it everywhere
- `@Inject` requests injection of a dependency (constructor or field)
- `@Named("qualifier")` disambiguates when multiple same-type dependencies exist
- Build the project to generate `DaggerAppComponent` class

## Patterns

### Core Annotations

| Annotation | Purpose |
|------------|---------|
| `@Module` | Class that provides dependencies |
| `@Provides` | Method inside Module that creates an instance |
| `@Singleton` | Create once, reuse everywhere |
| `@Component` | Interface connecting inject requests to providers |
| `@Inject` | Request injection of a dependency |
| `@Named("x")` | Qualifier when multiple same-type deps exist |
| `@Binds` | Abstract method to bind implementation to interface |
| `@IntoMap` | Contribute to a Map of dependencies |

### Module Examples

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

### Component Interface

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

### Application Class Setup

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

Register in AndroidManifest.xml:
```xml
<application android:name=".di.App" ...>
```

### ViewModel Injection

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

### Injection in Fragment

```kotlin
class CurrenciesListFragment : Fragment() {
    @Inject lateinit var apiService: CoinGeckoApi

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        (requireActivity().application as App).appComponent.inject(this)
    }
}
```

## Gotchas

- `DaggerAppComponent` is generated at compile time - build the project after defining the Component
- Every Fragment/Activity that uses `@Inject` must have a corresponding `inject()` method in the Component
- `@Singleton` scope is tied to the Component's lifetime - not truly global if Component is recreated
- `@Named` qualifier is a string - typos cause runtime injection failures
- Dagger 2 error messages can be cryptic - check that all dependencies have providers
- Modern alternative: Hilt (built on Dagger) simplifies setup with `@HiltAndroidApp`, `@AndroidEntryPoint`

## See Also

- [[android-mvvm-architecture]] - ViewModels consuming injected dependencies
- [[android-retrofit-networking]] - providing Retrofit via Dagger modules
- [[android-room-database]] - providing Room database via Dagger
- [[kotlin-android-fundamentals]] - companion object, lateinit
