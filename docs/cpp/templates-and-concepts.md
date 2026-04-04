---
title: Templates and Concepts
category: concepts
tags: [cpp, templates, concepts, generic, metaprogramming, cpp20]
---

# Templates and Concepts

Generic programming through compile-time type parameterization. Concepts (C++20) constrain templates with readable requirements.

## Key Facts

- Function templates: compiler generates code for each used type instantiation
- Class templates: parameterize entire classes on types/values
- Template instantiation happens at compile time - no runtime overhead
- SFINAE (Substitution Failure Is Not An Error) - failed substitution removes overload from candidate set
- `if constexpr` (C++17) - compile-time branch elimination inside templates
- Concepts (C++20) - named requirements that constrain template parameters
- `auto` in function parameters (C++20) - abbreviated function templates
- Variadic templates: `template<typename... Args>` - parameter packs with arbitrary count
- Non-type template parameters: `template<int N>` - compile-time constants
- Template specialization: provide specific implementation for particular types
- Two-phase lookup: names checked at definition and instantiation time

## Patterns

### Function Templates

```cpp
template<typename T>
T max_val(T a, T b) {
    return (a > b) ? a : b;
}

// Explicit instantiation
int m1 = max_val<int>(3, 7);

// Implicit deduction
double m2 = max_val(3.14, 2.71);

// Multiple type parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// C++20: auto parameters = abbreviated template
auto add_modern(auto a, auto b) {
    return a + b;
}
```

### Class Templates

```cpp
template<typename T, size_t N>
class StaticArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    const T& operator[](size_t i) const { return data_[i]; }
    constexpr size_t size() const { return N; }

    auto begin() { return std::begin(data_); }
    auto end() { return std::end(data_); }
};

StaticArray<int, 10> arr;
arr[0] = 42;
```

### Concepts (C++20)

```cpp
// Define a concept
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<typename T>
concept Sortable = requires(T t) {
    { t.begin() } -> std::input_iterator;
    { t.end() } -> std::input_iterator;
    { t.size() } -> std::convertible_to<size_t>;
};

template<typename T>
concept Printable = requires(std::ostream& os, T val) {
    { os << val } -> std::same_as<std::ostream&>;
};

// Use concepts - four equivalent syntaxes
template<Numeric T>
T square(T x) { return x * x; }

auto square2(Numeric auto x) { return x * x; }

template<typename T> requires Numeric<T>
T square3(T x) { return x * x; }

template<typename T>
T square4(T x) requires Numeric<T> { return x * x; }
```

### Variadic Templates

```cpp
// Base case
void print() {}

// Recursive case
template<typename T, typename... Rest>
void print(T first, Rest... rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) {
        std::cout << ", ";
        print(rest...);
    }
}

// C++17 fold expressions
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // unary right fold
}

template<typename... Args>
void print_all(Args&&... args) {
    ((std::cout << args << ' '), ...);  // comma fold
}
```

### Template Specialization

```cpp
// Primary template
template<typename T>
struct Serializer {
    static std::string serialize(const T& val) {
        return std::to_string(val);
    }
};

// Full specialization for std::string
template<>
struct Serializer<std::string> {
    static std::string serialize(const std::string& val) {
        return '"' + val + '"';
    }
};

// Partial specialization for pointers
template<typename T>
struct Serializer<T*> {
    static std::string serialize(T* val) {
        return val ? Serializer<T>::serialize(*val) : "null";
    }
};
```

### if constexpr (C++17)

```cpp
template<typename T>
auto process(T val) {
    if constexpr (std::is_integral_v<T>) {
        return val * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return val * 2.0;
    } else if constexpr (std::is_same_v<T, std::string>) {
        return val + val;
    } else {
        static_assert(false, "Unsupported type");  // C++23
    }
}
```

## Gotchas

- **Issue:** Template definitions in `.cpp` files cause linker errors -> **Fix:** Templates must be in header files (or use explicit instantiation in `.cpp`)
- **Issue:** Dependent names need `typename` keyword in templates -> **Fix:** `typename Container::value_type` not `Container::value_type` inside template
- **Issue:** SFINAE errors produce unreadable error messages -> **Fix:** Use Concepts (C++20) for clear constraint violation messages
- **Issue:** Template code bloat - each instantiation generates separate machine code -> **Fix:** Factor type-independent code into non-template base, use thin template wrappers
- **Issue:** Two-phase lookup: unqualified names not found in dependent base -> **Fix:** Use `this->member` or `Base<T>::member` to access base class members

## See Also

- [[stl-containers]]
- [[stl-algorithms]]
- [[lambda-expressions]]
- [cppreference: Concepts](https://en.cppreference.com/w/cpp/language/constraints)
