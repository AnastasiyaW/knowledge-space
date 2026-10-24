---
title: "Performance-Optimierung"
category: concepts
tags: [cpp, performance, cache, optimization, profiling, benchmarking]
level: 4
source_sha256: 38723d6630ac44fc52f4fa4f4362b82331ac5c2e1a65f8b30b15a4865b3684b2
translation: machine
translated_at: '2026-10-24'
---
# Performance-Optimierung {#performance-optimization}

Grundlagen der C++-Performance: Cache-Effizienz, Move-Semantik, Allokationsstrategien, Compiler-Optimierungen und Profiling-Techniken.

## Kernfakten {#key-facts}

- Zuerst messen, dann optimieren. Profiler verwenden (perf, VTune, Instruments), nicht raten
- Cache-Misses dominieren: sequentieller Speicherzugriff >> zufälliger Zugriff (Unterschied von 100x und mehr)
- `std::vector` schlägt `std::list` in fast allen Fällen aufgrund der Cache-Lokalität
- Move-Semantik vermeidet Kopien: Übergabe per Wert plus Move für Sink-Parameter
- `reserve()` auf Vektoren verhindert Reallokation in Schleifen
- Small Buffer Optimization (SBO): `std::string` und `std::function` vermeiden den Heap für kleine Daten
- `inline` ist ein Linkage-Hinweis, kein Performance-Hinweis - der Compiler entscheidet über Inlining
- `[[likely]]` / `[[unlikely]]` (C++20) - Hinweise für die Branch Prediction
- `-O2` / `-O3` für Release; `-Og` für Debug mit Optimierungen
- Link-Time Optimization (LTO): `-flto` ermöglicht Inlining über Übersetzungseinheiten hinweg
- Profile-Guided Optimization (PGO): kompilieren, ausführen, mit Profildaten neu kompilieren

## Muster {#patterns}

### Cache-freundliches Datenlayout {#cache-friendly-data-layout}

```cpp
// BAD: Array of Structs with unused fields (AoS)
struct ParticleBad {
    float x, y, z;       // position (hot)
    float r, g, b, a;    // color (cold)
    std::string name;    // metadata (cold)
    float vx, vy, vz;    // velocity (hot)
};
std::vector<ParticleBad> particles;  // iterating position touches cold data

// GOOD: Struct of Arrays (SoA) - separate hot from cold
struct Particles {
    std::vector<float> x, y, z;       // positions together
    std::vector<float> vx, vy, vz;    // velocities together
    std::vector<float> r, g, b, a;    // colors together (separate cache lines)
};
// Physics update only touches x,y,z,vx,vy,vz - no cache pollution from colors
```

### Vermeiden von Kopien {#avoiding-copies}

```cpp
// Return by value - NRVO eliminates copy
std::vector<int> generate() {
    std::vector<int> result;
    result.reserve(1000);
    for (int i = 0; i < 1000; ++i) result.push_back(i);
    return result;  // NRVO: constructed directly in caller
}

// Sink parameter: by value + move
class Registry {
    std::vector<std::string> items_;
public:
    void add(std::string item) {        // copy/move into param
        items_.push_back(std::move(item)); // move into container
    }
};

// Pass large read-only by const ref
void process(const std::vector<int>& data);  // no copy
void process(std::span<const int> data);      // even lighter (C++20)
```

### Reserve und Shrink {#reserve-and-shrink}

```cpp
std::vector<int> v;
v.reserve(10000);  // single allocation up front

for (int i = 0; i < 10000; ++i) {
    v.push_back(i);  // no reallocations
}

// Release excess memory
v.shrink_to_fit();

// For maps: rehash to reduce load factor
std::unordered_map<int, int> m;
m.reserve(1000);  // pre-allocate buckets
```

### constexpr-Berechnung {#constexpr-computation}

```cpp
// Move computation to compile time
constexpr auto lookup_table = [] {
    std::array<int, 256> table{};
    for (int i = 0; i < 256; ++i) {
        table[i] = (i * i) % 256;
    }
    return table;
}();

// Zero runtime cost - embedded in binary
int fast_square_mod(uint8_t x) {
    return lookup_table[x];
}
```

### Compiler-Hinweise {#compiler-hints}

```cpp
// Branch prediction
if ([[likely]] (ptr != nullptr)) {
    process(ptr);
} else [[unlikely]] {
    handle_error();
}

// Assume (C++23)
void process(int x) {
    [[assume(x > 0)]];  // compiler can optimize based on this
    // ...
}

// Restrict aliasing (compiler extension)
void add_arrays(float* __restrict a, const float* __restrict b, size_t n) {
    for (size_t i = 0; i < n; ++i) a[i] += b[i];  // auto-vectorized
}
```

### Benutzerdefinierter Allokator (Pool) {#custom-allocator-pool}

```cpp
#include <memory_resource>

// Stack-based buffer for temporary allocations
char buffer[4096];
std::pmr::monotonic_buffer_resource pool(buffer, sizeof(buffer));
std::pmr::vector<int> fast_vec(&pool);  // allocates from stack buffer

// No heap allocation until buffer exhausted
for (int i = 0; i < 100; ++i) {
    fast_vec.push_back(i);
}
```

## Fallstricke {#gotchas}

- **Problem:** Verfrühte Optimierung ohne Profiling -> es wird der falsche Codepfad optimiert -> **Lösung:** Zuerst profilen. 90 % der Zeit entfallen auf 10 % des Codes. Den Hot Path optimieren.
- **Problem:** `std::endl` leert den Stream bei jeder Zeile -> 10- bis 100-mal langsamer als `'\n'` -> **Lösung:** `'\n'` für Zeilenumbrüche verwenden, `std::endl` nur, wenn ein Flush nötig ist
- **Problem:** `std::string` per Wert übergeben, obwohl nur gelesen wird -> unnötige Kopie -> **Lösung:** `std::string_view` oder `const std::string&` für reinen Lesezugriff verwenden
- **Problem:** Atomarer Referenzzähler-Overhead von `shared_ptr` in single-threaded Code -> **Lösung:** `unique_ptr` verwenden, wenn kein geteiltes Eigentum nötig ist. Der Referenzzähler von `shared_ptr` ist immer atomar.
- **Problem:** Virtueller Funktionsaufruf in enger Schleife verhindert Inlining -> **Lösung:** CRTP für statischen Polymorphismus verwenden oder mit `final` devirtualisieren

## Siehe auch {#see-also}

- [[move-semantics]]
- [[stl-containers]]
- [[const-and-type-safety]]
- [[cmake-build-systems]]
