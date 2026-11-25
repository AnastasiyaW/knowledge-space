---
title: "STL-Container"
category: concepts
tags: [cpp, stl, containers, vector, map, data-structures]
level: 3
source_sha256: 3abfb672079c1858debf202b3173a646fd99c909c1f143bcd50e778987192818
translation: machine
translated_at: '2026-10-24'
---
# STL-Container {#stl-containers}

Container der Standard Template Library: typsichere, per RAII verwaltete Sammlungen mit klar definierten Komplexitätsgarantien.

## Wichtige Fakten {#key-facts}

- Sequenzcontainer: `vector`, `deque`, `list`, `forward_list`, `array`
- Assoziativ (geordnet): `set`, `map`, `multiset`, `multimap` - Rot-Schwarz-Baum, O(log n)
- Ungeordnet (Hash): `unordered_set`, `unordered_map` - Hashtabelle, O(1) im Mittel
- Container-Adaptoren: `stack`, `queue`, `priority_queue` - umhüllen den zugrunde liegenden Container
- `std::vector` ist der Standardcontainer - cache-freundlich, zusammenhängender Speicher
- `std::array<T,N>` - auf dem Stack alloziert, feste Größe, kein Overhead gegenüber einem C-Array
- Alle Container besitzen ihre Elemente (Wertsemantik, tiefe Kopie beim Kopieren des Containers)
- Die Regeln zur Iterator-Invalidierung unterscheiden sich je Container - unbedingt zu beachten
- C++17: `std::optional`, `std::variant`, `std::any` - Vokabulartypen (keine Container, werden aber häufig zusammen genannt)
- `emplace_back` statt `push_back` verwenden für Konstruktion an Ort und Stelle (vermeidet temporäres Objekt)

## Muster {#patterns}

### vector - Standardwahl {#vector-default-choice}

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

v.push_back(6);              // copy/move to end
v.emplace_back(7);           // construct in-place at end
v.reserve(100);              // pre-allocate (no reallocation until size > 100)
v.shrink_to_fit();           // release excess capacity

// Erase-remove idiom
v.erase(std::remove(v.begin(), v.end(), 3), v.end());

// C++20: std::erase
std::erase(v, 3);            // remove all 3s
std::erase_if(v, [](int x) { return x % 2 == 0; });

// Iterate
for (const auto& elem : v) { /* ... */ }
for (auto it = v.begin(); it != v.end(); ++it) { /* ... */ }
```

### map / unordered_map {#map-unordered_map}

```cpp
std::map<std::string, int> ages;  // ordered by key

ages["Alice"] = 30;
ages.insert({"Bob", 25});
ages.emplace("Carol", 28);

// Structured bindings (C++17)
for (const auto& [name, age] : ages) {
    std::cout << name << ": " << age << '\n';
}

// Safe lookup
if (auto it = ages.find("Alice"); it != ages.end()) {
    std::cout << it->second;  // 30
}

// C++17: try_emplace - doesn't move-from argument if key exists
ages.try_emplace("Alice", 99);  // no-op, Alice already exists

// C++17: insert_or_assign - always sets value
ages.insert_or_assign("Alice", 31);  // updates Alice to 31
```

### set {#set}

```cpp
std::set<int> s = {5, 3, 1, 4, 2};
// Always sorted: 1 2 3 4 5

auto [it, inserted] = s.insert(3);  // inserted = false (already exists)

// C++20: contains
if (s.contains(3)) { /* ... */ }

// Before C++20
if (s.count(3) > 0) { /* ... */ }
if (s.find(3) != s.end()) { /* ... */ }
```

### array und span {#array-and-span}

```cpp
// Fixed-size, stack-allocated
std::array<int, 5> arr = {1, 2, 3, 4, 5};
constexpr auto size = arr.size();  // compile-time

// C++20: span - non-owning view
void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
}
process(arr);
process(vec);
process({ptr, count});
```

### Containervergleich {#container-comparison}

```cpp
// Random access, contiguous memory, cache-friendly
std::vector<T>          // O(1) back, O(n) front/middle

// Double-ended, O(1) front and back
std::deque<T>           // O(1) front+back, O(n) middle

// O(1) insert/erase anywhere with iterator
std::list<T>            // O(1) splice, O(n) access by index

// Sorted keys, O(log n) all ops
std::map<K,V>           // ordered iteration, balanced tree

// Hash-based, O(1) average
std::unordered_map<K,V> // fastest lookup, no ordering
```

## Fallstricke {#gotchas}

- **Problem:** `vector::operator[]` führt keine Bereichsprüfung durch -> undefiniertes Verhalten (UB) bei Zugriff außerhalb des Bereichs -> **Lösung:** `.at()` für geprüften Zugriff verwenden oder `[]` mit eigener Bereichsprüfung
- **Problem:** Iteratoren werden nach `vector::push_back` ungültig, wenn eine Neuallokation stattfindet -> **Lösung:** `reserve()` verwenden oder Iteratoren nicht über Einfügeoperationen hinweg halten
- **Problem:** `map[key]` fügt einen Standardwert ein, wenn der Schlüssel fehlt -> **Lösung:** `find()`, `count()` oder `contains()` (C++20) für Suchen ohne Einfügen verwenden
- **Problem:** `unordered_map` mit einer schlechten Hashfunktion fällt auf O(n) zurück -> **Lösung:** Eine gute Hashfunktion für eigene Typen bereitstellen; für performancekritischen Code `robin_map` in Betracht ziehen
- **Problem:** Speicherung von `std::vector<bool>` - es handelt sich um einen speziellen Proxy-Typ und nicht um einen echten Container -> **Lösung:** `std::vector<char>` oder `std::bitset<N>` für eine echte Speicherung von bool-Werten verwenden

## Siehe auch {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference: Container](https://en.cppreference.com/w/cpp/container)
