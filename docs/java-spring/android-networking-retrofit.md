---
title: Android Networking - Retrofit, OkHttp, REST APIs
category: concepts
tags: [java-spring, android, retrofit, okhttp, rest, networking, gson, api]
---

# Android Networking - Retrofit, OkHttp, REST APIs

HTTP networking on Android using Retrofit (type-safe HTTP client), OkHttp, Gson serialization, coroutine integration, error handling patterns, pagination, and image loading.

## Key Facts

- Android forbids network on main thread - `NetworkOnMainThreadException`
- Retrofit builds on OkHttp, handles serialization/deserialization automatically
- `Call.enqueue()` runs on background thread; `suspend` functions with coroutines are the modern approach
- `@SerializedName` maps JSON field names to Kotlin/Java property names
- `INTERNET` permission required in AndroidManifest
- Glide/Coil for efficient image loading with caching and transformations

## Patterns

### Retrofit API Interface
```kotlin
interface ApiService {
    @GET("users") suspend fun getUsers(): Response<List<User>>
    @GET("users/{id}") suspend fun getUserById(@Path("id") id: Int): Response<User>
    @GET("users") suspend fun searchUsers(@Query("name") name: String): Response<List<User>>
    @POST("users") suspend fun createUser(@Body user: User): Response<User>
    @PUT("users/{id}") suspend fun updateUser(@Path("id") id: Int, @Body user: User): Response<User>
    @DELETE("users/{id}") suspend fun deleteUser(@Path("id") id: Int): Response<Void>
}
```

### Retrofit Client Singleton
```kotlin
object RetrofitClient {
    private val client = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    val api: ApiService = Retrofit.Builder()
        .baseUrl("https://api.example.com/")
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(ApiService::class.java)
}
```

### Data Models with Gson
```kotlin
data class User(
    @SerializedName("id") val id: Int,
    @SerializedName("user_name") val name: String,
    @SerializedName("email") val email: String
)
```

### Safe API Call Wrapper
```kotlin
sealed class NetworkResult<T> {
    data class Success<T>(val data: T) : NetworkResult<T>()
    data class Error<T>(val message: String, val code: Int? = null) : NetworkResult<T>()
    class Loading<T> : NetworkResult<T>()
}

suspend fun <T> safeApiCall(call: suspend () -> Response<T>): NetworkResult<T> = try {
    val response = call()
    if (response.isSuccessful) NetworkResult.Success(response.body()!!)
    else NetworkResult.Error("Error: ${response.message()}", response.code())
} catch (e: IOException) {
    NetworkResult.Error("Network error: check connection")
} catch (e: Exception) {
    NetworkResult.Error("Unexpected: ${e.message}")
}
```

### Pagination
```kotlin
private var currentPage = 1
private var isLastPage = false

fun loadNextPage() {
    if (isLastPage || _loading.value == true) return
    viewModelScope.launch {
        _loading.value = true
        val response = api.getCharacters(page = currentPage, limit = 20)
        if (response.isSuccessful) {
            val items = response.body() ?: emptyList()
            if (items.isEmpty()) isLastPage = true
            else { currentPage++; _data.value = _data.value.orEmpty() + items }
        }
        _loading.value = false
    }
}
```

### Image Loading (Glide)
```java
Glide.with(context)
    .load("https://example.com/image.jpg")
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error)
    .circleCrop()
    .into(imageView);
```

### Repository with Cache Fallback
```kotlin
class Repository(private val api: ApiService, private val dao: UserDao) {
    suspend fun getUsers(): Result<List<User>> = try {
        val response = api.getUsers()
        if (response.isSuccessful) {
            val data = response.body() ?: emptyList()
            dao.insertAll(data)  // cache locally
            Result.success(data)
        } else {
            Result.success(dao.getAllUsers())  // fallback
        }
    } catch (e: IOException) {
        val cached = dao.getAllUsers()
        if (cached.isNotEmpty()) Result.success(cached)
        else Result.failure(e)
    }
}
```

## Gotchas

- `response.body()` can be null even on success - always handle null
- `response.isSuccessful` only checks 2xx codes - 4xx/5xx are not exceptions, check `response.code()`
- Logging interceptor `Level.BODY` logs entire response body - disable in production builds
- `@Body` sends object as JSON; `@Field` (with `@FormUrlEncoded`) sends form data
- Missing `INTERNET` permission causes `SecurityException`, not `NetworkOnMainThreadException`

## See Also

- [[android-architecture-mvvm]] - ViewModel consuming API data
- [[android-data-storage]] - Room for local caching
- [[kotlin-coroutines]] - Async networking with coroutines
