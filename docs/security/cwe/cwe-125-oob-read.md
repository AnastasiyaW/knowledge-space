---
description: "CWE-125: Out-of-bounds Read - reads past buffer boundaries leak secrets, keys, adjacent heap contents. Heartbleed archetype. Detection mirrors CWE-787 in read contexts."
date: 2026-04-16
tags: [security, cwe, memory-corruption, information-disclosure, c, cpp, heartbleed]
level: Advanced
---

# CWE-125: Out-of-bounds Read

**CWE Top 25 Rank:** 6 (2024).
**Primary impact:** Information disclosure (secrets, keys, adjacent heap/stack contents). Secondary: crash/DoS.
**Key distinction from [[cwe-787-oob-write]]:** Reads do not corrupt process state; they silently return bytes from adjacent memory. The process continues executing normally while leaking data.

---

## Functional Semantics

A read operation accesses memory at `base + offset` where `offset >= allocated_size`. The CPU fetches bytes from adjacent memory regions (another allocation, stack frame, mapped region) and returns them as if they were part of the intended buffer. No exception occurs unless the address crosses an unmapped page boundary.

**What is adjacent to a heap allocation:**
- Other live allocations (containing passwords, keys, tokens, PII)
- Freed memory (may contain previously sensitive data not zeroed)
- Allocator metadata (heap headers containing pointers - useful for defeating ASLR)
- Guard pages (trigger crash - SIGBUS/SIGSEGV - which is detectable)

**What is adjacent to a stack buffer:**
- Other local variables of the same function
- Saved registers (RBP, RBX, R12-R15)
- Return address (leaking this defeats ASLR/PIE)
- Caller's stack frame (leaking canary values)

---

## Heartbleed: The Canonical CWE-125 Case Study

CVE-2014-0160. OpenSSL 1.0.1 through 1.0.1f. CVSS 7.5.

```c
// OpenSSL tls1_process_heartbeat() - simplified
int tls1_process_heartbeat(SSL *s) {
    unsigned char *p = &s->s3->rrec.data[0];
    unsigned int payload;

    // Read payload length from the TLS record (attacker-controlled)
    n2s(p, payload);   // reads 2 bytes from network, assigns to payload
                       // attacker sends: type=heartbeat, length=65535, actual_data=1_byte

    // Allocate response buffer
    unsigned char *buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    unsigned char *bp = buffer;

    // Copy payload bytes from request into response - NO bounds check
    memcpy(bp, p, payload);   // copies 65535 bytes from a 1-byte buffer
                              // reads 65534 bytes of adjacent heap memory
    // Send buffer back to client
    ssl3_write_bytes(s, TLS1_RT_HEARTBEAT, buffer, 3 + payload + padding);
}
```

**Fix:**
```c
// Check actual record length vs claimed payload length
if (1 + 2 + payload + 16 > s->s3->rrec.length) {
    return 0;  // Silently discard malformed heartbeat
}
```

The lesson: the *length field in the data* and the *actual data length* are separate values. Whenever a protocol allows a client to specify a length for data it provides, verify the claimed length against the actual received length.

---

## Root Causes

### 1. Length field from untrusted source controls read size

```c
// VULNERABLE: network-supplied length drives memcpy source
void process_packet(const uint8_t *pkt, size_t pkt_len) {
    uint16_t claimed_len = *(uint16_t *)(pkt + 2);  // from packet header
    uint8_t *data_section = pkt + 4;

    uint8_t response[256];
    memcpy(response, data_section, claimed_len);     // reads claimed_len bytes
    // if claimed_len > pkt_len - 4: reads past end of pkt into adjacent memory
}
```

```c
// FIXED: clamp to actual available bytes
void process_packet(const uint8_t *pkt, size_t pkt_len) {
    if (pkt_len < 4) return;
    uint16_t claimed_len = *(uint16_t *)(pkt + 2);
    size_t available = pkt_len - 4;
    size_t read_len = (claimed_len < available) ? claimed_len : available;

    uint8_t response[256];
    if (read_len > sizeof(response)) return;
    memcpy(response, pkt + 4, read_len);
}
```

### 2. Signedness confusion in index computation

```c
// VULNERABLE: signed index, negative wraps to huge positive
char lookup_table[256];

char get_char(int8_t user_input) {
    // user_input = -1 → (int8_t)(-1) = 255 as unsigned, but...
    // user_input = -128 → index becomes 128 + huge_offset in some contexts
    return lookup_table[(unsigned char)user_input];  // seems safe
}

// More dangerous pattern:
char get_at_offset(char *buf, size_t buf_size, int offset) {
    if (offset < buf_size) {          // offset=-1 passes this check (signed < unsigned)
        return buf[offset];           // buf[-1] reads before the buffer
    }
    return 0;
}
```

```c
// FIXED: explicit sign check
char get_at_offset(char *buf, size_t buf_size, int offset) {
    if (offset < 0 || (size_t)offset >= buf_size) return 0;
    return buf[offset];
}
```

### 3. String operation without length limit

```c
// VULNERABLE: reads past end of non-null-terminated buffer
void log_field(const char *data, size_t data_len) {
    char field[128];
    strncpy(field, data, sizeof(field));   // may not null-terminate if data_len >= 128
    printf("Field: %s\n", field);           // printf reads until null - past field boundary
}
```

```c
// FIXED: explicit null-termination
void log_field(const char *data, size_t data_len) {
    char field[128];
    size_t copy_len = (data_len < sizeof(field) - 1) ? data_len : sizeof(field) - 1;
    memcpy(field, data, copy_len);
    field[copy_len] = '\0';   // explicit null termination
    printf("Field: %s\n", field);
}
```

### 4. Format string over-read

```c
// VULNERABLE: format string from user causes OOB reads of stack
void log_request(const char *user_fmt) {
    printf(user_fmt);   // %s %s %s reads stack values as pointers, then dereferences them
                        // %x %x %x leaks stack values as hex integers
}
```

```c
// FIXED: never use user data as format string
void log_request(const char *user_input) {
    printf("%s", user_input);  // user_input is a value, not a format specifier
}
```

---

## Information Leakage Taxonomy

| Memory region read | Data typically leaked | Exploitation use |
|--------------------|-----------------------|------------------|
| Adjacent heap chunk | Strings, keys, tokens in live allocations | Direct credential theft |
| Freed heap chunk | Previously sensitive data (if not zeroed) | Historical credential theft |
| Stack frame above caller | Local variables of callers up the call stack | Key material, pointers |
| Saved RIP on stack | Return address (text segment pointer) | ASLR/PIE bypass |
| Stack canary | Canary value | Bypass stack protection before OOB write |
| Heap allocator metadata | Heap pointers | ASLR bypass for heap; combined with OOB write |
| TLS/SSL session state | Session keys, master secret | Decrypt traffic |

---

## Affected Ecosystems

| Language | Risk | Notes |
|----------|------|-------|
| C | Critical | `memcpy`, `strcpy`, `printf(%s)` have no built-in bounds |
| C++ | Critical | Same as C plus `std::string::operator[]` (unchecked) |
| Rust (safe) | None | Panics on OOB slice read |
| Rust (unsafe) | High | `ptr::read`, `slice::from_raw_parts` bypass checks |
| Go | Low | Slice bounds checked at runtime; `unsafe.Slice` does not check |
| Java | Very Low | `ArrayIndexOutOfBoundsException` rather than silent read |
| Python (C extension) | Medium | Extension code in CPython can have OOB reads |
| WASM | Medium | Linear memory is shared; OOB reads stay within linear memory |

---

## Detection Heuristics

**Patterns to flag in C/C++:**

1. `memcpy(dst, src, n)` where `n` comes from the same data stream as `src` - Heartbleed pattern. Verify `n <= actual_src_len`.
2. `memcpy` / `memmove` with `n` derived from external input and no prior check `n <= src_allocation_size`.
3. `strlen(buf)` where `buf` is not guaranteed null-terminated (fixed-size packet field, file format field).
4. `printf(user_string)` or `sprintf(dst, user_string)` without format string argument - format string vulnerability (also causes OOB reads).
5. Array read `arr[i]` where `i` is declared `int` and derived from external input with only an upper-bound check (missing lower-bound check for negative values).
6. `strncpy(dst, src, n)` followed by use of `dst` as a C-string - `strncpy` does not guarantee null termination.

**Taint flow:**
- Source: `recv()`, `read()`, `fread()`, `getenv()`, file content fields
- Sink: `memcpy src`, `printf` format arg, array index in read expression
- Check: is there a `claimed_len <= actual_len` guard between source and sink?

**Protocol-specific pattern:** whenever a protocol message contains both a `length` field and a `data` field, verify `length <= sizeof(remaining_data)` before using `length` to drive any read.

---

## Crash vs Silent Leak

An OOB read that crosses a page boundary will segfault. This makes it detectable but also reveals the vulnerability (DoS). An OOB read within the same mapped region will succeed silently and return garbage data to the caller, which then forwards it to the attacker.

**Implication for detection:** Address Sanitizer (`-fsanitize=address`) catches silent OOB reads that would not crash. Valgrind `memcheck` also catches these. Regular testing without ASan will miss sub-page OOB reads.

---

## Fixing Patterns

| Pattern | Application |
|---------|-------------|
| Length clamping | `actual_len = min(claimed_len, available_bytes)` before any copy |
| Protocol validation | Reject packets where `header.length > packet.total_bytes - header.size` |
| Explicit null termination | After any `strncpy`, `memcpy` of string data, set `buf[copy_len] = '\0'` |
| ASan in CI | `-fsanitize=address` catches silent OOB reads; run all tests under ASan |
| `__attribute__((format))` | Lets compiler check `printf`-family calls for format/arg mismatch |
| Memory zeroing on free | `memset(ptr, 0, size); free(ptr)` or `explicit_bzero()` - reduces impact of read-after-free leaks |
| Safe string functions | `strnlen()` instead of `strlen()` on untrusted buffers |

---

## Gotchas - False Positive Indicators

- **`memcpy(dst, src, sizeof(src))`** where `src` is a fixed-size stack array - `sizeof` gives compile-time size; safe as long as `dst` is at least as large.
- **Pointer arithmetic with known-safe offsets:** `pkt + 4` when there is a prior `if (pkt_len < 4) return` guard - safe; check that all subsequent reads also verify against remaining length.
- **`strncpy` with correct size:** `strncpy(dst, src, sizeof(dst))` - safe for the copy, but the output may not be null-terminated. Downstream `strlen(dst)` or `printf("%s", dst)` is the actual risky operation.
- **Static analysis false positives on loops:** some tools flag `for(i=0; i<n; i++) use(buf[i])` when `n` is a function parameter. If the caller always passes `n <= actual_buf_len`, this is safe. Evaluate the calling convention.

---

## See Also

- [[cwe-787-oob-write]] - write-side counterpart; often paired with CWE-125 (leak address → write to leaked address)
- CWE-416: Use After Free - freed memory OOB read variant; stale pointer reads freed allocations
- [[cwe-134-uncontrolled-format-string]] - format string as a CWE-125 trigger
- CWE-119: Buffer Errors - parent CWE
- [[cwe-200-information-exposure]] - consequence CWE when data is disclosed
