---
title: Android Firebase - Auth, Firestore, Storage
category: reference
tags: [java-spring, android, firebase, authentication, firestore, cloud-storage]
---

# Android Firebase - Auth, Firestore, Storage

Firebase integration for Android: Authentication (email/password), Cloud Firestore (NoSQL database), Cloud Storage (file uploads), and real-time listeners.

## Key Facts

- Firebase setup: create project in Console, add Android app, download `google-services.json` to app/
- Firebase BOM (Bill of Materials) manages version compatibility across Firebase libraries
- Firebase Auth supports email/password, Google Sign-In, phone, anonymous
- Firestore is a document-oriented NoSQL database with real-time sync
- `addSnapshotListener` provides real-time updates without polling
- Cloud Storage for file uploads (images, videos) with download URL retrieval

## Patterns

### Authentication
```kotlin
private val auth = Firebase.auth

// Register
auth.createUserWithEmailAndPassword(email, password)
    .addOnCompleteListener { task ->
        if (task.isSuccessful) { val user = auth.currentUser }
        else { /* task.exception?.message */ }
    }

// Login
auth.signInWithEmailAndPassword(email, password)
    .addOnCompleteListener { task ->
        if (task.isSuccessful) { /* navigate to main */ }
    }

// Check state
if (auth.currentUser != null) { /* signed in */ }

// Logout
auth.signOut()
```

### Cloud Firestore CRUD
```kotlin
private val db = Firebase.firestore

// Write
db.collection("users").document(user.id).set(user)
    .addOnSuccessListener { /* saved */ }
    .addOnFailureListener { e -> /* error */ }

// Read single
db.collection("users").document(userId).get()
    .addOnSuccessListener { doc -> val user = doc.toObject(User::class.java) }

// Query
db.collection("users")
    .whereEqualTo("house", "Gryffindor")
    .orderBy("name")
    .get()
    .addOnSuccessListener { snapshot ->
        val users = snapshot.toObjects(User::class.java)
    }

// Real-time listener
db.collection("orders").whereEqualTo("status", "NEW")
    .addSnapshotListener { snapshot, error ->
        if (error != null) return@addSnapshotListener
        val orders = snapshot?.toObjects(Order::class.java) ?: emptyList()
        updateUI(orders)
    }
```

### Cloud Storage
```kotlin
val storage = Firebase.storage

fun uploadImage(uri: Uri) {
    val ref = storage.reference.child("images/${UUID.randomUUID()}.jpg")
    ref.putFile(uri).addOnSuccessListener {
        ref.downloadUrl.addOnSuccessListener { url ->
            // Save url to Firestore
        }
    }
}
```

### Setup Dependencies
```gradle
// Project-level
classpath 'com.google.gms:google-services:4.4.0'

// App-level
apply plugin: 'com.google.gms.google-services'
implementation platform('com.google.firebase:firebase-bom:32.7.0')
implementation 'com.google.firebase:firebase-auth-ktx'
implementation 'com.google.firebase:firebase-firestore-ktx'
implementation 'com.google.firebase:firebase-storage-ktx'
```

## Gotchas

- `google-services.json` must be in the `app/` directory, not project root
- Firestore queries with `whereEqualTo` + `orderBy` on different fields require a composite index (Firestore logs the URL to create it)
- `addSnapshotListener` keeps connection open - remove listener in `onStop()` to save bandwidth
- Firebase operations are async - don't assume data is available synchronously after a call
- Firestore document size limit is 1MB; collection depth is unlimited but keep shallow for performance

## See Also

- [[android-architecture-mvvm]] - Repository pattern with Firebase as data source
- [[android-networking-retrofit]] - REST API alternative to Firebase
- [[spring-nosql-databases]] - Server-side NoSQL comparison
