---
title: Android Retrofit Networking
category: concepts
tags: [ios-mobile, android, retrofit, gson, rest-api, networking, okhttp]
---

# Android Retrofit Networking

Retrofit is the standard HTTP client for Android, converting REST API definitions into Kotlin interfaces. Combined with Gson for JSON parsing and OkHttp for transport, it provides type-safe API access with minimal boilerplate.

## Key Facts

- Retrofit converts annotated Kotlin interfaces into HTTP client implementations
- `@GET`, `@POST`, `@PUT`, `@DELETE` define HTTP methods on interface functions
- `@Path("id")` substitutes into URL path segments (`{id}`)
- `@Query("name")` appends URL query parameters
- `GsonConverterFactory` handles JSON serialization/deserialization
- `OkHttpClient` with logging interceptor enables network debugging
- Returns can be `Observable<T>` (RxJava), `Call<T>`, or `suspend` functions (coroutines)

## Patterns

### Data Models

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

### API Interface

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

### Retrofit Annotations Reference

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@GET("path")` | GET request | `@GET("coins/markets")` |
| `@POST("path")` | POST request | `@POST("users")` |
| `@PUT("path")` | PUT request | `@PUT("users/{id}")` |
| `@DELETE("path")` | DELETE request | `@DELETE("users/{id}")` |
| `@Path("name")` | URL path parameter | `{id}` in URL |
| `@Query("name")` | Query parameter | `?key=value` |
| `@QueryMap` | Multiple query params | `Map<String, String>` |
| `@Body` | Request body | For POST/PUT |

### Retrofit Builder

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

### With Dagger 2 Module

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

### Retrofit vs URLSession (iOS) Comparison

| Feature | Retrofit (Android) | URLSession (iOS) |
|---------|-------------------|------------------|
| Definition | Annotated interface | Inline URL construction |
| JSON parsing | Gson converter | JSONDecoder (Codable) |
| Type safety | Compile-time from annotations | Runtime from Decodable |
| HTTP client | OkHttp | Built-in URLSession |
| Async | RxJava / Coroutines | async/await |

### build.gradle Dependencies

```groovy
implementation "com.squareup.retrofit2:retrofit:2.9.0"
implementation "com.squareup.retrofit2:converter-gson:2.9.0"
implementation "com.google.code.gson:gson:2.10.0"
implementation "com.squareup.okhttp3:okhttp:4.11.0"
implementation "com.squareup.okhttp3:logging-interceptor:4.11.0"
```

## Gotchas

- Base URL must end with `/` or Retrofit throws an exception
- `@Path` parameters are URL-encoded by default; use `@Path(encoded = true)` for pre-encoded values
- Logging interceptor at `Level.BODY` logs full request/response bodies - disable in production for security
- Gson uses field names by default for JSON keys; use `@SerializedName("json_key")` for custom mapping
- Network calls on the main thread cause `NetworkOnMainThreadException` - always use background dispatchers
- `Observable<T>` requires RxJava2CallAdapterFactory; for coroutines, use `suspend fun` return types instead

## See Also

- [[android-mvvm-architecture]] - ViewModel consuming Retrofit data
- [[android-room-database]] - storing fetched data locally
- [[android-dagger-dependency-injection]] - injecting Retrofit as singleton
- [[kotlin-android-fundamentals]] - Kotlin basics, data class
