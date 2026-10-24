---
title: "Android-Retrofit-Netzwerkzugriff"
category: concepts
tags: [ios-mobile, android, retrofit, gson, rest-api, networking, okhttp]
level: 3
source_sha256: ba94622f1e563c0f81332a9e2314734ac72207c9add8e004a6c7f8d2fa0aab15
translation: machine
translated_at: '2026-10-24'
---
# Android-Retrofit-Netzwerkzugriff {#android-retrofit-networking}

Retrofit ist der Standard-HTTP-Client für Android. Er wandelt REST-API-Definitionen in Kotlin-Interfaces um. Zusammen mit Gson für das JSON-Parsing und OkHttp als Transportschicht bietet er typsicheren API-Zugriff mit minimalem Boilerplate-Code.

## Wichtige Fakten {#key-facts}

- Retrofit wandelt annotierte Kotlin-Interfaces in HTTP-Client-Implementierungen um
- `@GET`, `@POST`, `@PUT`, `@DELETE` definieren die HTTP-Methoden für Interface-Funktionen
- `@Path("id")` setzt Werte in URL-Pfadsegmente ein (`{id}`)
- `@Query("name")` hängt URL-Query-Parameter an
- `GsonConverterFactory` übernimmt die JSON-Serialisierung und -Deserialisierung
- `OkHttpClient` mit einem Logging-Interceptor ermöglicht das Debugging von Netzwerkaufrufen
- Rückgabetypen können `Observable<T>` (RxJava), `Call<T>` oder `suspend`-Funktionen (Coroutines) sein

## Muster {#patterns}

### Datenmodelle {#data-models}

```kotlin
data class GeckoCoin(
    val id: String,
    val symbol: String,
    val name: String,
    val image: String,
    val current_price: Float,
    val market_cap: Float,
    val market_cap_rank: Int,
    val total_volume: Float,
    val price_change_percentage_24h: Float
)

data class GeckoCoinChart(
    var prices: List<List<Float>>
)
```

### API-Schnittstelle {#api-interface}

```kotlin
import retrofit2.http.*

interface CoinGeckoApi {
    @GET("coins/markets")
    fun getCoinMarket(
        @Query("vs_currency") vs: String = "usd",
        @Query("per_page") perPage: Int = 100,
        @Query("sparkline") sparkline: Boolean = false,
        @Query("order") order: String = "market_cap_desc"
    ): Observable<List<GeckoCoin>>

    @GET("coins/{id}/market_chart")
    fun getCoinMarketChart(
        @Path("id") id: String,
        @Query("vs_currency") vsCurrency: String = "usd",
        @Query("days") days: String = "max"
    ): Observable<GeckoCoinChart>
}
```

### Referenz der Retrofit-Annotationen {#retrofit-annotations-reference}

| Annotation | Zweck | Beispiel |
|------------|-------|----------|
| `@GET("path")` | GET-Anfrage | `@GET("coins/markets")` |
| `@POST("path")` | POST-Anfrage | `@POST("users")` |
| `@PUT("path")` | PUT-Anfrage | `@PUT("users/{id}")` |
| `@DELETE("path")` | DELETE-Anfrage | `@DELETE("users/{id}")` |
| `@Path("name")` | URL-Pfadparameter | `{id}` in der URL |
| `@Query("name")` | Query-Parameter | `?key=value` |
| `@QueryMap` | Mehrere Query-Parameter | `Map<String, String>` |
| `@Body` | Request-Body | Für POST/PUT |

### Retrofit-Builder {#retrofit-builder}

```kotlin
val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(
        HttpLoggingInterceptor()
            .setLevel(HttpLoggingInterceptor.Level.BODY)
    )
    .connectTimeout(60, TimeUnit.SECONDS)
    .build()

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.coingecko.com/api/v3/")
    .addConverterFactory(GsonConverterFactory.create(gson))
    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
    .client(okHttpClient)
    .build()

val apiService = retrofit.create(CoinGeckoApi::class.java)
```

### Mit Dagger-2-Modul {#with-dagger-2-module}

```kotlin
@Module
class RestModule {
    @Provides
    @Singleton
    fun provideGson(): Gson = GsonBuilder().setLenient().create()

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient =
        OkHttpClient.Builder()
            .addInterceptor(
                HttpLoggingInterceptor()
                    .setLevel(HttpLoggingInterceptor.Level.BODY)
            )
            .connectTimeout(60, TimeUnit.SECONDS)
            .build()

    @Provides
    @Singleton
    fun provideRetrofit(gson: Gson, okHttpClient: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl("https://api.coingecko.com/api/v3/")
            .addConverterFactory(GsonConverterFactory.create(gson))
            .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
            .client(okHttpClient)
            .build()

    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): CoinGeckoApi =
        retrofit.create(CoinGeckoApi::class.java)
}
```

### Vergleich Retrofit vs. URLSession (iOS) {#retrofit-vs-urlsession-ios-comparison}

| Merkmal | Retrofit (Android) | URLSession (iOS) |
|---------|-------------------|------------------|
| Definition | Annotiertes Interface | Inline-URL-Konstruktion |
| JSON-Parsing | Gson-Converter | JSONDecoder (Codable) |
| Typsicherheit | Zur Compilezeit aus Annotationen | Zur Laufzeit aus Decodable |
| HTTP-Client | OkHttp | Eingebautes URLSession |
| Asynchrone Verarbeitung | RxJava / Coroutines | async/await |

### build.gradle-Abhängigkeiten {#buildgradle-dependencies}

```groovy
implementation "com.squareup.retrofit2:retrofit:2.9.0"
implementation "com.squareup.retrofit2:converter-gson:2.9.0"
implementation "com.google.code.gson:gson:2.10.0"
implementation "com.squareup.okhttp3:okhttp:4.11.0"
implementation "com.squareup.okhttp3:logging-interceptor:4.11.0"
```

## Stolperfallen {#gotchas}

- Die Base-URL muss mit `/` enden, sonst wirft Retrofit eine Exception
- `@Path`-Parameter werden standardmäßig URL-kodiert; verwende `@Path(encoded = true)` für bereits kodierte Werte
- Der Logging-Interceptor mit `Level.BODY` protokolliert vollständige Request- und Response-Bodies – in Produktion aus Sicherheitsgründen deaktivieren
- Gson verwendet standardmäßig die Feldnamen als JSON-Schlüssel; für eine eigene Zuordnung `@SerializedName("json_key")` verwenden
- Netzwerkaufrufe auf dem Main-Thread verursachen eine `NetworkOnMainThreadException` – immer Hintergrund-Dispatcher verwenden
- `Observable<T>` erfordert die `RxJava2CallAdapterFactory`; für Coroutines stattdessen Rückgabetypen mit `suspend fun` verwenden

## Siehe auch {#see-also}

- [[android-mvvm-architecture]] - ViewModel, das Retrofit-Daten konsumiert
- [[android-room-database]] - lokales Speichern der abgerufenen Daten
- [[android-dagger-dependency-injection]] - Retrofit als Singleton injizieren
- [[kotlin-android-fundamentals]] - Kotlin-Grundlagen, Data Class
