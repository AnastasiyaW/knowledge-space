---
title: "Kotlin-Sprachmerkmale"
category: concepts
tags: [java-spring, kotlin, null-safety, coroutines, data-classes, sealed-classes]
level: 3
source_sha256: eb934d615af22aa19c2a252ca88ee1f2700ad480f93c513914ad0ea53d32ddfd
translation: machine
translated_at: '2026-10-24'
---
# Kotlin-Sprachmerkmale {#kotlin-language-features}

Kotlin-spezifische Sprachmerkmale, die Kotlin von Java unterscheiden: Null-Sicherheit, Data Classes, Sealed Classes, Extension Functions, String-Templates und ausdrucksorientierte Syntax.

## Wichtige Fakten {#key-facts}

- `val` = unveränderlich (bevorzugt), `var` = veränderlich
- Keine primitiven Typen auf Syntaxebene – alles ist ein Objekt (`Int`, `Long` usw.), der Compiler optimiert zu JVM-Primitiven
- Typinferenz: `val x = 42` wird als `Int` inferiert
- `Unit` = Javas `void`
- Klassen sind standardmäßig `final` – mit `open` wird Vererbung erlaubt
- Keine Checked Exceptions in Kotlin
- `companion object` ersetzt Javas `static`
- `internal`-Sichtbarkeit = gleiches Modul

## Muster {#patterns}

### Null-Sicherheit {#null-safety}
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

### Extension Functions {#extension-functions}
```kotlin
fun String.addExclamation(): String = "$this!"
"Hello".addExclamation()  // "Hello!"

// Resolved at compile time (static methods), don't modify original class
```

### String-Templates und mehrzeilige Strings {#string-templates-and-multiline}
```kotlin
val name = "Kotlin"
val greeting = "Hello, $name!"
val expr = "Length: ${name.length}"
val multiline = """
    |First line
    |Second line
""".trimMargin()
```

### Ausdrucksorientierte Syntax {#expression-oriented-syntax}
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

### Funktionen {#functions}
```kotlin
// Default parameters
fun greet(name: String = "World") = "Hello, $name!"

// Named arguments
greet(name = "Kotlin")

// Single-expression functions
fun add(a: Int, b: Int): Int = a + b
```

### Collection-Operationen (eingebaut) {#collection-operations-built-in}
```kotlin
val items = listOf(1, 2, 3, 4, 5)
items.filter { it > 2 }.map { it * 2 }  // no .stream() needed

// Sequences for lazy evaluation
items.asSequence().filter { it > 2 }.map { it * 2 }.toList()
```

### Bereiche und Schleifen {#ranges-and-loops}
```kotlin
for (i in 0 until 10) { }          // 0..9
for (i in 10 downTo 0 step 2) { }  // 10, 8, 6, 4, 2, 0
list.forEach { println(it) }
list.forEachIndexed { index, item -> println("$index: $item") }
```

## Fallstricke {#gotchas}

- Explizite Typkonvertierung erforderlich: `val y: Long = x.toLong()` (keine implizite Erweiterung)
- `companion object` kann pro Klasse nur einmal existieren
- Extension Functions werden statisch aufgelöst – haben eine Member-Funktion und eine Extension dieselbe Signatur, gewinnt die Member-Funktion
- Der `!!`-Operator sollte sparsam eingesetzt werden – er hebelt den Sinn der Null-Sicherheit aus
- `open` muss sowohl an der Klasse als auch an überschreibbaren Funktionen ergänzt werden

## Siehe auch {#see-also}

- [[java-type-system-fundamentals]] – Java-Typsystem zum Vergleich
- [[kotlin-coroutines]] – Asynchrone Programmierung mit Coroutinen
- [[android-jetpack-compose]] – Compose nutzt Kotlin-Features intensiv
