---
title: Error Handling - Exceptions and Alternatives
category: concepts
tags: [cpp, exceptions, error-handling, optional, expected, noexcept]
---

# Error Handling - Exceptions and Alternatives

C++ supports exceptions, error codes, `std::optional`, and `std::expected` (C++23). Choose the right mechanism for the context.

## Key Facts

- Exceptions: for exceptional/unexpected errors. Zero-cost when not thrown (table-based unwinding)
- `noexcept` specifier: function promises not to throw. Enables optimizations (move in vector)
- Error codes: for expected failures (file not found, invalid input). No overhead, explicit control flow
- `std::optional<T>` (C++17): value-or-nothing. For functions that may not produce a result
- `std::expected<T,E>` (C++23): value-or-error. Type-safe alternative to exceptions
- Standard exception hierarchy: `std::exception` -> `runtime_error`, `logic_error`, etc.
- Catch by `const` reference: `catch (const std::exception& e)`
- Stack unwinding on exception: all local RAII objects destructed (see [[raii-resource-management]])
- `throw;` re-throws current exception (preserving type). `throw e;` slices to `std::exception`
- Never throw from destructor (terminates during stack unwinding)
- Exception specifications removed in C++17 except `noexcept`

## Patterns

### Exception Handling

```cpp
#include <stdexcept>

// Throwing
void parse(const std::string& input) {
    if (input.empty())
        throw std::invalid_argument("Input cannot be empty");
    if (input.size() > 1024)
        throw std::length_error("Input too long");
    // parse...
}

// Catching
try {
    parse(user_input);
} catch (const std::invalid_argument& e) {
    std::cerr << "Invalid: " << e.what() << '\n';
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << '\n';
} catch (...) {
    std::cerr << "Unknown error\n";
    throw;  // re-throw
}
```

### Custom Exceptions

```cpp
class AppError : public std::runtime_error {
    int code_;
public:
    AppError(int code, const std::string& msg)
        : std::runtime_error(msg), code_(code) {}
    int code() const { return code_; }
};

class NetworkError : public AppError {
public:
    NetworkError(const std::string& msg)
        : AppError(1001, msg) {}
};

// Usage
throw NetworkError("Connection refused");
```

### std::optional (C++17)

```cpp
#include <optional>

std::optional<int> find_index(const std::vector<int>& v, int target) {
    for (size_t i = 0; i < v.size(); ++i) {
        if (v[i] == target) return static_cast<int>(i);
    }
    return std::nullopt;
}

// Usage
if (auto idx = find_index(vec, 42)) {
    std::cout << "Found at index " << *idx << '\n';
} else {
    std::cout << "Not found\n";
}

// Value-or-default
int idx = find_index(vec, 42).value_or(-1);
```

### std::expected (C++23)

```cpp
#include <expected>

enum class ParseError { empty_input, invalid_format, overflow };

std::expected<int, ParseError> parse_int(std::string_view sv) {
    if (sv.empty())
        return std::unexpected(ParseError::empty_input);
    // parse logic...
    return 42;
}

// Usage
auto result = parse_int("123");
if (result) {
    use(*result);
} else {
    handle_error(result.error());
}

// Monadic operations (C++23)
auto final_result = parse_int(input)
    .transform([](int x) { return x * 2; })
    .or_else([](ParseError e) -> std::expected<int, ParseError> {
        log_error(e);
        return 0;  // default value
    });
```

### Multiple Exception Handling

Order matters: catch derived types before base types. Most specific first:

```cpp
try {
    open_file(path);
    parse_data(content);
    write_results(output_path);
} catch (const std::ios_base::failure& e) {
    // File I/O specific errors
    std::cerr << "I/O error: " << e.what() << '\n';
} catch (const std::invalid_argument& e) {
    // Parse errors
    std::cerr << "Invalid data: " << e.what() << '\n';
} catch (const std::runtime_error& e) {
    // Generic runtime errors
    std::cerr << "Runtime error: " << e.what() << '\n';
} catch (const std::exception& e) {
    // Catch-all for standard exceptions
    std::cerr << "Error: " << e.what() << '\n';
} catch (...) {
    // Non-standard exceptions (rare, e.g. from C libraries)
    std::cerr << "Unknown error\n";
    throw;  // re-throw - don't swallow unknown exceptions
}
```

**Practical pattern**: wrap main logic in try, handle specific recoverable errors, let unrecoverable ones propagate:

```cpp
int main() {
    try {
        run_application();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Fatal: " << e.what() << '\n';
        return 1;
    } catch (...) {
        std::cerr << "Unknown fatal error\n";
        return 2;
    }
}
```

### noexcept

```cpp
// Mark functions that won't throw
void swap(Widget& a, Widget& b) noexcept {
    std::swap(a.data_, b.data_);
}

// Conditional noexcept
template<typename T>
void safe_swap(T& a, T& b) noexcept(noexcept(std::swap(a, b))) {
    std::swap(a, b);
}

// Move operations MUST be noexcept for vector optimization
Widget(Widget&& other) noexcept;
Widget& operator=(Widget&& other) noexcept;
```

## Gotchas

- **Issue:** Catching exception by value slices derived type -> **Fix:** Always catch by `const` reference: `catch (const std::exception& e)`
- **Issue:** `throw e;` inside catch re-throws sliced copy -> **Fix:** Use `throw;` to re-throw preserving original type
- **Issue:** Exception in destructor during stack unwinding -> `std::terminate` -> **Fix:** Never throw from destructors. Catch and log inside destructor.
- **Issue:** `optional.value()` throws `bad_optional_access` if empty -> **Fix:** Check with `has_value()` / `if (opt)` or use `value_or(default)`
- **Issue:** Missing `noexcept` on move constructor makes vector copy instead of move during reallocation -> **Fix:** Always mark move ops `noexcept`

## See Also

- [[raii-resource-management]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference: Exceptions](https://en.cppreference.com/w/cpp/error/exception)
