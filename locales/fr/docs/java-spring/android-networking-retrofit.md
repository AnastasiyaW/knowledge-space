---
title: "Réseau sous Android - Retrofit, OkHttp, API REST"
category: concepts
tags: [java-spring, android, retrofit, okhttp, rest, networking, gson, api]
level: 3
source_sha256: 3dccc6cf937849080be33b8801ab92996cc209f3ab2eb12799c51bba76bacb90
translation: machine
translated_at: '2026-10-24'
---
# Réseau sous Android - Retrofit, OkHttp, API REST {#android-networking-retrofit-okhttp-rest-apis}

Communication HTTP sous Android avec Retrofit (client HTTP typé), OkHttp, la sérialisation Gson, l'intégration des coroutines, les schémas de gestion des erreurs, la pagination et le chargement d'images.

## Points clés {#key-facts}

- Android interdit les opérations réseau sur le thread principal - `NetworkOnMainThreadException`
- Retrofit s'appuie sur OkHttp et gère automatiquement la sérialisation et la désérialisation
- `Call.enqueue()` s'exécute sur un thread d'arrière-plan ; les fonctions `suspend` avec les coroutines constituent l'approche moderne
- `@SerializedName` associe les noms de champs JSON aux noms de propriétés Kotlin/Java
- La permission `INTERNET` est requise dans AndroidManifest
- Glide/Coil pour un chargement d'images efficace avec mise en cache et transformations

## Modèles {#patterns}

### Interface API Retrofit {#retrofit-api-interface}
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

### Singleton du client Retrofit {#retrofit-client-singleton}
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

### Modèles de données avec Gson {#data-models-with-gson}
```kotlin
data class User(
    @SerializedName("id") val id: Int,
    @SerializedName("user_name") val name: String,
    @SerializedName("email") val email: String
)
```

### Enveloppe sécurisée pour les appels API {#safe-api-call-wrapper}
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

### Chargement d'images (Glide) {#image-loading-glide}
```java
Glide.with(context)
    .load("https://example.com/image.jpg")
    .placeholder(R.drawable.placeholder)
    .error(R.drawable.error)
    .circleCrop()
    .into(imageView);
```

### Repository avec repli sur le cache {#repository-with-cache-fallback}
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

## Pièges {#gotchas}

- `response.body()` peut être null même en cas de succès - gérez toujours le cas null
- `response.isSuccessful` ne vérifie que les codes 2xx - les 4xx/5xx ne lèvent pas d'exception, vérifiez `response.code()`
- Le `Level.BODY` de l'intercepteur de logs journalise l'intégralité du corps de la réponse - désactivez-le dans les builds de production
- `@Body` envoie l'objet au format JSON ; `@Field` (avec `@FormUrlEncoded`) envoie des données de formulaire
- L'absence de la permission `INTERNET` provoque une `SecurityException`, et non une `NetworkOnMainThreadException`

## Voir aussi {#see-also}

- [[android-architecture-mvvm]] - ViewModel consommant les données de l'API
- [[android-data-storage]] - Room pour la mise en cache locale
- [[kotlin-coroutines]] - Réseau asynchrone avec les coroutines
