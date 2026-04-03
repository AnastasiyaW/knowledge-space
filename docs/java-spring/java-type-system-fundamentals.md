---
title: Java Type System and Language Fundamentals
category: concepts
tags: [java-spring, java, types, primitives, strings, generics]
---

# Java Type System and Language Fundamentals

Core Java type system covering primitives, wrappers, strings, type casting, generics, and exception handling. Foundation for all Java/Spring development.

## Key Facts

- Java has 8 primitive types: `byte` (1B), `short` (2B), `int` (4B), `long` (8B), `float` (4B), `double` (8B), `char` (2B), `boolean` (1 bit)
- Wrapper classes (`Integer`, `Long`, etc.) are required for generics: `List<Integer>` not `List<int>`
- Strings are immutable objects stored in JVM string pool
- `==` compares references, `.equals()` compares content - always use `.equals()` for strings
- Widening casts are implicit (`int` -> `long`), narrowing requires explicit cast and may lose data
- `BigDecimal` for precise arithmetic (financial) - always use String constructor, never double

## Patterns

### String Operations
```java
String s = "hello";
s.length();              // 5
s.substring(1, 4);       // "ell" (endIndex exclusive)
s.contains("ell");       // true
s.indexOf("l");          // 2
s.toUpperCase();         // "HELLO" - returns NEW string
s.replace("l", "r");     // "herro"
s.charAt(0);             // 'h'
s.trim();                // strip whitespace

// Parsing
int parsed = Integer.parseInt("42");
double d = Double.parseDouble("3.14");
```

### Generics
```java
public class Box<T> {
    private T content;
    public void set(T item) { this.content = item; }
    public T get() { return content; }
}

// Bounded generics
public <T extends Comparable<T>> T findMax(List<T> list) { ... }
```

### Exception Handling
```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Division by zero: " + e.getMessage());
} catch (Exception e) {
    System.out.println("General: " + e.getMessage());
} finally {
    // always executes
}
```

Hierarchy: `Throwable` -> `Exception` (+ `RuntimeException`) / `Error`. Checked exceptions must be caught or declared in Java.

### Comparable and Comparator
```java
// Natural ordering - class implements Comparable
public class User implements Comparable<User> {
    @Override
    public int compareTo(User other) {
        return this.name.compareTo(other.name);
    }
}

// Custom ordering - external Comparator
users.sort(Comparator.comparing(User::getAge).reversed());
```

### BigDecimal for Financial Math
```java
BigDecimal price = new BigDecimal("19.99");   // String constructor!
BigDecimal tax = new BigDecimal("0.08");
BigDecimal total = price.multiply(BigDecimal.ONE.add(tax));
// NEVER: new BigDecimal(19.99) - imprecise due to floating point
```

## Gotchas

- `String s1 = "hello"; String s2 = new String("hello"); s1 == s2` is `false` - different references
- `s.toUpperCase()` creates a NEW string, original is unchanged (immutability)
- `Integer.parseInt()` throws `NumberFormatException` for invalid input
- Narrowing cast truncates, does not round: `(int) 9.78` = `9`
- Autoboxing can cause `NullPointerException`: `Integer x = null; int y = x;`

## See Also

- [[kotlin-language-features]] - Kotlin equivalents and extensions
- [[java-collections-streams]] - Collection framework and Stream API
- [[java-concurrency]] - Threading and atomic types
