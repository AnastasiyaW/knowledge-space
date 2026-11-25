---
title: "Réseau Android avec Retrofit"
category: concepts
tags: [ios-mobile, android, retrofit, gson, rest-api, networking, okhttp]
level: 3
source_sha256: ba94622f1e563c0f81332a9e2314734ac72207c9add8e004a6c7f8d2fa0aab15
translation: machine
translated_at: '2026-10-24'
---
# Réseau Android avec Retrofit {#android-retrofit-networking}

Retrofit est le client HTTP de référence pour Android. Il convertit les définitions d'API REST en interfaces Kotlin. Associé à Gson pour l'analyse JSON et à OkHttp pour le transport, il offre un accès typé aux API avec un minimum de code répétitif.

## Faits clés {#key-facts}

- Retrofit convertit des interfaces Kotlin annotées en implémentations de client HTTP
- `@GET`, `@POST`, `@PUT`, `@DELETE` définissent les méthodes HTTP sur les fonctions de l'interface
- `@Path("id")` substitue la valeur dans les segments de chemin de l'URL (`{id}`)
- `@Query("name")` ajoute des paramètres de requête à l'URL
- `GsonConverterFactory` gère la sérialisation et la désérialisation JSON
- `OkHttpClient` avec un intercepteur de journalisation permet le débogage réseau
- Les retours peuvent être `Observable<T>` (RxJava), `Call<T>` ou des fonctions `suspend` (coroutines)

## Patrons {#patterns}

### Modèles de données {#data-models}

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

### Interface API {#api-interface}

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

### Référence des annotations Retrofit {#retrofit-annotations-reference}

| Annotation | Rôle | Exemple |
|------------|------|---------|
| `@GET("path")` | Requête GET | `@GET("coins/markets")` |
| `@POST("path")` | Requête POST | `@POST("users")` |
| `@PUT("path")` | Requête PUT | `@PUT("users/{id}")` |
| `@DELETE("path")` | Requête DELETE | `@DELETE("users/{id}")` |
| `@Path("name")` | Paramètre de chemin d'URL | `{id}` dans l'URL |
| `@Query("name")` | Paramètre de requête | `?key=value` |
| `@QueryMap` | Plusieurs paramètres de requête | `Map<String, String>` |
| `@Body` | Corps de la requête | Pour POST/PUT |

### Builder Retrofit {#retrofit-builder}

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

### Avec un module Dagger 2 {#with-dagger-2-module}

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

### Comparaison Retrofit vs URLSession (iOS) {#retrofit-vs-urlsession-ios-comparison}

| Caractéristique | Retrofit (Android) | URLSession (iOS) |
|-----------------|--------------------|------------------|
| Définition | Interface annotée | Construction d'URL inline |
| Analyse JSON | Convertisseur Gson | JSONDecoder (Codable) |
| Sûreté des types | À la compilation, à partir des annotations | À l'exécution, à partir de Decodable |
| Client HTTP | OkHttp | URLSession intégré |
| Asynchrone | RxJava / Coroutines | async/await |

### Dépendances build.gradle {#buildgradle-dependencies}

```groovy
implementation "com.squareup.retrofit2:retrofit:2.9.0"
implementation "com.squareup.retrofit2:converter-gson:2.9.0"
implementation "com.google.code.gson:gson:2.10.0"
implementation "com.squareup.okhttp3:okhttp:4.11.0"
implementation "com.squareup.okhttp3:logging-interceptor:4.11.0"
```

## Pièges {#gotchas}

- L'URL de base doit se terminer par `/`, sinon Retrofit lève une exception
- Les paramètres `@Path` sont encodés en URL par défaut ; utilisez `@Path(encoded = true)` pour les valeurs déjà encodées
- L'intercepteur de journalisation au niveau `Level.BODY` enregistre le corps complet des requêtes et des réponses ; désactivez-le en production pour des raisons de sécurité
- Gson utilise par défaut les noms de champs comme clés JSON ; utilisez `@SerializedName("json_key")` pour un mappage personnalisé
- Les appels réseau sur le thread principal provoquent une `NetworkOnMainThreadException` ; utilisez systématiquement des dispatchers d'arrière-plan
- `Observable<T>` nécessite `RxJava2CallAdapterFactory` ; pour les coroutines, utilisez plutôt des types de retour `suspend fun`

## Voir aussi {#see-also}

- [[android-mvvm-architecture]] - ViewModel consommant les données Retrofit
- [[android-room-database]] - stockage local des données récupérées
- [[android-dagger-dependency-injection]] - injection de Retrofit en singleton
- [[kotlin-android-fundamentals]] - bases de Kotlin, data class
