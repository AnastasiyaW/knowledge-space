---
description: "CWE-190: Arithmetische Operation liefert ein Ergebnis außerhalb des Wertebereichs, mit Umbruch oder Abschneiden. Führt zu zu klein dimensionierten Puffern, umgangenen Sicherheitsprüfungen und Speicherbeschädigung."
date: 2026-04-16
tags: [security, cwe, integer-overflow, buffer-overflow, c, cpp, go, java, rust, memory-safety]
level: Advanced
source_sha256: e10946a8eab72d3863c2828da5a9668701d94e38f4bb7ca0e0c6c72162f47b99
translation: machine
translated_at: '2026-10-24'
---
# CWE-190: Ganzzahlüberlauf oder Wraparound {#cwe-190-integer-overflow-or-wraparound}

**CWE-190** | CVSS-Basiswert-Bereich: 5,9–9,8 (bei Heap-Korruption) | Rang 23 in den CWE Top 25

## Funktionale Semantik {#functional-semantics}

Ein Ganzzahlüberlauf tritt auf, wenn eine arithmetische Operation ein mathematisches Ergebnis liefert, das im Zieltyp nicht darstellbar ist. Der gespeicherte Wert läuft um (vorzeichenlos), ist undefiniert (vorzeichenbehaftet in C/C++) oder wird gesättigt (hardwarespezifisch). Der beschädigte Wert gelangt anschließend in sicherheitsrelevante Operationen: Speicherallokationsgrößen, Berechnungen von Array-Indizes, Schleifengrenzen und Vergleiche mit Sicherheitsschwellen. Die unmittelbare Folge ist typischerweise nicht ausnutzbar; die ausnutzbare Bedingung entsteht, wenn der umgebrochene Wert als Größe (CWE-131/CWE-787), als Index (CWE-129) oder als Sicherheitsschranke (umgangene Prüfung) verwendet wird.

## Grundursache {#root-cause}

Ganzzahltypen haben feste Bitbreiten. In C, C++, Go und Java existiert standardmäßig keine sprachseitige Überlauferkennung. Der Programmierer geht davon aus, dass arithmetische Ergebnisse im gültigen Bereich bleiben; der Angreifer liefert Eingaben, die diese Annahme verletzen. Die Verwundbarkeit ist strukturell: Operation und Verwendung sind logisch gekoppelt, das Typsystem erzwingt ihre gemeinsame Sicherheit jedoch nicht.

## Taxonomie der Überläufe {#overflow-taxonomy}

| Typ | Verhalten | Sprache | Ausnutzbarkeit |
|---|---|---|---|
| Vorzeichenbehafteter Überlauf | Undefiniertes Verhalten (C/C++) — Optimierer kann Prüfung entfernen | C, C++ | Hoch — UB ermöglicht Compiler-Optimierungen, die Grenzprüfungen entfernen |
| Vorzeichenloser Wraparound | Wohldefiniert: `(UINT_MAX + 1) → 0` | C, C++, Go | Hoch — vorhersagbar, häufig ausgenutzt |
| Ganzzahl-Abschneiden | Hohe Bits gehen bei verengendem Cast verloren: `(uint8_t)256 → 0` | Alle | Hoch — tritt häufig beim Cast von Funktionsparametern auf |
| Multiplikationsüberlauf | `size_t count * size_t element_size` läuft auf kleinen Wert um | C, C++ | Hoch — klassische Unterdimensionierung bei Heap-Allokation |
| Vorzeichen-/Vorzeichenlos-Vergleich | Negativer vorzeichenbehafteter Wert wird als großer vorzeichenloser Wert verglichen | C, C++ | Mittel — umgeht Prüfungen wie `< MAX_SIZE` |

## Auslösebedingungen {#trigger-conditions}

- Der Benutzer kontrolliert einen Wert, der verwendet wird in: `malloc(n)`, `new T[n]`, Array-Zugriff `arr[n]`, `memcpy(dst, src, n)`, Schleifengrenze `for(i=0; i<n; i++)`
- Auf Benutzereingaben wird vor der sicherheitsrelevanten Verwendung gerechnet: `malloc(user_count * element_size)`
- Verengender Cast von einem breiteren in einen schmaleren Typ: `int n = (int) user_supplied_size_t`
- Vergleich mit gemischtem Vorzeichen: `if (user_int < MAX_UNSIGNED)`, wobei `user_int` vorzeichenbehaftet ist

## Sprachspezifisches Verhalten {#language-specific-behavior}

| Sprache | Vorzeichenbehafteter Überlauf | Vorzeichenloser Überlauf | Verengender Cast | Eingebaute Prüfung |
|---|---|---|---|---|
| C | **Undefiniertes Verhalten** (UB) | Wraparound (definiert) | Implementierungsabhängig | Flag `-ftrapv` (Leistungskosten) |
| C++ | **Undefiniertes Verhalten** | Wraparound (definiert) | Implementierungsabhängig | `-fsanitize=integer` (AddressSanitizer) |
| Go | Wraparound (definiert) | Wraparound (definiert) | Schneidet ab, kein Panic | Keine; `math/bits.Add` für überlaufsichere Operationen |
| Java | Wraparound (definiert) | Nicht zutreffend (kein Vorzeichenlos) | `(int) longValue` schneidet stillschweigend ab | `Math.addExact()` wirft `ArithmeticException` |
| Rust | Panic im Debug-Build, **Wraparound im Release-Build** | Gleich | Compilerfehler (expliziter Cast erforderlich) | `checked_add()`, `saturating_add()`, `wrapping_add()` |
| Python | Ganzzahlen beliebiger Genauigkeit — kein Überlauf | Kein Überlauf | Nicht zutreffend | Nicht zutreffend — immun |

## Verwundbare Muster {#vulnerable-patterns}

### C — Multiplikationsüberlauf bei der Allokation {#c-multiplication-overflow-in-allocation}

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

### C — vorzeichenbehafteter Überlauf in Schleife (UB → Optimierer entfernt Prüfung) {#c-signed-overflow-in-loop-ub-optimizer-removes-check}

```c
// VULNERABLE: signed integer overflow is UB in C
// Compiler may optimize: since i+1 > i is always true (no UB assumed),
// the loop continuation check may be removed entirely
int i;
for (i = 0; i <= INT_MAX; i++) { // compiler may prove i <= INT_MAX always, infinite loop or skip
    process(buf[i]);
}
```

### Java — stilles int-Abschneiden bei long-Multiplikation {#java-silent-int-truncation-on-long-multiplication}

```java
// VULNERABLE: count * PAGE_SIZE overflows int if count > 2^21 (page size = 1024)
public byte[] allocateBuffer(int count, int pageSize) {
    int totalSize = count * pageSize; // wraps negative if > Integer.MAX_VALUE
    return new byte[totalSize]; // NegativeArraySizeException or undersized
}

// Example: count=2097153, pageSize=1024 → 2097153*1024 = 2,147,484,672 > INT_MAX
// Actual stored value: -2146482624 → NegativeArraySizeException → DoS
```

### Go — stiller Wraparound, kein Panic {#go-silent-wraparound-no-panic}

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

## Korrigierte Muster {#fixed-patterns}

### C — sichere Multiplikation mit Überlaufprüfung {#c-safe-multiplication-with-overflow-check}

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

### Java — Math.addExact / multiplyExact {#java-mathaddexact-multiplyexact}

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

### Rust — geprüfte Arithmetik (explizite Überlaufbehandlung) {#rust-checked-arithmetic-explicit-overflow-handling}

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

### Go — explizite Vorprüfung auf Überlauf {#go-explicit-overflow-pre-check}

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

## Erkennungsheuristiken {#detection-heuristics}

**Auslöser für statische Analyse:**
- `malloc(a * b)` oder `calloc(a, b)`, wobei `a` oder `b` aus Benutzereingaben stammt, ohne vorherige Überlaufprüfung
- `new T[user_value]` oder `make([]T, user_value)` ohne Grenzprüfung
- Arithmetik mit benutzerkontrollierten Werten vor einem Array-Zugriff: `arr[user_a + user_b]`
- Verengender Cast eines Benutzerwerts: `(int)userLong`, `(uint8_t)userInt`, `(short)userInt`
- Vergleich mit gemischtem Vorzeichen: `if (signed_var < unsigned_constant)` — implizite Typanpassung kann die Logik umkehren
- Java: `int result = (int)(userLong * constant)` ohne `Math.multiplyExact`

**Auslöser nach Folge:**
- Zu kleine Allokation: Ergebnis der Arithmetik wird als Allokationsgröße verwendet
- Index außerhalb der Grenzen: Ergebnis der Arithmetik wird als Array-Index verwendet
- Umgehung einer Sicherheitsprüfung: Ergebnis der Arithmetik wird in `if (value < threshold)` oder `if (value == expected)` verwendet
- Finanzberechnung: Arithmetik mit Geldbeträgen, bei denen negative Ergebnisse möglich sind

**Indikatoren für Fehlalarme:**
- Multiplikation, bei der beide Operanden Compile-Zeit-Konstanten oder Enum-Werte mit bekanntem Wertebereich sind
- Benutzerwert wurde vor der Arithmetik bereits gegen ein Maximum geprüft: `if (n > 1000) return error; buf = malloc(n * 8);` — sicher, sofern `1000 * 8 < SIZE_MAX`
- Rust-Code, der `wrapping_add`/`wrapping_mul` absichtlich verwendet (z. B. Hashfunktionen, Prüfsummen) — der Wraparound ist hier das beabsichtigte Verhalten
- Go-Code, der mit Werten arbeitet, die durch vorherige Validierung begrenzt sind

## Compiler-Schutzmaßnahmen {#compiler-mitigations}

| Maßnahme | Wirkung | Kosten |
|---|---|---|
| `-ftrapv` (GCC/Clang) | Löst zur Laufzeit bei vorzeichenbehaftetem Überlauf eine Falle aus | 5–30 % Leistungseinbuße |
| `-fsanitize=integer` (UBSan) | Erkennt Ganzzahloperationen mit UB | Nur zum Testen |
| `FORTIFY_SOURCE=2` | Härtet Standardbibliotheksfunktionen für Strings und Speicher | Minimal |
| Java `-ea` (Assertions) | Aktiviert Assertion-Prüfungen; Verwendung z. B. `assert Math.multiplyExact(a,b) > 0` | Nur zum Testen |
| Rust-Debug-Builds | Panic bei Überlauf | Standardmäßig nur im Debug-Build |
| Rust `overflow-checks = true` in Cargo.toml | Panic bei Überlauf auch im Release-Build | ca. 5–10 % Leistungseinbuße |

## Fallstricke {#gotchas}

- **Vorzeichenbehafteter Überlauf ist in C/C++ undefiniertes Verhalten, kein Wraparound.** Optimierungsdurchläufe des Compilers (besonders Schwächung von Schleifenoperationen) nutzen die Annahme aus, dass vorzeichenbehafteter Überlauf nie auftritt. Code wie `if (i + 1 < i) { handle_overflow(); }` kann vollständig wegoptimiert werden, weil der Compiler annimmt, dass `i + 1 < i` immer falsch ist (vorzeichenbehafteter Überlauf → UB → Bedingung ist laut Compiler stets falsch). Mit `-fwrapv` wird vorzeichenbehafteter Überlauf als Wraparound behandelt; alternativ kann man vorzeichenlose Arithmetik mit expliziten Prüfungen verwenden.
- **calloc vs. malloc:** `calloc(count, size)` führt die Überlaufprüfung auf den meisten Plattformen intern durch. `malloc(count * size)` tut dies nicht. In C sollte für Array-Allokationen `calloc` bevorzugt werden.
- **Die Größe von `int` in Go ist plattformabhängig:** `int` ist auf 32-Bit-Plattformen 32 Bit breit, auf 64-Bit-Plattformen 64 Bit. Code, der auf 64-Bit-Entwicklungsrechnern die Überlaufprüfungen besteht, kann auf 32-Bit-Zielsystemen oder älteren ARM-Geräten überlaufen.
- **Rust im Release-Modus wraps standardmäßig stillschweigend.** Viele Rust-Entwickler gehen davon aus, dass Überläufe überall zu einem Panic führen, weil dies im Debug-Modus so ist. Sicherheitskritischer Rust-Code muss `checked_*`-Operationen verwenden oder `overflow-checks = true` in `Cargo.toml` aktivieren.
- **Finanzarithmetik erfordert Ganzzahlen beliebiger Genauigkeit oder Dezimaltypen.** `float64` hat 15–17 signifikante Dezimalstellen, akkumuliert aber Rundungsfehler. Für Geldberechnungen sollten in Go `big.Int`/`big.Float`, in Python `decimal.Decimal` und in Java `BigDecimal` verwendet werden. Ganzzahlüberläufe im Finanzcode können zu falschen Kontoständen führen, nicht nur zu Abstürzen.

## Siehe auch {#see-also}

- CWE-787: Schreiben außerhalb der Grenzen — häufigste Folge einer durch Überlauf zu klein dimensionierten Allokation
- CWE-125: Lesen außerhalb der Grenzen — Indexüberlauf führt zum Lesen über das Pufferende hinaus
- CWE-369: Division durch null — verwandter Arithmetikfehler; vom Angreifer kontrollierter Divisor = 0
- CWE-020: Eingabevalidierung — vorgelagerte Kontrolle: numerische Wertebereiche vor der Arithmetik validieren
