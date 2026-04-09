---
title: "Manual Memory Management in C++"
description: "Raw new/delete, stack vs heap, and the three failure modes that motivate smart pointers and RAII"
---

# Manual Memory Management in C++

Understanding raw `new`/`delete` is essential for comprehending why [[smart-pointers]] and [[raii-resource-management]] exist. Manual memory management is error-prone and should be avoided in modern C++, but knowing the failure modes is critical.

## Stack vs Heap (Free Store)

**Stack**: automatic storage. Objects created when scope is entered, destroyed when scope exits. No manual management needed.

**Heap (Free Store)**: dynamic storage. Objects created with `new`, persist until explicitly destroyed with `delete`. The programmer is fully responsible for lifetime.

```cpp
void example() {
    Resource local("local");     // stack: automatic cleanup at }

    Resource* p = new Resource("heap");  // heap: manual cleanup
    p->getName();
    delete p;                    // must explicitly destroy
}  // local destroyed here automatically, p's memory was freed above
```

## Three Failure Modes

### 1. Use After Delete (Dangling Pointer)

```cpp
Resource* p = new Resource("data");
delete p;
p->getName();  // UNDEFINED BEHAVIOR: p points to freed memory
// Crash, garbage data, or silent corruption
```

### 2. Double Delete

```cpp
Resource* p = new Resource("data");
Resource* p2 = p;    // copy the pointer, not the object
delete p2;           // frees the memory
delete p;            // CRASH: same memory freed twice
```

Copying raw pointers is dangerous because multiple pointers to the same object create ambiguity about who is responsible for deletion.

### 3. Memory Leak

```cpp
Resource* p = new Resource("data");
if (someCondition) {
    return;  // early return: delete never reached
}
delete p;    // never executes when condition is true
```

The rule "every `new` must have exactly one `delete`" sounds simple but breaks down with:
- Early returns
- Exceptions thrown between `new` and `delete`
- Complex control flow
- Pointer copies creating ownership ambiguity

## Overloading new and delete

`new` and `delete` are operators that can be overloaded for custom behavior. The overload only affects the memory allocation/deallocation part - construction and destruction are unchanged.

```cpp
#include <cstdlib>
#include <cstddef>

// Track allocations globally
static std::size_t allocated_mem = 0;

void* operator new(std::size_t size) {
    allocated_mem += size;
    std::cout << "Allocating " << size << " bytes\n";
    return std::malloc(size);
}

void operator delete(void* ptr, std::size_t size) noexcept {
    allocated_mem -= size;
    std::cout << "Deallocating " << size << " bytes\n";
    std::free(ptr);
}

// At program end: if allocated_mem != 0, there is a leak
```

Use cases for overloading:
- **Custom memory leak detection** - track allocation/deallocation balance
- **Memory pooling** - pre-allocate large blocks, stack objects together to reduce fragmentation
- **Embedded systems** - implement custom heap when OS does not provide one
- **Performance profiling** - graph allocation patterns over time
- **Class-specific overloads** - optimize allocation for a specific class

## Global vs Class-Scoped Overloads

```cpp
// Global: affects ALL allocations in the program
void* operator new(std::size_t size) { /* ... */ }

// Class-scoped: affects only this class
class MyObject {
    static void* operator new(std::size_t size) { /* ... */ }
    static void operator delete(void* ptr) { /* ... */ }
};
```

## Vector: Size vs Capacity

Understanding how `std::vector` manages memory internally:

```cpp
std::vector<Subject> v;
// size=0, capacity=0

v.reserve(3);
// size=0, capacity=3 (memory allocated, no objects constructed)

v.emplace_back("Math", 95);
// size=1, capacity=3 (one object constructed in-place)

v.push_back(Subject("History", 80));
// size=2, capacity=3 (temporary created then moved)

v.clear();
// size=0, capacity=3 (objects destroyed but memory NOT freed)
```

Key distinctions:
- `reserve(n)`: allocates capacity without constructing objects
- `resize(n)`: changes size, constructs/destroys objects as needed
- `emplace_back(args...)`: constructs object in-place (no temporary, no move)
- `push_back(obj)`: copies/moves existing object into vector
- `clear()`: destroys all objects but does NOT reduce capacity
- `shrink_to_fit()`: requests (non-binding) capacity reduction

**Prefer `emplace_back` over `push_back`** when constructing new objects - eliminates temporary and move constructor overhead.

## The Modern C++ Answer

The entire class of manual memory management bugs is solved by:
1. **RAII** - tie resource lifetime to object scope
2. **`std::unique_ptr`** - exclusive ownership, zero overhead
3. **`std::shared_ptr`** - shared ownership with reference counting
4. Never use raw `new`/`delete` in application code

## Gotchas

- **`delete` on a null pointer is safe** (no-op by standard), but `delete` on an already-deleted pointer is undefined behavior.
- **`clear()` does not free vector memory.** Only destructor or `shrink_to_fit()` can reduce capacity. This is by design for performance - avoids reallocations if you refill the vector.
- **Global `operator new` overloads affect the entire program**, including library code. Use class-scoped overloads for targeted behavior.
- **`malloc`/`free` do NOT call constructors/destructors.** Only use them inside `operator new`/`operator delete` overloads, never directly in C++ code.

## Cross-References

- [[smart-pointers]] - `unique_ptr`, `shared_ptr`, `weak_ptr`
- [[raii-resource-management]] - the pattern that replaces manual management
- [[object-lifetime]] - scope, storage duration, destruction order
- [[move-semantics]] - efficient transfer of resources
