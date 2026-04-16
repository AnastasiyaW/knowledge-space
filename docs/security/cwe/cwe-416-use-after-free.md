---
description: "CWE-416: Use After Free - accessing freed memory enables RCE, info disclosure, DoS. Dangling pointers, double-free, iterator invalidation, race conditions in free/use."
date: 2026-04-16
tags: [security, cwe, memory-corruption, use-after-free, c, cpp, rust]
level: Advanced
---

# CWE-416: Use After Free

**CWE Top 25 Rank:** 8 (2024). Consistent top-10 since 2019. 
**Severity:** CVSS 7.0–10.0. Most browser RCEs (V8, WebKit, Firefox) are UAF exploits.
**Root mechanism:** Memory manager reuses freed allocation; program accesses stale pointer; attacker-controlled allocation fills the freed region first.

---

## Functional Semantics

After `free(ptr)`, the allocator returns the memory to the heap. The allocator may immediately reuse that region for a subsequent `malloc()` call. If the program still holds a pointer to the freed region and accesses it:

- **Read:** returns attacker-influenced data if the allocator reused the region.
- **Write:** overwrites attacker-controlled allocation with program data.
- **Execute (function pointer/vtable):** jumps to attacker-controlled address.

**Heap grooming / type confusion attack:**
```
free(victim_object)      → allocator marks region free
malloc(attacker_size)    → if sizes match, region is reused for attacker allocation
attacker writes          → fills region with crafted data (fake vtable, fake object)
program uses victim_ptr  → reads/calls attacker's data as if it were victim_object
```

Modern allocators (tcmalloc, jemalloc, PartitionAlloc) segregate by size class and add security hardening, but UAF exploitation remains feasible via controlled allocation sequences.

---

## Root Causes

### 1. Dangling pointer after free

```c
// VULNERABLE: pointer not nulled after free
typedef struct { char name[32]; void (*callback)(void); } Handler;

void cleanup(Handler *h) {
    free(h);
    // h is now dangling - caller still holds the original pointer
}

void process_event(Handler *h, int event) {
    cleanup(h);
    if (event == RETRY) {
        h->callback();   // UAF: h was freed above; h->callback reads freed memory
    }
}
```

```c
// FIXED: null the pointer after free; check before use
void cleanup(Handler **h) {
    free(*h);
    *h = NULL;   // caller's pointer is nulled
}

void process_event(Handler **h, int event) {
    cleanup(h);
    if (event == RETRY && *h != NULL) {   // null check prevents UAF
        (*h)->callback();
    }
}
```

**Note:** Nulling the pointer prevents UAF via that specific pointer but not via *aliases* (other pointers pointing to the same allocation). Aliasing is the hard case.

### 2. Double-free

```c
// VULNERABLE: error path frees twice
int parse_message(Message *msg) {
    char *buf = malloc(msg->len);
    if (!buf) return -1;

    if (read_data(buf, msg->len) < 0) {
        free(buf);    // free on error
        return -1;
    }

    int result = process(buf);
    free(buf);        // free on success
    if (result < 0) {
        free(buf);    // BUG: double-free if process() returned error after buf was freed
    }
    return result;
}
```

```c
// FIXED: single ownership, one free path
int parse_message(Message *msg) {
    char *buf = malloc(msg->len);
    if (!buf) return -1;

    int result = -1;
    if (read_data(buf, msg->len) >= 0) {
        result = process(buf);
    }
    free(buf);   // single free, always executed
    return result;
}
```

Double-free in modern allocators (with tcache double-free detection) may abort with "double free detected in tcache 2". In older allocators or with bypass techniques, it's an exploitable heap corruption.

### 3. C++ iterator invalidation

```cpp
// VULNERABLE: modifying container while iterating invalidates iterators
void remove_inactive(std::vector<Session*>& sessions) {
    for (auto it = sessions.begin(); it != sessions.end(); ++it) {
        if ((*it)->is_inactive()) {
            delete *it;           // frees the Session object
            sessions.erase(it);   // invalidates it AND all iterators after it
            // ++it in loop increment now dereferences invalid iterator: UB/crash
        }
    }
}
```

```cpp
// FIXED: erase returns valid next iterator; or use remove_if
void remove_inactive(std::vector<Session*>& sessions) {
    for (auto it = sessions.begin(); it != sessions.end(); ) {
        if ((*it)->is_inactive()) {
            delete *it;
            it = sessions.erase(it);   // erase returns next valid iterator
        } else {
            ++it;
        }
    }
    // Or idiomatically:
    // sessions.erase(
    //     std::remove_if(sessions.begin(), sessions.end(),
    //         [](Session* s) { bool r = s->is_inactive(); if(r) delete s; return r; }),
    //     sessions.end());
}
```

**STL containers that invalidate iterators on mutation:**
- `std::vector`: insert/erase/push_back (realloc) invalidates all iterators
- `std::deque`: insert/erase at middle invalidates all; ends invalidate some
- `std::unordered_map`/`unordered_set`: rehash invalidates all iterators
- `std::list`/`std::map`/`std::set`: only iterators to erased elements are invalidated

### 4. Event handler / callback accessing freed object

```javascript
// JavaScript - conceptually UAF via closure (garbage-collected, but logic error pattern)
// In C++ event systems this is real UAF:

// C++ example
class Widget {
    ~Widget() { event_bus.unsubscribe(this); }  // MISSING: destructor doesn't unsubscribe
    void on_data(DataEvent& e) { this->process(e.data); }  // accesses this
};

// Elsewhere:
Widget *w = new Widget();
event_bus.subscribe("data", [w](DataEvent& e) { w->on_data(e); });
delete w;  // w freed but lambda still holds stale pointer in event_bus
// Next data event: lambda calls w->on_data() → UAF
```

```cpp
// FIXED: unsubscribe in destructor
class Widget {
    EventToken token_;
public:
    Widget() { token_ = event_bus.subscribe("data", [this](DataEvent& e) { on_data(e); }); }
    ~Widget() { event_bus.unsubscribe(token_); }  // explicit unsubscription
    void on_data(DataEvent& e) { process(e.data); }
};
```

### 5. Race condition: free in one thread, use in another

```c
// VULNERABLE: connection object freed in cleanup thread while worker uses it
typedef struct { int fd; char *buf; } Conn;

void *worker(void *arg) {
    Conn *c = (Conn *)arg;
    // ... uses c->buf, c->fd
    read(c->fd, c->buf, BUF_SIZE);   // race: c may be freed by cleanup thread
    return NULL;
}

void cleanup_thread(Conn *c) {
    free(c->buf);
    free(c);   // if worker is still running, UAF in worker
}
```

```c
// FIXED: reference counting with atomic ops
typedef struct { int fd; char *buf; _Atomic int refcount; } Conn;

Conn *conn_retain(Conn *c) { atomic_fetch_add(&c->refcount, 1); return c; }
void conn_release(Conn *c) {
    if (atomic_fetch_sub(&c->refcount, 1) == 1) {
        free(c->buf); free(c);
    }
}

void *worker(void *arg) {
    Conn *c = conn_retain((Conn *)arg);
    read(c->fd, c->buf, BUF_SIZE);
    conn_release(c);
    return NULL;
}
```

### 6. Rust `unsafe` UAF

```rust
// VULNERABLE: raw pointer use after deallocation
unsafe fn dangerous() {
    let b = Box::new(42i32);
    let ptr: *const i32 = &*b as *const i32;
    drop(b);               // b freed here
    println!("{}", *ptr);  // UAF: reads freed memory
}
```

```rust
// FIXED: use lifetime-tracked references; raw pointer only within known live scope
fn safe_version() -> i32 {
    let b = Box::new(42i32);
    let val = *b;  // copy the value before drop
    val            // return copy, not reference to freed memory
}
```

---

## Affected Ecosystems

| Language | Risk | Notes |
|----------|------|-------|
| C | Critical | Manual memory management, no lifetime tracking |
| C++ | Critical | `delete` + raw pointers; smart pointers mitigate if used consistently |
| C++ (smart ptrs) | Medium | `shared_ptr` cycles prevent deallocation; `weak_ptr` misuse → dangling |
| Rust (safe) | None | Borrow checker prevents UAF at compile time |
| Rust (unsafe) | High | Raw pointer operations bypass borrow checker |
| Go | Very Low | GC prevents UAF on GC-managed objects; `unsafe.Pointer` can UAF |
| Java/Python/JS | Very Low | GC prevents UAF; logic errors possible but not memory-level UAF |

---

## Detection Heuristics

**In C/C++:**

1. `free(ptr)` followed by any read/write/call via `ptr` or any alias without intervening `ptr = NULL`.
2. Search for `free(ptr)` inside functions that return `ptr` or store `ptr` elsewhere before freeing - multiple ownership.
3. Destructor patterns where a pointer is stored in multiple structures: `A.ptr = p; B.ptr = p; delete p;` - B.ptr is now dangling.
4. Event system patterns: `subscribe(lambda capturing raw pointer)` without corresponding `unsubscribe` in pointee's destructor.
5. Containers modified during iteration: range-for loops with `erase`, `insert`, `push_back` on the iterated container.
6. Multithreaded code: `free()` in one function, use in another, with no synchronization on the pointer.

**Static analysis tools:**
- Clang `scan-build` with `alpha.cplusplus.STLAlgorithmModeling`
- Cppcheck: `--enable=warning` flags obvious UAF
- Coverity: "USE_AFTER_FREE" checker
- CodeQL: `cpp/use-after-free`
- Valgrind `memcheck`: runtime detection with heap history

**Dynamic detection:**
- `-fsanitize=address` (ASan): catches UAF at runtime; reports exact allocation/free/use locations
- libdislocator (AFL): randomizes allocation to make UAF more likely to crash during fuzzing

---

## Exploitation Patterns

| Exploit type | Mechanism |
|-------------|-----------|
| Type confusion via UAF | Heap grooming: fill freed region with different type; original code reads it as original type → controlled field values |
| Virtual function table (vtable) overwrite | Object with vtable freed; new allocation placed at same address; attacker controls vtable pointer → arbitrary virtual call |
| Function pointer overwrite | Free struct containing function pointer; fill with crafted struct; code calls the function pointer → PC control |
| Info leak via UAF read | Read freed region containing adjacent allocation's sensitive data |
| Double-free to arbitrary write | Two frees → heap metadata corruption → controlled `malloc` return → write primitive |

---

## Fixing Patterns

| Pattern | Application |
|---------|-------------|
| Null pointer after free | `free(p); p = NULL;` - prevents use via that specific pointer |
| `std::unique_ptr` / `std::shared_ptr` | Ownership semantics prevent most UAF patterns in C++ |
| Reference counting | `shared_ptr`, custom atomic refcount; free only when count == 0 |
| RAII + scope-bounded lifetimes | Resource lifetime tied to scope; no manual free |
| `std::weak_ptr` for back-references | Non-owning reference that expires when owned object is destroyed |
| Epoch-based reclamation (RCU) | Deferred free until all readers finish; common in kernel/concurrent code |
| Address Sanitizer in CI | Catches UAF at runtime; essential for C/C++ test suites |
| Fuzzing with ASan | AFL++/libFuzzer + ASan is primary discovery method for browser/parser UAF |

---

## Gotchas - False Positive Indicators

- **`free(p); p = malloc(new_size);`** - pointer reused for new allocation in same scope; not UAF if there is no intervening use of the old value.
- **Smart pointer raw pointer extraction for interop:** `p.get()` passed to a C API that does not take ownership - safe as long as the `unique_ptr`/`shared_ptr` owner outlives the C API call.
- **`shared_ptr` passed to lambda:** the lambda captures a copy of the `shared_ptr`, extending lifetime; the pointee will not be freed until the lambda is destroyed - not UAF.
- **Pool allocators:** `free` in a pool context returns memory to the pool, not to the OS; subsequent "use" reads pool-managed memory which has not been overwritten by another allocation. Technically UAF but often not exploitable without pool grooming.
- **`std::vector` reallocation:** `vec.push_back(x)` may reallocate; references/iterators/pointers into the vector's old storage are invalidated, but this is a separate class of bug (dangling iterator/reference, not pointer UAF in the traditional sense).

---

## See Also

- [[cwe-787-oob-write]] - often chained: UAF read leaks address, OOB write exploits it
- CWE-125: Out-of-Bounds Read - read-side memory error; UAF read is a subclass
- CWE-415: Double Free - direct subtype; double-free → heap corruption → UAF-equivalent impact
- CWE-362: Race Condition - concurrent UAF root cause
- CWE-672: Operation On Resource After Expiration - semantic parent for expired resource access
