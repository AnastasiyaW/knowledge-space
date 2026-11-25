---
title: "STL-Algorithmen und Ranges"
category: concepts
tags: [cpp, stl, algorithms, ranges, sort, transform, cpp20]
level: 3
source_sha256: ea084749ae48f1700dc2203c1b11d19a203cf48e04e71774eb0b53c2431c8f7e
translation: machine
translated_at: '2026-10-24'
---
# STL-Algorithmen und Ranges {#stl-algorithms-and-ranges}

`<algorithm>` bietet über 100 generische Algorithmen, die mit Iteratoren arbeiten. C++20-Ranges ergänzen eine kombinierbare, verzögerte Pipeline-Syntax.

## Wichtige Fakten {#key-facts}

- Algorithmen arbeiten auf Iterator-Paaren `[begin, end)` - halboffener Bereich
- Nicht-modifizierend: `find`, `count`, `all_of`, `any_of`, `none_of`, `for_each`, `accumulate`
- Modifizierend: `transform`, `copy`, `fill`, `replace`, `remove`, `reverse`, `rotate`
- Sortieren: `sort`, `stable_sort`, `partial_sort`, `nth_element`
- Suchen: `binary_search`, `lower_bound`, `upper_bound`, `equal_range`
- `std::sort` ist Introsort (Quicksort + Heapsort + Insertion Sort) - garantiert O(n log n)
- `std::stable_sort` erhält die relative Reihenfolge gleicher Elemente
- `remove` / `remove_if` löschen nicht tatsächlich - sie verschieben Elemente und geben das neue Ende zurück
- C++17: parallele Ausführungsrichtlinien - `std::execution::par`, `seq`, `par_unseq`
- C++20: Ranges (`<ranges>`) - Algorithmen nehmen Container direkt entgegen, Views lassen sich verzögert kombinieren
- `std::ranges::sort(vec)` statt `std::sort(vec.begin(), vec.end())`

## Muster {#patterns}

### Häufige Algorithmen {#common-algorithms}

```cpp
std::vector<int> v = {5, 3, 1, 4, 2};

// Sort
std::sort(v.begin(), v.end());
std::sort(v.begin(), v.end(), std::greater<>());  // descending

// Find
auto it = std::find(v.begin(), v.end(), 3);
auto it2 = std::find_if(v.begin(), v.end(), [](int x) { return x > 3; });

// Transform
std::vector<int> squared;
std::transform(v.begin(), v.end(), std::back_inserter(squared),
    [](int x) { return x * x; });

// Accumulate (in <numeric>)
int sum = std::accumulate(v.begin(), v.end(), 0);

// Count
int evens = std::count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });

// All/Any/None
bool all_pos = std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });
```

### Erase-Remove-Idiom {#erase-remove-idiom}

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

// Classic (pre C++20)
v.erase(std::remove(v.begin(), v.end(), 2), v.end());

// With predicate
v.erase(std::remove_if(v.begin(), v.end(),
    [](int x) { return x < 3; }), v.end());

// C++20: much cleaner
std::erase(v, 2);
std::erase_if(v, [](int x) { return x < 3; });
```

### C++20-Ranges {#c20-ranges}

```cpp
#include <ranges>
namespace rv = std::views;

std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Ranges algorithms - take containers directly
std::ranges::sort(v);
auto it = std::ranges::find(v, 5);

// Views - lazy, composable pipelines
auto result = v
    | rv::filter([](int x) { return x % 2 == 0; })   // even numbers
    | rv::transform([](int x) { return x * x; })       // square them
    | rv::take(3);                                       // first 3

for (int x : result) { std::cout << x << ' '; }  // 4 16 36

// Collect into vector (C++23: ranges::to)
auto collected = result | std::ranges::to<std::vector>();  // C++23

// Pre-C++23: manual collection
std::vector<int> out;
std::ranges::copy(result, std::back_inserter(out));
```

### Parallele Algorithmen (C++17) {#parallel-algorithms-c17}

```cpp
#include <execution>

std::vector<int> v(1'000'000);
std::iota(v.begin(), v.end(), 0);

// Parallel sort
std::sort(std::execution::par, v.begin(), v.end());

// Parallel transform-reduce
int sum = std::transform_reduce(std::execution::par,
    v.begin(), v.end(), 0, std::plus<>(),
    [](int x) { return x * x; });
```

### Binäre Suche (auf sortierten Daten) {#binary-search-on-sorted-data}

```cpp
std::vector<int> v = {1, 3, 5, 7, 9, 11};

bool found = std::binary_search(v.begin(), v.end(), 5);       // true
auto lb = std::lower_bound(v.begin(), v.end(), 5);            // -> 5
auto ub = std::upper_bound(v.begin(), v.end(), 5);            // -> 7
auto [lo, hi] = std::equal_range(v.begin(), v.end(), 5);      // range of 5s
```

## Stolperfallen {#gotchas}

- **Problem:** `remove` ändert die Containergröße nicht - es verschiebt nur Elemente -> **Lösung:** Immer mit `erase` kombinieren (Erase-Remove-Idiom) oder die C++20-Funktionen `std::erase`/`std::erase_if` verwenden
- **Problem:** Die Verwendung von `sort` auf `list` benötigt aufgrund von Random-Access-Iteratoren zusätzlichen Speicher in Höhe von O(n log n) -> **Lösung:** Die Member-Funktion `list::sort()` verwenden, die mit O(1) Speicher auskommt und O(n log n) benötigt
- **Problem:** Ranges-Views sind verzögert - sie werden erst bei Iteration ausgeführt. Hängende Referenzen, wenn die Quelle zerstört wurde -> **Lösung:** Views materialisieren, bevor die Quelle den Gültigkeitsbereich verlässt
- **Problem:** Parallele Algorithmen setzen voraus, dass Elemente unabhängig voneinander verarbeitet werden können - Data Races bei gemeinsam genutztem Zustand -> **Lösung:** `std::atomic` verwenden oder das Design so ändern, dass kein gemeinsam veränderlicher Zustand entsteht

## Siehe auch {#see-also}

- [[stl-containers]]
- [[lambda-expressions]]
- [[templates-and-concepts]]
- [cppreference: Algorithms](https://en.cppreference.com/w/cpp/algorithm)
