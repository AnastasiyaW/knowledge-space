---
title: Object Lifetime and Construction
category: concepts
tags: [cpp, lifetime, constructor, destructor, initialization, copy-elision]
---

# Object Lifetime and Construction

Object construction, destruction, initialization forms, and copy elision. Understanding lifetime is essential for correctness and performance.

## Key Facts

- Object lifetime: construction -> use -> destruction
- Construction order: base classes (left to right) -> members (declaration order) -> constructor body
- Destruction order: reverse of construction
- Member initializer list: preferred over assignment in body (constructs directly, not default+assign)
- Delegating constructors (C++11): `MyClass(int x) : MyClass(x, 0) {}`
- `explicit` keyword: prevents implicit single-argument constructor conversions
- Copy elision (RVO/NRVO): compiler eliminates copy/move on return - mandatory in C++17
- Aggregate initialization: `Type{1, 2, 3}` for structs/arrays without user constructors
- Designated initializers (C++20): `Point{.x=1, .y=2}`
- Static local variables: initialized once, thread-safe in C++11
- Temporary lifetime extension: binding rvalue to `const T&` extends lifetime to ref scope

## Patterns

### Constructor Forms

```cpp
class Widget {
    int id_;
    std::string name_;
    std::vector<int> data_;
public:
    // Default constructor
    Widget() : id_(0), name_("default") {}

    // Parameterized - use initializer list
    Widget(int id, std::string name)
        : id_(id), name_(std::move(name)) {}  // move string into member

    // Delegating constructor
    Widget(int id) : Widget(id, "unnamed") {}

    // Explicit - prevent implicit conversion from int
    explicit Widget(double d) : Widget(static_cast<int>(d)) {}

    // In-class member initializers (C++11)
    int priority_ = 0;              // default if not in init list
    bool active_ = true;
};
```

### Initialization Syntax

```cpp
// Direct initialization
int a(42);
std::string s("hello");

// Copy initialization
int b = 42;
std::string s2 = "hello";

// List initialization (C++11) - narrowing-safe
int c{42};
// int d{3.14};  // ERROR: narrowing from double to int

// Aggregate initialization
struct Point { double x, y, z; };
Point p1{1.0, 2.0, 3.0};
Point p2{.x = 1.0, .y = 2.0};  // C++20 designated initializers

// std::initializer_list
std::vector<int> v{1, 2, 3, 4, 5};

// Default initialization vs value initialization
int* a1 = new int;     // indeterminate value (default init)
int* a2 = new int();   // zero (value init)
int* a3 = new int{};   // zero (value init via list init)
```

### Rule of Zero / Five

```cpp
// Rule of Zero: let standard types manage resources
struct Employee {
    std::string name;
    std::vector<std::string> skills;
    std::unique_ptr<Address> address;
    // No special member functions needed - compiler generates correct ones
};

// Rule of Five: when managing a raw resource
class RawBuffer {
    size_t size_;
    char* data_;
public:
    explicit RawBuffer(size_t n) : size_(n), data_(new char[n]) {}

    ~RawBuffer() { delete[] data_; }

    RawBuffer(const RawBuffer& other)
        : size_(other.size_), data_(new char[other.size_]) {
        std::memcpy(data_, other.data_, size_);
    }

    RawBuffer& operator=(const RawBuffer& other) {
        if (this != &other) {
            auto tmp = RawBuffer(other);
            std::swap(size_, tmp.size_);
            std::swap(data_, tmp.data_);
        }
        return *this;
    }

    RawBuffer(RawBuffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }

    RawBuffer& operator=(RawBuffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
};
```

### Copy Elision / RVO

```cpp
// Guaranteed copy elision (C++17) - no copy/move constructor needed
Widget create() {
    return Widget(42, "test");  // constructed directly in caller
}

// Named Return Value Optimization (NRVO) - not guaranteed but common
Widget build() {
    Widget w(1, "build");
    w.configure();
    return w;  // usually elided, otherwise moved
}

// Passing temporary to function
void consume(Widget w);
consume(Widget(42, "tmp"));  // elided: constructed directly in parameter
```

### Static and Thread-Local

```cpp
// Function-local static: initialized once, thread-safe (C++11)
Logger& get_logger() {
    static Logger instance;  // Meyers' Singleton
    return instance;
}

// Thread-local storage
thread_local int tls_counter = 0;
void per_thread_work() {
    ++tls_counter;  // each thread has its own copy
}
```

## Gotchas

- **Issue:** Most vexing parse: `Widget w();` declares a function, not an object -> **Fix:** Use `Widget w{};` or `Widget w;` for default construction
- **Issue:** Brace initialization with `std::initializer_list` overload surprises: `vector<int>{10}` creates 1-element vector with value 10, not 10-element vector -> **Fix:** Use `vector<int>(10)` for count-based constructor, `vector<int>{10}` for single-element list
- **Issue:** Member initializer list order doesn't match declaration order -> members initialized in declaration order regardless -> **Fix:** Always write init list in same order as member declarations. Enable `-Wreorder`.
- **Issue:** Temporary bound to `const T&` parameter in constructor stored as member -> dangling after constructor -> **Fix:** Take by value and move, or take by `string_view` and copy into string member

## See Also

- [[raii-resource-management]]
- [[move-semantics]]
- [[smart-pointers]]
- [[const-and-type-safety]]
