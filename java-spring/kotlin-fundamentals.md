---
title: Kotlin Fundamentals
category: concepts
tags: [kotlin, null-safety, coroutines, extensions, data-class, interop]
---
# Kotlin Fundamentals

## Key Facts

- Kotlin is 100% interoperable with Java - runs on JVM, can call Java code and vice versa
- `val` = immutable (like `final` in Java), `var` = mutable - prefer `val` whenever possible
- Null safety built into type system: `String` vs `String?` - compiler enforces null checks
- No primitive/wrapper distinction at source level - compiler optimizes to JVM primitives automatically
- Data classes generate `equals()`, `hashCode()`, `toString()`, `copy()`, `componentN()` functions
- Extension functions add methods to existing classes without inheritance or decoration
- `object` keyword creates singleton; `companion object` replaces Java's `static` members
- String templates: `"Hello, $name"` or `"Result: ${list.size}"` - no need for concatenation
- When expression replaces Java's switch - is an expression (returns value), supports pattern matching
- See [[java-type-system]] for Java's type system that Kotlin simplifies
- See [[android-architecture]] for Kotlin's dominant role in Android development

## Patterns

### Variables and types

```kotlin
// Immutable (preferred)
val name: String = "Alice"
val age = 30              // type inference

// Mutable
var count = 0
count++

// Nullable types
val email: String? = null
val length = email?.length        // safe call - returns null if email is null
val len = email?.length ?: 0      // elvis operator - default if null
val forced = email!!.length       // non-null assertion - throws if null
```

### String templates

```kotlin
val name = "Alice"
val age = 30

println("Name: $name, Age: $age")
println("Next year: ${age + 1}")
println("Upper: ${name.uppercase()}")
```

### Data classes

```kotlin
data class User(
    val name: String,
    val email: String,
    val age: Int = 0  // default parameter
)

val user = User("Alice", "alice@mail.com", 30)
val copy = user.copy(age = 31)         // copy with changes
val (name, email, _) = user            // destructuring
println(user)                           // User(name=Alice, email=alice@mail.com, age=30)
```

### When expression

```kotlin
val result = when (statusCode) {
    200 -> "OK"
    301 -> "Moved"
    404 -> "Not Found"
    in 500..599 -> "Server Error"
    else -> "Unknown"
}

// Type checking
fun describe(obj: Any): String = when (obj) {
    is String -> "String of length ${obj.length}" // smart cast
    is Int    -> "Integer: $obj"
    is List<*> -> "List of size ${obj.size}"
    else      -> obj.toString()
}
```

### Extension functions

```kotlin
// Add method to existing String class
fun String.toSlug(): String =
    this.lowercase().replace(" ", "-").replace(Regex("[^a-z0-9-]"), "")

"Hello World!".toSlug()  // "hello-world"

// Extension on nullable type
fun String?.orEmpty(): String = this ?: ""
```

### Collections

```kotlin
// Immutable (read-only)
val names = listOf("Alice", "Bob", "Charlie")
val map = mapOf("a" to 1, "b" to 2)

// Mutable
val mutableNames = mutableListOf("Alice")
mutableNames.add("Bob")

// Functional operations
val adults = users
    .filter { it.age >= 18 }
    .sortedBy { it.name }
    .map { it.name.uppercase() }

// fold/reduce
val total = prices.fold(BigDecimal.ZERO) { acc, price ->
    acc.add(price)
}
```

### Object and companion object

```kotlin
// Singleton
object DatabaseConfig {
    val url = "jdbc:postgresql://localhost/db"
    fun connect() { /* ... */ }
}
DatabaseConfig.connect()

// Companion object (static-like members)
class User(val name: String) {
    companion object {
        fun fromJson(json: String): User { /* ... */ }
    }
}
val user = User.fromJson("{...}")
```

### Kotlin-Java interop annotations

```kotlin
class BankAccount(
    @Volatile private var balance: Int  // @Volatile = Java volatile
) {
    @Synchronized   // = Java synchronized
    fun transfer(amount: Int) {
        balance -= amount
    }

    @JvmStatic      // accessible as static method from Java
    companion object {
        fun create(): BankAccount = BankAccount(0)
    }

    @JvmOverloads   // generates overloads for default params
    fun deposit(amount: Int, currency: String = "USD") { }
}
```

## Gotchas

- **Symptom**: `val list = listOf(1,2,3); list.add(4)` won't compile -> **Cause**: `listOf()` returns `List<T>` (read-only), not `MutableList<T>` -> **Fix**: Use `mutableListOf()` if mutation needed
- **Symptom**: NPE despite null safety -> **Cause**: Using `!!` operator, or interop with Java code that returns null -> **Fix**: Avoid `!!`; add `@Nullable`/`@NotNull` annotations to Java code; use `?.let { }` pattern
- **Symptom**: `object` declaration behaves differently from Java singleton -> **Cause**: Kotlin `object` is initialized lazily on first access (like `LazyHolder` pattern) -> **Fix**: This is usually the desired behavior; for eager init use `init` block
- **Symptom**: `data class` with mutable properties allows mutation via `copy()` -> **Cause**: `copy()` is shallow -> **Fix**: Use `val` for all data class properties; deep-copy mutable fields manually

## See Also

- [[java-type-system]] - Java types that Kotlin simplifies
- [[java-concurrency]] - Java threading that Kotlin replaces with coroutines
- [[android-architecture]] - Kotlin is the primary language for modern Android
- [[spring-boot-setup]] - Spring Boot supports Kotlin with Gradle Kotlin DSL
- Kotlin Docs: [Getting Started](https://kotlinlang.org/docs/getting-started.html)
- Kotlin Docs: [Kotlin for Java Developers](https://kotlinlang.org/docs/java-to-kotlin-guide.html)
