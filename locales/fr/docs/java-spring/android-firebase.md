---
title: "Android Firebase - Auth, Firestore, Storage"
category: reference
tags: [java-spring, android, firebase, authentication, firestore, cloud-storage]
level: 3
source_sha256: 5082cc4e3396f045a5f911199ce89de876cdd31ec176de247f054d819e525363
translation: machine
translated_at: '2026-10-24'
---
# Android Firebase - Auth, Firestore, Storage {#android-firebase-auth-firestore-storage}

Intégration de Firebase pour Android : Authentication (email/mot de passe), Cloud Firestore (base de données NoSQL), Cloud Storage (envoi de fichiers) et écouteurs en temps réel.

## Points clés {#key-facts}

- Configuration de Firebase : créer un projet dans la Console, ajouter une application Android, télécharger `google-services.json` dans app/
- Le Firebase BOM (Bill of Materials) gère la compatibilité des versions entre les bibliothèques Firebase
- Firebase Auth prend en charge l'email/mot de passe, Google Sign-In, le téléphone et l'authentification anonyme
- Firestore est une base de données NoSQL orientée documents avec synchronisation en temps réel
- `addSnapshotListener` fournit des mises à jour en temps réel sans interrogation périodique (polling)
- Cloud Storage pour l'envoi de fichiers (images, vidéos) avec récupération de l'URL de téléchargement

## Modèles d'usage {#patterns}

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

### CRUD Cloud Firestore {#cloud-firestore-crud}
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

### Dépendances de configuration {#setup-dependencies}
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

## Pièges à éviter {#gotchas}

- `google-services.json` doit se trouver dans le répertoire `app/`, et non à la racine du projet
- Les requêtes Firestore combinant `whereEqualTo` et `orderBy` sur des champs différents nécessitent un index composite (Firestore journalise l'URL permettant de le créer)
- `addSnapshotListener` maintient la connexion ouverte : supprimez l'écouteur dans `onStop()` pour économiser la bande passante
- Les opérations Firebase sont asynchrones : ne supposez pas que les données sont disponibles de manière synchrone après un appel
- La taille maximale d'un document Firestore est de 1 Mo ; la profondeur des collections n'est pas limitée, mais il est préférable de la garder faible pour les performances

## Voir aussi {#see-also}

- [[android-architecture-mvvm]] - Pattern Repository avec Firebase comme source de données
- [[android-networking-retrofit]] - Alternative REST aux API Firebase
- [[spring-nosql-databases]] - Comparaison des bases NoSQL côté serveur
