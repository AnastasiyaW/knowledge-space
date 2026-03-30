---
title: Android Networking (Retrofit, Firebase)
category: concepts
tags: [android, retrofit, firebase, rest-api, gson, networking, authentication]
---
# Android Networking (Retrofit, Firebase)

## Key Facts

- **Retrofit** is the standard HTTP client for Android REST API communication - type-safe, coroutine-compatible
- Retrofit uses interface annotations (`@GET`, `@POST`, `@PUT`, `@DELETE`) to define API endpoints
- **Gson** or **Moshi** converts JSON responses to Kotlin/Java data classes automatically
- `@SerializedName("json_key")` maps JSON keys to differently-named class properties
- **Firebase** provides authentication (email, Google Sign-In), Realtime Database, Cloud Firestore, Cloud Messaging
- Firebase Authentication handles sign-up, sign-in, password reset, and social login (Google, Facebook)
- OkHttp interceptors add headers (auth tokens), logging, and retry logic to all requests
- Network calls must run off the main thread - use `suspend` functions with coroutines
- See [[android-architecture]] for how networking fits in the repository layer
- See [[kotlin-fundamentals]] for coroutines that power async network calls

## Patterns

### Retrofit setup

```kotlin
// API interface
interface HarryPotterApi {
    @GET("characters")
    suspend fun getCharacters(): List<CharacterDto>

    @GET("characters/{id}")
    suspend fun getCharacter(@Path("id") id: String): CharacterDto

    @POST("orders")
    suspend fun createOrder(@Body order: OrderRequest): OrderResponse

    @GET("search")
    suspend fun search(
        @Query("name") name: String,
        @Query("house") house: String? = null
    ): List<CharacterDto>

    @PUT("characters/{id}")
    suspend fun updateCharacter(
        @Path("id") id: String,
        @Header("Authorization") token: String,
        @Body update: CharacterUpdate
    ): CharacterDto
}
```

### DTO with Gson annotations

```kotlin
data class CharacterDto(
    val id: String,

    @SerializedName("name")
    val characterName: String,

    @SerializedName("hogwartsHouse")
    val house: String,

    @SerializedName("image")
    val imageUrl: String?,

    val actor: String?,
    val alive: Boolean
)
```

### Retrofit instance creation

```kotlin
object RetrofitClient {
    private const val BASE_URL = "https://hp-api.herokuapp.com/api/"

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .addInterceptor { chain ->
            val request = chain.request().newBuilder()
                .addHeader("Accept", "application/json")
                .build()
            chain.proceed(request)
        }
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    val api: HarryPotterApi = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(HarryPotterApi::class.java)
}
```

### Repository with error handling

```kotlin
class CharacterRepository(private val api: HarryPotterApi) {

    suspend fun getCharacters(): Result<List<Character>> {
        return try {
            val dtos = api.getCharacters()
            val characters = dtos.map { it.toDomain() }
            Result.success(characters)
        } catch (e: HttpException) {
            Result.failure(Exception("Server error: ${e.code()}"))
        } catch (e: IOException) {
            Result.failure(Exception("Network error - check connection"))
        }
    }
}

// Mapper extension function
fun CharacterDto.toDomain() = Character(
    id = id,
    name = characterName,
    house = house,
    imageUrl = imageUrl
)
```

### Firebase Authentication setup

```kotlin
// Sign up with email/password
class AuthRepository(private val auth: FirebaseAuth) {

    suspend fun signUp(email: String, password: String): Result<FirebaseUser> {
        return try {
            val result = auth.createUserWithEmailAndPassword(email, password).await()
            Result.success(result.user!!)
        } catch (e: FirebaseAuthException) {
            Result.failure(e)
        }
    }

    suspend fun signIn(email: String, password: String): Result<FirebaseUser> {
        return try {
            val result = auth.signInWithEmailAndPassword(email, password).await()
            Result.success(result.user!!)
        } catch (e: FirebaseAuthException) {
            Result.failure(e)
        }
    }

    fun signOut() = auth.signOut()

    fun currentUser(): FirebaseUser? = auth.currentUser
}
```

### Google Sign-In with Firebase

```kotlin
class GoogleSignInHelper(private val activity: Activity) {

    private val googleSignInClient: GoogleSignInClient

    init {
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(activity.getString(R.string.default_web_client_id))
            .requestEmail()
            .build()
        googleSignInClient = GoogleSignIn.getClient(activity, gso)
    }

    fun getSignInIntent(): Intent = googleSignInClient.signInIntent

    suspend fun firebaseAuthWithGoogle(idToken: String): FirebaseUser? {
        val credential = GoogleAuthProvider.getCredential(idToken, null)
        val result = FirebaseAuth.getInstance()
            .signInWithCredential(credential)
            .await()
        return result.user
    }
}
```

### Firebase Realtime Database

```kotlin
class ForumRepository {
    private val db = FirebaseDatabase.getInstance()
    private val messagesRef = db.getReference("messages")

    fun sendMessage(message: ForumMessage) {
        val key = messagesRef.push().key ?: return
        messagesRef.child(key).setValue(message)
    }

    fun observeMessages(callback: (List<ForumMessage>) -> Unit) {
        messagesRef.addValueEventListener(object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                val messages = snapshot.children.mapNotNull {
                    it.getValue(ForumMessage::class.java)
                }
                callback(messages)
            }
            override fun onCancelled(error: DatabaseError) {
                Log.e("Forum", "Error: ${error.message}")
            }
        })
    }
}
```

## Gotchas

- **Symptom**: `NetworkOnMainThreadException` -> **Cause**: Retrofit call without `suspend` or running on main thread -> **Fix**: Use `suspend` functions with coroutines, or `enqueue()` for callback-based approach
- **Symptom**: `@SerializedName` not working -> **Cause**: ProGuard/R8 obfuscates field names in release builds -> **Fix**: Add `-keep class com.example.dto.** { *; }` to proguard-rules.pro, or use `@SerializedName` on ALL fields
- **Symptom**: Firebase Google Sign-In fails with error 10 -> **Cause**: SHA-1 fingerprint not registered in Firebase Console -> **Fix**: Add debug AND release SHA-1 fingerprints in Firebase project settings
- **Symptom**: API returns data but app shows empty list -> **Cause**: JSON key names don't match class property names -> **Fix**: Check JSON structure carefully, use `@SerializedName` for mismatched names
- **Symptom**: Firebase `await()` doesn't compile -> **Cause**: Missing `kotlinx-coroutines-play-services` dependency -> **Fix**: Add `implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")`

## See Also

- [[android-architecture]] - Repository pattern for network layer
- [[android-room-database]] - Cache network data locally
- [[kotlin-fundamentals]] - Coroutines for async networking
- Android Docs: [Retrofit](https://square.github.io/retrofit/)
- Firebase Docs: [Authentication](https://firebase.google.com/docs/auth)
- Firebase Docs: [Realtime Database](https://firebase.google.com/docs/database)
