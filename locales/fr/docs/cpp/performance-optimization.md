---
title: "Optimisation des performances"
category: concepts
tags: [cpp, performance, cache, optimization, profiling, benchmarking]
level: 4
source_sha256: 38723d6630ac44fc52f4fa4f4362b82331ac5c2e1a65f8b30b15a4865b3684b2
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des performances {#performance-optimization}

Fondamentaux de la performance en C++ : efficacité du cache, sémantique de déplacement, stratégies d'allocation, optimisations du compilateur et techniques de profilage.

## Points clés {#key-facts}

- Mesurer d'abord, optimiser ensuite. Utiliser un profileur (perf, VTune, Instruments), et non des suppositions
- Les défauts de cache dominent : accès mémoire séquentiel >> accès aléatoire (différence de plus de 100x)
- `std::vector` est meilleur que `std::list` dans presque tous les cas, grâce à la localité du cache
- La sémantique de déplacement élimine les copies : passage par valeur + move pour les paramètres de type sink
- `reserve()` sur les vecteurs évite les réallocations dans les boucles
- Optimisation des petits tampons (SBO) : `std::string` et `std::function` évitent le tas pour les petites données
- `inline` est une indication de liaison, pas une indication de performance : c'est le compilateur qui décide de l'inlining
- `[[likely]]` / `[[unlikely]]` (C++20) : indications pour la prédiction de branchement
- `-O2` / `-O3` pour la version de production ; `-Og` pour le débogage avec optimisations
- Optimisation à l'édition de liens (LTO) : `-flto` permet l'inlining entre unités de traduction
- Optimisation guidée par profil (PGO) : compiler, exécuter, recompiler avec les données de profil

## Motifs {#patterns}

### Disposition des données adaptée au cache {#cache-friendly-data-layout}

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

### Éviter les copies {#avoiding-copies}

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

### Reserve et Shrink {#reserve-and-shrink}

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

### Calcul constexpr {#constexpr-computation}

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

### Indications pour le compilateur {#compiler-hints}

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

### Allocateur personnalisé (pool) {#custom-allocator-pool}

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

## Pièges {#gotchas}

- **Problème :** Optimisation prématurée sans profilage -> on optimise le mauvais chemin d'exécution -> **Solution :** Profiler d'abord. 90 % du temps se situe dans 10 % du code. Optimiser le chemin critique.
- **Problème :** `std::endl` vide le flux à chaque ligne -> 10 à 100 fois plus lent que `'\n'` -> **Solution :** Utiliser `'\n'` pour les sauts de ligne, et `std::endl` uniquement lorsqu'un vidage est nécessaire
- **Problème :** Passer un `std::string` par valeur alors qu'on ne fait que le lire -> copie inutile -> **Solution :** Utiliser `std::string_view` ou `const std::string&` pour un accès en lecture seule
- **Problème :** Surcoût du compteur de références atomique de `shared_ptr` dans du code mono-thread -> **Solution :** Utiliser `unique_ptr` lorsque la propriété partagée n'est pas nécessaire. Le compteur de références de `shared_ptr` est toujours atomique.
- **Problème :** Un appel de fonction virtuelle dans une boucle serrée empêche l'inlining -> **Solution :** Utiliser le CRTP pour le polymorphisme statique, ou dévirtualiser avec `final`

## Voir aussi {#see-also}

- [[move-semantics]]
- [[stl-containers]]
- [[const-and-type-safety]]
- [[cmake-build-systems]]
