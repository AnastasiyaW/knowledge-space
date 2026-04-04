---
title: Move Semantics and Perfect Forwarding
category: concepts
tags: [cpp, move, rvalue, forwarding, cpp11, performance]
---

# Move Semantics and Perfect Forwarding

Transfer resources instead of copying them. Rvalue references (`T&&`) enable move constructors and move assignment, eliminating unnecessary deep copies.

## Key Facts

- lvalue = has identity, can take address of; rvalue = temporary, about to be destroyed
- `T&&` is an rvalue reference - binds to temporaries
- `std::move(x)` is just a cast to `T&&` - it does NOT move anything, only enables moving
- After `std::move`, the source is in a valid-but-unspecified state - don't read from it
- Move constructor: `Widget(Widget&& other) noexcept`
- Move assignment: `Widget& operator=(Widget&& other) noexcept`
- Mark move operations `noexcept` - STL containers use `std::move_if_noexcept` for strong exception guarantee
- Rule of Five: if you define any of destructor/copy ctor/copy assign/move ctor/move assign, define all five
- Rule of Zero: prefer classes that need none of the five (use smart pointers and standard containers)
- `std::forward<T>(arg)` preserves value category in template code - the basis of perfect forwarding
- Compiler generates moves implicitly if no user-declared copy ops, move ops, or destructor

## Patterns

### Move Constructor and Assignment

```cpp
class Buffer {
    size_t size_;
    int* data_;
public:
    // Move constructor - steal resources
    Buffer(Buffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;  // leave source in valid state
    }

    // Move assignment - release own, steal other's
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    // Copy-and-swap idiom handles both copy and move assignment
    // Buffer& operator=(Buffer other) { swap(*this, other); return *this; }
};
```

### Perfect Forwarding

```cpp
// Forward arguments preserving value category
template<typename T, typename... Args>
std::unique_ptr<T> make_unique_wrapper(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

// Forwarding reference (T&& where T is deduced)
template<typename T>
void wrapper(T&& arg) {
    // If called with lvalue: T = Widget&, arg is Widget&
    // If called with rvalue: T = Widget, arg is Widget&&
    target(std::forward<T>(arg));
}
```

### Return Value Optimization (RVO/NRVO)

```cpp
// Compiler elides copy/move entirely (mandatory in C++17)
Widget create() {
    Widget w(42);
    return w;  // NRVO: constructed directly in caller's space
}

// DON'T std::move the return value - it prevents NRVO
Widget bad_create() {
    Widget w(42);
    return std::move(w);  // WRONG: prevents NRVO
}
```

### Sink Parameters

```cpp
class Registry {
    std::vector<std::string> names_;
public:
    // By value + move: one interface for both lvalue and rvalue
    void add(std::string name) {
        names_.push_back(std::move(name));
    }
    // Called with lvalue: copy into param + move into vector
    // Called with rvalue: move into param + move into vector
};
```

## Gotchas

- **Issue:** Using object after `std::move` leads to reading moved-from state -> **Fix:** Only assign to or destroy moved-from objects, never read their value
- **Issue:** Move constructor without `noexcept` - `std::vector` reallocation falls back to copying -> **Fix:** Always mark move operations `noexcept` if they cannot throw
- **Issue:** `std::move` on `const` object silently calls copy constructor -> **Fix:** Never move from `const` objects - the const prevents the move
- **Issue:** `return std::move(local)` defeats NRVO -> **Fix:** Just `return local;` - compiler applies NRVO or implicit move
- **Issue:** Forwarding reference `T&&` confused with rvalue reference -> **Fix:** `T&&` is forwarding only when `T` is deduced template parameter. `Widget&&` is always rvalue reference.

## See Also

- [[smart-pointers]]
- [[raii-resource-management]]
- [[templates-and-concepts]]
- [cppreference: move](https://en.cppreference.com/w/cpp/utility/move)
