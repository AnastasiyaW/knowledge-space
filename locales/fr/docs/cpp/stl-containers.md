---
title: "Conteneurs STL"
category: concepts
tags: [cpp, stl, containers, vector, map, data-structures]
level: 3
source_sha256: 3abfb672079c1858debf202b3173a646fd99c909c1f143bcd50e778987192818
translation: machine
translated_at: '2026-10-24'
---
# Conteneurs STL {#stl-containers}

Les conteneurs de la Standard Template Library sont des collections typées et gérées selon le principe RAII, avec des garanties de complexité bien définies.

## Points clés {#key-facts}

- Conteneurs séquentiels : `vector`, `deque`, `list`, `forward_list`, `array`
- Conteneurs associatifs (ordonnés) : `set`, `map`, `multiset`, `multimap` - arbre rouge-noir, O(log n)
- Conteneurs non ordonnés (hachage) : `unordered_set`, `unordered_map` - table de hachage, O(1) en moyenne
- Adaptateurs de conteneurs : `stack`, `queue`, `priority_queue` - encapsulent un conteneur sous-jacent
- `std::vector` est le conteneur par défaut - favorable au cache, mémoire contiguë
- `std::array<T,N>` - alloué sur la pile, taille fixe, surcoût nul par rapport à un tableau C
- Tous les conteneurs possèdent leurs éléments (sémantique de valeur, copie profonde lors de la copie du conteneur)
- Les règles d'invalidation des itérateurs diffèrent selon le conteneur - point crucial à connaître
- C++17 : `std::optional`, `std::variant`, `std::any` - types de vocabulaire (ce ne sont pas des conteneurs, mais on les regroupe souvent avec eux)
- Préférer `emplace_back` à `push_back` pour une construction sur place (évite un objet temporaire)

## Modèles d'utilisation {#patterns}

### vector - Choix par défaut {#vector-default-choice}

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

### array et span {#array-and-span}

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

### Comparaison des conteneurs {#container-comparison}

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

## Pièges {#gotchas}

- **Problème :** `vector::operator[]` ne vérifie pas les bornes -> UB en cas d'accès hors limites -> **Correctif :** Utiliser `.at()` pour un accès vérifié, ou `[]` avec votre propre vérification de bornes
- **Problème :** Les itérateurs sont invalidés après `vector::push_back` si une réallocation a lieu -> **Correctif :** Utiliser `reserve()` ou ne pas conserver d'itérateurs à travers des insertions
- **Problème :** `map[key]` insère une valeur par défaut si la clé est absente -> **Correctif :** Utiliser `find()`, `count()` ou `contains()` (C++20) pour une recherche sans insertion
- **Problème :** `unordered_map` avec une mauvaise fonction de hachage dégrade les performances à O(n) -> **Correctif :** Fournir une bonne fonction de hachage pour les types personnalisés ; envisager `robin_map` pour le code critique en performance
- **Problème :** Stocker un `std::vector<bool>` - c'est un type proxy particulier, pas un véritable conteneur -> **Correctif :** Utiliser `std::vector<char>` ou `std::bitset<N>` pour un stockage réel de booléens

## Voir aussi {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference : Conteneurs](https://en.cppreference.com/w/cpp/container)
