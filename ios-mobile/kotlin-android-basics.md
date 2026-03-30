---
title: Kotlin and Android Development Basics
category: ios-mobile/android
tags: [kotlin, android, android-studio, retrofit, mvp, rxkotlin, google-play]
---

# Kotlin and Android Development Basics

## Key Facts

- Kotlin is the primary language for Android development (replaced Java as Google's recommended language)
- Android Studio is the IDE for Android development (equivalent of Xcode for iOS)
- Android Virtual Device (AVD) emulator is used for testing, similar to iOS Simulator
- MVP (Model-View-Presenter) is a common Android architecture pattern
- Retrofit is a type-safe HTTP client from Square for network requests (GET, POST, PUT, DELETE)
- Gson library converts JSON responses to Kotlin/Java objects (similar to Swift's Codable/JSONDecoder)
- RxKotlin provides reactive/asynchronous programming (similar to Swift's Combine or async/await)
- Gradle (`build.gradle`) is the build system - dependencies are declared in the app-level build file
- Apps are published to Google Play Store (vs Apple's App Store for iOS)
- RecyclerView is Android's equivalent of SwiftUI's [[lists-and-navigation]] List view

## Patterns

```kotlin
// build.gradle (app) - adding dependencies
dependencies {
    // Gson for JSON parsing
    implementation 'com.google.code.gson:gson:2.8.2'
    // Retrofit for networking
    implementation 'com.squareup.retrofit2:retrofit:2.3.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.3.0'
    // RxKotlin for async
    implementation 'io.reactivex.rxjava2:rxkotlin:2.2.0'
    implementation 'io.reactivex.rxjava2:rxandroid:2.0.1'
}
```

```kotlin
// Retrofit API interface
interface CryptoApi {
    @GET("v1/cryptocurrency/listings/latest")
    fun getLatest(
        @Query("limit") limit: Int
    ): Call<CryptoResponse>
}

// Data class (Kotlin equivalent of Swift struct)
data class Cryptocurrency(
    val id: Int,
    val name: String,
    val symbol: String,
    val price: Double
)

// MVP - Presenter
class MainPresenter(private val view: MainView) {
    fun loadData() {
        // Fetch from API, update view
        view.showCurrencies(currencies)
    }
}
```

## Gotchas

- Android uses `data class` (like Swift's `struct`) and regular `class` - no value type vs reference type distinction like Swift
- Gradle sync is required after adding dependencies - can be slow and sometimes fails
- Android permissions model differs from iOS - must declare in AndroidManifest.xml AND request at runtime
- RecyclerView requires an Adapter pattern (more boilerplate than SwiftUI's List/ForEach)
- Kotlin null safety uses `?` for nullable types, `!!` for force unwrap - similar concept to Swift optionals
- Android fragmentation: many OS versions and screen sizes to support vs iOS's more controlled ecosystem
- Retrofit handles background threading automatically in async mode; without it, network calls on main thread crash the app

## See Also

- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)
- [Android Developer Guide](https://developer.android.com/guide)
- [[swift-fundamentals]] (iOS equivalent)
- [[app-architecture-patterns]]
