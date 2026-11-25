---
title: "Android-Netzwerk – Retrofit, OkHttp, REST-APIs"
category: concepts
tags: [java-spring, android, retrofit, okhttp, rest, networking, gson, api]
level: 3
source_sha256: 3dccc6cf937849080be33b8801ab92996cc209f3ab2eb12799c51bba76bacb90
translation: machine
translated_at: '2026-10-24'
---
# Android-Netzwerk – Retrofit, OkHttp, REST-APIs {#android-networking-retrofit-okhttp-rest-apis}

HTTP-Netzwerkkommunikation unter Android mit Retrofit (typsicherer HTTP-Client), OkHttp, Gson-Serialisierung, Coroutine-Integration, Fehlerbehandlungsmustern, Paginierung und Bildladen.

## Key Facts {#key-facts}

- Android verbietet Netzwerkzugriffe auf dem Main-Thread – `NetworkOnMainThreadException`
- Retrofit baut auf OkHttp auf und übernimmt Serialisierung/Deserialisierung automatisch
- `Call.enqueue()` läuft auf einem Hintergrund-Thread; `suspend`-Funktionen mit Coroutines sind der moderne Ansatz
- `@SerializedName` ordnet JSON-Feldnamen Kotlin-/Java-Eigenschaftsnamen zu
- Die `INTERNET`-Berechtigung muss im AndroidManifest deklariert sein
- Glide/Coil für effizientes Laden von Bildern mit Caching und Transformationen

## Patterns {#patterns}

### Retrofit API Interface {#retrofit-api-interface}
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

### Retrofit Client Singleton {#retrofit-client-singleton}
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

### Data Models with Gson {#data-models-with-gson}
```kotlin
data class User(
    @SerializedName("id") val id: Int,
    @SerializedName("user_name") val name: String,
    @SerializedName("email") val email: String
)
```

### Safe API Call Wrapper {#safe-api-call-wrapper}
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

### Pagination {#pagination}
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

### Image Loading (Glide) {#image-loading-glide}
```java
Glide.with(context)
    .load("https://example.com/image.jpg")
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error)
    .circleCrop()
    .into(imageView);
```

### Repository with Cache Fallback {#repository-with-cache-fallback}
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

## Gotchas {#gotchas}

- `response.body()` kann auch bei Erfolg null sein – immer auf null prüfen
- `response.isSuccessful` prüft nur 2xx-Codes – 4xx/5xx werden nicht als Exceptions ausgelöst, `response.code()` prüfen
- Der Logging-Interceptor mit `Level.BODY` protokolliert den gesamten Response-Body – in Production-Builds deaktivieren
- `@Body` sendet das Objekt als JSON; `@Field` (mit `@FormUrlEncoded`) sendet Formulardaten
- Eine fehlende `INTERNET`-Berechtigung verursacht eine `SecurityException`, nicht eine `NetworkOnMainThreadException`

## See Also {#see-also}

- [[android-architecture-mvvm]] – ViewModel, das API-Daten konsumiert
- [[android-data-storage]] – Room für lokales Caching
- [[kotlin-coroutines]] – Asynchrone Netzwerkkommunikation mit Coroutines
