---
title: Java Collections Framework
category: concepts
tags: [java, collections, list, map, set, arraylist, hashmap, iterator]
---
# Java Collections Framework

## Key Facts

- Core interfaces hierarchy: `Collection` -> `List`, `Set`, `Queue`; separate `Map` interface
- `ArrayList<E>` - resizable array, O(1) random access, O(n) insert/remove in middle
- `LinkedList<E>` - doubly-linked, O(1) insert/remove at ends, O(n) random access
- `HashMap<K,V>` - key-value store, O(1) average get/put, unordered, allows one null key
- `TreeMap<K,V>` - sorted by key, O(log n) operations, implements `NavigableMap`
- `HashSet<E>` - unique elements, backed by HashMap, O(1) add/contains/remove
- Collections use generics: `List<String>`, `Map<String, Integer>` - type-safe at compile time
- `Collections.unmodifiableList()` wraps a list to prevent modification; Java 9+ `List.of()` creates truly immutable lists
- See [[java-type-system]] for why collections require wrapper types
- See [[java-concurrency]] for thread-safe concurrent collections

## Patterns

### ArrayList operations

```java
import java.util.ArrayList;
import java.util.List;

List<String> items = new ArrayList<>();
items.add("Guitar");
items.add("Drums");
items.add("Keyboard");

// Access
String first = items.get(0);       // "Guitar"
int size = items.size();           // 3
boolean has = items.contains("Drums"); // true

// Iterate
for (String item : items) {
    System.out.println(item);
}

// Stream API (Java 8+)
items.stream()
     .filter(s -> s.startsWith("G"))
     .map(String::toUpperCase)
     .forEach(System.out::println);

// Remove
items.remove("Drums");          // by value
items.remove(0);                // by index
```

### HashMap operations

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Double> prices = new HashMap<>();
prices.put("Guitar", 299.99);
prices.put("Drums", 499.99);
prices.put("Keyboard", 199.99);

// Access
Double price = prices.get("Guitar");             // 299.99
Double missing = prices.getOrDefault("Bass", 0.0); // 0.0

// Iterate
for (Map.Entry<String, Double> entry : prices.entrySet()) {
    System.out.println(entry.getKey() + ": $" + entry.getValue());
}

// Check
boolean exists = prices.containsKey("Guitar");   // true
int count = prices.size();                        // 3
```

### Sorting and comparators

```java
import java.util.Collections;
import java.util.Comparator;

List<String> names = new ArrayList<>(List.of("Charlie", "Alice", "Bob"));

// Natural order
Collections.sort(names);  // [Alice, Bob, Charlie]

// Custom comparator
names.sort(Comparator.comparingInt(String::length)); // by length

// Reverse
names.sort(Comparator.reverseOrder());
```

### Arrays (fixed-size)

```java
// Declaration + initialization
int[] ages = {25, 30, 35, 40};
String[] colors = new String[3];  // [null, null, null]

// Access
int first = ages[0];
int len = ages.length;     // property, not method

// Convert to List
List<Integer> list = Arrays.asList(1, 2, 3);  // fixed-size list
List<Integer> mutable = new ArrayList<>(Arrays.asList(1, 2, 3));
```

## Gotchas

- **Symptom**: `ConcurrentModificationException` during iteration -> **Cause**: Modifying a collection while iterating with for-each -> **Fix**: Use `Iterator.remove()`, or `removeIf()`, or iterate over a copy
- **Symptom**: `List.of()` throws `UnsupportedOperationException` on add/remove -> **Cause**: `List.of()` returns immutable list -> **Fix**: Wrap in `new ArrayList<>(List.of(...))` if mutation needed
- **Symptom**: HashMap returns `null` but key exists -> **Cause**: Key object's `hashCode()` or `equals()` not properly overridden -> **Fix**: Override both `hashCode()` and `equals()` consistently in key classes
- **Symptom**: `Arrays.asList()` modifications don't work -> **Cause**: Returns fixed-size list backed by array -> **Fix**: Wrap: `new ArrayList<>(Arrays.asList(...))`

## See Also

- [[java-concurrency]] - ConcurrentHashMap, CopyOnWriteArrayList for thread-safe access
- [[kotlin-fundamentals]] - Kotlin's `listOf()`, `mutableListOf()`, collection extensions
- [[design-patterns-behavioral]] - Iterator pattern is the foundation of Java's iteration
- Oracle Tutorial: [Collections](https://docs.oracle.com/javase/tutorial/collections/)
