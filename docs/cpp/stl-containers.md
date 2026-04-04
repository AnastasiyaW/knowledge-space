---
title: STL Containers
category: concepts
tags: [cpp, stl, containers, vector, map, data-structures]
---

# STL Containers

Standard Template Library containers - type-safe, RAII-managed collections with well-defined complexity guarantees.

## Key Facts

- Sequence containers: `vector`, `deque`, `list`, `forward_list`, `array`
- Associative (ordered): `set`, `map`, `multiset`, `multimap` - red-black tree, O(log n)
- Unordered (hash): `unordered_set`, `unordered_map` - hash table, O(1) average
- Container adaptors: `stack`, `queue`, `priority_queue` - wrap underlying container
- `std::vector` is the default container - cache-friendly, contiguous memory
- `std::array<T,N>` - stack-allocated, fixed-size, zero overhead over C array
- All containers own their elements (value semantics, deep copy on container copy)
- Iterators invalidation rules differ per container - critical to know
- C++17: `std::optional`, `std::variant`, `std::any` - vocabulary types (not containers but often grouped)
- Use `emplace_back` over `push_back` for in-place construction (avoids temporary)

## Patterns

### vector - Default Choice

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

### map / unordered_map

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

### set

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

### array and span

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

### Container Comparison

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

## Gotchas

- **Issue:** `vector::operator[]` has no bounds checking -> UB on out-of-range -> **Fix:** Use `.at()` for checked access, or `[]` with your own bounds check
- **Issue:** Iterators invalidated after `vector::push_back` if reallocation occurs -> **Fix:** Use `reserve()` or don't hold iterators across insertions
- **Issue:** `map[key]` inserts default value if key missing -> **Fix:** Use `find()`, `count()`, or `contains()` (C++20) for lookup without insertion
- **Issue:** `unordered_map` with poor hash function degrades to O(n) -> **Fix:** Provide good hash for custom types; consider `robin_map` for performance-critical code
- **Issue:** Storing `std::vector<bool>` - it's a special proxy type, not a real container -> **Fix:** Use `std::vector<char>` or `std::bitset<N>` for actual bool storage

## See Also

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference: Containers](https://en.cppreference.com/w/cpp/container)
