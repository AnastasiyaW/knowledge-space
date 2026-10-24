---
title: "Java-Collections und Stream-API"
category: concepts
tags: [java-spring, java, collections, streams, functional, list, map, set]
level: 3
source_sha256: 3c7b4d1822991028a4851fd9f0f99c34c21845fbb50981054e18955f087afc9e
translation: machine
translated_at: '2026-10-24'
---
# Java-Collections und Stream-API {#java-collections-and-stream-api}

Hierarchie des Java Collections Framework, Auswahl der passenden Collection und funktionale Datenverarbeitung mit der Stream-API. Enthält Kotlin-Entsprechungen.

## Wichtige Fakten {#key-facts}

- `List` - geordnet, erlaubt Duplikate; `Set` - keine Duplikate; `Queue` - FIFO; `Map` - Schlüssel-Wert-Paare
- `ArrayList` (O(1) Zugriff, O(n) Einfügen) ist die Standardwahl gegenüber `LinkedList` (O(n) Zugriff, O(1) Einfügen an bekannter Position)
- `HashMap` - ungeordnet, O(1); `LinkedHashMap` - nach Einfügereihenfolge geordnet; `TreeMap` - sortiert, O(log n)
- `HashSet` - basiert auf HashMap; `TreeSet` - sortiert; `LinkedHashSet` - nach Einfügereihenfolge geordnet
- Streams sind lazy - Zwischenoperationen werden erst ausgeführt, wenn eine Terminaloperation aufgerufen wird
- `Vector` und `Hashtable` sind veraltete synchronisierte Klassen - stattdessen `ConcurrentHashMap` und `CopyOnWriteArrayList` verwenden

## Muster {#patterns}

### Collection-Hierarchie {#collection-hierarchy}
```php
Iterable -> Collection -> List (ArrayList, LinkedList)
                       -> Set (HashSet, LinkedHashSet, TreeSet)
                       -> Queue (PriorityQueue, ArrayDeque)
Map (HashMap, LinkedHashMap, TreeMap) - separate hierarchy
```

### Verwendung von HashMap {#hashmap-usage}
```java
Map<String, Integer> prices = new HashMap<>();
prices.put("item_a", 250);
prices.get("item_a");           // 250
prices.containsKey("item_a");   // true
prices.getOrDefault("x", 0);   // 0
prices.forEach((k, v) -> System.out.println(k + ": " + v));
```

### Stream-Pipeline: Quelle -> Zwischenoperation -> Terminaloperation {#stream-pipeline-source-intermediate-terminal}
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

### Wichtige Stream-Operationen {#key-stream-operations}

**Zwischenoperationen** (lazy, geben einen Stream zurück): `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`

**Terminaloperationen** (lösen die Berechnung aus): `collect`, `forEach`, `reduce`, `count`, `min`, `max`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`, `toArray`

### Sortierung nach mehreren Feldern {#multi-field-sorting}
```java
orders.stream()
    .sorted(Comparator.comparing(Order::getStatus)
                       .thenComparing(Order::getDateTime).reversed())
    .collect(Collectors.toList());
```

### Kotlin-Collection-Funktionen {#kotlin-collection-functions}
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

### Unveränderliche vs. veränderliche Collections in Kotlin {#kotlin-immutable-vs-mutable-collections}
```kotlin
val list = listOf(1, 2, 3)             // read-only
val mutableList = mutableListOf(1, 2)  // mutable
mutableList.add(3)

val map = mapOf("a" to 1)             // read-only
val mutableMap = mutableMapOf("a" to 1)
mutableMap["b"] = 2
```

## Stolperfallen {#gotchas}

- `queryForObject` mit JdbcTemplate liefert `EmptyResultDataAccessException`, wenn keine Zeilen gefunden werden - `Optional` verwenden oder auf null prüfen
- `Collectors.toList()` liefert eine veränderliche Liste; `List.of()` liefert eine unveränderliche
- Stream-Operationen verbrauchen den Stream - nach einer Terminaloperation kann ein Stream nicht wiederverwendet werden
- `HashMap` erlaubt einen null-Schlüssel; `ConcurrentHashMap` erlaubt weder null-Schlüssel noch null-Werte
- `TreeMap`/`TreeSet` erfordern, dass Elemente `Comparable` implementieren oder ein `Comparator` angegeben wird
- Kotlins `listOf()` liefert eine schreibgeschützte Sicht, keine wirklich unveränderliche Liste - die zugrunde liegende Liste kann bei einem Cast weiterhin verändert werden

## Siehe auch {#see-also}

- [[java-type-system-fundamentals]] - Muster für Comparable/Comparator
- [[algorithms-data-structures]] - Sortieralgorithmen und Big O
- [[java-concurrency]] - Threadsichere Collections
