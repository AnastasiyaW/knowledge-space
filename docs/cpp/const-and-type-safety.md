---
title: Const Correctness and Type Safety
category: concepts
tags: [cpp, const, constexpr, type-safety, auto, casting]
---

# Const Correctness and Type Safety

`const` communicates intent, prevents accidental mutation, and enables compiler optimizations. Modern C++ type safety eliminates entire bug categories.

## Key Facts

- `const int* p` = pointer to const int (can't modify through p, can reassign p)
- `int* const p` = const pointer to int (can modify through p, can't reassign p)
- `const int* const p` = const pointer to const int
- Read declarations right-to-left: `int const* p` = "p is a pointer to const int"
- `const` member function: `void foo() const` - promises not to modify object state
- `mutable` member: can be modified even in const context (caches, mutexes)
- `constexpr` (C++11): evaluated at compile time if possible; `consteval` (C++20): must be compile-time
- `auto` deduces type from initializer - drops top-level `const` and references
- `decltype(expr)` deduces type preserving qualifiers
- C++ casts: `static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`
- `static_cast` for safe conversions; `dynamic_cast` for runtime-checked downcast
- `const_cast` to remove const - only safe if original object was not const
- `std::string_view` (C++17): non-owning view, replaces `const std::string&` parameters

## Patterns

### const Correctness

```cpp
class Matrix {
    std::vector<double> data_;
    size_t rows_, cols_;
public:
    // const accessor - can call on const Matrix
    double at(size_t r, size_t c) const {
        return data_[r * cols_ + c];
    }

    // non-const accessor - modifiable
    double& at(size_t r, size_t c) {
        return data_[r * cols_ + c];
    }

    // const-qualified getters
    size_t rows() const { return rows_; }
    size_t cols() const { return cols_; }

    // mutable for caching
    mutable std::optional<double> cached_det_;
    double determinant() const {
        if (!cached_det_) {
            cached_det_ = compute_determinant();
        }
        return *cached_det_;
    }
};

// Function parameter const correctness
void process(const Matrix& m);       // won't modify m
void transform(Matrix& m);           // may modify m
void consume(Matrix m);              // takes copy
```

### constexpr

```cpp
// Compile-time function
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

constexpr int f5 = factorial(5);  // computed at compile time
static_assert(f5 == 120);

// constexpr class
class Point {
    double x_, y_;
public:
    constexpr Point(double x, double y) : x_(x), y_(y) {}
    constexpr double distance_sq(Point other) const {
        double dx = x_ - other.x_;
        double dy = y_ - other.y_;
        return dx*dx + dy*dy;
    }
};

constexpr Point p1(0, 0), p2(3, 4);
constexpr double d = p1.distance_sq(p2);  // 25.0 at compile time

// C++20: consteval - MUST be compile-time
consteval int must_be_compiletime(int x) { return x * x; }

// C++20: constinit - compile-time initialization, runtime mutability
constinit int global = factorial(5);  // init at compile time
```

### auto and decltype

```cpp
// auto deduction
auto x = 42;                  // int
auto& r = x;                  // int&
const auto& cr = x;           // const int&
auto* p = &x;                 // int*

// auto with containers
std::map<std::string, std::vector<int>> data;
for (const auto& [key, values] : data) {   // structured bindings C++17
    for (auto val : values) { /* ... */ }
}

// decltype preserves qualifiers
int i = 0;
decltype(i) j = i;            // int
decltype((i)) k = i;          // int& (expression in parens = lvalue)

// Trailing return type
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}
```

### Safe Casting

```cpp
// static_cast: compile-time checked, common conversions
double d = 3.14;
int i = static_cast<int>(d);              // 3, explicit truncation
Base* bp = static_cast<Base*>(derived_ptr); // upcast (always safe)

// dynamic_cast: runtime-checked downcast (needs RTTI + virtual)
if (auto* dp = dynamic_cast<Derived*>(base_ptr)) {
    dp->derived_method();
}

// const_cast: remove const (danger zone)
void legacy_api(char* s);
const char* str = "hello";
legacy_api(const_cast<char*>(str));  // OK only if legacy_api doesn't write

// reinterpret_cast: type punning (last resort)
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
```

### string_view (C++17)

```cpp
// Efficient string parameter - no allocation
void process(std::string_view sv) {
    // sv.data(), sv.size(), sv.substr(), sv.find()
    // Supports string literals, std::string, char*, with/without length
}

process("hello");           // no allocation
process(std::string("hi")); // no copy
process(sv.substr(1, 3));   // no allocation (just pointer + length)
```

## Gotchas

- **Issue:** `auto` drops const and reference qualifiers -> **Fix:** Use `const auto&` when you want const reference
- **Issue:** `string_view` may dangle if underlying string destroyed -> **Fix:** Never store `string_view` longer than the source string lives. Don't return `string_view` to local.
- **Issue:** `const_cast` on truly const object then writing = UB -> **Fix:** Only use `const_cast` when you know the original object is non-const
- **Issue:** `constexpr` function not evaluated at compile time when args are runtime values -> **Fix:** Use `consteval` (C++20) if you need guaranteed compile-time evaluation

## See Also

- [[templates-and-concepts]]
- [[string-handling]]
- [[performance-optimization]]
- [cppreference: const](https://en.cppreference.com/w/cpp/language/cv)
