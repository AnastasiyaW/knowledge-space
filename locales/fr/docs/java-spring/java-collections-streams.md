---
title: "Collections Java et API Stream"
category: concepts
tags: [java-spring, java, collections, streams, functional, list, map, set]
level: 3
source_sha256: 3c7b4d1822991028a4851fd9f0f99c34c21845fbb50981054e18955f087afc9e
translation: machine
translated_at: '2026-10-24'
---
# Collections Java et API Stream {#java-collections-and-stream-api}

Hiérarchie du Java Collections Framework, choix de la collection adaptée, et traitement de données de style fonctionnel avec l'API Stream. Inclut les équivalents Kotlin.

## Points clés {#key-facts}

- `List` - ordonnée, autorise les doublons ; `Set` - pas de doublons ; `Queue` - FIFO ; `Map` - paires clé-valeur
- `ArrayList` (accès en O(1), insertion en O(n)) est le choix par défaut plutôt que `LinkedList` (accès en O(n), insertion en O(1) à une position connue)
- `HashMap` - non ordonnée, O(1) ; `LinkedHashMap` - ordonnée par ordre d'insertion ; `TreeMap` - triée, O(log n)
- `HashSet` - basée sur HashMap ; `TreeSet` - triée ; `LinkedHashSet` - ordonnée par ordre d'insertion
- Les Streams sont paresseux - les opérations intermédiaires ne s'exécutent que lorsqu'une opération terminale est appelée
- `Vector` et `Hashtable` sont des classes synchronisées héritées - utilisez plutôt `ConcurrentHashMap` et `CopyOnWriteArrayList`

## Patrons {#patterns}

### Hiérarchie des collections {#collection-hierarchy}
```php
Iterable -> Collection -> List (ArrayList, LinkedList)
                       -> Set (HashSet, LinkedHashSet, TreeSet)
                       -> Queue (PriorityQueue, ArrayDeque)
Map (HashMap, LinkedHashMap, TreeMap) - separate hierarchy
```

### Utilisation de HashMap {#hashmap-usage}
```java
Map<String, Integer> prices = new HashMap<>();
prices.put("item_a", 250);
prices.get("item_a");           // 250
prices.containsKey("item_a");   // true
prices.getOrDefault("x", 0);   // 0
prices.forEach((k, v) -> System.out.println(k + ": " + v));
```

### Pipeline Stream : Source -> Intermédiaire -> Terminale {#stream-pipeline-source-intermediate-terminal}
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

### Opérations Stream principales {#key-stream-operations}

**Intermédiaires** (paresseuses, retournent un Stream) : `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`

**Terminales** (déclenchent le calcul) : `collect`, `forEach`, `reduce`, `count`, `min`, `max`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`, `toArray`

### Tri multi-champs {#multi-field-sorting}
```java
orders.stream()
    .sorted(Comparator.comparing(Order::getStatus)
                       .thenComparing(Order::getDateTime).reversed())
    .collect(Collectors.toList());
```

### Fonctions de collection Kotlin {#kotlin-collection-functions}
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

### Collections Kotlin immuables et mutables {#kotlin-immutable-vs-mutable-collections}
```kotlin
val list = listOf(1, 2, 3)             // read-only
val mutableList = mutableListOf(1, 2)  // mutable
mutableList.add(3)

val map = mapOf("a" to 1)             // read-only
val mutableMap = mutableMapOf("a" to 1)
mutableMap["b"] = 2
```

## Pièges {#gotchas}

- `queryForObject` avec JdbcTemplate renvoie `EmptyResultDataAccessException` si aucune ligne n'est trouvée - utilisez `Optional` ou un test de nullité
- `Collectors.toList()` renvoie une liste modifiable ; `List.of()` renvoie une liste immuable
- Les opérations sur un Stream le consomment - impossible de réutiliser un Stream après une opération terminale
- `HashMap` autorise une clé null ; `ConcurrentHashMap` n'autorise ni clés ni valeurs null
- `TreeMap`/`TreeSet` exigent que les éléments implémentent `Comparable` ou fournissent un `Comparator`
- `listOf()` en Kotlin renvoie une vue en lecture seule, et non une structure réellement immuable - la liste sous-jacente peut toujours changer si elle est castée

## Voir aussi {#see-also}

- [[java-type-system-fundamentals]] - Patrons Comparable/Comparator
- [[algorithms-data-structures]] - Algorithmes de tri et notation Big O
- [[java-concurrency]] - Collections thread-safe
