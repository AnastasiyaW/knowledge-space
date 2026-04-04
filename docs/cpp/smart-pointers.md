---
title: Smart Pointers and Memory Management
category: concepts
tags: [cpp, memory, raii, smart-pointers, cpp11, cpp14]
---

# Smart Pointers and Memory Management

Ownership-based memory management through `unique_ptr`, `shared_ptr`, and `weak_ptr`. Core mechanism for eliminating manual `new`/`delete` and preventing leaks.

## Key Facts

- Smart pointers live in `<memory>` header
- `std::unique_ptr` - sole ownership, zero overhead over raw pointer, non-copyable, movable
- `std::shared_ptr` - reference-counted shared ownership, thread-safe ref count, ~2x pointer size (control block)
- `std::weak_ptr` - non-owning observer of `shared_ptr`, breaks circular references
- Always prefer `std::make_unique` (C++14) and `std::make_shared` (C++11) over direct `new`
- `make_shared` allocates object + control block in single allocation (cache-friendly)
- `unique_ptr` can hold arrays: `std::unique_ptr<int[]> arr(new int[10]);`
- Custom deleters: `unique_ptr<FILE, decltype(&fclose)> f(fopen("x","r"), &fclose);`
- `shared_ptr` aliasing constructor allows pointing into sub-objects while sharing ownership of parent
- [[raii-resource-management]] is the foundation - smart pointers are RAII for heap memory

## Patterns

### unique_ptr - Default Choice

```cpp
// Creation - always use make_unique
auto widget = std::make_unique<Widget>(42, "hello");

// Transfer ownership
auto other = std::move(widget);  // widget is now nullptr

// Factory pattern - return unique_ptr
std::unique_ptr<Base> create(int type) {
    switch (type) {
        case 1: return std::make_unique<DerivedA>();
        case 2: return std::make_unique<DerivedB>();
        default: return nullptr;
    }
}

// Pass to sink (transfers ownership)
void consume(std::unique_ptr<Widget> w);

// Pass for use (no ownership transfer)
void use(Widget& w);           // preferred
void use(Widget* w);           // if nullable
```

### shared_ptr - Shared Ownership

```cpp
auto sp = std::make_shared<Widget>(42);
auto sp2 = sp;  // ref count = 2

// Get ref count (debugging only, not for logic)
std::cout << sp.use_count();  // 2

// Custom deleter
auto sp3 = std::shared_ptr<Widget>(new Widget(1),
    [](Widget* w) {
        log("deleting widget");
        delete w;
    });

// Aliasing constructor - share ownership of parent, point to member
struct Node { int value; };
auto node = std::make_shared<Node>();
std::shared_ptr<int> val(node, &node->value);
```

### weak_ptr - Breaking Cycles

```cpp
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;    // weak to break cycle
};

// Using weak_ptr
std::weak_ptr<Widget> wp = sp;
if (auto locked = wp.lock()) {  // returns shared_ptr or nullptr
    locked->doSomething();
}
// Or check without locking
if (!wp.expired()) { /* might still expire before use */ }
```

### unique_ptr with Custom Deleter

```cpp
// C-style resource management
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), &fclose);

// SDL example
auto window = std::unique_ptr<SDL_Window, decltype(&SDL_DestroyWindow)>(
    SDL_CreateWindow("App", 0, 0, 800, 600, 0),
    &SDL_DestroyWindow);

// Lambda deleter (note: changes unique_ptr size)
auto p = std::unique_ptr<int, std::function<void(int*)>>(
    new int(42),
    [](int* p) { std::cout << "deleting\n"; delete p; });
```

## Gotchas

- **Issue:** Passing `this` to `shared_ptr` creates separate control block, double-free on destruction -> **Fix:** Inherit from `std::enable_shared_from_this<T>`, use `shared_from_this()` method
- **Issue:** `make_shared` delays deallocation when `weak_ptr` exists - control block keeps memory alive even after all `shared_ptr` die -> **Fix:** For large objects with long-lived observers, use `shared_ptr(new T(...))` instead
- **Issue:** Circular `shared_ptr` references cause memory leaks (ref count never reaches 0) -> **Fix:** Use `weak_ptr` for back-references / parent pointers
- **Issue:** `shared_ptr<T>` to array before C++17 needs custom deleter -> **Fix:** Use `shared_ptr<T[]>` (C++17) or `unique_ptr<T[]>` or just `std::vector<T>`
- **Issue:** Constructing multiple `shared_ptr` from same raw pointer -> **Fix:** Never create two `shared_ptr` from same raw pointer. Use `make_shared` or pass existing `shared_ptr`
- **Issue:** Using `get()` and storing the raw pointer beyond smart pointer lifetime -> **Fix:** Only use `get()` for transient access, never store the result

## See Also

- [[raii-resource-management]]
- [[move-semantics]]
- [[object-lifetime]]
- [cppreference: unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference: shared_ptr](https://en.cppreference.com/w/cpp/memory/shared_ptr)
