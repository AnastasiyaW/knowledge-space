---
title: Performance Optimization
category: concepts
tags: [cpp, performance, cache, optimization, profiling, benchmarking]
---

# Performance Optimization

C++ performance fundamentals: cache efficiency, move semantics, allocation strategies, compiler optimizations, and profiling techniques.

## Key Facts

- Measure first, optimize second. Use profiler (perf, VTune, Instruments), not guesses
- Cache misses dominate: sequential memory access >> random access (100x+ difference)
- `std::vector` beats `std::list` for almost everything due to cache locality
- Move semantics eliminate copies: pass-by-value + move for sink parameters
- `reserve()` on vectors prevents reallocation in loops
- Small Buffer Optimization (SBO): `std::string`, `std::function` avoid heap for small data
- `inline` is a linkage hint, not a performance hint - compiler decides inlining
- `[[likely]]` / `[[unlikely]]` (C++20) - branch prediction hints
- `-O2` / `-O3` for release; `-Og` for debug with optimizations
- Link-Time Optimization (LTO): `-flto` enables cross-TU inlining
- Profile-Guided Optimization (PGO): compile, run, recompile with profile data

## Patterns

### Cache-Friendly Data Layout

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

### Avoiding Copies

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

### Reserve and Shrink

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

### constexpr Computation

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

### Compiler Hints

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

### Custom Allocator (Pool)

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

## Gotchas

- **Issue:** Premature optimization without profiling -> optimizing wrong code path -> **Fix:** Profile first. 90% of time is in 10% of code. Optimize the hot path.
- **Issue:** `std::endl` flushes stream on every line -> 10-100x slower than `'\n'` -> **Fix:** Use `'\n'` for newlines, `std::endl` only when flush is needed
- **Issue:** Passing `std::string` by value when only reading -> unnecessary copy -> **Fix:** Use `std::string_view` or `const std::string&` for read-only access
- **Issue:** `shared_ptr` atomic ref-count overhead in single-threaded code -> **Fix:** Use `unique_ptr` when shared ownership not needed. `shared_ptr` ref count is always atomic.
- **Issue:** Virtual function call in tight loop prevents inlining -> **Fix:** Use CRTP for static polymorphism, or devirtualize with `final`

## See Also

- [[move-semantics]]
- [[stl-containers]]
- [[const-and-type-safety]]
- [[cmake-build-systems]]
