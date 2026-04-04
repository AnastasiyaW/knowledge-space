---
title: STL Algorithms and Ranges
category: concepts
tags: [cpp, stl, algorithms, ranges, sort, transform, cpp20]
---

# STL Algorithms and Ranges

`<algorithm>` provides 100+ generic algorithms that work with iterators. C++20 Ranges add composable, lazy pipeline syntax.

## Key Facts

- Algorithms operate on iterator pairs `[begin, end)` - half-open range
- Non-modifying: `find`, `count`, `all_of`, `any_of`, `none_of`, `for_each`, `accumulate`
- Modifying: `transform`, `copy`, `fill`, `replace`, `remove`, `reverse`, `rotate`
- Sorting: `sort`, `stable_sort`, `partial_sort`, `nth_element`
- Searching: `binary_search`, `lower_bound`, `upper_bound`, `equal_range`
- `std::sort` is introsort (quicksort + heapsort + insertion sort) - O(n log n) guaranteed
- `std::stable_sort` preserves relative order of equal elements
- `remove` / `remove_if` don't actually erase - they shift elements, return new end
- C++17: parallel execution policies - `std::execution::par`, `seq`, `par_unseq`
- C++20: Ranges (`<ranges>`) - algorithms take containers directly, views compose lazily
- `std::ranges::sort(vec)` instead of `std::sort(vec.begin(), vec.end())`

## Patterns

### Common Algorithms

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

### Erase-Remove Idiom

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

### C++20 Ranges

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

### Parallel Algorithms (C++17)

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

### Binary Search (on sorted data)

```cpp
std::vector<int> v = {1, 3, 5, 7, 9, 11};

bool found = std::binary_search(v.begin(), v.end(), 5);       // true
auto lb = std::lower_bound(v.begin(), v.end(), 5);            // -> 5
auto ub = std::upper_bound(v.begin(), v.end(), 5);            // -> 7
auto [lo, hi] = std::equal_range(v.begin(), v.end(), 5);      // range of 5s
```

## Gotchas

- **Issue:** `remove` doesn't change container size - it only moves elements -> **Fix:** Always pair with `erase` (erase-remove idiom) or use C++20 `std::erase`/`std::erase_if`
- **Issue:** Using `sort` on `list` is O(n log n) extra space due to random access iterators -> **Fix:** Use `list::sort()` member function which is O(n log n) with O(1) space
- **Issue:** Ranges views are lazy - they don't execute until iterated. Dangling references if source destroyed -> **Fix:** Materialize views before source goes out of scope
- **Issue:** Parallel algorithms require elements to be independently processable - data races on shared state -> **Fix:** Use `std::atomic` or redesign to avoid shared mutable state

## See Also

- [[stl-containers]]
- [[lambda-expressions]]
- [[templates-and-concepts]]
- [cppreference: Algorithms](https://en.cppreference.com/w/cpp/algorithm)
