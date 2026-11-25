---
title: "Android-Dagger-2-Dependency-Injection"
category: concepts
tags: [ios-mobile, android, dagger, dependency-injection, di, module, component, singleton]
level: 3
source_sha256: 70bf69ea65d4fb663479354f041ae3d2bdac2c351041ec221f367d871b63b6e9
translation: machine
translated_at: '2026-10-24'
---
# Android Dagger 2 Dependency Injection {#android-dagger-2-dependency-injection}

Dagger 2 generiert Dependency-Injection-Code zur Kompilierzeit ohne Reflection und ohne Laufzeitaufwand. Es verbindet Provider (Modules) mit Konsumenten (@Inject) über ein Component-Interface.

## Key Facts {#key-facts}

- Dagger 2 generiert DI-Code zur Kompilierzeit - keine Reflection, kein Laufzeitaufwand
- `@Module`-Klassen enthalten `@Provides`-Methoden, die Instanzen der Abhängigkeiten erzeugen
- Das `@Component`-Interface verbindet `@Inject`-Anfragen mit `@Module`-Providern
- Der `@Singleton`-Scope erzeugt eine Instanz und verwendet sie überall wieder
- `@Inject` fordert die Injection einer Abhängigkeit an (Konstruktor oder Feld)
- `@Named("qualifier")` unterscheidet zwischen mehreren Abhängigkeiten desselben Typs
- Projekt bauen, um die Klasse `DaggerAppComponent` zu generieren

## Patterns {#patterns}

### Core Annotations {#core-annotations}

| Annotation | Zweck |
|------------|---------|
| `@Module` | Klasse, die Abhängigkeiten bereitstellt |
| `@Provides` | Methode innerhalb eines Moduls, die eine Instanz erzeugt |
| `@Singleton` | Einmal erzeugen, überall wiederverwenden |
| `@Component` | Interface, das Inject-Anfragen mit Providern verbindet |
| `@Inject` | Injection einer Abhängigkeit anfordern |
| `@Named("x")` | Qualifier, wenn mehrere Abhängigkeiten desselben Typs existieren |
| `@Binds` | Abstrakte Methode, um eine Implementierung an ein Interface zu binden |
| `@IntoMap` | Beitrag zu einer Map von Abhängigkeiten leisten |

### Module Examples {#module-examples}

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

### Component Interface {#component-interface}

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

### Application Class Setup {#application-class-setup}

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

In AndroidManifest.xml registrieren:
```xml
<application android:name=".di.App" ...>
```

### ViewModel Injection {#viewmodel-injection}

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

### Injection in Fragment {#injection-in-fragment}

```kotlin
class CurrenciesListFragment : Fragment() {
    @Inject lateinit var apiService: CoinGeckoApi

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        (requireActivity().application as App).appComponent.inject(this)
    }
}
```

## Gotchas {#gotchas}

- `DaggerAppComponent` wird zur Kompilierzeit generiert - das Projekt nach der Definition der Component bauen
- Jedes Fragment/jede Activity, das/die `@Inject` verwendet, benötigt eine entsprechende `inject()`-Methode in der Component
- Der `@Singleton`-Scope ist an die Lebensdauer der Component gebunden - nicht wirklich global, wenn die Component neu erzeugt wird
- Der `@Named`-Qualifier ist ein String - Tippfehler führen zur Laufzeit zu Injection-Fehlern
- Fehlermeldungen von Dagger 2 können kryptisch sein - prüfen, ob alle Abhängigkeiten einen Provider haben
- Moderne Alternative: Hilt (auf Dagger aufgebaut) vereinfacht die Einrichtung mit `@HiltAndroidApp`, `@AndroidEntryPoint`

## See Also {#see-also}

- [[android-mvvm-architecture]] - ViewModels, die injizierte Abhängigkeiten verwenden
- [[android-retrofit-networking]] - Bereitstellung von Retrofit über Dagger-Module
- [[android-room-database]] - Bereitstellung der Room-Datenbank über Dagger
- [[kotlin-android-fundamentals]] - companion object, lateinit
