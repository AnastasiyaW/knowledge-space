---
title: "C++20 Ranges and Views"
description: "Composable lazy pipelines for sequence processing with the pipe operator and range adaptors"
---

# C++20 Ranges and Views

C++20 ranges provide a composable, lazy, pipeline-oriented way to work with sequences. They replace verbose iterator-pair patterns with cleaner syntax and often yield better performance through lazy evaluation.

## Core Concepts

**Range**: any type that provides `begin()` and `end()`. All standard containers are ranges.

**View**: a lightweight, non-owning, lazy range adaptor. Views do not copy data - they describe a transformation that is evaluated on-demand when iterated.

**Range algorithms**: drop-in replacements for `<algorithm>` functions that accept a whole container instead of iterator pairs.

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> nums = {32, 1, 26, 7, 10, 21};

// Old way: iterator pair
std::sort(nums.begin(), nums.end());

// C++20 ranges: pass entire container
std::ranges::sort(nums);
```

## View Pipeline (Pipe Operator)

Views compose via the `|` operator, similar to Unix pipes. Each stage produces a lazy view - no copies, no allocations, no computation until iteration begins.

```cpp
#include <ranges>
#include <vector>

struct PossibleValue {
    bool flag;
    int value;
};

std::vector<PossibleValue> values = {
    {true, 1}, {true, 2}, {false, 3}, {true, 4}, {false, 5}
};

auto flagged = [](const PossibleValue& pv) { return pv.flag; };

auto result = values
    | std::views::filter(flagged)           // keep only flagged
    | std::views::transform([](const PossibleValue& pv) { return pv.value; })  // extract int
    | std::views::reverse                   // reverse order
    | std::views::drop(1);                  // skip first element

// result is a lazy view: {4, 2} -> drop 1 -> {2}
// Nothing computed until iteration:
for (int v : result) {
    std::cout << v << " ";
}
```

Key property: the entire pipeline is **lazily evaluated**. No CPU cycles are spent evaluating the lambda or performing filtering until you begin iterating the result. This is both simpler AND faster than the equivalent imperative loop.

## Common View Adaptors

| Adaptor | Purpose |
|---------|---------|
| `std::views::filter(pred)` | Keep elements matching predicate |
| `std::views::transform(fn)` | Map each element through function |
| `std::views::take(n)` | First n elements |
| `std::views::drop(n)` | Skip first n elements |
| `std::views::reverse` | Reverse iteration order |
| `std::views::keys` / `std::views::values` | For map-like ranges |
| `std::views::split(delim)` | Split by delimiter |
| `std::views::join` | Flatten nested ranges |

## Ranges Sorting and Finding

```cpp
#include <ranges>
#include <algorithm>
#include <vector>

std::vector<int> v = {5, 3, 8, 1, 9};

// Sort with ranges
std::ranges::sort(v);

// Find with ranges
auto it = std::ranges::find(v, 8);

// Find with predicate
auto it2 = std::ranges::find_if(v, [](int x) { return x > 6; });

// Partial sort: nth_element
// Puts the correct element at position n, partitions rest
std::ranges::nth_element(v, v.begin() + 2);
// v[2] is now what would be at index 2 if fully sorted
// Elements before are <= v[2], elements after are >= v[2]
// Neither half is necessarily sorted - faster than partial_sort
```

## Algorithm Naming Conventions

The `<algorithm>` header uses consistent conventions that reduce the memorization burden:

- Parameters always follow same order: begin before end, source before destination
- `_if` suffix means predicate version: `find` vs `find_if`, `count` vs `count_if`
- `_copy` suffix means result goes to output iterator
- `_n` suffix means operates on count rather than range
- `ranges::` versions accept whole containers, `std::` versions take iterator pairs

## Compiler Support

Not all compilers fully support C++20 ranges. You may need:
- Latest compiler version
- Explicit flag: `-std=c++20` or `/std:c++latest`
- Online compilers (Compiler Explorer) for testing feature availability

## Gotchas

- **Views do not own data.** If the underlying container is destroyed or modified, the view becomes dangling. Never store views that outlive their source.
- **Debugger support is poor.** Most debuggers (as of 2024) cannot display view contents well. Use a loop-to-string approach to inspect values during debugging.
- **Not all view combinations compile.** Some view pipelines require the underlying range to satisfy specific concepts (e.g., `reverse` needs a bidirectional range). Error messages can be cryptic.
- **`nth_element` is NOT partial sort.** It partitions correctly but does not sort the "winners" - use it when you need top-N without caring about their order (faster than `partial_sort`).

## Cross-References

- [[stl-algorithms]] - traditional algorithm patterns
- [[stl-containers]] - container types that work with ranges
- [[lambda-expressions]] - writing predicates for filter/transform
- [[performance-optimization]] - lazy evaluation benefits
