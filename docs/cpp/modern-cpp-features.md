---
title: Modern C++ Features (C++17/20/23)
category: concepts
tags: [cpp, cpp17, cpp20, cpp23, structured-bindings, optional, variant, ranges, modules, coroutines]
---

# Modern C++ Features (C++17/20/23)

Key features from recent standards that change how C++ is written. Focus on the most impactful additions.

## Key Facts - C++17

- Structured bindings: `auto [key, value] = pair;`
- `std::optional<T>`, `std::variant<Ts...>`, `std::any`
- `if constexpr` - compile-time branching in templates
- Class Template Argument Deduction (CTAD): `std::vector v{1,2,3};`
- `std::string_view` - non-owning string reference
- `<filesystem>` - portable filesystem operations
- Fold expressions: `(args + ...)`
- Nested namespaces: `namespace A::B::C {}`
- `[[nodiscard]]`, `[[maybe_unused]]`, `[[fallthrough]]` attributes
- `std::invoke` - uniform callable invocation

## Key Facts - C++20

- Concepts and constraints
- Ranges and views (`<ranges>`)
- Coroutines (`co_await`, `co_yield`, `co_return`)
- Modules (`import`, `export module`)
- `std::format` - type-safe formatting
- `<=>` spaceship operator
- `std::span<T>` - non-owning contiguous view
- `std::jthread` - auto-joining thread with stop token
- `consteval`, `constinit`
- `requires` expressions and clauses

## Key Facts - C++23

- `std::expected<T,E>` - value-or-error
- `std::print` / `std::println` - formatted output
- `std::mdspan` - multidimensional array view
- Deducing `this` - explicit object parameter
- `std::generator` - synchronous coroutine generator
- `if consteval` - check if in constant evaluation
- `std::flat_map` / `std::flat_set` - sorted vector-based containers
- `std::stacktrace` - programmatic stack traces

## Patterns

### Structured Bindings (C++17)

```cpp
// With pairs/tuples
auto [min_it, max_it] = std::minmax_element(v.begin(), v.end());

// With maps
std::map<std::string, int> scores;
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << '\n';
}

// With custom structs (public members or structured binding support)
struct Result { bool ok; std::string message; };
auto [ok, msg] = get_result();
if (ok) process(msg);

// With arrays
int arr[] = {1, 2, 3};
auto [a, b, c] = arr;
```

### std::variant and std::visit (C++17)

```cpp
using Value = std::variant<int, double, std::string>;

Value v = 42;
v = "hello"s;

// Visit with overloaded lambdas
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

auto result = std::visit(overloaded{
    [](int i)              { return std::to_string(i); },
    [](double d)           { return std::to_string(d); },
    [](const std::string& s) { return s; }
}, v);

// Check which type is active
if (std::holds_alternative<int>(v)) {
    int i = std::get<int>(v);
}

// Safe get
if (auto* p = std::get_if<std::string>(&v)) {
    process(*p);
}
```

### Ranges and Views (C++20)

```cpp
#include <ranges>
namespace rv = std::views;

std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Pipeline
auto evens_squared = nums
    | rv::filter([](int n) { return n % 2 == 0; })
    | rv::transform([](int n) { return n * n; });

// Lazy evaluation - nothing computed until iterated
for (int n : evens_squared) { std::cout << n << ' '; }  // 4 16 36 64 100

// Range factories
for (int i : rv::iota(1, 11)) { /* 1..10 */ }
for (int i : rv::iota(0) | rv::take(5)) { /* 0..4 */ }

// String processing
std::string csv = "a,b,c,d";
for (auto word : csv | rv::split(',')) {
    // process each word
}
```

### std::span (C++20)

```cpp
#include <span>

// Non-owning view of contiguous data - replaces (T*, size_t) pairs
void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
    auto first3 = data.subspan(0, 3);
    auto last2 = data.last(2);
}

// Works with any contiguous container
std::vector<int> vec = {1, 2, 3};
std::array<int, 5> arr = {1, 2, 3, 4, 5};
int c_arr[] = {1, 2, 3, 4};

process(vec);
process(arr);
process(c_arr);
process({vec.data() + 1, 3});  // subview
```

### Deducing this (C++23)

```cpp
struct Widget {
    // Single implementation for const and non-const
    template<typename Self>
    auto&& value(this Self&& self) {
        return std::forward<Self>(self).value_;
    }

    // Recursive lambda (see also lambda-expressions)
    auto get_children(this const Widget& self) -> std::vector<Widget> {
        // can recurse: self.get_children()
    }

private:
    int value_;
};
```

### Modules (C++20)

```cpp
// mylib.cppm (module interface)
export module mylib;

export class Widget {
public:
    Widget(int val);
    int value() const;
private:
    int val_;
};

export int compute(int x);

// mylib.cpp (module implementation)
module mylib;

Widget::Widget(int val) : val_(val) {}
int Widget::value() const { return val_; }
int compute(int x) { return x * x; }

// main.cpp
import mylib;

int main() {
    Widget w(42);
    return compute(w.value());
}
```

## Gotchas

- **Issue:** `std::variant` default-constructs first alternative - fails if first type has no default ctor -> **Fix:** Put a default-constructible type first, or use `std::monostate` as first type
- **Issue:** Ranges views hold references to source - dangling if source is temporary -> **Fix:** Materialize views to containers before source destruction. Don't return views to local data.
- **Issue:** Modules support varies across compilers (partial in GCC/Clang as of 2025) -> **Fix:** Check compiler support matrix. Use headers as fallback with `#include` wrapper.
- **Issue:** `std::span` doesn't own data - same dangling risks as pointers -> **Fix:** Ensure source outlives the span. Never return span to local container.

## See Also

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[lambda-expressions]]
- [[error-handling]]
- [[string-handling]]
