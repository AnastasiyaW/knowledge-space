---
title: Java Type System
category: concepts
tags: [java, primitives, strings, type-casting, wrappers]
---
# Java Type System

## Key Facts

- Java has 8 primitive types: `byte` (8-bit), `short` (16-bit), `int` (32-bit), `long` (64-bit), `float` (32-bit), `double` (64-bit), `char` (16-bit), `boolean`
- `String` is NOT a primitive - it is a class (`java.lang.String`), immutable, stored on the heap
- Each primitive has a wrapper class: `Integer`, `Long`, `Double`, `Boolean`, etc. - required for generics and collections
- Autoboxing converts primitives to wrappers automatically; unboxing does the reverse
- `==` compares references for objects (including String), use `.equals()` for value comparison
- String pool: string literals are interned, `new String("x")` creates a separate heap object
- See [[kotlin-fundamentals]] for Kotlin's approach to nullability and type inference
- See [[java-collections]] for how wrapper types are used with generic collections

## Patterns

### Variable declaration

```java
// Primitives
int count = 10;
double price = 19.99;
boolean active = true;
char grade = 'A';
long bigNumber = 100_000_000L; // underscores for readability

// Wrapper classes
Integer nullableCount = null;  // primitives cannot be null
Double boxed = 3.14;           // autoboxing

// Strings
String name = "Alice";                      // string pool
String name2 = new String("Alice");         // heap, NOT interned
String greeting = "Hello, " + name + "!";   // concatenation
```

### Type casting

```java
// Widening (implicit) - no data loss
int i = 100;
long l = i;          // int -> long automatic
double d = l;        // long -> double automatic

// Narrowing (explicit) - potential data loss
double pi = 3.14159;
int truncated = (int) pi;  // 3 - decimal part lost

// String conversions
String s = String.valueOf(42);        // int -> String
int parsed = Integer.parseInt("42");  // String -> int
double dp = Double.parseDouble("3.14");
```

### StringBuilder for concatenation

```java
// Bad: creates many intermediate String objects in a loop
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;  // O(n^2) - new String each iteration
}

// Good: StringBuilder mutates in place
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();
```

## Gotchas

- **Symptom**: `Integer a = 127; Integer b = 127; a == b` returns `true`, but `Integer a = 128; Integer b = 128; a == b` returns `false` -> **Cause**: Java caches Integer values -128 to 127 -> **Fix**: Always use `.equals()` for wrapper comparison
- **Symptom**: `NullPointerException` on unboxing -> **Cause**: `Integer x = null; int y = x;` triggers NPE during unbox -> **Fix**: Null-check before unboxing, or use primitives when nullability is not needed
- **Symptom**: Floating-point comparison fails -> **Cause**: `0.1 + 0.2 != 0.3` due to IEEE 754 -> **Fix**: Use `BigDecimal` for financial calculations, or compare with epsilon tolerance

## See Also

- [[kotlin-fundamentals]] - Kotlin removes primitives/wrapper distinction at source level
- [[java-collections]] - Collections require wrapper types, not primitives
- Oracle Tutorial: [Primitive Data Types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)
- Oracle Tutorial: [Strings](https://docs.oracle.com/javase/tutorial/java/data/strings.html)
