# Function Pointers and Callbacks in C++

Functions in C++ have addresses in memory. A function pointer holds the address of a function and can invoke it indirectly. Modern C++ provides `std::function` and lambdas as safer, more flexible alternatives.

## Legacy C-Style Function Pointers

Every function is stored in memory. The function name without parentheses evaluates to its address:

```cpp
int sum(int a, int b) { return a + b; }

// Print function address
std::cout << reinterpret_cast<void*>(sum);  // some hex address

// Declare function pointer (C-style syntax)
int (*func_ptr)(int, int) = sum;

// Call through pointer
int result = func_ptr(3, 4);          // result = 7
int result2 = (*func_ptr)(3, 4);      // equivalent, explicit dereference
```

The syntax `int (*name)(int, int)` reads as: `name` is a pointer to a function taking two ints and returning int.

## auto for Simpler Syntax

```cpp
auto* func_ptr = sum;   // compiler deduces the type
func_ptr(3, 4);         // works identically
```

## Functions as Parameters

The real power: passing behavior as an argument.

```cpp
// Legacy: function pointer parameter
int calculate(int* arr, int size, int (*operation)(int, int)) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = operation(result, arr[i]);
    }
    return result;
}

int sum(int a, int b) { return a + b; }
int product(int a, int b) { return a * b; }

int arr[] = {1, 2, 3, 4, 5};
calculate(arr, 5, sum);      // 15
calculate(arr, 5, product);  // 120
```

## Lambdas as Inline Functions

Instead of defining named functions for single-use callbacks, use lambdas:

```cpp
// Lambda: anonymous function
calculate(arr, 5, [](int a, int b) { return a + b; });
calculate(arr, 5, [](int a, int b) { return a * b; });
```

Lambdas that capture nothing (empty `[]`) can implicitly convert to C-style function pointers.

## std::function (Modern C++)

`std::function` from `<functional>` is a general-purpose, type-erased function wrapper. It works with function pointers, lambdas (even capturing ones), and function objects.

```cpp
#include <functional>

// Accepts any callable with matching signature
int calculate(int* arr, int size, const std::function<int(int, int)>& op) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = op(result, arr[i]);
    }
    return result;
}

// Works with capturing lambda (function pointer cannot do this)
int offset = 10;
calculate(arr, 5, [offset](int a, int b) { return a + b + offset; });
```

## When to Use Which

| Mechanism | Overhead | Captures | Type Erasure |
|-----------|----------|----------|-------------|
| C function pointer | Zero | No | No |
| `auto` + lambda | Zero (inlined) | Yes | No |
| `std::function` | Small (heap possible) | Yes | Yes |
| Template parameter | Zero (compile-time) | Yes | No |

**Default choice**: `std::function` for API boundaries, templates for internal/performance-critical code. Raw function pointers only for C interop.

```cpp
// Best for library APIs: flexible, clear interface
void register_callback(std::function<void(int)> cb);

// Best for hot paths: zero overhead, inlined
template <typename F>
void hot_loop(F&& callback) { /* ... */ }
```

## Gotchas

- **Lambdas with captures cannot convert to raw function pointers.** Only capture-less lambdas (`[]`) are convertible. Use `std::function` for capturing lambdas.
- **`std::function` has overhead.** It may heap-allocate for large captures and uses virtual dispatch internally. For performance-critical code in tight loops, prefer template parameters.
- **Pass `std::function` by `const&`**, not by value, to avoid unnecessary copies of the internal callable.
- **Calling a null `std::function` throws `std::bad_function_call`.** Always check `if (func)` before calling if the function might be empty.

## Cross-References

- [[lambda-expressions]] - lambda syntax, captures, generic lambdas
- [[templates-and-concepts]] - using templates for zero-cost callbacks
- [[design-patterns-cpp]] - Strategy pattern uses function objects extensively
- [[stl-algorithms]] - algorithms accept callables as parameters
