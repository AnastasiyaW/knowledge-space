# C++20 Concepts and Constraints

Concepts are named sets of requirements on template parameters. They replace SFINAE and `enable_if` hacks with readable, compiler-enforced constraints that produce clear error messages.

## The Problem Concepts Solve

Before C++20, template errors were notoriously bad. If you passed an incompatible type to a template, the compiler would produce pages of errors deep inside the template implementation. The user had no way to know what the template actually required without reading the implementation.

Concepts move requirements from "implicit in the implementation" to "explicit in the declaration."

## Using Standard Concepts

The `<concepts>` header provides standard concepts:

```cpp
#include <concepts>

// Constrained function template: T must be integral
template <std::integral T>
T double_it(T value) {
    return value * 2;
}

double_it(42);      // OK: int is integral
double_it(3.14);    // Compile error: double is not integral
// Error message: "constraints not satisfied" - clear and short
```

Common standard concepts:

| Concept | Meaning |
|---------|---------|
| `std::integral` | Integer types (int, long, char, etc.) |
| `std::floating_point` | float, double, long double |
| `std::signed_integral` | Signed integer types |
| `std::unsigned_integral` | Unsigned integer types |
| `std::same_as<T, U>` | T and U are the same type |
| `std::convertible_to<From, To>` | From implicitly converts to To |
| `std::derived_from<Derived, Base>` | Inheritance relationship |
| `std::equality_comparable` | Supports == and != |
| `std::totally_ordered` | Supports <, >, <=, >= |
| `std::movable` | Move constructible and assignable |
| `std::copyable` | Copy constructible and assignable |

## Syntax Forms

Three equivalent ways to constrain a template:

```cpp
// 1. Requires clause
template <typename T>
    requires std::integral<T>
T add(T a, T b) { return a + b; }

// 2. Constrained template parameter
template <std::integral T>
T add(T a, T b) { return a + b; }

// 3. Trailing requires clause
template <typename T>
T add(T a, T b) requires std::integral<T> { return a + b; }
```

## Writing Custom Concepts

Custom concepts combine existing concepts and ad-hoc requirements:

```cpp
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
concept Printable = requires(T t) {
    { std::cout << t } -> std::same_as<std::ostream&>;
};

template <typename T>
concept Hashable = requires(T t) {
    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;
};

// Combine multiple concepts
template <typename T>
concept PrintableNumeric = Numeric<T> && Printable<T>;
```

## Benefits for Template Users

With concepts, looking at a template declaration tells you everything:

```cpp
template <std::totally_ordered T>
T find_max(std::vector<T>& v);
// Reading this, you know: T must support comparison operators
// Look up std::totally_ordered on cppreference for details
```

Without concepts (pre-C++20):
```cpp
template <typename T>
T find_max(std::vector<T>& v);
// What does T need to support? Must read implementation to find out.
```

## Benefits for Template Writers

- IDE autocomplete knows which operations are available based on the concept
- Accidental use of operations not in the concept is caught at definition time, not instantiation time
- Overload resolution can use concepts to select the most appropriate overload

## Adoption Strategy

1. Start by **using** existing standard concepts to constrain your templates
2. Then try **combining** existing concepts with `&&` and `||`
3. Only **write custom concepts** when standard ones do not cover your needs
4. Writing a custom concept should never be step one

## Gotchas

- **Concepts do not restrict the implementation.** A concept says "T must support X" but the template body can still use operations beyond what the concept requires. The concept constrains what types can be passed in, not what the template does with them.
- **Concept subsumption rules are subtle.** When two overloads have different concepts, the compiler picks the "most constrained" one. The rules for which concept is "more specific" can be non-obvious.
- **Standard concepts are in different headers.** Not all concepts live in `<concepts>` - some are in `<ranges>`, `<iterator>`, `<functional>`. Check cppreference for the right include.
- **Compiler support varies.** Older compilers or certain flags may not support all C++20 concepts. Test with your target compiler.

## Cross-References

- [[templates-and-concepts]] - generic programming foundations
- [[modern-cpp-features]] - other C++20 features
- [[error-handling]] - concepts improve template error diagnostics
