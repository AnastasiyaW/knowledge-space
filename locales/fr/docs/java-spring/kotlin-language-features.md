---
title: "Fonctionnalités du langage Kotlin"
category: concepts
tags: [java-spring, kotlin, null-safety, coroutines, data-classes, sealed-classes]
level: 3
source_sha256: eb934d615af22aa19c2a252ca88ee1f2700ad480f93c513914ad0ea53d32ddfd
translation: machine
translated_at: '2026-10-24'
---
# Fonctionnalités du langage Kotlin {#kotlin-language-features}

Fonctionnalités propres au langage Kotlin qui le distinguent de Java : sûreté vis-à-vis des valeurs nulles (null safety), data classes, sealed classes, fonctions d'extension, templates de chaînes et syntaxe orientée expression.

## Points clés {#key-facts}

- `val` = immuable (à privilégier), `var` = mutable
- Pas de types primitifs au niveau syntaxique : tout est un objet (`Int`, `Long`, etc.), le compilateur optimise vers les primitives de la JVM
- Inférence de type : `val x = 42` est inféré comme `Int`
- `Unit` = `void` de Java
- Les classes sont `final` par défaut : utiliser `open` pour autoriser l'héritage
- Pas d'exceptions vérifiées (checked exceptions) en Kotlin
- `companion object` remplace le `static` de Java
- La visibilité `internal` = même module

## Patterns {#patterns}

### Null Safety {#null-safety}
```kotlin
var s: String = "hello"    // non-nullable
var ns: String? = null     // nullable (? suffix)

ns.length                  // compile error!
ns?.length                 // safe call - returns null if ns is null
ns!!.length                // assert non-null - throws NPE if null
ns?.length ?: 0            // Elvis operator - default if null
```

### Data Classes {#data-classes}
```kotlin
data class User(val name: String, val age: Int)
// Auto-generates: equals(), hashCode(), toString(), copy(), componentN()

val user = User("Alice", 30)
val copy = user.copy(age = 31)
val (name, age) = user  // destructuring
```

### Sealed Classes {#sealed-classes}
```kotlin
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}

// Exhaustive when - compiler enforces all cases
when (result) {
    is Result.Success -> showData(result.data)
    is Result.Error -> showError(result.message)
    Result.Loading -> showSpinner()
}
```

### Fonctions d'extension {#extension-functions}
```kotlin
fun String.addExclamation(): String = "$this!"
"Hello".addExclamation()  // "Hello!"

// Resolved at compile time (static methods), don't modify original class
```

### Templates de chaînes et multiligne {#string-templates-and-multiline}
```kotlin
val name = "Kotlin"
val greeting = "Hello, $name!"
val expr = "Length: ${name.length}"
val multiline = """
    |First line
    |Second line
""".trimMargin()
```

### Syntaxe orientée expression {#expression-oriented-syntax}
```kotlin
// if is an expression
val result = if (x > 0) "positive" else "non-positive"

// when is an expression
val message = when {
    x > 0 -> "positive"
    x == 0 -> "zero"
    else -> "negative"
}

// try is an expression
val num = try { "42".toInt() } catch (e: Exception) { 0 }

// runCatching (idiomatic)
val result = runCatching { riskyOperation() }
    .getOrDefault(defaultValue)
    .onSuccess { println("OK: $it") }
    .onFailure { println("Error: ${it.message}") }
```

### Fonctions {#functions}
```kotlin
// Default parameters
fun greet(name: String = "World") = "Hello, $name!"

// Named arguments
greet(name = "Kotlin")

// Single-expression functions
fun add(a: Int, b: Int): Int = a + b
```

### Opérations sur les collections (intégrées) {#collection-operations-built-in}
```kotlin
val items = listOf(1, 2, 3, 4, 5)
items.filter { it > 2 }.map { it * 2 }  // no .stream() needed

// Sequences for lazy evaluation
items.asSequence().filter { it > 2 }.map { it * 2 }.toList()
```

### Intervalles et boucles {#ranges-and-loops}
```kotlin
for (i in 0 until 10) { }          // 0..9
for (i in 10 downTo 0 step 2) { }  // 10, 8, 6, 4, 2, 0
list.forEach { println(it) }
list.forEachIndexed { index, item -> println("$index: $item") }
```

## Pièges {#gotchas}

- Conversion de type explicite obligatoire : `val y: Long = x.toLong()` (pas d'élargissement implicite)
- `companion object` ne peut exister qu'une seule fois par classe
- Les fonctions d'extension sont résolues statiquement : si une fonction membre et une extension ont la même signature, la fonction membre l'emporte
- L'opérateur `!!` doit être utilisé avec parcimonie : il annule l'intérêt de la null safety
- `open` doit être ajouté à la fois à la classe et aux fonctions redéfinissables

## Voir aussi {#see-also}

- [[java-type-system-fundamentals]] - Système de types de Java, pour comparaison
- [[kotlin-coroutines]] - Programmation asynchrone avec les coroutines
- [[android-jetpack-compose]] - Compose utilise intensivement les fonctionnalités de Kotlin
