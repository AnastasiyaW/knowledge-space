---
title: "Java-Typsystem und Sprachgrundlagen"
category: concepts
tags: [java-spring, java, types, primitives, strings, generics]
level: 2
source_sha256: 41ba9ff58bbaed2311ddb47464c6fee2d0ed02cdc169018fd1bdd5403e42068a
translation: machine
translated_at: '2026-10-24'
---
# Java-Typsystem und Sprachgrundlagen {#java-type-system-and-language-fundamentals}

Das Typsystem von Core Java mit Primitiven, Wrapper-Klassen, Strings, Typumwandlung, Generics und Exception-Behandlung. Grundlage für die gesamte Java-/Spring-Entwicklung.

## Key Facts {#key-facts}

- Java hat 8 primitive Typen: `byte` (1B), `short` (2B), `int` (4B), `long` (8B), `float` (4B), `double` (8B), `char` (2B), `boolean` (1 Bit)
- Wrapper-Klassen (`Integer`, `Long` usw.) sind für Generics erforderlich: `List<Integer>` statt `List<int>`
- Strings sind unveränderliche Objekte, die im String-Pool der JVM abgelegt werden
- `==` vergleicht Referenzen, `.equals()` vergleicht Inhalte – für Strings immer `.equals()` verwenden
- Erweiternde Casts erfolgen implizit (`int` -> `long`), verengende erfordern einen expliziten Cast und können Daten verlieren
- `BigDecimal` für präzise Arithmetik (Finanzwesen) – immer den String-Konstruktor verwenden, niemals `double`

## Patterns {#patterns}

### String Operations {#string-operations}
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

### Generics {#generics}
```java
public class Box<T> {
    private T content;
    public void set(T item) { this.content = item; }
    public T get() { return content; }
}

// Bounded generics
public <T extends Comparable<T>> T findMax(List<T> list) { ... }
```

### Exception Handling {#exception-handling}
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

Hierarchie: `Throwable` -> `Exception` (+ `RuntimeException`) / `Error`. Geprüfte Exceptions müssen in Java entweder abgefangen oder deklariert werden.

### Comparable and Comparator {#comparable-and-comparator}
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

### BigDecimal for Financial Math {#bigdecimal-for-financial-math}
```java
BigDecimal price = new BigDecimal("19.99");   // String constructor!
BigDecimal tax = new BigDecimal("0.08");
BigDecimal total = price.multiply(BigDecimal.ONE.add(tax));
// NEVER: new BigDecimal(19.99) - imprecise due to floating point
```

## Gotchas {#gotchas}

- `String s1 = "hello"; String s2 = new String("hello"); s1 == s2` ergibt `false` – unterschiedliche Referenzen
- `s.toUpperCase()` erzeugt einen NEUEN String, das Original bleibt unverändert (Unveränderlichkeit)
- `Integer.parseInt()` wirft eine `NumberFormatException` bei ungültiger Eingabe
- Verengender Cast schneidet ab, rundet nicht: `(int) 9.78` = `9`
- Autoboxing kann eine `NullPointerException` auslösen: `Integer x = null; int y = x;`

## See Also {#see-also}

- [[kotlin-language-features]] - Kotlin-Entsprechungen und Erweiterungen
- [[java-collections-streams]] - Collection-Framework und Stream-API
- [[java-concurrency]] - Threading und atomare Typen
