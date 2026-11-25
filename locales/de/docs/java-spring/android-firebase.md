---
title: "Android Firebase – Auth, Firestore, Storage"
category: reference
tags: [java-spring, android, firebase, authentication, firestore, cloud-storage]
level: 3
source_sha256: 5082cc4e3396f045a5f911199ce89de876cdd31ec176de247f054d819e525363
translation: machine
translated_at: '2026-10-24'
---
# Android Firebase – Auth, Firestore, Storage {#android-firebase-auth-firestore-storage}

Firebase-Integration für Android: Authentication (E-Mail/Passwort), Cloud Firestore (NoSQL-Datenbank), Cloud Storage (Datei-Uploads) und Echtzeit-Listener.

## Key Facts {#key-facts}

- Firebase-Setup: Projekt in der Console anlegen, Android-App hinzufügen, `google-services.json` in das Verzeichnis app/ herunterladen
- Die Firebase BOM (Bill of Materials) verwaltet die Versionskompatibilität zwischen den Firebase-Bibliotheken
- Firebase Auth unterstützt E-Mail/Passwort, Google Sign-In, Telefon und anonyme Anmeldung
- Firestore ist eine dokumentenorientierte NoSQL-Datenbank mit Echtzeit-Synchronisation
- `addSnapshotListener` liefert Echtzeit-Updates ohne Polling
- Cloud Storage für Datei-Uploads (Bilder, Videos) mit Abruf der Download-URL

## Patterns {#patterns}

### Authentication {#authentication}
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

### Cloud Firestore CRUD {#cloud-firestore-crud}
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

### Cloud Storage {#cloud-storage}
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

### Setup Dependencies {#setup-dependencies}
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

## Gotchas {#gotchas}

- `google-services.json` muss im Verzeichnis `app/` liegen, nicht im Projekt-Root
- Firestore-Abfragen mit `whereEqualTo` und `orderBy` auf verschiedenen Feldern erfordern einen zusammengesetzten Index (Firestore protokolliert die URL zum Erstellen)
- `addSnapshotListener` hält die Verbindung offen – den Listener in `onStop()` entfernen, um Bandbreite zu sparen
- Firebase-Operationen sind asynchron – nicht davon ausgehen, dass Daten nach einem Aufruf synchron verfügbar sind
- Die Dokumentgröße in Firestore ist auf 1 MB begrenzt; die Verschachtelungstiefe von Collections ist unbegrenzt, sollte aber aus Performance-Gründen flach gehalten werden

## See Also {#see-also}

- [[android-architecture-mvvm]] - Repository-Pattern mit Firebase als Datenquelle
- [[android-networking-retrofit]] - REST-API-Alternative zu Firebase
- [[spring-nosql-databases]] - Vergleich serverseitiger NoSQL-Datenbanken
