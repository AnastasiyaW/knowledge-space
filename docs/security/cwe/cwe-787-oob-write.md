---
description: "CWE-787: Out-of-bounds Write - memory corruption via writes past buffer boundaries. Root causes, detection heuristics, exploitability factors, and fix patterns."
date: 2026-04-16
tags: [security, cwe, memory-corruption, buffer-overflow, c, cpp, rust]
level: Advanced
---

# CWE-787: Out-of-bounds Write

**CWE Top 25 Rank:** 2 (2024). Consistent top-3 since 2019.
**CVSS pattern:** typically 7.5–10.0. Heap OOB write = code execution primitive in modern exploits.

---

## Functional Semantics

A write operation targets memory address `base + offset` where `offset >= allocated_size`. The write lands in adjacent memory: another heap chunk's metadata, a stack frame's return address, or a global variable. The semantics are: the program believes it is writing to its own data; the CPU executes the write without fault; the process state is silently corrupted.

This is distinct from a segfault (which occurs only when the target address is unmapped). OOB writes within the same allocation arena succeed silently.

**Consequence chain:**
```
OOB write → corrupt adjacent data
           → if metadata (heap chunk header): heap corruption → malloc/free crash or controlled allocation
           → if return address (stack): control flow hijack
           → if vtable pointer: type confusion → arbitrary virtual dispatch
           → if adjacent buffer: data corruption, logic errors, secondary vulnerabilities
```

---

## Root Causes

### 1. Off-by-one in loop bounds

```c
// VULNERABLE: writes index n into buffer of size n
void copy_path(char *dst, const char *src, size_t n) {
    size_t i;
    for (i = 0; i <= n; i++) {   // <= should be <
        dst[i] = src[i];
    }
}
```

`dst[n]` writes one byte past the allocation. On the stack this overwrites the next local variable or saved frame pointer.

```c
// FIXED
void copy_path(char *dst, const char *src, size_t n) {
    size_t i;
    for (i = 0; i < n; i++) {
        dst[i] = src[i];
    }
    dst[n - 1] = '\0';  // explicit null termination within bounds
}
```

### 2. Integer overflow in size calculation

```c
// VULNERABLE: attacker controls nmemb and size
void *make_grid(size_t nmemb, size_t size) {
    void *buf = malloc(nmemb * size);   // overflow if nmemb=0x80000001, size=2 → allocates 2 bytes
    if (!buf) return NULL;
    memset(buf, 0, nmemb * size);       // writes nmemb*size bytes into 2-byte buffer
    return buf;
}
```

```c
// FIXED: use calloc (handles overflow internally) or check explicitly
#include <stdint.h>
void *make_grid(size_t nmemb, size_t size) {
    if (nmemb && size > SIZE_MAX / nmemb) return NULL;  // overflow check
    return calloc(nmemb, size);  // calloc zeroes + checks overflow
}
```

### 3. Unbounded string copy

```c
// VULNERABLE: strcpy/sprintf without length limit
char hostname[64];
void set_hostname(const char *user_input) {
    strcpy(hostname, user_input);   // OOB if input > 63 chars
}
```

```c
// FIXED
void set_hostname(const char *user_input) {
    snprintf(hostname, sizeof(hostname), "%s", user_input);
    // OR: strlcpy(hostname, user_input, sizeof(hostname));
}
```

### 4. Rust `unsafe` slice indexing

```rust
// VULNERABLE
unsafe fn write_header(buf: &mut [u8], offset: usize, value: u32) {
    let ptr = buf.as_mut_ptr().add(offset);  // no bounds check
    *(ptr as *mut u32) = value;              // UB if offset + 4 > buf.len()
}
```

```rust
// FIXED: bounds check before unsafe, or use safe API
fn write_header(buf: &mut [u8], offset: usize, value: u32) -> Option<()> {
    buf.get_mut(offset..offset + 4)?
       .copy_from_slice(&value.to_le_bytes());
    Some(())
}
```

---

## Trigger Conditions

| Condition | Mechanism |
|-----------|-----------|
| External input controls array index | Direct index injection |
| External input controls allocation size | Integer overflow in `n * sizeof(T)` |
| External input controls loop bound | Off-by-one via crafted length field |
| Network/file-supplied length field < actual data | Write past truncated allocation |
| Signed/unsigned mismatch in index | Negative index wraps to large positive |

**Signed/unsigned mismatch example:**

```c
// VULNERABLE: signed comparison with unsigned loop variable
int8_t index = get_user_index();  // attacker sends -1
if (index < MAX_ITEMS) {           // -1 < 10 → true
    table[index] = value;          // table[-1] = write before array
}
```

---

## Affected Ecosystems

| Language | Risk | Notes |
|----------|------|-------|
| C | Critical | No bounds checking anywhere in stdlib by default |
| C++ | Critical | STL `operator[]` unchecked; `.at()` throws but rarely used |
| Rust (safe) | None | Panics on OOB at runtime |
| Rust (unsafe) | High | `ptr::write`, `slice::from_raw_parts_mut` have no checks |
| Go | Low | Runtime panics on OOB slice write; `unsafe.Pointer` arithmetic bypasses this |
| Java/Python/JS | Very Low | Managed runtimes; array OOB = exception, not corruption |
| Assembly | Critical | No runtime protection |

---

## Detection Heuristics

**High-signal patterns (review immediately):**

1. `memcpy(dst, src, len)` where `len` derives from external input without a `len <= sizeof(dst)` guard immediately before.
2. `strcpy`, `strcat`, `gets`, `sprintf` (without `n` variants) - treat as automatic findings.
3. Array subscript `arr[i]` where `i` is `int` or `size_t` derived from a network/file/IPC source.
4. `malloc(a * b)` or `malloc(a + b)` where either operand is external input - overflow possible.
5. Pointer arithmetic: `ptr + offset` where `offset` is external and there is no `ptr + offset < ptr + alloc_size` check.
6. `for (i = 0; i <= len; i++)` - off-by-one; `<=` should almost always be `<`.

**Static analysis anchors:**
- Taint: source = `read()`, `recv()`, `fread()`, `getenv()`, `argv[]`
- Sink: `memcpy dst`, `strcpy dst`, array subscript write, pointer dereference write
- Check: is taint sanitized (bounds checked) on all paths between source and sink?

---

## Exploitability Factors

| Factor | Impact on exploitability |
|--------|--------------------------|
| Heap OOB vs stack OOB | Heap: ASLR/PIE bypass needed; Stack: often direct RIP/EIP control |
| Write size | 1 byte (off-by-one): hard but possible (House of Einherjar); arbitrary: straightforward |
| Adjacent data | Heap metadata > vtable ptr > return addr in terms of control |
| ASLR/PIE enabled | Increases difficulty; info leak (CWE-125) typically used to defeat |
| Stack canaries | Detects stack buffer overflow before return; heap OOB unaffected |

---

## Fixing Patterns

| Pattern | Application |
|---------|-------------|
| Use `n`-bounded functions | `strncpy`, `snprintf`, `strncat`, `fgets` over unbounded equivalents |
| `calloc` for array allocation | Handles `nmemb * size` overflow check per C11 |
| Explicit pre-condition check | `assert(offset + len <= buf_size)` or `if` guard returning error |
| Address Sanitizer (ASan) in tests | `-fsanitize=address` catches OOB at runtime in test suites |
| Fortify Source | `-D_FORTIFY_SOURCE=2` adds compile-time and runtime checks for string functions |
| Static analysis | Coverity, CodeQL `cpp/overflow-buffer`, PVS-Studio V531, Semgrep `c.lang.security.buffer-not-null-terminated` |
| Safe wrappers | `strlcpy`/`strlcat` (OpenBSD), `memcpy_s` (C11 Annex K) |

---

## Gotchas - False Positive Indicators

- **Ring buffer modulo:** `buf[i % SIZE]` - always in-bounds if `SIZE` matches `sizeof(buf)/sizeof(buf[0])`. Verify the modulus matches the allocation size exactly.
- **Sentinel-terminated copy:** `while (*src) dst[i++] = *src++;` - looks dangerous but caller may guarantee `strlen(src) < sizeof(dst)`. Verify contract at call site.
- **Known-size stack local + sizeof guard:** `memcpy(local, src, sizeof(local))` with `local` being a fixed stack array - this is safe; sizeof gives compile-time size.
- **Two-phase alloc+fill:** `malloc(n)` then `memset(p, 0, n)` with the same `n` - safe; the common dangerous pattern is where the fill uses a *different* `n` from the alloc.
- **Compiler-inserted array size:** GCC/Clang `-Warray-bounds` may catch some but not dynamic cases; absence of warning does not mean absence of bug.

---

## See Also

- CWE-125: Out-of-Bounds Read - read-side counterpart; often paired in Heartbleed-style bugs
- CWE-416: Use After Free - another memory corruption class; often chained with OOB write
- CWE-190: Integer Overflow - root cause for size-calculation OOB writes
- CWE-119: Buffer Errors - parent CWE
- CWE-121: Stack Overflow - stack-specific subtype
- CWE-122: Heap Overflow - heap-specific subtype
