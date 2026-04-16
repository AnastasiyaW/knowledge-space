---
description: "CWE-190: Arithmetic produces out-of-range result, wrapping or truncating. Leads to undersized buffer allocation, bypassed security checks, and memory corruption."
date: 2026-04-16
tags: [security, cwe, integer-overflow, buffer-overflow, c, cpp, go, java, rust, memory-safety]
level: Advanced
---

# CWE-190: Integer Overflow or Wraparound

**CWE-190** | CVSS Base Score range: 5.9-9.8 (when leading to heap corruption) | Rank 23 in CWE Top 25

## Functional Semantics

Integer overflow occurs when an arithmetic operation produces a mathematical result that cannot be represented in the target integer type. The stored value wraps (unsigned), is undefined (signed C/C++), or saturates (hardware-specific). The corrupted value subsequently propagates into security-sensitive operations: memory allocation sizes, array index calculations, loop bounds, and security threshold comparisons. The direct consequence is typically not exploitable; the exploitable condition arises when the wrapped value is used as a size (CWE-131/CWE-787), an index (CWE-129), or a security gate (bypassed check).

## Root Cause

Integer types have fixed bit widths. No language-level overflow detection exists in C, C++, Go, or Java by default. The programmer assumes arithmetic results remain in-range; the attacker provides inputs that violate this assumption. The vulnerability is structural: the operation and its use are logically coupled, but the type system does not enforce their combined safety.

## Overflow Taxonomy

| Type | Behavior | Language | Exploitability |
|---|---|---|---|
| Signed overflow | Undefined behavior (C/C++) — optimizer may eliminate check | C, C++ | High — UB enables compiler optimization that removes bounds checks |
| Unsigned wraparound | Well-defined: `(UINT_MAX + 1) → 0` | C, C++, Go | High — predictable, commonly exploited |
| Integer truncation | High bits lost on narrowing cast: `(uint8_t)256 → 0` | All | High — often occurs on function parameter cast |
| Multiplication overflow | `size_t count * size_t element_size` wraps to small value | C, C++ | High — classic heap allocation undersize |
| Signed/unsigned comparison | Signed negative compared as large unsigned positive | C, C++ | Medium — bypasses `< MAX_SIZE` checks |

## Trigger Conditions

- User controls a value used in: `malloc(n)`, `new T[n]`, array subscript `arr[n]`, `memcpy(dst, src, n)`, loop bound `for(i=0; i<n; i++)`
- Arithmetic is performed on user input before the security-sensitive use: `malloc(user_count * element_size)`
- Narrowing cast from wider to narrower type: `int n = (int) user_supplied_size_t`
- Comparison mixes signed and unsigned: `if (user_int < MAX_UNSIGNED)` where user_int is signed

## Language-Specific Behavior

| Language | Signed Overflow | Unsigned Overflow | Narrowing Cast | Built-in Check |
|---|---|---|---|---|
| C | **Undefined behavior** (UB) | Wraparound (defined) | Implementation-defined | `-ftrapv` flag (performance cost) |
| C++ | **Undefined behavior** | Wraparound (defined) | Implementation-defined | `-fsanitize=integer` (AddressSanitizer) |
| Go | Wraparound (defined) | Wraparound (defined) | Truncates, no panic | None; `math/bits.Add` for overflow-safe ops |
| Java | Wraparound (defined) | N/A (no unsigned) | `(int) longValue` silently truncates | `Math.addExact()` throws `ArithmeticException` |
| Rust | Panic in debug, **wraparound in release** | Same | Compile error (explicit cast required) | `checked_add()`, `saturating_add()`, `wrapping_add()` |
| Python | Arbitrary precision integers — no overflow | No overflow | N/A | N/A — immune |

## Vulnerable Patterns

### C — multiplication overflow in allocation

```c
// VULNERABLE: count=65537, size=65536 → 65537*65536 = 4,295,032,832
// On 32-bit: wraps to 65536 — allocates 64KB instead of 4GB
// memcpy then writes 4GB into 64KB buffer → heap overflow
void process_records(size_t count, size_t record_size, const char *src) {
    char *buf = malloc(count * record_size); // OVERFLOW: no check
    if (!buf) return;
    memcpy(buf, src, count * record_size);   // writes to undersized buffer
    free(buf);
}
```

### C — signed overflow in loop (UB → optimizer removes check)

```c
// VULNERABLE: signed integer overflow is UB in C
// Compiler may optimize: since i+1 > i is always true (no UB assumed),
// the loop continuation check may be removed entirely
int i;
for (i = 0; i <= INT_MAX; i++) { // compiler may prove i <= INT_MAX always, infinite loop or skip
    process(buf[i]);
}
```

### Java — silent int truncation on long multiplication

```java
// VULNERABLE: count * PAGE_SIZE overflows int if count > 2^21 (page size = 1024)
public byte[] allocateBuffer(int count, int pageSize) {
    int totalSize = count * pageSize; // wraps negative if > Integer.MAX_VALUE
    return new byte[totalSize]; // NegativeArraySizeException or undersized
}

// Example: count=2097153, pageSize=1024 → 2097153*1024 = 2,147,484,672 > INT_MAX
// Actual stored value: -2146482624 → NegativeArraySizeException → DoS
```

### Go — silent wraparound, no panic

```go
// VULNERABLE: Go integers wrap silently in all builds
func allocate(count, size int) []byte {
    total := count * size // wraps if count*size > MaxInt64
    return make([]byte, total) // panic: runtime: out of memory (if large) or undersized alloc
}

// More insidious: security bypass
func checkQuota(used, delta int64) bool {
    newUsed := used + delta // if delta is negative: used + large_negative = bypasses quota
    return newUsed <= QUOTA_MAX // attacker passes negative delta
}
```

## Fixed Patterns

### C — safe multiplication with overflow check

```c
#include <stdint.h>
#include <stddef.h>

// Method 1: __builtin_mul_overflow (GCC/Clang)
void process_records_safe(size_t count, size_t record_size, const char *src) {
    size_t total;
    if (__builtin_mul_overflow(count, record_size, &total)) {
        return; // overflow detected, reject
    }
    char *buf = malloc(total);
    if (!buf) return;
    memcpy(buf, src, total);
    free(buf);
}

// Method 2: pre-division check (portable C99)
void process_records_safe_v2(size_t count, size_t record_size, const char *src) {
    if (count > 0 && record_size > SIZE_MAX / count) {
        return; // would overflow
    }
    char *buf = malloc(count * record_size);
    if (!buf) return;
    memcpy(buf, src, count * record_size);
    free(buf);
}
```

### Java — Math.addExact / multiplyExact

```java
// FIXED: Math.multiplyExact throws ArithmeticException on overflow
public byte[] allocateBuffer(int count, int pageSize) {
    try {
        int totalSize = Math.multiplyExact(count, pageSize);
        if (totalSize > MAX_ALLOWED_SIZE) throw new IllegalArgumentException("Too large");
        return new byte[totalSize];
    } catch (ArithmeticException e) {
        throw new IllegalArgumentException("Buffer size overflow", e);
    }
}

// Alternative: promote to long before multiply, check, then cast
public byte[] allocateBuffer2(long count, long pageSize) {
    long totalSize = count * pageSize; // long multiplication — overflow at 2^63
    if (totalSize < 0 || totalSize > Integer.MAX_VALUE || totalSize > MAX_ALLOWED_SIZE) {
        throw new IllegalArgumentException("Invalid size");
    }
    return new byte[(int) totalSize];
}
```

### Rust — checked arithmetic (explicit overflow handling)

```rust
// VULNERABLE in release builds (wraps silently):
fn allocate(count: usize, size: usize) -> Vec<u8> {
    vec![0u8; count * size] // wraps in release, panics in debug
}

// FIXED: checked_mul returns None on overflow
fn allocate_safe(count: usize, size: usize) -> Result<Vec<u8>, &'static str> {
    let total = count.checked_mul(size).ok_or("size overflow")?;
    if total > MAX_ALLOCATION {
        return Err("allocation too large");
    }
    Ok(vec![0u8; total])
}

// For financial: saturating_add prevents wraparound, caps at MAX
fn add_to_balance(balance: u64, amount: u64) -> u64 {
    balance.saturating_add(amount) // returns u64::MAX instead of wrapping
}
```

### Go — explicit overflow pre-check

```go
import "math"

// FIXED: check before multiply
func allocateSafe(count, size int) ([]byte, error) {
    if count > 0 && size > math.MaxInt/count {
        return nil, fmt.Errorf("allocation overflow: count=%d size=%d", count, size)
    }
    total := count * size
    if total > MaxAllocationSize {
        return nil, fmt.Errorf("allocation too large: %d", total)
    }
    return make([]byte, total), nil
}
```

## Detection Heuristics

**Static analysis triggers:**
- `malloc(a * b)` or `calloc(a, b)` where `a` or `b` derives from user input without prior overflow check
- `new T[user_value]` or `make([]T, user_value)` without bounds check
- Arithmetic on user-controlled values preceding an array subscript: `arr[user_a + user_b]`
- Narrowing cast of user-supplied value: `(int)userLong`, `(uint8_t)userInt`, `(short)userInt`
- Mixed signed/unsigned comparison: `if (signed_var < unsigned_constant)` — implicit promotion may invert logic
- Java: `int result = (int)(userLong * constant)` without `Math.multiplyExact`

**Pattern triggers by consequence:**
- Allocation undersize: arithmetic result used as allocation size
- Index out of bounds: arithmetic result used as array subscript
- Security check bypass: arithmetic result used in `if (value < threshold)` or `if (value == expected)`
- Financial calculation: arithmetic on monetary values where negative results are possible

**False positive indicators:**
- Multiplication where both operands are compile-time constants or enum values with known ranges
- User-supplied value already validated against maximum before arithmetic: `if (n > 1000) return error; buf = malloc(n * 8);` — safe if `1000 * 8 < SIZE_MAX`
- Rust code using `wrapping_add`/`wrapping_mul` intentionally (e.g., hash functions, checksums) — semantic wraparound is the intended behavior
- Go code operating on values bounded by previous validation

## Compiler Mitigations

| Mitigation | Effect | Cost |
|---|---|---|
| `-ftrapv` (GCC/Clang) | Traps on signed overflow at runtime | 5-30% performance |
| `-fsanitize=integer` (UBSan) | Detects UB integer operations | For testing only |
| `FORTIFY_SOURCE=2` | Hardens stdlib string/memory functions | Minimal |
| Java `-ea` (assertions) | Enables assertion checks; use `assert Math.multiplyExact(a,b) > 0` | For testing only |
| Rust debug builds | Panic on overflow | Debug only by default |
| Rust `overflow-checks = true` in Cargo.toml | Panic on overflow in release | ~5-10% performance |

## Gotchas

- **Signed overflow is UB in C/C++, not wraparound.** Compiler optimization passes (especially loop strength reduction) exploit the assumption that signed overflow never occurs. Code like `if (i + 1 < i) { handle_overflow(); }` may be optimized away entirely because the compiler assumes `i + 1 < i` is always false (signed overflow → UB → condition always false per compiler). Use `-fwrapv` to treat signed overflow as wraparound, or use unsigned arithmetic with explicit checks.
- **calloc vs malloc:** `calloc(count, size)` performs the overflow check internally on most platforms. `malloc(count * size)` does not. Prefer `calloc` for array allocations in C.
- **Go int size is platform-dependent:** `int` is 32-bit on 32-bit platforms, 64-bit on 64-bit platforms. Code that passes overflow checks on 64-bit dev machines may overflow on 32-bit targets or older ARM devices.
- **Rust release mode wraps silently by default.** Many Rust developers assume overflow panics everywhere because debug mode does. Security-critical Rust code must use `checked_*` operations or enable `overflow-checks = true` in `Cargo.toml`.
- **Financial arithmetic demands arbitrary precision or decimal types.** `float64` has 15-17 significant decimal digits but accumulates rounding errors. Use `big.Int`/`big.Float` in Go, `decimal.Decimal` in Python, `BigDecimal` in Java for monetary calculations. Integer overflow in financial code can cause incorrect balances, not just crashes.

## See Also

- CWE-787: Out Of Bounds Write — most common consequence of allocation undersize from overflow
- CWE-125: Out Of Bounds Read — index overflow leading to read past buffer end
- CWE-369: Divide By Zero — related arithmetic error; attacker-controlled divisor = 0
- CWE-020: Input Validation — upstream control: validate numeric ranges before arithmetic
