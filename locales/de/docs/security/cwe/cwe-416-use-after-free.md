---
description: "CWE-416: Use After Free – Zugriff auf freigegebenen Speicher ermöglicht RCE, Informationsabfluss und DoS. Dangling Pointer, Double-Free, Iterator-Invalidierung, Race Conditions bei free/Nutzung."
date: 2026-04-16
tags: [security, cwe, memory-corruption, use-after-free, c, cpp, rust]
level: Advanced
source_sha256: 7e5d04770fa0794fc1e05ca2ad28e1d119a9de7162e2d01984516a42cbcfdef8
translation: machine
translated_at: '2026-10-24'
---
# CWE-416: Use After Free {#cwe-416-use-after-free}

**CWE Top 25 Rank:** 8 (2024). Seit 2019 durchgehend in den Top 10. 
**Schweregrad:** CVSS 7.0–10.0. Die meisten Browser-RCEs (V8, WebKit, Firefox) sind UAF-Exploits.
**Grundmechanismus:** Der Speichermanager verwendet eine freigegebene Allokation erneut; das Programm greift über einen veralteten Zeiger zu; eine vom Angreifer kontrollierte Allokation belegt zuerst den freigegebenen Bereich.

---

## Funktionale Semantik {#functional-semantics}

Nach `free(ptr)` gibt der Allocator den Speicher an den Heap zurück. Der Allocator kann diesen Bereich sofort für einen nachfolgenden `malloc()`-Aufruf wiederverwenden. Hält das Programm weiterhin einen Zeiger auf den freigegebenen Bereich und greift darauf zu, gilt:

- **Lesen:** liefert vom Angreifer beeinflusste Daten, falls der Allocator den Bereich wiederverwendet hat.
- **Schreiben:** überschreibt die vom Angreifer kontrollierte Allokation mit Programmdaten.
- **Ausführen (Funktionszeiger/vtable):** springt zu einer vom Angreifer kontrollierten Adresse.

**Heap Grooming / Type-Confusion-Angriff:**
```text
free(victim_object)      → allocator marks region free
malloc(attacker_size)    → if sizes match, region is reused for attacker allocation
attacker writes          → fills region with crafted data (fake vtable, fake object)
program uses victim_ptr  → reads/calls attacker's data as if it were victim_object
```

Moderne Allocator (tcmalloc, jemalloc, PartitionAlloc) unterteilen nach Größenklassen und enthalten Sicherheitshärtungen, UAF bleibt jedoch über kontrollierte Allokationsfolgen ausnutzbar.

---

## Grundursachen {#root-causes}

### 1. Dangling Pointer nach free {#1-dangling-pointer-after-free}

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

**Hinweis:** Das Nullsetzen des Zeigers verhindert einen UAF über genau diesen Zeiger, nicht jedoch über *Aliase* (weitere Zeiger auf dieselbe Allokation). Aliasing ist der schwierige Fall.

### 2. Double-Free {#2-double-free}

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

Double-Free wird in modernen Allocatorn (mit tcache-Double-Free-Erkennung) möglicherweise mit „double free detected in tcache 2“ abgebrochen. Bei älteren Allocatorn oder mit Bypass-Techniken handelt es sich um eine ausnutzbare Heap-Korruption.

### 3. C++ Iterator-Invalidierung {#3-c-iterator-invalidation}

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

**STL-Container, die Iteratoren bei Mutation invalidieren:**
- `std::vector`: insert/erase/push_back (Reallokation) invalidiert alle Iteratoren
- `std::deque`: insert/erase in der Mitte invalidiert alle; an den Enden werden einige invalidiert
- `std::unordered_map`/`unordered_set`: Rehashing invalidiert alle Iteratoren
- `std::list`/`std::map`/`std::set`: nur Iteratoren auf gelöschte Elemente werden invalidiert

### 4. Event-Handler/Callback greift auf freigegebenes Objekt zu {#4-event-handler-callback-accessing-freed-object}

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

### 5. Race Condition: free in einem Thread, Nutzung in einem anderen {#5-race-condition-free-in-one-thread-use-in-another}

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

### 6. UAF in Rust-`unsafe` {#6-rust-unsafe-uaf}

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

## Betroffene Ökosysteme {#affected-ecosystems}

| Sprache | Risiko | Hinweise |
|----------|------|-------|
| C | Kritisch | Manuelle Speicherverwaltung, keine Lebensdauerverfolgung |
| C++ | Kritisch | `delete` + Rohzeiger; Smart Pointer mindern das Risiko bei konsequenter Verwendung |
| C++ (Smart Pointer) | Mittel | `shared_ptr`-Zyklen verhindern die Freigabe; Fehlgebrauch von `weak_ptr` → Dangling |
| Rust (sicher) | Keines | Der Borrow Checker verhindert UAF zur Kompilierzeit |
| Rust (unsafe) | Hoch | Rohzeiger-Operationen umgehen den Borrow Checker |
| Go | Sehr gering | GC verhindert UAF bei GC-verwalteten Objekten; `unsafe.Pointer` kann UAF verursachen |
| Java/Python/JS | Sehr gering | GC verhindert UAF; Logikfehler sind möglich, aber keine UAF auf Speicherebene |

---

## Erkennungsheuristiken {#detection-heuristics}

**In C/C++:**

1. `free(ptr)`, gefolgt von einem Lese-, Schreib- oder Aufrufzugriff über `ptr` oder einen Alias, ohne dazwischenliegendes `ptr = NULL`.
2. Suche nach `free(ptr)` in Funktionen, die `ptr` zurückgeben oder `ptr` vor dem Freigeben an anderer Stelle speichern – mehrfache Eigentümerschaft.
3. Destruktormuster, bei denen ein Zeiger in mehreren Strukturen gespeichert wird: `A.ptr = p; B.ptr = p; delete p;` – `B.ptr` ist nun ein Dangling Pointer.
4. Event-System-Muster: `subscribe(lambda capturing raw pointer)` ohne entsprechendes `unsubscribe` im Destruktor des Zielobjekts.
5. Während der Iteration modifizierte Container: Range-for-Schleifen mit `erase`, `insert`, `push_back` auf dem iterierten Container.
6. Multithreaded-Code: `free()` in einer Funktion, Nutzung in einer anderen, ohne Synchronisation des Zeigers.

**Statische Analysewerkzeuge:**
- Clang `scan-build` mit `alpha.cplusplus.STLAlgorithmModeling`
- Cppcheck: `--enable=warning` erkennt offensichtliche UAF
- Coverity: Checker „USE_AFTER_FREE“
- CodeQL: `cpp/use-after-free`
- Valgrind `memcheck`: Erkennung zur Laufzeit mit Heap-Historie

**Dynamische Erkennung:**
- `-fsanitize=address` (ASan): erkennt UAF zur Laufzeit; meldet die genauen Orte von Allokation, Freigabe und Zugriff
- libdislocator (AFL): randomisiert Allokationen, damit UAF beim Fuzzing wahrscheinlicher abstürzt

---

## Ausnutzungsmuster {#exploitation-patterns}

| Exploit-Typ | Mechanismus |
|-------------|-----------|
| Type Confusion über UAF | Heap Grooming: Freigegebenen Bereich mit anderem Typ belegen; der ursprüngliche Code liest ihn als ursprünglichen Typ → kontrollierte Feldwerte |
| Überschreiben der Virtual Function Table (vtable) | Objekt mit vtable wird freigegeben; neue Allokation an derselben Adresse; Angreifer kontrolliert den vtable-Zeiger → beliebiger virtueller Aufruf |
| Überschreiben von Funktionszeigern | Struktur mit Funktionszeiger freigeben; mit präparierter Struktur füllen; Code ruft den Funktionszeiger auf → PC-Kontrolle |
| Info Leak über UAF-Lesezugriff | Freigegebenen Bereich lesen, der sensible Daten einer benachbarten Allokation enthält |
| Double-Free zu beliebigem Schreibzugriff | Zwei Freigaben → Korruption der Heap-Metadaten → kontrollierter `malloc`-Rückgabewert → Schreib-Primitive |

---

## Behebungsmuster {#fixing-patterns}

| Muster | Anwendung |
|---------|-------------|
| Zeiger nach free nullen | `free(p); p = NULL;` – verhindert Zugriff über genau diesen Zeiger |
| `std::unique_ptr` / `std::shared_ptr` | Eigentümersemantik verhindert die meisten UAF-Muster in C++ |
| Referenzzählung | `shared_ptr`, eigener atomarer Referenzzähler; Freigabe erst bei Zähler == 0 |
| RAII + scope-gebundene Lebensdauern | Ressourcenlebensdauer an den Gültigkeitsbereich gebunden; keine manuelle Freigabe |
| `std::weak_ptr` für Rückverweise | Nicht besitzende Referenz, die abläuft, wenn das besessene Objekt zerstört wird |
| Epochenbasierte Speicherrückgewinnung (RCU) | Verzögerte Freigabe, bis alle Leser fertig sind; üblich in Kernel- und nebenläufigem Code |
| Address Sanitizer in CI | Erkennt UAF zur Laufzeit; unverzichtbar für C/C++-Testsuiten |
| Fuzzing mit ASan | AFL++/libFuzzer + ASan ist die primäre Entdeckungsmethode für UAF in Browsern und Parsern |

---

## Stolpersteine – Indikatoren für Fehlalarme {#gotchas-false-positive-indicators}

- **`free(p); p = malloc(new_size);`** – Zeiger wird im selben Gültigkeitsbereich für eine neue Allokation wiederverwendet; kein UAF, sofern kein dazwischenliegender Zugriff auf den alten Wert erfolgt.
- **Extraktion des Rohzeigers aus Smart Pointern für Interop:** `p.get()` wird an eine C-API übergeben, die keine Eigentümerschaft übernimmt – sicher, solange der `unique_ptr`/`shared_ptr`-Eigentümer den Aufruf der C-API überlebt.
- **`shared_ptr` an Lambda übergeben:** Das Lambda erfasst eine Kopie des `shared_ptr` und verlängert damit die Lebensdauer; das Ziel wird erst freigegeben, wenn das Lambda zerstört wird – kein UAF.
- **Pool-Allokatoren:** `free` gibt in einem Pool-Kontext Speicher an den Pool zurück, nicht an das Betriebssystem; eine spätere „Nutzung“ liest Pool-verwalteten Speicher, der noch nicht durch eine andere Allokation überschrieben wurde. Technisch ein UAF, oft aber ohne Pool-Grooming nicht ausnutzbar.
- **`std::vector`-Reallokation:** `vec.push_back(x)` kann reallokieren; Referenzen, Iteratoren und Zeiger in den alten Speicher des Vektors werden invalidiert. Dies ist jedoch eine eigene Fehlerklasse (Dangling Iterator/Referenz, nicht UAF im klassischen Sinn eines Zeigers).

---

## Siehe auch {#see-also}

- [[cwe-787-oob-write]] – häufig verkettet: UAF-Lesezugriff leakt eine Adresse, OOB-Schreibzugriff nutzt sie aus
- CWE-125: Out-of-Bounds Read – Speicherfehler auf der Leseseite; UAF-Lesezugriff ist eine Unterklasse
- CWE-415: Double Free – direkter Untertyp; Double-Free → Heap-Korruption → Auswirkung vergleichbar mit UAF
- CWE-362: Race Condition – nebenläufige UAF-Grundursache
- CWE-672: Operation On Resource After Expiration – semantisches Oberkonzept für den Zugriff auf abgelaufene Ressourcen
