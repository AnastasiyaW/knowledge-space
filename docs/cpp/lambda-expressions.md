---
title: Lambda Expressions
category: concepts
tags: [cpp, lambda, closures, functional, cpp11, cpp14, cpp20]
---

# Lambda Expressions

Anonymous function objects with capture semantics. Core tool for callbacks, algorithms, and functional patterns.

## Key Facts

- Syntax: `[capture](params) -> return_type { body }`
- `[=]` captures all locals by value, `[&]` captures all by reference
- `[x]` capture by value, `[&x]` capture by reference, `[x = std::move(y)]` init capture (C++14)
- Lambdas are syntactic sugar for compiler-generated closure types (unnamed `struct` with `operator()`)
- Each lambda has a unique type - use `std::function<>` or `auto` to store
- `auto` lambda parameters (C++14) make generic/polymorphic lambdas
- `mutable` keyword allows modifying captured-by-value variables
- `constexpr` lambdas (C++17) - usable in compile-time contexts
- Template lambdas (C++20): `[]<typename T>(T x) { ... }`
- Lambdas with no capture can convert to function pointer
- Prefer lambda over `std::bind` - clearer, more efficient, better optimized

## Patterns

### Capture Modes

```cpp
int x = 10;
std::string name = "test";

auto by_val   = [x]() { return x; };            // copy of x
auto by_ref   = [&x]() { return x; };           // reference to x
auto all_val  = [=]() { return x + name.size(); }; // all by value
auto all_ref  = [&]() { x++; };                 // all by reference
auto mixed    = [&x, name]() { x += name.size(); }; // mix

// Init capture (C++14) - move into lambda
auto moved = [s = std::move(name)]() { return s.size(); };

// Capture this
struct Widget {
    int value_ = 42;
    auto get_printer() {
        return [this]() { std::cout << value_; };     // captures this ptr
        // return [*this]() { std::cout << value_; };  // C++17: copies *this
    }
};
```

### Generic Lambdas

```cpp
// C++14: auto parameters
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);       // int
add(1.5, 2.5);   // double
add("a"s, "b"s); // string

// C++20: template syntax for constraints
auto print = []<typename T>(const std::vector<T>& v) {
    for (const auto& x : v) std::cout << x << ' ';
};
```

### With STL Algorithms

```cpp
std::vector<int> v = {5, 3, 1, 4, 2};

// Sort with custom comparator
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// Find first matching
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x > 3; });

// Transform
std::vector<std::string> result;
std::transform(v.begin(), v.end(), std::back_inserter(result),
    [](int x) { return std::to_string(x); });

// Accumulate with lambda
auto product = std::accumulate(v.begin(), v.end(), 1,
    [](int acc, int x) { return acc * x; });
```

### Immediately Invoked Lambda (IIFE)

```cpp
// Complex initialization
const auto config = [&] {
    Config c;
    c.width = parse_int(args[1]);
    c.height = parse_int(args[2]);
    c.title = args[3];
    return c;
}();  // note: immediately invoked

// Conditional const initialization
const int value = [&] {
    if (mode == Mode::Fast) return compute_fast();
    else return compute_accurate();
}();
```

### Recursive Lambda

```cpp
// C++23: deducing this for recursion
auto fib = [](this auto self, int n) -> int {
    if (n <= 1) return n;
    return self(n-1) + self(n-2);
};

// Pre-C++23: use std::function
std::function<int(int)> fib = [&fib](int n) -> int {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
};
```

## Gotchas

- **Issue:** Capturing local by reference, lambda outlives the local -> dangling reference, UB -> **Fix:** Capture by value, or use init capture to move ownership into lambda
- **Issue:** `[=]` captures `this` pointer by value (the pointer, not the object) -> still dangling if object destroyed -> **Fix:** Use `[*this]` (C++17) to capture object copy, or ensure lifetime
- **Issue:** `std::function<>` has overhead (type erasure, heap allocation) -> **Fix:** Use `auto` when possible; `std::function` only when type-erased storage is needed
- **Issue:** Lambda modifying captured-by-value variable won't compile -> **Fix:** Add `mutable`: `[x]() mutable { x++; }`

## See Also

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference: Lambda](https://en.cppreference.com/w/cpp/language/lambda)
