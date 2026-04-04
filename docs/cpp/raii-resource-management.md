---
title: RAII and Resource Management
category: concepts
tags: [cpp, raii, memory, lifetime, resource, destructor]
---

# RAII and Resource Management

Resource Acquisition Is Initialization - tie resource lifetime to object lifetime. Constructor acquires, destructor releases. The single most important C++ idiom.

## Key Facts

- RAII guarantees cleanup via destructor, even during exceptions (stack unwinding)
- Every resource (memory, files, locks, sockets, handles) should be owned by an RAII wrapper
- Stack-allocated RAII objects are destroyed in reverse order of construction
- Destructor must not throw exceptions - if it does during stack unwinding, `std::terminate` is called
- Standard RAII wrappers: `unique_ptr`, `shared_ptr`, `lock_guard`, `unique_lock`, `fstream`, `string`, `vector`
- Raw `new`/`delete` should almost never appear in modern C++ - use [[smart-pointers]] or containers
- Copy semantics: deep copy or disable copying (`= delete`)
- Move semantics: transfer ownership cheaply, see [[move-semantics]]
- Rule of Zero > Rule of Five > manual management

## Patterns

### Basic RAII Wrapper

```cpp
class FileHandle {
    FILE* fp_;
public:
    explicit FileHandle(const char* path, const char* mode)
        : fp_(fopen(path, mode)) {
        if (!fp_) throw std::runtime_error("Cannot open file");
    }

    ~FileHandle() {
        if (fp_) fclose(fp_);
    }

    // Non-copyable
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Movable
    FileHandle(FileHandle&& other) noexcept : fp_(other.fp_) {
        other.fp_ = nullptr;
    }
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (fp_) fclose(fp_);
            fp_ = other.fp_;
            other.fp_ = nullptr;
        }
        return *this;
    }

    FILE* get() const { return fp_; }
};
```

### Lock Guard Pattern

```cpp
std::mutex mtx;

void safe_operation() {
    std::lock_guard<std::mutex> lock(mtx);  // acquires lock
    // ... critical section ...
}  // lock released automatically, even if exception thrown

// C++17 CTAD
void modern() {
    std::lock_guard lock(mtx);   // template args deduced
}

// For more control, use unique_lock
void flexible() {
    std::unique_lock lock(mtx);
    // can unlock/relock, use with condition_variable
    lock.unlock();
    // ... non-critical work ...
    lock.lock();
}
```

### Scope Guard (Generic RAII)

```cpp
template<typename F>
class ScopeGuard {
    F cleanup_;
    bool active_ = true;
public:
    explicit ScopeGuard(F f) : cleanup_(std::move(f)) {}
    ~ScopeGuard() { if (active_) cleanup_(); }
    void dismiss() { active_ = false; }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};

// Usage
void transactional_work() {
    begin_transaction();
    auto guard = ScopeGuard([] { rollback_transaction(); });

    do_step_1();
    do_step_2();
    commit_transaction();
    guard.dismiss();  // success - don't rollback
}
```

### Rule of Zero

```cpp
// Best practice: let compiler-generated defaults handle everything
class Person {
    std::string name_;                    // manages its own memory
    std::vector<std::string> aliases_;    // manages its own memory
    std::unique_ptr<Address> address_;    // manages its own memory

    // No destructor, no copy/move ops needed
    // Compiler generates correct versions automatically
};
```

### Constructor/Destructor Order

```cpp
class Base {
public:
    Base()  { std::cout << "Base ctor\n"; }
    ~Base() { std::cout << "Base dtor\n"; }
};

class Member {
public:
    Member()  { std::cout << "Member ctor\n"; }
    ~Member() { std::cout << "Member dtor\n"; }
};

class Derived : public Base {
    Member m_;
public:
    Derived()  { std::cout << "Derived ctor\n"; }
    ~Derived() { std::cout << "Derived dtor\n"; }
};

// Construction order:  Base -> Member -> Derived body
// Destruction order:   Derived body -> Member -> Base
```

## Gotchas

- **Issue:** Destructor throws during stack unwinding -> `std::terminate` called -> **Fix:** Destructors must be `noexcept` (implicit since C++11). Catch exceptions inside destructor.
- **Issue:** Raw `new` without matching `delete` - leak on exception between allocation and assignment -> **Fix:** Use `make_unique`/`make_shared`, never raw `new`
- **Issue:** Forgetting virtual destructor in polymorphic base class -> UB when deleting derived through base pointer -> **Fix:** Base class with virtual functions must have `virtual ~Base() = default;`
- **Issue:** Members initialized in wrong order (init-list order vs declaration order) -> **Fix:** Member initializer list order must match declaration order. Compiler warns with `-Wreorder`.

## See Also

- [[smart-pointers]]
- [[move-semantics]]
- [[error-handling]]
- [[object-lifetime]]
