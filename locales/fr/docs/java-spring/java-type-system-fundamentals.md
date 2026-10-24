---
title: "Système de types Java et fondamentaux du langage"
category: concepts
tags: [java-spring, java, types, primitives, strings, generics]
level: 2
source_sha256: 41ba9ff58bbaed2311ddb47464c6fee2d0ed02cdc169018fd1bdd5403e42068a
translation: machine
translated_at: '2026-10-24'
---
# Système de types Java et fondamentaux du langage {#java-type-system-and-language-fundamentals}

Système de types de base de Java couvrant les types primitifs, les wrappers, les chaînes de caractères, le transtypage, les génériques et la gestion des exceptions. Fondement de tout développement Java/Spring.

## Points clés {#key-facts}

- Java possède 8 types primitifs : `byte` (1 o), `short` (2 o), `int` (4 o), `long` (8 o), `float` (4 o), `double` (8 o), `char` (2 o), `boolean` (1 bit)
- Les classes wrapper (`Integer`, `Long`, etc.) sont requises pour les génériques : `List<Integer>` et non `List<int>`
- Les chaînes de caractères sont des objets immuables stockés dans le pool de chaînes de la JVM
- `==` compare les références, `.equals()` compare le contenu : utilisez toujours `.equals()` pour les chaînes
- Les conversions élargissantes sont implicites (`int` -> `long`), tandis que les conversions restrictives exigent un cast explicite et peuvent entraîner une perte de données
- `BigDecimal` pour les calculs arithmétiques précis (finance) : utilisez toujours le constructeur à partir d'une `String`, jamais à partir d'un `double`

## Modèles d'usage {#patterns}

### Opérations sur les chaînes {#string-operations}
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

### Génériques {#generics}
```java
public class Box<T> {
    private T content;
    public void set(T item) { this.content = item; }
    public T get() { return content; }
}

// Bounded generics
public <T extends Comparable<T>> T findMax(List<T> list) { ... }
```

### Gestion des exceptions {#exception-handling}
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

Hiérarchie : `Throwable` -> `Exception` (+ `RuntimeException`) / `Error`. Les exceptions vérifiées (checked) doivent être capturées ou déclarées en Java.

### Comparable et Comparator {#comparable-and-comparator}
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

### BigDecimal pour les calculs financiers {#bigdecimal-for-financial-math}
```java
BigDecimal price = new BigDecimal("19.99");   // String constructor!
BigDecimal tax = new BigDecimal("0.08");
BigDecimal total = price.multiply(BigDecimal.ONE.add(tax));
// NEVER: new BigDecimal(19.99) - imprecise due to floating point
```

## Pièges courants {#gotchas}

- `String s1 = "hello"; String s2 = new String("hello"); s1 == s2` vaut `false` : ce sont des références différentes
- `s.toUpperCase()` crée une NOUVELLE chaîne, l'original reste inchangé (immuabilité)
- `Integer.parseInt()` lève une `NumberFormatException` pour une entrée invalide
- Un cast restrictif tronque, il n'arrondit pas : `(int) 9.78` vaut `9`
- L'autoboxing peut provoquer une `NullPointerException` : `Integer x = null; int y = x;`

## Voir aussi {#see-also}

- [[kotlin-language-features]] - Équivalents Kotlin et extensions
- [[java-collections-streams]] - Framework Collections et API Stream
- [[java-concurrency]] - Threads et types atomiques
