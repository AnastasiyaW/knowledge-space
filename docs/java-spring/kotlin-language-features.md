---
title: Kotlin Language Features
category: concepts
tags: [java-spring, kotlin, null-safety, coroutines, data-classes, sealed-classes]
---

# Kotlin Language Features

Kotlin-specific language features that differentiate it from Java: null safety, data classes, sealed classes, extension functions, string templates, and expression-oriented syntax.

## Key Facts

- `val` = immutable (preferred), `var` = mutable
- No primitive types at syntax level - everything is an object (`Int`, `Long`, etc.), compiler optimizes to JVM primitives
- Type inference: `val x = 42` inferred as `Int`
- `Unit` = Java's `void`
- Classes are `final` by default - use `open` to allow inheritance
- No checked exceptions in Kotlin
- `companion object` replaces Java `static`
- `internal` visibility = same module

## Patterns

### Null Safety
```kotlin
var s: String = "hello"    // non-nullable
var ns: String? = null     // nullable (? suffix)

ns.length                  // compile error!
ns?.length                 // safe call - returns null if ns is null
ns!!.length                // assert non-null - throws NPE if null
ns?.length ?: 0            // Elvis operator - default if null
```

### Data Classes
```kotlin
data class User(val name: String, val age: Int)
// Auto-generates: equals(), hashCode(), toString(), copy(), componentN()

val user = User("Alice", 30)
val copy = user.copy(age = 31)
val (name, age) = user  // destructuring
```

### Sealed Classes
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

### Extension Functions
```kotlin
fun String.addExclamation(): String = "$this!"
"Hello".addExclamation()  // "Hello!"

// Resolved at compile time (static methods), don't modify original class
```

### String Templates and Multiline
```kotlin
val name = "Kotlin"
val greeting = "Hello, $name!"
val expr = "Length: ${name.length}"
val multiline = """
    |First line
    |Second line
""".trimMargin()
```

### Expression-Oriented Syntax
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

### Functions
```kotlin
// Default parameters
fun greet(name: String = "World") = "Hello, $name!"

// Named arguments
greet(name = "Kotlin")

// Single-expression functions
fun add(a: Int, b: Int): Int = a + b
```

### Collection Operations (Built-in)
```kotlin
val items = listOf(1, 2, 3, 4, 5)
items.filter { it > 2 }.map { it * 2 }  // no .stream() needed

// Sequences for lazy evaluation
items.asSequence().filter { it > 2 }.map { it * 2 }.toList()
```

### Ranges and Loops
```kotlin
for (i in 0 until 10) { }          // 0..9
for (i in 10 downTo 0 step 2) { }  // 10, 8, 6, 4, 2, 0
list.forEach { println(it) }
list.forEachIndexed { index, item -> println("$index: $item") }
```

## Gotchas

- Explicit type conversion required: `val y: Long = x.toLong()` (no implicit widening)
- `companion object` can only exist once per class
- Extension functions are resolved statically - if a member function and extension have the same signature, the member wins
- `!!` operator should be used sparingly - defeats the purpose of null safety
- `open` must be added to both class and overridable functions

## See Also

- [[java-type-system-fundamentals]] - Java type system for comparison
- [[kotlin-coroutines]] - Async programming with coroutines
- [[android-jetpack-compose]] - Compose uses Kotlin features extensively
