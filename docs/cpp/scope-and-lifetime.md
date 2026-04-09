---
title: "Variable Scope and Lifetime in C++"
description: "Block-level scoping rules, name shadowing, and deterministic destruction order as prerequisite for RAII"
---

# Variable Scope and Lifetime in C++

C++ has block-level scoping with strict rules about where variables are visible and when they are destroyed. Understanding scope prevents name shadowing bugs and is prerequisite for [[raii-resource-management]].

## Scope Levels

C++ supports three scope levels:

1. **Global scope** - declared outside all functions, accessible everywhere
2. **Function/local scope** - declared inside a function, accessible within that function
3. **Block scope** - declared inside `{}`, accessible only within that block

```cpp
int x = 10;  // global scope

int main() {
    int x = 20;  // local scope (shadows global x)

    {
        int x = 30;  // block scope (shadows local x)
        std::cout << x;  // prints 30 (nearest scope)
    }

    std::cout << x;  // prints 20 (block x is gone)

    // Access global x despite local shadow:
    std::cout << ::x;  // prints 10 (scope resolution operator)
}
```

## Name Lookup Rules

When a name is used, the compiler searches from the innermost scope outward:
1. Current block
2. Enclosing blocks
3. Function scope
4. Namespace scope
5. Global scope

The **first match wins**. Inner declarations shadow outer ones.

## Scope Resolution Operator

The `::` operator accesses a specific scope:

```cpp
int x = 10;  // global

int main() {
    int x = 20;  // local shadows global
    std::cout << x;    // 20 (local)
    std::cout << ::x;  // 10 (global, bypassing shadow)
}
```

Also used for namespace and class member access: `std::cout`, `MyClass::method`.

## Storage Duration

| Duration | Created | Destroyed | Example |
|----------|---------|-----------|---------|
| Automatic | Block entry | Block exit | Local variables |
| Static | Program start | Program end | `static` locals, globals |
| Dynamic | `new` | `delete` | Heap-allocated |
| Thread | Thread start | Thread end | `thread_local` |

## const as Documentation

Marking variables `const` serves as scope documentation:

```cpp
void process() {
    const int max_retries = 3;  // documents: this will not change
    int attempts = 0;           // documents: this WILL change

    // Technique for exploring unfamiliar code:
    // 1. Mark everything const
    // 2. Compile
    // 3. Remove const where compiler complains
    // Result: map of which variables actually vary
}
```

Rules for `const`:
- Must be initialized at declaration (no "make it const later")
- Compiler enforces: attempts to modify produce a compile error
- Communicates intent to other developers reading the code

## Global Variables

Global variables are:
- Created at program start, destroyed at program end
- Not stored on stack or heap (dedicated memory segment)
- Accessible from any function (bad for encapsulation)
- Initialization order across translation units is **undefined** (Static Initialization Order Fiasco)

**General rule**: avoid global mutable state. Use `const`/`constexpr` globals for true constants, pass state via parameters for everything else.

## Gotchas

- **Shadowing is silent by default.** Declaring a variable with the same name in an inner scope is valid C++ and produces no warning unless you enable `-Wshadow`. Always compile with warnings enabled.
- **Variables declared in `for` init are block-scoped to the loop.** `for (int i = 0; ...)` - `i` does not exist after the loop body.
- **`if`-init statements (C++17) are block-scoped.** `if (auto it = map.find(key); it != map.end())` - `it` only exists inside the if/else.
- **Static local variables are initialized once** on first function call, then persist. They are NOT re-initialized on subsequent calls - this is useful for lazy initialization patterns.

## Cross-References

- [[raii-resource-management]] - tying cleanup to scope exit
- [[object-lifetime]] - construction and destruction order
- [[const-and-type-safety]] - const correctness
- [[smart-pointers]] - scope-based memory management
