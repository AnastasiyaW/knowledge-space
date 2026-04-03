---
title: Java Collections and Stream API
category: concepts
tags: [java-spring, java, collections, streams, functional, list, map, set]
---

# Java Collections and Stream API

Java Collections Framework hierarchy, choosing the right collection, and functional-style data processing with the Stream API. Includes Kotlin equivalents.

## Key Facts

- `List` - ordered, allows duplicates; `Set` - no duplicates; `Queue` - FIFO; `Map` - key-value pairs
- `ArrayList` (O(1) access, O(n) insert) is the default choice over `LinkedList` (O(n) access, O(1) insert at known position)
- `HashMap` - unordered O(1), `LinkedHashMap` - insertion-ordered, `TreeMap` - sorted O(log n)
- `HashSet` - backed by HashMap, `TreeSet` - sorted, `LinkedHashSet` - insertion-ordered
- Streams are lazy - intermediate operations only execute when a terminal operation is called
- `Vector` and `Hashtable` are legacy synchronized classes - use `ConcurrentHashMap` and `CopyOnWriteArrayList` instead

## Patterns

### Collection Hierarchy
```
Iterable -> Collection -> List (ArrayList, LinkedList)
                       -> Set (HashSet, LinkedHashSet, TreeSet)
                       -> Queue (PriorityQueue, ArrayDeque)
Map (HashMap, LinkedHashMap, TreeMap) - separate hierarchy
```

### HashMap Usage
```java
Map<String, Integer> prices = new HashMap<>();
prices.put("item_a", 250);
prices.get("item_a");           // 250
prices.containsKey("item_a");   // true
prices.getOrDefault("x", 0);   // 0
prices.forEach((k, v) -> System.out.println(k + ": " + v));
```

### Stream Pipeline: Source -> Intermediate -> Terminal
```java
List<Item> items = getItems();

// Filter, transform, collect
List<String> names = items.stream()
    .filter(item -> item.getPrice() > 200)
    .map(Item::getName)
    .sorted()
    .collect(Collectors.toList());

// Aggregation
int total = items.stream().mapToInt(Item::getPrice).sum();

// Grouping
Map<Section, List<Item>> bySection = items.stream()
    .collect(Collectors.groupingBy(Item::getSection));

// Find / Match
Optional<Item> found = items.stream()
    .filter(i -> i.getName().equals("target"))
    .findFirst();
boolean any = items.stream().anyMatch(i -> i.getPrice() > 500);
```

### Key Stream Operations

**Intermediate** (lazy, return Stream): `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`

**Terminal** (trigger computation): `collect`, `forEach`, `reduce`, `count`, `min`, `max`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`, `toArray`

### Multi-Field Sorting
```java
orders.stream()
    .sorted(Comparator.comparing(Order::getStatus)
                       .thenComparing(Order::getDateTime).reversed())
    .collect(Collectors.toList());
```

### Kotlin Collection Functions
```kotlin
val items = getItems()
val names = items.filter { it.price > 200 }.map { it.name }.sorted()
val total = items.sumOf { it.price }
val bySection = items.groupBy { it.section }
val found = items.firstOrNull { it.name == "target" }
val (expensive, cheap) = items.partition { it.price > 200 }
val priceMap = items.associate { it.name to it.price }
val allTags = orders.flatMap { it.items }
```

### Kotlin Immutable vs Mutable Collections
```kotlin
val list = listOf(1, 2, 3)             // read-only
val mutableList = mutableListOf(1, 2)  // mutable
mutableList.add(3)

val map = mapOf("a" to 1)             // read-only
val mutableMap = mutableMapOf("a" to 1)
mutableMap["b"] = 2
```

## Gotchas

- `queryForObject` with JdbcTemplate returns `EmptyResultDataAccessException` if no rows found - use `Optional` or null check
- `Collectors.toList()` returns a mutable list; `List.of()` returns immutable
- Stream operations consume the stream - cannot reuse a stream after a terminal operation
- `HashMap` allows one null key; `ConcurrentHashMap` does not allow null keys or values
- `TreeMap`/`TreeSet` require elements to implement `Comparable` or provide a `Comparator`
- Kotlin `listOf()` returns read-only view, not truly immutable - the underlying list can still change if cast

## See Also

- [[java-type-system-fundamentals]] - Comparable/Comparator patterns
- [[algorithms-data-structures]] - Sorting algorithms and Big O
- [[java-concurrency]] - Thread-safe collections
