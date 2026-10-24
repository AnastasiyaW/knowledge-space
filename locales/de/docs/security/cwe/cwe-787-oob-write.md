---
description: "CWE-787: Out-of-Bounds Write - Speicherkorruption durch Schreibzugriffe über Puffergrenzen hinweg. Grundursachen, Erkennungsheuristiken, Ausnutzbarkeitsfaktoren und Korrekturmuster."
date: 2026-04-16
tags: [security, cwe, memory-corruption, buffer-overflow, c, cpp, rust]
level: Advanced
source_sha256: 13a326398df3cff31ce6d13423735f18bdb93338fdbfc28898f31505fdf40f17
translation: machine
translated_at: '2026-10-24'
---
# CWE-787: Out-of-Bounds Write {#cwe-787-out-of-bounds-write}

**CWE Top 25 Rang:** 2 (2024). Seit 2019 durchgehend in den Top 3.
**CVSS-Muster:** typischerweise 7.5–10.0. Heap-OOB-Write ist in modernen Exploits ein Primitiv zur Codeausführung.

---

## Funktionale Semantik {#functional-semantics}

Eine Schreiboperation zielt auf die Speicheradresse `base + offset`, wobei `offset >= allocated_size` gilt. Der Schreibzugriff landet im benachbarten Speicher: in den Metadaten eines anderen Heap-Chunks, in der Rücksprungadresse eines Stack-Frames oder in einer globalen Variable. Die Semantik lautet: Das Programm glaubt, in die eigenen Daten zu schreiben; die CPU führt den Schreibzugriff ohne Fehler aus; der Prozesszustand wird stillschweigend korrumpiert.

Dies unterscheidet sich von einem Segmentation Fault, der nur auftritt, wenn die Zieladresse nicht gemappt ist. OOB-Writes innerhalb derselben Allokationsarena gelingen stillschweigend.

**Konsequenzkette:**
```text
OOB write → corrupt adjacent data
           → if metadata (heap chunk header): heap corruption → malloc/free crash or controlled allocation
           → if return address (stack): control flow hijack
           → if vtable pointer: type confusion → arbitrary virtual dispatch
           → if adjacent buffer: data corruption, logic errors, secondary vulnerabilities
```

---

## Grundursachen {#root-causes}

### 1. Off-by-one in Schleifengrenzen {#1-off-by-one-in-loop-bounds}

```c
// VULNERABLE: writes index n into buffer of size n
void copy_path(char *dst, const char *src, size_t n) {
    size_t i;
    for (i = 0; i <= n; i++) {   // <= should be <
        dst[i] = src[i];
    }
}
```

`dst[n]` schreibt ein Byte über das Ende der Allokation hinaus. Auf dem Stack überschreibt dies die nächste lokale Variable oder den gesicherten Frame-Pointer.

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

### 2. Integer-Überlauf bei der Größenberechnung {#2-integer-overflow-in-size-calculation}

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

### 3. Ungebundenes String-Kopieren {#3-unbounded-string-copy}

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

### 4. Rust-`unsafe`-Slice-Indizierung {#4-rust-unsafe-slice-indexing}

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

## Auslösebedingungen {#trigger-conditions}

| Bedingung | Mechanismus |
|-----------|-------------|
| Externe Eingabe steuert den Array-Index | Direkte Index-Injektion |
| Externe Eingabe steuert die Allokationsgröße | Integer-Überlauf in `n * sizeof(T)` |
| Externe Eingabe steuert die Schleifengrenze | Off-by-one über manipuliertes Längenfeld |
| Netzwerk- oder dateibasiertes Längenfeld < tatsächliche Daten | Schreibzugriff über eine abgeschnittene Allokation hinaus |
| Vorzeichen-/Vorzeichenlos-Konflikt im Index | Negativer Index wird zu großem positivem Wert |

**Beispiel für Vorzeichen-/Vorzeichenlos-Konflikt:**

```c
// VULNERABLE: signed comparison with unsigned loop variable
int8_t index = get_user_index();  // attacker sends -1
if (index < MAX_ITEMS) {           // -1 < 10 → true
    table[index] = value;          // table[-1] = write before array
}
```

---

## Betroffene Ökosysteme {#affected-ecosystems}

| Sprache | Risiko | Anmerkungen |
|---------|--------|-------------|
| C | Kritisch | Standardmäßig keine Bounds-Prüfung in der Standardbibliothek |
| C++ | Kritisch | STL-`operator[]` ungeprüft; `.at()` wirft eine Exception, wird aber selten verwendet |
| Rust (sicher) | Keines | Panic bei OOB zur Laufzeit |
| Rust (unsicher) | Hoch | `ptr::write` und `slice::from_raw_parts_mut` haben keine Prüfungen |
| Go | Niedrig | Laufzeit-Panic bei OOB-Slice-Schreibzugriffen; `unsafe.Pointer`-Arithmetik umgeht dies |
| Java/Python/JS | Sehr niedrig | Verwaltete Laufzeiten; Array-OOB führt zu einer Exception, nicht zur Korruption |
| Assembler | Kritisch | Kein Laufzeitschutz |

---

## Erkennungsheuristiken {#detection-heuristics}

**Signalstarke Muster (sofort prüfen):**

1. `memcpy(dst, src, len)`, bei dem `len` aus externer Eingabe stammt und unmittelbar davor kein Guard `len <= sizeof(dst)` steht.
2. `strcpy`, `strcat`, `gets`, `sprintf` (ohne `n`-Varianten) – als automatischer Befund behandeln.
3. Array-Subskript `arr[i]`, bei dem `i` vom Typ `int` oder `size_t` ist und aus einer Netzwerk-, Datei- oder IPC-Quelle stammt.
4. `malloc(a * b)` oder `malloc(a + b)`, wobei einer der Operanden externe Eingabe ist – Überlauf möglich.
5. Zeigerarithmetik `ptr + offset`, bei der `offset` extern ist und keine Prüfung `ptr + offset < ptr + alloc_size` existiert.
6. `for (i = 0; i <= len; i++)` – Off-by-one; `<=` sollte fast immer `<` sein.

**Anker für statische Analyse:**
- Taint: Quelle = `read()`, `recv()`, `fread()`, `getenv()`, `argv[]`
- Senke: `memcpy dst`, `strcpy dst`, Schreibzugriff über Array-Subskript, Schreibzugriff über Zeiger-Dereferenzierung
- Prüfung: Wird der Taint auf allen Pfaden zwischen Quelle und Senke bereinigt (Bounds-geprüft)?

---

## Ausnutzbarkeitsfaktoren {#exploitability-factors}

| Faktor | Auswirkung auf die Ausnutzbarkeit |
|--------|-----------------------------------|
| Heap-OOB vs. Stack-OOB | Heap: Umgehung von ASLR/PIE nötig; Stack: oft direkte Kontrolle über RIP/EIP |
| Schreibgröße | 1 Byte (Off-by-one): schwierig, aber möglich (House of Einherjar); beliebig: unkompliziert |
| Benachbarte Daten | Hinsichtlich Kontrollierbarkeit: Heap-Metadaten > vtable-Pointer > Rücksprungadresse |
| ASLR/PIE aktiviert | Erhöht den Aufwand; ein Information Leak (CWE-125) wird typischerweise zur Umgehung genutzt |
| Stack-Canaries | Erkennen Stack-Buffer-Overflows vor dem Rücksprung; Heap-OOB bleibt unberührt |

---

## Korrekturmuster {#fixing-patterns}

| Muster | Anwendung |
|--------|-----------|
| `n`-begrenzte Funktionen verwenden | `strncpy`, `snprintf`, `strncat`, `fgets` statt unbegrenzter Entsprechungen |
| `calloc` für Array-Allokation | Behandelt die Überlaufprüfung von `nmemb * size` gemäß C11 |
| Explizite Vorbedingungsprüfung | `assert(offset + len <= buf_size)` oder `if`-Guard mit Fehlerrückgabe |
| Address Sanitizer (ASan) in Tests | `-fsanitize=address` erkennt OOB zur Laufzeit in Testsuiten |
| Fortify Source | `-D_FORTIFY_SOURCE=2` ergänzt Prüfungen zur Compile- und Laufzeit für String-Funktionen |
| Statische Analyse | Coverity, CodeQL `cpp/overflow-buffer`, PVS-Studio V531, Semgrep `c.lang.security.buffer-not-null-terminated` |
| Sichere Wrapper | `strlcpy`/`strlcat` (OpenBSD), `memcpy_s` (C11 Annex K) |

---

## Fallstricke – Indikatoren für Fehlalarme {#gotchas-false-positive-indicators}

- **Ringpuffer mit Modulo:** `buf[i % SIZE]` – immer innerhalb der Grenzen, wenn `SIZE` exakt `sizeof(buf)/sizeof(buf[0])` entspricht. Prüfen, ob der Modulus genau der Allokationsgröße entspricht.
- **Sentinel-terminiertes Kopieren:** `while (*src) dst[i++] = *src++;` – wirkt gefährlich, aber der Aufrufer könnte `strlen(src) < sizeof(dst)` garantieren. Vertrag an der Aufrufstelle prüfen.
- **Lokale Stack-Variable fester Größe mit sizeof-Guard:** `memcpy(local, src, sizeof(local))`, wobei `local` ein festes Stack-Array ist – dies ist sicher, da `sizeof` die Größe zur Compile-Zeit liefert.
- **Zweiphasige Allokation und Befüllung:** `malloc(n)` gefolgt von `memset(p, 0, n)` mit demselben `n` – sicher; das typische gefährliche Muster liegt vor, wenn die Befüllung ein *anderes* `n` als die Allokation verwendet.
- **Vom Compiler eingefügte Array-Größe:** GCC/Clang `-Warray-bounds` erkennt manche, aber nicht dynamische Fälle; das Fehlen einer Warnung bedeutet nicht das Fehlen eines Bugs.

---

## Siehe auch {#see-also}

- CWE-125: Out-of-Bounds Read – lesende Entsprechung; wird bei Heartbleed-artigen Bugs häufig zusammen genannt
- CWE-416: Use After Free – weitere Klasse von Speicherkorruption; wird oft mit OOB-Writes verkettet
- CWE-190: Integer Overflow – Grundursache für OOB-Writes durch Größenberechnung
- CWE-119: Buffer Errors – übergeordnete CWE
- CWE-121: Stack Overflow – Untertyp für den Stack
- CWE-122: Heap Overflow – Untertyp für den Heap
